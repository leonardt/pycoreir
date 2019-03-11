from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='coreir',
    version='2.0.0',
    description='Python bindings for CoreIR',
    packages=["coreir"],
    license='BSD License',
    url='https://github.com/leonardt/pycoreir',
    author='Leonard Truong',
    author_email='lenny@cs.stanford.edu',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["hwtypes>=1.0.*"]
)
