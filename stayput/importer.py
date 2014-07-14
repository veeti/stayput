from importlib.machinery import SourceFileLoader


def import_file(path):
    loader = SourceFileLoader(path, path)
    return loader.load_module()
