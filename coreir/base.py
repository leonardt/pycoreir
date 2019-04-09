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
    def __call__(cls,ptr,*args,**kwargs):
        cptr = get_pointer_value(ptr)
        if cptr in _cache:
            return _cache[cptr]
        else:
            inst = super().__call__(ptr,*args,**kwargs)
            _cache[cptr] = inst
        return inst

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
