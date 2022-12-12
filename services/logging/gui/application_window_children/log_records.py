import gi
from .log_records_children.tree_view import TreeView

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

LOG_RECORDS_FRAME_TITLE = 'Log Records'
LOG_RECORDS_FRAME_MARGIN = 10


class LogRecordsFrame(Gtk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configuration

        self.set_label(LOG_RECORDS_FRAME_TITLE)

        # Scrollable Window

        self._scrolled_window = Gtk.ScrolledWindow()
        self._scrolled_window.set_margin_start(LOG_RECORDS_FRAME_MARGIN)
        self._scrolled_window.set_margin_end(LOG_RECORDS_FRAME_MARGIN)
        self._scrolled_window.set_margin_top(LOG_RECORDS_FRAME_MARGIN)
        self._scrolled_window.set_margin_bottom(LOG_RECORDS_FRAME_MARGIN)
        self._scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        self.add(self._scrolled_window)

        # Tree view

        self._tree_view = TreeView()
        self._tree_view.get_selection().set_mode(Gtk.SelectionMode.NONE)
        self._tree_view.set_size_request(-1, 400)
        self._scrolled_window.add(self._tree_view)

    @GObject.Property(type=Gtk.ListStore)
    def current_list_store(self) -> Gtk.ListStore | None:
        return self._tree_view.get_model()

    @current_list_store.setter
    def current_list_store(self, list_store: Gtk.ListStore) -> None:
        self._tree_view.set_model(list_store)
