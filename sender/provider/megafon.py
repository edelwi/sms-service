import dataclasses
import logging
import string
import uuid
from typing import Any
from pydantic import BaseModel, Field, validator
import requests
from sender.core import (
    SMSSenderCreator,
    SomeSMSSender,
    SendStatus,
    ProviderConnectionError,
    ProviderResponseError,
)

log = logging.getLogger()


@dataclasses
class MegafonSendStatus:
    response_text: str
    status_code: int
    ipaddress: str

    @property
    def status(self) -> Any:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class MegafonMessageFormat(BaseModel):
    mobile: str = Field(
        ..., description="Mobile number", example="79001234567", min_length=11
    )
    message: str = Field(
        ..., description="SMS message", example="Hi!", min_length=1, max_length=1000
    )

    @validator("mobile")
    def mobile_reformat(cls, value) -> str:
        temp = "".join([_ for _ in value if _ in string.digits])
        if temp.startswith("8"):
            temp = "7" + temp[1:]
        if 11 < len(temp) > 15:
            raise ValueError("Invalid mobile phone format ")
        return temp


class MegafonSMSSenderCreator(SMSSenderCreator):
    def factory_method(self, **kwargs) -> SomeSMSSender:
        return MegafonSMSSender(**kwargs)


class MegafonSMSSender:
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

        short_message = MegafonMessageFormat(
            mobile=mobile, message=message
        )  # can raise ValueError
        payload = {
            "from": self._sms_from,
            "to": int(short_message.mobile),
            "message": short_message.message,
            "callback_url": self._callback_url,
            "msg_id": str(uuid.uuid4())[:16],
        }
        log.info(f"Send payload: {payload}")
        try:
            r = requests.post(
                self._api_url,
                json=payload,
                auth=requests.auth.HTTPBasicAuth(
                    self._api_client_login, self._api_client_password
                ),
                stream=True,
            )
        except requests.exceptions.ConnectionError as e:
            error_message = f"SMS API Server is not accessible. {e}"
            log.error(error_message)
            raise ProviderConnectionError(error_message)
        try:
            (ip, port) = r.raw._connection.sock.getpeername()
        except AttributeError:
            ip = "0.0.0.0"
        if r.status_code != 200:
            error_message = f"SMS API Server cannot complete the request. Code: {r.status_code} {r.text}"
            log.error(error_message)
            raise ProviderResponseError(error_message)
        return MegafonSendStatus(
            response_text=r.text, status_code=r.status_code, ipaddress=ip
        )
