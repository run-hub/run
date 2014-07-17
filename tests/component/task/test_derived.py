import unittest
from unittest.mock import Mock
from run.task.derived import DerivedTask

class DerivedTaskTest(unittest.TestCase):

    # Public

    def setUp(self):
        self.MockTask = self._make_mock_task_class()
        self.task = self.MockTask('task', meta_module=None)

    def test___call__(self):
        self.args = ('arg1',)
        self.kwargs = {'kwarg1': 'kwarg1'}
        self.assertEqual(self.task(*self.args, **self.kwargs), 'value')

    def test_meta_docstring(self):
        self.assertTrue(self.task.meta_docstring)

    def test_meta_signature(self):
        self.assertTrue(self.task.meta_signature)

    # Protected

    def _make_mock_task_class(self):
        class MockTask(DerivedTask):
            # Protected
            _task = Mock(return_value='value')
        return MockTask
