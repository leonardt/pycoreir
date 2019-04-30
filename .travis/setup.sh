#!/usr/bin/env bash

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
     wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
     chmod +x miniconda.sh
     ./miniconda.sh -b -p $TRAVIS_BUILD_DIR/miniconda
     export PATH=$TRAVIS_BUILD_DIR/miniconda/bin:$PATH
     hash -r
     conda config --set always_yes yes --set changeps1 no
     conda update -q conda 
     conda create -q -n test-env python=3.7
     source activate test-env
     conda install pip

else
     export PYTHON=3.7.0
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
