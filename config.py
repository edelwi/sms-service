import secrets
from functools import lru_cache

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days

    CELERY_BROKER_URL: str
    CELERY_BACKEND_URL: str

    REDIS_STORAGE_URL: str
    # if < 0 no limits  # SMSMessage models
    REDIS_STORAGE_MESSAGE_TTL_SECONDS: int = 2 * 24 * 60 * 60
    # if < 0 no limits  # MessageStatus models
    REDIS_STORAGE_STATUS_TTL_SECONDS: int = 4 * 24 * 60 * 60

    # Megafon SMA API
    MF_API_URL: AnyHttpUrl = "https://a2p-api.megalabs.ru/sms/v1/sms"
    MF_API_SMS_FROM: str = "Compashka"
    MF_API_LOGIN: str = ""
    MF_API_PASSWORD: str = ""
    MF_CALLBACK_URL: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env_demo"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()