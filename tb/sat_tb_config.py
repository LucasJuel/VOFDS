from pyuvm import uvm_object


class sat_tb_config(uvm_object):
    def __init__(self, name="sat_tb_config"):
        super().__init__(name)
        self.input_if = None
        self.output_if = None
        self.input_width = 16
        self.output_width = 8

    @property
    def input_min(self):
        return -(1 << (self.input_width - 1))

    @property
    def input_max(self):
        return (1 << (self.input_width - 1)) - 1

    @property
    def saturation_min(self):
        return -(1 << (self.output_width - 1))

    @property
    def saturation_max(self):
        return (1 << (self.output_width - 1)) - 1

    def expected(self, value):
        return max(self.saturation_min, min(self.saturation_max, value))
