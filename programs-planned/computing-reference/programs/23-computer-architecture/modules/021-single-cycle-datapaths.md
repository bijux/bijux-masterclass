---
module_id: CA-021
program: Computer Architecture
level: 1
module_number: 21
title: Single-Cycle Datapaths
status: complete
last_verified: 2026-09-04
---

# Single-Cycle Datapaths

## One-Page Review

### Governing question

How can a processor implement each supported instruction as one clocked architectural transition while keeping combinational dataflow, resource use, control, timing, memory behavior and exceptions correct?

### Essential definitions

- A **single-cycle datapath** completes the architectural effects of each supported instruction between one launching clock edge and the next committing edge.
- The **datapath** contains state elements, combinational operators, buses and selectors that transform instruction operands into next state.
- The **control path** derives enables, operation selects and mux choices from the instruction and conditions.
- A **state element** retains architectural or implementation state across clock edges, such as the PC or register file.
- A **combinational path** transforms current inputs/state without intentional intermediate clocked storage.
- **critical path** is the longest relevant register-to-register or interface timing path under required corners/modes.
- **CPI** is cycles per retired instruction; a basic nonstalled single-cycle processor targets CPI 1.
- **clock period** is constrained by launch delay, combinational delay, setup time, skew/uncertainty and margin.
- A **resource conflict** occurs when simultaneous uses require more ports or copies than hardware provides.
- A **structural hazard** is an inability to perform required simultaneous actions with available resources.
- A **write enable** guards a state update; mux selection alone does not imply commit.
- **writeback** routes a result to an architectural destination at the committing edge.
- **Harvard organization** exposes separate instruction/data paths; a unified memory needs enough ports or another conflict solution.
- A **precise exception** commits a permitted prefix and redirects state without ordinary faulting-instruction effects.
- A **timing exception** is a physical-design constraint term and must not be confused with an architectural exception.

### Central model, mechanism, or theorem

For current architectural state `S_n` and instruction `I_n`, combinational logic computes

`S_next = F(S_n, I_n, memory_response)`.

At the active clock edge, guarded state elements commit `S_(n+1)=S_next`. For every synchronous path,

`T_clk >= t_cq + t_comb,max + t_setup + t_skew + t_uncertainty`.

The slowest supported instruction path determines the basic clock period even when faster instructions use less logic. CPI 1 does not imply high throughput: throughput is approximately `frequency/CPI` only after stalls, memory readiness and interface assumptions are accounted for.

### Critical invariants

- Current state is sampled once and all architectural writes occur only at the committing edge.
- Every instruction class selects correct sources, ALU operation, memory action, writeback and next PC.
- State not in the instruction’s permitted write set has its write enable deasserted.
- Instruction fetch and data access have sufficient independent ports or explicit conflict behavior.
- Load data is available within the declared cycle or the architecture stalls/changes implementation model.
- Branch/jump target and condition settle before the PC setup deadline.
- Illegal/faulting instructions suppress ordinary register and memory writes and select precise trap state.
- The clock constraint covers every functional path, corner, mode, hold requirement and interface assumption.

### Common failures

Frequent failures are equating single-cycle with one gate delay, assuming CPI 1 means one instruction per nanosecond, sizing the clock for arithmetic while ignoring loads, reading and writing a single-port memory simultaneously, treating two drawn memory boxes as proof of two physical memories, letting mux selects stand in for write enables, committing a store before a permission fault resolves, computing a branch target but forgetting the condition, relying on asynchronous memory when the implementation uses synchronous SRAM, overlooking register-file read/write timing, and validating functional simulation without static timing or physical corners.

### Compact example

Suppose an illustrative component model gives ALU path 2.70 ns, branch path 2.45 ns, store path 3.90 ns and load path 4.10 ns. The load is critical, so an idealized setup-only upper frequency is about `1000/4.10 = 243.90 MHz`. All instructions still take one cycle, but an add cannot use a shorter cycle unless the design introduces multiple periods, clock gating semantics or a multicycle/pipelined organization.

### Connections

Single-cycle datapaths connect ISA transitions, combinational logic, register files, memories, control decoding, static timing, physical design, exceptions, verification and later multicycle/pipelined processors.

## Governing Question

A single-cycle processor is the clearest bridge from ISA semantics to hardware. Each instruction’s reads, transformations and guarded writes can be followed across one combinational network.

