import coreir
from coreir.module import NotAGeneratorException
def test_module():
    c = coreir.Context()
    module_typ = c.Record({"input": c.Array(8, c.BitIn()), "output": c.Array(9, c.Bit())})
    module = c.global_namespace.new_module("multiply_by_2", module_typ)
    assert module.generated == False
    try:
        generator_args = module.generator_args
        assert False, "Should throw an exception for a non generator module"
    except NotAGeneratorException:
        pass
