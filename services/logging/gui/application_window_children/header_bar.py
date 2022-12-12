import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject

HEADER_BAR_TITLE = 'SkyNet'
HEADER_BAR_SUBTITLE = 'Real-Time Log Explorer'


class HeaderBar(Gtk.HeaderBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configuration

        self.set_title(HEADER_BAR_TITLE)
        self.set_subtitle(HEADER_BAR_SUBTITLE)

        self.set_show_close_button(True)

        # Info button

        self._info_button_image = Gtk.Image(stock=Gtk.STOCK_INFO)
        self._info_button = Gtk.Button()
        self._info_button.set_image(self._info_button_image)
        self._info_button.set_tooltip_text('Application information')
        self._info_button.connect('clicked', lambda widget: self.emit('about_button_clicked', widget))
        self.pack_end(self._info_button)

        # Clear button

        self._clear_button_image = Gtk.Image(stock=Gtk.STOCK_DELETE)
        self._clear_button = Gtk.Button()
        self._clear_button.set_image(self._clear_button_image)
        self._clear_button.set_tooltip_text('Clear logs')
        self._clear_button.connect('clicked', lambda widget: self.emit('clear_button_clicked', widget))
        self.pack_end(self._clear_button)


GObject.signal_new('about_button_clicked', HeaderBar, GObject.SIGNAL_RUN_FIRST,
                   GObject.TYPE_NONE, [Gtk.Button])
GObject.signal_new('clear_button_clicked', HeaderBar, GObject.SIGNAL_RUN_FIRST,
                   GObject.TYPE_NONE, [Gtk.Button])
