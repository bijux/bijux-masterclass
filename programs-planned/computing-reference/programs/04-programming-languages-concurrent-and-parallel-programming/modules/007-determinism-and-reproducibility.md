---
module_id: CONPAR-007
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 7
title: Determinism and Reproducibility
status: complete
last_verified: 2026-08-29
---

# Determinism and Reproducibility

## One-Page Review

### Governing question

Which inputs and equivalence relation make a concurrent computation deterministic, which environment facts must be captured to reproduce an execution, and when may implementation schedules vary without changing the promised result?

### Essential definitions

- **Determinism** means that a specified initial condition admits one observable result under a stated semantic model and observation boundary.
- **Schedule determinism** means relevant events or work assignments occur in a prescribed order; it is stronger than result determinism.
- **Reproducibility** means an independent repetition under a declared source, input, environment, and procedure produces an output equivalent by a declared comparator.
- **Repeatability** commonly means the same team or setup can repeat the result; terminology varies, so define actors and conditions explicitly.
- **Replay** drives an execution from recorded nondeterministic choices or events. A replayed symptom is evidence about the recorded model, not every possible run.
- **Observational equivalence** relates outputs that a contract treats as the same, such as byte identity, equal sets, a numerical tolerance, or a valid linearizable history.
- **Canonicalization** maps equivalent values to one representation so comparison is stable.
- **Seeded pseudorandomness** deterministically generates a stream only when algorithm, seed interpretation, version, and draw order are fixed.
- A **determinism envelope** is the complete boundary of source, inputs, configuration, runtime, hardware properties, external responses, clocks, randomness, and schedules on which a claim depends.
- A **deterministic reduction** uses a fixed combination structure or an operation whose permitted reordering preserves the declared result.

### Central model, mechanism, or theorem

Let program (P) execute under environment (E), explicit input (x), and unresolved choice sequence (c). Its observation is (O(P,E,x,c)). Result determinism under equivalence relation (approximately) requires:

(forall c_1,c_2 in C(E,x)): O(P,E,x,c_1) approximately O(P,E,x,c_2).

Reproducibility is an experimental claim: two executions with recorded envelopes (D_1,D_2) satisfy a declared relation on artifacts or measurements. Equal outputs from two trials do not prove the universal quantifier above; one differing output refutes a byte-identical claim for that envelope.

### Critical invariants

Every claim names its observable and comparator. Hidden inputs are either eliminated, captured, or declared. The random generator, seed, and draw order are controlled. Clock and external effects enter through injectable interfaces. Parallel reductions define order and arithmetic semantics. Serialization is canonical when byte identity matters. Replay logs carry version and integrity information. Stable tests assert contractual values, not incidental thread order. A tolerance includes units, domain, rounding, and statistical protocol. Evidence distinguishes observed repetition from semantic proof.

### Common failures

Teams say “deterministic” without naming inputs; seed a generator but let concurrent draw order vary; freeze a clock but not time zone or locale; compare unordered data through unstable serialization; use floating-point addition as if associative; pin a thread count but not partitioning; record results without external responses; replay against changed code; replace concurrency with sleeps; accept any output difference as harmless; or infer universal determinism from repeated passing tests.

### Compact example

Three independent workers produce A, B, and C. Appending on completion admits six strings, so the trace and byte result are schedule-dependent. If the contract is the set {A,B,C}, collecting by identity and canonically sorting yields ABC for all six schedules. The schedule remains variable while the contract result becomes deterministic. This redesign is valid only if arrival order is not itself meaningful.

### Connections

[Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md) defines schedules; [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md) distinguishes allowed outcomes from eventual outcomes; [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md) prevents corrupted observations. The [program roadmap](../ROADMAP.md) next covers critical sections, ownership transfer, locks, atomics, happens-before, and linearizability.

## Governing Question

How can engineers make a precise, testable promise about sameness when concurrent schedules, randomized algorithms, clocks, external systems, toolchains, hardware, and numerical order may legitimately vary?

