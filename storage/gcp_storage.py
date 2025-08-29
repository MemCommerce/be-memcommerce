from uuid import uuid4
from tempfile import TemporaryDirectory
from os import getenv

from google.oauth2 import service_account
from google.cloud.storage import Client
from google.cloud.storage.blob import Blob
from google.cloud.exceptions import NotFound
from datetime import datetime, timedelta, UTC

from config import BUCKET_NAME, SA_KEY_PATH
from cache.client import redis_client


def get_gcs_client() -> Client:
    if sa_credentials := getenv("SA_CREDENTIALS"):
        from json import loads
        credentials = service_account.Credentials.from_service_account_info(loads(sa_credentials))
        client = Client(credentials=credentials)
    else:
        credentials = service_account.Credentials.from_service_account_file(SA_KEY_PATH)
        client = Client(credentials=credentials)

    return client


client = get_gcs_client()


def upload_bytes_image(
    image_bytes: bytes, image_extension: str = ".webp", content_type: str = "image/webp"
) -> str:
    file_name = f"{uuid4()}{image_extension}"

    with TemporaryDirectory() as temp_dir:
        temp_file_path = f"{temp_dir}/{file_name}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(image_bytes)

        bucket = client.get_bucket(BUCKET_NAME)

        blob = bucket.blob(file_name)
        blob.upload_from_filename(temp_file_path, content_type=content_type)

    return file_name


async def generate_signed_url(file_name: str, expiration_days: int = 6) -> str:
    try:
        cache_key = f"signed_url:{file_name}:{expiration_days}"
        import time
        start = time.time()
        cached_url = await redis_client.get(cache_key)
        end = time.time()

        print(f"Cache get took {end - start}")
        if cached_url:
            return cached_url

        bucket = client.bucket(BUCKET_NAME)
        blob = Blob(file_name, bucket)

        expiration_time = datetime.now(UTC) + timedelta(days=expiration_days)
        # TODO make this async somehow
        signed_url = blob.generate_signed_url(
            version="v4", expiration=expiration_time, method="GET"
        )

        await redis_client.set(cache_key, signed_url, ex=expiration_days * 86400)

        return signed_url
    except Exception as e:
        print(f"Error generating signed URL: {e}")
        return ""


def delete_blob_by_file_name(file_name: str) -> None:
    try:
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.delete()
        print(f"Deleted {file_name} from storage")
    except NotFound:
        print(f"{file_name} not found in storage")
