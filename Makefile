SUBDIRS:=opentitan sifive-hifive1

all: $(SUBDIRS)

.PHONY: all

$(SUBDIRS):
	make -C $@

.PHONY: $(SUBDIRS)

clean: $(addprefix clean-,$(SUBDIRS))

$(addprefix clean_,$(SUBDIRS)): clean_%:
	make -C $* clean

.PHONY: clean $(addprefix clean_,$(SUBDIRS))