The key is not to force every execution to look identical. It is to define which variation the contract permits, control or record every relevant input, and compare at the right abstraction. Deterministic semantics, deterministic scheduling, replay, repeatable debugging, reproducible research, and reproducible builds solve related but different problems.

## Why This Matters

Concurrency multiplies sources of variation. Runnable tasks may be assigned differently, I/O completions can arrive in another order, hash iteration can change presentation, retries can shift request timing, and floating-point reductions can group operands differently. A data-race-free program may still produce several correct winners or orderings. Conversely, identical output can conceal a race that happened not to affect the observed trial.

Reproducibility is essential for diagnosis, science, finance, security, and supply-chain verification. A developer needs a failing schedule to replay. A researcher needs another group to regenerate a table from declared data and software. An artifact distributor may require bit-for-bit identical builds from the same source, instructions, and relevant environment. A ledger or cache needs stable canonical bytes for hashing. Each use case has a distinct comparator and evidence burden.

Ambiguous claims cause brittle systems. “Same result” might mean equal mathematical sets, equal JSON values, identical bytes, outputs within tolerance, the same error category, or the same event history. Sorting an unordered collection can stabilize presentation, but sorting a stream whose arrival order carries causality destroys information. Rounding can make numerical reports look stable while hiding materially different trajectories.

Determinism also has cost. Fixed scheduling can reduce load balance. Central sequencing can limit throughput. Recording every event increases storage and changes timing. Strict floating-point order can prevent vectorization. Hermetic environments reduce accidental input but require maintenance. The aim is a deliberately sized determinism envelope, not ritual serialization.

## Prerequisites and Retrieval

Retrieve these ideas:

- transition systems, enabled actions, schedules, traces, and state-space exploration from [Interleavings and State-Space Explosion](003-interleavings-and-state-space-explosion.md);
- safety, liveness, fairness, and bounded evidence from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- atomic operations and linearizable histories from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md);
- deadlock, starvation, timeout, and scheduler assumptions from [Deadlock, Livelock, and Starvation](006-deadlock-livelock-and-starvation.md);
- equivalence relations, functions, quantifiers, induction, and counterexamples;
- floating-point representation, rounding, associativity, commutativity, and stable summation; and
- hashes, serialization, process environments, dependency locks, and test isolation.

Retrieval prompt: list the six interleavings of three one-event workers A, B, and C. Give one observation function that distinguishes all schedules and another that treats them as equal. Explain why both answers can be correct for different contracts.

## Learning Objectives

After completing this module, a learner can:

1. distinguish semantic, result, trace, schedule, build, and experimental reproducibility claims;
2. state a determinism property with quantified choices and a precise observation equivalence;
3. inventory a determinism envelope across code, data, time, randomness, runtime, hardware, and services;
4. design deterministic aggregation without erasing contractually meaningful order;
5. reason about seeded randomness, concurrent draw order, and substream assignment;
6. explain why floating-point parallel reductions may vary and choose an appropriate remedy;
7. design record/replay evidence with versioning, integrity, and external-event capture;
8. build tests that expose schedule variation without depending on incidental timing; and
9. bound high-consequence reproducibility claims that require named authorized review.

## Core Exposition

### Define the observation before controlling execution

Model an execution as a trace of internal and external events. An observation function projects that trace to what the contract exposes. It may return final state, response sequence, multiset of records, exit status, serialized artifact, numerical vector, or a history with real-time constraints. Determinism is always relative to this projection.

Suppose two work queues process independent keyed updates. Their internal dequeue order differs, yet the final map is equal. The system is result-deterministic under map equality but not trace-deterministic. If clients observe intermediate callbacks, callback order joins the contract and the same runs may no longer be equivalent. Avoid hiding a disagreement by choosing an overly coarse comparator.

Use three layers:

1. **Value semantics:** which abstract outputs are permitted?
2. **Representation:** how is an abstract value encoded?
3. **Execution evidence:** which internal events must be repeatable for diagnosis or audit?

