---
module_id: CA-028
program: Computer Architecture
level: 1
module_number: 28
title: Pipeline Stalls and Flushes
status: complete
last_verified: 2026-09-04
---

# Pipeline Stalls and Flushes

## One-Page Review

### Governing question

How should a pipeline transform each stage when progress is temporarily impossible or work becomes invalid, so live tokens are held without duplication, bubbles are inserted deliberately, doomed tokens are killed promptly, and older permitted work still completes?

### Essential definitions

- A **stall** prevents selected pipeline state from advancing while its live token remains valid.
- A **hold** preserves a stage's validity, data, controls, identity and required output protocol state.
- A **bubble** is an invalid stage entry; inserting one consumes a cycle of capacity without representing an instruction.
- A **flush** or **kill** invalidates selected live tokens so they cannot perform later effects.
- **backpressure** communicates unavailable downstream capacity toward upstream producers.
- An **interlock** automatically stalls a consumer until a hazard clears.
- A **redirect** supplies a replacement fetch path and kills incompatible younger work.
- A **drain** stops new admission while allowing selected in-flight work to finish.
- A **replay** re-executes an operation under a proven idempotence and identity contract.
- A **freeze** is a coordinated hold over a declared stage set; it is not necessarily the whole pipeline.
- **valid/ready transfer** occurs when a valid sender and ready receiver agree on one token movement.
- A **skid buffer** preserves a token that arrives during registered backpressure latency.
- **event priority** determines the result when reset, fault, flush, response, stall and advance coincide.
- A **stall cycle** is a cycle whose useful progress is prevented by a named cause under a counting policy.
- A **flush penalty** is lost work/time caused by invalidation and correct-path refill, not merely the number of killed tokens.

### Central model, mechanism, or theorem

Let stage `j` hold `(v_j,x_j)`. Each edge applies exactly one coherent action selected by priority: reset/containment invalidates or initializes; kill sets `v_j'=0` for targeted identities; hold gives `(v_j',x_j')=(v_j,x_j)`; transfer captures `(1,x_{j-1})` when upstream valid and this stage accepts; otherwise the stage becomes/remains invalid. Older downstream stages may transfer while a younger upstream stage holds, creating a bubble between them. Correctness requires conservation of every non-killed token, suppression of every killed effect, exact age/path selection, and eventual progress under declared readiness assumptions.

### Critical invariants

- A hold preserves the complete live token bundle and any unaccepted protocol payload.
- A bubble has invalidity, not a fabricated no-op instruction with accidental effects.
- Each valid token transfers at most once across a boundary per cycle.
- Backpressure prevents overwrite when downstream lacks capacity.
- Kills dominate ordinary advance/hold for targeted tokens and cannot be undone by later readiness.
- Flush scope uses age/path identity and preserves older/resolving permitted work.
- Accepted non-cancellable requests remain tracked even when their owning instruction is killed.
- Late responses cannot revive a killed or reset token or alias a reused identity.
- Fault, redirect, interrupt, debug and reset priorities produce one permitted architectural path.
- Stall/flush counters use an explicit attribution policy and avoid double-counting overlapping causes.

### Common failures

Common failures include treating stall and bubble as synonyms, holding valid but not payload, holding upstream while overwriting a full downstream stage, freezing a stage that must accept a response, inserting the same token twice, letting stall beat a flush, flushing the redirecting instruction, clearing an outstanding request record too early, reissuing an accepted store after replay, using a no-op encoding as a bubble, losing exception metadata during a hold, deasserting valid while still claiming a request, double-counting simultaneous stall causes, and reducing cycles while lengthening the clock enough to lose performance.

### Compact example

An invented 2,000-instruction five-stage run has 2,004 ideal finite-run cycles. Raw counters attribute 120 data, 80 structural, 100 control and 300 memory stall cycles, but 50 cycles overlap; the union is 550, not 600. Actual 2,554 cycles at 1.45 ns take 3,703.30 ns, CPI 1.277 and 540.06 MIPS. An earlier redirect reduces the union to 530 cycles, yet a 1.50 ns clock yields 3,801.00 ns and 526.18 MIPS. Correct counting and time—not one counter—govern comparison.

