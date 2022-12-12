from enum import Enum
from .proto.logging_pb2 import Log

SKYNET_EXCHANGE_NAME_FOR_LOGS = 'logs'
SKYNET_EXCHANGE_NAME_FOR_COMMANDS = 'commands'
SKYNET_EXCHANGE_NAME_FOR_REPLIES = 'replies'
SKYNET_EXCHANGE_NAME_FOR_UPDATES = 'updates'


class SkyNetLogLevel(Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'
    FATAL = 'fatal'

    def format_routing_key(self, slave_name: str = 'anonymous') -> str:
        """
        Formats a routing key for the current level
        :param slave_name: the name of the slave
        :return: the routing key
        """
        return f'{slave_name}.{self.value}'


class SkyNetLogger:
    def __init__(self, channel, log_name: str):
        self._channel = channel
        self._log_name = log_name

    def info(self, message: str, origin: str | None = '') -> None:
        self.log(level=SkyNetLogLevel.INFO, message=message, origin=origin)

    def debug(self, message: str, origin: str | None = '') -> None:
        self.log(level=SkyNetLogLevel.DEBUG, message=message, origin=origin)

    def warn(self, message: str, origin: str | None = '') -> None:
        self.log(level=SkyNetLogLevel.WARN, message=message, origin=origin)

    def error(self, message: str, origin: str | None = '') -> None:
        self.log(level=SkyNetLogLevel.ERROR, message=message, origin=origin)

    def fatal(self, message: str, origin: str | None = '') -> None:
        self.log(level=SkyNetLogLevel.FATAL, message=message, origin=origin)

    def log(self, level: SkyNetLogLevel, message: str, origin: str | None = '') -> None:
        log = Log()
        log.origin = origin
        log.message = message

        self._channel.basic_publish(exchange=SKYNET_EXCHANGE_NAME_FOR_LOGS,
                                    routing_key=level.format_routing_key(self._log_name),
                                    body=log.SerializeToString())
