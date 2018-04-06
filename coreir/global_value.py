from .base import CoreIRType
import ctypes as ct
import coreir
from .lib import libcoreir_c

class COREGlobalValue(ct.Structure):
    pass

COREGlobalValue_p = ct.POINTER(COREGlobalValue)

class GlobalValue(CoreIRType):
    @property
    def namespace(self):
        return coreir.namespace.Namespace(libcoreir_c.COREGlobalValueGetNamespace(self.ptr), self.context)
