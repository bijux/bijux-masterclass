---
module_id: CA-029
program: Computer Architecture
level: 1
module_number: 29
title: Precise Exceptions
status: complete
last_verified: 2026-09-04
---

# Precise Exceptions

## One-Page Review

### Governing question

When an instruction faults amid overlapped, speculative or variable-latency execution, how can the processor expose an architectural state equal to a legal sequential prefix, identify the exact boundary and cause, suppress the faulting instruction's prohibited effects, and restart or terminate predictably?

### Essential definitions

- An **exception** is a synchronous event attributed to the execution of a particular instruction.
- An **interrupt** is an asynchronous request accepted at an architecturally defined boundary.
- A **trap** is the transfer of control and state caused by an exception or interrupt under the architecture's rules.
- A **precise exception** exposes a state in which all older permitted instructions have completed, the faulting instruction has not performed prohibited ordinary effects, and no younger instruction has completed architecturally.
- The **faulting instruction** is the instruction to which the synchronous exception is attributed.
- A **trap cause** identifies the architectural event class.
- An **exception PC** records the architecture-specified instruction boundary for handler return or diagnosis.
- **trap value** is architecture-defined auxiliary information such as a faulting address or instruction bits.
- A **committed prefix** is the maximal in-order sequence of architectural instruction effects preceding the trap boundary.
- A **killed suffix** is the set of younger in-flight work prevented from architectural completion.
- A **restartable exception** permits corrected state and trap return to retry or continue according to architectural rules.
- A **fatal/contained fault** enters reset, machine-check or another defined terminal/recovery state rather than ordinary retry.
- **exception priority** selects among multiple fault indications for one instruction or simultaneous in-flight candidates.
- A **retirement boundary** is where instruction effects become architecturally irrevocable in order.
- **imprecise state** cannot be represented as the specified sequential prefix because younger effects or missing older effects are visible.

### Central model, mechanism, or theorem

Let the initial architectural state be `S0` and program-order instructions be `I0...`. If `Ik` is selected as the faulting instruction, precision requires visible state `Sk=Exec(I_{k-1},...Exec(I0,S0))`, plus architecture-defined trap updates `Trap(Sk, pc_k, cause, tval)`. Ordinary effects of `Ik` that the exception forbids and every younger `I_j, j>k`, are absent. Internal work may finish in any allowed schedule, but commit selection must preserve this prefix. In an in-order pipeline this follows age-based flush and gated side effects; wider/out-of-order designs commonly buffer results until ordered retirement.

### Critical invariants

- Every in-flight token carries instruction identity, PC and sufficient exception metadata.
- Fault detection is attached to the instruction that caused it, not merely the detecting stage.
- The selected synchronous fault is the oldest architecturally eligible faulting instruction.
- For one instruction, cause priority matches the exact ISA/profile and operation phase.
- All older permitted instructions form a complete committed prefix before trap state becomes visible.
- The faulting instruction cannot perform prohibited register, memory, PC or control-state effects.
- Younger instructions cannot commit, store, forward into surviving work or overwrite trap metadata.
- Accepted irreversible effects are ordered so they cannot make a later-discovered older fault imprecise.
- Trap PC, cause, value, privilege/status and vector target update atomically under the architectural rule.
- Return from trap restores only validated state and cannot revive stale pipeline or request tokens.

### Common failures

Common failures include equating precise with fast, flushing without preserving older completion, using the detection-stage PC, letting a younger early fault beat an older late fault, choosing arbitrary cause priority, writing a destination before a later fault, issuing a store before all older exceptions are ruled out, forwarding from a faulting producer, losing fault metadata during a stall, accepting an interrupt ahead of an older synchronous exception, recording the next PC instead of the faulting PC, treating every machine integrity error as an ISA exception, double-taking a replayed fault, and testing only one exception at a time.

### Compact example

Suppose tokens 40–44 are in flight and tokens 40–41 already form the next committable prefix. Token 42, at PC `0x1008`, reports a load access fault while younger token 43 reports illegal instruction and an interrupt is pending. Ordered selection chooses token 42: commit prefix `[40,41]`, suppress token 42's load destination, kill `[43,44]`, write exception PC `0x1008` and cause, then redirect to the configured handler. The younger fault and interrupt may be reconsidered only after architectural recovery; they cannot change this boundary.

