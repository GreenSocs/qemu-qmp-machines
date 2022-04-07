#!/usr/bin/env python3

import argparse
import sys
import qmpgen
from qmpgen import qom_set, device_add, sysbus_mmio_map, exit_preconfig

parser = argparse.ArgumentParser(
        description="QMP generator for arm virt machine",
        parents=[qmpgen.parser])

parser.add_argument('ncpus', type=int, help='number of cpus')

args = parser.parse_args()

qmpgen.conf_from_parser(args)

ncpus = args.ncpus

# RAM (need to do that before machine-init -> before any - device_add)
#Note: ram size must be set on CLI eg -m size: 128M
qom_set('/machine', 'ram-addr', 0x40000000)

# FLASH0
devid = device_add('cfi.pflash01', 'flash0', **{
    'sector-length': 0x40000, # 256KiB
    'num-blocks': 0x100, # size is 0x04000000
    'width': 4,
    'device-width': 2,
    'big-endian': False,
    'id0': 0x89,
    'id1': 0x18,
    'id2': 0x00,
    'id3': 0x00,
    'name': 'virt.flash0',
    })
sysbus_mmio_map(devid, 0x00000000)
# TODO: machine's pflash0 alias to flash0/drive ?

# FLASH1
devid = device_add('cfi.pflash01', 'flash1', **{
    'sector-length': 0x40000, # 256KiB
    'num-blocks': 0x100, # size is 0x04000000
    'width': 4,
    'device-width': 2,
    'big-endian': False,
    'id0': 0x89,
    'id1': 0x18,
    'id2': 0x00,
    'id3': 0x00,
    'name': 'virt.flash1',
    })
sysbus_mmio_map(devid, 0x04000000)
#TODO: machine's pflash1 alias to flash1/drive ?

# CPUS
device_add('arm-cpus', 'cpus', **{
    'cpu-type': 'cortex-a53-arm-cpu',
    'num-cpus': ncpus,
    'has_el3': False,
    'has_el2': False,
    'reset-cbar': 0x08000000,
    'start-powered-off': True,
    'psci-conduit': 2,
    })
#memory: memory region
#secure-memory: memory region
#only cpu[0] will start on
qom_set('cpus/cpu[0]', 'start-powered-off', False)

# GIC v2
devid = device_add('arm_gic', 'gic', **{
    'revision': 2,
    'num-cpu': ncpus,
    'num-irq': 288,
    'has-security-extensions': False,
    'has-virtualization-extensions': False,
    })
sysbus_mmio_map(devid, 0x08000000, mmio=0)
sysbus_mmio_map(devid, 0x08010000, mmio=1)
for cpuidx in range(ncpus):
    cpu = 'cpus/cpu[%d]' % cpuidx
    base = 256 + 16 + (cpuidx * 32)
    # gtimer_phys
    qom_set(cpu, 'unnamed-gpio-out[0]', 'gic/unnamed-gpio-in[%d]' % (base + 14))
    # gtimer_virt
    qom_set(cpu, 'unnamed-gpio-out[1]', 'gic/unnamed-gpio-in[%d]' % (base + 11))
    # gtimer_hyp
    qom_set(cpu, 'unnamed-gpio-out[2]', 'gic/unnamed-gpio-in[%d]' % (base + 10))
    # gtimer_sec
    qom_set(cpu, 'unnamed-gpio-out[3]', 'gic/unnamed-gpio-in[%d]' % (base + 13))
    # pmu-interrupt
    qom_set(cpu, 'pmu-interrupt[0]', 'gic/unnamed-gpio-in[%d]' % (base + 7))
    # irq
    qom_set(devid, 'sysbus-irq[%d]' % (cpuidx), cpu + '/unnamed-gpio-in[0]')
    # fiq
    qom_set(devid, 'sysbus-irq[%d]' % (ncpus + cpuidx), cpu + '/unnamed-gpio-in[1]')
    # virq
    qom_set(devid, 'sysbus-irq[%d]' % ((2*ncpus) + cpuidx), cpu + '/unnamed-gpio-in[2]')
    # vfiq
    qom_set(devid, 'sysbus-irq[%d]' % ((3*ncpus) + cpuidx), cpu + '/unnamed-gpio-in[3]')

