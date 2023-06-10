from netaddr import IPAddress, AddrFormatError
from fastapi import Request, Depends

from config import settings


# def on_request(request: Request):
#     return request


def is_granted_ip(request: Request) -> bool:
    ip = request.client.host
    try:
        ip_addr = IPAddress(ip)
    except (ValueError, AddrFormatError):
        return False
    for net in settings.CALLBACK_GRANTED_NETWORKS:
        if ip_addr in net:
            return True
    else:
        return False
