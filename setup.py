from setuptools import setup

setup(
    name='coreir',
    version='0.26-alpha',
    description='Python bindings for CoreIR',
    packages=["coreir"],
    license='BSD License',
    url='https://github.com/leonardt/pycoreir',
    author='Leonard Truong',
    author_email='lenny@cs.stanford.edu',
    install_requires=["bit_vector >= 0.34a, <=0.36a"]
)
