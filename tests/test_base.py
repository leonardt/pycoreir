import coreir

def test_eq():
    c = coreir.Context()
    assert c.get_namespace("coreir") == c.get_namespace("coreir")
    assert c.get_namespace("coreir") is c.get_namespace("coreir")

def test_lib_eq():
    c = coreir.Context()
    assert c.load_library("commonlib") is c.load_library("commonlib")

def test_hash():
    c = coreir.Context()
    dict0 = {}
    ns1 = c.get_namespace("coreir")
    dict0[ns1] = ns1
    assert dict0[c.get_namespace("coreir")] == ns1

def test_metadata():
    c = coreir.Context()
    add16 = c.get_namespace("coreir").generators["add"](width=16)
    class A:
        pass
    add16._metadata_ = ["metadata",4,A,A()]

    add16_ = c.get_namespace("coreir").generators["add"](width=16)
    assert hasattr(add16_,"_metadata_")
    metadata = add16_._metadata_
    assert metadata[0] == "metadata"
    assert metadata[1] == 4
    assert metadata[2] is A
    assert isinstance(metadata[3],A)
    
