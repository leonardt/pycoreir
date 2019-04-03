import coreir

@coreir.type_gen
def add_type_gen(context, values):
    width = values['width'].value
    N = values['N'].value
    return context.Record({
        "in": context.Array(N, context.Array(width, context.BitIn())),
        "out": context.Array(width, context.Bit())
    })

@coreir.generator_
def add_generator(context, values, module_def):
    width = values['width'].value
    N = values['N'].value


    add_gen = context.get_namespace("coreir").generators["add"]
    join = add_gen(width=width)

    join_inst = module_def.add_module_instance("join", join)
    module_def.connect(join_inst.select("out"), module_def.interface.select('out'))
    if N == 2:
        module_def.connect(module_def.interface.select("in").select("0"), join_inst.select("in0"))
        module_def.connect(module_def.interface.select("in").select("1"), join_inst.select("in1"))
    else:
        # FIXME: Recursion means c++ -> python -> c++ -> python which then
        # causes a segfault, GIL?
        subAdd = context.global_namespace.generators["addN"]
        addN_0 = module_def.add_generator_instance("addN_0", subAdd, {"width": width, "N": N // 2})
        addN_1 = module_def.add_generator_instance("addN_1", subAdd, {"width": width, "N": N // 2})
        for i in range(0, N//2):
            module_def.connect(module_def.interface.select("in").select(str(i)),
                               addN_0.select("in").select(str(i)))
            module_def.connect(module_def.interface.select("in").select(str(i + N // 2)),
                               addN_1.select("in").select(str(i)))
        module_def.connect(addN_0.select("out"), join_inst.select("in0"))
        module_def.connect(addN_1.select("out"), join_inst.select("in1"))
    module_def.print_()

@coreir.type_gen
def double_type_gen(context, values):
    width = values['width'].value
    return context.Record({
        "I": context.Array(width, context.BitIn()),
        "O": context.Array(width, context.Bit())
    })

@coreir.generator_
def double(context, values, module_def):
    import magma.backend.coreir_
    width = values['width'].value
    doubleT = magma.Bits[width]
    double = magma.DefineCircuit("double", "I", magma.In(doubleT), "O", magma.Out(doubleT))
    shift_amount = 2
    output = magma.concat(double.I[shift_amount:width], magma.bits(0, shift_amount))
    magma.wire(output, double.O)
    magma.backend.coreir_.CoreIRBackend(context).compile_definition_to_module_definition(double, module_def)
