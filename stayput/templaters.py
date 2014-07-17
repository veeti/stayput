class Templater(object):

    def template(self, item, site, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, item, site, *args, **kwargs):
        return self.template(item, site)


class SimpleTemplater(Templater):
    """A simple templater that replaces any occurrence of %contents% in the specified template
    with the item's contents."""

    def __init__(self):
        self.default_template = "%contents%"

    def template(self, item, site, *args, **kwargs):
        """
        Templates the specified item.
        :param item: Item
        :return: Result
        """
        return self.default_template.replace('%contents%', item.contents)