### Connections

Precise exceptions connect ISA trap semantics, pipeline age/flush control, memory ordering, privilege state, virtual memory, interrupts/debug, reorder buffers, verification refinement, operating-system recovery and safety/security containment.

## Governing Question

Execution hardware discovers faults at different times. Decode can find an illegal instruction early; a load may fault after translation or memory response; an older divide may finish much later. Detection time cannot replace program order.

The architectural contract requires a coherent boundary understandable to software. A handler must see a state corresponding to completed older instructions and an identified faulting instruction, not a mixture caused by pipeline timing.

## Why This Matters

Operating systems rely on precise page faults to install mappings and retry. Debuggers, signals, virtualization and security monitors rely on exact PCs and causes. Imprecise stores or register writes can make recovery impossible.

Speculation and variable latency widen the gap between execution completion and architectural order. Designs need explicit commit/retirement even if a simple pipeline can make writeback and commit coincide.

Not every internal failure is recoverable as an ordinary exception. Integrity errors, timeout and uncorrectable corruption require a containment policy that preserves only claims the remaining evidence supports.

## Prerequisites and Retrieval

Before studying this module, be able to:

- describe sequential ISA state transitions;
- trace valid/age-tagged pipeline tokens and commit;
- distinguish stalls, flushes, replay and redirects;
- explain memory request acceptance and side effects;
- distinguish synchronous exceptions from interrupts.

Retrieve exact unprivileged/privileged ISA version, profile and extensions; exception/interrupt cause table and priority; PC/tval/status/vector/delegation rules; restart/return semantics; instruction PC/length; pipeline and commit organization; token age/identity; exception detection point per cause; memory translation/protection/alignment/cache/bus error mapping; store visibility boundary; CSR/control-state effects; long/optional units; fault metadata path; flush/stall/replay priority; outstanding request cancellation/tags; interrupt/debug/reset/NMI/integrity policy; virtualization/delegation; formal ISA model and refinement mapping; directed/random tests and coverage; OS/hypervisor tests; synthesis/STA; hardware/errata; and exact RTL/configuration/firmware/tool/library/revision data.

## Learning Objectives

After completing this module, you should be able to:

1. define precision as an architectural sequential-prefix property;
2. distinguish exception detection, selection, retirement and trap entry;
3. derive oldest-fault and within-instruction cause priority;
4. carry exact PC, cause, value and privilege metadata through stalls;
5. suppress faulting/younger effects while completing permitted older work;
6. integrate memory faults, stores, long units, replay, interrupts and debug;
7. define restart, trap return and fatal containment boundaries;
8. compare in-order gating with reorder-buffer retirement;
9. verify trap traces against an independent architectural model;
10. bind precision claims to exact configuration and adversarial evidence.

## Core Exposition

### Define the sequential prefix first

Write the architectural transition sequence independent of the pipeline. Precision means trap state is derived from one boundary between instructions, with the architecture's rule for whether the faulting instruction is retried or skipped.

Do not define precision as “all pipeline registers cleared.” Flushing is an implementation mechanism; prefix state is the observable requirement.

### Distinguish detection from selection

A stage detects a condition: illegal encoding, misalignment, permission failure, access error or arithmetic event. Detection records metadata on the responsible token.

Selection waits until program-order/priority logic can determine which architectural event wins. A younger early detection cannot preempt an older later-detected fault.

### Carry the instruction PC

Every token needs its own architectural instruction address and, where relevant, length. The current fetch PC may refer to a younger path and is unsuitable for a fault detected later.

Carry or reconstruct exact faulting instruction bits only under a proven mapping. Compressed/variable-length decoding changes the sequential PC and possible trap value.

### Carry cause and trap value

Exception metadata travels with valid identity through stalls, queues and replays. Trap value may contain an address, instruction or zero depending on cause and ISA rules.

Never combine PC from one token with cause/address from another. Bundle coherence is a first-class invariant.

### Define cause priority within an instruction

One instruction can trigger several candidate checks. Architecture may prioritize instruction-address faults, illegal encoding, breakpoints, address misalignment, page/access faults or other classes in a specified order.

