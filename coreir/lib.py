from ctypes import cdll
import platform
import os


def load_shared_lib(lib):
    _system = platform.system()
    if _system == "Linux":
        shared_lib_ext = "so"
    elif _system == "Darwin":
        shared_lib_ext = "dylib"
    else:
        raise NotImplementedError(_system)

    return cdll.LoadLibrary("{}.{}".format(lib, shared_lib_ext))


def load_coreir_lib(suffix):
    return load_shared_lib('libcoreir-{}'.format(suffix))


libcoreir_c = load_coreir_lib("c")
libcoreir_sim_c = load_shared_lib("libcoreirsim-c")
