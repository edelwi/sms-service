from typing import Optional

from pydantic import Field

from sender.model.base_class import Base, utcnow_isoformat


class DeliveryStatus(Base):
    """SMS delivery status model"""

    message_id: str = Field(..., description="message uuid", index=True)
    receipted_message_id: str = Field(
        ...,
        description="Message id received from SMSC",
    )
    status: str = Field(..., description="Delivery status")
    short_message: Optional[str] = Field(
        "",
        description="Delivery details.",
    )
    response_datetime: Optional[str] = Field(
        default_factory=utcnow_isoformat, description="response date and time"
    )
