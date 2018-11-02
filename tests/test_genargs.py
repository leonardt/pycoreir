import coreir
import os


def test_genargs():
    context = coreir.Context()
    mod = context.load_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "genargs.json"))
    for instance in mod.definition.instances:
        assert instance.module.generator_args["width"].value == 4


if __name__ == "__main__":
    test_genargs()
