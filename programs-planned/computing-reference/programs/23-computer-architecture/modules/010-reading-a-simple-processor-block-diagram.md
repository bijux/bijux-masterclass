---
module_id: CA-010
program: Computer Architecture
level: 1
module_number: 10
title: Reading a Simple Processor Block Diagram
status: complete
last_verified: 2026-09-04
---

# Reading a Simple Processor Block Diagram

## One-Page Review

### Governing question

How can an architect read a processor block diagram as an executable hardware contract, trace each instruction from architectural inputs to committed state, and identify the control, timing, resource and exception assumptions the picture leaves unstated?

### Essential definitions

- A **datapath** contains state and transformations that carry instruction, address and data values.
- A **control path** decodes state and status into selects, enables, operation codes and sequencing decisions.
- The **program counter**, or PC, is architectural control-flow state naming the current or next instruction address under the ISA convention.
- An **instruction memory/interface** supplies encoded instruction bits for a requested address.
- A **decoder** extracts fields and determines instruction class and control intent.
- A **register file** supplies source operands and accepts architectural destination writes.
- An **immediate generator** reassembles and sign- or zero-extends encoded constants.
- An **ALU** performs arithmetic, logic, comparison and address-generation operations.
- A **multiplexer** selects one of several candidate sources according to control.
- **writeback** is the path and event that commits a produced value into architectural register state.
- A **single-cycle datapath** completes one instruction's modeled state transition per clock interval; it does not mean signals propagate instantaneously.
- A **block diagram** is an abstraction whose arrows and boxes require width, timing, ownership and protocol definitions.

### Central model, mechanism, or theorem

Read an instruction as an architectural transition:

`(PC, registers, memory, privilege/state) --instruction--> (PC', registers', memory', privilege/state')`.

Then map each changed value to a physical path and control condition: fetch instruction at `PC`; decode fields; read operands; generate immediate; select ALU inputs and operation; access data memory when required; select writeback; update exactly the permitted destination and next PC. For every unchanged architectural location, verify that its write enable is false. A diagram is understood only when each supported instruction class has a complete trace and each side effect has a unique guarded commit event.

### Critical invariants

- PC, register file, memory and control/status state have explicit owners and update events.
- Instruction fields, source/destination addresses and immediates preserve ISA widths and signedness.
- Every mux select has one defined source for each legal instruction class and safe behavior for illegal instructions.
- Register and memory write enables assert only for instructions authorized to commit those effects.
- Branch/jump target and fall-through PC calculations use the correct base, offset and alignment rules.
- Load/store width, byte lanes, extension, alignment and memory-response behavior match the interface.
- Timing boundaries account for the longest supported path and for minimum-delay obligations.
- Exceptions, reset, stalls, interrupts and memory faults are either modeled or explicitly excluded from the simple diagram.

### Common failures

Frequent failures are reading arrows as instantaneous transfers, confusing architectural state with combinational values, assuming the PC always increments by four, treating every instruction field alike, sign-extending an immediate from the wrong bit, forgetting a write-enable guard, letting stores write the register file, selecting ALU output instead of memory data for loads, treating branch comparison and target calculation as one unspecified box, ignoring register zero rules, assuming separate instruction/data boxes prove separate physical memories, overlooking the single-cycle critical path, and inventing behavior for exceptions or variable-latency memory absent from the diagram.

### Compact example

With `x1=100`, a load instruction `lw x4,12(x1)` reads base 100, sign-extends immediate 12, selects those as ALU inputs, computes address 112, requests a 32-bit memory read, extends returned data 55 as specified, selects memory data at the writeback mux and commits 55 to `x4`. PC selects fall-through. If memory is not guaranteed to respond within the cycle, the supposed single-cycle transition needs a stall or multicycle protocol not shown by the simple path.

### Connections

Processor diagrams connect ISA contracts, registers, arithmetic, memory representation, finite-state control, timing, pipelines, exceptions, caches, buses, operating systems, verification and physical implementation.

