from datetime import datetime
from typing import Optional

from pydantic import Field

from sender.model.base_class import Base, utcnow_isoformat


class MessageStatus(Base):
    """SMS message status model"""

    message_id: str = Field(..., description="message uuid", index=True)  #
    description: str = Field(
        ...,
        description="status description",
    )
    code: int = Field(..., description="status code")
    ipaddress: str = Field(..., description="provider response node IP address")
    response_datetime: Optional[str] = Field(
        default_factory=utcnow_isoformat, description="response date and time"
    )
