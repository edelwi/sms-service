from sender.crud.base import CRUDBase
from sender.model.message_status import MessageStatus


class CRUDMessageStatus(CRUDBase[MessageStatus, MessageStatusCreate, MessageStatusUpdate]):
    pass