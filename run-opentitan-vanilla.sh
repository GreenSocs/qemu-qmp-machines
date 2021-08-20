#!/bin/bash

if test $# -lt 1
then
    echo "usage: $0 elf_file [qemu_args...]" >&2
    exit 1
fi

elf="$1"
shift

qemu-system-riscv32 -display none \
     -M opentitan \
     -serial mon:stdio \
     -kernel "$elf" \
     "$@"
