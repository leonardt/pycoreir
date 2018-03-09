import coreir
#
# seq to int
#
def seq2int(l):
    n = len(l)

    i = 0
    for j in range(n):
        if l[j]:
            i |= 1 << j
    return i


#
# int to seq
#
def int2seq(i, n=0):
    # if isinstance(i, StringTypes):
    #     i = ord(i)

    # find minimum number of bits needed for i
    if n == 0:
        j = i
        while j:
            n += 1
            j >>= 1

    return [1 if i & (1 << j) else 0 for j in range(n)]

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

primitives = ["add"]

def pytest_generate_tests(metafunc):
    if 'primitive' in metafunc.fixturenames:
        metafunc.parametrize("primitive", primitives)

def test_primitive(primitive):
    coreir_add = import_("coreir", primitive)
    width = 16
    add16 = coreir_add(width=width)
    module_typ = context.Record({
        "in0": context.Array(width, context.BitIn()),
        "in1": context.Array(width, context.BitIn()),
        "out": context.Array(width, context.Bit())
    })
    module = context.global_namespace.new_module(f"test_{primitive}", module_typ)
    module_def = module.new_definition()
    add16_inst = module_def.add_module_instance(f"{primitive}_inst", add16)
    interface = module_def.interface
    module_def.connect(interface.select("in0"), add16_inst.select("in0"))
    module_def.connect(interface.select("in1"), add16_inst.select("in1"))
    module_def.connect(interface.select("out"), add16_inst.select("out"))
    module.definition = module_def
    sim_add16 = coreir.SimulatorState(module)

    a = 3
    b = 5
    sim_add16.set_value(["self.in0"], int2seq(a, 16))
    sim_add16.set_value(["self.in1"], int2seq(b, 16))
    sim_add16.execute()
    assert seq2int(sim_add16.get_value(["self"], ["out"])) == a + b
