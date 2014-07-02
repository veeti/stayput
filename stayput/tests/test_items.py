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
        return Site(root_path='', scanner=fake_scanner)

    def test_scan_items(self):
        site = self._make()
        site.scan()
        self.assertEqual(3, len(site.items))
        self.assertEqual(site.items['a'].path, 'a')


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
