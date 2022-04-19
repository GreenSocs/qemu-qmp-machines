
qmp: machine.qmp

all: qmp fw

.PHONY: all qmp fw clean lfs

lfs:
	cp fw/*.elf lfs/

clean:
	rm -f machine.qmp

fw:
	make -C fw

include ../scripts/include.mk
