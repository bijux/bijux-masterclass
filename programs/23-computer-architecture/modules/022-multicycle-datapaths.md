---
module_id: CA-022
program: Computer Architecture
level: 1
module_number: 22
title: Multicycle Datapaths
status: complete
last_verified: 2026-09-04
---

# Multicycle Datapaths

## One-Page Review

### Governing question

How can a processor divide one architectural instruction across several shorter clock cycles while reusing datapath resources, handling variable-latency interfaces, and still committing exactly one permitted ISA transition?

### Essential definitions

- A **multicycle datapath** sequences one instruction through multiple internal clocked steps before architectural completion.
- A **microstate** is an implementation control state such as fetch, decode, execute, memory or writeback.
- An **instruction register** (`IR`) holds the current instruction while later microstates reuse fetch resources.
- An **operand register** holds a source value across internal cycles.
- An **ALU-output register** stores an intermediate arithmetic result such as an effective address or branch target.
- A **memory-data register** stores a memory response before architectural writeback.
- A **control finite-state machine** selects datapath operations, enables and next microstate.
- A **resource schedule** states which hardware unit and ports each microstate uses.
- **architectural commit** is the point at which the instruction’s permitted state effects become visible.
- **variable CPI** means different instruction classes or stalls consume different cycle counts.
- A **memory handshake** uses request/ready/valid/error events rather than assuming fixed response latency.
- A **replay** repeats an internal operation safely after a wait or retry condition.
- An **idempotent request** may be repeated without changing the architectural result under its interface contract.
- A **precise exception** exposes the correct architectural prefix even though an instruction has partially executed internally.
- A **multicycle timing constraint** in physical design intentionally permits a path more than one clock period; it is distinct from a multicycle processor organization.

### Central model, mechanism, or theorem

Let architectural state be `S` and implementation state be `(S, u, X)`, where `u` is the microstate and `X` holds IR/intermediates. Internal transition function `G` advances cycles:

`(S, u, X) ->G (S*, u', X')`.

Noncommit steps preserve architectural state (`S*=S`) except explicitly allowed externally visible request protocol state. A terminal commit step produces `S'=Exec_ISA(S,I)` or its permitted trap alternative and returns to fetch. Resource reuse is correct when the schedule never demands conflicting simultaneous uses and every intermediate consumed later was captured with the right validity and instruction identity.

### Critical invariants

- `IR` and all intermediate registers belong to exactly one in-flight architectural instruction.
- Noncommit microstates cannot update architectural registers, PC or memory except through explicitly staged/authorized protocol effects.
- Each instruction class follows a legal finite microstate path to commit, trap or reset recovery.
- Reused ALU, memory and register-file ports are scheduled without same-cycle conflicts.
- Memory requests are issued once or replayed only under a proven idempotent handshake rule.
- Wait states preserve request operands, control and intermediates until a terminal response.
- Faults discard or suppress partial internal work and commit precise trap state.
- Clock timing covers every microstate path; CPI/latency covers state count plus data-dependent stalls.

### Common failures

Frequent failures are calling any long combinational operation multicycle, overwriting the instruction register during a stall, recomputing an address from changed operands, using one ALU twice in the same microstate, incrementing PC again when fetch waits, issuing duplicate stores while ready is low, treating a captured load value as architectural before writeback, forgetting validity on intermediate registers, returning to fetch after an unhandled microstate, counting nominal states but not wait cycles, assuming shorter clock guarantees faster programs, and adding a physical multicycle exception to hide an architecturally late path.

### Compact example

A simple sequence can use fetch, decode, execute and writeback for ALU operations; loads add memory and writeback; stores add a memory commit state; branches resolve after decode/execute. If illustrative stage maxima require a 1.40 ns clock and an instruction mix averages 4.10 cycles, mean instruction time is 5.74 ns (174.22 MIPS idealized). A 4.10 ns single-cycle reference reaches 243.90 MIPS. Multicycle organization can still be preferred for synchronous memory, area and extensibility; shorter clock alone does not ensure higher throughput.

### Connections

Multicycle datapaths connect ISA refinement, finite-state control, resource sharing, memory protocols, precise exceptions, performance modeling, synthesis, formal verification and later pipelining/microprogramming.

## Governing Question