Implement the exact applicable specification. “First stage that noticed” is not a portable priority rule.

### Select the oldest fault across instructions

In an in-order pipeline, later stage often implies older age, but detached units, replay and queues can violate a simple stage order. Use explicit sequence identity where needed.

If an older instruction is still capable of faulting, a younger irreversible effect must wait or be held speculative/recoverable.

### Complete the older prefix

Older instructions may already have committed. Remaining older instructions either finish before trap entry or are represented in an ordered retirement structure that commits them first.

A global immediate flush that discards an older valid result creates a missing prefix effect and is not precise.

### Suppress the faulting ordinary effects

For a fault-before-completion instruction, disable its normal destination write, memory effect, PC/link update and ordinary CSR modification as required. Trap-state writes are separate authorized effects.

Some architecture-defined operations can have partial or reported effects; precision must follow their explicit semantics rather than assume universal all-or-nothing behavior.

### Kill the younger suffix

Invalidate younger tokens before they forward to surviving operations, issue irreversible effects, train state contrary to policy, write back or retire. Already accepted cancellable/nondestructive work may be drained/discarded with tags.

For non-cancellable work, retain ownership until completion and suppress its architectural result. Do not reuse identity while a late response can alias.

### Define the store visibility boundary

Stores are the classic precision challenge because memory effects may become externally visible. An in-order design can delay store request/commit until all older faults are resolved and the store is architecturally next.

A store buffer may hold speculative data privately, but drain to coherence/device memory only under ordered commit rules. Device and non-idempotent regions need especially strict treatment.

### Treat loads as value plus possible fault

A load result is not definitive until translation, permission, alignment, access response and required data transformation succeed. Do not forward ordinary data from a load that will fault.

Younger consumers normally die with the load's precise exception. Speculative value use requires recovery/security analysis beyond basic precision.

### Handle long and variable operations

Divide, accelerator or cache-miss completion may arrive after younger instructions have executed. Track tag, age, destination and possible fault until ordered retirement.

If an operation is noninterruptible, document latency. If restartable/cancellable, prove repeated work cannot duplicate effects.

### Use in-order pipeline priority

For a simple pipeline, allow older downstream stages to commit, mark the faulting token, hold/kill as necessary, suppress its normal write and invalidate younger stages. Then write trap state and redirect.

Write a simultaneous-event table. Older fault, younger branch redirect, memory response, stall and interrupt can coincide.

### Use a reorder buffer for wider execution

Out-of-order execution records results and exceptions in program-order entries. Instructions may execute/finish out of order, but only the head commits architectural effects.

When a faulting entry reaches the head, all older entries have committed; the head's ordinary effect is suppressed, younger entries are flushed and trap entry occurs. ROB correctness depends on allocation, tags, wrap, store ordering and recovery.

### Separate completion and retirement

Completion means execution produced a result/fault. Retirement means the instruction becomes architecturally irrevocable in order. A completed younger instruction remains speculative until retirement.

Counters and debug should distinguish executed, completed, killed and retired events. Only retired instructions form the architectural prefix.

### Integrate interrupts

An interrupt is pending asynchronously but accepted at a defined architectural boundary. A synchronous fault on the next retiring instruction normally has architecture-defined priority over an interrupt at a different boundary.

Record the specified resume PC and status. Interrupt latency includes drain/noninterruptible work, synchronization and masking, not merely vector redirection.

### Integrate debug and breakpoints

Debug triggers can be defined before/after instruction effects and may have special priority. Single-step must stop at an exact architectural boundary with no younger commit.

Preserve distinction among breakpoint exception, debug mode entry and external halt request. Their resume and privilege rules differ.

### Integrate reset, NMI and integrity faults

Reset may discard architectural continuity under its platform contract. NMI or machine-check may have stronger priority and weaker restart guarantees than ordinary traps.

State explicitly which architectural registers/memory effects are trustworthy after uncorrectable control/data corruption. Do not label containment precise unless the prefix property is actually preserved.

### Compute the trap vector

Trap entry writes architecture-defined exception PC, cause, trap value and status/privilege fields, then selects direct/vectored handler address under delegation rules. Validate alignment and mode semantics.

These updates form one architectural trap transition. Partial CSR update visible with the old PC is invalid.

