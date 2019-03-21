import curses

from curses_ui.widget import BaseWidget


class BlockWidget(BaseWidget):
    """
    A simple block that creates a square of characters, useful for testing.

    If you want a dimensional panel without any rendering, use the PanelWidget instead.
    """

    def __init__(self, base, ch=None, **kwargs):
        super(BlockWidget, self).__init__(base, **kwargs)
        self.ch = ch

    def paint_content(self):
        x1, y1, x2, y2, width, height = self.get_dimensions()
        ch = self.ch if self.ch is not None else curses.ACS_CKBOARD

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.addch(y, x, ch)


class HorizontalRule(BaseWidget):
    """
    A horizontal line
    """

    T_CONNECTION = 'T'
    PLUS_CONNECTION = '+'
    UP_CONNECTION = 'U'
    DOWN_CONNECTION = 'D'

    def __init__(self, base, left_connection=None, right_connection=None, colour='default', **kwargs):
        kwargs['height'] = 1
        super(HorizontalRule, self).__init__(base, **kwargs)
        self.left_connection = left_connection
        self.right_connection = right_connection
        self.colour = colour

    def paint_content(self):
        x1, y1, x2, y2, width, height = self.get_dimensions()
        for x in range(x1 + 1, x2):
            self.addch(y1, x, curses.ACS_HLINE, self.colour)

        if self.left_connection == self.T_CONNECTION:
            lchar = curses.ACS_LTEE
        elif self.left_connection == self.PLUS_CONNECTION:
            lchar = curses.ACS_PLUS
        elif self.left_connection == self.UP_CONNECTION:
            lchar = curses.ACS_LLCORNER
        elif self.left_connection == self.DOWN_CONNECTION:
            lchar = curses.ACS_ULCORNER
        else:
            lchar = curses.ACS_HLINE

        if self.right_connection == self.T_CONNECTION:
            rchar = curses.ACS_RTEE
        elif self.right_connection == self.PLUS_CONNECTION:
            rchar = curses.ACS_PLUS
        elif self.right_connection == self.UP_CONNECTION:
            rchar = curses.ACS_LRCORNER
        elif self.right_connection == self.DOWN_CONNECTION:
            rchar = curses.ACS_URCORNER
        else:
            rchar = curses.ACS_HLINE

        self.addch(y1, x1, lchar, self.colour)
        self.addch(y1, x2, rchar, self.colour)


class VerticalRule(BaseWidget):
    """
    A vertical line
    """

    T_CONNECTION = 'T'
    PLUS_CONNECTION = '+'
    LEFT_CONNECTION = 'L'
    RIGHT_CONNECTION = 'R'

    def __init__(self, base, top_connection=None, bottom_connection=None, colour='default', **kwargs):
        kwargs['width'] = 1
        super(VerticalRule, self).__init__(base, **kwargs)
        self.top_connection = top_connection
        self.bottom_connection = bottom_connection
        self.colour = colour

    def paint_content(self):
        x1, y1, x2, y2, width, height = self.get_dimensions()
        for y in range(y1 + 1, y2):
            self.addch(y, x1, curses.ACS_VLINE, self.colour)

        if self.top_connection == self.T_CONNECTION:
            tchar = curses.ACS_TTEE
        elif self.top_connection == self.PLUS_CONNECTION:
            tchar = curses.ACS_PLUS
        elif self.top_connection == self.LEFT_CONNECTION:
            tchar = curses.ACS_URCORNER
        elif self.top_connection == self.RIGHT_CONNECTION:
            tchar = curses.ACS_ULCORNER
        else:
            tchar = curses.ACS_VLINE

        if self.bottom_connection == self.T_CONNECTION:
            bchar = curses.ACS_BTEE
        elif self.bottom_connection == self.PLUS_CONNECTION:
            bchar = curses.ACS_PLUS
        elif self.bottom_connection == self.LEFT_CONNECTION:
            bchar = curses.ACS_LRCORNER
        elif self.bottom_connection == self.RIGHT_CONNECTION:
            bchar = curses.ACS_LLCORNER
        else:
            bchar = curses.ACS_VLINE

        self.addch(y1, x1, tchar, self.colour)
        self.addch(y2, x1, bchar, self.colour)
