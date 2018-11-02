import ctypes as ct
from coreir.type import CoreIRType
from coreir.lib import libcoreir_c
from coreir.type import COREValueType_p, ValueType
from coreir.module import Module


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

    def __call__(self, *args, **kwargs):
        assert len(args) == 0, "TODO: Try mapping args by order, for now require explicit kwargs"
        gen_args = {}
        for key, value in kwargs.items():
            if key not in self.params:
                raise KeyError("key={key} not in params={keys}".format(key=key, keys=self.params.keys()))
            if not isinstance(value, self.params[key].kind):
                raise ValueError("Arg(name={key}, value={value}) does not match expected type {kind}".format(key=key, value=value, kind=self.params[key].kind))
            gen_args[key] = value
        gen_args = self.context.new_values(gen_args)
        return Module(libcoreir_c.COREGeneratorGetModule(self.ptr, gen_args.ptr), self.context)
