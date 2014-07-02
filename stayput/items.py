from os import path

from stayput import scanners

class Site(object):

    def __init__(self, root_path, scanner=scanners.filesystem_scanner):
        self.root_path = root_path
        self.items_path = path.join(root_path, 'items/')
        self.templates_path = path.join(root_path, 'templates/')
        self.output_path = path.join(root_path, 'output/')

        self.scanner = scanner
        self.items = {}
        self.templater = None
        self.router = None

    def scan(self):
        for item in self.scanner(self):
            self.items[item.path] = item


class Node(object):

    def __init__(self, path=None, content_provider=None):
        """
        :param path: The path to this node relative to the site
        :param content_provider: A function that when called returns the contents for the node
        """
        self.path = path
        self.content_provider = content_provider
        self._cached_contents = None

    @property
    def contents(self):
        if not self.content_provider:
            raise NotImplementedError("This node does not have a content provider.")

        if not self._cached_contents:
            self._cached_contents = self.content_provider()

        return self._cached_contents
