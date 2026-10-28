---
module_id: CONPAR-096
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 96
title: Race Detection and Concurrency Sanitizers
status: complete
last_verified: 2026-08-29
---

# Race Detection and Concurrency Sanitizers

## One-Page Review

### Governing question

How can dynamic instrumentation turn an observed race, lifetime violation, undefined operation, leak, or device hazard into reproducible evidence and a memory-model-correct fix, while stating exactly which executions, libraries, platforms, address spaces, and bug classes were not checked?

### Essential definitions

- A **data race** is a language-model-defined pair of conflicting accesses not ordered by required synchronization, at least one a write; precise definition depends on language.
- **ThreadSanitizer (TSan)** instruments host code/runtime to detect observed data races and related synchronization misuse on supported platforms.
- **AddressSanitizer (ASan)** detects observed out-of-bounds, use-after-free and selected stack/global/free errors through compiler/runtime instrumentation.
- **UndefinedBehaviorSanitizer (UBSan)** checks selected executed undefined operations such as overflow, invalid shifts, misalignment, or null access.
- **LeakSanitizer (LSan)** reports allocations still reachable/unreachable according to its runtime model/configuration; a reported leak is not necessarily unbounded growth and a clean run is not proof of bounded memory.
- A **device sanitizer** instruments or observes accelerator memory, synchronization, initialization, or shared-memory hazards within documented scope.
- **dynamic coverage** is the set of executed paths, schedules, inputs, binaries/libraries, address spaces, and tool-supported events actually observed.
- A **symbolized report** maps program counters to function, source, line, module and build identity.
- A **suppression/ignorelist** intentionally excludes reports/instrumentation; every entry is reviewed, narrow, owned, justified, and expiring where possible.
- A **benign race** is not a license to leave language-level undefined behavior; use defined atomics/synchronization or a proved supported idiom.
- A **false negative** is an existing defect not reported because path/schedule/tool coverage missed it; **tool limitation** differs from a false positive.
- A **sanitizer build** is a distinct instrumented artifact whose runtime/performance/security characteristics differ from production.

### Central model, mechanism, or theorem

Dynamic sanitizers establish conditional evidence: for instrumented code I, tool/version/config C, input/schedule/environment E, the runtime observed or did not observe an event within its detection model. A race report is triaged by reconstructing the two accesses, allocation/object lifetime, threads/tasks, and missing happens-before edge. The fix changes ownership, synchronization, atomics, immutability, or lifetime—not merely timing—and is accepted only after the reproducer, regression, sanitizer matrix, semantic tests, and relevant unsupported configurations pass.

### Critical invariants

All relevant translation units and compatible libraries are instrumented; compile and final link use matching compiler/runtime; debug information and symbolizer/build IDs are retained; sanitizer combinations are supported rather than guessed; test inputs/schedules cover ownership boundaries; reports/logs are unique and nontruncated; first error is preserved; object/address/thread/device identities map to source; suppressions never hide project defects for convenience; the fix obeys the language/device memory model; production validation remains separate; sanitizer artifacts are not exposed as production by default; and a clean run is described only as no detected issue in the observed coverage.

### Common failures

Teams run only one happy path, instrument an executable but not the racing library, strip symbols, combine incompatible sanitizers, optimize differently enough to remove the path, treat timing changes as proof a race vanished, add sleeps, mark shared data volatile, suppress third-party stacks without ownership/version, ignore the first error and chase cascades, assume host TSan covers GPU/MPI/RDMA, treat GPU racecheck as global-memory race proof beyond documented scope, compare sanitizer timing to production, publish raw addresses/secrets, or say “race-free” after one clean run.

### Compact example

A test matrix has 3 inputs × 4 thread counts × 5 deterministic seeds × 2 optimization configurations = 120 cases. If 7 abort during setup, only 113 executed target code; reporting “120 clean sanitizer tests” is false. Matrix arithmetic tracks intended coverage, not schedule/path completeness or correctness.

### Connections

[Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md) defines the defect. [Happens-Before Relations](023-happens-before-relations.md) guides triage. [Concurrent Memory Allocators](095-concurrent-memory-allocators.md) supplies lifetime/reuse cases. [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md) scopes device memory. The [program roadmap](../ROADMAP.md) next explores schedules systematically rather than relying on naturally observed interleavings.

## Governing Question

Which dynamic checker can observe the suspected defect in the relevant address space/runtime, how will tests drive the needed path and schedule, what constitutes a semantic fix, and how will uninstrumented/unsupported coverage remain visible?

Sanitizers are executable evidence amplifiers. They neither define correctness alone nor replace reasoning, static analysis, model checking, or production observability.

## Why This Matters

Concurrency bugs can survive years because a rare schedule, lifetime, architecture, or optimizer exposes them. Instrumentation observes accesses and synchronization at runtime, catching defects that ordinary functional assertions miss. Address/undefined/leak tools find memory corruption that can masquerade as races. Device tools cover hazards host tools cannot see.

Instrumentation changes time, memory, layout, scheduling, and sometimes supported features. Dynamic tools see only executed code and their model. Partial instrumentation hides edges. Distributed/device executions span runtimes with different visibility. Clean reports therefore require a coverage ledger.

Production-grade use builds a deliberate matrix, preserves exact evidence, fixes root semantics, adds a deterministic regression when possible, and separates sanitizer confidence from release evidence.

## Prerequisites and Retrieval

Retrieve:

- race/atomicity/happens-before/memory-order reasoning from [Race Conditions and Atomicity Violations](005-race-conditions-and-atomicity-violations.md), [Happens-Before Relations](023-happens-before-relations.md), [Acquire and Release Ordering](027-acquire-and-release-ordering.md), and [Relaxed Atomics](028-relaxed-atomics.md);
- lifetime/ABA/reclamation from [ABA Problems and Tagged References](054-aba-problems-and-tagged-references.md), [Hazard Pointers](055-hazard-pointers.md), [Epoch-Based Reclamation](056-epoch-based-reclamation.md), and [Concurrent Memory Allocators](095-concurrent-memory-allocators.md); and
- GPU/MPI hybrid boundaries from [GPU Memory Hierarchies](076-gpu-memory-hierarchies.md) and [Hybrid Threads, SIMD, GPU, and Message Passing](094-hybrid-threads-simd-gpu-and-message-passing.md).

Retrieval prompt: record suspected invariant; languages/address spaces; compiler/linker/tool/runtime versions; instrumented/uninstrumented modules; build flags/debug info/symbolizer; compatible checker matrix; inputs/threads/processes/devices/seeds/schedules/optimization; timeouts/resources; report destination; suppression ledger; reproduction/minimization; fix hypothesis/happens-before; regression; production-equivalence checks; and unavailable coverage.

## Learning Objectives

After completing this module, a learner can:

1. choose host race, address, undefined, leak, and accelerator checks by defect class;
2. build and link fully instrumented symbolizable artifacts;
3. design schedule/input/configuration matrices and coverage ledgers;
4. triage reports to allocation, accesses, threads and missing ordering/lifetime edges;
5. distinguish root reports, cascades, limitations, false negatives, and suppressions;
6. replace timing workarounds with memory-model-correct ownership/synchronization;
7. validate host/device/MPI boundaries without assuming cross-tool coverage;
8. minimize reproducers and add deterministic regression oracles;
9. integrate sanitizer shards into CI with artifacts, timeouts and resource budgets; and
10. scope security, operations, and high-stakes review.

## Core Exposition

### Select the checker

Use a race detector for conflicting host accesses and synchronization recognized by its runtime. Use address checking for bounds, UAF, invalid/double free and supported stack/global cases. Use undefined checks for selected executed language UB; enable specific subchecks/trap/recover policy deliberately. Use leak checking after controlled teardown. Run device memcheck/racecheck/initcheck/synccheck according to documented address-space and primitive support.

Do not assume tools compose. Address and thread sanitizers often require separate builds; platform/architecture/runtime combinations differ. Read current tool docs, query compiler features, and encode a supported matrix. Static analysis, compiler warnings, fuzzing, model checking, and hardware-assisted tools add different coverage.

