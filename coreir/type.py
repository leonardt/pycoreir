import coreir
import ctypes as ct
from coreir.base import CoreIRType
from coreir.lib import libcoreir_c
from collections import namedtuple

class BitVector:
    def __init__(self, width=None, val=None):
        self.width = width
        self.val = val

class COREType(ct.Structure):
    pass

COREType_p = ct.POINTER(COREType)

class Params(CoreIRType):
    pass

class COREValueType(ct.Structure):
  pass

COREValueType_p = ct.POINTER(COREValueType)

class ValueType(CoreIRType):
    @property
    def kind(self):
        return {
            # Defined in ir/valuetype.h
            0: bool,
            1: int,
            2: BitVector,
            3: str,
            4: CoreIRType,
            5: coreir.Module,
        }[libcoreir_c.COREValueTypeGetKind(self.ptr)]

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
            if libcoreir_c.COREValueBitVectorIsBinary(self.ptr):
                width = ct.c_int()
                value = ct.c_uint64()
                libcoreir_c.COREValueBitVectorGet(self.ptr, ct.byref(width), ct.byref(value))
                return BitVector(width.value, value.value)
            else:
                width = ct.c_int()
                libcoreir_c.COREValueBitVectorGetWidth(self.ptr, ct.byref(width))
                return BitVector(width.value)
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

    def is_input(self):
        return libcoreir_c.CORETypeIsInput(self.ptr)

    @property
    def element_type(self):
        if self.kind != "Array":  # Not a TK_Array
            raise Exception("`element_type` called on a {}".format(self.kind))
        return Type(libcoreir_c.COREArrayTypeGetElemType(self.ptr), self.context)

    def __len__(self):
        if self.kind != "Array":  # Not a TK_Array
            raise Exception("`len` called on a {}".format(self.kind))
        return libcoreir_c.COREArrayTypeGetLen(self.ptr)


class Record(Type):
    def __getitem__(self, key):
        keys = ct.POINTER(ct.c_char_p)()
        values = ct.POINTER(COREType_p)()
        size = ct.c_int()
        libcoreir_c.CORERecordTypeGetItems(self.ptr, ct.byref(keys),
                ct.byref(values), ct.byref(size))
        for i in range(size.value):
            if keys[i].decode() == key:
                return Type(values[i], self.context)
        raise KeyError(f"key={key} not found")

    def items(self):
        keys = ct.POINTER(ct.c_char_p)()
        values = ct.POINTER(COREType_p)()
        size = ct.c_int()
        libcoreir_c.CORERecordTypeGetItems(self.ptr, ct.byref(keys),
                ct.byref(values), ct.byref(size))
        retval = {}
        for i in range(size.value):
            retval[keys[i].decode()] = Type(values[i], self.context)
        return retval.items()


class NamedType(Type):
    @property
    def name(self):
        return libcoreir_c.CORENamedTypeToString(self.ptr).decode()
