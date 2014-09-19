from box.functools import Function
from ...module import Module
from ...task import FunctionTask


class AutoModule(Module):
    """Module with auto generated tasks from sources.

    For every function (callable or box.functools.Function) in every source
    module creates :class:`run.task.FunctionTask` object. It may to be
    used as regular run's tasks.

    Parameters
    ----------
    sources: list
        Python objects with attributes include functions.

    Examples
    --------
    Usage example::

      >>> module = AutoModule([os.path], meta_module=None)
      >>> module.list()
      abspath
      ...
      splitext
      >>> module.info('basename')
      basename(p)
      ...
      Returns the final component of a pathname
      >>> module.basename('dir/file.py')
      'file.py'
    """

    # Public

    def __init__(self, sources=None, *args, **kwargs):
        if sources is None:
            sources = []
        self.__sources = sources + self._default_sources
        for task_name, task_function in self.__functions.items():
            if not hasattr(type(self), task_name):
                task = FunctionTask(task_function, meta_module=self)
                setattr(type(self), task_name, task)
        super().__init__(*args, **kwargs)

    @property
    def meta_docstring(self):
        return self.meta_get_parameter(
            'docstring',
            inherit=False,
            default=('AutoModule with following sources: {sources}'.
                     format(sources=self.__sources)))

    # Protected

    _default_sources = []

    # Private

    @property
    def __functions(self):
        functions = {}
        for obj in reversed(self.__sources):
            for name in dir(obj):
                if name.startswith('_'):
                    continue
                attr = getattr(obj, name)
                if not callable(attr):
                    continue
                if isinstance(attr, type):
                    if not isinstance(attr, Function):
                        continue
                functions[name] = attr
        return functions