The governing question is whether that network is complete and physically feasible. Every value must arrive before setup, every control must guard the right state, and every interface must actually supply the assumed service within the cycle.

## Why This Matters

Single-cycle designs teach state-transition implementation without pipeline overlap. They expose why instruction classes share resources, why muxes exist, and why the longest instruction governs timing.

They also reveal abstraction traps. A diagram with instantaneous memory is not a production SRAM interface. A correct truth table is not a timing closure. A short test program does not cover illegal encodings, faults or unintended writes.

The design remains valuable for small cores, formal reference RTL, teaching and control processors when clock and memory assumptions are acceptable. Its limits motivate multicycle reuse and pipelining.

## Prerequisites and Retrieval

Before studying this module, be able to:

- express an instruction as a pre-state to post-state transition;
- trace register operands, immediates, ALU, memory and PC updates;
- distinguish combinational logic from edge-triggered state;
- calculate propagation/setup timing and clock frequency;
- read instruction decode and write-enable tables.

Retrieve ISA/profile/subset; instruction encodings and semantics; architectural state; exception rules; reset vector; register-file ports/timing; instruction/data memory interfaces and latency; byte enables; address/data widths; combinational unit delays; mux/control topology; clock definition; PVT corners; setup/hold/skew/uncertainty; timing constraints/exceptions; interface ready/error behavior; HDL parameters; synthesis/netlist; static-timing reports; lint/formal properties; simulator/model; test programs; physical implementation; power data; fault/errata records; and exact tool/library/hardware revisions.

## Learning Objectives

After completing this module, you should be able to:

1. partition a single-cycle processor into state, combinational datapath and control;
2. trace ALU, load, store, branch and jump instructions through one cycle;
3. construct mux, operation and write-enable controls from ISA semantics;
4. identify register-file and memory port/resource requirements;
5. calculate instruction path delays, critical path and maximum frequency;
6. distinguish CPI, latency, frequency and throughput;
7. specify load/store alignment, byte enables and interface assumptions;
8. integrate illegal instructions and precise exceptions into next-state logic;
9. verify functional refinement, timing, reset and faults independently;
10. decide when single-cycle architecture is appropriate or must evolve.

## Core Exposition

### Start from architectural state

List PC, registers, memory-visible effects and control/status state. These are current-state inputs and guarded next-state destinations.

Do not add a clocked intermediate merely for drawing convenience; that would create another cycle. Pure wires and combinational outputs remain within the one transition.

### Define the clock boundary

At one active edge, PC and registers expose current values. Combinational logic settles. At the next edge, enabled state elements capture their next values.

Memory can be an exception only under an explicit interface model. If its response is registered one cycle later, a load cannot complete in one cycle without a stall or changed architecture.

### Fetch the instruction

The current PC addresses instruction memory. Instruction bits feed decoder, immediate generator and register-index ports.

Instruction memory delay belongs to every path starting from PC. Fetch errors and execute permission must reach exception selection in time.

### Decode fields

Opcode/function fields choose instruction class and ALU/control operations. Register indices and immediate fragments are extracted in parallel when possible.

Full legality checks include reserved bits, mode and extensions. A broad opcode match must not allow a near-illegal encoding to write state.

### Read the register file

Typical integer operations need two combinational read ports and one clocked write port. Stores need base and store-data sources; branches often compare two sources.

Define same-edge read/write behavior. A single-cycle sequential instruction stream ordinarily reads pre-edge state and captures the new result at the following edge.

### Generate immediates

The immediate unit concatenates scattered bits, inserts implied zeros and extends to datapath width. It can operate beside register read.

Each format needs an exact function. Selecting the wrong immediate form can yield a plausible address that fails only for certain bits.

### Select ALU operands

Operand muxes choose registers, PC, zero or immediate values. Control must encode every supported instruction combination.

Avoid relying on “don’t care” selects when a state write can accidentally occur. Safe defaults and explicit enables limit unintended effects.

### Execute arithmetic and logic

The ALU performs arithmetic, logic, shifts and comparisons. A shared adder may compute both results and effective addresses.

If branch target and data result need additions simultaneously, one adder may be insufficient in one cycle. Duplicate hardware or restructure the computation.

### Compute effective addresses

