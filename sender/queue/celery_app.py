import logging

from celery import Celery

from config import settings
from sender.core import sender_initializer
from sender.provider.stub import StubSMSSenderCreator

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


@celery_app.task(rate_limit=settings.PVR_RATE_LIMIT_MPS, ignore_result=True)
def send_sms(
    mobile: str,
    message: str,
) -> None:
    return smser.send_sms(mobile=mobile, message=message)
