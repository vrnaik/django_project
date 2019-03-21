import threading


class Dispatcher(object):
    def __init__(self):
        super(Dispatcher, self).__init__()
        self.listeners = {}
        self.subscribers = []

    def subscribe(self, fn, events=None):
        """
        Subscribe to one or more events
        :param fn: callable with signature fn(string event, dict args)
        :param events: string or an array of string, if None then listen for all events
        :return:
        """
        if isinstance(events, basestring):
            events = [events]

        if events is None:
            self.subscribers.append(fn)
        else:
            for event in events:
                if event not in self.listeners:
                    self.listeners[event] = []
                self.listeners[event].append(fn)

    def notify(self, event):
        """
        Notify all subscribers in a thread.
        :param event: Event
        :return: int Number of listeners notified
        """

        def notify_runner(e, subscribers, listeners):
            for subscriber in subscribers:
                subscriber(e)
                if e.handled:
                    return

            if e.name in listeners:
                for subscriber in listeners[e.name]:
                    subscriber(e)
                    if e.handled:
                        return

        t = threading.Thread(target=notify_runner,
                             kwargs={'e': event, 'subscribers': self.subscribers, 'listeners': self.listeners})
        t.daemon = False
        t.start()


class Event(object):
    def __init__(self, name):
        super(Event, self).__init__()
        self.name = name
        self.handled = False
