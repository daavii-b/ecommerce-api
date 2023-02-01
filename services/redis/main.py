import os

from redis import Redis

redis: Redis = Redis.from_url(
    os.environ.get('REDIS_CACHE_LOCATION', 'redis://localhost:6379')
)
