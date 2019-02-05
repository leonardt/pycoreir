from setuptools import setup

setup(
    name='coreir',
    version='1.0.0',
    description='Python bindings for CoreIR',
    packages=["coreir"],
    license='BSD License',
    url='https://github.com/leonardt/pycoreir',
    author='Leonard Truong',
    author_email='lenny@cs.stanford.edu',
    install_requires=["bit_vector >= 0.39a, <=0.42a0"]
)
