import coreir


def test_array_len():
    context = coreir.Context()
    array_type = context.Array(8, context.BitIn())
    assert len(array_type) == 8
    bit_type = context.BitIn()
    try:
        len(bit_type)
        assert False, \
            "Calling len on a non array type should throw an exception"
    except Exception as e:
        assert str(e) == "`len` called on a BitIn"


def test_type_size():
    context = coreir.Context()
    array1_type = context.Array(7, context.BitIn())
    assert array1_type.size == 7
    array2_type = context.Array(10, array1_type)
    assert array2_type.size == 7*10
    assert array1_type.is_input()
    assert not array1_type.is_output()


def test_type_isoutput():
    context = coreir.Context()
    array1_type = context.Array(7, context.Bit())
    assert array1_type.is_output()
    assert not array1_type.is_input()