Loads/stores add base and extended displacement. Address width, alignment and access-size checks feed memory control and exception logic.

The calculation is combinational, but translation/cache/memory latency may not be. State the system boundary honestly.

### Access data memory

A load presents address/size and receives data/error soon enough for writeback selection. A store presents address, data and byte enables but commits only when permitted.

Instruction fetch and data access happen in the same cycle. Separate memories/caches or a multiported interface avoid a unified single-port conflict.

### Extend load data

Byte/halfword loads select addressed lanes and sign- or zero-extend them. Endianness and address low bits determine lane mapping.

Extension sits on the already long load path. Do not omit it from delay or semantic verification.

### Generate store byte enables

Store size and address low bits select byte lanes. Store data may be shifted/replicated to match interface conventions.

Alignment or permission failure must suppress every byte enable. Partially correct enables can corrupt adjacent data.

### Select writeback

The writeback mux chooses ALU result, load data, PC-plus-length or other supported result. Destination index comes from the instruction format.

Register write enable is separate. Stores and branches generally choose no architectural integer write, while constant-register destinations suppress writes.

### Advance the PC

Default next PC is current PC plus actual instruction length. Branch, jump and trap paths override it under exact priority.

PC mux inputs need both values and validity/conditions. A correct target with a late condition still violates timing.

### Resolve branches

Read operands, compare them, generate target and select PC. Signed/unsigned compare and immediate scaling follow the ISA.

Branch timing can include instruction memory, register read, comparator and PC mux. It may be critical even without data memory.

### Implement jumps and links

Direct/indirect jumps compute a target while optionally writing fall-through to a link destination. Target normalization and alignment checks apply.

Because PC and register file both update at the edge, target and link values must settle simultaneously.

### Build the control table

For each legal instruction class, list operand selects, ALU operation, memory read/write, access size, writeback source, register enable and PC select.

Add illegal/default and exception overrides. Review columns by state owner so no instruction accidentally writes memory or registers.

### Prefer safe control defaults

Initialize state-changing controls inactive, then assert them for fully decoded legal operations. Assign deterministic nonwriting mux values to avoid unknown propagation.

Safety by default does not replace full decode proofs. It limits damage from unhandled combinations.

### Distinguish data and control paths

Control bits are data physically, but the conceptual split helps: datapath computes candidate values; control chooses and commits permitted ones.

Verification must cover both. A correct ALU output with incorrect register enable is still an ISA violation.

### Identify shared resources

List every same-cycle use. PC increment, branch target and ALU arithmetic may require separate adders; fetch and load/store require memory bandwidth.

Resource sharing that is natural across multiple cycles creates a conflict here. Either duplicate resources or abandon strict one-cycle completion.

### Model memories realistically

Teaching designs often assume combinational read memory. FPGA block RAM and compiled SRAM commonly use registered/synchronous behavior.

Map the intended technology before finalizing the architecture. An inferred asynchronous array may synthesize to costly logic rather than the desired macro.

### Handle variable memory latency

If memory uses ready/valid and can delay, the core can stretch/stall the current instruction, making CPI exceed one even if no intermediate datapath state exists.

Call this honestly: one architectural instruction in flight with stalls, not unconditional one-cycle retirement.

### Integrate alignment and translation

Address alignment, translation and permission must resolve before load write or store commit. Full virtual-memory translation rarely fits a simple pedagogical single cycle.

A small physical-address core may omit translation by profile. The omission belongs in the supported contract, not in an unlabeled shortcut.

### Handle illegal instructions

The decoder marks unsupported/reserved encodings. Exception control suppresses ordinary writes and selects cause, saved PC and handler target.

Illegal handling adds control and timing paths. Treating the word as a no-op violates most ISA contracts.

### Handle precise faults

For load/store faults, destination and memory write enables are suppressed; trap state and PC update at the edge. Older state already resides in current registers.

Single-cycle nonoverlap simplifies the prefix, but fault signals must arrive before commit. A late bus error cannot retroactively undo an external store.

### Establish reset behavior

Reset initializes PC and required control state. Register/memory contents are only initialized if the architecture/platform says so.

Verify assertion/deassertion timing and first fetch. Asynchronous reset release near an edge can create metastability without proper synchronization.

### Derive the clock constraint

For each launched state/interface input and captured state/interface output, sum clock-to-Q, combinational cell/net delay, setup, skew/uncertainty and margin.

