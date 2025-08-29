import asyncio
from typing import Iterable, List, Dict

from cache.client import redis_client
from storage.gcp_storage import generate_signed_url


def _cache_key(file_name: str, expiration_days: int) -> str:
    # Include expiration in the key so different expiries don't collide
    return f"signed_url:{file_name}:{expiration_days}d"


async def get_signed_urls(
    image_names: Iterable[str],
    *,
    expiration_days: int = 5,
) -> List[str]:
    """
    Given a list of image names, return a list of signed URLs in the same order.
    First try Redis (one MGET), then generate missing ones, cache via one pipeline.
    """

    names: List[str] = list(image_names)
    keys: List[str] = [_cache_key(n, expiration_days) for n in names]

    # 1) One request to Redis to fetch all cached values
    cached_values: List[str | None] = await redis_client.mget(keys)

    # 2) Figure out which items are missing
    missing_indices: List[int] = [
        i for i, val in enumerate(cached_values) if val is None
    ]
    missing_names: List[str] = [names[i] for i in missing_indices]

    # 3) Generate signed URLs for the missing ones concurrently
    generated_urls: List[str] = []
    if missing_names:
        generated_urls = await asyncio.gather(
            *[
                generate_signed_url(name, expiration_days=expiration_days)
                for name in missing_names
            ]
        )

        # 4) Cache the newly generated URLs in one pipeline write
        ttl_seconds = expiration_days * 24 * 60 * 60
        async with redis_client.pipeline(transaction=False) as pipe:
            for name, url in zip(missing_names, generated_urls):
                pipe.set(_cache_key(name, expiration_days), url, ex=ttl_seconds)
            await pipe.execute()

    # 5) Merge cached + generated back in original order
    result: List[str] = list(cached_values)  # type: ignore
    for idx, url in zip(missing_indices, generated_urls):
        result[idx] = url

    # Defensive: if any generator returned empty/None, replace with ""
    return [r or "" for r in result]


async def get_signed_urls_as_dict(
    image_names: Iterable[str],
    *,
    expiration_days: int = 5,
) -> Dict[str, str]:
    """Same as above but returns a dict {image_name: signed_url}."""
    names = list(image_names)
    urls = await get_signed_urls(names, expiration_days=expiration_days)
    return dict(zip(names, urls))
