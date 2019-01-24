import coreir
from bit_vector import BitVector

context = coreir.Context()
coreir_primitives = context.get_namespace("coreir")
counter_type = context.Record({
    "out": context.Array(16, context.Bit()),
    "clk": context.named_types[("coreir", "clkIn")]
})

counter = context.global_namespace.new_module("counter", counter_type)
counter_definition = counter.new_definition()

Add = coreir_primitives.generators["add"]
Reg = coreir_primitives.generators["reg"]
Const = coreir_primitives.generators["const"]

add_inst = counter_definition.add_generator_instance(
    "add_inst", Add, context.new_values({
        "width": 16
    }))

const_inst = counter_definition.add_generator_instance(
    "const_inst", Const, context.new_values({
        "width": 16
    }), context.new_values({
        "value": BitVector(1, 16)
    }))

reg_inst = counter_definition.add_generator_instance(
    "reg_inst", Reg, context.new_values({
        "width": 16
    }), context.new_values({
        "init": BitVector(0, 16)
    }))

counter_definition.connect(add_inst.select("out"), reg_inst.select("in"))

counter_interface = counter_definition.interface

counter_definition.connect(
    counter_interface.select("clk"), reg_inst.select("clk"))

counter_definition.connect(
    counter_definition.select("const_inst.out"),
    counter_definition.select("add_inst.in0"))

counter_definition.connect(
    counter_definition.select("reg_inst.out"),
    counter_definition.select("add_inst.in1"))

counter_definition.connect(
    counter_definition.select("reg_inst.out"),
    counter_definition.select("self.out"))

counter.definition = counter_definition

counter.print_()

context.run_passes(["rungenerators"])

context.print_()
