from collections.abc import MutableMapping


class CustomKeyModifier(MutableMapping):
    def __init__(self, modifier, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        self._modifier = modifier

    def __getitem__(self, key):
        return self._d[key]

    def __setitem__(self, key, value):
        if key.startswith('__') and key.endswith('__'):
            self._d[key] = value
        else:
            self._d[self._modifier.format(key)] = value

    def __delitem__(self, key):
        del self._d[key]

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __contains__(self, key):
        return key in self._d

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self._d)


class CustomMeta(type):
    modifier = 'custom_{}'

    def __new__(mcls, name, bases, classdict):
        cls = super().__new__(mcls, name, bases, dict(classdict))
        cls_setattr = getattr(cls, '__setattr__')
        setattr(
            cls,
            '__setattr__',
            CustomMeta.modify_setattr_name(cls_setattr, CustomMeta.modifier)
        )
        return cls

    @staticmethod
    def modify_setattr_name(func, modifier):
        def wrapped(self, name, value):
            func(self, modifier.format(name), value)
        return wrapped

    @classmethod
    def __prepare__(mcls, name, bases, **kwargs):
        return CustomKeyModifier(CustomMeta.modifier)