The maximum across modes/corners constrains period. Combinational loops and unconstrained paths invalidate the analysis.

### Find instruction-specific paths

ALU path ends at register writeback. Load adds data-memory and extension. Store ends at memory interface. Branch ends at PC.

Enumerate paths instead of assuming loads are always critical. Physical mux fanout or branch control can reverse intuition.

### Check hold time

Setup constrains maximum delay; hold constrains minimum launch-to-capture delay around the same edge. Faster paths can violate hold.

Adding period does not repair hold. Physical implementation inserts delay or changes clocking while preserving function.

### Include PVT corners

Cell/net delays vary with process, voltage and temperature. Setup and hold often have different worst corners.

Report library, voltage, temperature, RC extraction and derating. A nominal schematic sum is educational, not sign-off.

### Distinguish CPI and frequency

A basic single-cycle core retires one instruction per nonstalled cycle, so CPI approaches one. The long critical path can make that cycle slow.

A multicycle core may use shorter cycles but several per instruction; a pipeline overlaps instructions. Compare execution time, not CPI alone.

### Analyze area

Duplicated adders and separate memories avoid conflicts but cost area. Wide muxes and register-file ports also contribute.

Synthesis reports need hierarchy and macro accounting. A cell-only area that omits memories is not a processor total.

### Analyze power and energy

All combinational regions may toggle during each instruction unless gated. Even unused candidate paths can consume dynamic energy.

Operand isolation reduces switching but adds control/delay. Measure energy per instruction/workload and leakage at realistic frequency.

### Verify combinational completeness

HDL combinational blocks assign every output on every path, preventing inferred latches. Defaults plus case overrides are common.

Unknown-value simulation can expose missing assignments, but formal/lint checks give stronger coverage.

### Verify state enables

Assert that each instruction writes only its architectural write set. Illegal/fault paths have distinct permitted trap writes.

Use temporal properties from one edge to the next: if register enable is false, value remains stable; if store enable is false, no transaction occurs.

### Compare against an ISA model

At each retired edge, compare PC, register writes, memory event and exception with an independent executable model.

Normalize only specified nondeterminism. A shared decoder between model and RTL can hide the same encoding error.

### Synthesize and time

Functional simulation cannot establish frequency. Synthesize to intended technology, constrain clocks/interfaces, place/route when required and inspect reports.

Review unconstrained endpoints, false/multicycle paths and clock-domain crossings. A passing summary with bad constraints is weak evidence.

### Decide when to move on

If memory latency, resource duplication or clock period violates requirements, use multicycle sequencing or pipelining rather than disguising the problem.

Retain the single-cycle model as a functional reference. Its clarity remains useful when implementation grows.

### Govern lifecycle evidence

Bind ISA subset, RTL parameters, memory model, constraints, libraries, synthesis/place-route tools, netlist and hardware revision. Preserve test binaries and timing reports.

Track errata involving decode, byte enables, exceptions or marginal timing. Workarounds remain revision-specific.

## Definitions and Notation

- `S_n`: architectural/current state launched at cycle `n`.
- `S_next`: combinational candidate state before the committing edge.
- `I`: instruction fetched from current PC.
- `F(S,I)`: combinational next-state function under interface responses.
- `T_clk`: clock period.
- `t_cq`: launch clock-to-Q delay.
- `t_comb`: combinational cell plus interconnect path delay.
- `t_setup`: destination setup requirement.
- `t_hold`: destination hold requirement.
- `t_skew`, `t_uncertainty`: clock relationship and margin terms.
- `PC_next`: selected sequential/branch/jump/trap address.
- `RegWrite`, `MemWrite`: architectural write enables.
- `WB`: writeback value.
- `CPI`: cycles divided by retired instructions.
- `f_max`: maximum clock frequency supported by verified timing constraints.

Illustrative delays in this module are synthetic nanosecond values, not sign-off measurements.

## Mechanisms, Invariants, or Proof Structure

