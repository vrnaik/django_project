import threading

from curses_ui.event.key import KeyPressEvent
from curses_ui.event.screen import ExitEvent
from curses_ui.exception import ScreenException


class ScreenManager(object):
    """
    Manages a pool of screens and their input.
    """

    def __init__(self, stdscr, colour_pack, start_runner=True):
        super(ScreenManager, self).__init__()
        self.stdscr = stdscr
        self.colour_pack = colour_pack
        self.screens = {}
        self.active_screen = None
        self.screen_locks = {}
        self.key_runner_active = False

        if start_runner:
            self.start_key_runner()

    def add_screen(self, screen_id, cls, kwargs=None, activate=False):
        """
        Create and build a screen, returning the instance.
        :param screen_id: string
        :param cls: class
        :param kwargs: dict of screen constructor args, `colour_pack` will be overridden
        :param activate: bool
        :return: Screen
        """
        if kwargs is None:
            kwargs = {}

        if screen_id in self.screens:
            raise ScreenException("A screen with ID '{}' is already registered".format(screen_id))

        kwargs['colour_pack'] = self.colour_pack
        kwargs['screen_id'] = screen_id

        self.screens[screen_id] = cls(**kwargs)
        self.screens[screen_id].build(self.stdscr)

        if activate:
            self.set_active_screen(screen_id)

        return self.screens[screen_id]

    def get_screen(self, screen_id):
        """
        Return a registered screen by ID
        :param screen_id: string
        :return:
        """
        return self.screens[screen_id]

    def has_screen(self, screen_id):
        """
        Check if a screen ID has been registered with the manager
        :param screen_id: string
        :return: bool
        """
        return screen_id in self.screens

    def paint(self):
        """
        Fully repaint the active screen
        :return:
        """
        if self.active_screen is None:
            self.stdscr.clear()
            self.stdscr.refresh()
            return

        self.screens[self.active_screen].paint(clear=True, refresh=True)

    def set_active_screen(self, screen_id):
        """
        Set the active screen
        :param screen_id: string
        :return:
        """
        if screen_id is not None and screen_id not in self.screens:
            raise ScreenException("Screen {} is not registered with the manager".format(screen_id))

        if self.active_screen is not None:
            self.screens[self.active_screen].active = False

        self.active_screen = screen_id

        if self.active_screen is not None:
            self.screens[self.active_screen].active = True

        self.paint()

    def modal(self, screen_id):
        """
        Set the active screen to `screen_id`, wait for it to exit then return to the current screen.
        :param screen_id: string
        :return:
        """
        if screen_id not in self.screens:
            raise ScreenException("Screen {} is not registered with the manager".format(screen_id))

        former = self.active_screen
        self.set_active_screen(screen_id)
        self.wait_for_exit(screen_id)
        self.set_active_screen(former)

    def start_key_runner(self):
        """
        Start listening on the keyboard, notify the _active_ screen only of key presses
        :return:
        """
        if self.key_runner_active:
            return

        self.key_runner_active = True

        def key_runner_thread(mgr):
            while mgr.key_runner_active:
                c = mgr.stdscr.getch()
                if mgr.active_screen and mgr.key_runner_active:
                    mgr.screens[mgr.active_screen].dispatcher.notify(KeyPressEvent(c))

        t = threading.Thread(target=key_runner_thread, kwargs={'mgr': self})
        t.daemon = True
        t.start()

    def stop_key_runner(self):
        """
        Disable the key listener, preventing further keyboard notifications
        :return:
        """
        self.key_runner_active = False

    def wait_for_exit(self, screen_id=None):
        """
        Let a screen run and wait for it to pass an exit request
        :param screen_id: string If None, the active screen will be used
        :return:
        """
        if screen_id is None:
            screen_id = self.active_screen

        if screen_id not in self.screens:
            return

        if screen_id not in self.screen_locks:
            self.screens[screen_id].dispatcher.subscribe(self.exit_flag, ExitEvent.EVENT_NAME)
            self.screen_locks[screen_id] = threading.Lock()

        self.screen_locks[screen_id].acquire(False)  # Lock the screen, ignore if it was already locked
        self.screen_locks[screen_id].acquire(True)  # Wait for it to unlock

    def exit_flag(self, e):
        if e.screen_id in self.screen_locks:
            self.screen_locks[e.screen_id].release()

        e.handled = True
