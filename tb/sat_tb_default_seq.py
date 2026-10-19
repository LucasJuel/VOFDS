import cocotb
from cocotb.triggers import Combine
from pyuvm import uvm_sequence

from uvc.ssdt import uvc_ssdt_basic_seq, uvc_ssdt_seq_item


class sat_tb_default_seq(uvm_sequence):
    def __init__(self, name="sat_tb_default_seq"):
        super().__init__(name)
        self.sequencer = None
        self.cfg = None
        self.producer_seq = None
        self.consumer_seq = None

    async def pre_body(self):
        self.cfg = self.sequencer.cfg
        self.producer_seq = uvc_ssdt_basic_seq.create("producer_seq")
        self.consumer_seq = uvc_ssdt_basic_seq.create("consumer_seq")

    async def send_and_check(self, value):
        seq_item = uvc_ssdt_seq_item.create("producer_item")
        seq_item.data = value & ((1 << self.cfg.input_width) - 1)
        self.producer_seq.seq_item = seq_item

        prod_task = cocotb.start_soon(
            self.producer_seq.start(
                seqr=self.sequencer.ssdt_producer_sequencer
            )
        )
        cons_task = cocotb.start_soon(
            self.consumer_seq.start(
                self.sequencer.ssdt_consumer_sequencer
            )
        )
        await Combine(prod_task, cons_task)

        actual = self.consumer_seq.rsp.data
        expected = self.cfg.expected(value)
        expected_unsigned = expected & ((1 << self.cfg.output_width) - 1)

        assert actual == expected_unsigned, (
            f"input={value}: expected {expected} ({expected_unsigned}), "
            f"received {actual}"
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
            await self.send_and_check(value)

        self.logger.info("Default sequence checked %d values", len(values))