## Governing Question

A processor block diagram compresses thousands or millions of implementation details into boxes and arrows. The abstraction is valuable because it reveals ownership and flow, but dangerous when a reader assumes the picture fully specifies behavior.

The governing question is how to reconstruct an executable contract from it. Which boxes store state? Which transform values combinationally? Which arrows carry data versus control? Which clock edge commits results? Which ISA cases are unsupported or omitted?

## Why This Matters

Architecture work repeatedly moves between levels. An ISA describes software-visible transitions; a block diagram maps them onto hardware resources; RTL and physical design implement timing and electrical behavior. Confusing levels leads to false conclusions.

A diagram-tracing method also prepares later modules. Pipeline hazards are conflicts between traces at different stages. Cache behavior elaborates the memory boxes. Exceptions add alternative state transitions. Performance analysis starts with path and resource structure.

The goal is not memorizing one textbook processor. It is learning to interrogate any diagram: state, data, control, time, interfaces, invariants and omissions.

## Prerequisites and Retrieval

Before studying this module, be able to:

- decode basic instruction fields and fixed-width values;
- explain registers, memories, clocking and finite-state control;
- perform integer arithmetic and sign extension;
- identify combinational and sequential timing paths;
- distinguish ISA-visible state from implementation state.

Retrieve ISA edition and supported subset; instruction length and alignment; PC convention; register count, width and constant registers; field layouts; immediate encodings; ALU operations; load/store widths, endianness and alignment; branch/jump semantics; illegal instruction behavior; memory request/response contract; reset vector; privilege, exception and interrupt scope; diagram legend; bus widths; state elements; clock edges; control truth table; write enables; latency and frequency target; resource sharing; RTL or reference model; tests; synthesis/timing evidence; and explicit omissions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish architectural state, combinational datapath and control signals;
2. trace fetch, decode, execute, memory and writeback conceptually;
3. map instruction fields to register and immediate inputs;
4. derive control settings for ALU, load, store, branch and jump classes;
5. identify every architectural commit enable;
6. calculate branch, load and store data/address paths;
7. infer single-cycle critical-path and resource constraints;
8. expose unstated memory, exception, reset and timing assumptions;
9. compare a diagram with an ISA and executable reference model;
10. explain how multicycle and pipelined designs refine the simple model.

## Core Exposition

### Start with the legend

Identify shapes for registers, memories, combinational blocks, muxes and control. Determine whether thick lines mean buses and whether arrows indicate direction or only association.

If the diagram lacks a legend, treat symbol meaning as a hypothesis to verify. Similar-looking blocks can have synchronous or asynchronous interfaces.

### Mark architectural state

Circle the PC, architectural register file and memory or memory interface. Add control/status registers if the supported ISA includes them.

Intermediate wires are not architectural state merely because they have names. Pipeline registers or queues would be microarchitectural state in a more detailed diagram.

### Mark combinational transformations

Decoders, immediate generators, ALUs, adders, comparators and muxes transform current inputs. Annotate input/output widths and signedness.

A box named “ALU” can hide arithmetic, logic, comparison and target calculation. Determine the selected function for each instruction.

### Mark control signals

Control selects operand sources, ALU operation, memory action, writeback source and next-PC source. Write names next to mux selects and enables.

Separate data values from control bits. An instruction opcode is data entering a decoder; the decoder's `reg_write` output is control.

### Identify commit points

Architectural state changes only at specified events: PC update, register write and store acceptance or completion. Mark every enable.

The absence of an enable on a diagram may mean it was omitted for clarity, not that the resource writes every cycle. Resolve ambiguity from specification or RTL.

### Trace instruction fetch

The PC provides an instruction address. The instruction interface returns encoded bits. In a single-cycle pedagogical model, response is often combinational inside the clock interval.

Real memories have latency, faults and handshakes. State the simplifying assumption before using the path to infer timing.

