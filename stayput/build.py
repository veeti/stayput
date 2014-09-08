import os.path
import json

def get_manifest_path(site):
    return os.path.join(site.cache_path, 'manifest.json')


def load_manifest(site):
    path = get_manifest_path(site)
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.loads(f.read())


def save_manifest(site, manifest):
    path = get_manifest_path(site)

    # Ensure cache exists
    if not os.path.exists(site.cache_path):
        os.makedirs(site.cache_path)

    with open(path, 'w') as f:
        f.write(json.dumps(manifest))


def build_item(site, item):
    # Create paths
    output = os.path.join(site.output_path, site.route_item(item))
    directory = os.path.dirname(output)

    # Ensure directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write
    with open(output, 'w') as f:
        f.write(site.template_item(item))