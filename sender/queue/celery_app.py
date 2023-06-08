import logging
import random

from celery import Celery

from config import settings
from sender.core import sender_initializer
from sender.model.message_status import MessageStatus
from sender.model.redis_connector import get_redis_db
from sender.model.sms_message import SMSMessage
from sender.provider.stub import StubSMSSenderCreator, StubSMSSender

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BACKEND_URL,
)
celery_app.conf.broker_transport_options = {"visibility_timeout": 3600}
celery_app.conf.task_serializer = "pickle"
celery_app.conf.timezone = settings.CELERY_TZ
celery_app.conf.accept_content = ["json", "pickle"]

# celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
log = logging.getLogger(__name__)

smser = sender_initializer(StubSMSSenderCreator())


class WrongStateRepeatTask(Exception):
    pass


@celery_app.task(rate_limit=settings.PVR_RATE_LIMIT_MPS, ignore_result=True)
def send_sms(
    mobile: str,
    message: str,
) -> None:
    smser.send_sms(mobile=mobile, message=message)


@celery_app.task(
    rate_limit=settings.PVR_RATE_LIMIT_MPS,
    autoretry_for=(WrongStateRepeatTask,),
    retry_backoff=5,
    max_retries=11,
    retry_jitter=True,
    ignore_result=True,
)
def send_sms_by_pk(pk: str) -> None:
    SMSMessage.Meta.database = get_redis_db()
    message = SMSMessage.get(pk=pk)
    result = smser.send_sms(
        mobile=message.mobile,
        message=message.message_text,
        idempotency_key=message.message_id,
    )
    if result.status_code == 200:
        message.is_sent = 1
        message.save()
        print(f"SMS {type(smser)=}")
        if isinstance(smser, StubSMSSenderCreator):
            # run task that receive fake callback
            responses = (fake_response_ok, fake_response_fail)
            response_method = random.choice(responses)
            fake_response = response_method(message_id=message.message_id)
            fake_response.create(
                ttl_seconds=settings.REDIS_STORAGE_MESSAGE_STATUS_TTL_SECONDS
            )
        return
    raise WrongStateRepeatTask()


def fake_response_ok(message_id: str) -> MessageStatus:
    return MessageStatus(
        message_id=message_id, description="ok", code=0, ipaddress="127.0.0.1"
    )


def fake_response_fail(message_id: str) -> MessageStatus:
    return MessageStatus(
        message_id=message_id,
        description="Message ID is invalid",
        code=12,
        ipaddress="127.0.0.1",
    )