### Decode fields by format

Opcode and function fields select instruction semantics. Register fields name sources and destination where the format defines them.

The same bit positions can contribute to an immediate in another format. Do not feed every apparent register field to architectural effects unconditionally.

### Generate immediates

Immediate bits may be contiguous or scattered to keep register fields stable across encodings. Reassemble by significance, append required low zeros and extend from the defined sign bit.

Annotate the immediate's pre-extension width. Sign-extending each fragment independently is incorrect.

### Read the register file

Source addresses select operand values. A two-read-port file can supply both in one modeled cycle. The destination address flows to the write port.

Read-during-write behavior matters when one instruction writes a register another reads in a pipeline, but a one-instruction-at-a-time single-cycle model separates commits by edges.

### Preserve constant registers

In RV32I, register `x0` always reads zero and writes have no architectural effect. The register-file array and bypass path must enforce this.

A diagram may label `x0` without showing suppression logic. Record it as a required invariant.

### Select the first ALU operand

Register-register arithmetic uses `rs1`. Some PC-relative operations use the current PC. Other instructions may use zero or a control/status source.

Trace the mux select rather than assuming the left ALU input always means register value.

### Select the second ALU operand

Register arithmetic uses `rs2`; immediate arithmetic, loads and stores use the decoded immediate. Shift-immediate instructions may use a narrower encoded amount.

The mux source width must match the ALU after extension. Mixed signed interpretation changes comparison and shifting, not raw addition bits.

### Select the ALU operation

Opcode and function bits determine add, subtract, AND, OR, XOR, shifts and comparisons. Address generation usually uses addition.

Use a control table: instruction class, operand selects, ALU function, memory action, writeback source, register write and PC source.

### Trace register arithmetic

For `add rd,rs1,rs2`, read both registers, select them into ALU, choose add, select ALU result for writeback and assert register write for `rd`.

Memory write is false and PC selects fall-through. Every unmentioned state remains unchanged.

### Trace immediate arithmetic

For `addi`, read `rs1`, decode/sign-extend the immediate, select it as ALU operand B, add and write ALU result to `rd`.

Do not select `rs2` merely because those instruction bits reach the register-file address pins physically; control determines semantic use.

### Trace logical and shift operations

Logical operations select their Boolean ALU function. Shifts use the low permitted shift-amount bits and choose logical or arithmetic fill.

An implementation may contain a barrel shifter separate from ALU. The diagram's one box is functional grouping, not proof of one circuit.

### Trace comparisons

Signed and unsigned less-than use the same operand bits with different interpretation. Equality can use subtraction-zero or a comparator.

Branch decision and set-less-than result are different consumers even if they share comparison logic.

### Trace a load

Read base `rs1`, generate signed offset, add for effective address and issue a memory read of declared width. Select returned data at writeback and extend based on signed/unsigned load.

Register write occurs only after valid data. Memory write is false. Alignment and access faults must suppress architectural destination commit.

### Trace a store

Read base from `rs1` and store payload from `rs2`. Add immediate to base for address. Generate byte enables and write selected low payload bytes.

Register write is false. Store commit semantics depend on the memory interface; presenting address/data is not necessarily durable completion.

### Separate address and store data

The ALU produces address while the second register-file read often supplies store data through a different path. A mux that uses immediate at ALU input does not discard `rs2`.

Label both arrows. Many beginner traces incorrectly route the immediate into memory write data.

### Trace fall-through PC

For a fixed 32-bit instruction, fall-through is often `PC+4`. Compressed or variable-length instructions use decoded length.

The incrementer can be a dedicated adder or shared ALU. Resource choice changes timing and simultaneous availability.

### Trace a conditional branch

Read operands and compare under signed/equality semantics. Generate signed branch offset, add it to the specified PC base and select target only when condition is true.

Register and data-memory writes are false. Misaligned target or instruction-access faults require behavior beyond the simplest diagram.

### Trace jumps

