import ctypes as ct
from coreir.type import CoreIRType
from coreir.lib import libcoreir_c


class COREGenerator(ct.Structure):
    pass

COREGenerator_p = ct.POINTER(COREGenerator)


class Generator(CoreIRType):
    @property
    def name(self):
        return libcoreir_c.COREGeneratorGetName(self.ptr).decode()
