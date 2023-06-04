import logging

import grpc

import sender.grpc_stuff.sms_sender_pb2_grpc as sms_sender_pb2_grpc
import sender.grpc_stuff.sms_sender_pb2 as sms_sender_pb2


def send_one_message(stub, message):
    print(f"Sending message: {message}")
    sms_to_out = stub.SendMessage(message)
    print(f"Got response: {sms_to_out}")


def send_messages(stub):
    send_one_message(
        stub, sms_sender_pb2.SMSMessage(mobile_number="79991234567", message="Hi")
    )
    send_one_message(
        stub,
        sms_sender_pb2.SMSMessage(mobile_number="79991234567", message="Hello again!"),
    )


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = sms_sender_pb2_grpc.SMSServiceStub(channel)
        print("-------------- SendMessages --------------")
        send_messages(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()
