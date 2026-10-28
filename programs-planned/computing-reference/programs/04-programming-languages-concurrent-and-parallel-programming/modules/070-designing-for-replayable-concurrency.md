---
module_id: CONPAR-070
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 70
title: Designing for Replayable Concurrency
status: complete
last_verified: 2026-08-29
---

# Designing for Replayable Concurrency

## One-Page Review

### Governing question

What must a system capture and control so that a concurrent execution can be reconstructed for diagnosis, and how can replay detect incompatibility instead of silently producing a different history?

### Essential definitions

- **record/replay** captures nondeterministic inputs and decisions during one execution and later re-executes under constraints derived from that record.
- **faithful replay** reconstructs the specified original event/state history; **output-deterministic replay** may construct another history with equivalent recorded outputs.
- A **replay boundary** divides deterministic computation from events whose values or delivery positions must be recorded.
- An **external input** originates outside the recorded deterministic machine: system-call results, network/file bytes, time, randomness, signals, device events, or operator input.
- A **synchronization event** orders threads through locks, atomics, condition variables, channels, futures, or other communication.
- A **data race** is conflicting unsynchronized access under the relevant memory model; faithfully replaying races may require memory-access order beyond synchronization logs.
- A **logical event identity** is stable across record and replay and does not rely only on reused addresses or native thread IDs.
- A **checkpoint** captures enough deterministic state to start replay before a target event.
- A **replay trace** is a versioned, integrity-protected sequence of inputs, choices, and landmarks.
- **divergence** means replay's next observed state or enabled event context is incompatible with the trace.
- **reverse debugging** repeatedly restores checkpoints and replays to inspect earlier states; execution is not literally reversed.
- **execution sketching** records partial constraints and searches unresolved choices during diagnosis rather than guaranteeing first-attempt faithful replay.

### Central model, mechanism, or theorem

Let deterministic transition function δ advance state given one recorded input/event. Record an initial checkpoint C and log `L=[(kind,id,context,value/order)]`. Replay restores C, resolves each event against the compatible runtime state, verifies its context, injects the recorded value or ordering constraint, and applies δ. By induction, if checkpoint, deterministic code, instruction/memory semantics, and every result-affecting nondeterministic event agree, replay reaches the same scoped state. Missing an event, changing the binary/environment, allowing an uncontrolled race, or interpreting a reused identity invalidates the premise and must yield explicit divergence.

### Critical invariants

The replay boundary covers all result-affecting nondeterminism. Trace order is monotonic and records enough context to reject a wrong match. Checkpoints, binary, libraries, configuration, inputs, architecture/memory model, and trace schema are content/version bound. External side effects are suppressed, simulated, or redirected during replay. Thread/task identities survive creation and reuse. Recorder buffers cannot lose events on crash without labeling the trace incomplete. Secrets and personal data are minimized, encrypted, access controlled, and retained under policy. Divergence is reported at the first mismatch. Diagnostic perturbation creates a branch and cannot rejoin the original trace without a valid state correspondence.

### Common failures

Systems record only wall-clock timestamps; assume synchronization order captures racy memory; save a seed but not external bytes; identify threads by reused OS ID; record values without call/event identity; ignore signals, time, CPU counters, allocation addresses, filesystem metadata, or library callbacks; replay real external writes; accept a different enabled set; use a trace against a changed binary; let log buffers vanish on crash; expose credentials in traces; call output-equivalent search faithful replay; or treat reproducing one failure as proof the program is correct after a repair.

### Compact example

Two tasks each read shared x then write its private read plus one. A trace records the enabled operation set and selects `A:R, B:R, A:W, B:W`, reproducing final x=1. If a trace entry claims only A's write was enabled when B's write was also enabled, replay stops at that choice with the expected and actual sets. Silent selection would turn a compatibility failure into misleading evidence.

### Connections

[Deterministic Schedulers for Testing](066-deterministic-schedulers-for-testing.md) explores controlled test schedules; record/replay reconstructs one observed run or constraints from it. [Reproducible Randomness in Parallel Programs](069-reproducible-randomness-in-parallel-programs.md) removes random values from the logging burden when identities are stable. Earlier race, memory-model, and lifecycle modules define events a replay system must cover.

## Governing Question

Which nondeterministic events, state, identities, compatibility metadata, and integrity controls must be captured to make a concurrent failure reproducible at the fidelity the debugger or forensic analysis actually requires?

