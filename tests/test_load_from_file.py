import coreir


def test_load_from_file1():
    context = coreir.Context()
    context.load_library("cgralib")
    mod = context.load_from_file("tests/DesignTop.json")
    assert mod.name == "DesignTop"
