import unittest

from stayput.items import Site, Node


class TestCase(unittest.TestCase):

    def make_site(self, root_path='', scanner=lambda *args, **kwargs: [], **kwargs):
        site = Site(root_path, scanner=scanner, **kwargs)
        return site

    def make_templater(self, template='Test %contents%'):
        return lambda item, *args, **kwargs: template.replace('%contents%', item.contents)

    def make_item(self, path='test', content=None, content_provider=None, *args, **kwargs):
        if content:
            content_provider = lambda *args, **kwargs: content
        return Node(path=path, content_provider=content_provider, *args, **kwargs)