Canonicalization addresses representation, not computation. Sorting object keys can give stable bytes for an already equal mapping; it cannot repair a lost update or decide whether two concurrent writes should commute.

### Write the determinism property

Let (C(E,x)) be all unresolved choices admitted by the model: scheduling, message arrival, random draws, allocation, or external responses. Exact result determinism requires equality of observations for every pair of admissible choices. Contract determinism replaces equality with an explicit equivalence relation.

This universal form supplies a practical review method. Inventory each choice. Show it cannot affect the observation, show different results are equivalent, control the choice, record it, or change the specification to acknowledge permitted outcomes. A single counterexample pair disproves the claim. Testing many equal runs increases confidence but does not discharge the universal quantifier unless exploration is exhaustive for a justified finite model.

Confluence is one structural route. If independent transitions commute and divergent steps can rejoin an equivalent state, schedule differences may disappear from the final result. Kahn process networks give a classical deterministic model: deterministic sequential processes communicate through unbounded single-writer/single-reader FIFO channels, yielding determinate stream values under the model. Real bounded queues, nondeterministic selection, timeouts, failures, and side effects can violate those premises.

### Inventory the determinism envelope

Treat every observation not derived solely from declared input as an input candidate:

- source revision, generated source, patches, and build instructions;
- dependencies, compiler, linker, runtime, flags, and feature selection;
- input bytes, schema, ordering, partitioning, and preprocessing;
- environment variables, locale, time zone, working directory, and filesystem metadata;
- wall clock, monotonic clock, timer resolution, and deadline configuration;
- random algorithm, seed, stream/substream identity, and draw count;
- thread count, work partition, affinity, scheduling policy, and accelerator topology;
- processor instruction set, floating-point mode, library implementation, and device firmware;
- service responses, network faults, database snapshots, credentials, and feature flags; and
- output encoding, canonicalization, compression, signatures, and comparator version.

Eliminate accidental inputs where practical. Inject clocks, pass configuration explicitly, lock dependencies, normalize paths, and isolate temporary state. Capture remaining inputs in a machine-readable provenance record. Never record secrets merely for convenience; store safe identifiers, controlled fixtures, or authorized encrypted evidence.

An envelope is claim-specific. Byte-reproducible builds need source, instructions, and relevant build environment. A numerical experiment may permit platform variation within a validated tolerance. A concurrent object proof may quantify over all legal schedules instead of fixing one. Record the minimum complete boundary, not every fact in the universe.

### Randomness: a seed is necessary but often insufficient

A pseudorandom generator maps internal state to a deterministic stream. Reproducing that stream requires the generator definition, seed conversion, version, and identical sequence of draws. In concurrent code, sharing one seeded generator does not fix which task receives which draw. A schedule change reassigns samples even when the global sequence is unchanged.

Prefer identity-derived substreams: assign each logical work item a stable stream key, use a splittable or counter-based generator with a documented algorithm, and keep draw count within the item deterministic. This decouples sample identity from task scheduling. Validate independence assumptions; merely hashing an ID into an arbitrary generator may create statistical defects.

Cryptographic randomness has a different contract. Making secret nonces predictable for reproducibility can destroy security. Test through deterministic fixtures or an injected approved test source while production uses an authorized cryptographic generator. Never export production random state or keys as a replay shortcut.

### Time and external systems

Wall time changes continuously and can jump because of synchronization or administrative adjustment. Monotonic time measures intervals but still depends on the execution environment. Inject a clock for deterministic domain tests, and test calendar rules with explicit time zone databases and ambiguous or nonexistent local times.

External services add choices: response bodies, status codes, order, latency, retries, and side effects. A replayable test uses versioned fixtures or a protocol-level event log and verifies outgoing requests. Recording only responses can conceal that changed code sent a different request. Replaying authenticated or personal data creates retention and access obligations.

For databases, capture the logical snapshot or seed data, schema, migration state, isolation level, query plan assumptions that affect semantics, and canonical output order. SQL without an ordering contract may legally return rows in another order. Adding `ORDER BY` stabilizes presentation only when its keys define a complete desired order; ties require an explicit policy.

