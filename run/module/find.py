import os
import inspect
from ..find import find
from .module import Module


class FindModule(Module):

    # Public

    default_recursively = True

    @classmethod
    def __meta_create__(cls, *args, meta_module, meta_updates, **kwargs):
        basedir = kwargs.pop('basedir', None)
        notfilepath = os.path.relpath(
            inspect.getfile(type(meta_module)), start=basedir)
        Module = cls._find(
            names=kwargs.pop('names', None),
            tags=kwargs.pop('tags', None),
            file=kwargs.pop('file', None),
            basedir=basedir,
            recursively=kwargs.pop('recursively', cls.default_recursively),
            filters=[{'notfilepath': notfilepath}],
            getfirst=True)
        module = Module(
            *args,
            meta_module=meta_module,
            meta_updates=meta_updates,
            **kwargs)
        return module

    # Protected

    _find = find
