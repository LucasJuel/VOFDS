# Memory Arbiter (MARB) — Assignment Overview

## The Device: Memory Arbiter (MARB)

A shared-memory access controller. Three clients compete to read/write the same memory — the MARB decides who gets access and when.

### Architecture (4 submodules inside `mem_arb`)

**1. APB Control** — Configuration interface via APB bus. Two registers:
- **Control Register** (`0x00`): bit 0 = `enable` (on/off), bits 2:1 = `mode` (0 = static, 1 = dynamic)
- **Dynamic Priority Register** (`0x04`): three 8-bit fields (one per client), higher value = higher priority. Can only be changed while MARB is **disabled**. Takes **6 clock cycles** to update internally.

**2. Priority Selector** — Sorts clients by priority using a cascade of `single_sort` modules and an FSM with 3 states:
- **Static mode**: fixed order — CIF1 > CIF2 > CIF3
- **Dynamic mode**: sorted by the Dynamic Priority register values. The FSM goes IDLE → CLEAR → SORT → IDLE, taking as many cycles as there are clients.

**3. CRC Module** — Computes a CRC8 checksum (SMBus polynomial `x^8 + x^2 + x + 1`, i.e. `0x07`) over `{address, data}` for every MIF transaction. Broadcasts via the sSDT interface when MIF acknowledges.

**4. Combinatory Arbitration Logic** — The actual mux: picks the highest-priority client that has a pending request and drives the MIF.

### Three Protocols

| Protocol | Where used | Signals |
|----------|-----------|---------|
| **SDT** (SyoSil Data Transfer) | CIF1-3 and MIF | `rd`, `wr`, `addr`, `rd_data`, `wr_data`, `ack` |
| **sSDT** (Simple SDT) | CRC interface | `valid`, `data` |
| **APB** | Configuration | `conf_wr`, `conf_sel`, `conf_addr`, `conf_wdata`, etc. |

**SDT rules**: `rd` and `wr` can't both be high; when either is high, `addr` must be valid; when `wr` is high, `wr_data` must be valid.

**sSDT rules**: during reset, `valid` must be low; when `valid` is high, `data` must be valid; when `valid` is low, `data` must be 0.

### Design Requirements (DR01–DR14)

Key ones: reset via `rst`, synchronous to `clk`, 3 CIFs + 1 MIF + 1 APB, configurable priority, must disable before changing dynamic priority, must wait for sort to finish before re-enabling, MIF serves one client at a time, highest priority wins (ties: CIF1 > CIF2 > CIF3), CRC uses polynomial `0x07` on `{addr, data}`.

---

## The Assignment (8 tasks)

**A1. Verification Plan** — Fill in `template_svp.csv`. For each design requirement: what you're checking, how, what coverage to collect, priority, and whether it's design or protocol.

**A2. Integrate uVCs** — Wire up the **SDT** and **SSDT** uVCs (from `tb/uvc/`) into the testbench. APB is already done. Create a minimal test that does a read and a write in both static and dynamic mode.

**A3. Coverage** — Analyze built-in uVC coverage, then implement a register covergroup with:
- `cp_enable` — enable bit
- `cp_mode` — mode bits (sampled when enabled)
- `cp_prio` — priority register (sampled when enabled + dynamic)
- Cross of `cp_enable` x `cp_mode`

**A4. Fully Random Testcase** — Randomize everything you can using `pyvsc`. Discuss what should/shouldn't be randomized, which coverpoints get hit, and what additional tests would close coverage.

**A5. SDT & sSDT Protocol Checkers** — The sSDT checker exists in `ssdt_if_assertions.py`. Write the missing **SDT protocol checker** based on the protocol rules. Integrate both.

**A6. Reference Model & Scoreboard** — Build:
- `cl_marb_seq_item` (extends `cl_sdt_seq_item` with a CRC field + custom `__eq__`)
- A **reference model** that receives SDT transactions and computes the expected CRC8
- A **MIF-CRC connector** that combines MIF + CRC sSDT transactions into `cl_marb_seq_item`
- Complete the **scoreboard** (skeleton in `cl_marb_scb.py`) to compare expected vs actual

**A7. Memory Arbiter Timing Checker** — Pin-level assertion checker that verifies the arbitration is correct (which client gets served when), since the TLM-level scoreboard can't check timing/ordering.

**A8. Bonus Tasks** (optional, must be done in order):
1. Test cases to close coverage
2. Multiple-acknowledge checker
3. Test cases that assert all checkers
