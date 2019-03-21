import curses

from curses_ui.event import key, Dispatcher
from curses_ui.event.key import KeyPressEvent
from curses_ui.event.screen import ExitEvent
from curses_ui.exception import IndexOutOfRangeException, InvalidArgumentException
from curses_ui.interface import TabAware, Selectable


class Screen(object):
    """
    Represents a display state on the screen, which may include multiple windows.
    """

    def __init__(self, colour_pack, screen_id):
        super(Screen, self).__init__()
        self.stdscr = None
        self.dispatcher = Dispatcher()
        self.widgets = []
        self.colour_pack = colour_pack
        self.screen_id = screen_id

        # If using a screen manager, it will toggle this property to inform the screen if it is active on the display.
        # If NOT using a screen manager, you must set this property to True before widgets will paint.
        self.active = False

    def build(self, stdscr):
        """
        Should be called by curses.wrapper() directly or a main application loop inside curses.wrapper()
        :param stdscr:
        :return:
        """
        self.stdscr = stdscr

    def paint(self, clear=False, refresh=True):
        """
        Repaint all widgets
        :param clear: bool
        :param refresh: bool
        :return:
        """
        for widget in self.widgets:
            widget.paint(clear=clear, refresh=False)

        if refresh:
            self.stdscr.refresh()

    def add_widget(self, widget, **args):
        """
        Add a widget to the screen
        :param widget: Widget class
        :param args: dict of widget parameters
        :return: An instance of the new widget
        """
        instance = widget(self, **args)
        self.widgets.append(instance)
        return instance

    @staticmethod
    def set_cursor(state):
        """
        Enable or disable the cursor
        :param state: bool
        :return:
        """
        curses.curs_set(state)

    def exit(self):
        """
        Inform anyone listening that we're done and want to close
        :return:
        """
        self.dispatcher.notify(ExitEvent(self.screen_id))


class KeyAwareScreen(Screen):
    """
    A screen class that automatically listens for key presses
    """

    def __init__(self, colour_pack, screen_id):
        super(KeyAwareScreen, self).__init__(colour_pack, screen_id)

        # Default listener for key presses
        self.dispatcher.subscribe(self.on_key_press, KeyPressEvent.EVENT_NAME)

    def on_key_press(self, e):
        """
        Event dispatcher listener for key presses
        :param e: event
        :return:
        """
        if self.active:
            self.key_press(e.key)

    def key_press(self, c):
        """
        Executed when the screen is notified of a key press and it is active
        :param c: int
        :return:
        """
        pass


class TabAwareScreen(KeyAwareScreen, TabAware):
    """
    A screen class that will allow tabbing between widgets
    """

    def __init__(self, colour_pack, screen_id, arrow_nav=True):
        super(TabAwareScreen, self).__init__(colour_pack, screen_id)
        self.tab_widgets = []
        self.tab_index = 0
        self.arrow_nav = arrow_nav
        self.dispatcher.subscribe(self.tab_listener, KeyPressEvent.EVENT_NAME)

    def add_tab(self, *args):
        """
        Register one or more widgets on the tab pool
        :param args: SelectableWidget[]
        :return:
        """
        for w in args:
            if not isinstance(w, Selectable):
                raise InvalidArgumentException("Only Selectable widgets can enable tab support")

            self.tab_widgets.append(w)

            if len(self.tab_widgets) == 1:
                # Set the first/only widget to be selected
                w.set_selected(True)

    def tab_listener(self, e):
        """
        Event dispatcher listener for key presses
        :param e: event
        :return:
        """
        if not self.active:
            return

        if e.key == key.TAB:
            e.handled = True
            return self.tab_next()

        if e.key == key.SHIFT_TAB:
            e.handled = True
            return self.tab_previous()

        if self.arrow_nav and e.key == key.ARROW_DOWN:
            e.handled = True
            return self.tab_next()

        if self.arrow_nav and e.key == key.ARROW_UP:
            e.handled = True
            return self.tab_previous()

    def tab_next(self):
        return self.tab_iterate(forward=True)

    def tab_previous(self):
        return self.tab_iterate(forward=False)

    def tab_iterate(self, forward=True):
        if not self.active or (len(self.tab_widgets) < 2):
            return

        start_index = self.tab_index
        self.tab_widgets[self.tab_index].set_selected(False)

        while True:
            self.tab_index += 1 if forward else -1
            if self.tab_index < 0:
                self.tab_index = len(self.tab_widgets) - 1
            elif self.tab_index >= len(self.tab_widgets):
                self.tab_index = 0

            if (self.tab_index == start_index) or self.tab_widgets[self.tab_index].is_renderable():
                break

        self.tab_widgets[self.tab_index].set_selected(True)

    def set_tab_index(self, index):
        if index < 0 or index >= len(self.tab_widgets):
            raise IndexOutOfRangeException("Tab index '{}' not valid".format(index))

        self.tab_widgets[self.tab_index].set_selected(False)
        self.tab_index = index
        self.tab_widgets[self.tab_index].set_selected(True)
