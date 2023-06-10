from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Status(BaseModel):
    code: int = Field(..., description="Status code")
    description: Optional[str] = Field("", description="Status description")
    payload: Optional[str] = Field("", description="Details")


class Result(BaseModel):
    status: Status
    msg_id: Optional[str] = Field(
        "", description="Message ID", max_length=16
    )  # Megafon restriction


class Response(BaseModel):
    result: Result


class DeliveryStatus(str, Enum):
    delivered = "delivered"
    delivery_failed = "delivery_failed"


class DeliveryMessage(BaseModel):
    msg_id: str = Field(..., description="Message ID", regex="A-Za-z0-9_:-")
    receipted_message_id: str = (
        Field(..., description="Message id received from SMSC"),
    )
    status: DeliveryStatus = Field(..., description="Delivery status")
    short_message: Optional[str] = Field(
        "",
        description="Text with delivery result. Contains the "
        "value of the short_message field from "
        "the deliver_sm response from the SMSC.",
        example="id:917615ac sub:001 dlvrd:001 submit date:1701241159 done date:1701241159 stat:DELIVRD err:000"
    )