### Deterministic aggregation and floating-point order

If concurrent workers append results as they finish, completion time becomes an input. Replace arrival position with stable logical identity, collect keyed results, and emit in declared key order when order has no domain meaning. If results form a set, compare as a set and canonicalize only at the representation boundary. If order expresses causality or priority, preserve and model it instead.

Reductions need algebra. An associative and commutative operation yields the same abstract result under regrouping and reordering. Integer addition is associative only absent overflow or under explicitly modular semantics. Floating-point addition is not associative: (10^16 + (-10^16)) + 1 gives 1 in common binary64 evaluation, while 10^16 + ((-10^16) + 1) gives 0 because the small addend is rounded away.

Options include a fixed reduction tree, reproducible summation algorithms, higher precision, exact accumulators for bounded domains, compensated summation, or a tolerance-based numerical contract. Fixed order gives run-to-run stability for the same implementation but does not necessarily give the most accurate answer. Tolerances must state absolute/relative form, scale, exceptional values, and validation domain; “close enough” is not a specification.

OpenMP 6.0 distinguishes reproducible from unconstrained loop scheduling in specific constructs. That schedule property concerns consistent iteration-to-thread or lane assignment under its stated conditions; it does not automatically make racy code, external I/O, unordered serialization, or floating-point results reproducible.

### Reproducible artifacts and canonical bytes

The Reproducible Builds project defines a reproducible build through the same source code, build environment, and build instructions producing bit-by-bit identical specified artifacts. Timestamps, filesystem order, embedded paths, build IDs, locale, tool versions, and nondeterministic archives are common accidental inputs. The verifier needs an independently recreated environment and byte/hash comparison, not a second artifact copied from the first build.

Canonical serialization specifies exactly how equivalent data becomes bytes. RFC 8785, for example, constrains JSON data and defines primitive serialization, recursive property sorting, and UTF-8 output for its canonicalization scheme. Alphabetically sorting whatever a local library emits is not general conformance. Canonicalization also does not prove the abstract data were correctly computed.

When signatures, hashes, or cache keys depend on bytes, version the canonicalization algorithm and reject unsupported or ambiguous values. Duplicate keys, Unicode handling, number range, negative zero, NaN, infinity, and normalization policy can otherwise create cross-runtime disagreement.

### Record, replay, and schedule control

Record/replay systems capture nondeterministic inputs such as system-call results, signals, thread ordering, or synchronization decisions, then reproduce them against compatible code and runtime state. The log needs an execution identity, code and schema version, ordering rule, integrity protection, and explicit unsupported events.

Replay is strongest for diagnosis: it can make one failure repeatable and support causal inspection. It does not prove other schedules safe. Changed instrumentation can perturb timing; changed code can make an old log invalid; distributed replay must account for clocks and message causality across processes.

Systematic schedulers control yield points and enumerate or prioritize schedules. Deterministic schedulers choose a repeatable policy. Stress tools introduce variation. Use each deliberately: repeat the known trace, explore nearby choices, and separately prove invariants where possible. A deterministic test scheduler that never exercises a problematic interleaving can produce perfectly repeatable false confidence.

## Definitions and Notation

Let execution (e = Exec(P,D,c)) run program (P) with declared envelope (D) and unresolved choices (c in C_D). Observation (O(e)) is compared by equivalence relation (approximately_D).

**Exact determinism** means (O(Exec(P,D,c_1)) = O(Exec(P,D,c_2))) for all admissible (c_1,c_2). **Contract determinism** replaces equality with (approximately_D). A deterministic schedule fixes the relevant scheduling component of (c); it need not fix time, services, allocation, or hardware.

A reproduction protocol (R) maps a provenance record to an execution attempt. Its result is successful when (Compare_D(O(e_original), O(R(D)))) passes. The claim must define who may reproduce, which envelope differences are allowed, and the comparator.

