import coreir
from functools import wraps
import ctypes

def type_gen(fn):
    @wraps(fn)
    def wrapped(context, names, values, num_values):
        """
        Only use these arguments in this function, coreir will cleanup the
        pointers after this function returns, DO NOT store
        """
        context = coreir.Context(ctypes.cast(context, coreir.COREContext_p))
        values = ctypes.cast(values, ctypes.POINTER(coreir.COREValue_p))
        names = ctypes.cast(names, ctypes.POINTER(ctypes.c_char_p))
        values_map = {}
        for i in range(num_values):
            values_map[names[i].decode()] = coreir.Value(values[i], context)
        type_obj = fn(context, values_map)
        return ctypes.addressof(type_obj.ptr.contents)
    return wrapped

def generator_(fn):
    @wraps(fn)
    def wrapped(context, names, values, num_values, module_def):
        """
        Only use these arguments in this function, coreir will cleanup the
        pointers after this function returns, DO NOT store
        """
        context = coreir.Context(ctypes.cast(context, coreir.COREContext_p))
        values = ctypes.cast(values, ctypes.POINTER(coreir.COREValue_p))
        names = ctypes.cast(names, ctypes.POINTER(ctypes.c_char_p))
        module_def = ctypes.cast(module_def, coreir.COREModuleDef_p)
        values_map = {}
        for i in range(num_values):
            values_map[names[i].decode()] = coreir.Value(values[i], context)
        fn(context, values_map, coreir.ModuleDef(module_def, context))
    return wrapped
