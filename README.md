# 02207 Verification of Digital Systems

Course repo for DTU 02207. Contains our exercise solutions and the final
assignment (Memory Arbiter verification).

## Repository structure

```
course-material/       # Submodule → github.com/Pakkutaq/DTU-2026-02207
  assignment/
    marb/              # ← Assignment: Memory Arbiter testbench (work here)
      src/rtl/         # DUT (SystemVerilog)
      src/tb/          # Testbench (pyUVM / cocotb)
  lectures/            # Lecture slides, exercises, reference material
exercises/
  E06_sat_pyuvm_env_vseq/   # Our saturation filter exercise (E06/E07)
assignment_description.md   # Summary of the MARB assignment tasks (A1–A8)
```

## Setup

Requires Python 3, a virtual environment, and Icarus Verilog (or another
supported simulator).

```sh
# Clone with submodule
git clone --recurse-submodules git@github.com:LucasJuel/VOFDS.git
cd VOFDS

# Create venv and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r course-material/DTU-2026-02207/bin/requirements.txt
```

## Running the assignment (Memory Arbiter)

```sh
source .venv/bin/activate
cd course-material/DTU-2026-02207/assignment/marb/src/tb
make
```

This runs the default test (`cl_marb_basic_test`) against the `mem_arb_wrapper`
DUT using cocotb + Icarus Verilog.

To run a specific test:

```sh
make COCOTB_TEST_MODULES=tests.cl_marb_<test_name>
```

To view coverage:

```sh
make coverage
```

## Updating course material

The `course-material/` submodule points at our fork. To pull upstream changes:

```sh
cd course-material/DTU-2026-02207
git remote add upstream git@github.com:syosil/DTU-2026-02207.git  # only once
git fetch upstream
git merge upstream/main
git push origin main
cd ../..
git add course-material/DTU-2026-02207
git commit -m "Update course material"
```
