import coreir
from test_utils import get_pointer_addr, assert_pointers_equal

#TODO, do this with cgralib instead
#def test_load_library():
#    c = coreir.Context()
#    stdlib = c.load_library("stdlib")
#    assert stdlib.name == "stdlib"

def test_save_module():
    c = coreir.Context()
    module_typ = c.Record({"input": c.Array(8, c.BitIn()), "output": c.Array(9, c.Bit())})
    module = c.global_namespace.new_module("multiply_by_2", module_typ)
    module.print_()
    assert module.definition is None, "Should not have a definition"
    module_def = module.new_definition()
    configparams = c.newParams({"init":c.Int(), "test_param0": c.Int(), "test_param1": c.Int()})
    add8 = c.global_namespace.new_module("add8",
        c.Record({
            "in1": c.Array(8, c.BitIn()),
            "in2": c.Array(8, c.BitIn()),
            "out": c.Array(9, c.Bit())
        }),
        configparams
    )
    for key, value in add8.params.items():
        if key == "init":
            assert value.kind == int
        elif key == "test_param0":
            assert value.kind == int
        elif key == "test_param1":
            assert value.kind == int
        else:
            assert False, f"Found unexpected param {key}"
    for port, type_ in add8.type.items():
        assert type_.kind == "Array"
        if port in ["in1", "in2"]:
            assert len(type_) == 8
        else:
            assert len(type_) == 9
    add8_inst = module_def.add_module_instance("adder", add8,
        c.new_values({"init":5, "test_param0": 1, "test_param1": 0}))
    assert add8_inst.module.namespace.name == "global"
    assert add8_inst.module.name == "add8"
    assert add8_inst.config["init"].value == 5
    expected = {"init": 5, "test_param0": 1, "test_param1": 0}
    assert len(add8_inst.config) == len(expected)
    for key, value in add8_inst.config.items():
        assert key in expected and expected[key] == value.value
        del expected[key]
    assert not expected, "Should be empty"
    add8_in1 = add8_inst.select("in1")
    add8_in2 = add8_inst.select("in2")
    add8_out = add8_inst.select("out")
    interface = module_def.interface
    _input = interface.select("input")
    output = interface.select("output")
    try:
        interface.select("BadSelect")
        assert(False)
    except Exception:
        pass

    module_def.connect(_input, add8_in1)
    module_def.connect(_input, add8_in2)
    module_def.connect(output, add8_out)
    module.definition = module_def
    assert module.definition is not None, "Should have a definition"
    module.print_()
    module.save_to_file("_python_test_output.json")
    mod = c.load_from_file("_python_test_output.json")
    mod_def = mod.definition
    print("=====================")
    mod_def.print_()
    module_def.print_()
    print("=====================")
    c.run_passes(['printer'])


def test_module_def_instances():
    c = coreir.Context()
    module_typ = c.Record({"input": c.Array(8, c.BitIn()), "output": c.Array(9, c.Bit())})
    module = c.global_namespace.new_module("multiply_by_2", module_typ)
    module_def = module.new_definition()
    add8 = c.global_namespace.new_module("add8",
        c.Record({
            "in1": c.Array(8, c.BitIn()),
            "in2": c.Array(8, c.BitIn()),
            "out": c.Array(9, c.Bit())
        })
    )
    add8_inst_1 = module_def.add_module_instance("adder1", add8)
    add8_inst_2 = module_def.add_module_instance("adder2", add8)
    instances = module_def.instances
    pointers_actual = [get_pointer_addr(inst.ptr) for inst in instances]
    pointers_expected = [get_pointer_addr(inst.ptr) for inst in [add8_inst_1, add8_inst_2]]
    for pointer in pointers_actual:
        assert pointer in pointers_expected
        pointers_expected.remove(pointer)
    assert not len(pointers_expected), "Missing pointers {}".format(pointers_expected)

    assert_pointers_equal(instances[0].module_def.ptr, module_def.ptr)
    assert_pointers_equal(instances[0].module.ptr, add8.ptr)

