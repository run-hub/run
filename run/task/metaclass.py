from abc import ABCMeta
from box.types import Null
from .build import build
from .null_module import NullModule


class TaskMetaclass(ABCMeta):

    # Public

    def __call__(self, *args, meta_module=Null, meta_updates=None, **kwargs):
        prototype = self.meta_prototype(
            *args, meta_class=self, meta_updates=meta_updates, **kwargs)
        if meta_module is Null:
            # Return prototype
            return prototype
        else:
            # Build and return task
            if meta_module is None:
                meta_module = NullModule()
            task = build(prototype, meta_module)
            return task
