import coreir
import ctypes as ct
from coreir.base import CoreIRType
from coreir.lib import libcoreir_c
from collections import namedtuple
from hwtypes import BitVector

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
        elif type == 1:
            return libcoreir_c.COREValueIntGet(self.ptr)
        elif type == 2:
            if libcoreir_c.COREValueBitVectorIsBinary(self.ptr):
                from math import ceil
                width = ct.c_int()

                libcoreir_c.COREValueBitVectorGetWidth(self.ptr, ct.byref(width))
                value_str = ct.create_string_buffer((str(width.value) + "'h" + "0"*ceil(width.value/4)).encode())
                libcoreir_c.COREValueBitVectorGetString(self.ptr, value_str)
                prefix, value = value_str.value.split(b"'h")
                value = int(value, 16)
                return BitVector[width.value](value)
            else:
                width = ct.c_int()
                libcoreir_c.COREValueBitVectorGetWidth(self.ptr, ct.byref(width))
                return BitVector[width.value](None)
        elif type == 3:
            return libcoreir_c.COREValueStringGet(self.ptr).decode()
        raise NotImplementedError(type)

class Values(CoreIRType):
    pass

def getPyCoreIRType(ptr, context):
    kind = libcoreir_c.COREGetTypeKind(ptr)
    if (kind == 3):
        return Record(ptr, context)
    elif (kind == 4):
        return NamedType(ptr, context)
    else:
        # don't need to handle arrays, bit, and bitin separately as they all
        # don't subclass the CoreIR Type class
        return Type(ptr, context)

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

    def is_output(self):
        return libcoreir_c.CORETypeIsOutput(self.ptr)

    @property
    def element_type(self):
        if self.kind != "Array":  # Not a TK_Array
            raise Exception("`element_type` called on a {}".format(self.kind))
        return getPyCoreIRType(libcoreir_c.COREArrayTypeGetElemType(self.ptr),
                               self.context)

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
        raise KeyError("key={key} not found".format(key=key))

    def items(self):
        keys = ct.POINTER(ct.c_char_p)()
        values = ct.POINTER(COREType_p)()
        size = ct.c_int()
        libcoreir_c.CORERecordTypeGetItems(self.ptr, ct.byref(keys),
                ct.byref(values), ct.byref(size))
        retval = {}
        for i in range(size.value):
            retval[keys[i].decode()] = getPyCoreIRType(values[i], self.context)
        return retval.items()


class NamedType(Type):
    @property
    def name(self):
        return libcoreir_c.CORENamedTypeToString(self.ptr).decode()