### Return from trap safely

Trap return restores privilege/interrupt status and next PC according to the architecture. Software may adjust exception PC before return to retry or skip under cause-specific policy.

Flush stale handler/user pipeline state as needed and revalidate fetch context. Trap return cannot resurrect pre-trap tokens or outstanding responses.

### Handle nested traps

A handler can itself fault or receive an interrupt depending on masking/delegation. Hardware supplies specified stacking/status behavior; software must preserve additional state.

Double-fault or critical-error behavior needs a bounded containment path. Infinite recursive trapping is not recovery.

### Define replay identity

If a transient condition replays an instruction internally without architectural trap, retain one instruction identity and ensure no prior irreversible effect occurred. A later architectural fault is reported once for that identity.

Counters, predictor training and requests need exactly-once or explicitly speculative rules across replay.

### Verify architectural refinement

Snapshot pre-state and compare the commit/trap event trace against an independent ISA model. At a trap, verify exact committed prefix, faulting PC/cause/value/status/vector and absence of younger effects.

Use symbolic ages and simultaneous faults so detection order varies independently from program order.

### Verify liveness and containment

Under eventual older completion and memory response assumptions, a selected fault must eventually reach trap entry. A pipeline that holds forever remains safe-looking but unusable.

For fatal errors, prove bounded transition to the documented contained state and suppression of untrusted effects; liveness target may be reset/alert rather than handler execution.

### Measure exception cost carefully

Separate detection-to-trap, handler service, recovery/retry, cache/TLB disturbance and return-to-useful-retirement. Exception frequency and cause distribution dominate averages.

Page fault service is largely software/storage behavior; a short hardware trap entry does not make it cheap. Preserve raw distributions and platform identity.

### Gather layered evidence

Use per-cause directed tests, simultaneous older/younger faults, load/store/device cases, stalls/replay/late responses, interrupt/debug/reset/NMI priority, nested traps, privilege/delegation/virtualization, random fault injection, symbolic-prefix assertions, ISA differential testing, formal safety/liveness/refinement, OS/hypervisor suites, synthesis/STA, hardware traces and errata.

Bind evidence to exact ISA/spec revision, RTL/configuration, memories/protocols, firmware, OS/hypervisor, constraints, tools/libraries, binaries/seeds, hardware and errata. Precision in one subset/mode does not validate all configured causes.

## Definitions and Notation

- `S0`: architectural state before the considered instruction sequence.
- `I_i`: instruction at program-order index `i`.
- `S_k`: state after exactly instructions older than `I_k` have executed.
- `pc_k`: architectural address of candidate faulting instruction `I_k`.
- `cause_k`, `tval_k`: selected cause and auxiliary value for `I_k`.
- `Trap(S_k,...)`: architecture-defined atomic trap-state transition.
- `age(i)`: program-order identity used for selection and suffix kill.
- `head`: oldest unretired entry in an ordered retirement structure.
- **detection:** observation of a possible exception condition.
- **selection:** architectural priority decision choosing one event/boundary.
- **completion:** internal result or exception becomes known.
- **retirement:** ordered architectural effect becomes irrevocable.
- **prefix property:** visible state equals effects of exactly an initial program-order subsequence.
- **restart:** handler return causes the faulting or following instruction to execute per ISA/software policy.
- **containment:** transition limiting effects after a fault whose normal correctness evidence is no longer trusted.

## Mechanisms, Invariants, or Proof Structure

1. **Semantics obligation:** every configured cause, PC, tval, status and vector rule matches the exact ISA/profile/mode.
2. **Identity obligation:** each detection remains coherently attached to its instruction PC, age and operation.
3. **Within-instruction priority obligation:** simultaneous cause candidates for one instruction select the specified cause.
4. **Across-instruction priority obligation:** the oldest eligible synchronous fault wins regardless of detection time.
5. **Prefix obligation:** every permitted older instruction and no younger instruction has architecturally completed at trap entry.
6. **Faulting-effect obligation:** prohibited ordinary effects of the selected instruction are absent.
7. **Younger-effect obligation:** killed suffix tokens cannot write, store, forward, redirect, train impermissibly or retire.
8. **Memory obligation:** stores/device effects and load faults respect the precise visibility boundary.
9. **Outstanding obligation:** killed non-cancellable work remains tagged and late responses cannot alias/revive state.
10. **Trap-state obligation:** PC, cause, value, status, delegation and handler address update as one permitted transition.
11. **Interrupt/debug obligation:** asynchronous/debug events use defined boundaries and priority relative to synchronous faults.
12. **Replay/return obligation:** replay and trap return cannot duplicate effects or resurrect stale tokens.
13. **Progress/containment obligation:** under assumptions, selected faults reach handler or documented fatal containment finitely.
14. **Refinement obligation:** commit/trap traces match an independent sequential architectural model.
15. **Evidence obligation:** precision claims cover exact configured causes, protocols, privilege modes and implementation identity.

