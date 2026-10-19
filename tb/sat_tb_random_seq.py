import os
import random

from sat_tb_default_seq import sat_tb_default_seq


class sat_tb_random_seq(sat_tb_default_seq):
    def __init__(self, name="sat_tb_random_seq"):
        super().__init__(name)

    async def body(self):
        seed = int(os.getenv("SAT_SEED", "20260928"))
        count = int(os.getenv("SAT_RANDOM_COUNT", "100"))
        rng = random.Random(seed)

        values = [
            self.cfg.saturation_min - 1,
            self.cfg.saturation_min,
            self.cfg.saturation_min + 1,
            self.cfg.saturation_max - 1,
            self.cfg.saturation_max,
            self.cfg.saturation_max + 1,
        ]
        values.extend(
            rng.randint(self.cfg.input_min, self.cfg.input_max)
            for _ in range(count)
        )

        for value in values:
            await self.send_and_check(value)

        self.logger.info(
            "Random sequence checked %d values with seed %d", len(values), seed
        )
