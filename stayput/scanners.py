"""
Scanners are responsible for locating and creating node objects from a data source. They must
also implement a method that provides the actual contents for the node.
"""

import os
import os.path


def empty_scanner(*args, **kwargs):
    """An empty stub scanner."""
    pass


def create_filesystem_provider(filename, *args, **kwargs):
    """Creates a new provider function for the specified file."""
    def provide():
        with open(filename, 'r') as f:
            return f.read()
    return provide

def filesystem_scanner(site, *args, **kwargs):
    """A scanner that finds items from the file system."""
    from stayput.items import Node
    all = []

    def walk_path(path):
        all = []
        for directory, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full = os.path.join(directory, filename)
                relative = os.path.relpath(full, path)
                normalized = relative.replace(os.path.pathsep, '/')

                fingerprint = int(os.path.getmtime(full))

                all.append((full, normalized, fingerprint))
        return all

    for path, key, fingerprint in walk_path(site.items_path):
        site.items[key] = Node(key, content_provider=create_filesystem_provider(path), fingerprint=fingerprint)

    for path, key, fingerprint in walk_path(site.templates_path):
        site.templates[key] = Node(key, fingerprint=fingerprint)
