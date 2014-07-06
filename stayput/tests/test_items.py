import unittest

from stayput.items import Site, Node


def fake_scanner(*args, **kwargs):
    return [
        Node('a'),
        Node('b'),
        Node('c')
    ]


class TestSite(unittest.TestCase):

    def _make(self):
        site = Site(root_path='', scanner=fake_scanner)
        site.scan()
        return site

    def _make_templater(self, template='Test %contents%'):
        from stayput.templaters import SimpleTemplater
        templater = SimpleTemplater()
        templater.set_default_template(template)
        return templater

    def test_scan_items(self):
        site = self._make()
        site.scan()
        self.assertEqual(3, len(site.items))
        self.assertEqual(site.items['a'].path, 'a')

    def test_template_item(self):
        site = self._make()
        site.templater = self._make_templater('Global %contents%')
        site.items['a'].content_provider = lambda *args, **kwargs: 'abc'

        result = site.template_item(site.items['a'])
        self.assertEqual('Global abc', result)

    def test_template_item_local_templater(self):
        site = self._make()
        site.items['a'].templater = self._make_templater('Local %contents%')
        site.items['a'].content_provider = lambda *args, **kwargs: 'def'

        result = site.template_item(site.items['a'])
        self.assertEqual('Local def', result)

    def test_route_item(self):
        site = self._make()
        site.router = lambda item, *args, **kwargs: item.path

        result = site.route_item(site.items['a'])
        self.assertEqual('a', result)

class TestNode(unittest.TestCase):

    def test_no_content_provider_no_contents(self):
        with self.assertRaises(NotImplementedError):
            test = Node(content_provider=None).contents

    def test_content_provider(self):
        def provider():
            return "Hello"

        self.assertEqual("Hello", Node(content_provider=provider).contents)

    def test_content_provider_cached(self):
        self._counter = 0
        def provider():
            self._counter += 1
            return self._counter

        node = Node(content_provider=provider)
        self.assertEqual(1, node.contents)
        self.assertEqual(1, node.contents)
