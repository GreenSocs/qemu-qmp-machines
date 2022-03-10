#!/bin/bash

if test $# -lt 1
then
    cat >&2 <<EOF
usage: $0 config [qmp-shell-args...]

The socket is fetch using the QMP_SOCKET env variable.
If QEMUPID is defined it is considered the PID of qemu process.
In that case we wait for the socket file to exists. And use the
PID to ensure qemu is still alive and do not wait for nothing
EOF
    exit 1
fi

if test -z "$QMP_SOCKET"
then
    echo "QMP_SOCKET is not defined" >&2
    exit 1
fi

config=$1
shift

# wait for QEMU to create the socket
if test -n "$QEMUPID"
then
    while kill -0 "$QEMUPID"
    do
        if test -e "$QMP_SOCKET"
        then
            break
        fi
        sleep 1
    done
fi

#send the qmp commands (remove comments first)
grep -v '^#' $config | qmp-shell "$QMP_SOCKET" "$@"
