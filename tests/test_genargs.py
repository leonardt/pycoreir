import coreir
import os


def test_genargs():
    context = coreir.Context()
    cgra = context.load_library("cgralib")
    mod = context.load_from_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "genargs.json"))
    for instance in mod.definition.instances:
        for name, arg in instance.generator_args.items():
            if name == "width":
                assert arg.value == 4
            elif name in {"has_en", "has_clr", "has_rst"}:
                assert instance.module_name == "reg"
                assert arg.value == False
            else:
                assert False, "Should not reach this statement, {}".format(name)


if __name__ == "__main__":
    test_genargs()
