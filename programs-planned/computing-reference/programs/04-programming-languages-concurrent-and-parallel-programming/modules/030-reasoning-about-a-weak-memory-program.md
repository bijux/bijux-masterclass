---
module_id: CONPAR-030
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 30
title: Reasoning About a Weak-Memory Program
status: complete
last_verified: 2026-08-29
---

# Reasoning About a Weak-Memory Program

## One-Page Review

### Governing question

Given a concurrent program and a proposed result, how can we decide whether an exact language or architecture memory model permits that execution—and repair the program without relying on interleaving intuition?

### Essential definitions

- An **event** is one modeled read, write, RMW, fence, lock, or other relevant action.
- A **candidate execution** assigns events, read values, and relations for one proposed outcome.
- **Sequenced-before (sb)** orders relevant events within one source-level agent.
- **Reads-from (rf)** maps each read to the write whose value it observes.
- **Modification order (mo)** orders modifications of one atomic object.
- **From-read (fr)** relates a read to modifications later than its rf source in that object's mo.
- **Synchronizes-with (sw)** is a model-defined cross-agent edge, often conditioned on rf.
- **Happens-before (hb)** is the transitive closure of sb and sw.
- A **litmus test** is a minimal concurrent program asking whether selected outcomes are permitted or observed.
- A **repair** adds or changes a semantic edge, state representation, or ownership boundary so every prohibited production outcome is excluded.

### Central model, mechanism, or theorem

Reasoning is constraint solving: fix one model; normalize the program into events; propose rf and mo for the outcome; derive fr, sw, hb, coherence, and any SC order; then check every model axiom and data-race rule. A candidate is allowed only if all constraints hold. An execution seen on hardware is evidence of possibility for that build/target; an unseen execution is not proof of prohibition.

### Critical invariants

The named model and version are explicit. Source-language reasoning precedes compiler/ISA mapping. Every read has a justified source. Every atomic object's mo is total. RMWs are indivisible. sw is created only by a qualifying observation. Conflicting ordinary accesses are hb-ordered or the program is rejected under its language rules. SC operations satisfy their additional common-order constraints. Initial values, widths, dependencies, fences, failure paths, object lifetime, and compiler transformations are modeled. The repair closes the actual missing relation.

### Common failures

Engineers enumerate only source interleavings; assume wall-clock order; let a read observe a value with no write; draw sw without rf; ignore initial writes or fr; merge per-object mo into a fictitious global order; reason about assembly while source has a data race; assume x86 observations prove portability; use a stress test to prove impossibility; strengthen an unrelated atomic; add a fence without its pairing rule; or repair a litmus outcome while leaving lifecycle/reclamation invalid.

### Compact example

Store buffering starts `x=y=0`. Thread 0 stores `x=1` then loads `y`; thread 1 stores `y=1` then loads `x`. Candidate result `r0=r1=0` creates SC constraints `Wx< Ry< Wy< Rx< Wx`, a cycle, so SC forbids it. Relaxed source/target models may permit it because they do not require that one global order. This does not imply every language/architecture or ordinary-racy spelling permits it.

### Connections

[Sequential Consistency in Shared Memory](022-sequential-consistency-in-shared-memory.md), [Happens-Before Relations](023-happens-before-relations.md), [Acquire and Release Ordering](027-acquire-and-release-ordering.md), and [Relaxed Atomics](028-relaxed-atomics.md) supply the relations. The [program roadmap](../ROADMAP.md) next moves to asynchronous execution.

## Governing Question

How can engineers turn source, a surprising observed or hypothesized result, and a named memory model into an auditable execution graph—and select a repair whose correctness follows from the graph rather than from stronger-hardware luck?

Weak-memory reasoning is not guessing which instruction “ran first.” It is checking whether a relational execution satisfies an exact specification.

## Why This Matters

Lock-free structures, publication flags, counters, queues, reference counts, device interfaces, and compiler-generated atomics all run under models weaker than a single intuitive interleaving. A result can be legal even though no source-line total order explains it. Conversely, an appealing graph can violate coherence, RMW atomicity, hb, or an SC constraint.

The cost of informal reasoning is high. Bugs can disappear under logging, occur only on another architecture, or remain latent until a compiler optimization. “Works on x86” cannot validate C++ with a data race. “Thread sanitizer is clean” cannot prove a relaxed algorithm has its intended invariant. “Never saw both zero” cannot establish that both zero is forbidden.