For reduction operator (oplus), associativity requires ((a oplus b) oplus c = a oplus (b oplus c)); commutativity requires (a oplus b = b oplus a). These properties apply to actual representation semantics, including overflow and rounding, not merely the corresponding mathematical operation.

A canonicalizer (K) should satisfy idempotence (K(K(x)) = K(x)) within its domain and map equivalent allowed representations to the same bytes. It must not collapse values the contract distinguishes.

## Mechanisms, Invariants, or Proof Structure

Apply this workflow:

1. **Name the claim.** Result determinism, trace replay, byte reproducibility, or numerical reproducibility are separate.
2. **Choose the observation.** List outputs and events visible to users, auditors, or downstream systems.
3. **Define equivalence.** Exact bytes, abstract equality, ordering constraints, or justified numerical/statistical criteria.
4. **Inventory choices and hidden inputs.** Include schedules, random draws, clocks, services, environment, toolchains, and hardware.
5. **Classify each source.** Eliminate, control, capture, quantify over, or explicitly permit its effect.
6. **Design stable composition.** Use keyed aggregation, canonical serialization, fixed reduction structure, logical clocks, or deterministic ownership.
7. **Record provenance.** Bind source, inputs, configuration, tool versions, fixture identities, comparator, and integrity.
8. **Test variation.** Change schedules, worker counts, hash seeds, locale, time zone, paths, clocks, and partitioning within the declared envelope.
9. **Reproduce independently.** Avoid sharing undeclared build products or mutable state with the original.
10. **Bound the conclusion.** Separate counterexample, sampled repetition, exhaustive finite exploration, proof, and external review.

Maintain these invariants:

- every sameness claim names an observation and comparator;
- logical identity, not completion timing, owns deterministic aggregation position;
- all random work items have stable stream ownership and versioned algorithms;
- injected time and external fixtures preserve the contract being tested;
- numerical combination order and exceptional-value behavior are explicit;
- canonicalization is domain-defined, versioned, and idempotent;
- replay logs are integrity-bound to compatible code and schemas;
- stable tests do not require incidental worker IDs or wall-clock timing;
- provenance excludes secrets while retaining safe evidence; and
- finite repetition never masquerades as a universal proof.

## Alternatives and Trade-Offs

**Serialize all work** makes order obvious but sacrifices parallelism and can create a bottleneck. **Deterministic parallel structure** retains concurrency by fixing partitions and combination trees; it may underuse heterogeneous resources.

**Canonicalize at output** is inexpensive when variation is representational. It cannot repair semantic divergence and may conceal meaningful arrival order. **Compare abstract values** keeps the contract clean but downstream hashes and signatures still require canonical bytes.

**Capture the environment** preserves fidelity for replay but creates storage, privacy, versioning, and compatibility burdens. **Hermetic execution** eliminates many inputs but cannot fully isolate processor behavior, kernels, devices, or external services unless those too are modeled.

**Record/replay** reproduces one observed trace efficiently. **Systematic exploration** searches several traces. **Formal proof** quantifies over the modeled traces. These evidence types complement one another and differ sharply in cost and coverage.

**Fixed seeds** help repeat randomized tests. **Fresh generated seeds recorded on failure** explore more behavior while retaining replay. Identity-owned substreams scale better than a shared generator but require a stable generator contract.

**Exact numerical reproducibility** supports auditing and regression but can constrain vectorization and accelerators. **Tolerance-based comparison** allows useful optimization but needs scientifically justified bounds and can miss structured bias. **Statistical reproducibility** needs prespecified estimands, sampling, uncertainty, and test power.

**Stable toolchains and containers** reduce environment variance. They are not complete provenance by themselves: mutable tags, base images, kernels, build context, network downloads, timestamps, and CPU features remain potential inputs.

## Failure Modes and Misconceptions

