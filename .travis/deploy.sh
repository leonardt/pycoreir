#!/usr/bin/env bash

echo [distutils]                                  > ~/.pypirc
echo index-servers =                             >> ~/.pypirc
echo "  pypi"                                    >> ~/.pypirc
echo                                             >> ~/.pypirc
echo [pypi]                                      >> ~/.pypirc
echo repository=https://upload.pypi.org/legacy/  >> ~/.pypirc
echo username=keyi                               >> ~/.pypirc
echo password=$PYPI_PASSWORD                     >> ~/.pypirc

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    docker cp ~/.pypirc manylinux:/home/
    docker exec -i manylinux bash -c 'pip install twine'
    docker exec -i manylinux bash -c 'cd  /pycoreir && twine upload --config-file /home/.pypirc wheelhouse/*'
else
    export PYTHON=3.7.0
    export PYENV_VERSION=$PYTHON
    export PATH="/Users/travis/.pyenv/shims:${PATH}"
    source /Users/travis/.pyenv/versions/${PYTHON}/envs/venv/bin/activate
    # osx
    pip install twine
    twine upload dist/*
fi
