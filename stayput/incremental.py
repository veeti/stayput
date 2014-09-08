from collections import namedtuple


def compare_items(before, after):
    result = namedtuple('ComparisonResult', 'dirty new deleted unchanged')(set(), set(), set(), set())

    for key, fingerprint in after.items():
        if key in before:
            if before[key] != after[key]:
                result.dirty.add(key)
            else:
                result.unchanged.add(key)
        else:
            result.new.add(key)
            result.dirty.add(key)

    for key, fingerprint in before.items():
        if key not in after:
            result.deleted.add(key)

    return result


def build_manifest(site):
    items = {}
    templates = {}

    for key, item in site.items.items():
        items[key] = item.fingerprint
    for key, template in site.templates.items():
        templates[key] = template.fingerprint

    return {'items': items, 'templates': templates}


def invalidate_all(site, result):
    for key, item in site.items.items():
        result.dirty.add(key)
    return result


def scan_work(site, cached_manifest, manifest=None):
    result = namedtuple('Work', ['dirty', 'deleted'])(set(), set())

    # No cached manifest, no incremental build
    if not cached_manifest:
        return invalidate_all(site, result)

    if not manifest:
        manifest = build_manifest(site)

    items = compare_items(cached_manifest.get('items', {}), manifest['items'])
    templates = compare_items(cached_manifest.get('templates', {}), manifest['templates'])

    # Any template change invalidates the site
    if templates.dirty or templates.new or templates.deleted:
        return invalidate_all(site, result)

    result.dirty.update(items.dirty)
    result.deleted.update(items.deleted)
    return result
