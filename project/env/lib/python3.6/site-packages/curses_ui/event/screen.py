from curses_ui.event import Event


class ExitEvent(Event):
    """
    Screen is notifying any managers it wants to exit
    """

    EVENT_NAME = 'screen.exit'

    def __init__(self, screen_id):
        super(ExitEvent, self).__init__(self.EVENT_NAME)
        self.screen_id = screen_id
