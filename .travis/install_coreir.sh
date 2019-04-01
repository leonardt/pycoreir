#!/bin/bash

set -e

if [ "$TRAVIS_BRANCH" == "dev" ]; then
    cd deps;
    git clone -b dev https://github.com/rdaly525/coreir.git;
    cd coreir;
    export CXX="g++-4.9";
    cd build
    cmake ..
    make install prefix=$TRAVIS_BUILD_DIR/deps;
    cd ..;  # build
    cd ..;  # coreir
    cd ..;  # deps
else
    # based on https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8
    curl -s -L https://github.com/rdaly525/coreir/releases/latest | grep "href.*coreir.tar.gz" | cut -d \" -f 2 | xargs -I {} wget https://github.com"{}"
    mkdir coreir_release;
    tar -xf coreir.tar.gz -C coreir_release --strip-components 1;
    cd coreir_release;
    make install prefix=$TRAVIS_BUILD_DIR/deps;
    cd ..
    pip install coreir;
fi