A direct jump generates a PC-relative target and writes the return address to `rd`. An indirect jump adds register base and immediate, then applies ISA alignment masking.

Two values commit conceptually: next PC and link register. Exception rules determine whether either commits on target fault.

### Distinguish PC value conventions

Some diagrams label PC as current instruction address; others show next PC at a register input. Pipeline diagrams can have several PCs in flight.

Annotate current, fall-through, target and committed next values explicitly. One unlabeled “PC” arrow is insufficient for a proof.

### Read muxes as alternatives

List every mux input and control encoding. A three-input writeback mux might select ALU, memory or PC-plus-length.

Unused select codes need safe behavior or must be unreachable by proved decoder logic. Avoid treating X/don't-care values as harmless in safety or security control.

### Build the control table

Rows represent instruction classes; columns represent ALU source selects, operation, memory read/write, result source, register write, branch/jump and illegal status.

Derive the table independently from ISA semantics, then compare decoder implementation. Defaults should suppress writes before a legal row enables them.

### Handle illegal instructions safely

Unsupported opcode/function combinations must not write registers or memory. They raise an illegal-instruction exception or follow the architecture's declared behavior.

Decoder don't-cares used for synthesis must remain inside side-effect-free guards. Fuzz every encoding for privilege and side effects.

### Trace widths and extension

Mark PC, instruction, register, immediate, address, memory data and byte-enable widths. Adapters or truncation must be visible.

A 64-bit address feeding a 32-bit interface is not resolved by drawing a narrower arrow. Define supported range or translation.

### Trace endianness

Register values are significance-ordered bit vectors. Memory maps their bytes by the ISA's data-endian rule. Load/store lane steering reassembles values.

Instruction field numbering is separate from byte display order. Decode the fetched instruction word under ISA rules before extracting fields.

### Identify the single-cycle path

A load path can cross PC clock-to-Q, instruction access, decode, register read, immediate generation, ALU, data memory, writeback mux, and destination setup.

The longest supported instruction constrains period even when most instructions use fewer blocks. Realistic memory makes this path unattractive or impossible.

### Check minimum paths

Short paths such as PC feedback, simple mux selections or control enables can violate hold after clock-tree insertion.

Single-cycle diagrams emphasize maximum delay but do not remove minimum-delay sign-off.

### Check resource conflicts

Separate PC increment and address/branch adders allow simultaneous calculations at area cost. Sharing one ALU requires sequencing or additional cycles.

Separate instruction and data memories avoid a structural conflict in the simple model. They may be ports or caches backed by one lower memory system.

### Distinguish logical and physical separation

Two boxes can be separate interfaces rather than physically independent arrays. One box can contain replicated or banked structures.

Use implementation evidence before inferring area, bandwidth, fault domains or contention from diagram boundaries.

### Add memory handshakes

If instruction or data response can stall, requests need valid/ready or request/acknowledge state. PC and architectural writes hold until outcome is known.

A finite-state multicycle processor can reuse resources and wait. A pipeline can decouple stages. Both refine the same architectural transition.

### Account for memory faults

Instruction-access, load and store faults change control flow and suppress normal commit. Fault address and cause become architectural state.

Precise exception behavior requires identifying which effects have happened. The simple normal-path diagram commonly omits it.

### Account for reset

Reset sets PC to a reset vector and establishes valid control state. Register-file and memory initialization follow architecture/platform rules rather than being assumed zero.

Clock availability, reset release and instruction interface readiness form a boot protocol.

### Account for interrupts

Interrupt acceptance saves a return point/cause, changes privilege and redirects PC. It can occur only at an architecturally permitted boundary.

An unprivileged simple core may omit interrupts. Mark omission rather than routing an unexplained line to PC.

### Separate ISA from microarchitecture

ISA specifies architectural state transitions, not number of ALUs, mux placement or cycle count. Many implementations satisfy the same ISA.

