from ctypes import cdll
import platform
import os


def load_shared_lib(suffix):
    _system = platform.system()
    if _system == "Linux":
        shared_lib_ext = "so"
    elif _system == "Darwin":
        shared_lib_ext = "dylib"
    else:
        raise NotImplementedError(_system)

    return cdll.LoadLibrary('libcoreir-{}.{}'.format(suffix, shared_lib_ext))

libcoreir_c = load_shared_lib("c")
