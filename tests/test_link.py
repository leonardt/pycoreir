import coreir
import filecmp

def test_serialize_file():
    src_file = "tests/srcs/add2.json"
    build_file = "tests/build/add2.json"
    c = coreir.Context()
    c.load_from_file(src_file)
    c.serialize_to_file(build_file)
    del c
    c = coreir.Context()
    #Test loading serialized file
    c.load_from_file(build_file)


def test_serialize_header():
    header_file = "tests/build/link_header.json"
    gold_file = "tests/gold/link_header.json"
    src_file = "tests/srcs/add2.json"
    c = coreir.Context()
    c.load_from_file(src_file)
    m = c.global_namespace.modules["Add2"]
    c.serialize_header(header_file, [m])
    filecmp.cmp(header_file, gold_file)

def test_serialize_definitions():
    def_file = "tests/build/link_defs.json"
    gold_file = "tests/gold/link_defs.json"
    src_file = "tests/srcs/add2.json"
    c = coreir.Context()
    c.load_from_file(src_file)
    m = c.global_namespace.modules["Add2"]
    c.serialize_definitions(def_file, [m])
    filecmp.cmp(def_file, gold_file)

def test_load_and_link():
    header_file = "tests/gold/link_header.json"
    def_file = "tests/gold/link_defs.json"
    c = coreir.Context()
    modules = c.load_header(header_file)
    assert len(modules) == 1
    add2 = modules[0]
    assert add2.ref_name == "global.Add2"
    assert add2.definition is None
    add2.print_()

    c.link_definitions(def_file)
    add2.print_()
    assert add2.definition is not None