A log is replayable only relative to a machine model. Application events, synchronization calls, system calls, virtual-machine inputs, and individual memory conflicts define increasingly broad and costly boundaries.

## Why This Matters

Concurrency failures often disappear when logs or debuggers alter timing. A trace that reconstructs the failure turns a transient production incident into a repeatable experiment: engineers can inspect state, set watchpoints, execute forward from checkpoints, and validate candidate repairs against the same witness.

Replay also supports reverse debugging, security forensics, flaky-test diagnosis, deterministic simulation, audit, and failure minimization. But production recording consumes CPU, storage, I/O, and operational attention. Broader fidelity captures more behavior while increasing overhead and sensitive data.

The essential engineering move is to specify fidelity. Reproducing returned values may suffice for one bug. Race diagnosis may require the exact conflicting access order. Security forensics may need guest instruction and device input history below a compromised operating system. No one trace format supplies all goals cheaply.

## Prerequisites and Retrieval

Retrieve:

- happens-before and race scope from [Happens-Before Relations](023-happens-before-relations.md);
- lifecycle identity from [Creating and Joining Threads](011-creating-and-joining-threads.md);
- controlled schedule traces from [Deterministic Schedulers for Testing](066-deterministic-schedulers-for-testing.md);
- immutable checkpoints from [Immutable Snapshots and Multi-Version State](067-immutable-snapshots-and-multi-version-state.md); and
- logical random identity from [Reproducible Randomness in Parallel Programs](069-reproducible-randomness-in-parallel-programs.md).

Retrieval prompt: list every value a concurrent program may obtain without deriving it from explicit immutable input. Classify which can be recomputed, which must be recorded, and which require an ordering position as well as a value.

## Learning Objectives

After completing this module, a learner can:

1. distinguish faithful, synchronization, output-equivalent, and probabilistic replay;
2. define a replay boundary at application, language/runtime, process, OS, or VM level;
3. inventory external, scheduling, signal, memory, and runtime nondeterminism;
4. design versioned event identities, contexts, checkpoints, and trace schemas;
5. prove replay by deterministic-transition induction and identify its trusted base;
6. handle races, weak memory, system calls, signals, time, randomness, and side effects;
7. detect divergence and branch diagnostic executions honestly;
8. engineer buffering, compression, retention, privacy, integrity, and crash recovery;
9. verify replay fidelity and repair effectiveness with independent evidence; and
10. scope replay for security, safety, and regulated environments.

## Core Exposition

### Specify the fidelity target

Bit-for-bit instruction replay aims to reproduce architectural register/memory state at specified instruction points. Synchronization replay reproduces communication order under an assumption such as data-race freedom. Application replay injects recorded request, message, time, and decision events at semantic boundaries. Output-deterministic replay seeks any execution producing equivalent recorded outputs. Probabilistic replay records a sketch and searches remaining interleavings.

These are not interchangeable. Output equivalence can be enough to reproduce an assertion but may alter hidden state or causality. A synchronization-only trace cannot faithfully reproduce an unsynchronized race. A full VM trace can replay guest execution but still depends on the virtualizer, host/hardware assumptions, and protected log integrity.

Define observation O: exact instruction state, program-visible values, synchronization history, external output, failure signature, or forensic evidence. Define the allowed replay set. Label partial or probabilistic methods with attempt counts and unresolved choices.

### Deterministic machine and nondeterministic inputs

Conceptually, execution is deterministic once all nondeterministic inputs and their delivery positions are fixed. The chosen machine includes code, initial state, instruction semantics, memory model, runtime, libraries, OS interface, devices, and external environment.

Nondeterminism includes system-call return values and output buffers; file/network/device bytes; time and clocks; entropy/randomness; process/thread IDs; address layout and allocation when observed; signals, interrupts, exceptions, and cancellation; scheduler and synchronization winners; weak-memory/read-from choices; JIT/GC/finalizer decisions when visible; locale/environment; and other processes' shared-memory effects.

Some events can be derived. A deterministic counter-based random mapping with stable inputs need not be logged per draw. Pure computation need not be logged. But the derivation algorithm and inputs must be compatibility bound.

### Choose the boundary

An application boundary is portable and compact but trusts instrumentation and libraries below it. A managed-runtime boundary can control tasks, synchronization, GC-sensitive semantics, and system interfaces while tying replay to a runtime version. A process boundary intercepts syscalls/signals and constrains scheduling. A kernel or VM boundary captures a broader machine and can support unmodified software at greater operational cost.

