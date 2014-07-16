import os
import unittest
from io import StringIO
from functools import partial
from unittest.mock import patch
from run.cluster.find import find

class find_Test(unittest.TestCase):

    # Public

    def setUp(self):
        self.stdout = patch('sys.stdout', new_callable=StringIO).start()
        self.addCleanup(patch.stopall)
        self.pfind = partial(find, basedir=self._basedir)

    def test_find(self):
        modules = list(self.pfind(file='runfile.py'))
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0].__name__, 'Module1')
        self.assertEqual(
            self.stdout.getvalue(),
            'Hits runfile.py\n')

    def test_find_recursively(self):
        modules = list(self.pfind(file='runfile.py', recursively=True))
        self.assertEqual(len(modules), 3)
        self.assertEqual(modules[0].__name__, 'Module1')
        self.assertEqual(modules[1].__name__, 'Module2')
        self.assertEqual(modules[2].__name__, 'Module3')
        self.assertEqual(
            self.stdout.getvalue(),
            'Hits runfile.py\n'
            'Hits dir/runfile.py\n'
            'Hits dir/subdir/runfile.py\n')

    def test_find_with_names(self):
        modules = list(self.pfind(
            names=['name1'], file='runfile.py', recursively=True))
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0].__name__, 'Module1')

    def test_find_with_tags(self):
        modules = list(self.pfind(
            tags=['tag2'], file='runfile.py', recursively=True))
        self.assertEqual(len(modules), 1)
        self.assertEqual(modules[0].__name__, 'Module2')

    # Protected

    @property
    def _basedir(self):
        return os.path.join(os.path.dirname(__file__), 'fixtures')
