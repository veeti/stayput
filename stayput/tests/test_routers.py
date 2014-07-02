import unittest

from stayput.routers import simple_router
from stayput.items import Node

class TestSimpleRouter(unittest.TestCase):

    def _make_item(self, path):
        return Node(path)

    def test_index_is_index(self):
        self.assertEqual('index.html', simple_router(self._make_item('index.html')))

    def test_root_name_to_subdirectory_index(self):
        self.assertEqual('test/index.html', simple_router(self._make_item('test.html')))

    def test_subdirectories(self):
        self.assertEqual('posts/hello-world/index.html',
                         simple_router(self._make_item('posts/hello-world.html')))

    def test_extension(self):
        self.assertEqual('posts/hello-world/index.xml',
                         simple_router(self._make_item('posts/hello-world.xml')))