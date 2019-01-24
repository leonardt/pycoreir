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
print(f"Add: {Add}")

Add6 = Add(width=6)
print(f"Add6: {Add6}")
Add6.print_()
# TODO: This just gets the "short name". There is a C++ API for "long name"
# which includes the generator arguments
print(f"Add6.name: {Add6.name}")
print(f"Add6.generator_args: {Add6.generator_args}")
gen_args = {x: y.value for (x, y) in Add6.generator_args.items()}
print(f"Add6.generator_args (formatted): {gen_args}")
