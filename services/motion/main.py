import os

import pika
import socket
import logging
from services.common.proto.logging_pb2 import Log
from services.common.logging import SKYNET_EXCHANGE_NAME_FOR_LOGS, SkyNetLogLevel, SkyNetLogger

def main():
    mq_connection = pika.BlockingConnection()
    mq_channel = mq_connection.channel()

    mq_channel.exchange_declare(SKYNET_EXCHANGE_NAME_FOR_LOGS, exchange_type='topic')

    logger = SkyNetLogger(channel=mq_channel, log_name=f'motion@{socket.gethostname()}')
    logger.info('Motion service is ready.', origin='main')


    try:
        mq_channel.start_consuming()
    except KeyboardInterrupt:
        mq_channel.stop_consuming()

    mq_connection.close()


if __name__ == '__main__':
    main()
