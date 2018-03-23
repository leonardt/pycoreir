import ctypes as ct
from .lib import libcoreir_c
import coreir

class CoreIRType(object):
    def __init__(self, ptr, context):
        self.ptr = ptr
        assert isinstance(context, coreir.context.Context)
        self.context = context
