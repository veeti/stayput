import os
import sys
import json

from stayput import Site, Builder
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

    builder = Builder(site)

    # Load cached manifest for incremental build
    manifest = None
    manifest_path = os.path.join(site.cache_path, 'manifest.json')
    try:
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r') as f:
                manifest = json.loads(f.read())
    except ValueError:
        pass

    # Parse manifest
    if manifest:
        builder.load_manifest(manifest)

    builder.scan()

    # Build each item
    for key in builder.dirty:
        builder.build(key)
        print("\x1b[1mOK\x1b[0m %s" % key)

    print("Done. Built \x1b[1m%d\x1b[0m items. \x1b[1m%d\x1b[0m up to date." % (len(builder.dirty),
        len(site.items) - len(builder.dirty)))

    # Write manifest
    if not os.path.exists(site.cache_path):
        os.makedirs(site.cache_path)
    with open(manifest_path, 'w') as f:
        f.write(json.dumps(builder.build_manifest()))