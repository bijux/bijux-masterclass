---
module_id: CA-023
program: Computer Architecture
level: 1
module_number: 23
title: Hardwired and Microprogrammed Control
status: complete
last_verified: 2026-09-04
---

# Hardwired and Microprogrammed Control

## One-Page Review

### Governing question

How should a processor generate a correct sequence of datapath controls: directly from decode and state logic, from words in a control store, or from a deliberately verified combination of both?

### Essential definitions

- **control signals** select sources, operations, destinations, write enables, requests and next-state behavior.
- A **hardwired controller** derives controls and next state from combinational logic plus explicit state registers.
- A **microprogrammed controller** reads control words from a control store and advances a microprogram counter or sequencer.
- A **microinstruction** is one control-store word governing one internal step.
- A **microprogram** is a control-flow graph of microinstructions implementing an architectural operation or helper sequence.
- A **control store** holds microinstructions; it may be immutable ROM-like logic, writable storage or a mixture.
- A **microprogram counter** (`uPC`) identifies the current microinstruction address.
- A **dispatch** maps an instruction class or event to a microprogram entry address.
- **horizontal microcode** exposes many control bits directly and tends to be wide.
- **vertical microcode** encodes mutually exclusive choices into fields and requires local decoding.
- A **nanostore** is a second-level store used to share or expand recurring control patterns.
- A **micro-subroutine** shares a control sequence through call/return state.
- A **patch mechanism** replaces selected control behavior under a documented trust and compatibility contract.
- **architectural microcode** is software-visible instruction encoding; implementation microcode is normally hidden. They are not synonyms.
- **control equivalence** means two controllers produce the same permitted architectural traces under the same interface assumptions.

### Central model, mechanism, or theorem

Let `d` be decoded instruction/event information, `u` internal control state, `f` current flags and handshakes, and `c` the control vector. A hardwired controller implements

`H(d,u,f) = (c,u')`.

A microprogrammed controller reads `M[u] = (c,b)` from control store `M`; sequencer `Q(b,d,f)` chooses `u'`. Correctness is not determined by representation. For every legal instruction and environment trace, noncommit steps must preserve architectural state, enabled controls must respect datapath/protocol invariants, and the terminal transition must match the ISA step or permitted trap. Hardwired and microprogrammed implementations are equivalent only when their commit/trap traces refine the same architectural model.

### Critical invariants

- Every reachable control state emits a safe, fully defined control vector.
- At most the permitted architectural destination and external side effect are enabled.
- Dispatch selects an entry compatible with the decoded instruction and privilege/context.
- Conditional branches test the intended, temporally valid flag or handshake.
- A microinstruction cannot request mutually conflicting uses of a shared resource.
- Wait loops hold transaction payload and suppress duplicate acceptance or commit.
- Microcalls and returns preserve bounded, valid return state.
- Illegal state/address/ECC conditions enter a defined recovery or trap path.
- Patches are authenticated, version-compatible, atomic and auditable before activation.
- Every accepted instruction eventually commits or traps under stated response assumptions.

### Common failures

Common failures include equating hardwired with combinational, treating microcode as firmware or ISA code, leaving unused controls as don't-cares, dispatching on incompletely validated decode, testing stale flags, incrementing `uPC` during a wait, issuing a store on every wait-loop cycle, overflowing a micro-return stack, allowing a fall-through into another routine, patching only one core, accepting incompatible patch revisions, exposing partially updated control words, assuming writable control is automatically field-updatable, comparing only ROM bits instead of timing/verification, and using microcode to conceal an ISA or protocol violation.

### Compact example

An illustrative 256-word horizontal store has 36 datapath-control bits plus 12 sequencing bits: 12,288 bits (1,536 bytes). Encoding mutually exclusive functions into 22 datapath bits reduces the word to 34 bits and the store to 8,704 bits (1,088 bytes), a 29.17% reduction, but adds decode logic. Under invented delays and instruction mixes, a hardwired design averages 3.25 cycles at 1.25 ns, or 4.06 ns/instruction; a microcoded design averages 3.70 cycles at 1.32 ns, or 4.88 ns/instruction. These numbers establish arithmetic, not a universal ranking.

