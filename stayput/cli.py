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

    # Compile each item
    for key, item in site.items.items():
        # Generare route and output
        route = site.route_item(item)
        output = site.template_item(item)

        # Create output paths
        file = os.path.join(site.output_path, route)
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write
        with (open(file, 'w')) as f:
            f.write(output)

        print("\x1b[1mOK\x1b[0m %s" % key)