Compare single-cycle, multicycle and pipeline structures by trace refinement: all committed outcomes agree for the same legal instruction sequence.

### Use executable traces

Choose a small initial state and compute source values, immediate, ALU result, memory action, writeback and next PC for representative instructions.

Include negative checks: stores never write registers, branches never write data memory, and illegal encodings cause no ordinary side effects.

### Verify control and datapath together

Datapath unit tests cannot catch wrong mux selects. Decoder tests cannot catch swapped register ports. Compare architectural post-state end to end.

Assertions can state write-enable implications and next-PC rules. Formal instruction-level equivalence can compare RTL with an ISA reference under memory assumptions.

### Inspect observability

Waveforms should include current instruction/PC, decoded class, operands, immediate, ALU, memory request/response, writeback and commit validity.

Internal signal names are not a stable architectural trace interface. Define semantic commit records for longer-lived tools.

### Review omitted complexity

List caches, virtual memory, privilege, exceptions, interrupts, atomics, unaligned access, variable latency, speculation, debug, power and security features absent from the diagram.

Omission is acceptable for a teaching model when explicit. It is not permission to infer production behavior.

## Definitions and Notation

- `PC`: current architectural instruction address under a declared convention.
- `PC_next`: value committed to PC for the next architectural step.
- `rs1`, `rs2`: source-register identifiers.
- `rd`: destination-register identifier.
- `R[i]`: architectural register value at index `i`.
- `imm`: decoded and extended immediate value.
- `EA`: effective data-memory address.
- `IR`: fetched instruction bits or instruction register where present.
- `reg_write`: control permitting architectural register update.
- `mem_write`: control permitting data-memory update.
- `wb_select`: writeback-source selection.
- `pc_select`: next-PC-source selection.
- **architectural state:** software-visible state defined by the ISA.
- **microarchitectural state:** implementation state used to realize architectural transitions.
- **commit:** event at which an effect becomes architecturally visible and no longer speculative.

## Mechanisms, Invariants, or Proof Structure

1. **ISA claim:** fix supported instructions, fields, state and exception rules.
2. **State invariant:** identify PC, registers, memory and control/status owners.
3. **Fetch invariant:** instruction bits correspond to the declared current PC or accepted request.
4. **Decode invariant:** legal encodings select exactly their ISA operation; illegal ones suppress ordinary writes.
5. **Operand invariant:** register and immediate sources preserve identifiers, width and signedness.
6. **Execute invariant:** ALU/comparison computes the required value or condition.
7. **Memory invariant:** address, width, lanes, order and response match load/store semantics.
8. **Writeback invariant:** only authorized destinations receive the selected valid result.
9. **PC invariant:** fall-through, branch, jump and exception select the correct next address.
10. **Commit invariant:** every architectural side effect occurs once and together as required.
11. **Timing invariant:** all maximum and minimum paths meet the chosen clock contract.
12. **Interface invariant:** stalls, faults, reset and interrupts refine the transition safely.
13. **Resource claim:** sharing and separation match simultaneous operation requirements.
14. **Evidence invariant:** compare independent ISA traces, RTL, timing and physical reports.
15. **Change invariant:** revalidate after ISA, control, memory or stage-boundary changes.

## Alternatives and Trade-Offs

