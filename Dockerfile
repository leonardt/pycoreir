FROM quay.io/pypa/manylinux1_x86_64

LABEL description="A docker image using GCC-4.9"
LABEL maintainer="keyi@cs.stanford.edu"

ARG GCC_VERSION=4.9.0
ARG GCC_PATH=/usr/local/gcc-$GCC_VERSION
ARG PYTHON_BIN=/opt/python/cp37-cp37m/bin/

ARG MPFR=mpfr-2.4.2
ARG GMP=gmp-4.3.2
ARG MPC=mpc-0.8.1
ARG ISL=isl-0.14

RUN yum -y update && yum -y install \
    curl \
    bison \
    flex \
    && yum clean all

RUN cd /tmp \
    && curl -L -o gcc.tar.gz "http://ftp.gnu.org/gnu/gcc/gcc-${GCC_VERSION}/gcc-${GCC_VERSION}.tar.gz" \
    && tar xf gcc.tar.gz

RUN cd /tmp/gcc-$GCC_VERSION \
    && curl -LO ftp://gcc.gnu.org/pub/gcc/infrastructure/$MPFR.tar.bz2 || exit 1 \
    && tar xjf $MPFR.tar.bz2 || exit 1 \
    && ln -sf $MPFR mpfr || exit 1

RUN cd /tmp/gcc-$GCC_VERSION \
    && curl -LO ftp://gcc.gnu.org/pub/gcc/infrastructure/$GMP.tar.bz2 || exit 1 \
    && tar xjf $GMP.tar.bz2  || exit 1 \
    && ln -sf $GMP gmp || exit 1

RUN cd /tmp/gcc-$GCC_VERSION \
    && curl -LO ftp://gcc.gnu.org/pub/gcc/infrastructure/$MPC.tar.gz || exit 1 \
    && tar xzf $MPC.tar.gz || exit 1 \
    && ln -sf $MPC mpc || exit 1

RUN cd /tmp/gcc-$GCC_VERSION \
    && curl -LO ftp://gcc.gnu.org/pub/gcc/infrastructure/$ISL.tar.bz2 || exit 1 \
    && tar xjf $ISL.tar.bz2  || exit 1 \
    && ln -sf $ISL isl || exit 1

RUN cd /tmp/gcc-$GCC_VERSION \
    && mkdir build \
    && cd build \
    && ../configure -v \
        --build=x86_64-linux-gnu \
        --host=x86_64-linux-gnu \
        --target=x86_64-linux-gnu \
        --prefix=/usr/local/gcc-$GCC_VERSION \
        --enable-checking=release \
        --enable-languages=c,c++,fortran \
        --disable-multilib \
        --program-suffix=-$GCC_VERSION \
    && make -j8 \
    && make install-strip \
    && rm -rf /tmp/*

ENV CC=/usr/local/gcc-${GCC_VERSION}/bin/gcc-${GCC_VERSION}
ENV CXX=/usr/local/gcc-${GCC_VERSION}/bin/g++-${GCC_VERSION}
ENV PATH="${PYTHON_BIN}:${PATH}"

RUN pip install cmake twine auditwheel