1. **State obligation:** prove every architectural state owner launches current values and commits only permitted next values at the edge.
2. **Fetch obligation:** prove current PC selects the correct instruction/error under the stated memory interface.
3. **Decode obligation:** prove every legal encoding selects correct controls and every unsupported encoding selects no ordinary writes.
4. **Operand obligation:** prove register/immediate/PC sources and widths match ISA semantics.
5. **Execute obligation:** prove ALU, compare, target and address candidates are exact for each instruction class.
6. **Memory obligation:** prove access address, size, byte enables, data, alignment, readiness and error behavior.
7. **Writeback obligation:** prove destination, value and enable commit exactly the permitted register effect.
8. **PC obligation:** prove sequential, branch, jump and trap priority selects the correct next PC.
9. **Resource obligation:** prove simultaneous instruction/data, add, compare and register-port demands fit physical resources.
10. **Exception obligation:** prove illegal/fault events suppress ordinary writes and commit precise trap state before the edge.
11. **Setup obligation:** prove every maximum path satisfies period under all required modes/corners/uncertainty.
12. **Hold obligation:** prove every minimum path satisfies hold independently of clock period.
13. **Reset obligation:** prove reset assertion/release establishes the required first architectural transition safely.
14. **Refinement obligation:** compare every retired edge with an independent ISA transition including memory and exceptions.
15. **Evidence obligation:** bind ISA, RTL, memories, constraints, libraries, tools, netlist, physical design, hardware and errata versions.

## Alternatives and Trade-Offs

1. **Single-cycle versus multicycle:** one-cycle control is clear; multicycle reuse supports shorter periods and synchronous memory.
2. **Single-cycle versus pipelined:** single-cycle avoids hazards; pipelines overlap work for throughput.
3. **Separate versus unified memory:** separation removes fetch/data conflict; unification saves storage/ports.
4. **Duplicate versus shared adders:** duplication enables simultaneous paths; sharing saves area but creates conflicts.
5. **Combinational versus synchronous register read:** combinational read fits one cycle; synchronous read maps efficiently to some technologies.
6. **Asynchronous versus registered memory:** asynchronous response simplifies the model; registered macros improve implementation quality but add cycles.
7. **Central versus distributed decode:** central tables ease review; distributed control can shorten/localize paths.
8. **Wide versus staged muxes:** wide muxes are conceptually direct; staged selection can improve layout/timing.
9. **Early versus late branch compare:** early compare shortens control path; shared ALU reduces hardware.
10. **Safe defaults versus don’t-care optimization:** safe inactive controls aid assurance; true don’t-cares may reduce logic.
11. **Full ISA versus small subset:** full support increases applicability; subset keeps paths/control bounded.
12. **Physical addressing versus translation:** physical-only cores are simple; virtual memory supports isolation/general OSes.
13. **Fast clock versus low voltage:** frequency improves latency/throughput; voltage reduction improves energy with timing cost.
14. **Operand isolation versus always-active paths:** isolation saves power; extra gates/control can hurt timing/area.
15. **Pedagogical clarity versus production optimization:** clarity aids proof; optimized physical structures meet real constraints.

## Failure Modes and Misconceptions

1. “Single-cycle means one combinational gate.” It means one clock interval between architectural states.
2. “Every instruction takes the same physical delay.” The clock reserves the worst path; actual settling differs.
3. “CPI 1 guarantees high performance.” Clock period and stalls matter.
4. “An add can finish early and start the next instruction.” Synchronous commit waits for the edge.
5. “Instruction memory delay is outside execution.” Fetch lies on every current-PC path.
6. “Two read operands need one register port.” Simultaneous reads require adequate ports/replication.
7. “Register writeback value alone causes a write.” A guarded enable is required.
8. “A mux don’t-care is safe on a nonwriting instruction.” Only if all relevant enables are proven inactive.
9. “One adder can compute ALU result, PC increment and branch target simultaneously.” That needs separate uses or serialization.
10. “Two memory symbols prove separate hardware.” The implementation mapping must provide independent service.
11. “Unified single-port memory supports fetch and load together.” It has a structural conflict.
12. “Asynchronous memory is available in every technology.” SRAM/FPGA macros often register reads.
13. “A ready/valid wait keeps unconditional CPI 1.” Stalls add cycles per retired instruction.
14. “Signed load changes address signedness.” It usually changes loaded-data extension.
15. “A correct address proves a correct store.” Byte enables, data, permission and commit matter.
16. “Branch target alone determines next PC.” Condition and priority select it.
17. “PC always increments by four.” Instruction length and control flow vary.
18. “Illegal instructions can safely become no-ops.” The ISA generally requires a trap.
19. “A late memory error can undo an external store.” Commit/error handshake must prevent premature visibility.
20. “Single-cycle automatically gives precise exceptions.” Signals must arrive and suppress writes before commit.
21. “Nominal delay sums prove timing.” PVT, nets, skew, uncertainty and physical implementation matter.
22. “Longer clock period fixes hold.” Hold concerns minimum delay and needs another remedy.
23. “Passing timing summary means constraints are complete.” Unconstrained paths/false exceptions can hide failures.
24. “Functional simulation verifies maximum frequency.” It normally does not model sign-off delay.
25. “Cell area is total core area.” Memories and physical overhead may be omitted.
26. “Single-cycle is always only educational.” Small systems can choose it when requirements/interfaces fit.

