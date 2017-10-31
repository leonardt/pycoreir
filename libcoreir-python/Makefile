UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S), Linux)
TARGET = so
prefix?=/usr
endif
ifeq ($(UNAME_S), Darwin)
TARGET = dylib
prefix?=/usr/local
endif

CXX ?= g++

override CXXFLAGS += -std=c++11 -Wall -fPIC -Werror -I./include/
override LDFLAGS += -lcoreir

PYTHON_CONFIG ?= python-config
PYTHONHOME = $(shell $(PYTHON_CONFIG) --prefix)
override CXXFLAGS += $(shell $(PYTHON_CONFIG) --includes) -DCOREIR_INCLUDE_PYTHON_TYPEGEN -DPYTHON_HOME="L\"$(PYTHONHOME)\""
PYTHON_LIBS = $(PYTHONHOME)/lib
override LDFLAGS += -L $(PYTHON_LIBS) $(shell $(PYTHON_CONFIG) --libs)
DYLDFLAGS = -Wl,-rpath,$(PYTHON_LIBS)

clean:
	rm -rf build/*

build/libcoreir-python.so: build/libcoreir-python.o
	$(CXX) $(LDFLAGS) -shared -o $@ $^ $(PYLDFLAGS)

build/libcoreir-python.dylib: build/libcoreir-python.o
	$(CXX) $(LDFLAGS) $(DYLDFLAGS) -dynamiclib -o $@ $^

build/libcoreir-python.o: coreir-python.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

.PHONY: install
install: build/libcoreir-python.$(TARGET)
	install build/libcoreir-python.$(TARGET) $(prefix)/lib

.PHONY: uninstall
uninstall:
	-rm $(prefix)/lib/libcoreir-python.$(TARGET)

test: build/libcoreir-python.$(TARGET) test/pythonTypegen.cpp
	$(CXX) $(CXXFLAGS) -o build/testPythonTypegen test/pythonTypegen.cpp -L ./build/ -lcoreir -lcoreir-python $(LDFLAGS) $(DYLDFLAGS)
	./build/testPythonTypegen
