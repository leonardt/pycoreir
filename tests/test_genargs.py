import coreir
import os


def test_genargs():
    context = coreir.Context()
    commonlib = context.load_library("commonlib")
    mod = context.load_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "genargs.json"))
    for instance in mod.definition.instances:
        for name, arg in instance.module.generator_args.items():
            if name == "bitwidth":
                assert arg.value == 16
            elif name == "image_width":
                assert arg.value == 10
            elif name == "stencil_height":
                assert arg.value == 3
            elif name == "stencil_width":
                assert arg.value == 1
            else:
                assert False, "Should not reach this statement, {}".format(name)


if __name__ == "__main__":
    test_genargs()
