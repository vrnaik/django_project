from curses_ui.event import key
from curses_ui.widget.button import ButtonGroupWidget


class TabWidget(ButtonGroupWidget):
    """
    A button group widget that will not respond to the enter keypress
    """

    def __init__(self, base, group_name, **kwargs):
        super(TabWidget, self).__init__(base, group_name, **kwargs)

    def on_key_press(self, event):
        if not self.selected:
            return

        if event.key == key.ARROW_LEFT:
            self.set_index(self.index - 1)
            event.handled = True
        elif event.key == key.ARROW_RIGHT:
            self.set_index(self.index + 1)
            event.handled = True

    def paint_content(self):
        super(TabWidget, self).paint_content()