A repeatable graph method makes assumptions reviewable. It also focuses repairs: release/acquire when publication is missing, one atomic representation when a compound invariant is missing, a lock when ownership is unclear, or lifecycle/reclamation when the memory order was never the true defect.

## Prerequisites and Retrieval

Retrieve:

- reordering layers from [Compiler and Processor Reordering](021-compiler-and-processor-reordering.md);
- SC total-order constraints from [Sequential Consistency in Shared Memory](022-sequential-consistency-in-shared-memory.md);
- sb, sw, and hb from [Happens-Before Relations](023-happens-before-relations.md);
- construction and lifetime from [Visibility and Publication](024-visibility-and-publication.md);
- mo and RMW from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- failure paths from [Compare-and-Swap Loops](026-compare-and-swap-loops.md);
- release/acquire rf conditions from [Acquire and Release Ordering](027-acquire-and-release-ordering.md); and
- relaxed independence from [Relaxed Atomics](028-relaxed-atomics.md).

Retrieval prompt: for a release store and acquire load on one flag, name the observation needed to derive sw and the ordinary accesses hb then protects.

## Learning Objectives

After completing this module, a learner can:

1. choose and name the relevant source or architecture model;
2. normalize a small concurrent program into events;
3. construct rf, mo, fr, sw, hb, and SC-order candidates;
4. reject candidates with race, coherence, cycle, value, or RMW violations;
5. analyze store-buffering and message-passing outcomes;
6. distinguish model simulation, hardware litmus testing, stress, and race detection;
7. validate compiler/ISA mappings without replacing source proof;
8. derive a minimal semantic repair and test its scope; and
9. state where lifetime, progress, devices, and external effects require additional models.

## Core Exposition

### Choose the model before the graph

“Weak memory” names a family, not one specification. Possible targets include:

- the C++ abstract machine at a named draft/standard;
- Rust atomic API guarantees plus the applicable evolving language model;
- the Java Memory Model;
- the Go memory model;
- an AArch64, RISC-V, x86-TSO, GPU, or device architecture model;
- the Linux Kernel Memory Model; or
- a library abstraction with its own contract.

Source and architecture questions differ. First ask whether the source program is defined and which outcomes its language allows. Then ask whether the compiler mapping preserves that contract and which ISA executions implement it. Architecture strength cannot rescue undefined source behavior.

Record tool/model revision. Release-sequence, dependency, mixed-size, and fence details can change or differ.

### Normalize events

Reduce the relevant fragment to named events:

- `Ix0`: initialize x to 0
- `T0.Wx1`: thread 0 stores x=1
- `T0.Ry`: thread 0 loads y
- `Iy0`: initialize y to 0
- `T1.Wy1`: thread 1 stores y=1
- `T1.Rx`: thread 1 loads x

Keep type, atomicity, width, ordering mode, address, and returned value. Treat RMW as one event with read and write aspects. Include fences, failed CAS reads, object lifetime start/end, and compiler-visible dependencies when relevant.

Remove unrelated computation only after showing it cannot affect control, address, data dependency, synchronization, lifetime, or observable behavior.

### Program order is partial

sb orders events within one thread as the language specifies:

`T0.Wx1 sb→ T0.Ry` and `T1.Wy1 sb→ T1.Rx`.

It does not order events across threads. Drawing thread 0's store before thread 1's load on paper adds no cross-thread relation.

Compilers preserve the abstract machine's permitted behavior, not the visual instruction order. Architecture models may use program order plus preserved-order subsets rather than the language's sb. Use the vocabulary of the chosen layer.

### Assign reads-from

Every read value must come from a compatible write in the candidate model. For both-zero store buffering:

`Iy0 rf→ T0.Ry` and `Ix0 rf→ T1.Rx`.

This is the decisive outcome choice. For a result of one, the corresponding load reads from the other thread's store instead.

Do not say “the load missed the store” without specifying rf. Check address, width, value, atomic object, lifetime, and whether the language permits that source.

### Assign modification order

Each atomic object's modifications have a total mo. Here:

`Ix0 mo→ T0.Wx1` and `Iy0 mo→ T1.Wy1`.

mo is per object; it is not one total order across x and y. For three or more writes, enumerate candidate orders consistent with the model's constraints.

