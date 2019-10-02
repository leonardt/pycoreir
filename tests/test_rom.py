import json
import coreir


def test_upsample():
    c = coreir.Context()
    ROM = c.get_namespace("memory").generators["rom"]
    ROM_6x4 = ROM(depth=6, width=4)
    for k, v in ROM_6x4.params.items():
        assert k == "init"
        assert v.kind == json
    inst = ROM_6x4
    module_typ = c.Record({"I": c.Array(4, c.BitIn()), "O": c.Array(4, c.Bit())})
    module = c.global_namespace.new_module("top", module_typ)
    module_def = module.new_definition()
    config = c.new_values({
        "init": [i for i in range(6)]
    })
    inst = module_def.add_module_instance("rom", ROM_6x4, config)
    for key, value in inst.config.items():
        assert key == "init"
        assert value.value == [i for i in range(6)]
    module.definition = module_def
    module.save_to_file("tests/rom_test.json")
    with open("tests/rom_test.json") as actual:
        with open("tests/rom_test_gold.json") as gold:
            assert actual.read() == gold.read()