## Worked Examples

### Example 1

An integer add follows PC→instruction memory→decode/register read→ALU→writeback mux→register setup and simultaneously computes sequential PC.

### Example 2

A load extends the add path through effective-address ALU, data memory, lane/extension logic and writeback, often making it critical.

### Example 3

A store reads base and data, computes address and asserts selected byte enables only if alignment/permission/error state permits.

### Example 4

A branch reads operands, evaluates its condition, computes target and selects PC; it normally leaves integer registers/memory unchanged.

### Example 5

A jump-and-link selects target for PC and fall-through for register writeback at the same edge.

### Example 6

If one memory port must fetch and load in the same interval, the stated single-cycle resource schedule is infeasible without another port/copy.

### Example 7

A synchronous one-cycle-latency data SRAM returns load data after the next edge, so strict one-edge load completion is infeasible.

### Example 8

An illegal encoding drives ordinary `RegWrite=0`, `MemWrite=0` and trap-state/PC enables under exact priority.

### Example 9

With illustrative delays, the load path at 4.10 ns limits ideal frequency to 243.90 MHz while the 2.70 ns add still consumes that cycle.

### Example 10

A 20 ps minimum path can violate a 60 ps hold requirement even when a 5 ns clock easily passes setup.

## Cross-Program Connections

