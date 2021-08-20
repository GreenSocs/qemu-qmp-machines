
# Testing the qmp creation machine

This directory contains several examples to demonstrate how to
use and test the creation of machine using qmp commands. You need
a qemu supporting this feature. Our working branch is located here:
https://github.com/GreenSocs/qemu/tree/qmp-machine

This directory mostly contains:
+ qmp commands file (with a .qmp extension)
+ firmware for qemu machines (for example .elf files)
+ qemu starter scripts (`run-*-qmp.sh` or `run-*-vanilla.sh`)

qmp-config.sh is a utility script we use to load the '.qmp' command
files in order to test in a single terminal. It only discards
the comment and watches if qemu crashes.

But in order to start qemu the 2 followings commands can be typed
in 2 diffrent terminals:

```
qemu-system-ARCH -preconfig -qmp unix:/tmp/qmp-socket,server ....
grep -v '^#' some-file.qmp | qmp-shell -v /tmp/qmp-socket
```
Note that some additional arguments must be given to qemu.
Generally we gives `-machine none -cpu some-cpu-type` to start
from an empty machine with a given cpu.
Please look at the content of `run-*-qmp.sh` scripts, they
almost only consists in a qemu starting command line.

## opentitan

This corresponds to the qemu `opentitan` machine.

Run one of the following command to start qemu
with the `opentitan` vanilla C machine or with the `none`
machine configured using qmp commands.

```
./run-opentitan-vanilla.sh opentitan-echo.elf
./run-opentitan-qmp.sh     opentitan-echo.elf
```

These two scripts expect that qemu-system-riscv32 is in the PATH.

The opentitan-echo.elf firmware just print back whatever
characters it receives on the uart. It uses interrupts
to receive characters.

The firmware sources can be found there:
https://github.com/GreenSocs/qemu-opentitan-firmware.git

## sifive-e

This correspond to the qemu `sifive_e` machine (implementing the
sifive's hifive1 board).

Run one of the following command to start qemu
with the `sifive_e` vanilla C machine or with the `none`
machine configured using qmp commands.

```
./run-sifive-e-vanilla.sh sifive-e-hello.elf
./run-sifive-e-qmp.sh     sifive-e-hello.elf
```

These two scripts expect that qemu-system-riscv32 is in the PATH.

The sifive-e-hello.elf firmware is just an hello world. It comes
from sifive freedom-e-sdk.
https://github.com/sifive/freedom-e-sdk.git

In that SDK the firmware can be compiled using:
```
make PROGRAM=hello TARGET=sifive-hifive1 software
```

