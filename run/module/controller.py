import logging
from ..helpers import sformat
from ..task import CallTaskSignal, DoneTaskSignal, FailTaskSignal
from ..settings import settings  # @UnusedImport


class Controller:

    # Public

    def __init__(self, *, compact=settings.compact, plain=settings.plain):
        self.__compact = compact
        self.__plain = plain
        self.__stack = []

    def __call__(self, signal):
        # Stack operations
        if isinstance(signal, CallTaskSignal):
            self.__stack.append(signal.task)
        formatted_stack = self.__format_stack(self.__stack)
        if isinstance(signal, (DoneTaskSignal, FailTaskSignal)):
            self.__stack.pop()
        # Logging operations
        formatted_signal = '[+] '
        if formatted_signal:
            message = formatted_signal + formatted_stack
            logger = logging.getLogger('task')
            logger.info(message)

    # Private

    def __format_stack(self, stack):
        names = []
        if len(stack) >= 1:
            previous = self.__stack[0]
            name = previous.meta_qualname
            if not self.__plain:
                name = sformat(name, previous.meta_style, settings.styles)
            names.append(name)
            for task in stack[1:]:
                current = task
                if current.meta_module == previous.meta_module:
                    name = current.meta_name
                    if not self.__plain:
                        name = sformat(name, current.meta_style, settings.styles)
                    names.append(name)
                else:
                    name = current.meta_qualname
                    if not self.__plain:
                        name = sformat(name, current.meta_style, settings.styles)
                    names.append(name)
                previous = current
        return '/'.join(filter(None, names))
