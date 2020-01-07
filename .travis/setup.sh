#!/usr/bin/env bash

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    docker pull keyiz/manylinux
    docker pull keyiz/garnet-flow
    docker run -d --name manylinux --rm -it --mount type=bind,source="$(pwd)"/../pycoreir,target=/pycoreir keyiz/manylinux bash
    docker run -d --name garnet-flow --rm -it --mount type=bind,source="$(pwd)"/../pycoreir,target=/pycoreir keyiz/garnet-flow bash
    docker cp ../pycoreir manylinux:/
    docker exec manylinux bash -c "cd pycoreir && python setup.py bdist_wheel"
    docker exec manylinux bash -c "pip install auditwheel"
    docker exec manylinux bash -c "auditwheel show /pycoreir/dist/*.whl"
    # we should have any external linked libraries at this point
    docker exec manylinux bash -c "cd pycoreir && LD_LIBRARY_PATH=/pycoreir/coreir-cpp/build/lib:/opt/rh/devtoolset-2/root/usr/lib64:/opt/rh/devtoolset-2/root/usr/lib:/usr/local/lib64:/usr/local/lib auditwheel repair dist/*.whl"
    # install the wheel for testing
    # use garnetflow container to test since it has all the prereqs
    docker exec garnet-flow bash -c "cd pycoreir && pip install wheelhouse/*.whl"
    docker exec garnet-flow pip install pytest
else
     python --version
     python -m pip install cmake twine wheel pytest delocate
     python setup.py bdist_wheel
     delocate-listdeps dist/*.whl
     delocate-wheel -v dist/*.whl
     pip install dist/*.whl
fi