### Build complete artifacts

Compile and link with the sanitizer-enabled compiler driver so runtime libraries are present. Instrument every project module participating in the suspected interaction where supported; audit prebuilt/shared/plugin/JIT/foreign-language code. Partial instrumentation creates blind spots and stack gaps.

Retain optimization representative enough to preserve behavior while producing useful stacks, debug info, frame pointers when recommended, build ID/source revision, exact flags, runtime options, environment, and symbolizer. Reproducible paths/container/toolchain help CI and local parity.

Separate artifacts by checker and configuration. Never silently ship test runtimes to production; sanitizer runtimes/reports may not be security hardened and greatly change memory/time.

### Executable matrix accounting

This deterministic model counts intended and executed cases. It does not run sanitizers, enumerate interleavings, or prove coverage/correctness.

<!-- bijux-verify: {"id":"sanitizer-matrix-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"inputs=3\nthread_counts=4\nseeds=5\noptimization_configs=2\nintended_cases=120\nsetup_aborts=7\nexecuted_target_cases=113\nexecution_fraction=0.941667\nclean_claim_allowed=False\n","stderr":""}} -->
```python
inputs = 3
thread_counts = 4
seeds = 5
optimization_configs = 2
intended = inputs * thread_counts * seeds * optimization_configs
setup_aborts = 7
executed = intended - setup_aborts
print(f"inputs={inputs}")
print(f"thread_counts={thread_counts}")
print(f"seeds={seeds}")
print(f"optimization_configs={optimization_configs}")
print(f"intended_cases={intended}")
print(f"setup_aborts={setup_aborts}")
print(f"executed_target_cases={executed}")
print(f"execution_fraction={executed / intended:.6f}")
print(f"clean_claim_allowed={setup_aborts == 0}")
```

### Design dynamic coverage

Build axes from invariants: empty/single/many/max inputs; 1,2,oversubscribed and production thread counts; partitions; queue empty/full; cancellation/shutdown; allocation reuse; weak-memory-sensitive operations; seeds; repeated deterministic schedules; optimization; platform; device shapes; MPI ranks; failures/timeouts.

Record intended, built, started, target-reached, completed, report-free, failed, timed-out, skipped and unavailable separately. A crash before the target is not clean. Test duration should exercise steady state and teardown. Random repetition helps but does not enumerate schedules.

Add synchronization hooks/barriers only in test builds to force a known ordering window without “fixing” production. Module 097 supplies systematic scheduling. Fuzz inputs while varying concurrency. Use workload traces scrubbed of secrets.

### Triage the first report

Preserve raw report, stderr, exit status, core/minidump if governed, build/source/tool/options, input/seed/schedule, topology and logs. Symbolize before code changes. Start with the earliest reliable report because memory corruption cascades.

For a race, identify object allocation/generation, two conflicting accesses, threads/tasks, locks/atomics and expected happens-before. Determine whether both accesses are valid lifetime-wise. Reconstruct the missing edge using the language/runtime model, not wall-clock timestamps.

For address errors, locate allocation/free stacks, requested bounds, object generation and last valid owner. For UB, determine whether language semantics make the operation invalid and whether the report is reachable with trusted/untrusted data. For device hazards, respect tool severity/address-space/synchronization scope.

### Fix semantics

Preferred fixes simplify ownership: immutability after publication, single-writer handoff, thread confinement, message passing, structured lifetime, or removal of shared state. Otherwise use the correct mutex/condition/barrier/task dependency or atomics with a proved order. Compound invariants rarely become safe by making individual fields atomic.

`volatile`, sleeps, yields, logging, affinity, optimization changes and wider timing windows are not synchronization. A report disappearing after instrumentation changes is not proof. Suppressing project code without a proved recognized synchronization annotation hides risk.

For UAF, fix lifetime/reclamation rather than quarantine size. For bounds/overflow, validate sizes and arithmetic at the source. For GPU hazards, add the narrow correct barrier/event/stream dependency and verify participating scope; not every block/global dependency can be fixed with a block barrier.

### Suppressions and third-party code

First update/fix upstream or instrument correctly. A suppression record names tool, exact library/function/report signature, owner, reason, upstream issue/version, risk, scope, test proving project isolation, and removal condition. Pin third-party versions so patterns do not broaden silently.

Prefer runtime suppressions for known external reports over disabling instrumentation across large project regions. Instrumentation ignorelists can hide synchronization events and create false reports/misses. Review diffs and count matches; zero/unexpected growth is actionable.

Never call a report benign merely because output looks correct. A language data race can be undefined. If an intentional low-level idiom is supported by the tool/language, use documented annotations and independent proof.

### Host, device, MPI, and foreign runtimes

Host TSan does not generally observe device shared/global execution, NIC DMA, other MPI processes, or uninstrumented foreign runtimes. GPU racecheck may focus on shared memory and documented barriers; memcheck covers different errors. Run both host and device suites and test boundary events/buffer lifetimes.

MPI processes need per-rank log paths and rank/build identity; aggregate without overwriting. A race within a process may be detected, but distributed message-order/deadlock/protocol bugs require MPI/runtime tools and systematic tests. Instrumented timing can change progress and timeouts.

Language FFI boundaries require consistent ABI/lifetime. Managed runtimes and custom allocators may need supported integration. Record what could not be instrumented.

### CI integration

Create separate sanitizer jobs/shards with deterministic seeds plus rotating extended seeds. Set resource/memory/time multipliers based on observed overhead, not production budgets. Avoid running incompatible jobs concurrently on undersized hosts.

Fail on sanitizer findings, abnormal exit, setup abort, missing report, timeout unless explicitly categorized, symbolization failure, or unexpected suppression. Upload bounded artifacts under protected retention. Deduplicate by normalized top stacks without discarding distinct objects/access pairs.

Nightly/periodic matrices cover expensive device, high thread/process counts, long churn, and platforms; per-change jobs cover focused tests. Track time-to-triage, open suppressions, flaky reproducers, instrumented coverage, and unsupported modules—not vanity “zero race” metrics.

### Regression and closure

Minimize while retaining the same semantic defect/report. Add a regression that fails before the fix and passes after, ideally forcing the dependency window and asserting the invariant rather than merely absence of a diagnostic. Preserve original integration case.

Run relevant sanitizer suite, address/UB companions, systematic schedules, unit/integration/property tests, and production-like optimized noninstrumented validation. Inspect code generation/performance separately when synchronization changes. Review memory order and lifetime line by line.

Closure records root cause, happens-before/lifetime proof, changed ownership, report IDs, reproducer, coverage matrix, suppressions, commands/results, unsupported surfaces and reviewer. A clean rerun means no observed supported report, not proof of race freedom.

### Security, operations, and high-stakes limits

Reports include raw addresses, paths, environment, hostnames, inputs, stack/type names and possibly secrets. Redact/pseudonymize, restrict access, encrypt transport/storage, bound retention and report volume. Treat untrusted reproducers and symbolizers as tooling inputs in isolated environments.

Sanitizer runtimes are usually testing tools; production use requires explicit security/performance review. Failures can create large cores/logs; enforce quotas. Do not upload customer/clinical data.

High-stakes closure requires concurrency/memory-model, toolchain/runtime/device, security/privacy, operations, domain, quality/regulatory, ethics, accessibility/human-factors and independent validation reviewers. A clean sanitizer matrix never certifies safety.

## Definitions and Notation

- I: instrumented code/modules; U: known uninstrumented surface.
- C: compiler/tool/runtime/version/options configuration.
- E: executed input, schedule, topology, platform and failure conditions.
- D(C): documented detection model/limitations.
- `HB(a,b)`: relevant happens-before relation between accesses/events.
- `M_intended`, `M_executed`: intended and target-executed matrix cases.
- `S`: suppression ledger with owner/scope/removal condition.
- `R`: raw and symbolized report identity.
- **clean observed run**: no supported finding for `(I,C,E,D)`, never global correctness.
- Obs: build, coverage, reports, root cause, fix proof, tests, limitations and reviewers.

## Mechanisms, Invariants, or Proof Structure

### Instrumentation proof

Audit every translation unit/library/runtime/address space; record supported/unsupported code, exact compiler/link/runtime, debug/symbolization, checker compatibility and build identity. Test known-positive probes where appropriate.

### Dynamic-coverage proof

Matrix derives from ownership/lifetime/boundary/failure invariants; every case has target-reached/completion status; schedules/seeds and environment are reproducible; skips/timeouts/setup failures remain nonclean.

### Root-cause proof

Map report to live object generation, accesses and threads; derive missing happens-before or lifetime/bounds rule from the language/device model; distinguish earliest root from cascades and tool limitation.

### Fix/regression proof

Change ownership/synchronization/reclamation; minimized and integration reproducers fail before/pass after; sanitizer/systematic/functional/optimized results pass; suppression ledger does not expand improperly.

### Claim-boundary proof

Handoff names observed coverage, supported detectors, uninstrumented modules, unavailable platforms, suppression risks, raw artifacts, exact commands/results and human review. It never says race-free universally.

## Alternatives and Trade-Offs

| Technique | Detects/establishes | Principal limitation |
|---|---|---|
| host race sanitizer | observed supported host races | schedule/instrumentation/platform coverage |
| address sanitizer | observed spatial/temporal memory errors | large overhead/layout change |
| UB sanitizer | executed selected UB | not all UB; policy varies |
| leak sanitizer | teardown allocation evidence | reachability/teardown/model limits |
| device sanitizer | documented GPU hazards/errors | address-space/primitive/device scope |
| static analysis | paths without execution | abstractions/false alarms/misses |
| systematic scheduler | controlled interleavings | state-space/model limits |
| model checking/formal proof | properties in formal model | model-code mapping effort |
| production telemetry | real workload symptoms | limited access semantics |

## Failure Modes and Misconceptions

- **“Clean means race-free.”** only observed supported coverage is clean.
- **“TSan covers all concurrency.”** devices/processes/foreign code may be invisible.
- **“ASan finds races.”** it targets memory errors, not general data races.
- **“All sanitizers combine.”** supported combinations vary.
- **“Instrumenting main is enough.”** libraries/plugins can contain accesses.
- **“A setup crash is a clean case.”** target code was not exercised.
- **“Sleep fixes the race.”** timing is not happens-before.
- **“volatile fixes the race.”** it is not general synchronization.
- **“No report after refactor proves fix.”** add semantic proof/regression.
- **“Every report is independent.”** corruption cascades; start earliest.
- **“Benign output means benign race.”** language UB remains.
- **“Suppressions are harmless.”** they can hide owned defects and events.
- **“GPU racecheck covers global memory universally.”** documented scope matters.
- **“Sanitizer speed predicts production.”** instrumentation changes execution.
- **“Timeout means deadlock.”** overhead/resource starvation also cause it.
- **“Random seeds enumerate schedules.”** they sample only.
- **“Reports are safe to publish.”** stacks/paths/addresses/data are sensitive.
- **“Sanitizers certify safety.”** proof, testing and domain review remain.

## Worked Examples

### Example 1

**Host race.** Two writes to a shared counter lack ordering. Replace with locked compound invariant or correct atomic semantics. **Conclusion:** fix the memory model, not timing.

### Example 2

**Partial instrumentation.** Uninstrumented plugin writes shared state; no report appears. Rebuild/inventory or record blind spot. **Conclusion:** coverage begins at build graph.

### Example 3

**UAF masquerade.** Race report address was already freed. ASan allocation/free stacks reveal lifetime root. **Conclusion:** run complementary tools.

### Example 4

**Cascading reports.** First heap overflow corrupts a mutex and produces races. Fix earliest error first. **Conclusion:** temporal report order matters.

### Example 5

**Suppression governance.** Pinned third-party version has upstream issue and narrow signature; suppression has owner/removal test. **Conclusion:** exceptions are auditable debt.

### Example 6

**GPU scope.** Device racecheck finds shared-memory RAW hazard; host TSan was silent. Correct block synchronization and validate active lanes. **Conclusion:** address spaces need their own tools.

### Example 7

**MPI logs.** Rank-specific filenames preserve four reports that a shared path overwrote. **Conclusion:** artifacts need distributed identity.

### Example 8

**Instrumentation timeout.** TSan 10× overhead trips production timeout. Use sanitizer-specific evidence budget while retaining a separate timeout test. **Conclusion:** classify, do not hide.

### Example 9

**Forced regression.** Test barriers pause both threads around publication and reproduce missing release/acquire deterministically. **Conclusion:** deterministic hooks improve evidence.

### Example 10

**Autonomous braking component.** Sanitizer closure must preserve sensor/frame/vehicle/model/configuration/time/unit generations, bounded command/state ownership, deadline/failure/safe-state behavior, raw-report privacy/security, toolchain/target equivalence, replay/fault evidence and release gates. Named automotive dynamics/braking, real-time/concurrency/memory-model, compiler/toolchain/device, functional safety/cybersecurity, operations, quality/regulatory/certification, human-factors, ethics, accessibility and independent validation reviewers must approve evidence; none is claimed here. **Conclusion:** clean dynamic checks do not certify braking safety.

## Cross-Program Connections

- **Languages:** memory models and UB define what reports mean.
- **Compilers:** instrumentation, optimization, debug info, linking and symbolization create evidence.
- **Runtimes:** recognized locks/tasks/atomics, custom synchronization and allocators affect visibility.
- **Distributed/GPU systems:** separate address spaces, DMA, streams and processes need specialized tools.
- **Testing:** matrices, fuzzing, deterministic hooks, minimization and systematic scheduling expand coverage.
- **Formal methods:** root-cause invariants and happens-before proofs complement dynamic observations.
- **Security/privacy:** reports expose internals and sanitizer runtimes are not default production defenses.
- **Operations:** artifacts, suppression debt, flakes, timeouts and CI resources need ownership.
- **Quality/release:** observed coverage and limitations belong in evidence gates.
- **Safety:** dynamic absence of findings is never certification.

## References

1. LLVM Project, *ThreadSanitizer*, current Clang documentation; retrieved 2026-08-29. <https://clang.llvm.org/docs/ThreadSanitizer.html>
2. LLVM Project, *AddressSanitizer*, current Clang documentation; retrieved 2026-08-29. <https://clang.llvm.org/docs/AddressSanitizer.html>
3. LLVM Project, *UndefinedBehaviorSanitizer*, current Clang documentation; retrieved 2026-08-29. <https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html>
4. LLVM Project, *LeakSanitizer*, current Clang documentation; retrieved 2026-08-29. <https://clang.llvm.org/docs/LeakSanitizer.html>
5. LLVM Project, *Sanitizer Special Case List*, current documentation; retrieved 2026-08-29. <https://clang.llvm.org/docs/SanitizerSpecialCaseList.html>
6. LLVM Project, *MemorySanitizer*, current Clang documentation; retrieved 2026-08-29. <https://clang.llvm.org/docs/MemorySanitizer.html>
7. GCC Project, *Instrumentation Options*, current documentation; retrieved 2026-08-29. <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>
8. NVIDIA, *Compute Sanitizer*, current documentation; retrieved 2026-08-29. <https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html>
9. Konstantin Serebryany et al., “AddressSanitizer: A Fast Address Sanity Checker,” USENIX ATC, 2012. <https://www.usenix.org/conference/atc12/technical-sessions/presentation/serebryany>
10. Konstantin Serebryany and Timur Iskhodzhanov, “ThreadSanitizer: Data Race Detection in Practice,” WBIA, 2009. <https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf>

## Exercises

### Exercise 1

A matrix has 4 inputs, 5 thread counts, 10 seeds, 3 optimization modes, and 2 platforms. Compute intended cases. If 12 fail setup, 18 time out after target, and 6 are unsupported before start, state ledger counts and what can be called clean.

### Exercise 2

Given a TSan report with a producer write and consumer read, design a triage packet and derive three possible semantic fixes. Explain why sleep and volatile fail.

### Exercise 3

Design separate host and GPU sanitizer jobs for a CUDA/MPI application, including instrumentation boundaries, rank/device logs, stream/buffer tests, limitations and artifact controls.

### Exercise 4

Create suppression governance and CI policy covering third-party defects, unexpected match growth, timeouts, symbolization, first-error handling, and closure.

### Exercise 5

Transfer sanitizer evidence to concurrent clinical laboratory result processing. Specify data/lifetime, privacy/security, failure, validation/release and named human reviewer invariants without claiming review.

## Answers to the Exercises

### Answer 1

Intended cases are `4*5*10*3*2=1200`. Unsupported-before-start 6, so 1194 startable; setup failures 12 leave 1182 target-executed if failures occurred before target; 18 target-reaching timeouts are executed but incomplete. The ledger must record 6 unavailable, 12 setup-failed/not-target-executed, 18 target-executed/time-out, and 1164 completed (assuming no other outcomes). Only those completed cases with no reports can be described as report-free; none of the matrix is universally “clean,” and timeouts require findings/log/coverage classification rather than being silently excluded.

### Answer 2

Capture raw/symbolized report, build/tool/options, source revision, input/seed/schedule, allocation/object generation, both stacks/access sizes, thread creation stacks, locks/atomics and target invariant. Reproduce/minimize and determine missing happens-before. Fix options: publish immutable object through a mutex/condition and read under the same protocol; transfer single ownership via a synchronized queue; or use an atomic with release publication/acquire consumption if the entire object initialization and lifetime proof match that pattern. For compound mutation, use a lock or versioned immutable snapshot rather than field atomics. Sleep/yield changes scheduling but creates no language happens-before; volatile generally controls accesses/optimization for specific purposes but is not interthread synchronization.

### Answer 3

Host jobs build/link all supported host translation units with separate TSan and ASan/UBSan artifacts, debug symbols and rank-unique protected logs; audit MPI/prebuilt/plugin blind spots and test threads, ranks, progress and staging lifetime. GPU jobs use current Compute Sanitizer memcheck before racecheck/initcheck/synccheck with device-unique/rank-unique logs, deterministic kernels, boundary blocks/active masks, streams/events, async allocation, transfers and error checking. Host TSan cannot claim device/MPI cross-process access coverage; GPU racecheck retains shared-memory/documented primitive limits. Record compiler/MPI/CUDA/driver/GPU/tool versions, configs, target-reached statuses and unsupported paths; bound time/memory/report sizes and redact hostnames/addresses/data before controlled artifact retention.

### Answer 4

Each suppression names tool, exact module/version/function/report signature, owner, upstream issue, rationale/risk, test proving project isolation, approved reviewer, creation/expiry/removal version. CI fails on unsuppressed findings, setup/target/report/symbolization failure, abnormal exit and unexpected suppression count/signature; timeouts are separate failures with partial artifacts. Pin dependencies and alert on zero matches after upgrade as well as growth. Preserve earliest raw report and deduplicate only presentation. Closure requires upstream upgrade or project fix, before/after reproducer, removal of suppression, full relevant sanitizer/systematic/functional runs, memory-model review and remaining blind spots.

### Answer 5

Give specimen/order/patient/consent/instrument/reference/rule/result generations one owner and bounded lifetime; publication and reclamation are synchronized and stale/duplicate results rejected. Use deidentified synthetic/approved datasets in sanitizer jobs; encrypt/restrict/redact reports, paths, identifiers and payloads with retention/audit. Separate instrumented artifacts from production, pin compiler/runtime, inventory LIS/database/vendor blind spots, and fail CI on reports/setup/timeout/missing artifacts. Validate schema/units/reference ranges/provenance, duplicate/missing/out-of-order/cancelled specimens, shutdown/restart, concurrency schedules, independent expected results and optimized production-equivalent behavior. Release requires named laboratory medicine/pathology, clinical informatics, concurrency/memory-model/toolchain, privacy/security/data governance, operations, quality/regulatory, ethics, accessibility/human-factors and independent validation reviewers. No external review, clinical validity, privacy guarantee, approval or deployment authorization is claimed.
