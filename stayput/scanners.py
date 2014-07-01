"""
Scanners are responsible for locating and creating node objects from a data source. They must
also implement a method that provides the actual contents for the node.
"""

import os, os.path


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
    """
    A scanner that finds items from the file system.
    :param site: Site object
    :param args: Arguments
    :param kwargs: Arguments
    :return: List of items
    """
    from stayput.items import Node
    all = []
    items_path = os.path.join(site.root_path, 'items')
    for directory, dirnames, filenames in os.walk(items_path):
        for filename in filenames:
            full = os.path.join(directory, filename)
            relative = os.path.relpath(full, items_path)
            normalized = relative.replace(os.path.pathsep, '/')
            all.append(Node(normalized, content_provider=create_filesystem_provider(full)))
    return all
