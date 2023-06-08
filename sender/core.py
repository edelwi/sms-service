from abc import abstractmethod, ABC
from typing import Any, Protocol


class SendStatus(Protocol):
    @property
    def status(self) -> Any:
        ...


class SomeSMSSender(Protocol):
    def send_sms(
        self,
        mobile: str,
        message: str,
        idempotency_key: str,
    ) -> SendStatus:
        ...


class SMSSenderCreator(ABC):
    @abstractmethod
    def factory_method(self) -> SomeSMSSender:
        pass

    def send_sms(self, mobile: str, message: str, idempotency_key: str) -> SendStatus:
        sender_obj = self.factory_method()
        return sender_obj.send_sms(mobile=mobile, message=message, idempotency_key=idempotency_key)


class ProviderError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class ProviderConnectionError(ProviderError):
    pass


class ProviderResponseError(ProviderError):
    pass


def sender_initializer(sender_obj: SMSSenderCreator):
    return sender_obj
