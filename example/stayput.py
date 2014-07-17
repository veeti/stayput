from os import path

from stayput import SimpleTemplater, simple_router

def configure(site):
    # Set default router.
    site.router = simple_router

    # Set default template.
    site.templater = SimpleTemplater()
    with open(path.join(site.root_path, 'templates', 'default.html')) as f:
        site.templater.default_template = f.read()

