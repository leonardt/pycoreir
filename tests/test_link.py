import coreir

def test_save_header():
    c = coreir.Context()
    c.load_from_file("add2.json")
    m = c.global_namespace.modules["Add2"]
    c.serialize_header("build/link_header.json", [m])

