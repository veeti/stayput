from stayput.templaters import Templater, SimpleTemplater
from stayput.items import Node
from stayput.tests import TestCase


class TestTemplater(TestCase):
    """Test the base class for a templater."""

    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            Templater().template(None, None)


class TestSimpleTemplater(TestCase):
    """Tests the simple built-in templater."""

    def get_item(self):
        return self.make_item('test', content="Unit test")

    def get_templater(self):
        templater = SimpleTemplater()
        templater.default_template = "<html>%contents%</html>"
        return templater

    def test_replaces_content(self):
        self.assertEqual(self.get_templater().template(self.get_item(), site=None), "<html>Unit test</html>")

    def test_is_callable(self):
        self.assertEqual(self.get_templater()(self.get_item(), site=None), "<html>Unit test</html>")
