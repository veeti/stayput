from stayput.incremental import compare_items

from stayput.tests import TestCase


class TestIncrementalCompare(TestCase):

    def test_unchanged(self):
        before = {
            'index.html': 1
        }
        after = {
            'index.html': 1
        }
        result = compare_items(before, after)

        self.assertNotIn('index.html', result.dirty)
        self.assertNotIn('index.html', result.new)
        self.assertNotIn('index.html', result.deleted)
        self.assertIn('index.html', result.unchanged)

    def test_changed(self):
        before = {
            'index.html': 1
        }
        after = {
            'index.html': 2
        }

        result = compare_items(before, after)

        self.assertIn('index.html', result.dirty)
        self.assertNotIn('index.html', result.new)
        self.assertNotIn('index.html', result.deleted)
        self.assertNotIn('index.html', result.unchanged)

    def test_new(self):
        before = {
            'index.html': 1
        }

        after = {
            'index.html': 2,
            'new.html': 1
        }
        result = compare_items(before, after)

        self.assertIn('new.html', result.new)
        self.assertIn('new.html', result.dirty)
        self.assertNotIn('new.html', result.deleted)
        self.assertNotIn('new.html', result.unchanged)

    def test_deleted(self):
        before = {
            'index.html': 1
        }
        after = {}
        result = compare_items(before, after)

        self.assertIn('index.html', result.deleted)
        self.assertNotIn('index.html', result.new)
        self.assertNotIn('index.html', result.dirty)
        self.assertNotIn('index.html', result.unchanged)
