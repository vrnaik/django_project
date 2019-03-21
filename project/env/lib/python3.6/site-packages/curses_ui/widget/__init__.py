import curses
from abc import abstractmethod

from curses_ui.interface import Selectable
from curses_ui.screen import Screen


class InvalidBaseException(Exception):
    pass


class BaseWidget(object):
    def __init__(self, base, x=0, y=0, width=None, height=None, visible=True, enabled=True):
        super(BaseWidget, self).__init__()

        if not isinstance(base, Screen) and not isinstance(base, BaseWidget):
            raise InvalidBaseException()

        # Parent widget or screen
        self.base = base

        # General properties
        self.visible = visible
        self.enabled = enabled

        # Child widgets
        self.widgets = []

        # Coordinates relative to parent
        self.x = x
        self.y = y

        # Widget dimensions
        self.width = width
        self.height = height

        # Relative painting boundaries (eg offset for the frame) in order top, right, bottom, left
        self.boundaries = (0, 0, 0, 0)

    def add_widget(self, widget, **args):
        """
        Add a widget to the screen
        :param widget: Widget class
        :param args: dict of widget parameters
        :return: Widget instance
        """
        instance = widget(self, **args)
        self.widgets.append(instance)
        return instance

    def get_dimensions(self, include_boundary=True):
        """
        Get the absolute screen position of this widget in a tuple.
        :param include_boundary: bool
        :return: (x1, y1, x2, y2, width, height)
        """
        width = self.width
        height = self.height
        x = self.x
        y = self.y

        if isinstance(self.base, BaseWidget):
            parent_dimensions = self.base.get_dimensions()
        else:
            parent_dimensions = (0, 0, curses.COLS - 1, curses.LINES - 1, curses.COLS, curses.LINES)

        if x is None:
            x = 0
        elif x < 0:
            x += parent_dimensions[4]

        if y is None:
            y = 0
        elif y < 0:
            y += parent_dimensions[5]

        if width is None:
            width = parent_dimensions[4] - x
        elif width < 0:
            width += parent_dimensions[4] - x

        if height is None:
            height = parent_dimensions[5] - y
        elif height < 0:
            height += parent_dimensions[5] - y

        if include_boundary:
            return (
                parent_dimensions[0] + x + self.boundaries[3],
                parent_dimensions[1] + y + self.boundaries[0],

                parent_dimensions[0] + x + width - 1 - self.boundaries[1],
                parent_dimensions[1] + y + height - 1 - self.boundaries[2],

                width - self.boundaries[1] - self.boundaries[3],
                height - self.boundaries[0] - self.boundaries[2]
            )
        else:
            return (
                parent_dimensions[0] + x,
                parent_dimensions[1] + y,

                parent_dimensions[0] + x + width - 1,
                parent_dimensions[1] + y + height - 1,

                width,
                height
            )

    def get_screen(self):
        """
        Get the screen that this widget (or its ancestors) are built upon.
        :return:
        """
        if isinstance(self.base, BaseWidget):
            return self.base.get_screen()
        elif isinstance(self.base, Screen):
            return self.base
        else:
            return None

    def is_renderable(self):
        """
        Checks that this widget, all ancestors and the base screen are both enabled and visible.
        :return: bool
        """
        return self.is_enabled() and self.is_visible()

    def is_enabled(self):
        """
        Checks that this widget, all ancestors and the base screen are enabled.
        :return: bool
        """
        if not self.enabled:
            return False

        if isinstance(self.base, BaseWidget):
            return self.base.is_enabled()
        elif isinstance(self.base, Screen):
            return self.base.active
        else:
            return False

    def is_visible(self):
        """
        Checks that this widget, all ancestors and the base screen are visible.
        :return: bool
        """
        if not self.visible:
            return False

        if isinstance(self.base, BaseWidget):
            return self.base.is_visible()
        elif isinstance(self.base, Screen):
            return self.base.active
        else:
            return False

    def get_dispatcher(self):
        if isinstance(self.base, BaseWidget):
            return self.base.get_dispatcher()
        elif isinstance(self.base, Screen):
            return self.base.dispatcher
        else:
            return None

    def paint(self, clear=False, refresh=False):
        """
        Draw the window, optionally clearing the content or refreshing the stdscr.
        :param clear: bool
        :param refresh: bool
        :return:
        """
        if not self.is_renderable():
            return

        x1, y1, x2, y2, width, height = self.get_dimensions()

        if clear:
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    self.addch(y, x, 32)

        self.paint_content()

        for widget in self.widgets:
            widget.paint(clear=clear, refresh=False)

        if refresh:
            self.get_screen().stdscr.refresh()

    @abstractmethod
    def paint_content(self):
        pass

    def addch(self, y, x, ch, colour='default'):
        """
        Shorthand to use the stdscr of the parent Screen object to add a character, using the Screen colour pack.
        If you attempt to use this on the bottom right character of the screen, it will fallback to insch to avoid an
        overflow error with the cursor.
        :param y: int
        :param x: int
        :param ch: int
        :param colour: string
        :return:
        """
        if y >= curses.LINES or x >= curses.COLS:
            return

        if y == curses.LINES - 1 and x == curses.COLS - 1:
            self.get_screen().stdscr.insch(y, x, ch, self.get_screen().colour_pack.get(colour))
        else:
            self.get_screen().stdscr.addch(y, x, ch, self.get_screen().colour_pack.get(colour))

    def addstr(self, y, x, txt, colour, wrap=False):
        """
        Shorthand to use the stdscr of the parent Screen object to add a string, using the Screen colour pack.
        This function will not draw off the screen, and will fallback to insstr if on the last line and painting to the
        edge of the screen.
        :param y: int
        :param x: int
        :param txt: string
        :param colour: string
        :param wrap: bool
        :return:
        """
        if y >= curses.LINES or x >= curses.COLS:
            return

        if not wrap and (len(txt) + x) > curses.COLS:
            # Need to truncate text
            txt = txt[:curses.COLS - len(txt) - x]

        # If on last line and will paint to the edge of the screen, use insstr
        if (y == curses.LINES - 1) and (len(txt) + x >= curses.COLS):
            self.get_screen().stdscr.insstr(y, x, txt, self.get_screen().colour_pack.get(colour))
        else:
            self.get_screen().stdscr.addstr(y, x, txt, self.get_screen().colour_pack.get(colour))

    def write(self, y, x, txt, colour):
        """
        Write text inside the current widget, using relative coordinates to the widgets position on its parent.
        :param y: int
        :param x: int
        :param txt: string
        :param colour: string
        :return:
        """
        x1, y1, x2, y2, width, height = self.get_dimensions()
        x1 += self.boundaries[3] + x
        y1 += self.boundaries[0] + y

        self.addstr(y1, x1, txt, colour)

    def insch(self, y, x, ch, colour='default'):
        """
        Shorthand to use the stdscr of the parent Screen object to insert a character, using the Screen colour pack.
        :param y: int
        :param x: int
        :param ch: int
        :param colour: string
        :return:
        """
        if y >= curses.LINES or x >= curses.COLS:
            return

        self.get_screen().stdscr.insch(y, x, ch, self.get_screen().colour_pack.get(colour))

    def insstr(self, y, x, txt, colour):
        """
        Shorthand to use the stdscr of the parent Screen object to insert a string, using the Screen colour pack.
        :param y: int
        :param x: int
        :param txt: string
        :param colour: string
        :return:
        """
        if y >= curses.LINES or x >= curses.COLS:
            return

        self.get_screen().stdscr.insstr(y, x, txt, self.get_screen().colour_pack.get(colour))


class SelectableWidget(BaseWidget, Selectable):
    def __init__(self, base, x=0, y=0, width=None, height=None, visible=True, enabled=True, selected=False):
        super(SelectableWidget, self).__init__(base, x, y, width, height, visible, enabled)
        self.selected = selected

    def set_selected(self, selected):
        if selected != self.selected:
            self.selected = selected
            self.paint(clear=True, refresh=True)

    def paint_content(self):
        super(SelectableWidget, self).paint_content()
