from abc import ABCMeta, abstractmethod

class Module(metaclass=ABCMeta):

    # Public

    @abstractmethod
    def meta_lookup(self, name):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_basedir(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_cache(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_chdir(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_dispatcher(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_fallback(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_fullname(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_is_main_module(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_qualname(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_main_module(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_plain(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_strict(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def meta_tasks(self):
        pass  # pragma: no cover