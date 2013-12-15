from lib31.python import cachedproperty

class AttributeMixin:
    
    #Public
    
    def __get__(self, namespace, namespace_class=None):
        try: 
            self.__namespace
        except AttributeError:
            self.__namespace = namespace
        if self.namespace != namespace:
            raise RuntimeError(
                'Attribute "{0}" is already attached to namespace "{1}"'.
                format(self, self.__namespace))
        return self
    
    def __set__(self, namespace, value):
        raise RuntimeError('Can\'t set attribute')

    @cachedproperty
    def namespace(self):
        try:
            return self.__namespace
        except AttributeError:
            raise RuntimeError(
                'Attribute "{0}" is not attached to any namespace'.
                format(self))
    
    
class DependentAttributeMixin(AttributeMixin):
    
    #Public
    
    def __init__(self, *args, **kwargs):
        self.__require = kwargs.pop('require', [])
        super().__init__(*args, **kwargs)
    
    def resolve(self):
        for task_name in self.__require:
            task = getattr(self.namespace, task_name)
            task()    