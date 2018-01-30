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
    add16 = coreir_add(width=16)
    assert add16.name == "add"
    assert add16.generated == True
    assert isinstance(add16.type, coreir.Record)
    add16.type.print_()
    for arg in ['in0', 'in1', 'out']:
        assert add16.type[arg].kind == "Array"
        assert len(add16.type[arg]) == 16