### Connections

Stalls and flushes connect valid/ready protocols, data/structural/control hazards, caches and long units, precise exceptions, interrupts/debug/reset, replay, formal token conservation, counter design and performance attribution.

## Governing Question

Pipelines must sometimes wait and sometimes discard work. Waiting means the work remains live; discarding means it must never act again. Confusing those transformations causes token loss, duplication or wrong-path effects.

The design problem is per stage and per event. “Stall the pipeline” is too vague: which stages hold, which older stages advance, where does invalidity appear, what happens to accepted requests, and what wins if a redirect or fault occurs simultaneously?

## Why This Matters

Variable-latency memory and long arithmetic make holds routine. Branch recovery, faults and debug make kills routine. Their simultaneous corner cases are where apparently correct instruction tests often fail.

Global freezing can be correct but unnecessarily blocks independent progress or response acceptance. Fine-grained flow improves utilization but expands state and priority logic.

Performance reporting also depends on semantics. Hardware events often overlap, and a cycle may be attributable to multiple causes. Summing counters can exceed elapsed cycles unless attribution is defined.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace valid, age-tagged tokens through pipeline stages;
- distinguish data, structural and control hazards;
- interpret valid/ready and request/response protocols;
- explain precise commit, faults and redirects;
- compute finite-run CPI, latency and throughput.

Retrieve the exact pipeline/configuration and stage bundles; valid/ready/enable equations; storage capacity and skid buffers; every stall source; every kill/flush source; event-priority table; age/path/epoch representation and wrap bound; hazard/scoreboard state; branch resolution/redirect; cache/TLB/memory request and cancellation/replay rules; long-unit tags; exception/interrupt/debug/reset behavior; store/irreversible effect boundary; clock-gating interaction; assertions and formal assumptions; counters and attribution definitions; workload traces; synthesis/STA/area/power; tests/coverage; hardware/errata; and exact RTL, memory, tool, library and revision identities.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish hold, transfer, bubble insertion, kill, replay and drain;
2. derive per-stage next-state equations from valid/ready and event priority;
3. propagate backpressure without token loss, duplication or combinational loops;
4. insert an interlock bubble while older work advances;
5. flush exactly the intended age/path set;
6. handle outstanding non-cancellable requests and late responses safely;
7. integrate exceptions, redirects, interrupts, debug, reset and clock gating;
8. define and validate stall/flush performance counters;
9. prove token conservation, killed-effect suppression and progress;
10. compare remedies using elapsed instruction time and representative evidence.

## Core Exposition

### Define each stage as state

A stage is not just combinational logic; its boundary contains validity and a coherent token bundle. Write the next-state behavior for every event rather than relying on informal enable descriptions.

List all side effects driven from the stage. They must be gated by live, non-killed validity and any terminal handshake.

### Define normal transfer

In a valid/ready pipeline, a token crosses only when sender valid and receiver ready. The sender may simultaneously accept a replacement token if its own upstream transfer occurs.

The transfer event captures data, controls, identity and fault metadata together. Split enables that can disagree require proof or should be unified.

### Define hold

When a valid token cannot transfer, preserve every field needed later. If the stage presents an unaccepted request, hold address, data, mask, tag and attributes stable according to the interface.

Internal combinational recomputation may toggle, but the registered/output contract cannot change in a way that creates a different logical request or instruction.

### Define bubble insertion

Suppose a dependent token in decode must wait while the older execute token advances. Hold fetch/decode and set the newly freed execute entry invalid. This is a bubble.

Do not encode a bubble as an architectural no-op unless every control and exception path proves it harmless. A valid no-op is still an instruction and may retire/counter differently.

### Define flush/kill

Kill converts selected live tokens to invalid or killed state. It is irreversible for that token identity. The data bits may remain physically unchanged, but no forwarding, request, writeback, predictor training or commit may treat them as live.

Some accepted operations cannot be cancelled. Keep a killed outstanding record to consume their completion safely without architectural effect.

### Establish event priority

Construct a table for reset/integrity containment, oldest precise fault, redirect, debug/interrupt, response completion, local kill, stall and normal transfer. Priority can differ by stage, but global architectural outcome must agree.

