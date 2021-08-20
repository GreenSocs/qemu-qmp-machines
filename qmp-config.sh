#!/bin/bash

if test $# -lt 2
then
    echo "usage: $0 socket config-file [qmp-shell-additional-args...]" >&2
    echo >&2
    echo "If QEMUPID is defined it is considered the PID of qemu process." &>2
    echo "In that case we wait for the socket file to exists. And use the" &>2
    echo "PID to ensure qemu is still alive and do not wait for nothing" &>2
    exit 1
fi

socket=$1
config=$2
shift 2

# wait for QEMU to create the socket
if test -n "$QEMUPID"
then
    while kill -0 "$QEMUPID"
    do
        if test -e "$socket"
        then
            break
        fi
        sleep 1
    done
fi

#send the qmp commands (remove comments first)
grep -v -e '^#' "$config" | qmp-shell "$socket" "$@"