## Alternatives and Trade-Offs

1. **Immediate flush versus ordered drain:** immediate recovery is fast; ordered drain preserves prefix when older work remains.
2. **Writeback-as-commit versus separate retirement:** coincidence is compact in simple cores; separation supports variable/out-of-order completion.
3. **Distributed versus centralized fault metadata:** local detection is timely; centralized selection makes age/priority explicit.
4. **Stage position versus sequence age:** stage order is cheap in simple pipelines; explicit IDs handle queues/replay.
5. **Early versus late checks:** early faults reduce wasted work; late checks may use definitive information.
6. **Block versus speculate past old uncertainty:** blocking simplifies precision; speculation improves overlap with buffering/recovery.
7. **Store-at-memory versus store-at-retirement:** early issue reduces latency; ordered commit preserves precision and needs buffering.
8. **Cancel versus drain younger operations:** cancellation saves work if supported; drain/discard handles non-cancellable units.
9. **Retry versus report trap:** internal retry hides transients; trap exposes software-manageable state and cost.
10. **Interruptible versus noninterruptible long operation:** interruption lowers latency; restart/checkpoint complexity grows.
11. **Direct versus vectored handler:** direct entry centralizes dispatch; vectored entry reduces some dispatch time with more address rules.
12. **Hardware versus software save:** hardware reduces entry work; software keeps architectural state smaller/flexible.
13. **Precise recovery versus fatal containment:** recovery preserves service; containment is safer when state trust is lost.
14. **Commit-time versus execute-time counters:** commit counters reflect architectural work; execute counters expose speculative activity.
15. **Lower trap latency versus simpler critical paths:** early selection can improve response while adding priority/routing timing.

## Failure Modes and Misconceptions

1. “Precise means detected immediately.” Precision concerns visible architectural boundary.
2. “Flushing the pipeline proves precision.” Older required effects may be lost or younger effects already visible.
3. “The detecting stage identifies the oldest fault.” Program order, not stage timing, decides.
4. “The first signal to assert wins.” ISA cause/age priority governs selection.
5. “Use current fetch PC for exception PC.” Fetch usually points at younger work.
6. “Next PC is always the saved PC.” Cause/architecture determines resume boundary.
7. “A faulting instruction writes then traps.” Prohibited ordinary effects must be suppressed.
8. “Younger register writes are the only concern.” Stores, redirects, training and forwarding also matter.
9. “A load value is usable before fault status.” The ordinary result is not definitive.
10. “A speculative store can always be undone.” External/device effects may be irreversible.
11. “A store buffer alone proves precision.” Drain/ordering and error rules are essential.
12. “Later pipeline stage always means older.” Detached/replayed operations break that shortcut.
13. “Completion equals retirement.” Out-of-order/variable execution separates them.
14. “A ROB automatically gives precise exceptions.” Allocation, head, stores, tags and recovery need proof.
15. “Interrupts are instruction exceptions.” They are accepted asynchronous events at defined boundaries.
16. “Pending interrupt beats any fault.” Exact architectural priority/boundary applies.
17. “Debug halt is just an interrupt.” Entry/resume semantics can differ.
18. “Reset is a precise trap.” Reset may intentionally abandon continuity.
19. “Every integrity error can be restarted.” Corruption may invalidate prefix evidence.
20. “Replay is invisible automatically.” Requests, counters and updates can duplicate.
21. “Returning from trap restores the old pipeline.” Only architectural state is resumed; stale tokens remain dead.
22. “One exception test covers priority.” Simultaneous and age-reversed cases are required.
23. “ISA tests prove device/store precision.” Interface visibility and platform behavior require evidence.
24. “Short hardware entry means cheap exception.” Handler and recovery dominate many causes.
25. “Safety properties prove handler entry.” Deadlock can preserve safety forever.
26. “Precision in machine mode proves every mode.” Delegation, virtualization and extensions change rules.

