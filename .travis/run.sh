#!/usr/bin/env bash
if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    pip install magma-lang
    pytest -s tests/

else
    # osx
    pip install magma-lang
    pytest -s tests/
fi
