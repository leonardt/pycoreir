import coreir
from bit_vector import BitVector
import operator

binary_primitives = [
    ("and", operator.and_),
    ("or", operator.or_),
    ("xor", operator.xor),
    ("add", operator.add),
    ("sub", operator.sub),
    ("mul", operator.mul),
]

def pytest_generate_tests(metafunc):
    if 'binary_primitive' in metafunc.fixturenames:
        metafunc.parametrize("binary_primitive", binary_primitives)
    if 'width' in metafunc.fixturenames:
        metafunc.parametrize("width", [4])
    if 'binary_input0' in metafunc.fixturenames:
        metafunc.parametrize("binary_input0", range(16))
    if 'binary_input1' in metafunc.fixturenames:
        metafunc.parametrize("binary_input1", range(16))


def test_binary_primitive(binary_primitive, width, binary_input0, binary_input1):

    context = coreir.Context()

    def get_lib(lib):
        if lib in {"coreir", "mantle", "corebit"}:
            return context.get_namespace(lib)
        elif lib == "global":
            return context.global_namespace
        else:
            return context.load_library(lib)

    def import_(lib, name):
        return get_lib(lib).generators[name]
    primitive_name, primitive_op = binary_primitive
    coreir_primitive = import_("coreir", primitive_name)
    primitive16 = coreir_primitive(width=width)
    module_typ = context.Record({
        "in0": context.Array(width, context.BitIn()),
        "in1": context.Array(width, context.BitIn()),
        "out": context.Array(width, context.Bit())
    })
    module = context.global_namespace.new_module(f"test_{primitive_name}", module_typ)
    module_def = module.new_definition()
    primitive16_inst = module_def.add_module_instance(f"{primitive_name}_inst", primitive16)
    interface = module_def.interface
    module_def.connect(interface.select("in0"), primitive16_inst.select("in0"))
    module_def.connect(interface.select("in1"), primitive16_inst.select("in1"))
    module_def.connect(interface.select("out"), primitive16_inst.select("out"))
    module.definition = module_def
    sim_primitive16 = coreir.SimulatorState(module)

    a = BitVector(binary_input0, 16)
    b = BitVector(binary_input1, 16)
    sim_primitive16.set_value(["self.in0"], a.as_bool_list())
    sim_primitive16.set_value(["self.in1"], b.as_bool_list())
    sim_primitive16.execute()
    assert sim_primitive16.get_value(["self"], ["out"]) == primitive_op(a, b).as_bool_list()
