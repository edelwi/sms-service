from abc import abstractmethod, ABC
from typing import Optional, Dict, Any, Protocol


class SendStatus(Protocol):
    @property
    def status(self) -> Any:
        ...


class SomeSMSSender(Protocol):
    def send_sms(
        self,
        mobile: str,
        message: str,
    ) -> SendStatus:
        ...


class SMSSenderCreator(ABC):
    @abstractmethod
    def factory_method(self, **kwargs) -> SomeSMSSender:
        pass

    def send_sms(self, mobile: str, message: str, **kwargs) -> SendStatus:
        sender_obj = self.factory_method(**kwargs)
        return sender_obj.send_sms(mobile=mobile, message=message)


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