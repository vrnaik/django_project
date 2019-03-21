from abc import ABCMeta, abstractmethod


class Selectable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_selected(self, selected):
        pass


class TabAware(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def tab_next(self):
        pass

    @abstractmethod
    def tab_previous(self):
        pass

    @abstractmethod
    def set_tab_index(self, index):
        pass
