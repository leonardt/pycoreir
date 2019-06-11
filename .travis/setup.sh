#!/usr/bin/env bash

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    docker pull keyiz/garnet-flow
    docker run -d --name garnet-flow --rm -i -t keyiz/garnet-flow bash
    docker exec garnet-flow git clone https://github.com/leonardt/pycoreir
    docker exec garnet-flow bash -c "cd pycoreir && python setup.py bdist_wheel"
    docker exec garnet-flow bash -c "pip install auditwheel"
    docker exec garnet-flow bash -c "auditwheel show /pycoreir/dist/*.whl"
    # we should have any external linked libraries at this point
    docker exec garnet-flow bash -c "cd pycoreir && auditwheel repair dist/*.whl"
    # install the wheel for testing
    docker exec garnet-flow bash -c "cd pycoreir && pip install wheelhouse/*.whl"
    docker exec garnet-flow pip install pytest
else
     export PYTHON=3.7.0
     brew install gmp mpfr libmpc
     brew install pyenv-virtualenv
     pyenv install ${PYTHON}
     export PYENV_VERSION=$PYTHON
     export PATH="/Users/travis/.pyenv/shims:${PATH}"
     pyenv virtualenv venv
     source /Users/travis/.pyenv/versions/${PYTHON}/envs/venv/bin/activate
     python --version

     python -m pip install cmake twine wheel pytest
     python setup.py bdist_wheel
     pip install dist/*.whl
fi
