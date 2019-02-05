import ctypes as ct
from .lib import libcoreir_c
import coreir


def get_pointer_value(pointer):
    """
    Converts ctypes pointer to its underlying integer representation
    """
    return ct.cast(pointer, ct.c_void_p).value


class CoreIRType(object):
    def __init__(self, ptr, context):
        self.ptr = ptr
        assert isinstance(context, coreir.context.Context)
        self.context = context

    def __hash__(self):
        return get_pointer_value(self.ptr)

    def __eq__(self, other):
        if not isinstance(other, CoreIRType):
            return False
        return get_pointer_value(self.ptr) == get_pointer_value(other.ptr)