For a targeted younger token, flush normally dominates stall. Otherwise a held wrong-path instruction can survive recovery.

### Preserve older progress

A front-end interlock need not freeze memory/writeback. Let older stages advance and retire while holding the consumer, subject to capacity and ordering.

This movement creates bubbles. Recompute forwarding/producer locations as older tokens move; do not retain stale selection codes.

### Propagate backpressure

A full blocked stage deasserts readiness upstream unless buffering can accept another token. Propagate capacity, not simply the downstream valid bit.

Combinational ready chains can cross many stages and form loops. Registered backpressure needs skid/elastic capacity to absorb tokens already launched.

### Size elastic buffers

A one-entry pipeline register can either hold its token or accept/replace it under a simultaneous outgoing transfer. A two-entry elastic/skid buffer can tolerate one cycle of delayed stop.

Prove occupancy bounds for every simultaneous enqueue/dequeue/kill case. Overflow is token loss; underflow can duplicate stale data.

### Interlock data hazards

When the youngest matching producer is unavailable, hold the consumer and upstream admission while older stages progress. Insert invalidity into the downstream slot unless it is independently occupied/blocked.

Release only when every operand can meet its use deadline or when the consumer is killed by an older event.

### Stall for structural capacity

If two live operations need one resource, grant according to policy and hold the loser. Atomic multi-resource allocation prevents a token from advancing with only part of its required capacity.

Arbitration state and payload remain coherent across stalls. Fairness assumptions and starvation bounds are separate from safety.

### Stall for variable latency

A cache miss or iterative unit holds/reserves state until matched success/error completion. Fixed-cycle countdowns are correct only for interfaces that guarantee them.

Other stages may continue if ordering, queues and response capacity permit. A global freeze is a design choice, not an inevitable consequence.

### Redirect control flow

On misprediction or resolved jump, select the actual PC and kill younger incompatible tokens. Advance fetch epoch/tag so late instruction responses from the old path are rejected.

Preserve the resolving instruction's permitted link/commit effect. A wrong target with correct direction still requires recovery.

### Handle precise faults

An older fault generally dominates younger redirects and stalls. Allow still-older permitted instructions to finish according to commit policy, suppress the faulting instruction's prohibited ordinary effects, kill younger work and enter trap once.

Exception metadata must hold with the token during backpressure. Losing cause/PC while retaining valid can produce an imprecise trap.

### Handle interrupts and debug

Interrupt acceptance chooses a documented instruction boundary. The design may drain older work, kill younger work and redirect to the handler while preserving outstanding protocol obligations.

Debug halt needs a defined quiescent point. “Pipeline stalled” does not imply no external request or clock-domain activity remains.

### Handle reset

Reset invalidates stages, reservations and effect enables. Accepted external operations follow cancellation/drain/tag-discard rules; reset cannot assume the peer forgets them.

Reset assertion/deassertion and clock gating must satisfy CDC/RDC and recovery/removal timing. Late completion cannot attach to a reused token after reset.

### Handle replays

Replay is valid only when re-executing does not duplicate an already accepted non-idempotent effect. Record whether request acceptance occurred and resume from the correct internal point.

Loads can often be retried under a memory contract; device reads and stores may not be. Address space and attributes affect replay safety.

### Coordinate clock gating

A held stage may be clock-gated if it need not capture kill, reset, response or wakeup events. Otherwise gating must include those events in its enable.

Never gate off the only state that can consume a response or clear a killed token. Verify clock-gate enable timing and scan/test behavior.

### Count stalls by opportunity

Define the denominator and opportunity. A front-end blocked cycle, issue slot lost and retirement slot empty are different metrics. A cycle can have data and memory causes simultaneously.

Use exclusive priority attribution, a bitset of simultaneous causes, or opportunity-cost analysis. Do not sum nonexclusive event counters and call the result elapsed stalls.

### Count flush cost

Count redirect events, killed tokens, cycles to first correct fetch and cycles to recovered retirement separately. Penalty varies with resolution point, cache state, width and queues.

Wrong-path instructions are not identical to lost cycles because some work overlaps useful older progress.

### Compute performance

