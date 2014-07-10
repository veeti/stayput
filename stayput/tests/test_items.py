import unittest

from stayput.items import Site, Node


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


class TestNode(unittest.TestCase):

    def _make(self, *args, **kwargs):
        return Node(*args, **kwargs)

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

        def content(*args, **kwargs):
            return 'raw'

        node = self._make(filters=filter, content_provider=content)
        self.assertEqual('filtered', node.contents)

    def test_filter_order(self):
        def first(content, *args, **kwargs):
            return content.replace('a', 'b')

        def second(content, *args, **kwargs):
            return content.replace('b', 'c')

        def content(*args, **kwargs):
            return 'a'

        node = self._make(filters=[first, second], content_provider=content)
        self.assertEqual('c', node.contents)

    def test_filter_cached(self):
        self._counter = 0
        def filter(*args, **kwargs):
            self._counter += 1
            return self._counter

        def content(*args, **kwargs):
            return 'raw'

        node = self._make(filters=filter, content_provider=content)
        self.assertEqual(1, node.contents)
        self.assertEqual(1, node.contents)