The boundary must be closed. A native extension using unrecorded shared memory, a library starting an unmanaged thread, direct hardware access, shared memory with another process, or asynchronous device DMA is an escape. Detect or explicitly exclude escapes.

Security forensics may put recording below the component that could be compromised and protect logs remotely or append-only. Debug replay may accept a trusted application/runtime recorder. Threat model determines placement.

### Event identity and trace schema

Each event includes monotonically ordered log position, event kind/version, stable task/process identity, operation identity, call-site/build symbol where useful, causal or synchronization context, recorded value/order, and integrity framing. Stable task IDs derive from parent logical ID plus creation sequence within controlled semantics, not only native IDs.

Recording “read returned 5” is ambiguous if code performs two similar reads. Replay must match kind, logical operation, expected state/arguments, and position. Include an enabled-set or state landmark digest at important choices. Overly weak context misapplies events; overly strong address/timing context makes valid replay brittle.

Trace headers bind source/binary build ID, dependencies, configuration, architecture, endianness, runtime/OS, memory-model mode, checkpoint digest, input artifact digests, schema, recorder options, clocks/counters, and completion/integrity status.

### Checkpoints

Replay from program start may be too slow. Checkpoints capture address space or application/VM state plus trace offset and external-model state. Copy-on-write can reduce pause but requires a consistent cut. Threads, registers, mappings, file offsets, pending signals, virtual devices, runtime queues, and logical clocks may belong to the snapshot.

A checkpoint without intervening nondeterministic events cannot show how state arose. It accelerates replay; it does not replace the log. Checkpoint and log durability must be coordinated so the offset references complete frames.

Period balances pause, storage, recovery/replay latency, and failure risk. Branching from a checkpoint after diagnostic mutation creates a new execution with new nondeterminism; retain provenance linking it to the original prefix.

### Synchronization replay and data-race assumptions

For a data-race-free program under a suitable language model, reproducing external inputs and synchronization order can often determine ordinary memory observations. Log lock acquisitions, condition wake selection, atomic/volatile order or values as required, channel pairings, future completion, barriers, and thread lifecycle.

If unsynchronized conflicting accesses exist, different memory orders or read-from choices can change behavior between identical synchronization events. Faithful replay then needs to record/force relevant memory conflicts, serialize execution, use hardware support, or weaken fidelity. Detecting races during recording can select a slower mode, but detection completeness is itself evidence.

Language undefined behavior defeats a clean replay claim. Reproducing one operational manifestation of undefined behavior does not legitimize the program. Compiler transformations and weak-memory behaviors must match or be captured at a lower boundary.

### System calls and external data

Intercept calls that observe or affect the external world. Record return codes, output buffers, partial counts, errors, metadata, blocking/completion order, and signal interruption. A repeated `read` must receive the same bytes at the same logical call even if the real file or socket changed.

During replay, suppress writes or redirect them to a sandbox/model. Reissuing email, payment, actuator, filesystem, or network effects is unsafe and may also perturb return values. Validate intended write arguments against the trace and return recorded results where appropriate.

Memory-mapped files, shared memory, async I/O, ioctls, futexes, polling readiness, DNS, environment, process control, and device-specific behavior need dedicated modeling. “We intercept syscalls” is not a proof that every input crosses that interface.

### Signals, interrupts, and time

An asynchronous signal value is insufficient; replay must deliver it at a compatible execution point. Instruction/event counters, branches retired, logical epochs, or safe points can locate delivery. Hardware performance counters may themselves have platform constraints and nondeterministic skid.

Record wall/monotonic clocks, timer expirations, sleeps, deadlines, and time-zone/locale inputs if observed. Replay usually supplies virtual recorded time rather than waiting in real time. If timing is the property—real-time deadline or race—the debugger needs separate physical timing evidence; ordinary replay changes performance.

Nested signals, masking, handler reentrancy, cancellation, and interrupted syscalls must match. Unsupported signals or nondeterministic instructions should fail recording or mark the trace nonreplayable.

### Executable context-checked replay

The following sequential model records the enabled logical operations alongside each chosen transition for a two-task lost update. Replay validates context before applying the choice. A deliberately corrupted context stops at choice 2. This is a finite teaching model, not a thread runtime, recorder, memory-model implementation, or security log.

