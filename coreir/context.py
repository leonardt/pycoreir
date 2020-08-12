import json
import ctypes as ct
from coreir.base import _cache
from coreir.type import COREType_p, Type, Params, COREValue_p, Values, Record
from coreir.generator import Generator
from coreir.namespace import Namespace, CORENamespace_p
from coreir.lib import libcoreir_c, load_coreir_lib, libcoreir_sim_c
from hwtypes import BitVector
import coreir.module
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

class COREContext(ct.Structure):
    pass

COREContext_p = ct.POINTER(COREContext)

COREMapKind = ct.c_int
COREMapKind_STR2TYPE_ORDEREDMAP = COREMapKind(0)
COREMapKind_STR2PARAM_MAP = COREMapKind(1)
COREMapKind_STR2VALUE_MAP = COREMapKind(2)


class NamedTypesDict:
    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        if not isinstance(key, tuple) and len(key) == 2 \
                and isinstance(key[0], str) and isinstance(key[1], str):
            raise KeyError("Key should be a tuple of the form (str, str), "
                    "not {}".format(key))
        namespace = key[0]
        type_name = key[1]
        # TODO: Check existence of namespace and named type
        return Type(
            libcoreir_c.COREContextNamed(
                self.context.context, str.encode(namespace),
                str.encode(type_name)
            ),
            self.context
        )


_library_cache = {}

def namespace_cache(f):
    def method(self, name: str):
        c_addr = ct.addressof(self.context)
        if name in _library_cache[c_addr]:
            return _library_cache[c_addr][name]
        ns = f(self, name)
        assert isinstance(ns, Namespace)
        _library_cache[c_addr][name] = ns
        return ns
    return method

