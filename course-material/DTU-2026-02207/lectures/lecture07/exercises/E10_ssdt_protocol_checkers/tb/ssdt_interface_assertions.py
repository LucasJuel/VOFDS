""" SSDT interface asserations wrapper"""

import cocotb
from cocotb.triggers import ReadOnly, RisingEdge
from cocotb.types import LogicArray


class ssdt_interface_assert_check_tb:

    passed = True
    
    def __init__(self, clk, rst, data, valid):
        self.clk = clk
        self.rst = rst
        self.data = data
        self.valid = valid
        
        
    def check(self):
        self.passed = True
        
    