import os.path

from stayput.builder import Builder
from stayput.tests import TestCase

TEMPLATES_FIXTURE = os.path.join(os.path.dirname(__file__), 'fixtures', 'templates')


class TestBuilder(TestCase):

    def setUp(self):
        self.site = self.make_site()
        self.site.items['a'] = self.make_item('a', content='a', fingerprint=1)
        self.site.items['b'] = self.make_item('b', content='b', fingerprint=1)
        self.manifest = {
            'items': {
                'a': 1,
                'b': 1
            },
            'templates': {
            }
        }
        self.builder = Builder(self.site)

    def test_scan_clean(self):
        self.builder.scan()

        self.assertIn('a', self.builder.dirty)
        self.assertIn('b', self.builder.dirty)

    def test_scan_clean_manifest(self):
        self.builder.load_manifest(self.manifest)
        self.builder.scan()

        self.assertFalse(self.builder.dirty)

    def test_scan_change_with_manifest(self):
        self.manifest['items']['a'] = 0
        self.builder.load_manifest(self.manifest)
        self.builder.scan()

        self.assertIn('a', self.builder.dirty)
        self.assertNotIn('b', self.builder.dirty)

    def test_scan_new_with_manifest(self):
        self.site.items['c'] = self.make_item('c', content='c', fingerprint=1)
        self.builder.load_manifest(self.manifest)
        self.builder.scan()

        self.assertIn('c', self.builder.dirty)

    def test_scan_deleted_with_manifest(self):
        del self.site.items['b']
        self.builder.load_manifest(self.manifest)
        self.builder.scan()

        self.assertIn('b', self.builder.deleted)

    def test_scan_template_change_with_manifest(self):
        # Use real template fixture.
        self.site.templates_path = TEMPLATES_FIXTURE
        self.manifest['templates']['template'] = None
        self.builder.load_manifest(self.manifest)
        self.builder.scan()

        self.assertIn('a', self.builder.dirty)
        self.assertIn('b', self.builder.dirty)

    def test_build_manifest(self):
        # Use real template fixture.
        self.site.templates_path = TEMPLATES_FIXTURE
        self.builder.scan()
        manifest = self.builder.build_manifest()

        self.assertIn('items', manifest)
        self.assertEqual(2, len(manifest['items']))
        self.assertEqual(1, manifest['items']['a'])
        self.assertEqual(1, manifest['items']['b'])
        self.assertIn('templates', manifest)
        self.assertEqual(1, len(manifest['templates']))