### Connections

Control organization connects finite-state machines, multicycle datapaths, ISA refinement, control-flow graphs, memory protocols, exceptions, formal equivalence, synthesis, update trust, security response, observability and later pipeline control.

## Governing Question

The datapath supplies possible movements and operations. The controller decides which are allowed now, what internal state follows, and when an architectural instruction completes. A wrong enable can corrupt state even if every datapath component is individually correct.

Hardwired and microprogrammed control are representations for the same sequencing responsibility. Neither representation removes the need for a precise transition contract. The decision concerns instruction complexity, timing, area, change policy, assurance and operational lifecycle.

## Why This Matters

Simple instruction subsets often map cleanly to compact hardwired logic. Irregular or long sequences can be easier to express and inspect as control-store programs. Real processors may hardwire common paths and invoke sequenced assists for rarer operations.

Control is also a trust boundary. It governs memory requests, privilege transitions, faults and commit. Writable control creates a powerful update surface; immutable control turns mistakes into silicon or bitstream changes. Both require evidence tied to exact implementations.

The visible label can mislead. Synthesis may transform a case-statement FSM into a ROM-like network, while a nominal microcode table may become gates. Reason about behavior, timing and update authority, not source-code aesthetics.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace instruction paths through a multicycle datapath;
- construct and verify finite-state machines;
- distinguish architectural from microarchitectural state;
- interpret ready/valid or request/response interfaces;
- explain precise commit and exception behavior.

Retrieve the exact ISA/profile/extensions; decode legality and priority; instruction-class entry points; architectural commit/trap model; datapath control inventory and active polarity; resource-conflict table; hardwired equations or RTL; state encoding; control-store image, format, depth and ECC/parity; sequencer rules; dispatch tables; condition sources and validity; microcall depth; reset entry; interrupt/fault priority; memory and iterative-unit protocols; patch format, signing roots, version matrix, anti-rollback, activation and per-core synchronization; debug/trace visibility; synthesis/STA/area/power reports; formal properties/equivalence mappings; tests and coverage; hardware/errata results; and exact source, generator, tool, library and build identities.

## Learning Objectives

After completing this module, you should be able to:

1. express control generation as a transition function independent of implementation form;
2. design a safe hardwired FSM with explicit defaults and priorities;
3. specify a microinstruction format and control-store sequencer;
4. compare horizontal, vertical and two-level encodings;
5. construct dispatch, branch, wait and micro-subroutine behavior;
6. prevent duplicate effects and stale-condition decisions;
7. define precise exception, interrupt and reset control paths;
8. evaluate timing, storage, area, energy and verification trade-offs;
9. specify secure, compatible and atomic patch lifecycle requirements;
10. verify controller refinement and bounded progress against an ISA model.

## Core Exposition

### Start from a control contract

List every datapath control: mux choices, ALU function, register enables, PC source/write, instruction/intermediate captures, memory request fields, byte enables and commit/trap indicators. Specify active polarity and safe inactive value.

Then define legal combinations. A single word may select exactly one ALU source, but independent captures may occur together if timing and semantics allow. Resource constraints belong in machine-checkable assertions where possible.

### Hardwired control is state plus logic

A multicycle hardwired controller stores a state encoding and computes the next state and outputs from that state, decoded instruction and environment conditions. “Hardwired” does not mean stateless.

Moore-style outputs depend mainly on registered state; Mealy-style outputs may respond directly to inputs. Mealy paths can save a state but extend timing and risk glitches if external controls are not registered or protocol-safe.

### Use complete defaults

Default all writes and requests inactive, then enable only those proven for the selected state and instruction. Define next state for every encoding. Unspecified HDL branches can infer latches, propagate unknowns or let synthesis choose unsafe behavior.

Illegal state recovery should suppress side effects before entering reset/trap/recovery. Merely assigning a legal next state does not make the current cycle safe.

