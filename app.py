import logging
import os

print(f"{os.getcwd()=}")

print(f"{os.listdir()=}")

from sender.grpc_stuff.server import serve

if __name__ == '__main__':
    logging.basicConfig()
    logging.info('Start server')
    serve()