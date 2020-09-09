import coreir
import os


def test_genargs():
    context = coreir.Context()
    mod = context.load_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "genargs.json"))
    for instance in mod.definition.instances:
        assert instance.module.generator_args["width"].value == 4

    # test creating coreir module from Value
    width_value = mod.definition.instances[0].module.generator_args["width"]
    assert isinstance(width_value, coreir.Value)
    const_mod = context.get_namespace("coreir").generators["const"](width=width_value)


if __name__ == "__main__":
    test_genargs()
