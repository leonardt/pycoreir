import coreir


def test_eq():
    c = coreir.Context()
    assert c.get_namespace("coreir") == c.get_namespace("coreir")


def test_hash():
    c = coreir.Context()
    dict0 = {}
    ns1 = c.get_namespace("coreir")
    dict0[ns1] = ns1
    assert dict0[c.get_namespace("coreir")] == ns1
