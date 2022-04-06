
SCRIPTS_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

%.qmp: %.yaml
	$(SCRIPTS_DIR)/qmp-converter.py $< -o $@
