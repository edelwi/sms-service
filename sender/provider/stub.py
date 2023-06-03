import dataclasses
import logging
import uuid
from typing import Any
from pydantic import BaseModel, Field
from sender.core import (
    SMSSenderCreator,
    SomeSMSSender,
    SendStatus,
)

log = logging.getLogger()


@dataclasses
class StubSendStatus:
    response_text: str
    status_code: int
    ipaddress: str

    @property
    def status(self) -> Any:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class StubMessageFormat(BaseModel):
    mobile: str = Field(
        ...,
        description="Mobile number",
    )
    message: str = Field(
        ..., description="SMS message", example="Hi!", min_length=1, max_length=1000
    )


class StubSMSSenderCreator(SMSSenderCreator):
    def factory_method(self, **kwargs) -> SomeSMSSender:
        return StubSMSSender(**kwargs)


class StubSMSSender:
    def __init__(
        self,
        api_url: str,
        api_client_login: str,
        api_client_password: str,
        from_label: str,
        callback_url: str,
    ):
        self._api_url = api_url
        self._api_client_login = api_client_login
        self._api_client_password = api_client_password
        self._sms_from = from_label
        self._callback_url = callback_url

    def send_sms(
        self,
        mobile: str,
        message: str,
    ) -> SendStatus:

        short_message = StubMessageFormat(
            mobile=mobile, message=message
        )  # can raise ValueError
        payload = {
            "from": self._sms_from,
            "to": int(short_message.mobile),
            "message": short_message.message,
            "callback_url": self._callback_url,
            "msg_id": str(uuid.uuid4())[:16],
        }
        log.info(f"Stub send payload: {payload}")

        return StubSendStatus(response_text="Ok", status_code=200, ipaddress="0.0.0.0")
