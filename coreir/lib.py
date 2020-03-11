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

SYSTEM = platform.system()
if SYSTEM == "Linux":
    LIBRARY_PATH_VAR = "LD_LIBRARY_PATH"
    SHARED_LIB_EXT = ".so"
elif SYSTEM == "Darwin":
    LIBRARY_PATH_VAR = "DYLD_LIBRARY_PATH"
    SHARED_LIB_EXT = ".dylib"
else:
    raise NotImplementedError(SYSTEM)

FILE_PATH = os.path.abspath(os.path.dirname(__file__))

# Assume we did a static build, append to LD path for libs
if COREIR_BINARY_PATH is None:
   os.environ[LIBRARY_PATH_VAR] = f"{os.environ.get(LIBRARY_PATH_VAR, '')}:{FILE_PATH}"


def get_lib_dir():
    '''Return path to the library directory for coreir libs'''
    if COREIR_BINARY_PATH is None:
        # Assume we did a static build and use the libraries we built
        return FILE_PATH

    # There's a binary on $PATH. Use the corresponding libraries (which we
    # assume to be at ../lib relative to it)
    bin_dir = os.path.dirname(COREIR_BINARY_PATH)
    lib_dir = os.path.normpath(os.path.join(bin_dir, '../lib'))

    if not os.path.isdir(lib_dir):
        raise RuntimeError('We found a coreir binary at {}, but there\'s no '
                           'corresponding library directory at {}.'
                           .format(COREIR_BINARY_PATH, lib_dir))

    return lib_dir


def load_shared_lib(lib):
    lib_dir = get_lib_dir()
    lib_path = os.path.join(lib_dir, lib + SHARED_LIB_EXT)
    if not os.path.exists(lib_path):
        raise RuntimeError('No library at {}.'.format(lib_path))

    return cdll.LoadLibrary(lib_path)


def load_coreir_lib(suffix):
    return load_shared_lib('libcoreir-{}'.format(suffix))


libcoreir_c = load_coreir_lib("c")
libcoreir_sim_c = load_shared_lib("libcoreirsim-c")
