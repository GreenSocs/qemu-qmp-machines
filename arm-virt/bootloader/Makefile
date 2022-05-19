
OUTPUT?=.
AARCH64_PREFIX?=aarch64-linux-gnu-

OBJCOPY:=${AARCH64_PREFIX}objcopy
OBJDUMP:=${AARCH64_PREFIX}objdump
AS:=${AARCH64_PREFIX}as

all: ${OUTPUT}/bootloader.bin

.PHONY: all

${OUTPUT}:
	mkdir -p $@

${OUTPUT}/bootloader.bin: ${OUTPUT}/bootloader.o | ${OUTPUT}
	${OBJCOPY} -Obinary -Ielf64-little $< $@

${OUTPUT}/bootloader.o: bootloader.s | ${OUTPUT}
	${AS} -mlittle-endian $< -o $@

objdump: ${OUTPUT}/bootloader.o
	${OBJDUMP} -maarch64 -D $<

bindump: ${OUTPUT}/bootloader.bin
	${OBJDUMP} -maarch64 -bbinary -D $<

.PHONY: objdump bindump