A single-cycle datapath performs every required action within one long interval and may duplicate resources. A multicycle datapath introduces internal state so the same ALU or memory port can serve different roles in different cycles.

The governing question is whether that sequencing remains invisible architecturally. Software should observe one instruction transition, not intermediate addresses, temporary register values or duplicate bus effects.

## Why This Matters

Multicycle design maps naturally to synchronous memories and iterative arithmetic. It can reduce area and shorten the clock period. It also adds a control-state space where lost enables, stale intermediates and repeated requests create subtle failures.

Performance becomes a product of clock period and instruction-specific cycle count. A design can clock much faster and still retire fewer instructions per second. Workload mix and wait-state distribution matter.

Verification must cover sequences, not only combinational truth tables. Every legal opcode, response timing, exception, reset point and transition should terminate safely with exactly the permitted architectural effects.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace a single-cycle datapath and its critical paths;
- design a synchronous finite-state machine;
- distinguish architectural state from microarchitectural state;
- interpret ready/valid and request/response protocols;
- compute clock period, CPI, latency and throughput.

Retrieve ISA/profile/subset; instruction classes and exceptions; architectural commit definition; microstate diagram/table; intermediate-register inventory and validity; resource schedule; register-file timing; memory request/response protocol; retry/idempotence rules; iterative-unit protocol; PC update states; register/memory write states; fault priority; interrupt acceptance; reset from every microstate; per-state timing paths; clock constraints and PVT corners; instruction-mix/stall distributions; HDL parameters; synthesis/STA reports; formal liveness/refinement properties; test binaries; power/area; hardware traces; errata; and exact tool/library/revision data.

## Learning Objectives

After completing this module, you should be able to:

1. separate architectural state from multicycle intermediate state;
2. construct microstate sequences for ALU, load, store, branch and jump instructions;
3. schedule shared ALU, register-file and memory resources without conflicts;
4. design instruction, operand, address and memory-data registers with valid enables;
5. integrate ready/valid waits and avoid duplicate side effects;
6. define commit and precise fault behavior across partial internal execution;
7. derive cycle time, class-specific CPI and workload-average performance;
8. distinguish multicycle architecture from physical timing exceptions;
9. verify safety, liveness, reset and ISA refinement properties;
10. decide when resource reuse outweighs control and latency costs.

## Core Exposition

### Keep the ISA boundary fixed

Begin with the same architectural transition used for a single-cycle core. Internal cycles are a refinement, not new software-visible instructions.

Identify the commit event for registers, PC and memory. If memory becomes visible earlier than register commit, prove the combined instruction remains precise under faults and interrupts.

### Introduce microstate

The control FSM records which internal step is active. Its state is microarchitectural and normally inaccessible to software.

Use durable semantic names such as fetch, decode, address, memory-read and writeback. Encodings can be optimized later while formal/debug maps preserve meaning.

### Capture the instruction

Fetch reads memory at PC and captures returned instruction in `IR` only when the response is valid and accepted.

Later states decode `IR`, not a changing memory bus. During a wait, PC and IR write enables remain inactive unless the protocol completes.

### Update PC during fetch carefully

The sequential PC can be computed during fetch and committed when instruction acceptance occurs. It must not increment on every wait cycle.

Branches/jumps later override or replace the sequential value according to the chosen organization. Saved exception PC requires preserving the instruction address separately if PC advanced early.

### Capture source operands

Decode can read register sources and store them in operand registers `A` and `B`. This frees register-file ports in later states.

Source capture uses the instruction’s architectural pre-state. Validity and instruction identity prevent stale operands from a prior instruction.

### Compute common values early

The ALU can compute branch target or immediate-derived values during decode while register operands settle, if resource timing permits.

Speculative intermediate calculation is safe when it has no architectural effect and later control selects only the correct value.

### Execute ALU instructions

An execute state selects `A`, `B` or immediate and produces an ALU result captured into `ALUOut`. A later writeback state writes the destination.

Alternatively, execute can write the register directly if commit conditions are already known. Keep the architectural commit definition consistent across classes.

### Compute memory addresses

Load/store address state reuses the ALU for `base+offset` and captures the effective address. Alignment and early protection checks can occur here.

The address must remain stable through a memory wait. Recomputing from registers risks seeing later debug or erroneous state changes.

### Issue a load request

