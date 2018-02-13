import ctypes as ct
from coreir.base import CoreIRType
from coreir.lib import libcoreir_c
from coreir.type import Type, COREValue_p, Value
from coreir.util import LazyDict
import coreir.module

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
        if  not libcoreir_c.COREWireableCanSelect(self.ptr,str.encode(field)):
            raise Exception("Cannot Select this Wireable with " + field)
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


class Select(Wireable):
    pass
    # @property
    # def parent(self):
    #     return Wireable(libcoreir_c.CORESelectGetParent(self.ptr))


class Instance(Wireable):
    def __init__(self, ptr, context):
        super(Instance, self).__init__(ptr, context)
        self.config = LazyDict(self, Value, libcoreir_c.COREGetModArg,
                libcoreir_c.COREHasModArg)

    @property
    def module(self):
        module = libcoreir_c.COREGetModuleRef(self.ptr)
        return coreir.module.Module(module, self.context)

    def __str__(self):
        return f"{self.module.name}.{self.name}"

    @property
    def name(self):
        return libcoreir_c.COREInstanceGetInstname(self.ptr).decode()


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
