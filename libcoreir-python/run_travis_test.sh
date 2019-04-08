make install prefix=/pycoreir/coreir-cpp/include LDFLAGS=-L/pycoreir/coreir-cpp/lib
PYTHONPATH=$PYTHONPATH:test make test CXXFLAGS=-I/pycoreir/coreir-cpp/include LDFLAGS=-L/pycoreir/coreir-cpp/lib
