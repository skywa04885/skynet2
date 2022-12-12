import os

PIKA_HOST = os.environ.get('RABBITMQ_HOST', '127.0.0.1')
PIKA_PORT = int(os.environ.get('RABBITMQ_PORT', '5672'))
PIKA_RECONNECT_TIMEOUT = 0.5
