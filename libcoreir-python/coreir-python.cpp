#include "coreir/coreir-python.hpp"
#include "coreir/ir/namespace.h"

static PyGILState_STATE gstate;

void CoreIR::pythonInitialize() {
    wchar_t python_home[] = PYTHON_HOME;
    Py_SetPythonHome(python_home);
    wchar_t python_executable[] = PYTHON_EXECUTABLE;
    Py_SetProgramName(python_executable);
    Py_Initialize();
    PyEval_InitThreads();
}

void CoreIR::pythonFinalize() {
    gstate = PyGILState_Ensure();
    Py_Finalize();
}

CoreIR::Type* CoreIR::TypeGenFromPython::createType(Values values) {
  gstate = PyGILState_Ensure();
  Type* type_ptr = NULL;
  PyObject *py_module = PyImport_ImportModule(moduleName.c_str());
  if (py_module != NULL) {
    Py_INCREF(py_module);
    PyObject *py_typeGenFunc = PyObject_GetAttrString(py_module, functionName.c_str());
    if (py_typeGenFunc && PyCallable_Check(py_typeGenFunc)) {
      Py_INCREF(py_typeGenFunc);
      int size = values.size();
      char** names = (char**) malloc(size * sizeof(char*));
      Value** values_ptrs = (Value**) malloc(sizeof(Value*) * size);
      int count = 0;
      for (auto element : values) {
          std::size_t name_length = element.first.size();
          names[count] = (char*) malloc(sizeof(char) * name_length + 1);
          memcpy(names[count], element.first.c_str(), name_length + 1);
          values_ptrs[count] = element.second;
          count++;
      }
      char signature[] = "llli";
      Context *c = ns->getContext();
      PyObject* value_object = PyObject_CallFunction(py_typeGenFunc, signature,
              (void *) c, (void *) names, (void *) values_ptrs, size);
      if (!value_object) {
        if (PyErr_Occurred()) PyErr_Print();
        std::cerr << "Error calling typegen function `" << functionName << "`" << std::endl;
        exit(1);
      } else {
        type_ptr = (Type *) PyLong_AsVoidPtr(value_object);
        Py_DECREF(value_object);
      }
      for (uint i = 0; i < values.size(); i++) {
        free(names[i]);
      }
      free(names);
      free(values_ptrs);
      Py_DECREF(py_typeGenFunc);
    } else {
      if (PyErr_Occurred()) PyErr_Print();
      std::cerr << "Cannot find function `" << functionName << "`" << std::endl;
      exit(1);
    }
    Py_DECREF(py_module);
  } else {
    PyErr_Print();
    std::cerr << "Failed to load module `" << moduleName << "`" << std::endl;
    exit(1);
  }
  PyGILState_Release(gstate);

  // FIXME: Can we free char** names and Value** values_ptrs because
  // they are no longer used since the interpreter's been finalized?
  // Currently they will be cleaned up eventually by the context, but
  // if we can free here that should reduce memory consumption
  return type_ptr;
}

CoreIR::ModuleDefGenFun CoreIR::ModuleDefGenFunFromPython(std::string moduleName, std::string functionName) {
  return [=](Context* c, Values genargs, ModuleDef* def) {
    gstate = PyGILState_Ensure();
    PyObject *py_module = PyImport_ImportModule(moduleName.c_str());
    if (py_module != NULL) {
      Py_INCREF(py_module);
      PyObject *py_moduleDefGenFunc = PyObject_GetAttrString(py_module, functionName.c_str());
      if (py_moduleDefGenFunc && PyCallable_Check(py_moduleDefGenFunc)) {
        Py_INCREF(py_moduleDefGenFunc);
        int size = genargs.size();
        char** names = (char**) malloc(size * sizeof(char*));
        Value** values_ptrs = (Value**) malloc(sizeof(Value*) * size);
        int count = 0;
        for (auto element : genargs) {
            std::size_t name_length = element.first.size();
            names[count] = (char*) malloc(sizeof(char) * name_length + 1);
            memcpy(names[count], element.first.c_str(), name_length + 1);
            values_ptrs[count] = element.second;
            count++;
        }
        char signature[] = "lllil";
        PyObject_CallFunction(py_moduleDefGenFunc, signature,
                (void *) c, (void *) names, (void *) values_ptrs, size, (void *) def);
        if (PyErr_Occurred()) {
            PyErr_Print();
            std::cerr << "Error calling generator function `" << functionName << "`" << std::endl;
            exit(1);
        }
        for (uint i = 0; i < genargs.size(); i++) {
          free(names[i]);
        }
        free(names);
        free(values_ptrs);
        Py_DECREF(py_moduleDefGenFunc);
      } else {
        if (PyErr_Occurred()) PyErr_Print();
        std::cerr << "Cannot find function `" << functionName << "`" << std::endl;
        exit(1);
      }
      Py_DECREF(py_module);
    } else {
      PyErr_Print();
      std::cerr << "Failed to load `" << moduleName << "`" << std::endl;
      exit(1);
    }
    PyGILState_Release(gstate);
  };
}

CoreIR::TypeGenFromPython* CoreIR::TypeGenFromPython::make(CoreIR::Namespace* ns, std::string name, Params genparams, std::string moduleName, std::string functionName, bool flipped) {
  
  CoreIR::TypeGenFromPython* tg = new CoreIR::TypeGenFromPython(ns,name,genparams,moduleName,functionName,flipped);
  ns->addTypeGen(tg);
  return tg;

}

bool CoreIR::TypeGenFromPython::hasType(Values genargs) {
    return true;
}
