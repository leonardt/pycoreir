#!/bin/bash

set -e

if [ "$TRAVIS_BRANCH" == "dev" ]; then
    cd deps;
    git clone -b dev https://github.com/rdaly525/coreir.git;
    cd coreir;
    export COREIRCONFIG="g++-4.9";
    export COREIR=$PWD;
    make install prefix=$TRAVIS_BUILD_DIR/deps;
    cd ..;
    cd ..;
elif [ "$TRAVIS_BRANCH" == "test_release" ]; then
    # based on https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8
    wget https://github.com/rdaly525/coreir/releases/download/v0.1.0/coreir.tar.gz;
    mkdir coreir_release;
    tar -xf coreir.tar.gz -C coreir_release --strip-components 1;
    cd coreir_release;
    make DESTDIR=$TRAVIS_BUILD_DIR/deps install
    cd ..
    pip install coreir;
fielse
    # based on https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8
else
    curl -s -L https://github.com/rdaly525/coreir/releases/latest | grep "href.*coreir.tar.gz" | cut -d \" -f 2 | xargs -I {} wget https://github.com"{}"
    mkdir coreir_release;
    tar -xf coreir.tar.gz -C coreir_release --strip-components 1;
    cd coreir_release;
    make install prefix=$TRAVIS_BUILD_DIR/deps;
    cd ..
    pip install coreir;
fi
