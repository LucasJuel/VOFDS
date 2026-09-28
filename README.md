# Saturation Filter PyUVM exercise

This is a self-contained implementation of Exercise 06. It has the class
structure requested in the handout: a testbench configuration, environment,
virtual sequencer, default virtual sequence, random virtual sequence, and a
factory override in the random test.

## Assumed DUT behavior

The handout does not provide the original DUT or its numerical specification,
so this project makes the assumptions explicit:

- `in_data` is a signed 16-bit value.
- `out_data` is a signed 8-bit value.
- Values are clamped to the output range `-128..127`.
- A valid input produces a registered valid output on the same rising edge
  (one sequential processing stage).
- `rst` is synchronous and active high.

The widths are parameters in `rtl/saturation_filter.sv`; the Python reference
model discovers the actual signal widths automatically.

## Structure

```text
rtl/saturation_filter.sv
tb/ssdt_interface_wrapper.py
tb/sat_tb_config.py
tb/sat_tb_virt_sequencer.py
tb/sat_tb_env.py
tb/sat_tb_default_seq.py
tb/sat_tb_random_seq.py
tb/sat_default_test.py
tb/sat_random_test.py
```

## Setup and execution

Install a supported simulator first. On macOS with Homebrew, Icarus Verilog is
the smallest option:

```sh
brew install icarus-verilog
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the deterministic boundary test:

```sh
make
```

Run the random test:

```sh
make random
```

The random test defaults to 100 random values and a repeatable seed. Override
them when needed:

```sh
SAT_RANDOM_COUNT=1000 SAT_SEED=123 make random
```
