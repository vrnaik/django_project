class CursesUiException(Exception):
    pass


class ScreenException(CursesUiException):
    pass


class InvalidArgumentException(CursesUiException):
    pass


class IndexOutOfRangeException(CursesUiException):
    pass
