def memoize(fn):
    """Decorator to memoize a method"""
    attr_name = "_{}".format(fn.__name__)
    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return wrapper