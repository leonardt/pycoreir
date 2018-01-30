import ctypes as ct
from coreir.type import CoreIRType
from coreir.lib import libcoreir_c
from coreir.type import COREValueType_p, ValueType


class COREGenerator(ct.Structure):
    pass

COREGenerator_p = ct.POINTER(COREGenerator)


class Generator(CoreIRType):
    @property
    def name(self):
        return libcoreir_c.COREGeneratorGetName(self.ptr).decode()

    @property
    def params(self):
        num_params = ct.c_int()
        names = ct.POINTER(ct.c_char_p)()
        params = ct.POINTER(COREValueType_p)()
        libcoreir_c.COREGeneratorGetGenParams(self.ptr, ct.byref(names),
                ct.byref(params), ct.byref(num_params))
        ret = {}
        for i in range(num_params.value):
            ret[names[i].decode()] = ValueType(params[i], self.context)
        return ret
