import coreir

def test_namespace():
    context = coreir.Context()
    coreir_namespace = context.get_namespace("coreir")
    for name, generator in coreir_namespace.generators.items():
        assert isinstance(name, str)
        assert isinstance(generator, coreir.Generator)
        print(name, generator)

    ice40_library = context.load_library("ice40")
    for name, module in ice40_library.modules.items():
        assert isinstance(name, str), name
        assert isinstance(module, coreir.Module), module
        print(name, module)

