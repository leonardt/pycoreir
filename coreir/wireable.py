import ctypes as ct
from coreir.base import CoreIRType
from coreir.lib import libcoreir_c
from coreir.type import Type, COREValue_p, Value
from coreir.util import LazyDict
import coreir.module
import random
from hwtypes import BitVector

class COREWireable(ct.Structure):
    pass

COREWireable_p = ct.POINTER(COREWireable)


class Wireable(CoreIRType):
    @property
    def connected_wireables(self):
        size = ct.c_int()
        result = libcoreir_c.COREWireableGetConnectedWireables(self.ptr, ct.byref(size))
        return [Wireable(result[i],self.context) for i in range(size.value)]

    @property
    def selectpath(self):
        size = ct.c_int()
        result = libcoreir_c.COREWireableGetSelectPath(self.ptr, ct.byref(size))
        return [result[i].decode() for i in range(size.value)]

    def select(self, field):
        if not libcoreir_c.COREWireableCanSelect(self.ptr,str.encode(field)):
            raise Exception(f"Cannot Select {self.selectpath} with {field}")
        return Select(libcoreir_c.COREWireableSelect(self.ptr, str.encode(field)),self.context)

    @property
    def module_def(self):
        return coreir.module.ModuleDef(libcoreir_c.COREWireableGetContainer(self.ptr),self.context)

    @property
    def module(self):
        return self.module_def.module

    @property
    def type(self):
        return Type(libcoreir_c.COREWireableGetType(self.ptr), self.context)

    def add_metadata(self, key, value):
        libcoreir_c.COREWireableAddMetaDataStr(self.ptr, str.encode(key), str.encode(value))


class Select(Wireable):
    @property
    def parent(self):
        return Wireable(libcoreir_c.COREWireableGetParent(self.ptr), self.context)


class Instance(Wireable):
    def __init__(self, ptr, context):
        super(Instance, self).__init__(ptr, context)
        self.config = LazyDict(self, Value, COREValue_p, libcoreir_c.COREGetModArg,
                libcoreir_c.COREHasModArg, libcoreir_c.COREGetModArgs)

    @property
    def module(self):
        module = libcoreir_c.COREGetModuleRef(self.ptr)
        return coreir.module.Module(module, self.context)

    def __str__(self):
        return "{modulename}.{name}".format(modulename=self.module.name, name=self.name)

    @property
    def name(self):
        return libcoreir_c.COREInstanceGetInstname(self.ptr).decode()


def inline_instance(instance):
    if not isinstance(instance,Instance):
        raise TypeError("Needs to be an Instance")
    return libcoreir_c.COREInlineInstance(instance.ptr)


class Interface(Wireable):
    pass


class Connection(CoreIRType):
    @property
    def size(self):
        assert self.first.type.size == self.second.type.size
        return self.first.type.size

    @property
    def first(self):
        return Wireable(libcoreir_c.COREConnectionGetFirst(self.ptr), self.context)

    @property
    def second(self):
        return Wireable(libcoreir_c.COREConnectionGetSecond(self.ptr), self.context)


def cast_to_select(wire : Wireable):
    return Select(wire.ptr, wire.context)

_CNT = 0
def connect_const(port : Wireable,value : int):
    if not isinstance(port,Wireable):
        raise TypeError("Needs to be an Instance")
    c = port.context
    if not (port.type.kind in ("BitIn","Array")):
        raise NotImplementedError(f"{port.type.kind} bad. Use Bit or Array(Bit)")
    width = 1 if port.type.kind == "BitIn" else port.type.size
    if 2**width <= value:
        raise TypeError(f"{value} cannot fit in {width} bits")
    mdef = port.module_def
    if width==1:
        cnst = c.get_namespace("corebit").modules["const"]
        value0 = c.new_values({"value":(value==1)})
    else:
        cnst = c.get_namespace("coreir").generators["const"](width=width)
        value0 = c.new_values({"value":BitVector[width](value)})

    global _CNT
    cinst = mdef.add_module_instance(name=f"c_{_CNT}",module=cnst,config=value0)
    _CNT += 1
    mdef.connect(cinst.select("out"),port)


