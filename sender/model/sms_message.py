from typing import Optional

from pydantic import Field

from sender.model.base_class import Base


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
