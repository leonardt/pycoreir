import coreir
from collections import OrderedDict
from hwtypes import BitVector
import test_utils
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


def test_coreir():
    context = coreir.Context()
    assert context.global_namespace.name == "global"
    assert context.has_namespace("coreir")
    coreir_stdlib = context.get_namespace("coreir")
    assert coreir_stdlib.name == "coreir"

    add_generator = coreir_stdlib.generators["add"]
    assert add_generator.name == "add"

    module_typ = context.Record({"input": context.Array(8, context.BitIn()), "output": context.Array(9, context.Bit())})
    module = context.global_namespace.new_module("multiply_by_2", module_typ)
    module_def = module.new_definition()
    add8_inst = module_def.add_generator_instance("add8_inst", add_generator, context.new_values({"width": 8}))
    assert add8_inst.module.generator_args["width"].value == 8

def test_ice40():
    context = coreir.Context()
    coreir_ice40 = context.load_library("ice40")
    SB_LUT4 = coreir_ice40.modules["SB_LUT4"]
    SB_CARRY = coreir_ice40.modules["SB_CARRY"]
    SB_DFF = coreir_ice40.modules["SB_DFF"]
    SB_DFFE = coreir_ice40.modules["SB_DFFE"]
    module_typ = context.Record(
        # NOTE: A sorted OrderedDict so the json output is deterministic
        OrderedDict(
            sorted({
                "I": context.Array(4, context.BitIn()),
                "O": context.Bit()
            }.items())
        )
    )
    module = context.global_namespace.new_module("test_module", module_typ)
    module_def = module.new_definition()
    A0 = 0xAAAA
    A1 = 0xCCCC
    A2 = 0xF0F0
    A3 = 0xFF00

    lut0 = module_def.add_module_instance("lut0", SB_LUT4, context.new_values({"LUT_INIT": BitVector[16](A0 & A1)}))
    module_def.connect(module_def.select("self.I.0"), module_def.select("lut0.I0"))
    module_def.connect(module_def.select("self.I.1"), module_def.select("lut0.I1"))
    module_def.connect(module_def.select("self.I.2"), module_def.select("lut0.I2"))
    module_def.connect(module_def.select("self.I.3"), module_def.select("lut0.I3"))
    module_def.connect(module_def.select("self.O")  , module_def.select("lut0.O"))
    module.definition = module_def
    module.save_to_file(os.path.join(dir_path, "ice40_test.json"))
    with open(os.path.join(dir_path, "ice40_test.json")) as actual:
        with open(os.path.join(dir_path, "ice40_test_gold.json")) as gold:
            assert actual.read() == gold.read()

def test_new_namespace():
    context = coreir.Context()
    assert not context.has_namespace("foo")
    foons = context.new_namespace("foo")
    assert context.has_namespace("foo")
    module_typ = context.Record({"input": context.Array(8, context.BitIn()), "output": context.Array(9, context.Bit())})
    module = foons.new_module("bar", module_typ)
    assert module.namespace == foons
    assert module.params is not None

if __name__ == "__main__":
    test_ice40()