For finite work, start with fill/drain and add the union of nonoverlapped lost cycles. `CPI_eff=cycles/retired`; `time=cycles*T_clk`. Report throughput and latency distributions.

Control changes can reduce stalls but lengthen ready/kill/redirect paths. Use implemented period and power rather than nominal cycle count alone.

### Assert token conservation

Assign symbolic identity at admission. Across a normal edge, every live token either remains once, transfers once, commits/traps once, or is killed once under policy. No identity appears twice or vanishes silently.

Outstanding physical operations may outlive killed architectural tokens; track them in a separate conservation domain until response disposal.

### Assert killed-effect suppression

For every killed identity, assert no future register/memory write, redirect, forwarding, training or retirement is attributed to it. Cover late completion and tag reuse.

For a store already committed/accepted at the architectural boundary, it may not be called killed afterward; define commit precisely.

### Prove progress

Under eventual downstream readiness, memory/unit completion and bounded higher-priority events, each live non-killed token eventually commits or traps. A correct hold can still deadlock forever.

Use ranking/occupancy arguments and isolate fairness assumptions. Check ready loops and circular reservations structurally.

### Gather layered evidence

Use event-priority review, per-boundary assertions, directed holds/bubbles/flushes, simultaneous hazard/fault/redirect cases, randomized latency/backpressure, reset/clock-gate/replay fault injection, symbolic conservation, ISA differential tests, formal safety/liveness/refinement, synthesis/STA/power, counter validation, workloads and errata.

Bind evidence to exact pipeline/configuration, protocols, RTL, memories, constraints, tools/libraries, counter definitions, binary/workload/seeds, hardware and firmware/errata. A passing simple stall trace does not validate all priority combinations.

## Definitions and Notation

- `j`: pipeline stage index.
- `v_j`, `x_j`: validity and coherent token bundle at stage `j`.
- `ready_j`: stage `j` has capacity to accept under the chosen protocol.
- `transfer_j`: one valid token crosses boundary `j`.
- `hold_j`: stage `j` preserves its current live state.
- `kill_j`: stage `j` invalidates its targeted token.
- `occ`: current occupancy of an elastic buffer.
- `e`: path epoch/generation used to reject stale work.
- `C_i`: set of cycles attributed to stall cause `i`.
- `|union C_i|`: distinct elapsed stall cycles across overlapping causes.
- **priority table:** complete mapping from simultaneous events to next-state actions.
- **token conservation:** live identities are neither duplicated nor silently lost.
- **late response:** completion arriving after redirect, kill or reset changed architectural ownership.
- **quiescent state:** declared condition with no prohibited in-flight effects for halt/update.
- **exclusive attribution:** each lost opportunity is charged to at most one primary cause.

## Mechanisms, Invariants, or Proof Structure

1. **State obligation:** each stage's valid and bundle fields form one coherent token state.
2. **Transfer obligation:** a boundary moves at most one token exactly on its defined handshake.
3. **Hold obligation:** stalled token/payload state remains stable and live.
4. **Capacity obligation:** backpressure/buffers prevent overwrite, overflow and underflow.
5. **Bubble obligation:** inserted invalidity cannot cause forwarding, requests, writes or retirement.
6. **Kill obligation:** targeted identities become permanently ineligible for ordinary effects.
7. **Age/path obligation:** flush preserves permitted older/resolving work and kills exactly incompatible work.
8. **Priority obligation:** every simultaneous reset/fault/redirect/response/stall/advance combination has one coherent result.
9. **Outstanding obligation:** accepted non-cancellable operations remain uniquely tracked through safe response disposal.
10. **Replay obligation:** retry/resume cannot duplicate an accepted effect or consume stale completion.
11. **Exception obligation:** fault metadata survives holds and produces one precise trap transition.
12. **Reset/debug obligation:** reset, interrupt and halt establish their declared safe architectural/protocol state.
13. **Progress obligation:** under explicit fairness, live non-killed tokens eventually advance, commit or trap.
14. **Timing obligation:** ready, enable, kill, response and clock-gate paths meet all implementation constraints.
15. **Evidence obligation:** counters, penalties and correctness claims bind to exact definitions/configuration/workloads.

## Alternatives and Trade-Offs

