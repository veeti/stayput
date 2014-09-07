import os.path

from stayput.incremental import compare_items

class Builder(object):

    def __init__(self, site):
        self.site = site
        self.cached_manifest = None
        self.dirty = set()
        self.deleted = set()

    def load_manifest(self, manifest):
        self.clear()
        self.cached_manifest = manifest

    def build_manifest(self):
        items = {}
        templates = {}

        # Load templates if there are any.
        # TODO refactor: Templates should be scanned into the site.
        if os.path.exists(self.site.templates_path):
            for directory, dirnames, filenames in os.walk(self.site.templates_path):
                for filename in filenames:
                    full = os.path.join(directory, filename)
                    relative = os.path.relpath(full, self.site.templates_path)
                    normalized = relative.replace(os.path.pathsep, '/')
                    templates[normalized] = os.path.getmtime(full)

        for key, item in self.site.items.items():
            items[key] = item.fingerprint

        return {'items': items, 'templates': templates}

    def scan(self):
        manifest = self.build_manifest()

        # Do an incremental build if we have an old manifest
        if self.cached_manifest:
            template_changes = compare_items(self.cached_manifest['templates'], manifest['templates'])
            if template_changes.new or template_changes.deleted or template_changes.dirty:
                self.invalidate_all()
                return

            changes = compare_items(self.cached_manifest['items'], manifest['items'])
            self.dirty = changes.dirty
            self.deleted = changes.deleted
        else:
            self.invalidate_all()

    def build(self, key):
        item = self.site.items[key]

        # Create paths
        output = os.path.join(self.site.output_path, self.site.route_item(item))
        directory = os.path.dirname(output)

        # Ensure directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write
        with open(output, 'w') as f:
            f.write(self.site.template_item(item))

    def invalidate_all(self):
        self.clear()
        for key, item in self.site.items.items():
            self.dirty.add(key)

    def clear(self):
        self.dirty.clear()
        self.deleted.clear()