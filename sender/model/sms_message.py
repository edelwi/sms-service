from typing import Optional

from pydantic import Field
from pydantic.types import UUID

from sender.model.base_class import Base


class SMSMessage(Base):
    """SMS message model"""
    message_id: UUID = Field(..., description="message uuid", index=True)
    mobile: str = Field(
        ...,
        description="recipient's mobile phone number",
        index=True,
    )
    message_text: str = Field(..., description="short message")
    is_sent: Optional[bool] = Field(False, description="sending status")
