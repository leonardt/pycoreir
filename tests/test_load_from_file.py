import coreir


def test_load_from_file1():
    context = coreir.Context()
    mod = context.load_from_file("DesignTop.json")
