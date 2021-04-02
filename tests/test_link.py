import coreir
import filecmp

def test_save_header():
    header_file = "build/link_header.json"
    gold_file = "gold/link_header.json"
    c = coreir.Context()
    c.load_from_file("add2.json")
    m = c.global_namespace.modules["Add2"]
    c.serialize_header(header_file, [m])
    filecmp.cmp(header_file, gold_file)


def test_load_header():
    src_file = "gold/link_header.json"
    c = coreir.Context()
    modules = c.load_header(src_file)
    assert len(modules) == 1
    add2: coreir.Module = modules[0]
    assert add2.ref_name == "global.Add2"
    add2.print_()