- **ISA:** the combinational function implements one permitted architectural transition.
- **Digital logic:** adders, muxes, decoders and enables form candidate next values.
- **Registers/memory:** ports and timing determine feasible same-cycle reads/writes.
- **Control:** instruction fields and conditions select operations and guarded commits.
- **Timing:** the longest setup and shortest hold paths constrain physical realization.
- **Exceptions:** fault signals override ordinary writes and select trap state.
- **Verification:** ISA-model comparison, assertions and negative decode tests establish refinement.
- **Physical design:** placement, interconnect, PVT and clocks replace schematic delay guesses.
- **Power:** unused candidate-path toggling can dominate a simple organization.
- **Pipelining:** long combinational paths motivate stage boundaries and hazards.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), instruction semantics, formats, registers, branches and loads/stores for a base datapath; retrieved 2026-09-04.
2. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), single-cycle processor datapath/control teaching resources; retrieved 2026-09-04.
3. Nand to Tetris, [Project 5: Computer Architecture](https://www.nand2tetris.org/project05), state, ALU, memory and instruction-driven CPU construction; retrieved 2026-09-04.
4. Clifford Wolf, [PicoRV32](https://github.com/YosysHQ/picorv32), compact RISC-V core with configurable interfaces and concrete area/frequency trade-offs; retrieved 2026-09-04.
5. lowRISC, [Ibex Pipeline Details](https://ibex-core.readthedocs.io/en/latest/03_reference/pipeline_details.html), production pipeline/control comparison and multicycle operation behavior; retrieved 2026-09-04.
6. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), integrated core interfaces, configuration, security and verification context; retrieved 2026-09-04.
7. YosysHQ, [Yosys Documentation](https://yosyshq.readthedocs.io/projects/yosys/en/latest/), RTL synthesis and reporting needed to validate implementation assumptions; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), independent executable ISA semantics for retirement-edge comparison; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace R-type add, immediate add, load, store, conditional branch and jump-and-link through a single-cycle datapath and control table.

### Exercise 2

Compute illustrative ALU, load, store and branch delays from component terms, identify the critical path and derive ideal maximum frequency.

### Exercise 3

Prove why a unified single-port synchronous memory cannot support unconditional one-cycle fetch plus load/store for the stated ISA.

### Exercise 4

Design functional, exception, reset, synthesis and static-timing verification for a single-cycle core.

### Exercise 5

Construct a decision record comparing single-cycle, multicycle and pipelined organizations for a small safety controller.

## Answers to the Exercises

### Answer 1

Add reads two registers, selects ALU add, writes ALU result to destination and advances PC. Immediate add selects extended immediate for the second input. Load computes base+offset, reads memory, extends/selects lanes and writes load data. Store computes address and writes register data with byte enables but no register write.

Branch compares sources and selects target/fall-through with no ordinary data write. Jump-and-link computes target, writes fall-through to link destination and selects target PC. Every row includes legal decode, exact write enables and exception override.

### Answer 2

The synthetic model below sums named path components. Values are pedagogical and exclude real PVT/interconnect analysis.

<!-- bijux-verify: {"id":"single-cycle-critical-path","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"alu_path_ns=2.70\nload_path_ns=4.10\nstore_path_ns=3.90\nbranch_path_ns=2.45\ncritical=load delay_ns=4.10 ideal_fmax_mhz=243.90\n"}} -->
```python
delay = {
    "pc_q": 0.10,
    "imem": 1.00,
    "decode": 0.25,
    "regread": 0.45,
    "alu": 0.60,
    "dmem": 1.40,
    "wb_mux": 0.20,
    "branch_cmp": 0.35,
    "pc_mux": 0.20,
    "setup": 0.10,
}
paths = {
    "alu": sum(delay[k] for k in ("pc_q", "imem", "decode", "regread", "alu", "wb_mux", "setup")),
    "load": sum(delay[k] for k in ("pc_q", "imem", "decode", "regread", "alu", "dmem", "wb_mux", "setup")),
    "store": sum(delay[k] for k in ("pc_q", "imem", "decode", "regread", "alu", "dmem", "setup")),
    "branch": sum(delay[k] for k in ("pc_q", "imem", "decode", "regread", "branch_cmp", "pc_mux", "setup")),
}

for name in ("alu", "load", "store", "branch"):
    print(f"{name}_path_ns={paths[name]:.2f}")
critical = max(paths, key=paths.get)
print(
    f"critical={critical} delay_ns={paths[critical]:.2f} "
    f"ideal_fmax_mhz={1000 / paths[critical]:.2f}"
)
```

The computation establishes only arithmetic over synthetic component values. A real sign-off constraint also includes routed delays, clock uncertainty, derating, modes/corners and interface constraints.

### Answer 3

Every instruction needs an instruction read from the current PC. A load/store simultaneously needs a data read/write at its effective address. One single-port memory accepts only one address/operation in the interval, so these requirements conflict. A synchronous read also returns data after an edge, too late for same-edge load writeback.

Solutions include separate instruction/data memories, dual/multiport storage, a stall/multicycle protocol or a pipeline/cache structure. The last two abandon unconditional one-cycle retirement. Prove the actual macro/interface rather than relying on two logical diagram boxes.

### Answer 4

Build decoder/control assertions for each legal/illegal class and compare every retirement edge against an independent ISA model. Exercise operands, immediates, overlaps, byte lanes, branches/jumps, memory ready/errors, illegal encodings and precise write suppression. Verify reset assertion/release and first fetch.

Lint combinational completeness and loops; synthesize with exact parameters and memory macros. Constrain all clocks and I/O, inspect unconstrained paths and timing exceptions, run setup/hold across required PVT/modes, then place/route and recheck extracted timing. Add gate-level or hardware tests proportional to risk. Preserve reports, netlists, constraints, libraries and tool versions.

### Answer 5

Define ISA subset, interrupt latency, clock/throughput, area/power, memory technology, safety goals and verification budget. Single-cycle offers simple transition reasoning but inherits the longest path and may require resource duplication/asynchronous memory. Multicycle enables resource reuse/synchronous memory but adds control-state sequencing. Pipelining raises throughput but adds hazards, forwarding and precise recovery.

Prototype/synthesize all plausible organizations with the same ISA, technology and constraints. Compare worst-case latency, sustained throughput, energy, area, fault containment and proof complexity. For safety, include timing bounds, fault injection, diagnostic coverage and safe state. Named architecture, RTL, physical, memory, safety, verification, operations and independent-assurance reviewers approve their scopes. This module supplies no certification.
