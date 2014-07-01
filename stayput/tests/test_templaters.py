import unittest
from unittest import mock

from stayput.templaters import Templater, SimpleTemplater

class TestTemplater(unittest.TestCase):
    """Test the base class for a templater."""

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            Templater().template(None)


class TestSimpleTemplater(unittest.TestCase):
    """Tests the simple built-in templater."""

    def get_item(self):
        item = mock.Mock()
        item.contents = "Unit test"
        return item

    def get_templater(self):
        templater = SimpleTemplater()
        templater.set_default_template("<html>%contents%</html>")
        return templater

    def test_replaces_content(self):
        self.assertEqual(self.get_templater().template(self.get_item()), "<html>Unit test</html>")

