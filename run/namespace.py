import types
import inspect
import importlib
from abc import ABCMeta
from lib31.python import cachedproperty
from .attribute import AttributeMixin

class NamespaceMeta(ABCMeta):
   
    #Public
   
    def __new__(cls, name, bases, attrs):
        for name, attr in attrs.items():
            if not name.startswith('_'):
                if (not isinstance(attr, type) and
                    not isinstance(attr, AttributeMixin)):
                    if isinstance(attr, types.FunctionType):
                        MethodTask = cls.__import('task', 'MethodTask')
                        attrs[name] = MethodTask(attr)
                    elif inspect.isdatadescriptor(attr):
                        PropertyVar = cls.__import('var', 'PropertyVar')
                        attrs[name] = PropertyVar(attr)
                    else:
                        ValueVar = cls.__import('var', 'ValueVar')
                        attrs[name] = ValueVar(attr) 
        return super().__new__(cls, name, bases, attrs)
    
    #Private
        
    @classmethod
    def __import(cls, module_name, attr_name):
        package_name = inspect.getmodule(cls).__package__
        module = importlib.import_module('.'+module_name, package_name)
        attr = getattr(module, attr_name)
        return attr  


class NamespaceMixin(metaclass=NamespaceMeta):
    
    #Protected

    @cachedproperty
    def _attributes(self):
        return NamespaceAttributes(self)


class NamespaceAttributes(dict):
    
    #Public
    
    def __init__(self, namespace):
        for cls in namespace.__class__.mro():
            for name, attr in cls.__dict__.items():
                if isinstance(attr, AttributeMixin):
                    self[name] = attr
    
    def find(self, attribute):
        for name, value in self.items():
            if attribute == value:
                return name
        else:
            raise ValueError('Attribute "{0}" is not found'.
                             format(attribute))
        
    def filter(self, attribute_class):
        return {name: value for name, value in self.items() 
                if isinstance(value, attribute_class)}               