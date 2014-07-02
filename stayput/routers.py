import os.path


def simple_router(node, *args, **kwargs):
    if node.path == 'index.html':
        return node.path
    split = os.path.splitext(node.path)
    return "%s/index%s" % split