- **“The same input gives the same output.”** Specify whether input includes environment, seed, schedule, time, and external responses.
- **“Data-race-free means deterministic.”** Correct synchronization can permit several valid orders or winners.
- **“Deterministic means single-threaded.”** Parallel computations can have deterministic abstract results.
- **“We set the seed.”** Concurrent draw assignment, algorithm version, and draw count can still differ.
- **“Sorting fixes nondeterminism.”** It fixes representation only when order is not semantic.
- **“Floating-point addition is associative enough.”** Parallel grouping can produce different bits and error.
- **“A tolerance of 0.001 is objective.”** Units, magnitude, exceptional values, and domain determine meaning.
- **“The container captures the environment.”** Host kernel, processor, device, mutable inputs, and external services may remain.
- **“Replay proves the bug fixed.”** It shows behavior for a compatible recorded trace.
- **“One matching rebuild proves reproducibility.”** Independence and meaningful environment variation matter.
- **“Hash equality proves correct computation.”** It proves byte equality under the hash assumption, not semantic correctness.
- **“Canonical JSON means sorted keys.”** A scheme must also define number, string, Unicode, whitespace, and invalid-value behavior.
- **“Stable tests should assert thread order.”** Assert contractual order; incidental execution detail makes tests brittle.
- **“No observed differences proves determinism.”** Sampled equality is not universal quantification.

## Worked Examples

### Example 1

**Question:** Two schedules update disjoint keys and finish with equal maps but different log order. Is the computation deterministic?

**Reasoning:** Under final-map equality, yes. Under byte log equality, no. The answer changes with the observation.

**Conclusion:** State the observation and equivalence before making the claim.

### Example 2

**Question:** A seeded shared generator supplies samples to whichever worker requests next.

**Reasoning:** The global stream repeats, but scheduling changes which logical item receives each sample.

**Conclusion:** Seed alone is insufficient; assign stable substreams by logical identity.

### Example 3

**Question:** Why can a parallel binary64 sum change across worker counts?

**Reasoning:** Partitioning changes grouping, and floating-point addition is not associative. For example, the two groupings of 10^16, -10^16, and 1 can yield 1 or 0.

**Conclusion:** Fix the reduction tree or specify and validate another numerical contract.

### Example 4

**Question:** A SQL query returns the same rows in varying orders and feeds a byte hash.

**Reasoning:** Abstract bag equality does not imply byte equality. The query lacks a complete ordering contract.

**Conclusion:** Add a deterministic total ordering or canonicalize the abstract result if order is not meaningful.

### Example 5

**Question:** A build made twice in the same directory has equal hashes.

**Reasoning:** This is useful repeatability evidence, but the trials may share cached or generated artifacts and do not establish independent recreation.

**Conclusion:** Rebuild independently from declared source, instructions, and relevant environment while varying likely accidental inputs.

### Example 6

**Question:** A replay log reproduces a crash after 50 runs. What follows?

**Reasoning:** The log and compatible runtime provide a stable witness for that execution. Unrecorded inputs and other schedules remain outside coverage.

**Conclusion:** Use replay for diagnosis, then test or prove the repaired invariant more broadly.

### Example 7

**Question:** Three workers return A, B, and C in any completion order. Can result determinism coexist with schedule variation?

**Reasoning:** Enumerate all schedules and compare raw append order with identity-based canonical aggregation.

<!-- bijux-verify: {"id":"schedule-independent-canonical-result","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schedules=6\nobserved_orderings=6\ncanonical_results=1\ncanonical_value=ABC\n","stderr":""}} -->
```python
items = ["A", "B", "C"]
schedules = []

def arrange(prefix, remaining):
    if not remaining:
        schedules.append(prefix)
        return
    for index in range(len(remaining)):
        arrange(prefix + [remaining[index]], remaining[:index] + remaining[index + 1:])

arrange([], items)
observed = {"".join(schedule) for schedule in schedules}
canonical = {"".join(sorted(schedule)) for schedule in schedules}

print(f"schedules={len(schedules)}")
print(f"observed_orderings={len(observed)}")
print(f"canonical_results={len(canonical)}")
print(f"canonical_value={next(iter(canonical))}")
```

