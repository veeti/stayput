from stayput.incremental import compare_items, build_manifest, scan_work

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


class TestBuildManifest(TestCase):

    def test_build_manifest(self):
        site = self.make_site()
        site.items['a'] = self.make_item('a', fingerprint=123)
        site.templates['b'] = self.make_item('b', fingerprint=456)
        
        manifest = build_manifest(site)
        self.assertIn('a', manifest['items'])
        self.assertEqual(123, manifest['items']['a'])
        self.assertIn('b', manifest['templates'])
        self.assertEqual(456, manifest['templates']['b'])


class TestScanWork(TestCase):

    def setUp(self):
        self.site = self.make_site()
        self.site.items['a'] = self.make_item('a', content='a', fingerprint=1)
        self.site.items['b'] = self.make_item('b', content='b', fingerprint=1)
        self.site.templates['c'] = self.make_item('c', fingerprint=1)

        self.manifest = {
            'items': {
                'a': 1,
                'b': 1
            },
            'templates': {
                'c': 1
            }
        }

    def test_scan_no_manifest(self):
        work = scan_work(self.site, None)

        self.assertIn('a', work.dirty)
        self.assertIn('b', work.dirty)

    def test_scan_clean_manifest(self):
        work = scan_work(self.site, self.manifest)

        self.assertFalse(work.dirty)
        self.assertFalse(work.deleted)

    def test_scan_change_with_manifest(self):
        self.manifest['items']['a'] = 0
        work = scan_work(self.site, self.manifest)

        self.assertIn('a', work.dirty)
        self.assertNotIn('b', work.dirty)

    def test_scan_new_with_manifest(self):
        self.site.items['c'] = self.make_item('c', content='c', fingerprint=1)
        work = scan_work(self.site, self.manifest)

        self.assertIn('c', work.dirty)

    def test_scan_deleted_with_manifest(self):
        del self.site.items['b']
        work = scan_work(self.site, self.manifest)

        self.assertIn('b', work.deleted)

    def test_scan_template_change_with_manifest(self):
        self.site.templates['c'].fingerprint = "changed"
        work = scan_work(self.site, self.manifest)

        self.assertIn('a', work.dirty)
        self.assertIn('b', work.dirty)
