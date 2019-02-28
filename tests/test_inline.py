import coreir

def test_inline():
    c = coreir.Context()
    g = c.global_namespace
    _not = c.get_namespace("coreir").generators["not"](width=16)
    
    #Create a double not module
    double_knot = g.new_module("dnot",_not.type)
    dn_def = double_knot.new_definition()
    io = dn_def.interface
    first = dn_def.add_module_instance("first",_not)
    second = dn_def.add_module_instance("second",_not)
    dn_def.connect(io.select("in"),first.select("in"))
    dn_def.connect(first.select("out"),second.select("in"))
    dn_def.connect(second.select("out"),io.select("out"))
    double_knot.definition = dn_def

    #Create top
    top = g.new_module("top",_not.type)
    top_def = top.new_definition()
    io = top_def.interface
    out = io.select("in")
    for i in range(5):
        inst = top_def.add_module_instance(f"i{i}",double_knot)
        top_def.connect(inst.select("in"),out)
        out = inst.select("out")
    
    def num_instances():
        return len(top_def.instances)

    assert num_instances() == 5
    for i in range(5):
        inst = top_def.instances[0]
        coreir.inline_instance(inst)
        assert num_instances() == 6+i