class Context:
    def __init__(self, ptr=None):
        # FIXME: Rename this to ptr or context_ptr to be consistent with other
        #        API objects
        self.external_ptr = True
        if ptr is None:
            self.external_ptr = False
            ptr = libcoreir_c.CORENewContext()
            _library_cache.setdefault(ct.addressof(ptr), {})
        self.context = ptr
        #self.global_namespace = Namespace(libcoreir_c.COREGetGlobal(self.context),self)
        self.named_types = NamedTypesDict(self)

    def __str__(self):
        return f"Context<{self.external_ptr}, {self.context}>"

    @property
    def global_namespace(self):
        return self.get_lib("global")


    @property
    def G(self):
        raise Exception("Context.G has been removed, use Context.global_namespace instead")

    def get_version(self):
        return libcoreir_c.COREGetVersion().decode()

    def get_revision(self):
        return libcoreir_c.COREGetRevision().decode()

    def print_errors(self):
        libcoreir_c.COREPrintErrors(self.context)

    def BitInOut(self):
        return Type(libcoreir_c.COREBitInOut(self.context),self)

    def BitIn(self):
        return Type(libcoreir_c.COREBitIn(self.context),self)

    def Bit(self):
        return Type(libcoreir_c.COREBit(self.context),self)

    def Array(self, length, typ):
        assert isinstance(typ, Type)
        assert isinstance(length, int)
        return Type(libcoreir_c.COREArray(self.context, length, typ.ptr),self)

    def Record(self, fields):
        keys = []
        values = []
        for key, value in fields.items():
            keys.append(str.encode(key))
            values.append(value.ptr)
        keys   = (ct.c_char_p * len(fields))(*keys)
        values = (COREType_p * len(fields))(*values)
        record_params = libcoreir_c.CORENewMap(self.context, ct.cast(keys,
            ct.c_void_p), ct.cast(values, ct.c_void_p), len(fields),
            COREMapKind_STR2TYPE_ORDEREDMAP)
        return Type(libcoreir_c.CORERecord(self.context, record_params),self)

    def Flip(self, typ):
        return Type(
            libcoreir_c.COREContextFlip(
                self.context, typ.ptr
            ),
            self
        )

    def newParams(self, fields={}):
        keys = (ct.c_char_p * len(fields))(*(str.encode(key) for key in fields.keys()))
        values = (COREType_p * len(fields))(*(value for value in fields.values()))
        gen_params = libcoreir_c.CORENewMap(self.context, ct.cast(keys,
            ct.c_void_p), ct.cast(values, ct.c_void_p), len(fields),
            COREMapKind_STR2PARAM_MAP)
        return Params(gen_params,self)

    def new_values(self,fields={}):
        args = []
        for v in fields.values():
            if type(v) is int:
                args.append(libcoreir_c.COREValueInt(self.context, ct.c_int(v)))
            elif type(v) is str:
                args.append(libcoreir_c.COREValueString(self.context,
                    ct.c_char_p(str.encode(v))))
            elif type(v) is bool:
                args.append(libcoreir_c.COREValueBool(self.context, ct.c_bool(v)))
            elif isinstance(v, BitVector):
                hex_string = "{0:d}'h{1:x}".format(len(v), v.as_uint())
                args.append(libcoreir_c.COREValueBitVectorString(self.context,
                    hex_string.encode()))
            elif isinstance(v, coreir.Module):
                args.append(libcoreir_c.COREValueModule(self.context,
                    v.ptr))
            elif isinstance(v, coreir.Type):
                args.append(libcoreir_c.COREValueCoreIRType(self.context,
                    v.ptr))
            elif isinstance(v, (dict, list)):
                args.append(libcoreir_c.COREValueJSON(self.context, json.dumps(v).encode()))
            else:
                raise NotImplementedError(v, type(v))

        keys = (ct.c_char_p * len(fields))(*(str.encode(key) for key in fields.keys()))
        values = (COREValue_p * len(fields))(*(arg for arg in args))
        gen_args = libcoreir_c.CORENewMap(self.context, ct.cast(keys,
            ct.c_void_p), ct.cast(values, ct.c_void_p), len(fields),
            COREMapKind_STR2VALUE_MAP)
        return Values(gen_args,self)

    def load_from_file(self, file_name):

        err = ct.c_bool(False)
        m = libcoreir_c.CORELoadModule(
                self.context, ct.c_char_p(str.encode(file_name)),ct.byref(err))
        if (err.value):
           self.print_errors()

        return coreir.module.Module(m,self)

    def save_to_file(self, file_name, include_coreir=False, include_default_libs=True):
        err = ct.c_bool(False)
        libcoreir_c.CORESaveContext(self.context, str.encode(file_name),
                                    include_coreir is False,
                                    include_default_libs is False,
                                    ct.byref(err))
        if err.value is not False:
            raise Exception("Error saving context")

    @namespace_cache
    def load_library(self, name):
        lib = load_coreir_lib(name)
        func = getattr(lib,"CORELoadLibrary_{}".format(name))
        func.argtypes = [COREContext_p]
        func.restype = CORENamespace_p
        return Namespace(func(self.context), self)

    def enable_symbol_table(self):
        libcoreir_sim_c.COREEnSymtable(self.context)

    @namespace_cache
    def get_namespace(self,name):
        ns = libcoreir_c.COREGetNamespace(self.context,ct.c_char_p(str.encode(name)))
        return Namespace(ns, self)

    def new_namespace(self,name):
        c_addr = ct.addressof(self.context)
        if name in _library_cache[c_addr]:
            raise ValueError(f"Namespace {name} already exists!")
        ns = libcoreir_c.CORENewNamespace(self.context,ct.c_char_p(str.encode(name)))
        return Namespace(ns, self)

    @namespace_cache
    def get_lib(self, lib):
        if lib in {"global", "coreir", "mantle", "corebit", "memory"}:
            return self.get_namespace(lib)
        #elif lib == "global":
        #    return self.global_namespace
        else:
            return self.load_library(lib)

    def import_generator(self, lib: str, name: str) -> Generator:
        return self.get_lib(lib).generators[name]

    def run_passes(self, passes, namespaces = ["global"]):
        for ns in namespaces:
            self.get_lib(ns)
        pass_arr = (ct.c_char_p * len(passes))(*(p.encode() for p in passes))
        namespaces_arr = (ct.c_char_p * len(namespaces))(*(n.encode() for n in namespaces))
        return libcoreir_c.COREContextRunPasses(self.context,
                                                pass_arr, ct.c_int(len(passes)),
                                                namespaces_arr, ct.c_int(len(namespaces)))

    def compile_to_verilog(self, top, filename, libs=(), split="",
                           product="", inline=False, verilator_debug=False,
                           disable_width_cast=False):
        top = top.ptr
        num_libs = ct.c_int(len(libs))
        libs = (ct.c_char_p * len(libs))(*(lib.encode() for lib in libs))
        filename = ct.c_char_p(filename.encode())
        split = ct.c_char_p(split.encode())
        product = ct.c_char_p(product.encode())
        inline = ct.c_bool(inline)
        verilator_debug = ct.c_bool(verilator_debug)
        disable_width_cast = ct.c_bool(disable_width_cast)
        return libcoreir_c.CORECompileToVerilog(self.context, top, filename,
                                                num_libs, libs, split, product,
                                                inline, verilator_debug,
                                                disable_width_cast)

    def __del__(self):
        if self.context is not None and not self.external_ptr:
            self.delete()

    def delete(self):
        """
        WARNING: Unsafe, will set self.context to None.  The pycoreir internal
        code does not check for this.  For performance reasons, we do not add a
        None check for all the API code, instead we assume if this is used that
        the user is certain that the context object will no longer be used.
        """
        if self.context is None:
            raise Exception("Context already deleted")
        c_addr = ct.addressof(self.context)
        if c_addr in _library_cache:
            del _library_cache[c_addr]
        if c_addr in _cache:
            del _cache[c_addr]
        libcoreir_c.COREDeleteContext(self.context)
        self.context = None

    def Int(self):
        return libcoreir_c.COREContextInt(self.context)

    def String(self):
        return libcoreir_c.COREContextString(self.context)

    def Bool(self):
        return libcoreir_c.COREContextBool(self.context)

    def BitVector(self):
        return libcoreir_c.COREContextBitVector(self.context)

    def CoreIRType(self):
        return libcoreir_c.COREContextCOREIRType(self.context)

    def set_top(self, module):
        libcoreir_c.COREContextSetTop(self.context, module.ptr)
