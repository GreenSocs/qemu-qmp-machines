
CPUS:=1 4
DTB:=$(patsubst %,virt-smp%.dtb, $(CPUS))
QMP:=$(patsubst %,machine-smp%.qmp, $(CPUS))

OUTPUT:=output
HERE:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))

BR_SRC?=../buildroot
BR_OUTPUT:=${HERE}/${OUTPUT}
BR_CONF:=${HERE}/../buildroot-configs

# generate config files (dtb, qmp raw files)

conf: $(DTB) $(QMP)

$(DTB): %.dtb: %.dts
	dtc -O dtb -I dts -o $@ $<

$(QMP): machine-smp%.qmp: machine.py
	./machine.py $* -o $@

clean:
	rm -f *.dtb *.qmp

all: conf fw

.PHONY: all conf clean

# generate fw files (bootloader + buildroot images)

fw: buildroot bootloader

.PHONY: fw fwclean bootloader buildroot

bootloader:
	make -C bootloader OUTPUT=../output/bootloader

buildroot: | ${OUTPUT}/Makefile
	make -C ${OUTPUT}

${OUTPUT}/Makefile:
	make -C ${BR_SRC} O=${BR_OUTPUT} BR2_EXTERNAL=${BR_CONF} qemu_aarch64_virt_defconfig

fwclean:
	rm -rf ${OUTPUT}

# copy fw files into cache

lfs:
	mkdir -p lfs/bootloader
	cp ${OUTPUT}/bootloader/bootloader.bin lfs/bootloader/
	mkdir -p lfs/images
	cp ${OUTPUT}/images/Image ${OUTPUT}/images/rootfs.ext4 lfs/images/

.PHONY: lfs