### Decode once, but validate it

Decode may produce an instruction class and attributes such as destination use, memory size, signedness and privilege requirements. The controller should not act on a class until encoding legality and extension availability are established.

Priority among reset, fatal integrity error, synchronous fault, accepted interrupt, response completion and normal sequencing must be explicit. Different priorities can change architectural traces.

### Microinstructions encode the same controls

A microinstruction commonly contains datapath-control fields plus sequencing fields. Direct bits can drive enables; encoded fields select one of several operations. Sequencing fields can mean next, jump, conditional branch, dispatch, call, return, wait or terminal commit.

Document every reserved encoding. Treat invalid control words as integrity failures rather than convenient no-ops unless the architecture explicitly requires otherwise.

### Choose horizontal or vertical encoding deliberately

Horizontal encoding spends bits to expose parallel controls directly. It can reduce decode depth and make concurrent actions obvious, but wide stores consume routing and storage.

Vertical encoding groups mutually exclusive operations. It saves bits and may simplify authoring, but local decoders add delay and can obscure illegal cross-field combinations. The true cost comes from synthesized implementation, not source-level bit counts alone.

### Dispatch enters a routine

A dispatch table maps validated instruction class, mode or event to a microprogram entry. A default illegal-instruction entry is safer than an accidental alias.

If dispatch depends on privilege, extension state or operand conditions, include those inputs in the table contract or branch within a common checked prologue. Record which choice is timing-critical.

### Sequence ordinary steps

An ALU routine may capture operands, execute, write back and commit. A load adds effective-address generation, request/wait, response capture and writeback. A store separates request acceptance from architectural completion according to the memory contract.

Each microstep states what values it consumes, which values it creates, their valid lifetime and whether any effect is externally visible. Comments such as “do load” are too weak for review.

### Branch on valid conditions

Conditional sequencing may inspect ALU flags, decode properties, memory ready/error, iteration done or privilege state. Specify when each condition becomes valid and whether it is registered.

A branch that reads a flag in the same cycle it is produced creates a combined control/datapath path. Capturing the flag first may cost a cycle but simplify timing and proof.

### Wait without repeating effects

When a request has not yet been accepted, hold its payload stable if the protocol requires it. Once accepted, record outstanding state and stop creating new requests. A wait-loop back edge must not reassert a one-shot store as a new transaction.

Responses must match the outstanding operation or tag. Error and success are terminal alternatives, not two controls that may both fire.

### Reuse micro-subroutines carefully

Micro-subroutines can share effective-address, normalization or exception-entry sequences. They require a return-address register or stack with explicit maximum depth and integrity behavior.

Avoid hidden calling conventions. Specify inputs, clobbered intermediate registers, return values, possible traps and whether interrupts may be accepted inside the routine.

### Two-level control can share patterns

A first-level microinstruction may index a nanostore containing common datapath patterns. This reduces repeated wide words at the cost of another lookup, indirection and verification boundary.

Compression wins should be measured after implementation. Added store access or routing can dominate saved bits on a target technology.

### Define commit explicitly

Terminal microinstructions must identify which architectural changes become visible. Register write, final PC, flags and trap state must correspond to one ISA transition.

Stores may become externally visible before a later internal terminal state. Then the proof must define the store-acceptance event as part of commit or guarantee faults/interrupts cannot create an imprecise suffix.

### Handle exceptions precisely

Synchronous faults belong to the current instruction. Suppress its uncommitted destination writes, preserve the correct faulting PC and cause, and enter the trap sequence once.

A control-store integrity error is not automatically an ISA exception. Define whether it causes machine-check, reset, containment or fail-stop behavior and what evidence remains trustworthy.

### Accept interrupts at named boundaries

Interrupt policy may sample only between instructions or at selected restartable microstates. If a long routine is interruptible, preserve enough microarchitectural state to resume or restart without duplicated effects.

Latency claims must include the longest noninterruptible sequence, outstanding transaction policy, priority masking and synchronization delay.

