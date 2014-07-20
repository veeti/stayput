import unittest
import tempfile
import os

from stayput.scanners import create_filesystem_provider


class TestFilesystemContentProvider(unittest.TestCase):

    def setUp(self):
        self.file = tempfile.mktemp('stayput')
        with open(self.file, 'w') as f:
            f.write('TestFilesystemContentProvider')

    def tearDown(self):
        os.unlink(self.file)

    def test_provides_contents(self):
        provider = create_filesystem_provider(self.file)
        self.assertEqual('TestFilesystemContentProvider', provider())
