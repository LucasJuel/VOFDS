import cocotb
import pyuvm
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from pyuvm import ConfigDB, uvm_test

from sat_tb_config import sat_tb_config
from sat_tb_default_seq import sat_tb_default_seq
from sat_tb_env import sat_tb_env
from uvc.ssdt import ssdt_interface_wrapper


@pyuvm.test()
class sat_default_test(uvm_test):
    def __init__(self, name="sat_default_test", parent=None):
        super().__init__(name, parent)
        self.cfg = None
        self.env = None
        self.input_if = None
        self.output_if = None

    def build_phase(self):
        self.input_if = ssdt_interface_wrapper("input_if")
        self.output_if = ssdt_interface_wrapper("output_if")

        self.cfg = sat_tb_config.create("cfg")
        self.cfg.ssdt_prod_cfg.vif = self.input_if
        self.cfg.ssdt_cons_cfg.vif = self.output_if
        self.cfg.input_width = len(cocotb.top.in_data)
        self.cfg.output_width = len(cocotb.top.out_data)

        ConfigDB().set(self, "sat_tb_env", "cfg", self.cfg)
        self.env = sat_tb_env.create("sat_tb_env", self)

    def connect_phase(self):
        dut = cocotb.top
        self.input_if.connect(dut.clk, dut.rst, dut.in_valid, dut.in_data)
        self.output_if.connect(dut.clk, dut.rst, dut.out_valid, dut.out_data)

    async def run_phase(self):
        self.raise_objection("Running saturation-filter stimulus")
        clock = Clock(cocotb.top.clk, 10, unit="ns")
        cocotb.start_soon(clock.start())

        self.input_if.valid.value = 0
        self.input_if.data.value = 0
        cocotb.top.rst.value = 1
        for _ in range(2):
            await RisingEdge(cocotb.top.clk)
        cocotb.top.rst.value = 0
        await RisingEdge(cocotb.top.clk)

        sequence = sat_tb_default_seq.create("sequence")
        await sequence.start(self.env.virtual_sequencer)

        self.drop_objection("Saturation-filter stimulus complete")
