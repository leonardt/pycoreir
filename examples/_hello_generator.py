"""
NOTE: Example does not currently work, need to add support for defining a
type_gen in Python
"""
import coreir


context = coreir.Context()

params = context.newParams({"width": int})

def type_gen(context, args):
    width = args["width"]
    return context.Record({
        "en": context.BitIn(),
        "out": context.Array(width, context.Bit()),
        "clk": context.named_types[("coreir", "clkIn")]
    })

counter_type_gen = context.global_namespace.new_type_gen("counterTypeGen", params, type_gen)

counter = context.global_namespace.new_generator_decl("counter", counter_type_gen, params)

def generator_definition(module_definition, context, type_, args):
    inst_args = context.newArgs({"width": args["width"]})
    module_definition.add_instance("add_inst", "coreir.add", inst_args)
    module_definition.add_instance("const_inst", "coreir.const", inst_args,
            context.newArgs({"value": 1}))
    module_definition.add_instance("reg_inst", "coreir.reg",
            context.newArgs({"width": args["width"], "en": True}))

    module_definition.connect("self.clk", "reg_inst.clk")
    module_definition.connect("self.en", "reg_inst.en")
    module_definition.connect("const_inst.out", "add_inst.in0")
    module_definition.connect("add_inst.out", "reg_inst.in")
    module_definition.connect("reg_inst.out", "add_inst.in1")
    module_definition.connect("reg_inst.out", "self.out")

test_bench = context.global_namespace.new_module("counterTestBench", context.Record())
test_bench_definition = test_bench.new_definition()

test_bench_definition.add_generator_instance("counter0", "global.counter",
        context.newArgs({"width": 17}))
test_bench_definition.add_generator_instance("counter1", "global.counter",
        context.newArgs({"width": 23}))
test_bench_definition.connect("counter0.out.16", "counter1.en")

test_bench.definition = test_bench_definition

counter.print_()
test_bench.print_()

context.run_passes(["rungenerators"])
