import datetime
import hashlib
import uuid
from concurrent import futures

from redis_om import Migrator
from redis_om.model.migrations.migrator import IndexMigration, MigrationAction

from config import settings
from sender.grpc_stuff import sms_sender_pb2_grpc, sms_sender_pb2
from sender.model.delivery_status import DeliveryStatus
from sender.model.message_status import MessageStatus
from sender.model.redis_connector import get_redis_db
from sender.queue.celery_app import send_sms_by_pk
import grpc


import sender.model.sms_message as sms_message


class SMSServiceServicer(sms_sender_pb2_grpc.SMSServiceServicer):
    """Service to send SMS and get status"""

    def SendMessage(self, request, context):
        """Send message"""
        message_id = str(uuid.uuid4())
        message = sms_message.SMSMessage(
            message_id=message_id,
            mobile=request.mobile_number,
            message_text=request.message,
        )
        sms_message_obj = message.create(
            ttl_seconds=settings.REDIS_STORAGE_SMS_MESSAGE_TTL_SECONDS
        )
        # print(f"{sms_message_obj}")
        send_sms_by_pk.delay(pk=message.pk)
        return sms_sender_pb2.MessageID(uuid=str(message_id))

    def GetMessageStatus(self, request, context):
        """Get message status"""
        message_id = str(request.uuid)
        redis = get_redis_db()

        MessageStatus.Meta.database = redis
        # print(f"=== {redis=} {type(redis)=} {MessageStatus.Meta.index_name=}")
        #
        # schema = MessageStatus.redisearch_schema()
        # current_hash = hashlib.sha1(schema.encode("utf-8")).hexdigest()
        # IndexMigration(
        #     model_name="MessageStatus",
        #     index_name=MessageStatus.Meta.index_name,
        #     schema=schema,
        #     hash=current_hash,
        #     action=MigrationAction.CREATE,
        #     conn=redis,
        # ).run()
        # print(f"~~~ IndexMigration !!!")
        # Upff, .find does not work!
        # statuses = (
        #     MessageStatus.find(MessageStatus.message_id == message_id).all()
        #     # .sort_by("response_datetime")
        #     # .first()
        # )
        statuses = []
        for item in MessageStatus.all_pks():
            current_item = MessageStatus.get(item)
            if current_item.message_id == message_id:
                statuses.append(
                    sms_sender_pb2.MessageStatus(
                        description=current_item.description,
                        code=current_item.code,
                        ipaddress=current_item.ipaddress,
                        response_datetime=current_item.response_datetime,
                    )
                )
        sorted(statuses, key=lambda x: x.response_datetime)
        if not statuses:
            return sms_sender_pb2.MessageStatus(
                description="Dose not found.",
                code=-1,
                ipaddress="0.0.0.0",
                response_datetime=datetime.datetime.utcnow().isoformat(),
            )
        else:
            return statuses[-1]

    def GetDeliveryStatus(self, request, context):
        """Get message status"""
        message_id = str(request.uuid)
        redis = get_redis_db()

        DeliveryStatus.Meta.database = redis

        statuses = []
        for item in DeliveryStatus.all_pks():
            current_item = DeliveryStatus.get(item)
            if current_item.message_id == message_id:
                statuses.append(
                    sms_sender_pb2.DeliveryStatus(
                        message_id=message_id,
                        receipted_message_id=current_item.receipted_message_id,
                        status=current_item.status,
                        short_message=current_item.short_message,
                        response_datetime=current_item.response_datetime,
                    )
                )
        sorted(statuses, key=lambda x: x.response_datetime)
        if not statuses:
            return sms_sender_pb2.DeliveryStatus(
                message_id=message_id,
                receipted_message_id="",
                status="Delivery notification does not found.",
                short_message="",
                response_datetime=datetime.datetime.utcnow().isoformat(),
            )
        else:
            return statuses[-1]


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=settings.GRPC_MAX_WORKERS)
    )
    sms_sender_pb2_grpc.add_SMSServiceServicer_to_server(SMSServiceServicer(), server)
    server.add_insecure_port(f"[::]:{settings.GRPC_PORT}")
    server.start()
    server.wait_for_termination()
