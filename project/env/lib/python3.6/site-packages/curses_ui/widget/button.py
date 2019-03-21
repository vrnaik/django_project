from curses_ui.event import Event, key
from curses_ui.widget import SelectableWidget


class ButtonWidget(SelectableWidget):
    """
    A button, press it, press it hard.
    """

    def __init__(self, base, name, title, auto_width=True, **kwargs):
        kwargs['height'] = 1
        super(ButtonWidget, self).__init__(base, **kwargs)
        self._name = name
        self._title = title
        self.auto_width = auto_width

        if self.auto_width and title:
            self.width = len(title) + 4

        self.get_dispatcher().subscribe(self.on_key_press, ['key.press'])

    def paint_content(self):
        self.write(0, 0, '[', 'frame')
        self.write(0, 1, ' {} '.format(self.title), 'title' if self.selected else 'default')
        self.write(0, len(self.title) + 3, ']', 'frame')

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        if self.auto_width:
            self.width = len(title) + 4
        self.paint(clear=True, refresh=True)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def on_key_press(self, event):
        if not self.selected:
            return

        if event.key == key.ENTER:
            self.get_dispatcher().notify(ButtonClickEvent(self))
            event.handled = True

    def set_selected(self, selected):
        super(ButtonWidget, self).set_selected(selected)


class ButtonGroupWidget(ButtonWidget):
    """
    A horizontal line of buttons
    """

    def __init__(self, base, group_name, **kwargs):
        kwargs['height'] = 1
        super(ButtonGroupWidget, self).__init__(base, name=None, title=None, **kwargs)
        self.buttons = []
        self.index = 0
        self.group_name = group_name

    def add_button(self, name, title):
        self.buttons.append((name, title))

        if self.auto_width:
            self.width = 1 + len(self.buttons)
            for name, title in self.buttons:
                self.width += len(title) + 2

    def paint_content(self):
        self.write(0, 0, '[', 'frame')
        x = 1
        index = 0

        for name, title in self.buttons:
            if index > 0:
                self.write(0, x - 1, '|', 'frame')

            self.write(0, x, ' {} '.format(title), 'selected' if self.selected and self.index == index else 'default')

            index += 1
            x += len(title) + 3

        self.write(0, x - 1, ']', 'frame')

    def set_index(self, index):
        if index >= len(self.buttons):
            index = 0

        if index < 0:
            index = len(self.buttons) - 1

        # Notify the event dispatcher of the index change, _after_ it has been actually changed
        former = self.index
        self.index = index
        self.paint(clear=False, refresh=True)

        if self.index != former:
            self.get_dispatcher().notify(ButtonIndexChangedEvent(self, former))

    def on_key_press(self, event):
        if not self.selected:
            return

        if event.key == key.ARROW_LEFT:
            self.set_index(self.index - 1)
            event.handled = True
        elif event.key == key.ARROW_RIGHT:
            self.set_index(self.index + 1)
            event.handled = True
        elif 0 <= self.index < len(self.buttons) and event.key == key.ENTER:
            self.get_dispatcher().notify(ButtonClickEvent(self))
            event.handled = True

    @property
    def name(self):
        if 0 <= self.index < len(self.buttons):
            return self.buttons[self.index][0]
        else:
            return None

    @name.setter
    def name(self, name):
        raise AttributeError("You cannot set the name of a ButtonGroupWidget")

    @property
    def title(self):
        if 0 <= self.index < len(self.buttons):
            return self.buttons[self.index][1]
        else:
            return None

    @title.setter
    def title(self, title):
        raise AttributeError("You cannot set the title of a ButtonGroupWidget")

    def set_selected(self, selected):
        super(ButtonGroupWidget, self).set_selected(selected)


class ButtonClickEvent(Event):
    """
    A button, or button group click

    The 'button' attribute will be a ButtonWidget or a ButtonGroup widget. Index will only be non-None if triggered
    via a button group.
    """

    EVENT_PREFIX = 'button.click.'

    def __init__(self, button):
        super(ButtonClickEvent, self).__init__(self.EVENT_PREFIX + button.name)
        self.button = button


class ButtonIndexChangedEvent(Event):
    """
    A button group index has changed value
    """

    EVENT_PREFIX = 'button.index.'

    def __init__(self, button_group, former_index):
        super(ButtonIndexChangedEvent, self).__init__(self.EVENT_PREFIX + button_group.group_name)
        self.button_group = button_group
        self.former_index = former_index
