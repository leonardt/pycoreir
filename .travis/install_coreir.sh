#!/bin/bash

set -e

if [ "$TRAVIS_BRANCH" != "master" ]; then
    cd deps;
    git clone -b dev https://github.com/rdaly525/coreir.git;
    cd coreir;
    export COREIRCONFIG="g++-4.9";
    export COREIR=$PWD;
    make install prefix=$TRAVIS_BUILD_DIR/deps;
    cd ..;
    cd ..;
else
    wget https://github.com/rdaly525/coreir/releases/download/v0.0.10/coreir.tar.gz;
    mkdir coreir_release;
    tar -xf coreir.tar.gz -C coreir_release --strip-components 1;
    cd coreir_release;
    make install prefix=$TRAVIS_BUILD_DIR/deps;
    cd ..
    pip install coreir;
fi