**Conclusion:** All six schedules differ as traces, while canonical set-style output has one value. The execution proves these counts only; it does not prove that sorting is valid for a domain, that real tasks are independent, or that a production system is deterministic.

### Example 8

**Question:** Does an injected fixed clock make a billing test reproducible?

**Reasoning:** It controls clock reads, but time zone data, currency rules, database state, service responses, and retry order may remain inputs.

**Conclusion:** The fixed clock is one envelope component, not the complete protocol.

### Example 9

**Question:** Two numerical runs differ by 0.0005 and the test tolerance is 0.001.

**Reasoning:** The comparator passes, but no scientific conclusion follows without units, expected scale, accumulated error, exceptional-value handling, and domain justification.

**Conclusion:** Passing an arbitrary tolerance is not evidence of meaningful reproducibility.

### Example 10

**Question:** A clinical risk model gives identical recommendations in two replayed trials. Is that enough to approve deterministic deployment?

**Reasoning:** Dataset provenance, subgroup behavior, preprocessing, numerical platforms, drift, missingness, uncertainty, clinical consequences, and governance lie beyond two matching trials.

**Conclusion:** No. Approval requires named authorized clinical, statistical, and safety reviewers under the applicable process. This chapter claims no external review or fitness for clinical use.

## Cross-Program Connections

- **Programming languages:** memory models, iteration contracts, purity, effect systems, and runtime schedulers determine allowed variation.
- **Algorithms:** confluence, commutative monoids, stable sorting, numerical analysis, and canonical forms support deterministic composition.
- **Distributed systems:** logical clocks, consensus order, idempotency, replay, and partial failures define cross-node observations.
- **Data science:** dataset versions, seeds, preprocessing, numerical kernels, and statistical protocols govern experimental reproducibility.
- **Security:** canonical bytes, reproducible builds, provenance, and secret-safe randomness affect signatures and supply-chain assurance.
- **Cloud engineering:** mutable images, regional services, autoscaling, and managed dependencies expand the environment envelope.
- **Testing:** property testing, schedule control, fixture isolation, metamorphic relations, and failure-seed retention provide complementary evidence.
- **Formal methods:** observational equivalence, refinement, confluence, and model checking can quantify over choices instead of sampling them.

## References

