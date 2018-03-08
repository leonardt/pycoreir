#include "coreir.h"
#include "coreir/coreir-python.hpp"

using namespace std;
using namespace CoreIR;


int main() {
  
  pythonInitialize();
  // New context
  Context* c = newContext();
  
  //Put this addN in the global namespace
  Namespace* g = c->getGlobal();
  
  //Declare a TypeGenerator (in global) for addN
  TypeGen* typegen = new TypeGenFromPython(g, "addN_type", {{"width",
          c->Int()},{"N", c->Int()}}, "add", "add_type_gen");
  g->addTypeGen(typegen);

  Generator* addN =
      g->newGeneratorDecl("addN",g->getTypeGen("addN_type"),{{"width", c->Int()},{"N", c->Int()}});
  
  addN->setGeneratorDefFromFun(ModuleDefGenFunFromPython("add", "add_generator"));
  
  // Define Add12 Module
  Type* add12Type = c->Record({
    {"in8",c->BitIn()->Arr(13)->Arr(8)},
    {"in4",c->BitIn()->Arr(13)->Arr(4)},
    {"out",c->Bit()->Arr(13)}
  });

  Namespace* coreir = c->getNamespace("coreir");
  Module* add12 = g->newModuleDecl("Add12",add12Type);
  ModuleDef* add12Def = add12->newModuleDef();
    add12Def->addInstance("add8_upper",addN,{{"width",Const::make(c,13)},{"N",Const::make(c,8)}});
    add12Def->addInstance("add4_lower",addN,{{"width",Const::make(c,13)},{"N",Const::make(c,4)}});
    add12Def->addInstance("add2_join",coreir->getGenerator("add"),{{"width",Const::make(c,13)}});
    add12Def->connect("self.in8","add8_upper.in");
    add12Def->connect("self.in4","add4_lower.in");
    add12Def->connect("add8_upper.out","add2_join.in0");
    add12Def->connect("add4_lower.out","add2_join.in1");
    add12Def->connect("add2_join.out","self.out");
  add12->setDef(add12Def);
  add12->print();
  
  c->runPasses({"rungenerators","flatten"});
  add12->print();

  // Define Add4 Module
  Type* add4Type = c->Record({
    {"in0",c->BitIn()->Arr(13)->Arr(2)},
    {"in1",c->BitIn()->Arr(13)->Arr(2)},
    {"out",c->Bit()->Arr(13)}
  });
  Module* add4 = g->newModuleDecl("Add4",add4Type);
  ModuleDef* def = add4->newModuleDef();
    def->addInstance("add2_upper",addN,{{"width",Const::make(c,13)},{"N",Const::make(c,2)}});
    def->addInstance("add2_lower",addN,{{"width",Const::make(c,13)},{"N",Const::make(c,2)}});
    def->addInstance("add2_join",coreir->getGenerator("add"),{{"width",Const::make(c,13)}});
    def->connect("self.in0","add2_upper.in");
    def->connect("self.in1","add2_lower.in");
    def->connect("add2_upper.out","add2_join.in0");
    def->connect("add2_lower.out","add2_join.in1");
    def->connect("add2_join.out","self.out");
  add4->setDef(def);
  add4->print();
  
  c->runPasses({"rungenerators","flatten"});
  add4->print();

  TypeGen* double_typegen = new TypeGenFromPython(g, "double_type", {{"width",
          c->Int()}}, "add", "double_type_gen");
  g->addTypeGen(double_typegen);

  Generator* doubleGen =
      g->newGeneratorDecl("double",g->getTypeGen("double_type"),{{"width", c->Int()}});
  
  doubleGen->setGeneratorDefFromFun(ModuleDefGenFunFromPython("add", "double"));
  Type* doubleType = c->Record({
    {"in",c->BitIn()->Arr(13)},
    {"out",c->Bit()->Arr(13)}
  });
  Module* doubleMod = g->newModuleDecl("Double",doubleType);
  ModuleDef* doubleDef = doubleMod->newModuleDef();
    doubleDef->addInstance("double",doubleGen,{{"width",Const::make(c,13)}});
    doubleDef->connect("self.in","double.I");
    doubleDef->connect("double.O","self.out");
  doubleMod->setDef(doubleDef);
  doubleMod->print();
  
  c->runPasses({"rungenerators","flatten"});
  doubleMod->print();

  deleteContext(c);
  pythonFinalize();
}
