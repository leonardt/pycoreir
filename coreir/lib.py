from ctypes import cdll
import platform
import os


def is_binary(path):
    # adapted from https://stackoverflow.com/a/7392391
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    with open(path, "rb") as f:
        try:
            return is_binary_string(f.read(1024))
        except UnicodeDecodeError:
            # assume binary
            return True


# see if a coreir binary exists in the user's path
COREIR_BINARY_PATH = None
for line in os.popen("which -a coreir").read().splitlines():
    if is_binary(line):
        COREIR_BINARY_PATH = line
        break


def load_shared_lib(lib):
    _system = platform.system()
    if _system == "Linux":
        shared_lib_ext = "so"
    elif _system == "Darwin":
        shared_lib_ext = "dylib"
    else:
        raise NotImplementedError(_system)
    if COREIR_BINARY_PATH is None:
        # Assume we did a static build and use the corresponding binary
        libpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), lib)
        libpath = "{}.{}".format(libpath, shared_lib_ext)
    else:
        # Found existing binary, load lib from system path
        libpath = "{}.{}".format(lib, shared_lib_ext)
    return cdll.LoadLibrary(libpath)


def load_coreir_lib(suffix):
    return load_shared_lib('libcoreir-{}'.format(suffix))


libcoreir_c = load_coreir_lib("c")
libcoreir_sim_c = load_shared_lib("libcoreirsim-c")
