echo [distutils]                                  > ~/.pypirc
echo index-servers =                             >> ~/.pypirc
echo "  pypi"                                    >> ~/.pypirc
echo                                             >> ~/.pypirc
echo [pypi]                                      >> ~/.pypirc
echo repository=https://upload.pypi.org/legacy/  >> ~/.pypirc
echo username=leonardt                           >> ~/.pypirc
echo password=$PYPI_PASSWORD                     >> ~/.pypirc
docker cp ~/.pypirc manylinux:/home/
docker exec -i manylinux bash -c 'cd  /pycoreir && twine upload --config-file /home/.pypirc wheelhouse/*'
