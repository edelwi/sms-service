from typing import Optional

from pydantic import Field

from config import settings
from sender.model.base_class import Base
from sender.model.redis_connector import get_redis_db


class SMSMessage(Base):
    """SMS message model"""
    message_id: str = Field(..., description="message uuid", index=True)
    mobile: str = Field(
        ...,
        description="recipient's mobile phone number",
        index=True,
    )
    message_text: str = Field(..., description="short message")
    is_sent: Optional[int] = Field(0, description="sending status", ge=0, le=1)

    # def __int__(self, **kwargs):
    #     print()
    #     super().__init__(**kwargs)
    #     self.__ttl = settings.REDIS_STORAGE_SMS_MESSAGE_TTL_SECONDS
    #     self.Meta.database = get_redis_db()
