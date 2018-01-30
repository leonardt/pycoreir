import coreir
from coreir.type import ValueType

context = coreir.Context()

def get_lib(lib):
    if lib in {"coreir", "mantle", "corebit"}:
        return context.get_namespace(lib)
    elif lib == "global":
        return context.global_namespace
    else:
        return context.load_library(lib)

def import_(lib, name):
    return get_lib(lib).generators[name]

def test_add():
    coreir_add = import_("coreir", "add")
    assert isinstance(coreir_add, coreir.Generator)
    assert coreir_add.name == "add"
    assert 'width' in coreir_add.params
    assert isinstance(coreir_add.params['width'], ValueType)
    assert coreir_add.params['width'].kind == int
