from setuptools import setup

setup(
    name='coreir',
    version='0.29-alpha',
    description='Python bindings for CoreIR',
    packages=["coreir"],
    license='BSD License',
    url='https://github.com/leonardt/pycoreir',
    author='Leonard Truong',
    author_email='lenny@cs.stanford.edu',
    install_requires=["bit_vector == 0.39a"]
)
