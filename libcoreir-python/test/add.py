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
        subAdd = context.global_namespace.generators["addN"](width=width, N=N // 2)
        addN_0 = module_def.add_module_instance("addN_0", subAdd)
        addN_1 = module_def.add_module_instance("addN_1", subAdd)
        for i in range(0, N//2):
            module_def.connect(module_def.interface.select("in").select(str(i)),
                               addN_0.select("in").select(str(i)))
            module_def.connect(module_def.interface.select("in").select(str(i)),
                               addN_1.select("in").select(str(i)))
        module_def.connect(addN_0.select("out"), join_inst.select("in0"))
        module_def.connect(addN_1.select("out"), join_inst.select("in1"))
