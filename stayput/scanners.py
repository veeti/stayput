"""
Scanners are responsible for locating and creating node objects from a data source. They must
also implement a method that provides the actual contents for the node.
"""

import os
import os.path


def empty_scanner(*args, **kwargs):
    """A stub scanner that returns zero items."""
    return []


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
    for directory, dirnames, filenames in os.walk(site.items_path):
        for filename in filenames:
            full = os.path.join(directory, filename)
            relative = os.path.relpath(full, site.items_path)
            normalized = relative.replace(os.path.pathsep, '/')
            all.append(Node(normalized, content_provider=create_filesystem_provider(full),
                            fingerprint=int(os.path.getmtime(full))))
    return all