1. **Global freeze versus local backpressure:** global control is compact; local flow preserves unrelated progress.
2. **Rigid versus elastic stages:** rigid timing is predictable; elasticity handles variable latency with occupancy state.
3. **Combinational versus registered ready:** combinational ready reduces buffering; registered ready breaks paths and needs skid capacity.
4. **Hold versus replay:** hold preserves state directly; replay frees capacity and requires idempotence/recovery.
5. **Bubble versus valid no-op:** invalidity cleanly suppresses effects; no-op reuse can simplify datapath and pollute semantics/counters.
6. **Central versus distributed stall logic:** central priority is visible; distributed controls scale and risk inconsistency/loops.
7. **Flush bits versus epochs:** explicit kills target residents; epochs cheaply reject path responses and need wrap proof.
8. **Cancel versus drain request:** cancellation saves work if supported; drain/discard preserves interface compatibility.
9. **Drain versus immediate flush:** drain simplifies irreversible effects; immediate recovery lowers latency with more tracking.
10. **Fixed versus dynamic latency:** countdown is small for guaranteed timing; readiness handles caches/units variability.
11. **Flush-at-resolution versus commit:** early recovery improves time; later certainty reduces speculative repair.
12. **Clock-gate held state versus keep active:** gating saves power; active state readily captures recovery/response events.
13. **Exclusive versus multi-label counters:** exclusive causes sum cleanly; multi-label data preserves concurrency and needs union analysis.
14. **Early versus late redirect:** early reduces killed work; late may shorten clock and simplify operand readiness.
15. **Cycle reduction versus clock margin:** extra priority/forwarding can save stalls while lowering frequency.

## Failure Modes and Misconceptions

1. “A stall is a bubble.” A stall holds a live token; a bubble is invalid.
2. “Holding valid preserves the token.” Every payload/control/identity field must hold too.
3. “Hold every stage on any wait.” Older independent work may need to progress or accept responses.
4. “A full downstream stage can be overwritten if upstream is stalled next cycle.” Capacity must prevent the current transfer.
5. “Registered ready needs no buffer.” A token may already be in flight during stop latency.
6. “A bubble is just an ADD x0,x0,x0.” A valid instruction can retire and trigger unrelated controls.
7. “Flush and stall are interchangeable.” Flush destroys eligibility; stall preserves it.
8. “Stall should win because data must remain stable.” A targeted wrong-path token must be killed.
9. “Redirect flushes the resolving branch.” Its permitted link/commit normally survives.
10. “Clear all stages on any branch.” Older correct work must remain.
11. “Kill cancels an accepted bus request.” Only the bus contract determines cancellation.
12. “Free a killed tag immediately.” Late completion can alias reuse.
13. “Replay means issue again.” Accepted non-idempotent effects may duplicate.
14. “Load replay is always safe.” Device reads and attributes can make it unsafe.
15. “Exception data can be recomputed after a stall.” PC/cause/value identity may be lost or changed.
16. “Reset makes external completions disappear.” Peers may still return them.
17. “Clock-gated held state needs no wake event.” Kill/reset/response may need capture.
18. “One-hot enables prove token conservation.” Tokens can still vanish or duplicate across stages.
19. “No killed instruction retires, so flush is correct.” Killed memory/training/forwarding effects also matter.
20. “Safety proves progress.” A permanent hold can satisfy safety.
21. “All stall counters are additive.” Causes often overlap.
22. “Killed instruction count equals penalty.” Overlap and refill timing differ.
23. “Total pipeline depth equals flush latency.” Resolution, queues, fetch and cache determine recovery.
24. “Fewer cycles proves faster.” Clock period and power may worsen.
25. “Directed one-cause tests cover priority.” Simultaneous events create different next states.
26. “One configuration validates all pipelines.” Buffers, memories and options change control equations.

## Worked Examples

### Example 1

A load-use interlock holds fetch/decode while the older load advances; execute receives invalidity rather than a duplicate consumer.

### Example 2

A memory-stage request is valid but unaccepted. Backpressure holds address/data/tag stable and prevents execute from overwriting the stage.

### Example 3

