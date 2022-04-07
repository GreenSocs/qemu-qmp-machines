
CPUS:=1 4

DTB:=$(patsubst %,virt-smp%.dtb, $(CPUS))
QMP:=$(patsubst %,machine-smp%.qmp, $(CPUS))

BR_SRC?=../buildroot

HERE:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
BR_OUTPUT:=${HERE}/output
BR_CONF:=${HERE}/../buildroot-configs

default: $(DTB) $(QMP)

all: default buildroot bootloader

.PHONY: all default clean

$(DTB): %.dtb: %.dts
	dtc -O dtb -I dts -o $@ $<

$(QMP): machine-smp%.qmp: machine.py
	./machine.py $* -o $@

clean:
	rm -f *.dtb *.qmp

bootloader:
	make -C bootloader

.PHONY: bootloader

buildroot: | ${BR_OUTPUT}
	make -C ${BR_OUTPUT}

${BR_OUTPUT}:
	make -C ${BR_SRC} O=${BR_OUTPUT} BR2_EXTERNAL=${BR_CONF} qemu_aarch64_virt_defconfig

buildroot-clean:
	rm -rf ${BR_OUTPUT}

.PHONY: buildroot-clean buildroot