1. Gilles Kahn, “The Semantics of a Simple Language for Parallel Programming,” in *Information Processing 74*, North-Holland, 1974, [author-hosted scan](https://www.cs.cmu.edu/~crary/819-f09/Kahn74.pdf).
2. Robert H. B. Netzer and Barton P. Miller, “What Are Race Conditions? Some Issues and Formalizations,” *ACM Letters on Programming Languages and Systems* 1(1), 1992, [doi:10.1145/130616.130623](https://doi.org/10.1145/130616.130623).
3. Emery D. Berger et al., “Grace: Safe Multithreaded Programming for C/C++,” *OOPSLA 2009*, [doi:10.1145/1640089.1640096](https://doi.org/10.1145/1640089.1640096).
4. Pat H. Sterbenz, *Floating-Point Computation*, Prentice-Hall, 1974.
5. Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*, second edition, SIAM, 2002, [doi:10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027).
6. OpenMP Architecture Review Board, *OpenMP Application Programming Interface 6.0*, November 2024, [official specification](https://www.openmp.org/specifications/) (retrieved 2026-08-29).
7. Reproducible Builds, “Definitions,” current project definition of reproducible builds, [project documentation](https://reproducible-builds.org/docs/definition/) (retrieved 2026-08-29).
8. Anders Rundgren, Bret Jordan, and Samuel Erdtman, “JSON Canonicalization Scheme (JCS),” RFC 8785, 2020, [RFC Editor](https://www.rfc-editor.org/rfc/rfc8785.html).
9. Robert O'Callahan et al., “Engineering Record and Replay for Deployability,” *USENIX ATC 2017*, [USENIX paper](https://www.usenix.org/conference/atc17/technical-sessions/presentation/ocallahan).
10. Sebastian Burckhardt et al., “A Randomized Scheduler with Probabilistic Guarantees of Finding Bugs,” *ASPLOS 2010*, [doi:10.1145/1736020.1736040](https://doi.org/10.1145/1736020.1736040).

## Exercises

### Exercise 1

A parallel image pipeline produces equal pixel arrays but writes metadata fields in completion order, so artifact hashes vary. Define three possible observations, decide which variation is contractual, and propose a verification protocol for byte-reproducible artifacts.

### Exercise 2

A simulation uses one seeded generator shared by 32 tasks. Explain how schedule changes reassign draws. Redesign stream ownership and list the generator facts that provenance must preserve.

### Exercise 3

For values 10^16, -10^16, and 1 under binary64 arithmetic, evaluate two parenthesizations. Explain why commutativity alone is insufficient for parallel reduction and compare a fixed tree with a tolerance-based contract.

### Exercise 4

Design a record/replay artifact for a concurrent service that reads time and calls a pricing API. Specify recorded events, request verification, version compatibility, integrity, secrets handling, and what replay cannot prove.

### Exercise 5

A credit-allocation model produces identical approvals on two machines after the team pins the container image and random seed. Assess the completion claim, identify missing envelope and fairness evidence, and state where named authorized human review is required.

## Answers to the Exercises

### Answer 1

Possible observations are abstract pixel-array equality, semantic image-plus-metadata equality, and exact artifact bytes. If metadata order has no domain meaning but signed artifacts require stable bytes, collect metadata by stable field identity and serialize through a specified canonical format; do not merely sort an opaque causal log. Start two clean builds from the same identified source and input image, declared toolchain and environment, and fixed metadata policy. Vary path, locale, filesystem order, worker count, and timestamp sources within the supported envelope. Compare complete bytes and preserve provenance and hashes. Matching trials support the declared protocol, while the concurrency argument or exhaustive finite test must separately show every admissible completion order maps to the same canonical value.

### Answer 2

The generator emits a repeatable global sequence, but whichever task runs its next request receives that value, so task results change with schedule. Give each logical simulation unit a stable stream identifier and derive or split a stream using a documented generator designed for independent substreams. Keep the unit's draw order deterministic. Provenance records generator family and version, seed encoding, root seed, stream-derivation algorithm, unit identity, draw-count policy, and any library or architecture constraints. It must also state the statistical independence evidence and avoid exposing production secrets.

### Answer 3

With common binary64 evaluation, (10^16 + (-10^16)) + 1 evaluates to 1, while 10^16 + ((-10^16) + 1) evaluates to 0 because adding 1 to -10^16 rounds away the small term. Commutativity permits swapping two operands but does not make regrouping safe; parallel trees regroup. A fixed tree provides bit stability for fixed semantics and inputs but may preserve a numerically weak order. A tolerance contract permits implementation variation but needs justified absolute/relative bounds, scales, exceptional-value rules, and validation over the operating domain.

### Answer 4

Record code and schema identity, monotonic and wall-clock observations, outgoing request method/body/headers after secret-safe normalization, response/status/order, retry decisions, cancellation, and relevant scheduler or synchronization events. During replay, assert that outgoing requests match rather than blindly returning recorded responses. Integrity-bind and access-control the log, replace credentials and personal data with authorized fixtures, and reject incompatible code or schemas. Replay can reproduce one captured trace; it cannot prove safety over unrecorded schedules, correctness of the price source, production timing, or absence of races.

### Answer 5

Two equal trials after pinning an image and seed are useful repeatability evidence, not a complete determinism, fairness, or deployment claim. Missing inputs may include source and data lineage, preprocessing, generator algorithm and task draw assignment, host CPU and numerical libraries, feature and policy versions, time, external data, subgroup definitions, comparator, and drift. Evaluation must include outcome validity, subgroup error and allocation impacts, sensitivity, uncertainty, and permitted numerical variation. Credit policy, fairness thresholds, adverse-action obligations, and deployment approval require named authorized legal, risk, statistical, and domain reviewers under the applicable governance process. No such external review is claimed by this chapter.
