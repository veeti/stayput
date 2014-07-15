import sys

if sys.version_info.major > 2:
    # python 3
    from importlib.machinery import SourceFileLoader

    def import_file(path):
        loader = SourceFileLoader(path, path)
        return loader.load_module()
else:
    # python 2
    from imp import load_source

    def import_file(path):
        return load_source('dynamic', path)