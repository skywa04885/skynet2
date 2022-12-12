import gi
import pika

from services.common.logging import SKYNET_EXCHANGE_NAME_FOR_LOGS
from services.common.config import PIKA_HOST, PIKA_PORT, PIKA_RECONNECT_TIMEOUT
from .application_window import ApplicationWindow
from .application_window_children.action_bar import ActionBarConnectedState, ActionBarReconnectingState, \
    ActionBarConnectingState
from services.common.proto.logging_pb2 import Log

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

APPLICATION_ID = 'nl.fannst.t500.log_viewer'


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_application_id(APPLICATION_ID)

        self._application_window = None
        self._log_listener_close_event = None
        self._pika_connection = None

    def do_activate(self) -> None:
        # Creates the application window

        self._application_window = ApplicationWindow()
        self._application_window.set_application(self)
        self._application_window.connect('destroy', self._destroy)
        self._application_window.show_all()

        # Registers signals

        GLib.idle_add(self._pika_connect)

    def _pika_connect(self) -> bool:
        try:
            # Indicates that we're connecting.

            self._application_window.set_connection_state(
                ActionBarConnectingState(PIKA_HOST, PIKA_PORT))

            # Attempts to create the pika connection.

            self._pika_connection = pika.BlockingConnection(pika.ConnectionParameters(host=PIKA_HOST, port=PIKA_PORT))

            # Updates the state to indicate we're connected.

            self._application_window.set_connection_state(
                ActionBarConnectedState(PIKA_HOST, PIKA_PORT))

            # Creates the channel, and declares the exchanges.

            mq_channel = self._pika_connection.channel()
            mq_channel.exchange_declare(exchange=SKYNET_EXCHANGE_NAME_FOR_LOGS, exchange_type='topic')

            # Creates the queues.

            mq_log_queue = mq_channel.queue_declare('', exclusive=True)
            mq_log_queue_name = mq_log_queue.method.queue

            # Binds the queues.

            mq_channel.queue_bind(queue=mq_log_queue_name, exchange=SKYNET_EXCHANGE_NAME_FOR_LOGS,
                                  routing_key='*.*')

            # Adds the consumers to the queues.

            mq_channel.basic_consume(queue=mq_log_queue_name,
                                     on_message_callback=self._on_log_message,
                                     auto_ack=True)

            # Processes the data every 1ms.

            GLib.timeout_add(1, self._pika_process_data)
        except:
            self._pika_schedule_reconnect()

        return False

    def _on_log_message(self, _channel, method, _properties, body) -> None:
        log = Log()
        log.ParseFromString(body)

        slave = method.routing_key.split('.')[0]
        self._application_window.append_log(slave, log)

    def _pika_process_data(self) -> bool:
        try:
            self._pika_connection.process_data_events()

            return True
        except:
            self._pika_schedule_reconnect()

            return False

    def _pika_schedule_reconnect(self) -> None:
        self._application_window.set_connection_state(
            ActionBarReconnectingState(PIKA_HOST, PIKA_PORT, PIKA_RECONNECT_TIMEOUT))
        GLib.timeout_add(int(PIKA_RECONNECT_TIMEOUT * 1000.0), self._pika_connect)

    def _destroy(self, _) -> None:
        self._log_listener_close_event.set()
        self.quit()
