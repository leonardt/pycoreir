#!/usr/bin/env bash

echo [distutils]                                  > ~/.pypirc
echo index-servers =                             >> ~/.pypirc
echo "  pypi"                                    >> ~/.pypirc
echo                                             >> ~/.pypirc
echo [pypi]                                      >> ~/.pypirc
echo repository=https://upload.pypi.org/legacy/  >> ~/.pypirc
echo username=keyi                               >> ~/.pypirc
echo password=$PYPI_PASSWORD                     >> ~/.pypirc

python setup.py sdist bdist_wheel
twine upload dist/*
