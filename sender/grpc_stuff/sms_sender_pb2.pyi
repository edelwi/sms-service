from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DeliveryStatus(_message.Message):
    __slots__ = ["message_id", "receipted_message_id", "response_datetime", "short_message", "status"]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIPTED_MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    SHORT_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    receipted_message_id: str
    response_datetime: str
    short_message: str
    status: str
    def __init__(self, message_id: _Optional[str] = ..., receipted_message_id: _Optional[str] = ..., status: _Optional[str] = ..., short_message: _Optional[str] = ..., response_datetime: _Optional[str] = ...) -> None: ...

class MessageID(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class MessageStatus(_message.Message):
    __slots__ = ["code", "description", "ipaddress", "response_datetime"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IPADDRESS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_DATETIME_FIELD_NUMBER: _ClassVar[int]
    code: int
    description: str
    ipaddress: str
    response_datetime: str
    def __init__(self, description: _Optional[str] = ..., code: _Optional[int] = ..., ipaddress: _Optional[str] = ..., response_datetime: _Optional[str] = ...) -> None: ...

class SMSMessage(_message.Message):
    __slots__ = ["message", "mobile_number"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MOBILE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    message: str
    mobile_number: str
    def __init__(self, mobile_number: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