An RMW must read the immediately relevant preceding value required by its atomic semantics and insert one indivisible modification. A candidate that lets two CAS successes consume the same current state may violate RMW atomicity.

### Derive from-read

If read `R` takes its value from write `W` and later modification `W'` follows `W` in mo, then `R fr→ W'` in common axiomatic notation. In store buffering:

`T0.Ry fr→ T1.Wy1` and `T1.Rx fr→ T0.Wx1`.

fr makes “read the old value before this later write” explicit. It is derived from rf and mo; it is not an independent story about wall time.

Exact relation names and axioms vary, but the reasoning obligation remains: old-value reads constrain their relationship to later modifications.

### Derive synchronization and hb

For a release/acquire pair, sw exists only when the acquire reads from the release or a qualifying language-defined sequence. Then hb closes transitively over sb and sw.

With relaxed store buffering, cross-thread rf from an initialization normally creates no release/acquire sw. hb contains the within-thread sb edges, not a global order between the threads.

For ordinary conflicting memory, check the language's race rule. In C++, two potentially concurrent conflicting ordinary accesses with neither hb-before the other create a data race and undefined behavior. Do not continue enumerating “weak outcomes” as though atomic-model constraints governed a racy program.

### Apply coherence constraints

Coherence prevents arbitrary histories for one atomic object. Common obligations relate:

- write-write order;
- write-read observations;
- read-read progression;
- read-before-later-write (fr); and
- RMW placement.

Do not reduce coherence to “all threads instantly see the newest value.” It is relational and model-specific. A later numeric value can be smaller due to program writes or wrap.

When an outcome seems magical, draw rf, mo, and fr for each object. Cycles forbidden by the selected model often become visible.

### Add SC constraints

SC atomics participate in an additional language-defined common order consistent with required relations. For both-zero store buffering, any SC explanation needs:

- `Wx1 < Ry` by thread 0
- `Ry < Wy1` because Ry reads y's initial value
- `Wy1 < Rx` by thread 1
- `Rx < Wx1` because Rx reads x's initial value

The cycle makes the outcome impossible under the relevant SC model. Under relaxed ordering, absence of that one common order can permit it, subject to all remaining axioms.

Do not infer that replacing one of four operations with SC necessarily closes the cycle. Check the exact mixed-order rules.

### Message passing

Producer writes ordinary payload, then release-stores flag one. Consumer acquire-loads flag and reads payload only after observing one.

For the positive candidate:

`Wpayload sb→ Srelease rf→ Lacquire sb→ Rpayload`.

The rf qualifies release/acquire sw, so `Wpayload hb→ Rpayload`. For a candidate where the acquire sees zero, sw from the release is absent and consumer must not read payload.

This analysis shows why “acquire load exists” is not enough and why strengthening an unrelated counter cannot repair publication.

### Store buffering as a litmus test

Store buffering is valuable because it separates SC interleaving intuition from relaxed execution constraints. It is not a production algorithm.

Ask four outcomes: (0,0), (0,1), (1,0), (1,1). For each, assign rf and test the model. A simulator can enumerate them. Hardware litmus runs can report observations on a compiled ISA spelling.

An observed (0,0) shows possibility for that environment. Zero observations after a billion trials do not show prohibition; scheduling and microarchitecture may make an allowed execution rare.

### Other classic patterns

**Load buffering** puts loads before stores and raises dependency/speculation/out-of-thin-air questions. Do not transfer conclusions from store buffering.

**IRIW** (independent reads of independent writes) tests whether observers can disagree on write order across objects. Results depend strongly on model and operation modes.

**Dekker-style mutual exclusion** uses flags and turn state; weakening operations without a full proof can admit both entrants or destroy progress.

**Publication** tests payload/flag causality. **RWC/WRC** patterns test causal chains. Use canonical names only after matching exact event shapes.

### Dependencies are not universal synchronization

Address, data, and control dependencies can constrain some architecture executions. Compilers can transform dependencies under source rules. C++ consume semantics have a complex history. An acquire operation is often the maintainable source-level choice when payload publication is intended.

Do not rely on a branch, function call, volatile access, opaque-looking arithmetic, or inline assembly as a portable dependency barrier without normative support. A dependency in an ISA litmus test is not automatically preserved from high-level source.

### Fences require pairing

