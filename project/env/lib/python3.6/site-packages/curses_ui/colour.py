import curses


class ColourPack(object):
    """
    Represents a colour theme, this class includes a default theme, extend this class to override/customise the
    colour pack.
    """

    def __init__(self, build=False):
        """
        Create a new colour pack, if the curses environment is not fully set up then set build=False and call build()
        when the environment is ready.
        :param build: bool
        :return:
        """
        super(ColourPack, self).__init__()

        self.colour_codes = {'default': 0}
        self.built = False

        if build:
            self.build()

    def get(self, code='default'):
        """
        Get a colour code based on the colour name, will build the pack if not currently built.
        :param code: string
        :return: int
        """
        if not self.built:
            self.build()

        if code in self.colour_codes:
            return self.colour_codes[code]
        else:
            return self.colour_codes['default']

    def build(self):
        """
        Builds the colour pack, including configuring curses colour pairs. Do not call this until the curses environment
        has been fully set up, or an exception will be raised.
        :return:
        """
        self.built = True

        # 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

        curses.init_pair(11, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_WHITE)
        curses.init_pair(13, curses.COLOR_YELLOW, curses.COLOR_WHITE)
        curses.init_pair(14, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(15, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        curses.init_pair(16, curses.COLOR_CYAN, curses.COLOR_WHITE)
        curses.init_pair(17, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Make some defaults, super classes can override/remove these
        self.colour_codes['default'] = curses.color_pair(7)
        self.colour_codes['frame'] = curses.color_pair(6)
        self.colour_codes['title'] = curses.color_pair(3) | curses.A_BOLD
        self.colour_codes['info'] = curses.color_pair(2)
        self.colour_codes['selected'] = curses.color_pair(3)
        self.colour_codes['highlight'] = curses.color_pair(4) | curses.A_STANDOUT
        self.colour_codes['error'] = curses.color_pair(1) | curses.A_BOLD
        self.colour_codes['input_selected'] = curses.color_pair(14) | curses.A_BOLD | curses.A_REVERSE
        self.colour_codes['input'] = curses.color_pair(7) | curses.A_DIM | curses.A_REVERSE
