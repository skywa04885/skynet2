import gi
from .about_dialog import AboutDialog
from .application_window_children.header_bar import HeaderBar
from .application_window_children.log_records import LogRecordsFrame
from .application_window_children.log_names_frame import LogNamesFrame
from .application_window_children.action_bar import ActionBar, ActionBarConnectionState, ActionBarConnectedState, ActionBarReconnectingState, ActionBarConnectingState
from services.common.proto.logging_pb2 import Log
from datetime import datetime
import logging

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

APPLICATION_WINDOW_TITLE = 'SkyNet Log Viewer'
APPLICATION_WINDOW_WIDTH, APPLICATION_WINDOW_HEIGHT = 900, 700


class ApplicationWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title(APPLICATION_WINDOW_TITLE)
        self.set_size_request(width=APPLICATION_WINDOW_WIDTH,
                              height=APPLICATION_WINDOW_HEIGHT)

        # Instance variables

        self._log_names_list_store = Gtk.ListStore(str)
        self._log_records_list_stores = {}

        # Header bar

        self._header_bar = HeaderBar()
        self._header_bar.connect("about_button_clicked", self._on_header_about_button_clicked)
        self._header_bar.connect("clear_button_clicked", self._on_header_clear_button_clicked)
        self.set_titlebar(self._header_bar)

        # Vertical wrapper

        self._v_wrapper = Gtk.Box()
        self._v_wrapper.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self._v_wrapper)

        # Horizontal wrapper

        self._h_wrapper = Gtk.Box()
        self._h_wrapper.set_orientation(Gtk.Orientation.HORIZONTAL)
        self._h_wrapper.set_vexpand(True)
        self._v_wrapper.add(self._h_wrapper)

        # Log records frame

        self._log_records_frame = LogRecordsFrame()
        self._log_records_frame.set_margin_start(10)
        self._log_records_frame.set_margin_end(5)
        self._log_records_frame.set_margin_bottom(10)
        self._log_records_frame.set_margin_top(10)
        self._log_records_frame.set_hexpand(True)
        self._log_records_frame.set_property("current_list_store", Gtk.ListStore(str, str, str))
        self._h_wrapper.add(self._log_records_frame)

        # Log names frame

        self._log_names_frame = LogNamesFrame()
        self._log_names_frame.set_margin_start(5)
        self._log_names_frame.set_margin_end(10)
        self._log_names_frame.set_margin_bottom(10)
        self._log_names_frame.set_margin_top(10)
        self._log_names_frame.set_hexpand(True)
        self._log_names_frame.set_property("current_list_store", self._log_names_list_store)
        self._log_names_frame.connect('changed', self._on_slave_tree_selection_changed)
        self._h_wrapper.add(self._log_names_frame)

        # Action bar

        self._action_bar = ActionBar()
        self._v_wrapper.add(self._action_bar)

    def set_connection_state(self, connection_state: ActionBarConnectionState):
        self._action_bar.set_property("connection_state", connection_state)

    def _on_header_clear_button_clicked(self, _header_bar, _widget) -> None:
        for list_store in self._log_records_list_stores.values():
            list_store.clear()

    def _on_header_about_button_clicked(self, _header_bar, _widget) -> None:
        about_dialog = AboutDialog()
        about_dialog.set_application(self.get_application())
        about_dialog.present()

    def _on_slave_tree_selection_changed(self, _widget: LogNamesFrame, selection: Gtk.TreeSelection) -> None:
        model, tree_iterator = selection.get_selected()
        if tree_iterator is not None:
            log_name: str = model[tree_iterator][0]
            self._change_active_log(log_name)

    def _change_active_log(self, log_name: str) -> None:
        logging.info(f'Changing active log to: {log_name}')

        if self._log_records_list_stores[log_name] is None:
            self._log_names_list_store.append([log_name])
            self._log_records_list_stores[log_name] = Gtk.ListStore(str, str, str)

        self._log_records_frame.set_property("current_list_store", self._log_records_list_stores[log_name])

    def append_log(self, log_name: str, log_record: Log) -> None:
        # Creates the list store if not existing yet.
        if self._log_records_list_stores.get(log_name) is None:
            self._log_names_list_store.append([log_name])
            self._log_records_list_stores.setdefault(log_name, Gtk.ListStore(str, str, str))

        # Adds the log record.
        self._log_records_list_stores[log_name].append(
            [datetime.now().strftime("%c"), log_record.origin, log_record.message])

        # Increases the total log count.
        self._action_bar.set_total_log_record_count(
            self._action_bar.get_total_log_record_count() + 1)
