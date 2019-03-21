from curses_ui.event import Event

ARROW_DOWN = 258
ARROW_UP = 259
ARROW_LEFT = 260
ARROW_RIGHT = 261
ENTER = 10
SPACE = 32
ESCAPE = 27
BACKSPACE = 263
TAB = 9
SHIFT_TAB = 353


class KeyPressEvent(Event):
    EVENT_NAME = 'key.press'

    def __init__(self, key):
        super(KeyPressEvent, self).__init__(self.EVENT_NAME)
        self.key = key
