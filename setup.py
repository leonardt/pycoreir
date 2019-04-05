import subprocess
import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import glob
import shutil


COREIR_PATH = "coreir-cpp"
COREIR_REPO = "https://github.com/Kuree/coreir"
COREIR_NAME = "coreir"


class CoreIRExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CoreIRBuild(build_ext):
    def run(self):
        if os.path.isdir(COREIR_PATH):
            shutil.rmtree(COREIR_PATH)
        subprocess.check_call(["git", "clone", "--depth=1", COREIR_REPO,
                               COREIR_PATH])
        build_dir = os.path.join(COREIR_PATH, "build")
        subprocess.check_call(["cmake", "-DSTATIC=ON", ".."], cwd=build_dir)
        subprocess.check_call(["make", "-C", build_dir, "-j2"])
        # we only have one extension
        assert len(self.extensions) == 1
        ext = self.extensions[0]
        extdir = \
            os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        extdir = os.path.join(extdir, COREIR_NAME)
        if not os.path.isdir(extdir):
            os.mkdir(extdir)
        # copy libraries over
        libs = ["libcoreir-c.so", "libcoreirsim-c.so"]
        for lib_name in libs:
            filename = os.path.join(COREIR_PATH, "lib", lib_name)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='coreir',
    version='2.0.1',
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
    cmdclass=dict(build_ext=CoreIRBuild),
    zip_safe=False,
)
