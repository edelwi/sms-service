from redis_om import get_redis_connection

from config import settings


def get_redis_db():
    return get_redis_connection(url=settings.REDIS_STORAGE_URL, decode_responses=True)
