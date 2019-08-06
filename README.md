[![Build Status](https://travis-ci.org/leonardt/pycoreir.svg?branch=master)](https://travis-ci.org/leonardt/pycoreir)

Ultralight Python bindings for [coreir](https://github.com/rdaly525/coreir) using ctypes.

```
pip install coreir
```

[CHANGELOG](./CHANGELOG.md)

# Development Setup
Install a local working copy to your python packages using
```
pip install -e .
```
**NOTE:** When working with an editable link, as of 7/31/19, `pip uninstall
coreir` will not correctly remove the installed script (see
https://github.com/pypa/pip/issues/5997), a workaround is to remove the scrip
manually when uninstalling, (e.g. `rm ~/miniconda3/bin/coreir`)

To run the tests
```
pip install pytest
pytest
```
