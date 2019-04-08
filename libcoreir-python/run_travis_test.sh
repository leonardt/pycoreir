make install PYTHON_CONFIG=python3-config prefix=/pycoreir/coreir-cpp/include CXXFLAGS=-I/pycoreir/coreir-cpp/include LDFLAGS=-L/pycoreir/coreir-cpp/lib
PYTHONPATH=$PYTHONPATH:test make test PYTHON_CONFIG=python3-config CXXFLAGS=-I/pycoreir/coreir-cpp/include LDFLAGS=-L/pycoreir/coreir-cpp/lib
