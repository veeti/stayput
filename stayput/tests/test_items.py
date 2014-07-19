import unittest

from stayput.items import Site, Node, parse_metadata
from stayput.errors import MetadataValueError


def fake_scanner(*args, **kwargs):
    return [
        Node('a'),
        Node('b'),
        Node('c')
    ]


class TestSite(unittest.TestCase):

    def _make(self, root_path='', scanner=fake_scanner, **kwargs):
        site = Site(root_path, scanner=scanner, **kwargs)
        site.scan()
        return site

    def _make_templater(self, template='Test %contents%'):
        return lambda item, *args, **kwargs: template.replace('%contents%', item.contents)

    def test_scan_items(self):
        site = self._make()
        site.scan()
        self.assertEqual(3, len(site.items))
        self.assertEqual(site.items['a'].path, 'a')

    def test_scan_items_clear(self):
        site = self._make()
        site.scan()

        # rescan with new scanner
        site.scanner = lambda *args, **kwargs: [Node('d')]
        site.scan()

        self.assertEqual(1, len(site.items))
        self.assertIn('d', site.items)

    def test_template_item(self):
        site = self._make(templater=self._make_templater('Global %contents%'))
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
        site = self._make(router=lambda item, *args, **kwargs: item.path)

        result = site.route_item(site.items['a'])
        self.assertEqual('a', result)

    def test_route_item_local_router(self):
        site = self._make()
        site.items['a'].router = lambda *args, **kwargs: 'local_route'

        result = site.route_item(site.items['a'])
        self.assertEqual('local_route', result)

    def test_find_items_starts_with(self):
        site = self._make(scanner=lambda *args, **kwargs: [Node('a'), Node('aa'), Node('b')])

        results = site.find_items_start_with('a')
        paths = [node.path for node in results]

        self.assertEqual(2, len(results))
        self.assertIn('a', paths)
        self.assertIn('aa', paths)

    def test_find_items_regular_expression(self):
        site = self._make(scanner=lambda *args, **kwargs: [Node('123'), Node('456'), Node('a2b'), Node('b')])

        results = site.find_items_regex(r'[1-9]+')
        paths = [node.path for node in results]

        self.assertEqual(2, len(results))
        self.assertIn('123', paths)
        self.assertIn('456', paths)


TEST_CONTENT_VALID_METADATA = """---
{
  "test": 123
}
---
test"""

TEST_CONTENT_INVALID_METADATA = """---
not json
---
test"""


class TestNode(unittest.TestCase):

    def _make(self, content=None, content_provider=None, *args, **kwargs):
        if content:
            content_provider = lambda *args, **kwargs: content
        return Node(content_provider=content_provider, *args, **kwargs)

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

    def test_filter_single_constructor(self):
        def filter(*args, **kwargs):
            pass

        node = self._make(filters=filter)
        self.assertEqual(1, len(node.filters))
        self.assertIn(filter, node.filters)

    def test_filter_multiple_constructor(self):
        def filter(*args, **kwargs):
            pass

        def filter_two(*args, **kwargs):
            pass

        node = self._make(filters=[filter, filter_two])
        self.assertEqual(2, len(node.filters))
        self.assertIn(filter, node.filters)
        self.assertIn(filter_two, node.filters)

    def test_filter(self):
        def filter(content, *args, **kwargs):
            return content.replace('raw', 'filtered')

        node = self._make(filters=filter, content='raw')
        self.assertEqual('filtered', node.contents)

    def test_filter_order(self):
        def first(content, *args, **kwargs):
            return content.replace('a', 'b')

        def second(content, *args, **kwargs):
            return content.replace('b', 'c')

        node = self._make(filters=[first, second], content='a')
        self.assertEqual('c', node.contents)

    def test_filter_cached(self):
        self._counter = 0
        def filter(*args, **kwargs):
            self._counter += 1
            return self._counter

        node = self._make(filters=filter, content='raw')
        self.assertEqual(1, node.contents)
        self.assertEqual(1, node.contents)

    def test_empty_metadata_by_default(self):
        node = self._make(content='test')
        self.assertIsNotNone(node.metadata)
        self.assertEqual(0, len(node.metadata))

    def test_metadata_parsed_as_json(self):
        node = self._make(content=TEST_CONTENT_VALID_METADATA)
        self.assertEqual(123, node.metadata['test'])
        self.assertEqual('test', node.contents)

    def test_metadata_invalid_json(self):
        with self.assertRaises(MetadataValueError):
            meta = self._make(content=TEST_CONTENT_INVALID_METADATA).metadata

    def test_disable_metadata(self):
        node = self._make(content=TEST_CONTENT_VALID_METADATA, has_metadata=False)
        self.assertEqual(0, len(node.metadata))

    def test_no_content_no_metadata(self):
        with self.assertRaises(NotImplementedError):
            test = self._make(content_provider=None).metadata


class TestMetadataParser(unittest.TestCase):

    def test_no_metadata(self):
        meta, content = parse_metadata("Hello, world.")
        self.assertEqual("Hello, world.", content)

    def test_metadata(self):
        content = """---
{
hello
}
---
Hello, world."""
        meta, content = parse_metadata(content)
        self.assertEqual("""{
hello
}""", meta)
        self.assertEqual("Hello, world.", content)
