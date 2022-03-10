# QMP Machines

This repo contains machines in order to test dynamic
creation of machine in QEMU.

There are several submodules (qemu and firmware related
repositories). Setting them up is not mandatory for testing.

## Setup

### Requirements

- python with pyyaml module

### QEMU setup

You'll need a qemu with the qapi features to dynamicaly create the
machines.

For example, you can do:
```
git submodule update --init --depth 1 qemu
cd qemu
./configure --target-list=riscv32-softmmu
make -C build -j
```

### environment

You need to put `./scripts` into your PATH and setup qemu environment too
with the following:

```
export PATH=/path/to/qemu/build:/path/to/qemu/scripts/qmp:$PATH
```

The `env.sourceme` contains this plus the qemu setup described above.
```
source ./env.sourceme
```

## Firmwares

You'll need adequate toolchains if you want to re-compile
the firmwares. Pre-built copies are provided (using git-lfs).

## test "release"

In order to give upstream access to our tests.
The 'release' target of the Makefile will fill a directory `qmp-machines`.
this directory contains 3 things:
+ qmp commands file (to create machines)
+ firmware (binaries to run on the machines)
+ scripts to provide working qemu command lines

```
make rm-release release
```

This directory is also a submodule linked to our github. So this is public
and available to demonstrate our work to the qemu mailing list.
