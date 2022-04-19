
FREEDOM_E_SDK:=../freedom-e-sdk
freedom_e_elf=$1/software/$2/debug/$2.elf

target:=sifive-hifive1
softwares:=hello

FW_ELF:=$(addsuffix .elf, $(softwares))

qmp: machine.qmp

all: qmp fw

.PHONY: all qmp fw clean lfs

lfs:
	cp $(FW_ELF) lfs/

clean:
	rm -f machine.qmp $(FW_ELF)

sdk_clean:
	make -C $(FREEDOM_E_SDK) TARGET=$(target) clean

fw: $(FW_ELF)

$(FW_ELF): %.elf: sdk_clean
	make -C $(FREEDOM_E_SDK) PROGRAM=$* TARGET=$(target) software
	cp $(call freedom_e_elf,$(FREEDOM_E_SDK),$*) $@

.PHONY: sdk_clean $(FW_ELF)

include ../scripts/include.mk
