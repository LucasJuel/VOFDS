from cocotb.triggers import FallingEdge, ReadOnly, RisingEdge


class ssdt_interface_wrapper:
    """Small wrapper for a synchronous streaming-data-transfer interface."""

    def __init__(self, name="ssdt_interface_wrapper"):
        self.name = name
        self.clk = None
        self.rst = None
        self.valid = None
        self.data = None

    def connect(self, clk, rst, valid, data):
        self.clk = clk
        self.rst = rst
        self.valid = valid
        self.data = data

    def initialise_driver(self):
        self.valid.value = 0
        self.data.value = 0

    async def reset_dut(self, cycles=2):
        self.initialise_driver()
        self.rst.value = 1
        for _ in range(cycles):
            await RisingEdge(self.clk)
        await FallingEdge(self.clk)
        self.rst.value = 0

    async def drive(self, value):
        """Drive one signed data item before the next active clock edge."""
        await FallingEdge(self.clk)
        width = len(self.data)
        self.data.value = value & ((1 << width) - 1)
        self.valid.value = 1

    async def drive_idle(self):
        await FallingEdge(self.clk)
        self.valid.value = 0

    async def sample(self):
        """Return (valid, signed_data) sampled after the next rising edge."""
        await RisingEdge(self.clk)
        await ReadOnly()
        valid = int(self.valid.value)
        data = self.data.value.to_signed() if valid else 0
        return valid, data