### Reset every internal state

Reset selects a known control entry, disables writes/requests and invalidates outstanding/intermediate state. If the external protocol cannot cancel a request, reset recovery must drain or tag late responses safely.

Writable control storage may need loading and integrity checking before instruction fetch. The core must not execute partially initialized words.

### Treat patches as privileged artifacts

Some platforms provide vendor-controlled microcode updates. That operational mechanism is implementation-specific; a classroom writable control store does not imply the same capability.

A patch system needs authenticated provenance, target/revision compatibility, anti-rollback policy, atomic activation, all-core coordination, failure recovery, measurement/attestation and observability. Updating one logical CPU while siblings run can violate system assumptions.

### Separate patch policy from ISA correctness

A patch can correct implementation behavior or mitigate a vulnerability, but validation must still show conformance for the exact updated image. “Latest” is not a proof and version numbers alone do not express applicability.

Updates can change performance counters, timing or feature availability. Operations need rollout cohorts, health signals, rollback rules and retained evidence.

### Model timing paths

Hardwired timing can include decode, state logic, priority muxing and high-fanout control distribution. Microprogrammed timing can include control-store access, field decode, condition selection and next-address logic.

Control and datapath paths interact. A mux select must arrive before its data setup deadline; a same-cycle flag-to-branch path may span datapath and sequencer. Use STA on the implemented netlist under declared constraints.

### Model cycle count and storage

For instruction classes `i` with fractions `p_i` and cycles `C_i`, `CPI_avg = sum_i p_i C_i`, including expected stalls. Mean time is `CPI_avg * T_clk`.

For a rectangular control store with depth `D` and word width `W`, raw capacity is `D*W` bits. ECC, tags, patch indirection, unused holes, decoders and physical macros change the realized cost.

### Compare verification surfaces

Hardwired logic requires state-transition, decode-priority and control-vector proof. Microcode adds address reachability, fall-through, branches, microcall discipline, image generation, integrity and possibly update verification.

Microcode can make sequences more legible and patchable; it can also create many control words and hidden paths. Measure coverage over semantic states, instructions, conditions and terminal effects rather than line count.

### Use an independent architectural oracle

At instruction acceptance, snapshot architectural pre-state and decoded instruction. Hide finite noncommit cycles. At commit or trap, compare state and event trace with an independent ISA model.

For two implementations, relational equivalence can align different numbers of internal steps at their commit boundaries. Do not require cycle-by-cycle equality when the representations deliberately differ.

### Prove progress under assumptions

Safety alone allows a controller to wait forever. State assumptions such as eventual memory response and eventual iterative-unit completion, then prove each accepted instruction reaches commit, trap or defined reset containment.

Use a ranking argument for acyclic routines and bounded counters. For wait loops, isolate the fairness assumption and prove the controller remains stable and side-effect-free while waiting.

### Observe semantic state

Expose safe debug signals such as decoded class, semantic control state, `uPC`, outstanding flag, commit/trap reason and image version. Preserve encoding maps for synthesized state recoding.

Trace must not leak secrets or create functional dependence on debug. Production access requires authorization and lifecycle policy.

### Gather layered evidence

Use lint and structural checks; unit tests per state/word; protocol assertions; illegal-state/address and integrity fault injection; instruction and exception suites; differential ISA testing; formal safety/liveness/refinement; synthesis/STA/power/area; update-signature and rollback tests; multicore activation tests; FPGA/silicon traces; workload measurements; and errata review.

Bind evidence to exact RTL, control-store source and binary digest, generator, patch, synthesis constraints, tools, libraries, hardware revision and configuration. A passing old image does not validate a changed image.

## Definitions and Notation

