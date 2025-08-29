from redis.asyncio import Redis

from config import REDIS_PORT, REDIS_HOST, REDIS_PASSWORD, REDIS_USERNAME

# TODO use connection pool in future
redis_client = Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    decode_responses=True,
    username=REDIS_USERNAME,
    password=REDIS_PASSWORD,
)
