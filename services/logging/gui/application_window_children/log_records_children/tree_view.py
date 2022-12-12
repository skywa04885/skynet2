import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

LOG_RECORD_TREE_VIEW_DATE_TIME_COLUMN_TITLE = 'Date Time'
LOG_RECORD_TREE_VIEW_ORIGIN_COLUMN_TITLE = 'Origin'
LOG_RECORD_TREE_VIEW_MESSAGE_COLUMN_TITLE = 'Message'


class TreeView(Gtk.TreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Date time column

        self._date_time_column = Gtk.TreeViewColumn(title=LOG_RECORD_TREE_VIEW_DATE_TIME_COLUMN_TITLE,
                                                    cell_renderer=Gtk.CellRendererText(), text=0)
        self._date_time_column.set_resizable(True)
        self._date_time_column.set_min_width(100)
        self.append_column(self._date_time_column)

        # Origin column

        self._origin_column = Gtk.TreeViewColumn(title=LOG_RECORD_TREE_VIEW_ORIGIN_COLUMN_TITLE,
                                                 cell_renderer=Gtk.CellRendererText(), text=1)
        self._origin_column.set_resizable(True)
        self._origin_column.set_min_width(60)
        self.append_column(self._origin_column)

        # Message column

        self._message_column = Gtk.TreeViewColumn(title=LOG_RECORD_TREE_VIEW_MESSAGE_COLUMN_TITLE,
                                                  cell_renderer=Gtk.CellRendererText(), text=2)
        self._message_column.set_resizable(True)
        self._message_column.set_min_width(100)
        self.append_column(self._message_column)
