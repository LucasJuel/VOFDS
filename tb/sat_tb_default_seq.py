from pyuvm import uvm_sequence


class sat_tb_default_seq(uvm_sequence):
    def __init__(self, name="sat_tb_default_seq"):
        super().__init__(name)
        self.sequencer = None
        self.cfg = None
        self.input_if = None
        self.output_if = None

    async def pre_body(self):
        self.cfg = self.sequencer.cfg
        self.input_if = self.cfg.input_if
        self.output_if = self.cfg.output_if

    async def check_value(self, value):
        await self.input_if.drive(value)
        valid, actual = await self.output_if.sample()
        expected = self.cfg.expected(value)

        assert valid, f"out_valid was low for input {value}"
        assert actual == expected, (
            f"input={value}: expected {expected}, received {actual}"
        )
        self.logger.info(
            "PASS input=%d expected=%d actual=%d", value, expected, actual
        )

    async def body(self):
        values = [
            self.cfg.input_min,
            self.cfg.saturation_min - 1,
            self.cfg.saturation_min,
            -1,
            0,
            1,
            self.cfg.saturation_max,
            self.cfg.saturation_max + 1,
            self.cfg.input_max,
        ]

        for value in values:
            await self.check_value(value)

        await self.input_if.drive_idle()
        self.logger.info("Default sequence checked %d values", len(values))