A fence has no value to read. Its synchronization depends on surrounding atomic operations and exact rf/mo rules. To analyze a fence:

1. name the release-side and acquire-side fence/operation;
2. identify the atomic carrier modifications and observations;
3. apply the model's fence synchronization rule;
4. derive hb for protected ordinary events; and
5. check every alternative rf candidate.

“Fence between them” is not a graph. Prefer direct acquire/release operations unless splitting value and ordering is required and proved.

### CAS success and failure

Successful CAS is an RMW with a modification. Failure is a read-only observation. Candidate graphs must use the success and failure orderings actually supplied.

A failed CAS can acquire published data if its witness is used and its failure ordering permits it. It cannot release because no desired write occurred. Weak CAS may fail spuriously; a spurious failure has no intervening modification to blame.

Retry loops add multiple events per logical call. Recompute desired from each witness and place external effects after successful commitment.

### Compilation and architecture

After proving source semantics, inspect optimized output for every supported compiler/target. Confirm atomic width, instruction selection, barriers, dependencies, ABI, and library calls. An operation can be implemented by a lock.

Then use the architecture model to analyze the emitted event pattern. A compiler mapping proof connects layers; assembly inspection alone is not the source proof.

Mixed-language and FFI programs need compatible atomic objects, alignment, lifetime, and memory-model contracts. “Both compile to the same instruction” does not establish cross-language semantics.

### Tools and their scopes

`herd7` is a generic simulator for executable memory models; `litmus7` runs architecture litmus tests; `diy7` generates tests. The model file, tool version, initial state, event spelling, and queried condition are part of evidence.

Language-specific model checkers, exhaustive schedulers, and libraries such as Loom cover their documented subsets. Read limitations: some tools approximate atomics, omit compiler behavior, bound executions, or model one language version.

Race detectors find some runtime data races; they do not validate all atomic-order protocols. Stress tests exercise integration; they do not prove forbidden outcomes. Formal/manual graph review and empirical tools are complementary.

### Repair selection

Repair the missing guarantee:

- missing payload hb: release/acquire on the actual carrier or a higher-level handoff;
- missing compound atomicity: one lock, packed state, immutable root, or transaction;
- stale CAS: witness refresh and recomputation;
- ambiguous reuse: generation plus lifetime/reclamation;
- true sharing/contention: shard, batch, or change ownership;
- progress/fairness: blocking/wakeup/scheduling protocol;
- device/durability: platform barriers, flushes, acknowledgements, and recovery.

Re-run the complete outcome analysis after repair. Stronger ordering can exclude one outcome while leaving wrap, cancellation, or lifetime broken.

### Production review

Extract minimal litmus cases from production code, but preserve the mapping:

- source lines to events;
- state invariants to queried outcomes;
- compiler flags/targets to mappings;
- lifecycle and allocation to object identity;
- failures/cancellation to alternative traces.

Keep a regression litmus/model test when tools are stable. Also keep end-to-end tests and target stress. A tiny model proves only the abstraction represented.

## Definitions and Notation

For candidate execution `E`, let:

- `Ev` be events;
- `sb` be source sequenced-before;
- `rf ⊆ W×R` assign read sources;
- `mo_x` totally order atomic modifications of object x;
- `fr = rf^{-1};mo` restricted appropriately to later modifications;
- `sw` be model-defined synchronization; and
- `hb=(sb∪sw)^+`.

A data-race check examines conflicting non-atomic/lifetime events not ordered by hb under the selected language. Additional predicates enforce atomic coherence, RMW atomicity, dependencies, fences, and SC order.

“Allowed” means `E` satisfies every applicable axiom—not that it is frequent. “Forbidden” means no candidate for the outcome satisfies them—not merely that a test did not observe it.

## Mechanisms, Invariants, or Proof Structure

Use this worksheet:

1. **Name the model, revision, and layer.**
2. **State initial values, types, widths, atomicity, lifetime, and queried outcome.**
3. **Enumerate events** including failed paths, fences, and RMW halves.
4. **Add sb/program-order relations.**
5. **Assign rf** for every read and validate value/address compatibility.
6. **Choose one total mo per atomic object.**
7. **Derive fr, sw, hb, coherence, dependency, and fence relations.**
8. **Check ordinary conflicts and lifetime races.**
9. **Construct/check SC or other model-specific global constraints.**
10. **Reject or accept the candidate with the first decisive axiom and full audit.**
11. **Use tools with recorded model/version; test hardware only as empirical evidence.**
12. **Repair the missing relation/ownership and repeat all candidates.**

