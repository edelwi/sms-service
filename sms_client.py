import logging
from typing import Tuple

import grpc
import requests

import sender.grpc_stuff.sms_sender_pb2_grpc as sms_sender_pb2_grpc
import sender.grpc_stuff.sms_sender_pb2 as sms_sender_pb2


def send_one_message(stub, message) -> sms_sender_pb2.MessageID:
    print(f"Sending message: {message}")
    sms_to_out = stub.SendMessage(message)
    print(f"Got response: {sms_to_out}")
    return sms_to_out


def send_messages(stub) -> Tuple[sms_sender_pb2.MessageID, ...]:
    r1 = send_one_message(
        stub, sms_sender_pb2.SMSMessage(mobile_number="79991234567", message="Hi")
    )
    r2 = send_one_message(
        stub,
        sms_sender_pb2.SMSMessage(mobile_number="79991234567", message="Hello again!"),
    )
    return r1, r2


def get_status(stub, message_id: sms_sender_pb2.MessageID):
    print(f"get_status: {message_id=}")
    return stub.GetMessageStatus(message_id)


def send_delivery_status(message_id: sms_sender_pb2.MessageID):
    print(f"send_delivery_status: {message_id=}")
    delivery_report = {
        "msg_id": message_id.uuid,
        "receipted_message_id": 42345,
        "status": "delivered",
        "short_message": "id:917615ac sub:001 dlvrd:001 submit date:1701241159 "
                         "done date:1701241159 stat:DELIVRD err:000",
    }
    requests.post("http://localhost:8000/callback", json=delivery_report)


def get_delivery_status(stub, message_id: sms_sender_pb2.MessageID):
    print(f"get_status: {message_id=}")
    return stub.GetDeliveryStatus(message_id)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = sms_sender_pb2_grpc.SMSServiceStub(channel)
        print("-------------- SendMessages --------------")
        ids = send_messages(stub)
        print("-------------- GetMessageStatuses --------------")
        for msg_id in ids:
            ms = get_status(stub, msg_id)
            print(f"Message: {msg_id} status => {ms}")
        print("-------------- SendDeliveryStatuses --------------")
        for msg_id in ids:
            send_delivery_status(msg_id)
            print(f"Message: {msg_id} status => {ms}")
        print("-------------- GetDeliveryStatuses --------------")
        for msg_id in ids:
            ds = get_delivery_status(stub, msg_id)
            print(f"Delivery: {msg_id} status => {ds}")


if __name__ == "__main__":
    logging.basicConfig()
    run()
