import uuid
from concurrent import futures
from sender.grpc_stuff import sms_sender_pb2_grpc, sms_sender_pb2
import grpc

import sender.model.sms_message as sms_message


class SMSServiceServicer(sms_sender_pb2_grpc.SMSServiceServicer):
    """Service to send SMS and get status
    """

    def SendMessage(self, request, context):
        """Send message
        """
        message_id = uuid.uuid4()
        # message = sms_message.SMSMessage(
        #     message_id=message_id,
        #     mobile=request.mobile_number,
        #     message_text=request.message
        # )
        # message.save()
        # TODO: Create celery task
        # task_send_sms_message.delay(pk=message.pk)
        return sms_sender_pb2.MessageID(uuid=str(message_id))

    def GetMessageStatus(self, request, context):
        """Get message status
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sms_sender_pb2_grpc.add_SMSServiceServicer_to_server(
        SMSServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
