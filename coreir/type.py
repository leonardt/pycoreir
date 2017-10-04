import ctypes as ct
from coreir.base import CoreIRType
from coreir.lib import libcoreir_c

class COREType(ct.Structure):
    pass

COREType_p = ct.POINTER(COREType)

class Params(CoreIRType):
    pass

class COREValue(ct.Structure):
  pass

COREValue_p = ct.POINTER(COREValue)

class Value(CoreIRType):
    @property
    def value(self):
        type = libcoreir_c.COREGetValueType(self.ptr)
        # type enum values defined in include/coreir-c/coreir-args.h
        if type == 0:
            return libcoreir_c.COREValueBoolGet(self.ptr)
        if type == 1:
            return libcoreir_c.COREValueIntGet(self.ptr)
        elif type == 2:
            return libcoreir_c.COREValueBitVectorGet(self.ptr)
        elif type == 3:
            return libcoreir_c.COREValueStringGet(self.ptr).decode()
        raise NotImplementedError()

class Values(CoreIRType):
    pass

class Type(CoreIRType):
    def print_(self):  # _ because print is a keyword in py2
        libcoreir_c.COREPrintType(self.ptr)

    @property
    def size(self):
        return libcoreir_c.CORETypeGetSize(self.ptr)

    @property
    def kind(self):
        # TypeKind enum defined in src/types.hpp
        kind = libcoreir_c.COREGetTypeKind(self.ptr)
        return {
            0: "Bit",
            1: "BitIn",
            2: "Array",
            3: "Record",
            4: "Named"
        }[kind]

    def __len__(self):
        if self.kind != "Array":  # Not a TK_Array
            raise Exception("`len` called on a {}".format(self.kind))
        return libcoreir_c.COREArrayTypeGetLen(self.ptr)
