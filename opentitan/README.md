
# Opentitan machine

## Quick test

Corresponds to the qemu `opentitan` machine.

Run one of the following command to start qemu
with the `opentitan` vanilla C machine or with the `none`
machine configured using qmp commands.

```
./run-vanilla.sh lfs/echo.elf
./run-qmp.sh     lfs/echo.elf
```

The echo.elf firmware just print back whatever
characters it receives on the uart. It uses interrupts
to receive characters.

There is also an `hello.elf` firmware.

## Building the firmware

The fw submodule contains the firmware sources.

```
make fw
```

Firmwares will be built inside fw/ subdirectory.
