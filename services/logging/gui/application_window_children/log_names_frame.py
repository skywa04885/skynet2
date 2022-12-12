import gi
from .log_names_children.tree_view import TreeView

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

LOG_NAMES_FRAME_TITLE = 'Log names'
LOG_NAMES_FRAME_MARGIN = 10


class LogNamesFrame(Gtk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configuration

        self.set_label(LOG_NAMES_FRAME_TITLE)

        # Tree view

        self._tree_view = TreeView()
        self._tree_view.set_margin_start(LOG_NAMES_FRAME_MARGIN)
        self._tree_view.set_margin_end(LOG_NAMES_FRAME_MARGIN)
        self._tree_view.set_margin_top(LOG_NAMES_FRAME_MARGIN)
        self._tree_view.set_margin_bottom(LOG_NAMES_FRAME_MARGIN)
        self._tree_view.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        self._tree_view.get_selection().connect('changed', lambda selection: self.emit('changed', selection))
        self.add(self._tree_view)

    @GObject.Property(type=Gtk.ListStore)
    def current_list_store(self) -> Gtk.ListStore | None:
        return self._tree_view.get_model()

    @current_list_store.setter
    def current_list_store(self, list_store: Gtk.ListStore) -> None:
        self._tree_view.set_model(list_store)


GObject.signal_new('changed', LogNamesFrame, GObject.SIGNAL_RUN_FIRST,
                   GObject.TYPE_NONE, [Gtk.TreeSelection])