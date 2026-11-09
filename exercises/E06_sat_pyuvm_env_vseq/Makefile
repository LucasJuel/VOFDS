PROJECT_ROOT := $(abspath .)
RTL_DIR := $(PROJECT_ROOT)/rtl
TB_DIR := $(PROJECT_ROOT)/tb

SIM ?= icarus
TOPLEVEL_LANG ?= verilog
TOPLEVEL := saturation_filter

# Each @pyuvm.test must be loaded from the module where it is declared.
TEST ?= sat_default_test
MODULE := $(TEST)
COCOTB_TEST_MODULES := $(TEST)

VERILOG_SOURCES := $(RTL_DIR)/saturation_filter.sv
export PYTHONPATH := $(TB_DIR):$(PYTHONPATH)

.PHONY: test default random clean
test default: sim

random:
	$(MAKE) sim TEST=sat_random_test

clean::
	$(RM) -r sim_build __pycache__ tb/__pycache__ results.xml

include $(shell cocotb-config --makefiles)/Makefile.sim
