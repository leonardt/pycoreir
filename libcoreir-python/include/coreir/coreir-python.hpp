#ifndef COREIR_PYTHON_HPP_
#define COREIR_PYTHON_HPP_

#include "coreir/ir/typegen.h"
#include <Python.h>
namespace CoreIR {
    void pythonInitialize();
    void pythonFinalize();

    class TypeGenFromPython : public TypeGen {
      std::string moduleName;
      std::string functionName;

      protected :
        virtual Type* createType(Values values) override;
      public :
        TypeGenFromPython(Namespace* ns, std::string name, Params params,
                          std::string moduleName, std::string functionName, bool
                          flipped=false) :
            TypeGen(ns,name,params,flipped), moduleName(moduleName),
            functionName(functionName) {}
        bool hasType(Values genargs) override;
        std::string toString() const override {return name; }
        static TypeGenFromPython* make(Namespace* ns, std::string name, Params genparams, std::string moduleName, std::string functionName, bool flipped=false);

    };

    ModuleDefGenFun ModuleDefGenFunFromPython(std::string moduleName, std::string functionName);
}
#endif //COREIR_PYTHON_HPP_
