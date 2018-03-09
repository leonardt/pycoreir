import coreir
from bit_vector import BitVector
import operator

def get_lib(lib, context):
    if lib in {"coreir", "mantle", "corebit"}:
        return context.get_namespace(lib)
    elif lib == "global":
        return context.global_namespace
    else:
        return context.load_library(lib)

def import_(lib, name):
    context = coreir.Context()
    lib = get_lib(lib, context)
    return lib.generators[name], context

unary_primitives = [
    ("not", operator.invert),
    # ("neg", operator.neg),
]

binary_primitives = [
    ("and", operator.and_),
    ("or", operator.or_),
    ("xor", operator.xor),
    ("add", operator.add),
    ("sub", operator.sub),
    ("mul", operator.mul),
    ("shl", operator.lshift),
    ("lshr", operator.rshift),
]

comparison_primitives = [
    ("slt", operator.lt, True),
    ("sle", operator.le, True),
    ("sgt", operator.gt, True),
    ("sge", operator.ge, True),
    ("ult", operator.lt, False),
    ("ule", operator.le, False),
    ("ugt", operator.gt, False),
    ("uge", operator.ge, False),
]

def pytest_generate_tests(metafunc):
    if 'binary_primitive' in metafunc.fixturenames:
        metafunc.parametrize("binary_primitive", binary_primitives)
    if 'unary_primitive' in metafunc.fixturenames:
        metafunc.parametrize("unary_primitive", unary_primitives)
    if 'comparison_primitive' in metafunc.fixturenames:
        metafunc.parametrize("comparison_primitive", comparison_primitives)
    if 'width' in metafunc.fixturenames:
        metafunc.parametrize("width", [4])
    if 'input0' in metafunc.fixturenames:
        metafunc.parametrize("input0", range(16))
    if 'input1' in metafunc.fixturenames:
        metafunc.parametrize("input1", range(16))

def test_unary_primitive(unary_primitive, width, input0):

    primitive_name, primitive_op = unary_primitive
    coreir_primitive, context = import_("coreir", primitive_name)
    primitive16 = coreir_primitive(width=width)
    module_typ = context.Record({
        "in": context.Array(width, context.BitIn()),
        "out": context.Array(width, context.Bit())
    })
    module = context.global_namespace.new_module(f"test_{primitive_name}", module_typ)
    module_def = module.new_definition()
    primitive16_inst = module_def.add_module_instance(f"{primitive_name}_inst", primitive16)
    interface = module_def.interface
    module_def.connect(interface.select("in"), primitive16_inst.select("in"))
    module_def.connect(interface.select("out"), primitive16_inst.select("out"))
    module.definition = module_def
    sim_primitive16 = coreir.SimulatorState(module)

    a = BitVector(input0, 16)
    sim_primitive16.set_value(["self.in"], a.as_bool_list())
    sim_primitive16.execute()
    assert BitVector(sim_primitive16.get_value(["self"], ["out"])) == primitive_op(a)

def test_binary_primitive(binary_primitive, width, input0, input1):

    primitive_name, primitive_op = binary_primitive
    coreir_primitive, context = import_("coreir", primitive_name)
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

    a = BitVector(input0, 16)
    b = BitVector(input1, 16)
    sim_primitive16.set_value(["self.in0"], a.as_bool_list())
    sim_primitive16.set_value(["self.in1"], b.as_bool_list())
    sim_primitive16.execute()
    assert BitVector(sim_primitive16.get_value(["self"], ["out"])) == primitive_op(a, b)

def test_eq(width, input0, input1):

    coreir_primitive, context = import_("coreir", "eq")
    primitive_name = "eq"
    primitive_op = operator.eq
    primitive16 = coreir_primitive(width=width)
    module_typ = context.Record({
        "in0": context.Array(width, context.BitIn()),
        "in1": context.Array(width, context.BitIn()),
        "out": context.Bit()
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

    a = BitVector(input0, 16)
    b = BitVector(input1, 16)
    sim_primitive16.set_value(["self.in0"], a.as_bool_list())
    sim_primitive16.set_value(["self.in1"], b.as_bool_list())
    sim_primitive16.execute()
    assert BitVector(sim_primitive16.get_value(["self"], ["out"])) == primitive_op(a, b)

def test_comparison_primitive(comparison_primitive, width, input0, input1):

    primitive_name, primitive_op, signed = comparison_primitive
    coreir_primitive, context = import_("coreir", primitive_name)
    primitive16 = coreir_primitive(width=width)
    module_typ = context.Record({
        "in0": context.Array(width, context.BitIn()),
        "in1": context.Array(width, context.BitIn()),
        "out": context.Bit()
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

    a = BitVector(input0, 16, signed=signed)
    b = BitVector(input1, 16, signed=signed)
    sim_primitive16.set_value(["self.in0"], a.as_bool_list())
    sim_primitive16.set_value(["self.in1"], b.as_bool_list())
    sim_primitive16.execute()
    assert BitVector(sim_primitive16.get_value(["self"], ["out"])) == primitive_op(a, b)

# TODO: mux
# TODO: reg
# TODO: regrst
# TODO: const
# TODO: term
# TODO: slice
# TODO: concat

# TODO: corebit
# TODO: and, or, xor
# TODO: wire, not
# TODO: mux
# TODO: const
# TODO: term
