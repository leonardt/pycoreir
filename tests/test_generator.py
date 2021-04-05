import coreir
from coreir.type import ValueType
from hwtypes import BitVector
import os
import filecmp
import pytest

def get_lib(c, lib):
    if lib in {"coreir", "mantle", "corebit"}:
        return c.get_namespace(lib)
    elif lib == "global":
        return c.global_namespace
    else:
        return c.load_library(lib)

def import_(c, lib, name):
    return get_lib(c, lib).generators[name]

def test_add():
    c = coreir.Context()
    coreir_add = import_(c, "coreir", "add")
    assert isinstance(coreir_add, coreir.Generator)
    assert coreir_add.name == "add"
    assert 'width' in coreir_add.params
    assert isinstance(coreir_add.params['width'], ValueType)
    assert coreir_add.params['width'].kind == int
    add16 = coreir_add(width=16)
    assert add16.name == "add"
    assert add16.generated == True
    assert isinstance(add16.type, coreir.Record)
    add16.type.print_()
    for arg in ['in0', 'in1', 'out']:
        assert add16.type[arg].kind == "Array"
        assert len(add16.type[arg]) == 16

#Need to skip this as serialize_to_file does not handle module dependencies in genargs
@pytest.mark.skip
def test_map_mulby2():
    c = coreir.Context()
    width = 8
    numInputs = 4
    module_typ = c.Record({"in": c.Array(width, c.BitIn()), "out": c.Array(width, c.Bit())})
    mulBy2 = c.global_namespace.new_module("mulBy2", module_typ)
    mulBy2.print_()
    mulBy2Def = mulBy2.new_definition()

    coreir_mul = import_(c, "coreir", "mul")
    mul = coreir_mul(width=width)
    mul_inst = mulBy2Def.add_module_instance("mul", mul)
    mulBy2Def.connect(mulBy2Def.interface.select("in"), mul_inst.select("in0"))
    const_instantiable = c.get_namespace("coreir").generators["const"]
    gen_args = c.new_values({"width": width})
    config_args = c.new_values({"value": BitVector[8](8)})
    two = mulBy2Def.add_generator_instance("two", const_instantiable, gen_args, config_args)
    mulBy2Def.connect(two.select("out"), mul_inst.select("in1"));
    mulBy2Def.connect(mul_inst.select("out"), mulBy2Def.interface.select("out"))
    mulBy2.definition = mulBy2Def

    mapParallelParams = c.new_values({"numInputs": numInputs, "operator": mulBy2})

    test_module_typ = c.Record({"in": c.Array(numInputs, c.Array(width,
        c.BitIn())), "out": c.Array(numInputs, c.Array(width, c.Bit()))})
    test_module = c.global_namespace.new_module("test_module", test_module_typ)
    test_module_def = test_module.new_definition()
    mapParallel = import_(c, "aetherlinglib", "mapParallel")
    mapMod = mapParallel(numInputs=numInputs, operator=mulBy2)
    mapMulBy2 = test_module_def.add_module_instance("mapMulBy2", mapMod)
    test_module_def.connect(test_module_def.interface.select("in"), mapMulBy2.select("in"));
    test_module_def.connect(mapMulBy2.select("out"), test_module_def.interface.select("out"));
    test_module_def.print_()
    test_module.definition = test_module_def
    test_module.print_()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    build_file = os.path.join(dir_path, "build/mapParallel_test.json")
    gold_file = os.path.join(dir_path, "gold/mapParallel_test_gold.json")

    c.set_top(test_module)
    c.serialize_to_file(build_file)
    filecmp.cmp(build_file, gold_file)
    del c

    c = coreir.Context()
    mod = c.load_from_file(build_file)
    mod.print_()

if __name__ == "__main__":
    test_map_mulby2()
