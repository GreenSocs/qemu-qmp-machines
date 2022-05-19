# QEMU Patches status

The general goal is to start from an empty QEMU configuration and add every using
QAPI commands. In practice we target to use the _none_ machine a base and rely
as little as possible on CLI options. We try to indtroduce QAPI commands required
to populate the machine with various devices.

## QAPI device cold-plug

[Latest patch series](https://lore.kernel.org/qemu-devel/20220223090706.4888-1-damien.hedde@greensocs.com/)

As of now `-device` CLI option is the only way the cold plug a device.
We need to extend `device_add` QAPI command.

There are 2 issues:
+ The monitor does not stop at the right time for us to cold plug devices
+ `-device` has specific `fw_cfg` handling.

## Sysbus device generic plug

[Latest patch series](https://lore.kernel.org/qemu-devel/20220223090706.4888-1-damien.hedde@greensocs.com/)

Sysbus device are, unless all other devices, mostly not user-creatable.
Memory and interrupt mapping is custom.

There are a few exceptions using a per-machine mechanism. A machine defines a
list of sysbus devices it can handle and provides a handler to cope with the
mappings.

Several solutions:
1. (in the latest series) Use the current mechanism: allow any sysbus devices
   in the `none` machine but obviously without any handling mechanism (any
   mapping operation must be done by QAPI commands).
2. Differentiate legacy sysbus devices using the old system and new ones
   not requiring this.

A possible issue is that unlocking sysbus device use in `-device` on any
random machine. On the CLI, the user might not be able to map interrupts
and or mmio region. And the device will not really be usable.

## Sysbus mapping

[Latest patch series](https://lore.kernel.org/qemu-devel/20220223090706.4888-1-damien.hedde@greensocs.com/)

1. Using a new `sysbus-mmio-map` QAPI command doing roughly what
   `sysbus_mmio_map()` does (in the latest series).
2. Using additional argument(s) to `device_add` to specify the mapping.

It is not sure that using the second option would be sufficient to handle all
cases.

## Interrupts mapping

Mapping of interrupts is possible using `qom_set`.

## CPUs

[Latest patch series](https://lore.kernel.org/qemu-devel/20220223090706.4888-1-damien.hedde@greensocs.com/)

## Memories / RAM

We proposed a sysbus-device memory.
TODO: rely on backend.

## Kernel loading

For now we rely on manual binary loading.

Complex kernel-aware loading is supported by machine specific code. This need to be moved
on some device (cpus cluster ?) to be available on dynamic machine...

