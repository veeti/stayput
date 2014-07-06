import os.path


def simple_router(item, *args, **kwargs):
    if item.path == 'index.html':
        return item.path
    split = os.path.splitext(item.path)
    return "%s/index%s" % split
