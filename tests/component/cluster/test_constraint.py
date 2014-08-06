import unittest
import inspect
from unittest.mock import Mock
from run.cluster.constraint import Constraint


class ConstraintTest(unittest.TestCase):

    # Public

    def setUp(self):
        self.constraint = Constraint(Mock,
            names=['name1', 'name2'],
            tags=['tag1', 'tag2'])
        self.emitter = Mock()
        self.emitter.object = Mock
        self.emitter.object.meta_name = 'name1'
        self.emitter.object.meta_tags = ['tag1', 'tag3']
        self.emitter.module = inspect.getmodule(self.emitter.object)

    def test___call__not_skip(self):
        self.constraint(self.emitter)
        self.assertFalse(self.emitter.skip.called)

    def test___call___skip_object_is_imported(self):
        self.emitter.module = 'other_module'
        self.constraint(self.emitter)
        self.assertTrue(self.emitter.skip.called)

    def test___call___skip_object_is_not_type(self):
        self.emitter.object = Mock()
        self.constraint(self.emitter)
        self.assertTrue(self.emitter.skip.called)

    def test___call___skip_object_is_not_subclass(self):
        self.constraint = Constraint(Exception)
        self.constraint(self.emitter)
        self.assertTrue(self.emitter.skip.called)

    def test___call___skip_name_is_descriptor(self):
        self.emitter.object.meta_name = property(lambda self: self)
        self.emitter.object.meta_tags = ['tag1', 'tag3']
        self.constraint(self.emitter)
        self.assertTrue(self.emitter.skip.called)

    def test___call___skip_name_does_not_match(self):
        self.emitter.object.meta_name = 'name3'
        self.emitter.object.meta_tags = ['tag1', 'tag3']
        self.constraint(self.emitter)
        self.assertTrue(self.emitter.skip.called)

    def test___call___skip_tags_is_descriptor(self):
        self.emitter.object.meta_name = 'name1'
        self.emitter.object.meta_tags = property(lambda self: self)
        self.constraint(self.emitter)
        self.assertTrue(self.emitter.skip.called)

    def test___call___skip_tags_do_not_match(self):
        self.emitter.object.meta_name = 'name1'
        self.emitter.object.meta_tags = ['tag3']
        self.constraint(self.emitter)