## Worked Examples

### Example 1

An illegal instruction in decode waits behind an older load whose response is pending; if that load later faults, its older exception wins.

### Example 2

A load access fault carries its own PC/address through a memory stall. Trap entry uses that bundle, not current fetch state.

### Example 3

A faulting arithmetic instruction suppresses its destination write; younger consumers are killed and cannot forward its computed bits.

### Example 4

A store remains private in a store buffer until it reaches ordered commit. An older fault discards the younger entry before external visibility.

### Example 5

A non-cancellable younger divide returns after trap selection. Its killed tag consumes the response without writeback, then releases safely.

### Example 6

A ROB records a younger completed illegal instruction, but the head load later reports a page fault; the head fault retires as trap first.

### Example 7

A synchronous breakpoint and pending interrupt coincide at a boundary. The exact privileged/debug specification selects the event and saved PC.

### Example 8

Trap return after a repaired page mapping retries the faulting load from saved exception PC; no old load token or response is resurrected.

### Example 9

An uncorrectable control-state error enters documented fatal containment rather than claiming a restartable precise ISA exception.

### Example 10

This deterministic model demonstrates oldest-fault selection and architectural prefix/suffix formation.

<!-- bijux-verify: {"id":"precise-exception-prefix-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"faulting_seq=42 cause=load_access_fault\ncommitted_prefix=[40, 41] killed_suffix=[43, 44]\ntrap_pc=0x00001008 handler_pc=0x00000100\nordinary_writes_suppressed=[42, 43, 44] interrupt_deferred=True\n"}} -->
```python
inflight = [
    {"seq": 40, "pc": 0x1000, "fault": None},
    {"seq": 41, "pc": 0x1004, "fault": None},
    {"seq": 42, "pc": 0x1008, "fault": "load_access_fault"},
    {"seq": 43, "pc": 0x100C, "fault": "illegal_instruction"},
    {"seq": 44, "pc": 0x1010, "fault": None},
]
faulting = min((token for token in inflight if token["fault"]), key=lambda token: token["seq"])
prefix = [token["seq"] for token in inflight if token["seq"] < faulting["seq"]]
suffix = [token["seq"] for token in inflight if token["seq"] > faulting["seq"]]
suppressed = [token["seq"] for token in inflight if token["seq"] >= faulting["seq"]]
handler_pc = 0x100
interrupt_pending = True

print(f"faulting_seq={faulting['seq']} cause={faulting['fault']}")
print(f"committed_prefix={prefix} killed_suffix={suffix}")
print(f"trap_pc=0x{faulting['pc']:08x} handler_pc=0x{handler_pc:08x}")
print(f"ordinary_writes_suppressed={suppressed} interrupt_deferred={interrupt_pending}")
```

The model establishes ordering arithmetic only. Actual cause priority, CSR names, vector calculation and interrupt policy come from the exact ISA/privilege configuration.

## Cross-Program Connections

- **ISA:** exception PC, cause, auxiliary value, status and return define the observable contract.
- **Operating Systems:** page faults, signals and recovery depend on restartable precise state.
- **Virtualization:** delegation and guest/host trap state add privilege boundaries.
- **Data Structures:** ROBs, store buffers, tags and queues retain ordered speculative results.
- **Security Engineering:** privilege faults and fatal containment govern effect suppression and trust.
- **Formal Methods:** prefix refinement, oldest-fault selection and liveness express precision directly.
- **Performance Engineering:** cause frequency, entry/service/retry latency and cache disturbance determine cost.
- **Systems Engineering:** hardware, firmware, OS, handler and errata evidence jointly support recovery claims.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), current instruction, faulting-PC and exception semantics; retrieved 2026-09-04.
2. RISC-V International, [Machine-Level ISA](https://docs.riscv.org/reference/isa/priv/machine.html), current machine trap, cause, status, vector and return semantics; retrieved 2026-09-04.
3. RISC-V International, [Supervisor-Level ISA](https://docs.riscv.org/reference/isa/priv/supervisor.html), current supervisor traps, delegation and virtual-memory fault semantics; retrieved 2026-09-04.
4. lowRISC, [Ibex Exceptions and Interrupts](https://ibex-core.readthedocs.io/en/latest/03_reference/exception_interrupts.html), current open-core priority and control behavior; retrieved 2026-09-04.
5. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), current integrated core security, alert and verification context; retrieved 2026-09-04.
6. Berkeley Architecture Research, [BOOM Reorder Buffer](https://docs.boom-core.org/en/latest/sections/reorder-buffer.html), current open out-of-order retirement and exception concepts; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), pipeline/exception teaching resources; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), independent executable architectural trap semantics; retrieved 2026-09-04.

## Exercises

### Exercise 1

Define precise architectural state for a five-instruction window where the third instruction faults and younger instructions have executed but not retired.

### Exercise 2

Design exception metadata and priority for illegal instruction, load misalignment, page fault, access fault and pending interrupt in an in-order pipeline.

### Exercise 3

Explain how a store buffer and a reorder buffer preserve precision when loads, stores and long arithmetic complete out of order.

### Exercise 4

Extend the executable model with two candidate causes on token 42 and implement an explicit within-instruction priority table.

### Exercise 5

Write a verification plan for precise exceptions across privilege modes, replay, reset/debug and non-cancellable interfaces.

## Answers to the Exercises

### Answer 1

Let instructions one and two form the complete committed prefix. Architectural state equals sequential execution through instruction two. Instruction three's prohibited ordinary destination/memory/PC effects are absent; trap state records its specified PC/cause/value/status and handler target. Instructions four/five have no architectural effect despite internal execution.

Kill or invalidate the younger suffix, retain tags for non-cancellable physical work, and prevent forwarding/training/late responses from reviving it. Trap return starts from architecture/software-selected PC, not old pipeline state.

### Answer 2

Each token carries valid, age, instruction PC/bits, address, detected cause bits and candidate tval. Decode legality, alignment, translation/permission and access response set candidates at their definitive points. A per-instruction priority encoder follows the exact configured ISA, not stage order.

Across instructions select the oldest eligible fault. Older synchronous fault dominates a younger one; interrupt is accepted only at its defined boundary after synchronous priority. Hold metadata through stalls, suppress the selected token's ordinary writes, kill younger tokens and atomically update trap state/vector.

### Answer 3

The ROB allocates program-order entries containing destination/result or fault. Execution may complete out of order, but retirement proceeds only at the head. A head fault suppresses its ordinary update and flushes younger entries after all older head entries committed.

Stores remain in ordered private entries until their ROB instruction commits; only then may they become externally visible under memory-order rules. Loads may execute early but a fault/result remains speculative. Long operations return by tag; killed completions are discarded without tag alias. ROB/store-buffer fullness and recovery need liveness proof.

### Answer 4

Represent each token's fault candidates as a set and define a cause-rank map copied from the exact ISA/profile, for example only after verifying whether misalignment or page/access fault has priority for that implementation/architecture allowance. Select `min(candidates,key=rank)` within token, then choose the minimum-age faulting token across tokens.

Keep priority data versioned with the cited specification and generate directed pairs for every simultaneous candidate. The printed prefix/suffix remain determined by token 42; only selected cause/tval may change.

### Answer 5

Create a cause/mode/delegation matrix with expected PC, tval, status, vector, return and priority. Directed tests cover every cause plus pairwise/multi-cause, older-late versus younger-early, stores/device effects, long units, replay, late responses, nested traps, interrupts, debug, reset/NMI and fatal integrity errors.

Use symbolic ages and a shadow ISA to assert exact committed prefix, selected fault, suppressed faulting/younger effects, coherent metadata, tag safety, one trap and progress/containment under assumptions. Run OS/hypervisor suites, differential testing, formal refinement, synthesis/STA and hardware fault injection. Bind exact specs, RTL/config, protocols, firmware/software, tools, seeds, hardware and errata. Internal evidence is not independent certification.
