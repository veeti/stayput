class ComparisonResult(object):

    def __init__(self):
        self.dirty = set()
        self.new = set()
        self.deleted = set()
        self.unchanged = set()


def compare_items(before, after):
    result = ComparisonResult()

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