Memory-read state presents captured address, size and attributes. A request handshake records that the transaction was accepted.

Response may arrive later. The FSM holds or moves into a distinct wait state without issuing uncontrolled duplicate requests.

### Capture load data

When response valid arrives without error, capture data into `MDR`. Lane selection and extension occur before or during capture/writeback.

Only load-writeback enables the architectural destination. A memory response itself is not a register commit.

### Issue a store request

Store state presents address, data and byte enables. Its externally visible commit point depends on the bus/memory protocol.

Once accepted, do not repeat a non-idempotent store. Track outstanding state until completion/error and delay instruction completion as required.

### Resolve branches

Branch state reuses ALU/comparator resources to evaluate operands and select target versus already computed sequential PC.

If target was computed earlier, preserve it in `ALUOut`. Ensure later address calculation has not overwritten that register along the branch path.

### Implement jumps and links

Jump state selects direct/indirect target and writes link state at commit. If sequential PC was captured early, it can supply the link value.

Target normalization, alignment and exception checks must complete before committing PC/link.

### Schedule resource reuse

Build a table with microstates as rows and ALU, memory, register read/write, mux and intermediate enables as columns.

One ALU can increment PC in fetch, form target in decode, execute arithmetic and form addresses on separate cycles. Any row requiring two results reveals a conflict.

### Add intermediate registers deliberately

Each register breaks a path and preserves a value for later reuse. Define width, enable, reset/unknown state and validity.

Do not expose unnecessary intermediates architecturally. Reset need not clear every data bit if validity prevents use, but verification must prove that invariant.

### Design control outputs

Control depends on current microstate plus decoded instruction and response conditions. State-changing outputs default inactive.

Separate request-valid, response-ready, internal capture and architectural commit enables. Collapsing them invites repeated effects.

### Define next-state logic

Fetch waits for instruction response; decode branches by opcode; execution paths reach commit/writeback or fault; terminal state returns to fetch.

Provide a safe illegal-state recovery, typically reset/trap rather than silent arbitrary writes. Prove no legal path enters unused encodings.

### Use Moore or Mealy control consciously

Moore outputs depend on registered microstate; Mealy outputs also depend on current inputs such as ready/error. Mealy response handling can save cycles.

It also creates longer combinational paths from interfaces to enables/next state. Register or constrain them and avoid protocol loops.

### Support fixed-latency memory

A known one-cycle synchronous memory can use request then response/capture states. The schedule is simple but tied to that interface.

If implementation later adds caches or external memory, fixed timing assumptions fail. Abstract handshakes improve portability.

### Support variable latency

Hold transaction identity and operands across arbitrary legal wait cycles. Only terminal response advances the instruction.

Liveness needs an environment assumption that a valid request eventually receives response. Safety must still hold if response is delayed indefinitely.

### Avoid duplicate requests

In decoupled protocols, keep valid asserted until acceptance without changing payload; after acceptance, mark outstanding and stop presenting a new request.

Stores and MMIO reads may be non-idempotent. A repeated request is not harmless even if final register values look right.

### Integrate iterative execution

Multiply/divide or cryptographic units can use start/busy/done. Issue start once, preserve operands and wait for done/error.

Cancellation on reset/trap and result validity need definition. A stuck busy signal becomes a liveness failure.

### Define architectural commit

Commit can occur in different terminal states per instruction class, but every event records instruction PC/encoding and exact write set.

Trace interfaces should emit one retirement per instruction, not one per microstate. This makes comparison with the ISA model direct.

### Handle exceptions before commit

Illegal decode, alignment, memory error or execution fault transitions to trap with ordinary writes suppressed. Intermediates are discarded via validity/control reset.

If a store request already committed externally before a later fault, all-or-none precision may be impossible. Order checks before irreversible effects.

### Accept interrupts at boundaries

A simple multicycle core can accept maskable interrupts between instructions after commit and before the next fetch.

Long waits increase latency. Supporting interruption mid-instruction requires restart/cancel semantics and preserved request state; do not improvise it.

### Reset from every microstate

Reset clears control/outstanding validity, selects reset PC and prevents stale response or intermediate state from committing.

External requests may already be in flight. The system protocol must define reset cancellation, drain or response tagging.

### Shorten the clock period

Each microstate path now covers a subset of work: fetch memory to IR, register read to operands, ALU to `ALUOut`, memory to `MDR`, or mux to register.

