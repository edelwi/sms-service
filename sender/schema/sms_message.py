from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import UUID


class SMSMessageBase(BaseModel):
    mobile: Optional[str] = Field(
        "",
        description="recipient's mobile phone number",
        index=True,
    )
    message_text: Optional[str] = Field("", description="short message")
    is_sent: Optional[bool] = Field(False, description="sending status")


# Properties to receive on SMSMessage creation
class SMSMessageCreate(BaseModel):
    message_id: UUID = Field(..., description="message uuid", index=True)
    mobile: str = Field(
        ...,
        description="recipient's mobile phone number",
        index=True,
    )
    message_text: str = Field(..., description="short message")


# Properties to receive on SMSMessage update
class SMSMessageUpdate(SMSMessageBase):
    pass


# Properties shared by models stored in DB
class SMSMessageInDBBase(SMSMessageBase):
    pk: str

    # class Config:
    #     orm_mode = True


# Properties to return to client
class SMSMessage(SMSMessageInDBBase):
    pass


# Properties  stored in DB
class SMSMessageInDB(SMSMessageInDBBase):
    pass
