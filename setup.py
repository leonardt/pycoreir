"""
Script for installing the pycoreir module
"""
import subprocess
import os
import shutil
import platform
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


SYSTEM = platform.system()
if SYSTEM == "Linux":
    LIB_EXT = "so"
    STATIC_BUILD = True
elif SYSTEM == "Darwin":
    LIB_EXT = "dylib"
    # osx default xcode doesn't support static build
    STATIC_BUILD = False
else:
    raise NotImplementedError(SYSTEM)


COREIR_PATH = "coreir-cpp"
COREIR_REPO = "https://github.com/rdaly525/coreir"
COREIR_NAME = "coreir"


class CoreIRBuild(build_ext):
    """
    Compile coreir libraries
    """
    libs = ["coreir-c", "coreirsim-c", "coreir-ice40", "coreir-aetherlinglib",
            "coreir-commonlib", "coreir-float", "coreir-rtlil",
            "coreir-float_CW", "coreir-float_DW"]
    def run(self):
        if not os.path.isdir(COREIR_PATH):
            subprocess.check_call(["git", "clone", "--depth=1", COREIR_REPO,
                                   COREIR_PATH])
        build_dir = os.path.join(COREIR_PATH, "build")
        if STATIC_BUILD:
            subprocess.check_call(["cmake", "-DSTATIC=ON", ".."], cwd=build_dir)
        else:
            subprocess.check_call(["cmake", ".."], cwd=build_dir)

        for lib_name in self.libs:
            subprocess.check_call(["make", "-C", build_dir, "-j2",
                                   lib_name])
        # make the binary
        subprocess.check_call(["make", "-C", build_dir, "-j2", "coreir-bin"])

        # we only have one extension
        assert len(self.extensions) == 1
        ext = self.extensions[0]
        extdir = \
            os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        extdir = os.path.join(extdir, COREIR_NAME)
        if not os.path.isdir(extdir):
            os.mkdir(extdir)
        # copy libraries over
        for lib_name in self.libs:
            filename = os.path.join(
                COREIR_PATH, "build", "lib",
                "lib{}.{}".format(lib_name, LIB_EXT)
            )
            shutil.copy(filename, extdir)

        # copy binary over
        filename = os.path.join(COREIR_PATH, "build", "bin", "coreir")
        shutil.copy(filename, extdir)

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name='coreir',
    version='2.0.19',
    description='Python bindings for CoreIR',
    packages=["coreir"],
    license='BSD License',
    url='https://github.com/leonardt/pycoreir',
    author='Leonard Truong',
    author_email='lenny@cs.stanford.edu',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=["hwtypes>=1.0.*"],
    ext_modules=[Extension('coreir', [])],
    scripts=[os.path.join(COREIR_PATH, "build", "bin", "coreir")],
    cmdclass=dict(build_ext=CoreIRBuild),
    zip_safe=False
)