def test_module_def_select():
    c = coreir.Context()
    module_typ = c.Record({"input": c.Array(8, c.BitIn()), "output": c.Array(9, c.Bit())})
    module = c.global_namespace.new_module("multiply_by_2", module_typ)
    # module.print()
    module_def = module.new_definition()
    add8 = c.global_namespace.new_module("add8",
        c.Record({
            "in1": c.Array(8, c.BitIn()),
            "in2": c.Array(8, c.BitIn()),
            "out": c.Array(9, c.Bit())
        })
    )
    interface = module_def.interface
    assert get_pointer_addr(interface.ptr) == get_pointer_addr(module_def.select("self").ptr)
    add8_inst = module_def.add_module_instance("adder", add8)
    add8_inst_select = module_def.select("adder")
    assert get_pointer_addr(add8_inst.ptr) == get_pointer_addr(add8_inst_select.ptr)

def test_wireable():
    c = coreir.Context()
    module_typ = c.Record({"input": c.Array(8, c.BitIn()), "output": c.Array(9, c.Bit())})
    module = c.global_namespace.new_module("multiply_by_2", module_typ)
    # module.print()
    module_def = module.new_definition()
    add8 = c.global_namespace.new_module("add8",
        c.Record({
            "in1": c.Array(8, c.BitIn()),
            "in2": c.Array(8, c.BitIn()),
            "out": c.Array(9, c.Bit())
        })
    )
    add8_inst = module_def.add_module_instance("adder", add8)
    add8_in1 = add8_inst.select("in1")
    add8_in2 = add8_inst.select("in2")
    add8_out = add8_inst.select("out")
    interface = module_def.interface
    _input = interface.select("input")
    output = interface.select("output")
    module_def.connect(_input, add8_in1)
    module_def.connect(_input, add8_in2)
    module_def.connect(output, add8_out)
    actual = [get_pointer_addr(wireable.ptr) for wireable in _input.connected_wireables]
    assert get_pointer_addr(add8_in1.ptr) in actual
    assert get_pointer_addr(add8_in2.ptr) in actual
    for expected, actual in zip(['adder', 'out'], add8_out.selectpath):
        assert expected == actual

    wireable = module_def.select("self")
    select = wireable.select("input")
    assert isinstance(select, coreir.Select)
    assert get_pointer_addr(select.ptr) == get_pointer_addr(_input.ptr)
    assert select.parent == wireable


def test_module_def_connections():
    c = coreir.Context()
    module_typ = c.Record({"input": c.Array(8, c.BitIn()), "output": c.Array(9, c.Bit())})
    module = c.global_namespace.new_module("multiply_by_2", module_typ)
    # module.print()
    module_def = module.new_definition()
    add8 = c.global_namespace.new_module("add8",
        c.Record({
            "in1": c.Array(8, c.BitIn()),
            "in2": c.Array(8, c.BitIn()),
            "out": c.Array(9, c.Bit())
        })
    )
    add8_inst = module_def.add_module_instance("adder", add8)
    add8_in1 = add8_inst.select("in1")
    add8_in2 = add8_inst.select("in2")
    add8_out = add8_inst.select("out")
    interface = module_def.interface
    _input = interface.select("input")
    output = interface.select("output")
    module_def.connect(_input, add8_in1)
    module_def.connect(_input, add8_in2)
    module_def.connect(output, add8_out)
    input_ptr = get_pointer_addr(_input.ptr)
    add8_in1_ptr = get_pointer_addr(add8_in1.ptr)
    add8_in2_ptr = get_pointer_addr(add8_in2.ptr)
    add8_out_ptr = get_pointer_addr(add8_out.ptr)
    output_ptr = get_pointer_addr(output.ptr)
    expected_conns = [
        (add8_in1_ptr, input_ptr, 8),
        (add8_in2_ptr, input_ptr, 8),
        (add8_out_ptr, output_ptr, 9)
    ]
    connections = module_def.connections
    seen = []
    for conn in connections:
        conn_info = (get_pointer_addr(conn.first.ptr), get_pointer_addr(conn.second.ptr), conn.size)
        reverse_conn_info = (conn_info[1], conn_info[0], conn.size)
        # Should be in expected, shouldn't see it twice
        assert (conn_info in expected_conns or reverse_conn_info in expected_conns) and \
               conn_info not in seen
        seen.append(conn_info)

    assert len(seen) == len(expected_conns)

def test_context():
    context = coreir.Context()
    _type = context.named_types[("coreir", "clkIn")]
    assert _type.kind == "Named"

def test_version():
    context = coreir.Context()
    version = context.get_version()
    revision = context.get_revision()
    assert isinstance(version, str) and len(version) > 0
    assert isinstance(revision, str) and len(revision) > 0
    print("version:", version, revision)

if __name__ == "__main__":
    test_module_def_instances()
