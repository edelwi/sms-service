import asyncio
import logging


from sender.grpc_stuff.server import serve

if __name__ == '__main__':
    logging.basicConfig()
    logging.info('Start server')
    asyncio.run(serve())

# if __name__ == '__main__':
#     serve()