The largest stage path plus sequential overhead constrains clock. Poorly balanced stages waste potential.

### Include register overhead

More cycles add clock-to-Q, setup, skew and energy at intermediate boundaries. Dividing logic does not make the sum of cycle delays equal the original combinational delay automatically.

Muxing for reuse can add delay. Measure synthesized paths, not only block estimates.

### Compute class CPI

Count microstates from accepted fetch through retirement, plus expected/observed wait cycles. Different instructions take different counts.

Branches can finish earlier than loads. Iterative divide is data- or implementation-dependent.

### Compute workload-average CPI

For class fractions `p_i` and mean cycle counts `c_i`, `CPI_avg=sum p_i*c_i` when fractions cover retired instructions.

Execution time is `IC*CPI_avg*T_clk` plus separately modeled effects. Validate instruction mix on representative binaries.

### Compare with single-cycle fairly

Use the same ISA subset, memory semantics, technology and workload. Single-cycle CPI 1 may have longer `T_clk`; multicycle has shorter `T_clk` but higher CPI.

Include stalls and interface feasibility. A single-cycle baseline with impossible combinational memory is not a fair implementation.

### Analyze area

One shared ALU and unified memory port reduce duplicated resources. Intermediate registers, muxes and control ROM/FSM add area.

Memory macros dominate many small cores. Report them consistently and include controller/interconnect overhead.

### Analyze energy

Resource reuse reduces duplicated combinational hardware but increases clocked cycles and intermediate-register toggles.

Clock gating and operand isolation help. Measure energy per retired instruction and workload, not power at unequal throughput alone.

### Verify safety properties

Assert write enables only in permitted states; request payload stable while stalled; one accepted store per instruction; no response captured without outstanding request.

Assert microstate/opcode combinations and intermediate validity. Cover every legal transition and exception exit.

### Verify liveness properties

Under fair response/unit-done assumptions, every accepted instruction eventually retires or traps. Detect FSM cycles that make no permitted progress.

Separate environment failure from core deadlock. Timeouts may be platform policy rather than ISA behavior.

### Prove ISA refinement

Hide internal microsteps and compare initial/final architectural state plus memory events against one ISA transition.

Stuttering refinement permits any finite number of noncommit internal steps. Proof needs a ranking/progress argument under environment assumptions.

### Validate timing constraints

Constrain the real clock and interfaces; time every state-dependent path across PVT/modes. Physical multicycle path exceptions are used only when capture truly occurs later by design.

Never apply a broad exception just because an operation spans microstates—the intermediate registers already define ordinary one-cycle paths.

### Govern lifecycle evidence

Bind ISA subset, FSM/control table, RTL parameters, protocol version, memories, constraints, libraries, tools, netlist and hardware revision. Preserve per-instruction traces.

Track errata involving duplicate transactions, stale intermediates, reset, exceptions or state lockup. Mitigations remain explicit.

## Definitions and Notation

- `S`: architectural state before the current instruction.
- `u`: current microstate.
- `X`: intermediate state (`IR`, operands, `ALUOut`, `MDR`, validity/outstanding bits).
- `G`: one internal clock transition.
- `Exec_ISA(S,I)`: permitted architectural result or trap alternative.
- `commit`: terminal event exposing one architectural instruction transition.
- `IRWrite`, `PCWrite`, `RegWrite`, `MemReq`: distinct guarded enables/events.
- `ready`, `valid`, `error`: interface handshake/terminal response signals.
- `c_i`: mean cycles for instruction class `i`, including its waits.
- `p_i`: retired instruction fraction for class `i`.
- `CPI_avg=sum p_i*c_i`.
- `T_clk`: verified microcycle period.
- `T_inst=CPI_avg*T_clk`: mean instruction time under stated assumptions.
- `IPC=1/CPI_avg`: mean retired instructions per cycle for a single-in-flight design.
- `stutter`: internal transition preserving architectural state and external architectural history.

Illustrative timing and instruction mixes are synthetic and exclude real cache/fabric distributions.

## Mechanisms, Invariants, or Proof Structure

