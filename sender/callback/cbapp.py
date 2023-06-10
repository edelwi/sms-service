import redis
from fastapi import FastAPI, Response, Depends

from config import settings
from sender.callback import deps
from sender.model.delivery_status import DeliveryStatus
from sender.model.redis_connector import get_redis_db
from sender.provider.schema import megafon

app = FastAPI(
    title="sms-sender delivery api",
    openapi_url="/openapi.json",
    version="0.0.1",
)


@app.post(
    f"{settings.CALLBACK_ROUTE}",
    responses={
        200: {"description": "Ok."},
    },
    dependencies=[
        Depends(deps.is_granted_ip),
    ],
    response_class=Response,
)
def receive_delivery_status_from_provider(
    status: megafon.DeliveryMessage,
    db: redis.Redis = Depends(get_redis_db),
):
    DeliveryStatus.Meta.database = db
    delivery_status = DeliveryStatus(
        message_id=status.msg_id,
        receipted_message_id=status.receipted_message_id,
        status=status.status,
        short_message=status.short_message,
    )
    delivery_status.create(
        ttl_seconds=settings.REDIS_STORAGE_DELIVERY_STATUS_TTL_SECONDS
    )
    return Response(status_code=200)