A branch redirect and front-end stall coincide. Redirect kills the younger held tokens and changes epoch; stall cannot preserve them.

### Example 4

An older load fault and younger branch redirect coincide. The precise fault path wins and kills the younger branch/training.

### Example 5

A killed divide cannot cancel. Its tag remains allocated; completion is consumed without forwarding/writeback, then released once.

### Example 6

A registered-ready stage uses a skid entry so the final already-launched upstream token is captured after backpressure changes.

### Example 7

Reset occurs with an accepted fetch. Pipeline validity clears, while epoch/request tracking discards its late response safely.

### Example 8

A clock-gated held stage receives a flush. Flush is included in the gate wake/enable so the token cannot remain live.

### Example 9

Data and structural counters both assert for one blocked issue cycle. A cause bitset records both; union counting charges one elapsed cycle.

### Example 10

This deterministic model compares raw stall attribution, union counting and an early-redirect timing trade-off.

<!-- bijux-verify: {"id":"stall-flush-performance-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"naive_attributed_stalls=600 union_stalls=550 overlap_cycles=50\nbase_cycles=2004 actual_cycles=2554 effective_cpi=1.277 time_ns=3703.30 throughput_mips=540.06\nearly_redirect_cycles=2534 effective_cpi=1.267 time_ns=3801.00 throughput_mips=526.18\n"}} -->
```python
instructions = 2000
depth = 5
base_cycles = instructions + depth - 1

data = set(range(0, 120))
structural = set(range(100, 180))
control = set(range(200, 300))
memory = set(range(270, 570))
causes = [data, structural, control, memory]
naive = sum(len(cause) for cause in causes)
union = set().union(*causes)

actual_cycles = base_cycles + len(union)
period_ns = 1.45
time_ns = actual_cycles * period_ns

early_control = set(range(200, 250))
early_union = set().union(data, structural, early_control, memory)
early_cycles = base_cycles + len(early_union)
early_period_ns = 1.50
early_time_ns = early_cycles * early_period_ns

print(f"naive_attributed_stalls={naive} union_stalls={len(union)} overlap_cycles={naive - len(union)}")
print(f"base_cycles={base_cycles} actual_cycles={actual_cycles} effective_cpi={actual_cycles / instructions:.3f} time_ns={time_ns:.2f} throughput_mips={1000 * instructions / time_ns:.2f}")
print(f"early_redirect_cycles={early_cycles} effective_cpi={early_cycles / instructions:.3f} time_ns={early_time_ns:.2f} throughput_mips={1000 * instructions / early_time_ns:.2f}")
```

The cause sets and periods are invented and assume each set element represents one lost opportunity. Real evaluation needs exact event definitions, trace correlation, physical timing and workload evidence.

## Cross-Program Connections

- **Concurrent Systems:** valid/ready, backpressure, buffering, fairness and deadlock are message-flow properties.
- **Data Structures:** FIFOs, tags, epochs and scoreboards preserve outstanding identities.
- **ISA:** precise trap and sequential commit determine which tokens may survive.
- **Operating Systems:** interrupts, debug, reset and performance counters depend on quiescence/attribution.
- **Security Engineering:** killed and stale-path effects must not cross architectural or threat boundaries.
- **Formal Methods:** symbolic conservation, priority, killed-effect and liveness properties expose corner cases.
- **Performance Engineering:** overlapping counters, CPI, penalty, frequency and energy require explicit denominators.
- **Systems Engineering:** protocol, configuration, evidence and errata ownership span components and lifecycle.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), architectural instruction, PC, memory and exception outcomes refined by pipeline control; retrieved 2026-09-04.
2. lowRISC, [Ibex Pipeline Details](https://ibex-core.readthedocs.io/en/latest/03_reference/pipeline_details.html), current stalls, forwarding, branch and multicycle behavior; retrieved 2026-09-04.
3. lowRISC, [Ibex Instruction Decode and Execute](https://ibex-core.readthedocs.io/en/latest/03_reference/instruction_decode_execute.html), current controller and execution-stage behavior; retrieved 2026-09-04.
4. lowRISC, [Ibex Exceptions and Interrupts](https://ibex-core.readthedocs.io/en/latest/03_reference/exception_interrupts.html), current exception, interrupt and debug priority context; retrieved 2026-09-04.
5. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), integrated core configuration, security, alerts and verification context; retrieved 2026-09-04.
6. Berkeley Architecture Research, [BOOM Branch Prediction](https://docs.boom-core.org/en/latest/sections/branch-prediction/index.html), current open redirect and branch-recovery concepts; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), pipeline stall/flush teaching resources; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), independent executable ISA semantics for commit/trap comparison; retrieved 2026-09-04.

## Exercises

### Exercise 1

Write per-stage next-state rules for a three-stage valid/ready pipeline supporting normal transfer, data interlock, branch flush, response completion and reset.

### Exercise 2

Design a registered-backpressure boundary with a skid buffer. State occupancy, simultaneous enqueue/dequeue and flush invariants.

### Exercise 3

Analyze a killed non-cancellable store or long-unit request. Define commit, tracking, tag reuse, response disposal and reset behavior.

### Exercise 4

Recompute the executable union-stall example and propose a hardware-counter schema that supports both exclusive and multi-cause analysis.

### Exercise 5

Write a verification plan for all simultaneous stall, flush, fault, response, debug and reset cases in a configurable pipeline.

## Answers to the Exercises

### Answer 1

For each stage, reset/containment safely invalidates first; an age-targeted older fault/redirect kill invalidates next; a held valid token remains bit-for-bit coherent; otherwise a valid-ready upstream handshake captures exactly one bundle; absent capture leaves invalidity. Response completion may make a waiting token ready/result-valid but cannot bypass higher-priority kill.

A data interlock holds front/consumer state and inserts invalidity only into a freed downstream slot while older work advances. Branch recovery preserves older/resolving work, kills younger identities and updates PC/epoch atomically. Assert token conservation across every priority combination.

### Answer 2

Use primary and skid entries with occupancy 0..2. Receiver ready reflects capacity for the current edge plus any outgoing transfer. If backpressure was registered one cycle late, capture the already-launched token into the free skid entry. Simultaneous dequeue/enqueue preserves occupancy; flush removes only targeted identities and compacts/selects entries consistently.

Assert bounds, no duplicate identity, FIFO order for survivors, stable blocked output, exact handshakes, and that killed entries never emerge. Ready must have no combinational cycle; reset invalidates both entries and handles external obligations separately.

### Answer 3

If a store request's acceptance is its architectural commit boundary, it cannot later be killed; younger recovery must preserve the committed prefix. If acceptance is provisional, the memory protocol must provide transactional cancellation—ordinary replay assumptions are insufficient. For a non-cancellable long unit, mark the operation killed but retain outstanding tag ownership.

Consume late response once without write/forward/commit, then release. Do not reuse tag/epoch while alias is possible. Reset drains/discards under the peer contract. Assertions cover one acceptance, no duplicate request, one disposal, no killed effects and safe release.

### Answer 4

The raw cause counts sum to 600, but set union contains 550 distinct cycles: 50 are overlaps. With 2,004 base cycles, total is 2,554 at 1.45 ns, or 3,703.30 ns/540.06 MIPS. Early redirect gives 2,534 cycles but 1.50 ns, or 3,801.00 ns/526.18 MIPS.

Expose per-cycle cause bits plus a primary exclusive cause selected by documented priority, opportunity denominator, retired count, elapsed cycles and redirect-to-fetch/retire latency histograms. Validate against trace windows. Preserve simultaneous bits for union analysis and exclusive count for additive summaries.

### Answer 5

Enumerate the event-priority Cartesian product per stage, pruning only proven impossible combinations. Directed and formal cases cover full/empty buffers, held payload, simultaneous transfers, dependency/structural/memory wait, older/younger faults and redirects, late responses, replay, tag wrap, clock gating, interrupt/debug and reset.

Use symbolic token IDs for conservation/order, killed-effect assertions, protocol stability/uniqueness, precise commit/trap comparison and progress under fairness. Run random backpressure/fault injection, ISA differential tests, CDC/RDC, synthesis/STA/power and counter-trace validation on exact configurations/workloads. Bind sources, constraints, tools, seeds, hardware and errata. Internal evidence is not independent certification.