1. **Ownership obligation:** prove IR and all valid intermediates belong to the one active instruction and are not overwritten early.
2. **Path obligation:** prove every legal instruction follows a defined finite microstate path to commit/trap.
3. **Resource obligation:** prove each microstate’s ALU, register and memory uses fit available ports/resources.
4. **Capture obligation:** prove each intermediate is captured once from correct sources and consumed only while valid.
5. **Control obligation:** prove default/decoded enables cannot write architectural or external state in noncommit states.
6. **Protocol obligation:** prove request/payload stability, single acceptance, response matching and no duplicate non-idempotent effects.
7. **Wait obligation:** prove arbitrary legal waits preserve control, operands and outstanding identity.
8. **Commit obligation:** prove each instruction emits exactly one permitted architectural transition and retirement record.
9. **Exception obligation:** prove faults suppress irreversible ordinary effects and commit exact trap state.
10. **Interrupt obligation:** prove acceptance occurs only at supported boundaries with bounded claims documented.
11. **Reset obligation:** prove reset from every microstate invalidates stale/outstanding work under the system protocol.
12. **Timing obligation:** prove all one-microcycle setup/hold paths meet constraints across required corners/modes.
13. **Performance obligation:** prove CPI/latency/throughput calculations include instruction mix and variable waits.
14. **Refinement obligation:** prove finite stuttering internal paths refine one ISA instruction under explicit fairness assumptions.
15. **Evidence obligation:** bind ISA, FSM, RTL, interfaces, memories, constraints, tools, hardware and errata versions.

## Alternatives and Trade-Offs

1. **Single-cycle versus multicycle:** single-cycle simplifies control; multicycle shortens paths and reuses resources.
2. **Multicycle versus pipeline:** multicycle has one instruction in flight; pipelining overlaps several for throughput.
3. **Hardwired FSM versus microcode:** FSM logic is direct; microcode makes complex sequencing table-driven.
4. **Shared versus duplicated ALU:** sharing saves area; duplication shortens schedules.
5. **Unified versus separate memory ports:** unification saves interface resources; separation avoids fetch/data serialization.
6. **Fixed versus variable memory latency:** fixed schedules are simple; handshakes support caches/external memory.
7. **Implicit versus explicit wait state:** self-loop is compact; explicit outstanding states make protocol reasoning clearer.
8. **Early versus late PC increment:** early computation reuses fetch time; late update simplifies faulting-PC bookkeeping.
9. **Direct writeback versus result register:** direct commit saves a cycle; captured results simplify timing/control.
10. **Moore versus Mealy outputs:** Moore control is registered/simple; Mealy response handling reduces latency but lengthens paths.
11. **One versus several intermediate buses/registers:** fewer save area; more isolate timing and preserve concurrent candidates.
12. **Boundary-only versus mid-instruction interrupts:** boundaries simplify precision; checkpoints reduce worst-case latency.
13. **Short clock versus fewer cycles:** finer steps shorten period; coarser steps reduce CPI/overhead.
14. **Area versus energy:** reuse reduces duplicated logic; extra cycles/clocking can increase energy.
15. **Optimized state encoding versus semantic traceability:** optimized encoding helps physical metrics; traceable state names aid assurance.

## Failure Modes and Misconceptions

1. “Multicycle means a combinational path gets several periods.” Architectural sequencing requires intermediate state/control.
2. “Each instruction still has CPI 1.” Different paths consume several cycles.
3. “Shorter clock guarantees faster programs.” CPI and waits can outweigh it.
4. “Internal registers are architectural.” They are hidden implementation state unless specified.
5. “IR can follow memory continuously.” It must capture once per accepted fetch.
6. “PC increments on every fetch-state cycle.” It advances only on the accepted event.
7. “Operands can be reread later safely.” Preserve pre-state values and dependencies explicitly.
8. “One ALU can produce two results in one microstate.” Resource time must be scheduled.
9. “ALUOut always contains the current needed value.” Path-specific overwrites and validity matter.
10. “Memory request valid means accepted.” Handshake distinguishes presentation and acceptance.
11. “Holding store request repeats harmlessly.” Protocol may accept it once or multiple times unless controlled.
12. “Every request is idempotent.” Stores and MMIO reads can have side effects.
13. “Load response can write the register immediately in any state.” Instruction identity, errors and commit control matter.
14. “Wait states need no explicit invariants.” Payload and intermediates must remain stable.
15. “A fixed memory state handles caches automatically.” Variable latency requires a protocol path.
16. “Iterative unit start may remain asserted.” It can restart work unless handshake semantics say otherwise.
17. “A store can commit before all faults resolve.” That can violate precise exceptions.
18. “Interrupting any microstate is safe.” Cancellation/restart semantics are needed.
19. “Reset only needs testing in fetch.” Outstanding requests and intermediates exist elsewhere.
20. “Unused FSM encodings can do anything.” Recovery/control must prevent unsafe writes.
21. “Nominal state count equals observed CPI.” Waits and iterative latency add cycles.
22. “Mean CPI proves worst-case latency.” Distributions and bounds differ.
23. “Resource reuse always saves energy.” Extra clock cycles/register toggles can reverse it.
24. “A physical multicycle constraint implements the FSM.” It only tells timing analysis about a real capture relationship.
25. “Functional completion proves liveness.” Some response patterns may deadlock.
26. “Matching final registers proves refinement.” Memory transactions, traps and duplicate effects also matter.

