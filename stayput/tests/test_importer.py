import unittest
from os import path

from stayput.importer import import_file

FIXTURE = path.abspath(path.join(path.dirname(__file__), 'fixtures', 'import_test.py'))


class TestImporter(unittest.TestCase):

    # see fixtures/import_test.py.
    def test_import(self):
        result = import_file(FIXTURE)

        self.assertTrue(hasattr(result.test, '__call__'))
        self.assertEqual('Test', result.test())
        self.assertEqual(123, result.stuff['test'])