- `d`: validated decoded instruction/event attributes.
- `u`, `u'`: current and next hardwired state or microaddress.
- `f`: condition inputs, flags, handshakes and fault indications.
- `c`: complete datapath/control vector for one internal step.
- `H(d,u,f)`: hardwired output and next-state function.
- `M[u]=(c,b)`: control-store word containing controls and sequencing field `b`.
- `Q(b,d,f)`: microsequencer next-address function.
- `D`, `W`: control-store depth and word width.
- `p_i`, `C_i`: workload fraction and cycles for instruction class `i`.
- `T_clk`: implemented clock period.
- **noncommit step**: internal transition with no new architectural instruction effect.
- **terminal step**: commit, precise trap or defined containment transition.
- **fall-through**: default progression to the next sequential microaddress.
- **field decode**: logic expanding an encoded microinstruction field into controls.
- **control image identity**: digest/version/applicability data naming exact microcode content.

## Mechanisms, Invariants, or Proof Structure

1. **Control-vector obligation:** every reachable state/word produces defined controls with safe inactive defaults.
2. **Decode obligation:** only legal, available instruction/event classes reach their intended entry.
3. **Resource obligation:** emitted controls never demand incompatible simultaneous resource uses.
4. **Intermediate-validity obligation:** every consumed operand, flag and response was created for the current instruction and remains valid.
5. **Sequencing obligation:** each branch, dispatch, fall-through, call and return targets a valid semantic state.
6. **Request obligation:** stalled payloads remain stable and each logical transaction is accepted at most once.
7. **Response obligation:** only the matching outstanding operation consumes a success/error response once.
8. **Write obligation:** register, PC and memory effects occur only at authorized states with correct masks/data.
9. **Commit obligation:** a terminal normal path equals exactly one permitted ISA transition.
10. **Exception obligation:** a fault suppresses younger/uncommitted effects and creates the precise permitted trap.
11. **Interrupt obligation:** acceptance occurs only at declared restartable boundaries with bounded stated latency.
12. **Reset/integrity obligation:** every internal state, illegal encoding and corrupt word reaches safe defined behavior without stray effects.
13. **Progress obligation:** under declared fairness, every accepted instruction reaches commit/trap/containment.
14. **Timing obligation:** implemented control, datapath and combined paths meet setup/hold and interface constraints at all corners.
15. **Image/evidence obligation:** generated or patched control content is authentic, compatible, atomically activated and bound to reproducible evidence.

## Alternatives and Trade-Offs

1. **Hardwired versus microprogrammed:** direct logic can be fast and compact for regular control; stored sequencing can organize complex flows.
2. **Pure versus hybrid:** one representation simplifies ownership; fast paths plus assists can optimize common and rare cases but add boundaries.
3. **Moore versus Mealy:** registered-state outputs simplify timing; input-dependent outputs may save states but add paths and glitch concerns.
4. **One-hot versus encoded state:** one-hot eases decode and debug; compact encoding saves flops and may add logic.
5. **Horizontal versus vertical microcode:** direct fields expose parallelism; encoded fields save store width and add decode.
6. **Single versus two-level store:** one lookup is simpler; a nanostore shares patterns but adds indirection.
7. **Fall-through versus explicit next address:** fall-through saves bits; explicit targets ease relocation and auditing.
8. **Inline sequence versus microcall:** inline control is local; subroutines reduce duplication and require return discipline.
9. **Registered versus same-cycle conditions:** registered flags simplify timing; same-cycle conditions may reduce CPI.
10. **ROM-like versus writable store:** immutability narrows attack surface; writability supports fixes but demands secure lifecycle controls.
11. **Global versus per-core activation:** global rendezvous improves uniformity; per-core mechanisms simplify hardware but expose mixed-version risk.
12. **Restart versus resume after interrupt:** restart reduces saved state if effects are replay-safe; resume reduces repeated work and adds checkpoint state.
13. **Dense addressing versus reserved holes:** density saves storage; reserved regions can support growth and containment.
14. **Parity versus ECC:** parity detects some corruption cheaply; ECC may correct but costs bits, latency and validation.
15. **Representation proof versus end-to-end refinement:** local equivalence is tractable; architectural refinement covers composition and interfaces.

## Failure Modes and Misconceptions

