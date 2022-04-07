
AARCH64_PREFIX?=aarch64-linux-gnu-

OBJCOPY:=${AARCH64_PREFIX}objcopy
OBJDUMP:=${AARCH64_PREFIX}objdump
AS:=${AARCH64_PREFIX}as

all: bootloader.bin

.PHONY: all

bootloader.bin: bootloader.o
	${OBJCOPY} -Obinary -Ielf64-little $< $@

bootloader.o: bootloader.s
	${AS} -mlittle-endian $< -o $@

objdump: bootloader.o
	${OBJDUMP} -maarch64 -D bootloader.o

bindump: bootloader.bin
	${OBJDUMP} -maarch64 -bbinary -D bootloader.bin

.PHONY: objdump bindump
