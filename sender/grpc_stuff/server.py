import uuid
from concurrent import futures

from config import settings
from sender.grpc_stuff import sms_sender_pb2_grpc, sms_sender_pb2
from sender.queue.celery_app import send_sms_by_pk
import grpc


import sender.model.sms_message as sms_message


class SMSServiceServicer(sms_sender_pb2_grpc.SMSServiceServicer):
    """Service to send SMS and get status
    """

    def SendMessage(self, request, context):
        """Send message
        """
        message_id = str(uuid.uuid4())
        message = sms_message.SMSMessage(
            message_id=message_id,
            mobile=request.mobile_number,
            message_text=request.message
        )
        sms_message_obj = message.create(ttl_seconds=settings.REDIS_STORAGE_SMS_MESSAGE_TTL_SECONDS)
        print(f"{sms_message_obj}")
        # TODO: Create celery task
        send_sms_by_pk.delay(pk=message.pk)
        return sms_sender_pb2.MessageID(uuid=str(message_id))

    def GetMessageStatus(self, request, context):
        """Get message status
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=settings.GRPC_MAX_WORKERS))
    sms_sender_pb2_grpc.add_SMSServiceServicer_to_server(
        SMSServiceServicer(), server)
    server.add_insecure_port(f'[::]:{settings.GRPC_PORT}')
    server.start()
    server.wait_for_termination()