1. “Hardwired means no FSM.” Multicycle hardwired control has registered state.
2. “Microcode is assembly language.” Implementation microinstructions are normally below and hidden from the ISA.
3. “CISC means microcoded.” ISA style does not dictate one control implementation.
4. “RISC means hardwired.” RISC implementations can use sequenced assists.
5. “A case statement proves hardwired hardware.” Synthesis chooses the physical network.
6. “A ROM declaration proves a physical ROM.” Mapping depends on technology and tools.
7. “Microcode is automatically patchable.” The store may be immutable or lack a secure update path.
8. “Patchable means safer.” Update authority and parsing add attack and failure surfaces.
9. “Unused controls can be don't-cares.” They can create unsafe synthesis choices and obscure proof.
10. “Illegal states recover on the next cycle.” Current-cycle controls may already cause damage.
11. “Dispatch only needs opcode.” Legality, mode, extensions and subfields may matter.
12. “Wait means repeat the same word.” Reassertion can duplicate accepted side effects.
13. “Ready is always a registered condition.” Same-cycle handshakes can extend timing paths.
14. “A stale flag is harmless.” It can choose the wrong routine path.
15. “Fall-through is obvious.” Layout edits can silently enter another routine.
16. “Microcalls are free.” Return storage, depth and interrupt behavior require proof.
17. “Smaller control store means smaller design.” Decoders, routing and macros determine realized cost.
18. “Fewer cycles means faster.” Clock period and stalls also determine time.
19. “Microcode fixes any hardware bug.” It cannot repair inaccessible datapaths or all timing/electrical defects.
20. “Newest patch fits every processor.” Applicability is model/revision/configuration-specific.
21. “Version equality proves uniform behavior.” Image, activation state and configuration also matter.
22. “Updating the boot CPU updates all cores.” Per-core application and hotplug behavior must be verified.
23. “Signature validity proves correctness.” It proves authorized origin under a key policy, not functional suitability.
24. “Simulation proves no hangs.” Liveness across arbitrary waits needs assumptions and stronger evidence.
25. “Cycle-by-cycle equality is required.” Commit-aligned stuttering refinement permits different internal schedules.
26. “Microcode hides architectural effects.” External requests and commit/trap traces remain observable and must conform.

## Worked Examples

### Example 1

A hardwired load FSM uses decode, address, request/wait and writeback states. The request state sets an outstanding bit only on acceptance; the wait state keeps writes inactive until the matching response arrives.

### Example 2

A microcoded load routine dispatches to address calculation, emits a request word, conditionally loops on response absence, captures data, writes the destination and terminates. The loop branches without reissuing an accepted request.

### Example 3

A vertical ALU field encodes add/subtract/and/or/shift. Its decoder reduces control-store width but lies on the select-arrival timing path, so synthesis and STA decide whether the encoding wins.

### Example 4

An illegal hardwired state defaults all enables low and enters a containment state. An assertion proves no memory request, register write or PC write is active for every illegal encoding.

### Example 5

A micro-routine calls a shared effective-address helper. A two-entry return stack is insufficient for a new nested helper, so static call-graph analysis rejects the image before generation.

### Example 6

A divide assist is interruptible only before start and after done. Worst-case interrupt latency therefore includes its bounded iterations; a later design adds restartable checkpoints and proves no partial result can commit twice.

### Example 7

A patch image is signed but targets a different stepping. Compatibility checking rejects it before rendezvousing cores, demonstrating that authentication and applicability are separate gates.

### Example 8

An ECC error on control-store read suppresses the decoded control vector and enters machine-check containment. Using the corrupted word for one cycle before trapping would not be safe recovery.

### Example 9

Hardwired and microcoded cores take different internal cycle counts for a store. A relational checker aligns instruction acceptance and commit events, then compares memory event, PC and trap traces rather than microstates.

### Example 10

The following deterministic model compares raw control-store encodings and invented performance inputs.

