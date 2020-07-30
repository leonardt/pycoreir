#!/usr/bin/env bash

echo [distutils]                                  > ~/.pypirc
echo index-servers =                             >> ~/.pypirc
echo "  pypi"                                    >> ~/.pypirc
echo                                             >> ~/.pypirc
echo [pypi]                                      >> ~/.pypirc
echo repository=https://upload.pypi.org/legacy/  >> ~/.pypirc
echo username=leonardt                           >> ~/.pypirc
echo password=$PYPI_PASSWORD                     >> ~/.pypirc

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    docker cp ~/.pypirc manylinux:/home/
    docker exec -i manylinux bash -c 'pip install twine'
    docker exec -i manylinux bash -c 'cd  /pycoreir && twine upload --config-file /home/.pypirc wheelhouse/*'

    # Upload source distribution too
    docker exec -i manylinux bash -c 'cd  /pycoreir && python setup.py sdist'
    docker exec -i manylinux bash -c 'cd  /pycoreir && twine upload --config-file /home/.pypirc dist/*.tar.gz'
else
    # osx
    pip install twine
    twine upload wheelhouse/*
fi
