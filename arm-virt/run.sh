#!/bin/bash

print_usage() {
    echo "usage: $0 [qmp|vanilla] num-cpus [qemu args....]"
}

if test $# -lt 2
then
    print_usage >&2
    exit 1
fi

mode=$1
smp=$2
shift 2

FWDIR=${FWDIR:-lfs}

QMP_SOCKET=/tmp/qmp-socket
commands=machine-smp$smp.qmp

image=$FWDIR/images/Image
bootloader=$FWDIR/bootloader/bootloader.bin
rootfs=$FWDIR/images/rootfs.ext4
dtb=virt-smp$smp.dtb

case $mode in
    vanilla)
        qemu-system-aarch64 -display none \
            -M virt,dtb-kaslr-seed=off -m 128M \
            -accel tcg \
            -cpu cortex-a53 -smp $smp \
            -serial mon:stdio \
            -kernel $image -append "rootwait root=/dev/vda console=ttyAMA0" \
            -drive file=$rootfs,if=none,format=raw,id=hd0 \
            -device virtio-blk-device,drive=hd0 \
            -netdev user,id=eth0 \
            -device virtio-net-device,netdev=eth0 \
            "$@"
        ;;

    qmp)
        if test ! -e "$commands"
        then
             echo "'$commands' does not exists">&2
             exit 1
        fi
        #run the config process in background, we give it our PID ($$)
        #so that it stops if qemu crashes early
        rm -f $QMP_SOCKET
        QMP_SOCKET=$QMP_SOCKET QEMUPID=$$ qmp-config.sh <(
            cat $commands - <<EOF
device_add driver=loader force-raw=True addr=0x40200000 file=$(realpath $image)
device_add driver=loader force-raw=True addr=0x44000000 file=$(realpath $dtb)
device_add driver=loader force-raw=True addr=0x40000000 file=$(realpath $bootloader) cpu-num=0
device_add driver=virtio-blk-device drive=hd0
device_add driver=virtio-net-device netdev=eth0
x-exit-preconfig
EOF
            ) -v &

        qemu-system-aarch64 -preconfig -display none \
            -qmp unix:$QMP_SOCKET,server \
            -M none -m 128M -smp 4 \
            -accel tcg \
            -serial mon:stdio \
            -drive file=$rootfs,if=none,format=raw,id=hd0 \
            -netdev user,id=eth0 \
            "$@"
        ;;
    *)
        print_usage >&2
        exit 1
esac
