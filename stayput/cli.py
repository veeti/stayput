import os
import sys
import json

from stayput import Site
from stayput.build import load_manifest, save_manifest, build_item
from stayput.incremental import build_manifest, scan_work
from stayput.importer import import_file


def main():
    cwd = os.path.abspath(os.getcwd())

    # No configuration, no site to build.
    if not os.path.exists(os.path.join(cwd, 'stayput.py')):
        print("Error: stayput.py not found.")
        sys.exit(1)

    # Create site object and scan for items
    site = Site(root_path=cwd)
    site.scan()

    # Configure the site
    try:
        config = import_file(os.path.join(cwd, 'stayput.py'))
        config.configure(site)
    except Exception as e:
        print(e)
        sys.exit(1)

    # Load cached manifest and build current for incremental build
    cached_manifest = load_manifest(site)
    manifest = build_manifest(site)
    print(cached_manifest)
    print(manifest)

    # Scan for incremental build
    work = scan_work(site, cached_manifest, manifest)

    # Calculate nice numbers
    todo = len(work.dirty)
    clean = len(site.items) - todo

    # Build dirty items
    for key in work.dirty:
        build_item(site, site.items[key])
        print("\x1b[1mOK\x1b[0m %s" % key)

    print("Built \x1b[1m%d\x1b[0m items. \x1b[1m%d\x1b[0m up to date. \x1b[1m%d\x1b[0m total." % (todo, clean, todo + clean))

    # Write manifest
    save_manifest(site, manifest)