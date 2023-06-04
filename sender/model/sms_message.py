from pydantic import Field
from pydantic.types import UUID
from redis_om import HashModel


class SMSMessage(HashModel):
    """SMS message model"""
    message_id: UUID = Field(..., description="message uuid", index=True)
    mobile: str = Field(
        ...,
        description="recipient's mobile phone number",
        index=True,
    )
    message_text: str = Field(..., description="short message")
    is_sent: bool = Field(False, description="sending status")
