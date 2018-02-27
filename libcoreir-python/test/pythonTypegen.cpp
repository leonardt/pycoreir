#include "coreir.h"
#include "coreir/coreir-python.hpp"

using namespace std;
using namespace CoreIR;


int main() {
  
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
  // Type* add12Type = c->Record({
  //   {"in8",c->BitIn()->Arr(13)->Arr(8)},
  //   {"in4",c->BitIn()->Arr(13)->Arr(4)},
  //   {"out",c->Bit()->Arr(13)}
  // });

  // Namespace* coreir = c->getNamespace("coreir");
  // Module* add12 = g->newModuleDecl("Add12",add12Type);
  // ModuleDef* def = add12->newModuleDef();
  //   def->addInstance("add8_upper",addN,{{"width",Const::make(c,13)},{"N",Const::make(c,8)}});
  //   def->addInstance("add4_lower",addN,{{"width",Const::make(c,13)},{"N",Const::make(c,4)}});
  //   def->addInstance("add2_join",coreir->getGenerator("add"),{{"width",Const::make(c,13)}});
  //   def->connect("self.in8","add8_upper.in");
  //   def->connect("self.in4","add4_lower.in");
  //   def->connect("add8_upper.out","add2_join.in0");
  //   def->connect("add4_lower.out","add2_join.in1");
  //   def->connect("add2_join.out","self.out");
  // add12->setDef(def);
  // add12->print();
  // 
  // c->runPasses({"rungenerators","flatten"});
  // add12->print();

  // Define Add4 Module
  Type* add4Type = c->Record({
    {"in0",c->BitIn()->Arr(13)->Arr(2)},
    {"in1",c->BitIn()->Arr(13)->Arr(2)},
    {"out",c->Bit()->Arr(13)}
  });
  Namespace* coreir = c->getNamespace("coreir");
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

  deleteContext(c);
}
