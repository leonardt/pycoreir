from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects

install_requires = []
extra_requires = {}
for item in parse_requirements("requirements.txt", session=False):
    req = str(item.req)
    if item.markers is not None:
        req += ";" + str(item.markers)
    install_requires.append(req)

setup(
    name='coreir',
    version='0.18-alpha',
    description='Python bindings for CoreIR',
    packages=["coreir"],
    license='BSD License',
    url='https://github.com/leonardt/pycoreir',
    author='Leonard Truong',
    author_email='lenny@cs.stanford.edu',
    install_requires=install_requires
)
