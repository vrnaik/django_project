import curses

from curses_ui.widget import BaseWidget


class TitleWindow(BaseWidget):
    """
    A framed window
    """

    def __init__(self, base, title, **kwargs):
        super(TitleWindow, self).__init__(base, **kwargs)
        self.title = title
        self.boundaries = (1, 1, 1, 1)

    def paint_content(self):
        x1, y1, x2, y2, width, height = self.get_dimensions(include_boundary=False)
        title_pos = int(((x2 - x1) / 2) - ((len(self.title) + 2) / 2))

        self.addch(y1, x1, curses.ACS_ULCORNER, 'frame')
        self.addch(y1, x2, curses.ACS_URCORNER, 'frame')
        self.addch(y2, x1, curses.ACS_LLCORNER, 'frame')
        self.addch(y2, x2, curses.ACS_LRCORNER, 'frame')

        for i in range(x1 + 1, x2):
            self.addch(y1, i, curses.ACS_HLINE, 'frame')
            self.addch(y2, i, curses.ACS_HLINE, 'frame')

        for i in range(y1 + 1, y2):
            self.addch(i, x1, curses.ACS_VLINE, 'frame')
            self.addch(i, x2, curses.ACS_VLINE, 'frame')

        self.addstr(y1, title_pos, " {} ".format(self.title), 'title')


class PanelWidget(BaseWidget):
    """
    A panel, has no actual rendering but can be used as a base for child widgets. If you require a rendered backdrop
    then consider using the BlockWidget instead.
    """

    def __init__(self, base, margin=0, **kwargs):
        super(PanelWidget, self).__init__(base, **kwargs)

        if margin > 0:
            self.boundaries = (margin, margin, margin, margin)

    def paint_content(self):
        pass
