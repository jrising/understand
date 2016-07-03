## A conditional is a check to see if something has a given property and what value it has
class RawConditional(object):
    def __init__(self, env):
        self.env = env

    def check(self, confidence=1, *args, **kw):
        """Return specifies the value of the property, or None if it does not have the property, to the given confidence."""
        return None

    def describe(self, value):
        """Prints something to the user to describe the property."""
        pass

    @classmethod
    def verbose_check(cls, env, *args, **kw):
        is_obj = cls(env)
        obj_property = is_obj.check(*args, **kw)
        is_obj.describe(obj_property)

        env.set(cls, obj_property)
        return obj_property

