from pyuvm import uvm_active_passive_enum, uvm_object

from uvc.ssdt import uvc_ssdt_config, uvc_ssdt_type_enum


class sat_tb_config(uvm_object):
    def __init__(self, name="sat_tb_config"):
        super().__init__(name)
        self.input_width = 16
        self.output_width = 8

        self.ssdt_prod_cfg = uvc_ssdt_config.create("ssdt_prod_cfg")
        self.ssdt_prod_cfg.is_active = uvm_active_passive_enum.UVM_ACTIVE
        self.ssdt_prod_cfg.driver_type = uvc_ssdt_type_enum.PRODUCER

        self.ssdt_cons_cfg = uvc_ssdt_config.create("ssdt_cons_cfg")
        self.ssdt_cons_cfg.is_active = uvm_active_passive_enum.UVM_ACTIVE
        self.ssdt_cons_cfg.driver_type = uvc_ssdt_type_enum.CONSUMER

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
