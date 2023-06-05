from config import settings
from sender.crud.base import CRUDBase
from sender.model.message_status import MessageStatus
from sender.schema.message_status import MessageStatusCreate, MessageStatusUpdate


class CRUDMessageStatus(
    CRUDBase[MessageStatus, MessageStatusCreate, MessageStatusUpdate]
):
    pass


message_status_crud = CRUDMessageStatus(
    MessageStatus, ttl_second=settings.REDIS_STORAGE_MESSAGE_STATUS_TTL_SECONDS
)
