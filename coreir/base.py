import ctypes as ct
from .lib import libcoreir_c
import coreir

def get_pointer_value(pointer):
    """
    Converts ctypes pointer to its underlying integer representation
    """
    return ct.cast(pointer, ct.c_void_p).value

_cache = {}
class Memoize(type):
    def __call__(cls, ptr, context, *args,**kwargs):
        assert isinstance(context, coreir.Context)
        cptr = get_pointer_value(ptr)
        ccontext = ct.addressof(context.context)
        key = (cptr, cls)
        _cache.setdefault(ccontext, {})
        if key not in _cache[ccontext]:
            inst = super().__call__(ptr, context, *args, **kwargs)
            _cache[ccontext][key] = inst
        return _cache[ccontext][key]


class CoreIRType(metaclass=Memoize):
    def __init__(self, ptr, context):
        self.ptr = ptr
        self.context = context

    def __hash__(self):
        return get_pointer_value(self.ptr)

    def __eq__(self, other):
        if not isinstance(other, CoreIRType):
            return False
        return get_pointer_value(self.ptr) == get_pointer_value(other.ptr)
