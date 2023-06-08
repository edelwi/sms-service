import secrets
from functools import lru_cache

from pydantic import AnyHttpUrl, BaseSettings, Field


class Settings(BaseSettings):

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days

    CELERY_BROKER_URL: str
    CELERY_BACKEND_URL: str
    CELERY_TZ: str = "UTC"

    REDIS_STORAGE_URL: str
    # if < 0 no limits  # SMSMessage models
    REDIS_STORAGE_SMS_MESSAGE_TTL_SECONDS: int = 2 * 24 * 60 * 60
    # if < 0 no limits  # MessageStatus models
    REDIS_STORAGE_MESSAGE_STATUS_TTL_SECONDS: int = 4 * 24 * 60 * 60

    # Megafon SMA API
    PVR_API_URL: AnyHttpUrl = "https://a2p-api.megalabs.ru/sms/v1/sms"
    PVR_API_SMS_FROM: str = "Compashka"
    PVR_API_LOGIN: str = "login"
    PVR_API_PASSWORD: str = "password"
    PVR_CALLBACK_URL: str = "https://example.com/to_me"
    PVR_RATE_LIMIT_MPS: int = Field(5, gt=0)

    GRPC_MAX_WORKERS: int = 10
    GRPC_PORT: int = 50051

    class Config:
        case_sensitive = True
        env_file = ".env_demo"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()