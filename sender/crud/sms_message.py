from config import settings
from sender.crud.base import CRUDBase
from sender.model.sms_message import SMSMessage
from sender.schema.sms_message import SMSMessageCreate, SMSMessageUpdate


class CRUDSMSMessage(
    CRUDBase[SMSMessage, SMSMessageCreate, SMSMessageUpdate]
):
    pass


sms_message_crud = CRUDSMSMessage(
    SMSMessage, ttl_second=settings.REDIS_STORAGE_SMS_MESSAGE_TTL_SECONDS
)
