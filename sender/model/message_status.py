from typing import Optional

from pydantic import Field
from datetime import datetime

from config import settings
from sender.model.base_class import Base
from sender.model.redis_connector import get_redis_db


def utcnow_isoformat():
    return datetime.utcnow().isoformat()


class MessageStatus(Base):
    """SMS message status model"""

    message_id: str = Field(..., description="message uuid", index=True)
    description: str = Field(
        ...,
        description="status description",
    )
    code: int = Field(..., description="status code")
    ipaddress: str = Field(..., description="provider response node IP address")
    response_datetime: Optional[str] = Field(
        default_factory=utcnow_isoformat, description="response date and time"
    )

    # def __int__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.__ttl = settings.REDIS_STORAGE_MESSAGE_STATUS_TTL_SECONDS
    #     self.Meta.database = get_redis_db()