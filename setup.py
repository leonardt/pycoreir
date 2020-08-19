import subprocess
import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.command.build import build
import glob
import shutil
import sys
import platform
import multiprocessing


_system = platform.system()
if _system == "Linux":
    extra_libs = []
    lib_ext = "so"
    static_build = True
elif _system == "Darwin":
    extra_libs = ["coreir", "coreirsim"]
    lib_ext = "dylib"
    # osx default xcode doesn't support static build
    static_build = False
else:
    raise NotImplementedError(_system)

if os.environ.get('TRAVIS') == 'true':
    njobs = 2
else:
    try:
        cpus = len(os.sched_getaffinity(0))
    except AttributeError:
        cpus = multiprocessing.cpu_count()
    njobs = max(2, cpus)

COREIR_PATH = "coreir-cpp"
COREIR_REPO = "https://github.com/rdaly525/coreir"
COREIR_NAME = "coreir"
COREIR_BRANCH = "master"


TEXT_CHARS = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) -
                       {0x7f})


def is_binary_string(bytes):
    return bool(bytes.translate(None, TEXT_CHARS))


def is_binary(path):
    # adapted from https://stackoverflow.com/a/7392391
    with open(path, "rb") as f:
        return is_binary_string(f.read(1024))


COREIR_BINARY_PATH = None
for line in os.popen("which -a coreir").read().splitlines():
    if is_binary(line):
        COREIR_BINARY_PATH = line
        break


class CoreIRExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CoreIRBuild(build_ext):
    libs = ["coreir-c", "coreirsim-c", "coreir-ice40", "coreir-aetherlinglib",
            "coreir-commonlib", "coreir-float", "coreir-rtlil",
            "coreir-float_CW", "coreir-float_DW", "verilogAST"] + extra_libs

    def run(self):
        # skip if coreir binary is found. this is useful if people want
        # to use their own version of coreir

        if COREIR_BINARY_PATH is not None:
            # we're done here since users provide their own coreir distribution
            return

        # we only have one extension
        assert len(self.extensions) == 1
        ext = self.extensions[0]
        extdir = \
            os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        extdir = os.path.join(extdir, COREIR_NAME)
        if not os.path.isdir(extdir):
            os.mkdir(extdir)

        if not os.path.isdir(COREIR_PATH):
            subprocess.check_call(["git", "clone", "--depth=1", "--branch",
                                   COREIR_BRANCH, COREIR_REPO, COREIR_PATH])
        build_dir = os.path.join(COREIR_PATH, "build")

        if static_build:
            subprocess.check_call(["cmake", "-DSTATIC=ON", ".."],
                                  cwd=build_dir)
        else:
            subprocess.check_call(["cmake", ".."], cwd=build_dir)

        for lib_name in self.libs:
            subprocess.check_call(["make", "-C", build_dir, f"-j{njobs}",
                                   lib_name])
        # make the binary
        subprocess.check_call(["make", "-C", build_dir, f"-j{njobs}",
                               "coreir-bin"])

        # copy libraries over
        for lib_name in self.libs:
            filename = os.path.join(
                COREIR_PATH, "build", "lib",
                "lib{}.{}".format(lib_name, lib_ext)
            )
            shutil.copy(filename, extdir)

        # copy binary over
        filename = os.path.join(COREIR_PATH, "build", "bin", "coreir")
        shutil.copy(filename, extdir)


scripts = []
if not COREIR_BINARY_PATH:
    scripts.append("bin/coreir")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='coreir',
    version='2.0.106',
    description='Python bindings for CoreIR',
    packages=["coreir"],
    license='BSD License',
    url='https://github.com/leonardt/pycoreir',
    author='Leonard Truong',
    author_email='lenny@cs.stanford.edu',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["hwtypes>=1.0.*"],
    ext_modules=[CoreIRExtension('coreir')],
    scripts=scripts,
    cmdclass=dict(build_ext=CoreIRBuild),
    zip_safe=False
)
