from pyuvm import ConfigDB, uvm_sequencer


class sat_tb_virt_sequencer(uvm_sequencer):
    def __init__(self, name="virtual_sequencer", parent=None):
        super().__init__(name, parent)
        self.cfg = None

    def build_phase(self):
        self.cfg = ConfigDB().get(self, "", "cfg")
