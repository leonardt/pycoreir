#!/usr/bin/env bash
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    docker exec manylinux pip install magma-lang  # For libcoreir-python test
    docker exec manylinux pytest -s /pycoreir/tests/
else
    # osx
    pip install magma-lang
    pytest -s /pycoreir/tests/
fi
