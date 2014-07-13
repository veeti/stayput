from collections import Iterable
from os import path
import re

from stayput import scanners


class Site(object):

    def __init__(self, root_path, scanner=scanners.filesystem_scanner, router=None, templater=None):
        self.root_path = root_path
        self.items_path = path.join(root_path, 'items/')
        self.templates_path = path.join(root_path, 'templates/')
        self.output_path = path.join(root_path, 'output/')

        self.scanner = scanner
        self.items = {}
        self.templater = templater
        self.router = router

    def scan(self):
        self.items.clear()
        for item in self.scanner(self):
            self.items[item.path] = item

    def template_item(self, item):
        templater = self.templater
        if item.templater:
            templater = item.templater
        return templater(item)

    def route_item(self, item):
        router = self.router
        if item.router:
            router = item.router
        return router(item, site=self)

    def find_items_start_with(self, path):
        return list(filter(lambda node: node.path.startswith(path), self.items.values()))

    def find_items_regex(self, expression):
        expression = re.compile(expression)
        return list(filter(lambda node: expression.match(node.path), self.items.values()))

class Node(object):

    def __init__(self, path=None, content_provider=None, router=None, templater=None, filters=None):
        """
        :param path: The path to this node relative to the site
        :param content_provider: A function that when called returns the contents for the node
        :param router: A local router to be used for this node
        :param templater: A local templater to be used for this node
        :param filters: Nothing, a filter function or an iterable collection of filter functions
        """
        self.path = path
        self.content_provider = content_provider
        self.router = router
        self.templater = templater

        self.filters = []
        if filters:
            if isinstance(filters, Iterable):
                self.filters.extend(filters)
            else:
                self.filters.append(filters)

        self._cached_contents = None

    @property
    def contents(self):
        if not self.content_provider:
            raise NotImplementedError("This node does not have a content provider.")

        if not self._cached_contents:
            self._cached_contents = self.content_provider()
            for filter in self.filters:
                self._cached_contents = filter(content=self._cached_contents)

        return self._cached_contents
