from stayput.items import Site, Node, parse_metadata
from stayput.errors import MetadataValueError, NoTemplaterError, NoRouterError
from stayput.tests import TestCase


def fake_scanner(site, *args, **kwargs):
    site.items['a'] = Node('a')
    site.items['b'] = Node('b')
    site.items['c'] = Node('c')


class TestSite(TestCase):

    def test_scan_items(self):
        site = self.make_site(scanner=fake_scanner)
        site.scan()
        self.assertEqual(3, len(site.items))
        self.assertEqual(site.items['a'].path, 'a')

    def test_scan_items_clear(self):
        site = self.make_site(scanner=fake_scanner)
        site.scan()

        # rescan with new scanner
        def new_scanner(site, *args, **kwargs):
            site.items['d'] = self.make_item('d')
        site.scanner = new_scanner
        site.scan()

        self.assertEqual(1, len(site.items))
        self.assertIn('d', site.items)

    def test_template_item(self):
        site = self.make_site(templater=self.make_templater('Global %contents%'))
        site.items['a'] = self.make_item('a', content='abc')

        result = site.template_item(site.items['a'])
        self.assertEqual('Global abc', result)

    def test_template_item_local_templater(self):
        site = self.make_site(templater=self.make_templater('Global %contents%'))
        site.items['a'] = self.make_item('a', content='abc', templater=self.make_templater('Local %contents%'))

        result = site.template_item(site.items['a'])
        self.assertEqual('Local abc', result)

    def test_template_item_local_templater_no_global(self):
        site = self.make_site(templater=None)
        site.items['a'] = self.make_item('a', content='abc', templater=self.make_templater('Local %contents%'))

        result = site.template_item(site.items['a'])
        self.assertEqual('Local abc', result)

    def test_template_item_no_templater(self):
        site = self.make_site()
        site.items['a'] = self.make_item('a', content='a')
        with self.assertRaises(NoTemplaterError):
            site.template_item(site.items['a'])

    def test_route_item(self):
        site = self.make_site(router=lambda item, *args, **kwargs: item.path)
        site.items['a'] = self.make_item('a')

        result = site.route_item(site.items['a'])
        self.assertEqual('a', result)

    def test_route_item_local_router(self):
        site = self.make_site()
        site.router = lambda *args, **kwargs: 'global_route'
        site.items['a'] = self.make_item('a', router=lambda *a, **kw: 'local_route')

        result = site.route_item(site.items['a'])
        self.assertEqual('local_route', result)

    def test_route_item_local_router_no_global(self):
        site = self.make_site(router=None)
        site.items['a'] = self.make_item('a', router=lambda *a, **kw: 'local_route')

        result = site.route_item(site.items['a'])
        self.assertEqual('local_route', result)

    def test_route_item_no_router(self):
        site = self.make_site()
        site.items['a'] = self.make_item('a')

        with self.assertRaises(NoRouterError):
            site.route_item(site.items['a'])

    def test_find_items_starts_with(self):
        site = self.make_site()
        for key in ('a', 'aa', 'b'):
            site.items[key] = self.make_item(key)

        results = site.find_items_start_with('a')
        paths = [node.path for node in results]

        self.assertEqual(2, len(results))
        self.assertIn('a', paths)
        self.assertIn('aa', paths)

    def test_find_items_regular_expression(self):
        site = self.make_site()
        for key in ('123', '456', 'a2b', 'b'):
            site.items[key] = self.make_item(key)

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


class TestNode(TestCase):

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

        node = self.make_item(filters=filter)
        self.assertEqual(1, len(node.filters))
        self.assertIn(filter, node.filters)

    def test_filter_multiple_constructor(self):
        def filter(*args, **kwargs):
            pass

        def filter_two(*args, **kwargs):
            pass

        node = self.make_item(filters=[filter, filter_two])
        self.assertEqual(2, len(node.filters))
        self.assertIn(filter, node.filters)
        self.assertIn(filter_two, node.filters)

    def test_filter(self):
        def filter(content, *args, **kwargs):
            return content.replace('raw', 'filtered')

        node = self.make_item(filters=filter, content='raw')
        self.assertEqual('filtered', node.contents)

    def test_filter_order(self):
        def first(content, *args, **kwargs):
            return content.replace('a', 'b')

        def second(content, *args, **kwargs):
            return content.replace('b', 'c')

        node = self.make_item(filters=[first, second], content='a')
        self.assertEqual('c', node.contents)

    def test_filter_cached(self):
        self._counter = 0
        def filter(*args, **kwargs):
            self._counter += 1
            return self._counter

        node = self.make_item(filters=filter, content='raw')
        self.assertEqual(1, node.contents)
        self.assertEqual(1, node.contents)

    def test_empty_metadata_by_default(self):
        node = self.make_item(content='test')
        self.assertIsNotNone(node.metadata)
        self.assertEqual(0, len(node.metadata))

    def test_metadata_parsed_as_json(self):
        node = self.make_item(content=TEST_CONTENT_VALID_METADATA)
        self.assertEqual(123, node.metadata['test'])
        self.assertEqual('test', node.contents)

    def test_metadata_invalid_json(self):
        with self.assertRaises(MetadataValueError):
            meta = self.make_item(content=TEST_CONTENT_INVALID_METADATA).metadata

    def test_disable_metadata(self):
        node = self.make_item(content=TEST_CONTENT_VALID_METADATA, has_metadata=False)
        self.assertEqual(0, len(node.metadata))

    def test_no_content_no_metadata(self):
        with self.assertRaises(NotImplementedError):
            test = self.make_item(content_provider=None).metadata


class TestMetadataParser(TestCase):

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
