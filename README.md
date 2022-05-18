# Dynamic QAPI machine creation in QEMU

This repository contains the work-in-progress state of the work done
to create machine dynamically in QEMU.

The general goal is to start from an empty QEMU configuration and add every using
QAPI commands. In practice we target to use the _none_ machine a base and rely
as little as possible on CLI options. We try to indtroduce QAPI commands required
to populate the machine with various devices.

QEMU current state is in this [fork](https://github.com/GreenSocs/qemu/tree/qmp-machine).
See [PATCHES.md](PATCHES.md) for information about current development state.

## Testing setup

This repository contains several submodules (qemu and firmware related
repositories). Setting them up is not mandatory for testing.

### Requirements

- make
- dtc
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

You need to put local direcoties into your PATHs:
```
export PATH=$PWD/scripts:$PATH
export PYTHONPATH=$PWD/scripts/python:$PYTHONPATH
```

Also setup qemu environment too with the following:
```
export PATH=/path/to/qemu/build:/path/to/qemu/scripts/qmp:$PATH
```

The `env.sourceme` contains these operations.
```
source ./env.sourceme
```

## Firmwares

You'll need adequate toolchains if you want to re-compile the firmwares.
the firmwares. Pre-built copies are provided (using git-lfs).