<!-- bijux-verify: {"id":"context-checked-replay","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"recorded_choices=4\nrecorded_final=1\nreplay_status=matched\nreplay_final=1\ndivergence=choice 2: expected ['A:W'] actual ['A:W', 'B:W']\n","stderr":""}} -->
```python
def enabled(state):
    operations = []
    for task in ["A", "B"]:
        step = state["step"][task]
        if step == 0:
            operations.append(f"{task}:R")
        elif step == 1:
            operations.append(f"{task}:W")
    return operations


def apply(state, operation):
    task, action = operation.split(":")
    if action == "R":
        state["private"][task] = state["shared"]
    else:
        state["shared"] = state["private"][task] + 1
    state["step"][task] += 1


def fresh_state():
    return {
        "shared": 0,
        "private": {"A": 0, "B": 0},
        "step": {"A": 0, "B": 0},
    }


def record(schedule):
    state = fresh_state()
    trace = []
    for operation in schedule:
        context = enabled(state)
        trace.append({"enabled": context, "selected": operation})
        apply(state, operation)
    return trace, state["shared"]


def replay(trace):
    state = fresh_state()
    for index, event in enumerate(trace):
        context = enabled(state)
        if event["enabled"] != context:
            return f"choice {index}: expected {event['enabled']} actual {context}", None
        if event["selected"] not in context:
            return f"choice {index}: selected operation unavailable", None
        apply(state, event["selected"])
    return "matched", state["shared"]


schedule = ["A:R", "B:R", "A:W", "B:W"]
trace, recorded_final = record(schedule)
status, replay_final = replay(trace)
corrupt = [dict(event) for event in trace]
corrupt[2] = {"enabled": ["A:W"], "selected": "A:W"}
divergence, _ = replay(corrupt)

print(f"recorded_choices={len(trace)}")
print(f"recorded_final={recorded_final}")
print(f"replay_status={status}")
print(f"replay_final={replay_final}")
print(f"divergence={divergence}")
```

The exact enabled list is appropriate for this tiny model. A production context may use stable digests plus diagnostic details, with collision and compatibility assumptions stated.

### Fidelity versus logging overhead

Record every conflicting memory access and fidelity improves while overhead/log volume rise. Record only synchronization and assume race freedom for lower overhead. Record partial execution sketches and spend diagnosis time exploring missing choices. Record outputs and solve for an output-equivalent path. These are engineering points, not a monotonic ladder where one is always best.

Buffers batch log writes, but a crash may lose the tail. Sequence frames, checksums/MACs, durable watermarks, and completeness markers distinguish intact prefixes from complete traces. Compression can exploit repeated event kinds, deltas, per-thread streams, and deterministic values; the decoder is part of the trusted base.

Backpressure must not silently drop events. Options include slowing the application, switching modes, rotating within retention guarantees, or marking replay disabled. Sampling event logs cannot support faithful replay unless omitted events are provably derivable.

### Replay divergence

Divergence causes include changed binary/library/configuration, corrupt or incomplete trace, missed nondeterminism, unstable identity, unsupported instruction/syscall, different memory semantics, recorder bug, and intentional diagnostic perturbation. Stop at the first mismatch and report trace position, expected event/context, actual state, build/runtime metadata, and last matching landmark.

Do not resynchronize by scanning forward for a similar event unless the replay mode explicitly implements a sound partial/output-equivalent search. Silent recovery destroys causal trust. A diagnostic tool may offer “branch from here,” clearly ending faithful replay.

Replay success should validate landmarks and final outcomes, not merely process exit. Hashes can detect differences but need canonical scope and collision assumptions. Compare memory/register/event histories at sampled checkpoints when fidelity requires them.

### Output-equivalent and probabilistic replay

Faithful multiprocessor replay is costly in the presence of data races. ODR observed that some debugging goals can accept an execution with the same recorded outputs and used constraints/search rather than reproducing every race. This weaker contract may reveal the failure while producing a different internal history.

PRES records execution sketches and uses unsuccessful diagnosis replays as feedback to search remaining nondeterminism. It trades production overhead for multiple replay attempts. Once a failing schedule is found it can be constrained more strongly, but the original sketch never becomes a complete faithful log retroactively.

Report attempt budget, search strategy, failure identity, and whether the found execution is original-equivalent by output only. Do not use reconstructed internal causality as forensic fact beyond the fidelity contract.

### Reverse debugging and analysis

To step backward, locate a checkpoint before the target, replay forward with instrumentation, and repeat using progressively narrower endpoints. Hierarchical checkpoints and event indices reduce cost. Watchpoints can search the last write that changed a value.

Instrumentation during replay can be heavier than during production because it need not preserve original timing, provided it does not change modeled semantics. External outputs remain suppressed. Debugger reads are observations; debugger writes branch execution.

Trace slicing and minimization remove irrelevant inputs/ordering constraints while retaining the failure. Revalidate after each deletion and preserve failure identity. A minimal witness is not necessarily the unique cause.

### Compatibility and retention

Replay against the exact binary/container/VM image is easiest. Symbolic application events can survive compatible upgrades only with explicit schema migration and semantic adapters. Never reinterpret an old numeric event kind using a new meaning.

Retain executable, debug symbols, dependencies, configuration, input snapshots, trace/checkpoints, recorder/replayer version, hardware/OS requirements, and provenance. Test restoration periodically; an archived trace without runnable dependencies is not replay evidence.

Retention competes with storage cost, privacy deletion, security incident holds, and legal rules. Content-addressed deduplication must respect encryption and access domains. A deletion request may make exact replay intentionally impossible; record that governance outcome rather than keeping shadow copies.

### Privacy, security, and integrity

Traces can contain credentials, personal data, file/network contents, memory, cryptographic keys, and business secrets. Minimize capture at the boundary, tokenize/redact only when replay semantics survive, encrypt in transit/at rest, separate keys, enforce least privilege, audit access, and expire data.

Redaction after capture may leave copies in checkpoints or compressed streams. Field-aware capture is safer than regex scrubbing. Security replay may require sensitive evidence, so use governed secure enclaves or isolated analysis environments.

An attacker may tamper with logs to conceal behavior. Use append-only remote storage, frame chaining/MAC/signatures, trusted timestamps where needed, durable sequence numbers, and independent recorder placement under the threat model. Integrity proves trace custody, not that instrumentation captured every event.

Never replay untrusted traces with a privileged unsafe decoder. Treat trace parsing and guest analysis as hostile-input processing with bounds and isolation.

### Distributed replay

Across processes/nodes, record external inputs and message identity/content/order plus local nondeterminism. Lamport happens-before gives causal constraints; a total wall-clock order is neither necessary nor reliable. TCP byte streams, retries, duplicates, timeouts, leader elections, storage responses, and membership changes need modeling.

Central logging can bottleneck; per-node logs require clock-independent causal correlation and a consistent snapshot/cut. Replaying real peers makes results depend on current state; simulate or record them. Partial failures and nondeterministic availability create large search spaces.

Application-integrated deterministic state machines can log commands and deterministic choices compactly, but hidden time/random/thread effects break replay. Distributed replay is developed more deeply in later systems programs.

### Verification and repair

Test the recorder with known nondeterministic programs across system calls, signals, threads, races, memory mappings, async I/O, process creation, clocks, randomness, JIT/GC, crashes, and supported hardware. Compare landmarks and outputs over repeated replay. Deliberately corrupt frames and change binaries to verify early divergence.

Maintain golden traces per schema, round-trip tests, fuzzed hostile trace parsers, checkpoint/log crash matrices, log-overflow/backpressure tests, privacy scans, and key-rotation/restoration drills. Measure record slowdown, log rate, tail loss window, checkpoint pause, replay speed, divergence rate, and successful replay coverage by workload.

After a code repair, the original trace may diverge because code changed. Build a regression input/schedule at the highest stable semantic level, or replay the old binary to diagnose and use a translated/minimized test for the new binary. Rerun systematic concurrency tests, race/memory tools, and production-realistic stress. One eliminated witness does not prove the defect class absent.

### High-stakes use

Replay can explain an observed medical, industrial, transport, financial, or security incident but cannot reproduce physical reality automatically. Sensor calibration, actuator mechanics, network environment, human action, timing, and unrecorded devices require separate evidence. Output-equivalent reconstruction is inappropriate as factual forensic history unless labeled.

Define evidentiary chain of custody, clock and identity semantics, completeness, authorized access, retention, independent tooling validation, and uncertainty. Named domain, incident-response/forensic, concurrency/runtime, hardware/real-time, security/privacy, quality/regulatory, operations, human-factors, and independent safety/assurance reviewers must approve intended use; none is claimed here.

## Definitions and Notation

- `C`: initial compatible checkpoint.
- `L=e_0…e_n`: ordered replay trace.
- `δ(s,e)`: deterministic transition from state s under recorded event e.
- `ctx(s)`: expected event-resolution context at state s.
- `O(x)`: declared observation/fidelity projection of execution x.
- `x ≡_O y`: executions x and y are equivalent under O, not necessarily internally identical.
- `hb`: happens-before relation among events.
- `B`: build/runtime/environment compatibility manifest.
- `H_i`: integrity/state landmark after event interval i.
- `D(k)`: divergence at first incompatible choice k.

Faithful scoped replay seeks state/history equality under its machine model. Output replay seeks `recorded ≡_O replayed`, a strictly weaker statement when O omits internal events.

## Mechanisms, Invariants, or Proof Structure

### Replay induction

Base: restore C and verify B. Inductive step: assume replay state agrees through event k. Resolve the unique compatible event identity/context, inject the recorded input/order, and apply deterministic δ. The next state agrees. If resolution, deterministic semantics, or completeness fails, stop with D(k); continuing would invalidate induction.

### Synchronization-replay obligation

Show every cross-thread communication is mediated by logged/reproduced synchronization and ordinary accesses are data-race-free under the same language/memory model. Then synchronization order plus external inputs determines relevant reads. A race, unsafe foreign access, or changed model breaks the premise.

### Checkpoint/log consistency

Checkpoint records trace offset q only after state and all frames through q form a durable consistent cut. Recovery accepts a checkpoint only if digest/integrity chain and referenced frames validate. Frames after the durable watermark are an incomplete suffix, never silently assumed present.

### Output-equivalence obligation

Define O and failure identity precisely. Constrain search so any accepted execution produces recorded O and satisfies the current binary's semantics. State explicitly which internal events may differ and prohibit forensic causal claims about those omitted events.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| Application event replay | compact, semantic, portable | trusts complete instrumentation |
| Synchronization replay | lower volume for race-free programs | fails on unlogged races/model changes |
| Memory-order replay | high multiprocessor fidelity | overhead and hardware/runtime complexity |
| Process syscall/signal replay | unmodified application support | OS/CPU constraints and shared-memory boundary |
| Full VM replay | broad guest and forensic visibility | heavyweight image/device/platform scope |
| Output-deterministic replay | lower recording burden | different internal history |
| Probabilistic/sketch replay | low production overhead | multiple attempts; no first-run fidelity |
| Controlled test scheduler | explores schedules before deployment | not replay of a production execution |

Choose based on the question the replay must answer. Preserve the fidelity label in every trace, UI, report, and downstream inference.

## Failure Modes and Misconceptions

- **“Same input replays threads.”** Scheduling, external events, and memory choices remain.
- **“Synchronization order is always enough.”** It assumes appropriately race-free communication.
- **“Timestamps order events.”** clocks drift/collide and timing may change under recording.
- **“A value log identifies the event.”** Context and stable identity are required.
- **“A checkpoint is replay.”** It lacks transitions between saved states.
- **“Replay can safely perform writes.”** It may duplicate irreversible effects.
- **“Changed binaries are close enough.”** event identities and semantics can diverge.
- **“Hash match proves faithful history.”** Only the hashed projection is compared.
- **“Output-equivalent means identical.”** Internal causality may differ.
- **“Probabilistic replay failed, so the report was wrong.”** incomplete sketches may need more search.
- **“Debugger mutation can rejoin replay.”** it creates a different execution unless correspondence is proved.
- **“Recording does not perturb behavior.”** overhead and serialization can mask or create timing.
- **“Encrypted logs are private.”** access, minimization, checkpoints, metadata, and retention still matter.
- **“Integrity means completeness.”** authenticated frames do not prove missed events were captured.
- **“One replayed bug proves the fix.”** broader schedules and defect variants remain.

## Worked Examples

### Example 1

**Lost update.** Context-checked trace replays A-read, B-read, A-write, B-write to final 1. **Conclusion:** stable choices reproduce one finite race witness.

### Example 2

**Trace mismatch.** Recorded enabled set omits B's write; replay stops at choice 2. **Conclusion:** divergence is evidence, not an inconvenience to hide.

### Example 3

**Race-free locks.** Same external input and mutex acquisition order reproduce protected state. An unprotected statistics counter remains outside fidelity. **Conclusion:** state the race-free boundary.

### Example 4

**Socket input.** Replay supplies recorded bytes and partial-read boundaries without contacting the server; outbound requests are validated then suppressed. **Conclusion:** values and interface behavior both matter.

### Example 5

**Signal delivery.** SIGTERM is recorded at a logical/instruction event and replayed with the same mask/handler state. **Conclusion:** asynchronous input needs a delivery position.

### Example 6

**Changed library.** A new allocator changes call path and logical event context. Replay reports build mismatch before execution. **Conclusion:** compatibility prevents false diagnosis.

### Example 7

**Output-equivalent failure.** Search finds a different race history that emits the same assertion and response bytes. **Conclusion:** useful debugging evidence can be weaker than faithful history.

### Example 8

**Crash tail.** Authenticated frames end at durable watermark 900 although memory buffered through 940. Trace is labeled replayable only through 900. **Conclusion:** integrity and completeness status must be explicit.

### Example 9

**Sensitive trace.** Network buffers include health data and credentials. Field-aware capture, encryption, isolated access, audit, and deletion policy are required. **Conclusion:** debugging artifacts are governed data.

### Example 10

**Autonomous transport incident.** Replay binds controller binary, sensors/messages, time, task order, device/vehicle model, operator input, outputs, integrity, and chain of custody, yet cannot recreate road physics from unrecorded state. Named transport/domain, control/real-time, hardware, concurrency/runtime, forensic, cybersecurity/privacy, human-factors, operations, regulatory, and independent safety reviewers must approve use and uncertainty; none is claimed here. **Conclusion:** replay evidence is not complete physical truth.

## Cross-Program Connections

- **Operating systems:** syscalls, signals, scheduling, performance counters, processes, and VMs define broad replay boundaries.
- **Programming languages:** memory models, managed tasks, JIT, GC, unsafe code, and exceptions determine hidden nondeterminism.
- **Distributed systems:** messages, causal order, partial failure, and consistent cuts extend traces across nodes.
- **Security:** protected below-guest logging, integrity chains, hostile trace parsing, and custody enable forensics.
- **Testing:** schedule exploration and race tools complement one production witness.
- **Storage:** checkpoints, WAL-like frames, durability watermarks, compression, and retention govern recoverability.
- **Privacy engineering:** memory and I/O traces require minimization, access, encryption, and deletion.
- **Safety engineering:** fidelity, uncertainty, independent validation, and physical evidence constrain incident conclusions.

## References

1. Thomas J. LeBlanc and John M. Mellor-Crummey, “Debugging Parallel Programs with Instant Replay,” *IEEE Transactions on Computers* 36(4), 1987. <https://doi.org/10.1109/TC.1987.1676929>
2. George W. Dunlap, Samuel T. King, Sukru Cinar, Murtaza A. Basrai, and Peter M. Chen, “ReVirt: Enabling Intrusion Analysis Through Virtual-Machine Logging and Replay,” OSDI 2002. <https://www.usenix.org/conference/osdi-02/revirt-enabling-intrusion-analysis-through-virtual-machine-logging-and-replay>
3. George W. Dunlap, Dominic G. Lucchetti, Michael A. Fetterman, and Peter M. Chen, “Execution Replay of Multiprocessor Virtual Machines,” VEE 2008. <https://doi.org/10.1145/1346256.1346273>
4. Soyeon Park et al., “PRES: Probabilistic Replay with Execution Sketching on Multiprocessors,” SOSP 2009. <https://doi.org/10.1145/1629575.1629593>
5. Gautam Altekar and Ion Stoica, “ODR: Output-Deterministic Replay for Multicore Debugging,” SOSP 2009. <https://doi.org/10.1145/1629575.1629594>
6. Kaushik Veeraraghavan, Dongyoon Lee, Benjamin Wester, Jessica Ouyang, Peter M. Chen, Jason Flinn, and Satish Narayanasamy, “DoublePlay: Parallelizing Sequential Logging and Replay,” ASPLOS 2011. <https://doi.org/10.1145/1950365.1950370>
7. Robert O'Callahan, Chris Jones, Nathan Froyd, Kyle Huey, Albert Noll, and Nimrod Partush, “Lightweight User-Space Record And Replay,” 2016. <https://arxiv.org/abs/1610.02144>
8. Leslie Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,” *Communications of the ACM* 21(7), 1978. <https://doi.org/10.1145/359545.359563>
9. Microsoft, *Coyote Documentation: Replay Executions*; retrieved 2026-08-29. <https://microsoft.github.io/coyote/get-started/using-coyote/#replaying-an-execution>
10. rr Project Contributors, *rr: Record and Replay Framework*; retrieved 2026-08-29. <https://github.com/rr-debugger/rr>

## Exercises

### Exercise 1

Define faithful, synchronization, output-equivalent, and probabilistic replay. Give a debugging question each can and cannot answer.

### Exercise 2

Design a replay trace schema for a multithreaded service using locks, atomics, timers, signals, files, and sockets. Include identity, context, compatibility, integrity, and divergence.

### Exercise 3

Prove synchronization replay sufficient for a small race-free program, then add one unsynchronized access and show which premise fails.

### Exercise 4

Design checkpointing, buffering, privacy, retention, and reverse-debugging operations for a production recorder with bounded overhead and crash-tail loss.

### Exercise 5

A regulated medical device incident may use replay evidence. Specify fidelity, physical boundaries, validation, security/privacy, custody, uncertainty, and mandatory review.

## Answers to the Exercises

### Answer 1

Faithful replay reconstructs the declared original history/state and can answer “which write supplied this read?” if memory read-from order is in scope; it cannot answer unrecorded physical timing. Synchronization replay reproduces external input and synchronization order and can diagnose lock/channel protocol failures in a race-free model; it cannot faithfully resolve an unlogged data race. Output-equivalent replay finds any valid execution with the same specified outputs and can reproduce an assertion cheaply; it cannot establish original internal causality. Probabilistic/sketch replay records partial constraints and searches at diagnosis, useful when production overhead must be low; failure within a finite attempt budget neither disproves the incident nor supplies first-attempt fidelity. Every artifact must state O and unresolved behavior.

### Answer 2

Header: schema/fidelity, build and dependency digests, runtime/OS/architecture/memory model, configuration/input/checkpoint digests, recorder modes, integrity key/version, and completeness watermark. Assign process/task IDs from controlled parent creation, plus monotonic event positions. Events contain kind/version, task/operation/call identity, arguments/context or enabled/happens-before landmarks, recorded return/buffer/error/order, and frame checksum/MAC chain. Log lock/atomic/condition/channel/lifecycle decisions; timer/clock results; signal kind and delivery coordinate/mask; file/socket read contents and boundaries; readiness and errors; and validate/suppress writes. Replay rejects incompatible headers and stops at first context mismatch with expected/actual details. Bound lengths before parsing, encrypt/access-audit sensitive frames, and mark tail/instrumentation escapes explicitly.

### Answer 3

Assume threads communicate only through modeled locks/atomics, all ordinary conflicting accesses are ordered by happens-before, deterministic thread-local computation, identical initial state/external inputs, and reproduced synchronization choices. Induct over synchronization segments: each segment begins with identical visible state, computes deterministically, and the same next communication publishes/observes the same values, yielding identical scoped state. Add an unsynchronized writer and reader of x. They can occur in different order between identical lock events, so the reader may observe old or new x. The premise that every communication/conflict is mediated by reproduced synchronization fails. Record/force the relevant memory order, remove the race, serialize, or weaken fidelity; replaying one outcome does not legalize undefined behavior.

### Answer 4

Use copy-on-write consistent checkpoints with registers/runtime queues, virtual external state, and durable log offset. Frame per-thread buffers with global/causal IDs, checksums/MAC chain, compression, bounded queues, and backpressure; never silently drop. Flush durable watermarks and atomically link checkpoint to verified frames. On crash label only the durable prefix complete and expose tail-loss duration. Capture fields selectively, encrypt with separated keys, isolate analysts, audit access, scan checkpoints as well as logs, and enforce retention/legal holds/deletion. Keep build images/symbols and restoration tests. Reverse debugging chooses a checkpoint before target, replays forward under read-only instrumentation, and binary-searches events; debugger mutation creates a branch. Monitor record slowdown/log rate/pause/storage and choose checkpoint period from replay-latency SLO without weakening completeness silently.

### Answer 5

Define whether replay covers application decisions, runtime scheduling, device/OS inputs, exact memory, or only output equivalence. Bind certified software/configuration, patient/device state, clocks, sensors, commands, alarms, communications, operator input, failures, checkpoint, and integrity metadata. State unrecorded physical processes—sensor calibration, infusion mechanics, environment, human behavior—and never infer them from software output alone. Validate recorder/replayer independently with fault, signal, timing, concurrency, crash, corruption, compatibility, and hardware-in-loop cases; preserve original evidence and branch analyses. Suppress actuators/external writes during replay. Encrypt/minimize patient data, isolate access, audit/export, govern deletion and legal hold, and maintain signed custody/watermarks. Report divergence, missing tail, model uncertainty, and output-equivalent reconstructions explicitly. Named clinical, biomedical/device, real-time/control, hardware, concurrency/runtime, forensic, cybersecurity/privacy, human-factors, quality/regulatory, operations, and independent safety reviewers must approve intended evidentiary use; replay alone cannot establish physical causality or patient safety.
