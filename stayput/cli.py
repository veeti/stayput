import os
import sys

from stayput import Site
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

    # TODO clean up this mess and move compilation steps elsewhere
    for key, item in site.items.items():
        route = site.route_item(item)
        content = site.template_item(item)
        output = os.path.join(site.output_path, route)
        output_dir = os.path.dirname(output)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output, 'w') as f:
            f.write(content)
        print("Compiled %s." % key)