<!-- bijux-verify: {"id":"control-organization-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"horizontal_bits=12288 bytes=1536\nvertical_bits=8704 bytes=1088 reduction_pct=29.17\nhardwired_period_ns=1.25 average_cpi=3.25 mean_instruction_ns=4.06 ideal_mips=246.15\nmicrocoded_period_ns=1.32 average_cpi=3.70 mean_instruction_ns=4.88 ideal_mips=204.75\n"}} -->
```python
depth = 256
horizontal_datapath_bits = 36
sequencer_bits = 12
vertical_fields = {
    "operation": 6,
    "source": 4,
    "destination": 4,
    "memory": 3,
    "misc": 5,
}

horizontal_width = horizontal_datapath_bits + sequencer_bits
vertical_width = sum(vertical_fields.values()) + sequencer_bits
horizontal_bits = depth * horizontal_width
vertical_bits = depth * vertical_width
reduction = 100 * (horizontal_bits - vertical_bits) / horizontal_bits

mix = {"alu": 0.50, "load": 0.25, "store": 0.10, "branch": 0.10, "jump": 0.05}
hardwired_cycles = {"alu": 3, "load": 4, "store": 3, "branch": 3, "jump": 3}
microcoded_cycles = {"alu": 3, "load": 5, "store": 4, "branch": 4, "jump": 3}
hardwired_period = 1.25
microcoded_period = max(1.25, 0.86 + 0.26 + 0.20)

def performance(cycles, period):
    cpi = sum(mix[k] * cycles[k] for k in mix)
    mean_ns = cpi * period
    return cpi, mean_ns, 1000 / mean_ns

h_cpi, h_ns, h_mips = performance(hardwired_cycles, hardwired_period)
m_cpi, m_ns, m_mips = performance(microcoded_cycles, microcoded_period)

print(f"horizontal_bits={horizontal_bits} bytes={horizontal_bits // 8}")
print(f"vertical_bits={vertical_bits} bytes={vertical_bits // 8} reduction_pct={reduction:.2f}")
print(f"hardwired_period_ns={hardwired_period:.2f} average_cpi={h_cpi:.2f} mean_instruction_ns={h_ns:.2f} ideal_mips={h_mips:.2f}")
print(f"microcoded_period_ns={microcoded_period:.2f} average_cpi={m_cpi:.2f} mean_instruction_ns={m_ns:.2f} ideal_mips={m_mips:.2f}")
```

The expected output is recorded in the verification annotation. The inputs are synthetic. Real decisions require implemented storage, decoding, control distribution, stalls, workloads, update machinery and assurance costs.

## Cross-Program Connections

- **Digital Logic:** controller state, decode and integrity logic compile to gates, flops and memories.
- **Programming Languages:** microprogram control flow has branches, calls, dataflow and static-analysis concerns.
- **Software Engineering Patterns:** generated images, schemas, compatibility and review ownership need durable interfaces.
- **Operating Systems:** platform microcode loading coordinates early boot, CPUs, hotplug, versions and policy.
- **Security Engineering:** writable control is a privileged update and supply-chain boundary.
- **Formal Methods:** safety, liveness and stuttering refinement connect microsteps to ISA transitions.
- **Performance Engineering:** clock period, CPI, instruction mix, stalls, area and energy require measured models.
- **Systems Engineering:** update rollout, rollback, observability and independent assurance span hardware and operations.

## References

1. RISC-V International, “RV32I Base Integer Instruction Set,” current unprivileged ISA reference. https://docs.riscv.org/reference/isa/unpriv/rv32.html
2. lowRISC, “Ibex Instruction Decode and Execute,” current core reference. https://ibex-core.readthedocs.io/en/latest/03_reference/instruction_decode_execute.html
3. lowRISC, “Ibex Exceptions and Interrupts,” current core reference. https://ibex-core.readthedocs.io/en/latest/03_reference/exception_interrupts.html
4. Linux Kernel documentation, “The Linux Microcode Loader.” https://docs.kernel.org/arch/x86/microcode.html
5. YosysHQ, “PicoRV32,” current open RTL implementation and configuration documentation. https://github.com/YosysHQ/picorv32
6. YosysHQ, “FSM handling,” current synthesis documentation. https://yosyshq.readthedocs.io/projects/yosys/en/latest/using_yosys/synthesis/fsm.html
7. RISC-V International, “Sail RISC-V Model,” current executable ISA semantics. https://github.com/riscv/sail-riscv
8. Nand to Tetris, “Project 5: Computer Architecture,” current educational CPU/control construction resource. https://www.nand2tetris.org/project05

## Exercises

### Exercise 1

Specify hardwired control for ALU, load and store instructions over a shared multicycle datapath. Include safe defaults, states, conditions, resource constraints, commit and fault behavior.

### Exercise 2

Translate the same three instruction classes into a microinstruction format and routines. Define dispatch, field encoding, next-address behavior, waits and invalid-word handling.

### Exercise 3

Design a request/wait/response micro-routine for a variable-latency memory. Prove it cannot duplicate a store or consume a stale load response under arbitrary stalls.

### Exercise 4

Compare horizontal and vertical stores at depth 256 using the executable model. Then explain why raw bit count and ideal throughput are insufficient for a product decision.

### Exercise 5

Write an assurance plan for a field-patchable control store in a multicore processor. Cover trust, compatibility, activation, rollback, verification and evidence boundaries.

## Answers to the Exercises

### Answer 1

Use fetch/decode plus ALU execute/writeback, load address/request-wait/writeback and store address/request-complete states. Default register, PC, memory and intermediate enables inactive. Decode only legal classes. Each state consumes valid instruction-owned operands and schedules the shared ALU/port once.

Record acceptance before waiting, match responses, update the destination only on successful load response, and define store commit at the protocol's accepted/complete boundary. Illegal state, response error and decode fault suppress normal writes and enter precise trap or containment. Prove all paths terminate under eventual response.

### Answer 2

One format can contain source selects, ALU function, destination/write enables, memory fields and sequencing kind/condition/target. Dispatch legal ALU/load/store classes to named entries and everything else to illegal-instruction handling. Use explicit targets at routine boundaries and a conditional wait branch.

Reserve encodings and addresses; an invalid word suppresses its controls and enters integrity containment. Generate the image and a semantic listing from one schema, validate branch targets and unreachable/fall-through regions, then bind the binary digest to tests and refinement evidence.

### Answer 3

Use idle, request, wait and response states plus outstanding identity. Before acceptance, keep request valid and payload stable. On the one acceptance event, set outstanding and transition so the request word cannot create another logical transaction. Consume only a matching success/error response once.

For stores, specify whether response marks commit and prohibit retry unless the protocol proves replay safety. For loads, capture data only from the matched response and enable architectural writeback later. Assert stability, at-most-one acceptance, response matching, one terminal event and eventual completion under fairness; inject reset at every state.

### Answer 4

The model gives 12,288 horizontal bits and 8,704 vertical bits, a 29.17% raw reduction. Its invented mix yields 4.06 ns per hardwired instruction and 4.88 ns per microcoded instruction. Recompute these from width, depth, weighted CPI and period rather than accepting the labels.

A real choice also needs mapped macro/gate area, field-decode and routing timing, combined flag/control paths, stalls, workload distributions, power, generator complexity, formal/test coverage, debug, patch lifecycle and defect cost. The example provides no universal ranking.

### Answer 5

Define signed image provenance, protected roots, target model/stepping/features, monotonic/rollback policy, parser limits and preactivation integrity. Coordinate all online and hotplug cores at a safe boundary; prevent partial words or mixed unsupported versions; preserve recovery if activation fails; measure exact active identity.

Test authorized/unauthorized, compatible/incompatible, corrupt, interrupted and rollback cases. Re-run ISA differential, safety/liveness/refinement, exception/interrupt, protocol, performance and multicore stress evidence on the exact image. Separate signature validity from functional correctness and vendor assertions from independent review. Name hardware, ISA, microarchitecture, RTL, OS, security, operations, formal and independent-assurance owners. This plan makes no certification claim.
