""" SSDT interface asserations wrapper"""

import cocotb
from cocotb.triggers import ReadOnly, RisingEdge
from cocotb.types import LogicArray


class ssdt_interface_assert_check:

    passed = True
    
    def __init__(self, clk = None, rst = None, data = None, valid = None):
        self.clk = clk
        self.rst = rst
        self.data = data
        self.valid = valid
        
        
    async def assert_reset(self):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()
            try: 
                if int(self.rst.value) == 1: 
                    assert int(self.valid.value) != 1, "Valid cannot be high, when rst is high."
            except AssertionError as msg:
                self.passed = False
                print(msg)
    
    
    async def assert_validity(self):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()
            try: 
                if int(self.valid.value) == 1:
                    assert self.data.value.is_resolvable, "When valid is high, data needs to be valid"
            except AssertionError as msg:
                self.passed = False      
                print(msg)  
                
    async def assert_invalidity(self):
        while True:
            await RisingEdge(self.clk)
            await ReadOnly()
            try:
                if int(self.valid.value) == 0:
                    assert int(self.data.value) == LogicArray("0" * len(self.data)), "When not valid data should be 0"
            except AssertionError as msg:
                self.passed = False
                print(msg)
                
    def check_assertions(self):
        cocotb.start_soon(self.assert_reset())
        cocotb.start_soon(self.assert_validity())
        cocotb.start_soon(self.assert_invalidity())
        