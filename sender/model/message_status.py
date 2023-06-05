from typing import Optional

from pydantic import Field
from pydantic.types import UUID
from datetime import datetime

from sender.model.base_class import Base


class MessageStatus(Base):
    """SMS message status model"""

    message_id: UUID = Field(..., description="message uuid", index=True)
    description: str = Field(
        ...,
        description="status description",
    )
    code: int = Field(..., description="status code")
    ipaddress: str = Field(..., description="provider response node IP address")
    response_datetime: Optional[datetime] = Field(
        default_factory=datetime.utcnow, description="response date and time"
    )