- **Single-cycle versus multicycle:** single-cycle control is conceptually direct; multicycle reuses resources and handles latency.
- **Single-cycle versus pipeline:** one instruction per long cycle simplifies overlap; pipelines improve throughput and add hazards/state.
- **Hardwired versus table control:** hardwired logic is direct; tabular/microcoded control can make complex sequencing explicit.
- **Dedicated versus shared adders:** dedicated units enable simultaneous PC/address work; sharing saves area and needs sequencing.
- **Separate versus unified instruction/data memory:** separate ports avoid structural conflict; unified storage simplifies capacity and needs arbitration/cache design.
- **Combinational versus registered memory:** combinational response supports a simple cycle; registered protocols scale timing and add latency.
- **ALU compare versus dedicated comparator:** sharing saves area; dedicated compare can improve branch timing.
- **Early versus late branch decision:** early resolution reduces control delay; late resolution reuses datapath and lengthens wrong-path exposure.
- **Central versus distributed decode:** central control is visible; distributed local decode can shorten wires and duplicate logic.
- **Explicit mux versus encoded bus:** muxes show ownership; buses can reduce wiring and need arbitration.
- **Full-width versus narrow control:** full-width operands simplify datapath; narrow units save area and add cycles.
- **Synchronous fault versus retry protocol:** immediate fault simplifies state; retry handles variable memory and needs ownership.
- **Architectural trace versus internal waveform:** commit traces are stable; internal signals localize implementation bugs.
- **Textbook omission versus production completeness:** omission teaches one concept; production must own every excluded boundary.
- **Diagram simplicity versus quantitative fidelity:** simple diagrams expose dataflow; detailed diagrams reveal timing, queues and physical costs.

## Failure Modes and Misconceptions

1. **“Every box is a state element.”** ALUs, decoders and muxes are usually combinational.
2. **“Every arrow transfers on a clock edge.”** many arrows carry combinational values during a cycle.
3. **“PC always equals the next instruction.”** diagrams vary between current and next conventions.
4. **“PC always increments by four.”** instruction length and control flow can differ.
5. **“Instruction fields always name registers.”** formats reuse positions for immediate bits.
6. **“An immediate is just contiguous low bits.”** fields can be scattered and shifted.
7. **“The register file writes every instruction.”** stores and branches suppress register write.
8. **“Stores use the immediate as write data.”** `rs2` commonly supplies payload.
9. **“Loads write the ALU result.”** ALU supplies address; returned memory data is writeback.
10. **“Register zero is safe without bypass review.”** alternate paths can expose forbidden writes.
11. **“One ALU input has one permanent source.”** mux control changes it by instruction.
12. **“Signed and unsigned compares need different stored bits.”** interpretation changes comparison.
13. **“A branch target is PC plus four plus offset.”** ISA defines the base exactly.
14. **“A jump only changes PC.”** link instructions also write a return value.
15. **“Two memory boxes prove Harvard physical storage.”** interfaces may converge below the diagram.
16. **“One-cycle memory is realistic by default.”** latency and handshake are assumptions.
17. **“Presenting a store equals durable commit.”** interface and memory hierarchy define completion.
18. **“Single-cycle means no timing analysis.”** it creates a long maximum path and hold paths.
19. **“The most boxes means the critical path.”** actual delay and resource mapping decide.
20. **“A mux unused code is harmless.”** illegal decode can assert side effects.
21. **“Illegal instructions may behave as don't-care.”** architectural containment is required.
22. **“Reset clears every register and memory.”** ISA/platform rules decide initialization.
23. **“Exceptions can be added after datapath design.”** precise commit changes control structure.
24. **“A block diagram specifies endianness.”** memory/ISA contracts do.
25. **“Datapath tests prove control.”** wrong selects and enables can still corrupt state.
26. **“One simple diagram describes all processors.”** ISA-equivalent implementations vary widely.

## Worked Examples

### Example 1

`add x3,x1,x2` with operands 7 and 9 selects two registers, ALU add and ALU writeback, committing 16 to `x3`.

### Example 2

`addi x3,x1,5` reads only `x1` semantically; bits in the `rs2` position belong to the immediate format.

### Example 3

`lw x4,12(x1)` computes 112 from base 100, reads memory value 55 and selects that value—not 112—for writeback.

### Example 4

`sw x2,12(x1)` uses the ALU for address and carries `x2` on a separate store-data path while register write stays disabled.

### Example 5

A taken branch at PC 64 with offset -8 selects PC 56. A not-taken branch selects the decoded fall-through.

### Example 6

