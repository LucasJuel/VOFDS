from pyuvm import ConfigDB, uvm_env

from sat_tb_virt_sequencer import sat_tb_virt_sequencer


class sat_tb_env(uvm_env):
    def __init__(self, name="sat_tb_env", parent=None):
        super().__init__(name, parent)
        self.cfg = None
        self.virtual_sequencer = None

    def build_phase(self):
        super().build_phase()
        
        self.cfg = ConfigDB().get(self, "", "cfg")
        ConfigDB().set(self, "virtual_sequencer", "cfg", self.cfg)
        self.virtual_sequencer = sat_tb_virt_sequencer.create(
            "virtual_sequencer", self
        )
