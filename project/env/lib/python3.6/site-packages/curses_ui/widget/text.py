from curses_ui.event import key
from curses_ui.interface import TabAware
from curses_ui.widget import BaseWidget, SelectableWidget


class LabelWidget(BaseWidget):
    """
    A basic single-line text area
    """

    def __init__(self, base, text='', colour=None, auto_width=True, height=1, **kwargs):
        super(LabelWidget, self).__init__(base, height=height, **kwargs)
        self.text = text
        self.colour = colour
        self.auto_width = auto_width

        if self.auto_width:
            self.width = len(text)

    def paint_content(self):
        self.write(0, 0, self.text, self.colour)

    def set_text(self, text):
        """
        Set the text content and repaint
        :param text: string
        :return:
        """
        self.text = text

        if self.auto_width:
            self.width = len(text)

        self.paint(clear=True, refresh=True)


class MultiLineLabelWidget(BaseWidget):
    """
    A basic multi-line text area
    """

    def __init__(self, base, lines=None, colour=None, **kwargs):
        super(MultiLineLabelWidget, self).__init__(base, **kwargs)
        self.lines = lines if lines else []
        self.colour = colour

    def paint_content(self):
        y = 0
        for line in self.lines:
            self.write(y, 0, line, self.colour)
            y += 1

    def set_lines(self, lines):
        """
        Set all lines and repaint
        :param lines: array
        :return:
        """
        self.lines = lines
        self.paint(clear=True, refresh=True)

    def add_line(self, line):
        self.lines.append(line)
        self.paint(clear=True, refresh=True)


class TextWidget(SelectableWidget):
    """
    A basic single-line text area
    """

    def __init__(self, base, value='', password_char=None, height=1, **kwargs):
        super(TextWidget, self).__init__(base, height=height, **kwargs)
        self._value = value
        self.password_char = password_char
        self.get_dispatcher().subscribe(self.on_key_press, ['key.press'])

    def paint_content(self):
        width = self.get_dimensions()[4]

        if self.password_char is None:
            value = self._value[max(0, len(self._value) - width):]
        else:
            value = self.password_char * len(self._value)

        if self.selected:
            value += '_'

        self.write(0, 0, "{{: <{}s}}".format(width).format(value), 'input_selected' if self.selected else 'input')

    @property
    def value(self):
        """
        Get the value of the text widget
        :return: string
        """
        return self._value

    @value.setter
    def value(self, s):
        """
        Set the text content and repaint
        :param s: string
        :return:
        """
        self._value = s
        self.paint(clear=True, refresh=True)

    def on_key_press(self, event):
        if not self.selected:
            return

        if event.key == key.BACKSPACE:
            if len(self.value) == 0:
                return
            elif len(self._value) == 1:
                self.value = ''
            else:
                self.value = self._value[:len(self._value) - 1]

        elif (128 > event.key > 32) or event.key == key.SPACE:
            self.value = self._value + chr(event.key)

        elif event.key == key.ENTER:
            if isinstance(self.get_screen(), TabAware):
                event.handled = True
                self.get_screen().tab_next()

    def set_selected(self, selected):
        super(TextWidget, self).set_selected(selected)
