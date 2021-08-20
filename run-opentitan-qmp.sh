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
QEMUPID=$$ ./qmp-config.sh $QMPSOCKET opentitan.qmp -v &

qemu-system-riscv32 -preconfig -qmp unix:$QMPSOCKET,server \
    -display none \
    -M none -cpu lowrisc-ibex \
    -device loader,addr=0x8090,cpu-num=0 \
    -device loader,file=$elf \
    -serial mon:stdio \
    "$@"
