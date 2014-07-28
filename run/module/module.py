import os
import inspect
from pprint import pprint
from collections import OrderedDict
from ..task import Task, NullTask
from .error import ModuleAttributeError
from .metaclass import ModuleMetaclass
from .signal import (InitiatedModuleSignal, SuccessedModuleSignal,
                     FailedModuleSignal)

class Module(Task, metaclass=ModuleMetaclass):

    # Public

    def __getattribute__(self, name):
        nested_name = None
        if '.' in name:
            name, nested_name = name.split('.', 1)
        try:
            task = super().__getattribute__(name)
        except AttributeError as exception:
            # To get correct AttributeError message here
            if isinstance(exception, ModuleAttributeError):
                raise
            raise ModuleAttributeError(
                'Module "{module}" has no task "{name}".'.
                format(module=self, name=name))
        if nested_name is not None:
            task = getattr(task, nested_name)
        return task

    @property
    def meta_basedir(self):
        if self.meta_is_main_module:
            basedir = os.path.dirname(inspect.getfile(type(self)))
        else:
            basedir = self.meta_module.meta_basedir
        return self._meta_params.get('basedir', basedir)

    @meta_basedir.setter
    def meta_basedir(self, value):
        self._meta_params['basedir'] = value

    @property
    def meta_cache(self):
        return self._meta_params.get('cache',
            self.meta_module.meta_cache)

    @meta_cache.setter
    def meta_cache(self, value):
        self._meta_params['cache'] = value

    @property
    def meta_is_main_module(self):
        """Module's main module status (is main module or not).
        """
        if self.meta_module:
            return False
        else:
            return True

    def meta_invoke(self, *args, **kwargs):
        return self.default(*args, **kwargs)

    @property
    def meta_main_module(self):
        if self.meta_is_main_module:
            return self
        else:
            return self.meta_module.meta_main_module

    @property
    def meta_name(self):
        if super().meta_name:
            return super().meta_name
        else:
            return self._default_meta_main_module_name

    @property
    def meta_tags(self):
        """Module's tag list.
        """
        return []

    @property
    def meta_tasks(self):
        """Module's tasks dict-like object.

        Dict contains task instances, not values.
        """
        tasks = {}
        for name, attr in vars(type(self)).items():
            if isinstance(attr, Task):
                tasks[name] = attr
        return tasks

    def list(self, task=None):
        """Print tasks.
        """
        if task != None:
            task = getattr(self, task)
        else:
            task = self
        names = []
        if isinstance(task, Module):
            for task in task.meta_tasks.values():
                names.append(task.meta_qualname)
            for name in sorted(names):
                self._print(name)
        else:
            raise TypeError(
                'Task "{task}" is not a module.'.
                format(task=task))

    def info(self, task=None):
        """Print information.
        """
        if task != None:
            task = getattr(self, task)
        else:
            task = self
        info = task.meta_qualname
        if isinstance(task, Task):
            info += task.meta_signature
        info += '\n---\n'
        info += 'Type: ' + task.meta_type
        info += '\n'
        info += 'Dependencies: ' + str(task.meta_dependencies)
        info += '\n'
        info += 'Default arguments: ' + str(task.meta_args)
        info += '\n'
        info += 'Default keyword arguments: ' + str(task.meta_kwargs)
        info += '\n---\n'
        info += task.meta_docstring
        self._print(info)

    def meta(self, task=None):
        """Print metadata.
        """
        if task != None:
            task = getattr(self, task)
        else:
            task = self
        meta = OrderedDict()
        for name in sorted(dir(task)):
            if name.startswith('meta_'):
                key = name.replace('meta_', '')
                meta[key] = getattr(task, name)
        self._pprint(meta)

    default = NullTask(
        meta_require=['list'],
    )

    # Protected

    _failed_signal_class = FailedModuleSignal  # Overriding
    _initiated_signal_class = InitiatedModuleSignal  # Overriding
    _print = staticmethod(print)
    _pprint = staticmethod(pprint)
    _successed_signal_class = SuccessedModuleSignal  # Overriding
