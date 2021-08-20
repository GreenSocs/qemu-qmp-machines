#!/bin/bash

if test $# -lt 1
then
    echo "usage: $0 elf_file [qemu_args...]" >&2
    exit 1
fi

elf="$1"
shift

QMPSOCKET=/tmp/qmp-socket

#run the config process in background, we give it our PID ($$)
#so that it stops if qemu crashes early
rm -f $QMPSOCKET
QEMUPID=$$ ./qmp-config.sh $QMPSOCKET sifive-e.qmp -v &

qemu-system-riscv32 -preconfig -qmp unix:$QMPSOCKET,server \
    -display none \
    -M none -cpu sifive-e31,resetvec=0x20400000 \
    -device loader,file=$elf \
    -serial mon:stdio -serial null \
    "$@"
# loading a binary file won't work on none machine (ram_size is 0)
# -M none -cpu sifive-e31,resetvec=0x1004 \
# -device loader,addr=0x1000,file=./hifive1-bootrom.bin \