The executable model constructs the four ordering constraints required to explain store-buffering both-zero under one SC total order and finds their cycle.

<!-- bijux-verify: {"id":"store-buffering-sc-cycle-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"events=4\nsc_constraints=4\ncycle_detected=True\nsc_both_zero_allowed=False\nrelaxed_common_order_required=False\nrelaxed_candidate_decided_by_full_model=True\n","stderr":""}} -->
```python
events = 4
write_x = 0
read_y = 1
write_y = 2
read_x = 3

before = [[False] * events for row in range(events)]
before[write_x][read_y] = True
before[read_y][write_y] = True
before[write_y][read_x] = True
before[read_x][write_x] = True

for middle in range(events):
    for source in range(events):
        for target in range(events):
            if before[source][middle] and before[middle][target]:
                before[source][target] = True

cycle = False
for event in range(events):
    if before[event][event]:
        cycle = True

print(f"events={events}")
print("sc_constraints=4")
print(f"cycle_detected={cycle}")
print(f"sc_both_zero_allowed={not cycle}")
print("relaxed_common_order_required=False")
print("relaxed_candidate_decided_by_full_model=True")
```

Limitations: this graph proves only that four stated constraints cannot coexist in a strict total order. It does not implement the C++, Rust, Java, Go, x86, Arm, RISC-V, GPU, or Linux memory models; determine whether a relaxed candidate is allowed; execute threads; model compilers, rf/mo/fr, dependencies, mixed widths, fences, races, RMWs, devices, or lifetime; or measure an outcome.

## Alternatives and Trade-Offs

**SC atomics** reduce allowed outcomes through a common order and can simplify review, but do not fix non-atomic races, compound state, lifetime, or progress.

**Acquire/release** supplies directed publication with fewer global constraints, requiring exact rf-based proof.

**Relaxed atomics** are appropriate for independent per-object claims and expose more executions.

**Mutexes/channels/once/futures** package synchronization with ownership, waiting, or lifecycle and often reduce graph surface.

**Packed/immutable state** makes compound observations one atomic representation at encoding and reclamation cost.

**Formal model simulation** exhaustively checks bounded litmus candidates against a selected model; production abstraction and tool fidelity remain.

**Hardware litmus/stress** reveals implemented behavior and mapping errors but cannot prove an allowed outcome impossible.

**Race detectors/systematic schedulers** find complementary defects but cover only their runtime/model scope.

## Failure Modes and Misconceptions

1. **Concurrency is all interleavings.** Weak models admit executions not captured by one source-line total order.
2. **Weak means arbitrary.** Exact axioms still constrain values and relations.
3. **A read can choose any value.** It needs a permitted write/source.
4. **mo is a global order.** It is per atomic object.
5. **Wall-clock order creates hb.** Only model-defined relations do.
6. **Acquire always synchronizes.** It must make a qualifying observation.
7. **A data-racy C++ program has interesting weak outcomes.** Undefined behavior invalidates that analysis.
8. **Both-zero is allowed everywhere.** Model, modes, and spelling decide.
9. **SC on one operation makes the program SC.** Mixed-mode constraints require analysis.
10. **A fence globally flushes memory.** It needs a normative pairing.
11. **A branch is portable synchronization.** Dependencies are layer/model-specific.
12. **CAS failure has release semantics.** It performs no desired write.
13. **x86 success proves source correctness.** Compiler/language and portability remain.
14. **An unobserved stress outcome is forbidden.** Rarity is not impossibility.
15. **Race-detector silence proves atomic protocol correctness.** It does not.
16. **A litmus simulator proves production.** Abstraction and lifecycle mapping must be justified.
17. **Stronger ordering solves ABA/reclamation.** Identity and lifetime are separate.
18. **CPU hb orders devices/durability.** Platform protocols are separate.

## Worked Examples

### Example 1

**Situation.** Store-buffering relaxed atomics produce both-zero.

**Reasoning.** Each read takes its initial write; per-object mo puts initialization before the thread store. No SC common-order cycle is required by relaxed mode, subject to the full selected model.

**Conclusion.** Interleaving intuition alone cannot reject the candidate.

### Example 2

**Situation.** The same four operations are SC.

**Reasoning.** sb and old-value constraints require `Wx<Ry<Wy<Rx<Wx`.

**Conclusion.** The cyclic strict order forbids both-zero under SC.

### Example 3

**Situation.** Acquire load reads zero while producer release-stored one.

**Reasoning.** rf comes from initialization, so no sw edge from producer release; consumer must not read payload.

**Conclusion.** Operation labels without qualifying rf do not publish.

### Example 4

**Situation.** Acquire load reads the producer's release one.

**Reasoning.** release sw acquire; surrounding sb closes payload-write hb payload-read.

**Conclusion.** The candidate safely publishes the protected immutable payload.

### Example 5

**Situation.** Two ordinary C++ fields conflict without hb.

**Reasoning.** The source has a data race. Architecture outcome enumeration cannot define it.

**Conclusion.** Repair source race before ISA analysis.

### Example 6

**Situation.** Two CAS attempts both claim success from one expected state.

**Reasoning.** Successful RMWs occupy mo indivisibly; after one modification, the other's stale comparison cannot also match that state.

**Conclusion.** Reject the candidate by RMW atomicity.

### Example 7

**Situation.** A fence is placed after a relaxed flag load.

**Reasoning.** It orders payload only if the load observed the relevant release carrier and the model's fence rule connects them.

**Conclusion.** Draw carrier rf and normative fence relation.

### Example 8

**Situation.** A billion x86 stress iterations never see an allowed Arm outcome.

**Reasoning.** Different ISA models and mappings apply; non-observation also lacks impossibility force.

**Conclusion.** Simulate the named model and test every supported target.

### Example 9

**Situation.** `herd7` forbids a minimized test under one model file.

**Reasoning.** This is strong bounded evidence for that exact test/model/version, not automatic proof that production maps to it.

**Conclusion.** Preserve event and lifecycle mapping plus complementary tests.

### Example 10

**Situation.** A railway controller's CPU litmus proof is offered as system safety evidence.

**Reasoning.** It does not prove WCET, compiler qualification, MMIO/device order, sensor validity, actuator acknowledgement, hazards, or fault recovery.

**Conclusion.** Named language, architecture, compiler, hardware, real-time, controls, security, domain, quality, and functional-safety reviewers need target evidence; no approval is implied.

## Cross-Program Connections

- **Programming languages:** abstract machines define races, atomics, and allowed executions.
- **Computer architecture:** ISA models, dependencies, barriers, and coherence implement another layer.
- **Formal methods:** axiomatic relations turn outcomes into satisfiability problems.
- **Operating systems:** the Linux kernel uses its own executable memory model and primitives.
- **Distributed systems:** causal graphs are analogous, but shared-memory rf/mo semantics do not transfer directly.
- **Security:** races, stale authorization, speculative effects, and lifetime errors become vulnerabilities.
- **Compilers:** mapping validation connects source orderings to instructions.
- **Safety engineering:** CPU-memory proof is only one system assurance component.

## References

1. Hans-J. Boehm and Sarita V. Adve. “Foundations of the C++ Concurrency Memory Model.” PLDI, 2008.
2. Mark Batty et al. “Mathematizing C++ Concurrency.” POPL, 2011.
3. Jade Alglave, Luc Maranget, and Michael Tautschnig. “Herding Cats: Modelling, Simulation, Testing, and Data Mining for Weak Memory.” TOPLAS 36(2), 2014.
4. Luc Maranget et al. `herdtools7` official repository and documentation. Current revision accessed 2026-08-29.
5. ISO C++ working draft. “Multi-threaded executions and data races; atomic order and consistency.” Current draft accessed 2026-08-29.
6. Oracle. *Java Language Specification*, Java SE 26, section 17.4. 2026.
7. The Go Authors. “The Go Memory Model.” Accessed 2026-08-29.
8. Arm. *Armv8-A Memory Model Guide* and architecture reference material. Accessed 2026-08-29.
9. Intel. *Intel 64 Architecture Memory Ordering White Paper* and Software Developer's Manual. Current versions accessed 2026-08-29.
10. Linux Kernel documentation. “Linux Kernel Memory Model.” Current documentation accessed 2026-08-29.

## Exercises

### Exercise 1

Define event, candidate execution, sb, rf, mo, fr, sw, and hb, and state why the model/revision must be named.

### Exercise 2

For store buffering, derive both-zero rf, mo, fr, and the SC cycle. Explain why the calculation alone does not decide a named relaxed model.

### Exercise 3

Diagnose a C++ publication program with ordinary payload, relaxed ready flag, an acquire fence after the consumer load, and storage freed by another thread. Provide a complete repair.

### Exercise 4

Compare SC atomics, release/acquire, a mutex, a channel, and model checking for a reusable single-slot handoff. Select a design and verification portfolio.

### Exercise 5

An industrial robot shares commands across C++, Rust, and an Arm device using atomics and MMIO. Specify the layered proof, executable evidence, fault tests, and human-review boundary.

## Answers to the Exercises

### Answer 1

An event is one modeled memory/synchronization action. A candidate execution assigns events, observed values, and relations for one outcome. sb orders same-thread source events; rf maps each read to its source write; mo totally orders modifications per atomic object; fr connects an old-value read to later modifications after its rf source; sw is model-defined cross-thread synchronization; hb is the transitive closure of sb and sw.

Models differ in relations, axioms, fence/dependency rules, mixed-size behavior, and revisions. An unqualified “weak memory” verdict is therefore not reproducible.

### Answer 2

Let initial writes be Ix0 and Iy0. Both-zero assigns `Ix0 rf→Rx` and `Iy0 rf→Ry`. Per-object orders are `Ix0 mo→Wx1` and `Iy0 mo→Wy1`. Thus `Rx fr→Wx1` and `Ry fr→Wy1`.

An SC total order must respect `Wx1<Ry` and `Wy1<Rx` from thread order. Reading initial values requires `Ry<Wy1` and `Rx<Wx1`. Together: `Wx1<Ry<Wy1<Rx<Wx1`, impossible.

Relaxed operations do not necessarily require that SC total order. Whether the candidate is allowed still requires the named model's coherence, hb, value, dependency, race, and other axioms. The small cycle model proves only SC-order impossibility.

### Answer 3

The relaxed ready store/load does not publish payload. An acquire fence can help only through an exact normative fence rule and qualifying carrier observation; unspecified placement is not enough. Concurrent free is a separate lifetime race.

Simplest repair: complete payload construction, release-store a generation-bearing READY state, acquire-load and verify that same generation before reading, and transfer exclusive ownership or protect lifetime through a lock, reference-counted live handle, hazard/epoch mechanism, GC, or another proved scheme. Reuse advances generation with wrap bounds. If mutable/reusable compound state is involved, use a mutex/condition or bounded channel instead. Model both matching and old-value rf candidates and delay reclamation until all readers quiesce.

### Answer 4

SC atomics simplify allowed-order reasoning but do not alone provide exclusive slot ownership, waiting, reuse generation, or lifetime. Release/acquire is efficient for a carefully specified single-producer/single-consumer state machine. A mutex/condition owns compound state and waiting. A channel directly represents ownership handoff and is usually the clearest application design.

Choose a bounded channel or mutex/condition unless nonblocking requirements justify atomics. Verify state conservation, close/cancel behavior, generation/reuse, and payload lifetime with unit/integration tests, systematic scheduling, race detection, and fault injection. For an atomic implementation, add minimized litmus/model tests under exact source and supported ISA models, inspect compiler mappings, and stress targets. Model checking complements rather than replaces production tests.

### Answer 5

Prove each layer: C++ and Rust source are race-free with compatible atomic representation, alignment, FFI, lifetime, and ordering; compiler outputs preserve those contracts; the exact Arm model permits only intended CPU executions; MMIO/DMA uses platform-defined device barriers/cache maintenance; command identity, acknowledgement, timeout, and recovery handle external commitment.

Record source/ISA litmus files, model/tool revisions, all candidate outcomes, optimized assembly, hardware litmus observations, race/systematic tests, delayed-reclamation cases, MMIO traces, hardware-in-loop timing, device faults, restart during each transition, authorization, and terminal reconciliation. Treat non-observation only as empirical frequency evidence.

Named C++/Rust, compiler, Arm architecture, kernel/driver, hardware/device, concurrency, real-time, controls/robotics, cybersecurity, quality, regulatory, and functional-safety reviewers must approve target-specific claims and hazards. This answer supplies no robotic or deployment approval.
