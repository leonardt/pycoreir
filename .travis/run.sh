#!/usr/bin/env bash
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    docker exec garnet-flow pip install magma-lang  # For libcoreir-python test
    docker exec garnet-flow bash -c "cd /pycoreir && pytest -s tests/"
else
    # osx
    pip install magma-lang
    pytest -s tests/
fi
