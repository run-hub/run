import unittest
from unittest.mock import Mock
from run.attribute.attribute import Attribute

class AttributeTest(unittest.TestCase):
    
    #Public
    
    def setUp(self):
        MockAttribute = self._make_mock_attribute_class()
        self.attribute = MockAttribute(meta_module=None)

    def test(self):
        self.assertIsInstance(self.attribute, Attribute)
   
    def test___repr__(self):
        self.assertTrue(repr( self.attribute))  
    
    def test_meta_dispatcher(self):
        self.assertEqual(self.attribute.meta_dispatcher,
                         self.attribute.meta_module.meta_dispatcher)
    
    def test_meta_dispatcher_setter(self):        
        self.attribute.meta_dispatcher = 'dispatcher'
        self.assertEqual(self.attribute.meta_dispatcher, 'dispatcher')   
    
    def test_meta_docstring(self):
        self.assertEqual(self.attribute.meta_docstring, 'docstring') 
           
    def test_meta_module(self):
        #Null module
        self.assertNotEqual(self.attribute.meta_module, None)
        self.assertFalse(self.attribute.meta_module) 
    
    def test_meta_name(self):
        self.assertEqual(self.attribute.meta_name, '')       
           
    def test_meta_qualname(self):
        self.assertEqual(self.attribute.meta_qualname, '') 
    
    def test_meta_type(self):
        self.assertEqual(self.attribute.meta_type, 'MockAttribute')
        
    #Protected
    
    def _make_mock_attribute_class(self):
        class MockAttribute(Attribute):
            """docstring"""
            #Public
            __get__ = Mock()
            __set__ = Mock()
        return MockAttribute
        
        
class AttributeTest_with_module(AttributeTest):
    
    #Public
    
    def setUp(self):
        MockAttribute = self._make_mock_attribute_class()
        MockModule = self._make_mock_module_class()
        self.module = MockModule()
        self.attribute = MockAttribute(meta_module=self.module)
        self.module.meta_attributes = {'attribute': self.attribute}
        
    def test_meta_module(self):
        self.assertEqual(self.attribute.meta_module, self.module)
    
    def test_meta_name(self):
        self.assertEqual(self.attribute.meta_name, 'attribute')
        
    def test_meta_qualname(self):
        self.assertEqual(self.attribute.meta_qualname, 'module.attribute') 
        
    #Protected
    
    def _make_mock_module_class(self):
        class MockModule:
            #Public
            meta_attributes = {}
            meta_basedir = 'basedir'
            meta_dispatcher = 'dispatcher'
            meta_is_main_module = False    
            meta_name = 'module'
            meta_qualname = 'module'
        return MockModule
        
        
class AttributeTest_with_module_is_main(AttributeTest_with_module):
    
    #Public
    
    def setUp(self):
        MockAttribute = self._make_mock_attribute_class()
        MockModule = self._make_mock_module_class()
        MockMainModule = self._make_mock_main_module_class(MockModule)
        self.module = MockMainModule()
        self.attribute = MockAttribute(meta_module=self.module)
        self.module.meta_attributes = {'attribute': self.attribute}
        
    def test_meta_qualname(self):
        self.assertEqual(self.attribute.meta_qualname, '[module] attribute')
        
    #Protected
    
    def _make_mock_main_module_class(self, mock_module_class):
        class MockMainModule(mock_module_class):
            #Public
            meta_is_main_module = True
        return MockMainModule        


class AttributeTest_with_docstring(AttributeTest):
    
    #Public
    
    def setUp(self):
        MockAttribute = self._make_mock_attribute_class()
        self.docstring = 'new_docstring'
        self.attribute = MockAttribute(
            meta_docstring=self.docstring,
            meta_module=None)
    
    def test_meta_docstring(self):
        self.assertEqual(self.attribute.meta_docstring, self.docstring)