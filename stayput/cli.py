import os
import sys
from importlib import machinery as imp

from stayput import Site


def main():
    cwd = os.path.abspath(os.getcwd())

    # No configuration, no site to build.
    if not os.path.exists(os.path.join(cwd, 'stayput.py')):
        print("Error: stayput.py not found.")
        sys.exit(1)

    # Create site object and scan for items
    site = Site(root_path=cwd)
    site.scan()

    # do terrible things
    try:
        loader = imp.SourceFileLoader('stayput', os.path.join(cwd, 'stayput.py'))
        config = loader.load_module()
        config.configure(site)
    except Exception as e:
        print(e)
        sys.exit(1)

    # TODO clean up this mess and move compilation steps elsewhere
    for key, item in site.items.items():
        route = site.router(item)
        baseroute = os.path.dirname(route)
        content = site.template_item(item)
        os.makedirs(os.path.join(site.output_path, baseroute), exist_ok=True)
        with open(os.path.join(site.output_path, route), 'w') as f:
            f.write(content)
        print("Compiled %s." % key)
