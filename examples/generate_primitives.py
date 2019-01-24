import coreir

context = coreir.Context()
coreir_primitives = context.get_namespace("coreir")
Add = coreir_primitives.generators["add"]

counter = context.global_namespace.new_module("counter", counter_type)
counter_definition = counter.new_definition()

add_inst = counter_definition.add_generator_instance(
    "add_inst", Add, context.new_values({
        "width": 16
    }))
