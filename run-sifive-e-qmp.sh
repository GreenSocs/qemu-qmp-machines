#!/bin/bash

if test $# -lt 1
then
    echo "usage: $0 elf_file [qemu_args...]" >&2
    exit 1
fi

if test ! -e "$1"
then
    echo "'$1' does not exists">&2
    exit 1
fi

if test ! -e sifive-e.qmp
then
    echo "'sifive-e.qmp' does not exists">&2
    exit 1
fi

elf=$1
shift

QMP_SOCKET=/tmp/qmp-socket

gen_config() {
    cat sifive-e.qmp - <<EOF
device_add driver=loader file=$(realpath $elf) cpu-num=0
x-exit-preconfig
EOF
}

#run the config process in background, we give it our PID ($$)
#so that it stops if qemu crashes early
rm -f $QMP_SOCKET
QMP_SOCKET=$QMP_SOCKET QEMUPID=$$ ./qmp-config.sh <(gen_config) -v &

qemu-system-riscv32 -preconfig -display none \
    -qmp unix:$QMP_SOCKET,server \
    -M none -m size=64K \
    -serial mon:stdio -serial null \
    "$@"
