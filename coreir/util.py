from collections import Mapping
import ctypes as ct
from .lib import libcoreir_c


class LazyDict(Mapping):
    """
    Lazy object that implements the ``dict[key]`` interface. Instead
    of building the dictionary explicitly for every call to config, we wait for
    the indexing function to be called and then use the api function
    """
    def __init__(self, parent, return_type, core_return_type, get_function, has_function, iter_function):
        self.parent = parent
        self.return_type = return_type
        self.core_return_type = core_return_type
        self.get_function = get_function
        self.has_function = has_function
        self.iter_function = iter_function

    def __contains__(self, key):
        return self.has_function(self.parent.ptr, str.encode(key))

    def __getitem__(self, key):
        if not key in self:
            raise KeyError("Could not find key: {}".format(key))
        return self.return_type(
                   self.get_function(self.parent.ptr,
                                     str.encode(key)),
                   self.parent.context)

    def __iter__(self):
        c_keys = ct.POINTER(ct.c_char_p)()
        c_values = ct.POINTER(self.core_return_type)()
        size = ct.c_int()
        self.iter_function(self.parent.ptr, ct.byref(c_keys), ct.byref(c_values), ct.byref(size))
        _dict = {}
        for i in range(0, size.value):
            _dict[c_keys[i].decode()] = self.return_type(c_values[i], self.parent.context)
        libcoreir_c.COREFree(c_keys, c_values)
        return iter(_dict)

    def __len__(self):
        # TODO: Should just be an API call
        _len = 0
        for _ in self:
            _len += 1
        return _len


    def __setitem__(self, key, value):
        raise NotImplementedError()
