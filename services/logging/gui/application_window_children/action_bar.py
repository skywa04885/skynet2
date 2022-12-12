import gi
from .log_names_children.tree_view import TreeView

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject


class ActionBarConnectionState:
    def __init__(self, show_spinner: bool):
        self.show_spinner = show_spinner

    def __str__(self):
        return '-'


class ActionBarConnectingState(ActionBarConnectionState):
    def __init__(self, host: str, port: int) -> None:
        super().__init__(True)

        self.host = host
        self.port = port

    def __str__(self) -> str:
        return f'Connecting to {self.host}:{self.port}.'


class ActionBarConnectedState(ActionBarConnectionState):
    def __init__(self, host: str, port: int) -> None:
        super().__init__(False)

        self.host = host
        self.port = port

    def __str__(self) -> str:
        return f'Connected to {self.host}:{self.port}.'


class ActionBarReconnectingState(ActionBarConnectionState):
    def __init__(self, host: str, port: int, timeout: float) -> None:
        super().__init__(True)

        self.host = host
        self.port = port
        self.timeout = timeout

    def __str__(self) -> str:
        return f'Reconnecting to {self.host}:{self.port} in {self.timeout} seconds.'


class ActionBar(Gtk.ActionBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Instance variables

        self._total_log_record_count = 0
        self._connection_state = ActionBarConnectionState(show_spinner=True)

        # Log info

        self._log_info_label = Gtk.Label()
        self.add(self._log_info_label)

        # Separator between log info & connection info.

        separator = Gtk.Separator()
        separator.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(separator)

        # Connection info

        self._connection_state_label = Gtk.Label()
        self.add(self._connection_state_label)

        # Connection spinner

        self._connection_state_spinner = Gtk.Spinner()
        self.add(self._connection_state_spinner)

        # Initializes

        self.set_connection_state(connection_state=ActionBarConnectionState(show_spinner=True))
        self.set_total_log_record_count(0)

    def _update_log_info(self) -> None:
        self._log_info_label.set_label(f'Total log records: {self._total_log_record_count}')

    def _update_connection_state(self) -> None:
        if self._connection_state.show_spinner is True:
            self._connection_state_spinner.start()
        else:
            self._connection_state_spinner.stop()

        self._connection_state_label.set_label(str(self._connection_state))

    @GObject.Property
    def connection_state(self):
        return self._connection_state

    @connection_state.setter
    def connection_state(self, connection_state) -> None:
        self._connection_state = connection_state
        self._update_connection_state()

    def set_connection_state(self, connection_state) -> None:
        self.set_property('connection_state', connection_state)

    def get_connection_state(self):
        return self.get_property("connection_state")

    @GObject.Property(type=int)
    def total_log_record_count(self) -> int:
        return self._total_log_record_count

    @total_log_record_count.setter
    def total_log_record_count(self, total_log_record_count: int) -> None:
        self._total_log_record_count = total_log_record_count
        self._update_log_info()

    def set_total_log_record_count(self, total_log_record_count: int) -> None:
        self.set_property('total_log_record_count', total_log_record_count)

    def get_total_log_record_count(self) -> int:
        return self.get_property('total_log_record_count')
