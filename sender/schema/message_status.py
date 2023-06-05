from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import UUID


class MessageStatusBase(BaseModel):
    description: Optional[str] = Field(
        "",
        description="status description",
    )
    code: Optional[int] = Field(0, description="status code")
    ipaddress: Optional[str] = Field(
        "", description="provider response node IP address"
    )


# Properties to receive on MessageStatus creation
class MessageStatusCreate(BaseModel):
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


# Properties to receive on MessageStatus update
class MessageStatusUpdate(MessageStatusBase):
    pass


# Properties shared by models stored in DB
class MessageStatusInDBBase(MessageStatusBase):
    pk: str

    # class Config:
    #     orm_mode = True


# Properties to return to client
class MessageStatus(MessageStatusInDBBase):
    pass


# Properties  stored in DB
class MessageStatusInDB(MessageStatusInDBBase):
    pass
