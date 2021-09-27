import collections
import functools

singleton = functools.lru_cache()


def infinite_defaultdict():
    return collections.defaultdict(infinite_defaultdict)


def get_location_from_frame(frame):
    return "%s:%i" % (frame.f_code.co_filename, frame.f_lineno)


class BaggyDictionary(collections.OrderedDict):
    def __setitem__(self, key, value):
        if key not in self:
            collections.OrderedDict.__setitem__(self, key, [])
        self[key].append(value)

    def items(self):
        for key in self:
            for value in self[key]:
                yield key, value

    def collapse(self):
        return super().__new__(*self.items())


class _ConfigClass:
    def __getattr__(self, name):
        name_lower = name.lower()
        if name_lower != name:
            return getattr(self, name_lower)
        raise AttributeError(name_lower)


Config = _ConfigClass()


def assign_config(config):
    vars(Config).clear()
    vars(Config).update(config)
