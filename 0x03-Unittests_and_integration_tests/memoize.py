def memoize(fn):
    """Decorator to cache a method's return value as a property.

    This decorator transforms a method into a property that caches
    its result after the first call. Subsequent accesses return
    the cached value without calling the original method again.

    Args:
        fn (function): The method to be memoized.

    Returns:
        property: A property that returns the cached value of the method.
    """
    attr_name = "_{}".format(fn.__name__)

    @property
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return wrapper