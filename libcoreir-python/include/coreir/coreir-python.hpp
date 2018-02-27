#ifndef COREIR_PYTHON_HPP_
#define COREIR_PYTHON_HPP_

#include "coreir/ir/typegen.h"
#include <Python.h>
namespace CoreIR {

    class TypeGenFromPython : public TypeGen {
      std::string moduleName;
      std::string functionName;

      public:
        TypeGenFromPython(Namespace* ns, std::string name, Params params,
                          std::string moduleName, std::string functionName, bool
                          flipped=false) :
            TypeGen(ns,name,params,flipped), moduleName(moduleName),
            functionName(functionName) {}
        Type* createType(Context* c, Values values) override;
        std::string toString() const override {return name; }
        void print() const override {}//TODO
    };

    ModuleDefGenFun ModuleDefGenFunFromPython(std::string moduleName, std::string functionName);
}

#endif //COREIR_PYTHON_HPP_