## Worked Examples

### Example 1

An ALU instruction follows fetch→decode→execute→writeback, with architectural register commit only in writeback.

### Example 2

A load follows fetch→decode→address→memory-read/wait→load-writeback, capturing address and memory data separately.

### Example 3

A store follows fetch→decode→address→store-request/completion; no register writeback occurs.

### Example 4

A branch can follow fetch→decode→branch-resolve and then return to fetch, consuming fewer cycles than a load.

### Example 5

One ALU increments PC in fetch, computes an effective address later and executes arithmetic on another path without same-cycle conflict.

### Example 6

A three-cycle memory wait adds three cycles to that instruction’s observed CPI while request address/data remain stable.

### Example 7

An illegal instruction leaves decode for trap, suppresses ordinary writes and invalidates intermediate work.

### Example 8

A store accepted once must not be reissued while waiting for completion; an outstanding bit separates accepted from presenting.

### Example 9

Synthetic 1.40 ns cycle and 4.10 average CPI produce 5.74 ns/instruction and idealized 174.22 MIPS.

### Example 10

A reset during load wait clears instruction/outstanding validity and follows the bus reset contract so a late response cannot write a new instruction’s destination.

## Cross-Program Connections

- **ISA:** internal microsteps stutter until one permitted architectural transition commits.
- **Finite-state machines:** control states and guarded transitions sequence resources.
- **Datapaths:** intermediate registers enable ALU, memory and port reuse.
- **Protocols:** ready/valid and outstanding identity govern variable latency.
- **Exceptions:** partial internal work is suppressed before precise trap commit.
- **Performance:** clock period and instruction/stall-specific CPI jointly determine time.
- **Formal methods:** safety, liveness and stuttering refinement cover sequencing.
- **Synthesis/timing:** state boundaries turn long paths into separately constrained paths.
- **Power/area:** resource reuse trades against registers, muxes and extra clock activity.
- **Pipelining:** overlapping instruction microsteps extends the schedule into a pipeline.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), instruction semantics and architectural outcomes refined by multicycle sequencing; retrieved 2026-09-04.
2. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), multicycle datapath and control teaching resources; retrieved 2026-09-04.
3. Nand to Tetris, [Project 5: Computer Architecture](https://www.nand2tetris.org/project05), CPU, memory and state construction foundations; retrieved 2026-09-04.
4. Clifford Wolf, [PicoRV32](https://github.com/YosysHQ/picorv32), compact multi-cycle RISC-V core, iterative options and memory interface; retrieved 2026-09-04.
5. lowRISC, [Ibex Pipeline Details](https://ibex-core.readthedocs.io/en/latest/03_reference/pipeline_details.html), multicycle operations, pipeline stalls and control comparison; retrieved 2026-09-04.
6. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), integrated core configuration, interfaces, security and verification; retrieved 2026-09-04.
7. YosysHQ, [Yosys Documentation](https://yosyshq.readthedocs.io/projects/yosys/en/latest/), synthesis and implementation reports for resource/timing validation; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), independent ISA semantics for stuttering-refinement comparison; retrieved 2026-09-04.

## Exercises

### Exercise 1

Construct microstate/control sequences for ALU, load, store, branch and jump-and-link instructions using one shared ALU and memory port.

### Exercise 2

Compute cycle period, workload-average CPI, mean instruction time and throughput for a synthetic multicycle design, then compare a single-cycle baseline.

### Exercise 3

Specify a ready/valid load/store FSM that prevents duplicate requests and stale responses under arbitrary waits and reset.

### Exercise 4

Design safety, liveness and ISA-refinement verification for the control FSM and intermediate state.

### Exercise 5

Construct a decision record for adding a long-latency divide unit and mid-instruction interrupt checkpoints.

## Answers to the Exercises

### Answer 1

All paths begin with accepted fetch/IR capture and decode/operand capture. ALU uses execute/result capture/writeback. Load uses address capture, request/wait, data capture and writeback. Store uses address capture then one accepted request/completion. Branch resolves condition and target without register writeback. Jump selects target and writes link at one terminal commit.

The resource table must show only one ALU and memory use per row. PC/IR, operand, result, MDR, architectural register and memory request enables are separate. Fault transitions override terminal ordinary writes.

### Answer 2

The synthetic model assumes stage maxima in nanoseconds and nominal no-extra-wait cycle counts.

<!-- bijux-verify: {"id":"multicycle-performance-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"clock_period_ns=1.40 ideal_fmax_mhz=714.29\naverage_cpi=4.10 mean_instruction_ns=5.74 ideal_mips=174.22\nsingle_cycle_instruction_ns=4.10 single_cycle_mips=243.90\n"}} -->
```python
state_delays_ns = {"fetch": 1.20, "decode": 0.90, "execute": 1.10, "memory": 1.40, "writeback": 0.70}
clock_period = max(state_delays_ns.values())
mix = {"alu": 0.50, "load": 0.25, "store": 0.10, "branch": 0.10, "jump": 0.05}
cycles = {"alu": 4, "load": 5, "store": 4, "branch": 3, "jump": 3}
average_cpi = sum(mix[name] * cycles[name] for name in mix)
mean_instruction = clock_period * average_cpi
single_cycle_period = 4.10

print(f"clock_period_ns={clock_period:.2f} ideal_fmax_mhz={1000 / clock_period:.2f}")
print(
    f"average_cpi={average_cpi:.2f} mean_instruction_ns={mean_instruction:.2f} "
    f"ideal_mips={1000 / mean_instruction:.2f}"
)
print(
    f"single_cycle_instruction_ns={single_cycle_period:.2f} "
    f"single_cycle_mips={1000 / single_cycle_period:.2f}"
)
```

This establishes arithmetic for invented delays/mix only. Real comparison includes waits, technology, memory feasibility, synthesis and workload distributions.

### Answer 3

Use idle/request/wait/response states plus an outstanding bit/tag. While request valid and not accepted, keep address, size, data and byte enables stable. On acceptance, mark outstanding and cease creating new transactions. Accept a response only for the outstanding instruction/tag; capture load data or error once.

For store, define the bus commit acknowledgment and never replay after acceptance unless protocol explicitly guarantees safe idempotence. On reset, follow the bus cancellation/drain/tag rule and invalidate internal destination state so late responses cannot commit. Assert these properties under arbitrary ready/valid timing.

### Answer 4

Safety: legal state transitions, correct opcode paths, valid intermediates, inactive default writes, stable stalled payload, one accepted request, matched response, precise faults and exactly one retirement. Liveness: under eventual-response/unit-done assumptions, each accepted instruction reaches commit/trap; reset reaches fetch.

Refinement: snapshot architectural pre-state/IR, hide finite noncommit microsteps, and compare terminal register/PC/memory/trap trace with an independent ISA step. Prove a ranking or exclude unfair infinite waits. Cover all opcodes, response/error timings, reset points and illegal FSM encodings.

### Answer 5

Define divide operands, signedness, divide-by-zero/overflow, result registers, start/done/cancel and worst-case cycles. Decide whether interruption waits, cancels/restarts or checkpoints; preserve exact architectural source and exception state.

Compare area/timing/energy of iterative versus faster divider and resulting interrupt latency. Verify one start, stable operands, eventual done under assumptions, correct boundary arithmetic, reset/trap cancellation and no stale result commit. Inject interrupts at every iteration and faults in control/datapath. Named ISA, microarchitecture, RTL, real-time, physical, safety, verification and independent-assurance reviewers approve their scopes. This module supplies no certification.