# GIC v2m
devid = device_add('arm-gicv2m', 'gicv2m', **{
    'base-spi': 48,
    'num-spi': 64,
    })
sysbus_mmio_map(devid, 0x08020000)
for i in range(64):
    qom_set(devid, 'sysbus-irq[%d]' % i, 'gic/unnamed-gpio-in[%d]' % (48+i))
#TODO: L3208 vms->msi_controller = VIRT_MSI_CTRL_GICV2M
#hotplug won't work as in virt

# UART
devid = device_add('pl011', 'uart', **{
    'chardev': 'serial0',
    })
sysbus_mmio_map(devid, 0x09000000)
qom_set(devid, 'sysbus-irq[0]', 'gic/unnamed-gpio-in[1]')

# RTC
devid = device_add('pl031', 'rtc')
sysbus_mmio_map(devid, 0x09010000)
qom_set(devid, 'sysbus-irq[0]', 'gic/unnamed-gpio-in[2]')

# PCIE
devid = device_add('gpex-pcihost', 'pcihost', **{
    'bypass-iommu': False,
    })
#ecam
sysbus_mmio_map(devid, 0x4010000000, mmio=0, alias=True,
                size=  0x0010000000)
#mmio
sysbus_mmio_map(devid, 0x10000000, mmio=1, alias=True,
                offset=0x10000000,
                size=  0x2eff0000)
sysbus_mmio_map(devid, 0x8000000000, mmio=1, alias=True, 
                offset=0x0010000000,
                size=  0x8000000000)
#pio
sysbus_mmio_map(devid, 0x3eff0000, mmio=2)
qom_set(devid, 'sysbus-irq[0]', 'gic/unnamed-gpio-in[3]')
qom_set(devid, 'sysbus-irq[1]', 'gic/unnamed-gpio-in[4]')
qom_set(devid, 'sysbus-irq[2]', 'gic/unnamed-gpio-in[5]')
qom_set(devid, 'sysbus-irq[3]', 'gic/unnamed-gpio-in[6]')
qom_set(devid, 'irq-num[0]', '3')
qom_set(devid, 'irq-num[1]', '4')
qom_set(devid, 'irq-num[2]', '5')
qom_set(devid, 'irq-num[3]', '6')
#FIXME NIC: pci_nic_init_nofail

# GPIO
devid = device_add('pl061', 'gpio', **{
    'pullups': 0,
    'pulldowns': 0xff,
    })
sysbus_mmio_map(devid, 0x09030000)
qom_set(devid, 'sysbus-irq[0]', 'gic/unnamed-gpio-in[7]')

# GPIO KEYS
devid = device_add('gpio-key', 'key-poweroff', **{
    'register-powerdown-notifier': True,
    })
qom_set(devid, 'sysbus-irq[0]', 'gpio/unnamed-gpio-in[3]')

# 32xMMIO
for i in range(32):
    devid = device_add('virtio-mmio', 'mmio%d' % i)
    sysbus_mmio_map(devid, 0x0a000000 + (0x200 * i))
    qom_set(devid, 'sysbus-irq[0]', 'gic/unnamed-gpio-in[%d]' % (16+i))

# FW_CFG
devid = device_add('fw_cfg_mem', 'fw-cfg', **{
    'data_width': 8,
    'dma_enabled': True,
    })
sysbus_mmio_map(devid, 0x09020008, mmio=0)
sysbus_mmio_map(devid, 0x09020000, mmio=1)
sysbus_mmio_map(devid, 0x09020010, mmio=2)

# PLATFORM_BUS
devid = device_add('platform-bus-device', 'platform-bus-device', **{
    'num_irqs': 64,
    'mmio_size': 0x02000000,
    })
sysbus_mmio_map(devid, 0x0c000000)
for i in range(64):
    qom_set(devid, 'sysbus-irq[%d]' % i, 'gic/unnamed-gpio-in[%d]' % (112 + i))

qmpgen.dump_commands()