A jump writes PC-plus-length to its destination while selecting a target for next PC. Both commit effects belong to one instruction.

### Example 7

An illegal opcode defaults mux selects arbitrarily but all write enables remain false before the exception path takes control.

### Example 8

A combinational instruction memory and data memory make a textbook load fit one cycle. Replacing either with a ready/valid interface requires state.

### Example 9

Separate instruction and data cache boxes share one lower interconnect. Concurrent misses reveal a conflict invisible at the top-level diagram.

### Example 10

An ISA reference and RTL agree on ALU values but differ on a faulting load because RTL writes `rd` before fault. Commit-level comparison finds it.

## Cross-Program Connections

- **Instruction sets:** architectural state and encoding supply the trace specification.
- **Registers and memories:** PC and register file own state; memory interfaces carry instructions and data.
- **Arithmetic:** ALU, comparison and address generation transform operands.
- **Finite-state control:** decoders, selects and enables govern side effects and multicycle waits.
- **Timing:** the block sequence identifies candidate critical paths and resource cuts.
- **Pipelining:** stage registers overlap several instruction traces and introduce hazards.
- **Caches and buses:** simple memory boxes expand into latency, ordering and fault protocols.
- **Operating systems:** exceptions, privilege and virtual memory rely on precise architectural state.
- **Verification:** instruction-level traces and commit properties compare implementation with ISA.
- **Physical design:** logical boxes do not determine area, placement, wires, power or clock behavior.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), architectural registers, instruction formats, immediates, control flow and loads/stores; retrieved 2026-09-04.
2. lowRISC, [Ibex Instruction Decode and Execute](https://ibex-core.readthedocs.io/en/latest/03_reference/instruction_decode_execute.html), concrete RISC-V decode, ALU, register and control organization; retrieved 2026-09-04.
3. lowRISC, [Ibex Instruction Fetch](https://ibex-core.readthedocs.io/en/latest/03_reference/instruction_fetch.html), fetch interface, PC behavior, buffering and branch redirection; retrieved 2026-09-04.
4. YosysHQ, [PicoRV32](https://github.com/YosysHQ/picorv32), small open RISC-V CPU implementation and configurable memory interface; retrieved 2026-09-04.
5. CHIPS Alliance, [Rocket Chip](https://github.com/chipsalliance/rocket-chip), open configurable RISC-V generator illustrating richer processor composition; retrieved 2026-09-04.
6. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), integrated core interfaces, configuration, alerts and security context; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), single-cycle and multicycle datapaths, control and processor design; retrieved 2026-09-04.
8. Nand to Tetris, [From NAND to a Computer System](https://www.nand2tetris.org/), constructive CPU, memory and machine-language projects; retrieved 2026-09-04.

## Exercises

### Exercise 1

Create a control table for register add, immediate add, load, store and equal branch with ALU sources, operation, memory action, writeback, register write and PC select.

### Exercise 2

Trace `add x3,x1,x2` for 7 and 9, `lw x4,12(x1)` for base 100 and memory 55, and a taken equal branch at PC 64 with offset -8.

### Exercise 3

Identify the single-cycle load critical-path candidates and redesign the diagram for a two-cycle memory response while preserving commit semantics.

### Exercise 4

Review a diagram for illegal instructions, misaligned loads, instruction faults, data faults, interrupts and reset. State required added state and side-effect suppression.

### Exercise 5

Construct assurance for a simple core used in an industrial safety controller, including ISA traceability, timing, faults, evidence and named review.

## Answers to the Exercises

### Answer 1

Register add selects `rs1`, `rs2`, ALU add, no memory, ALU writeback, register write true and fall-through PC. Immediate add selects `rs1`, immediate and otherwise the same. Load selects `rs1`, immediate, ALU add, memory read, memory-data writeback, register write true and fall-through. Store selects `rs1`, immediate, ALU add, memory write with `rs2` payload, register write false and fall-through. Equal branch selects `rs1`, `rs2`, equality compare, no data-memory or register write, and target PC only when equal.

Defaults suppress both register and memory writes. Width, extension, alignment and fault behavior refine each row. A real encoding can subdivide ALU and load/store widths by function fields.

### Answer 2

The register add reads 7 and 9, computes 16 and writes `x3`. The load computes effective address 112, reads 55 and writes `x4`; address 112 is not writeback. The equal branch compares two equal operands and selects `64 + (-8) = 56` as next PC without ordinary register or memory write.

<!-- bijux-verify: {"id":"simple-datapath-traces","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"add alu_result=16 write_register=x3 write_value=16\nlw effective_address=112 memory_value=55 write_register=x4 write_value=55\nbeq taken=true current_pc=64 next_pc=56 register_write=false memory_write=false\n"}} -->
```python
registers = {"x1": 7, "x2": 9}
add_result = registers["x1"] + registers["x2"]
print(f"add alu_result={add_result} write_register=x3 write_value={add_result}")

load_base = 100
load_offset = 12
memory = {112: 55}
address = load_base + load_offset
print(
    f"lw effective_address={address} memory_value={memory[address]} "
    f"write_register=x4 write_value={memory[address]}"
)

branch_pc = 64
branch_offset = -8
taken = 5 == 5
next_pc = branch_pc + branch_offset if taken else branch_pc + 4
print(
    f"beq taken={str(taken).lower()} current_pc={branch_pc} next_pc={next_pc} "
    "register_write=false memory_write=false"
)
```

This toy computes three architectural fragments. It does not decode binary instructions, model fixed-width overflow, memory handshakes, faults, timing, reset, privilege or a physical datapath.

### Answer 3

The single-cycle load path includes PC clock-to-output, instruction memory, decode/register read/immediate generation, operand mux, ALU address addition, data memory, extension/writeback mux and destination setup. Control paths to memory and register write can also be critical. Actual cell and wire delays decide the limiter.

For a two-cycle data response, add request state containing PC/instruction or decoded destination, load width/signedness, effective address and validity. Present one request, hold ownership until response or fault, then write `rd` and advance PC exactly once. Prevent new instruction commit while outstanding in the simple multicycle design. Add ready/valid handshakes, timeout/cancel policy if applicable, and assertions that faults suppress writeback and stalls preserve state.

### Answer 4

Decoder defaults suppress all ordinary writes and raise illegal cause with faulting PC/instruction. Address generation checks alignment or receives memory fault; load/store state retains address, destination/payload and instruction identity until outcome. A fault redirects PC and records cause/address without normal destination or store commit according to ISA rules.

Interrupt logic samples pending/enable at an architectural boundary, saves return PC and cause, changes privilege and redirects to a vector. Reset overrides ordinary commit, establishes reset PC and valid control, and waits for interfaces. Added state includes cause/status registers, outstanding-request ownership, saved instruction metadata and control FSM or pipeline validity. Verify priority among reset, interrupt, synchronous fault and completion plus precise side-effect ordering.

### Answer 5

Freeze ISA subset, privilege, exceptions, memory model, reset vector, clocks, implementation and toolchain. Derive an independent architectural transition model and compare every legal instruction plus illegal encodings, faults, reset and interrupts at commit. Prove write-enable, PC, constant-register, privilege and precise-exception invariants; test memory stalls, errors and resource conflicts.

Close setup/hold and I/O timing across voltage, temperature, process and aging. Analyze clock/reset loss, memory/DMA faults, state upset, arithmetic faults and common causes; add detection and independent safe control as hazards require. Run formal instruction equivalence, RTL simulation, synthesis review, static timing, fault injection, hardware-in-loop and environmental tests. Preserve source, config, netlist, constraints, binaries and results. Named architecture, RTL, ISA, formal, physical, clock/reset, safety, industrial-domain, cybersecurity, verification, manufacturing and independent-assurance authorities review their scopes. This module supplies no field authorization or certification.
