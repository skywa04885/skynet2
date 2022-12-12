import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

LOG_NAMES_TREE_VIEW_NAME_COLUMN_NAME = 'Name'


class TreeView(Gtk.TreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Name column

        self._name_column = Gtk.TreeViewColumn(title=LOG_NAMES_TREE_VIEW_NAME_COLUMN_NAME,
                                               cell_renderer=Gtk.CellRendererText(), text=0)
        self._name_column.set_resizable(True)
        self.append_column(self._name_column)
