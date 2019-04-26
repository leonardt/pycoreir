import coreir
import json


def test_module_metadata():
    c = coreir.Context()
    add16 = c.get_namespace("coreir").generators["add"](width=16)

    dummy_data = dict(
        a = [1,5.0,"a",False],
        b = dict(c=5,d=3)
    )
    add16.add_metadata("foo",json.dumps(dummy_data))
    check = add16.metadata
    assert check == dict(foo=dummy_data)

test_module_metadata()
