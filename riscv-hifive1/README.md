
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

