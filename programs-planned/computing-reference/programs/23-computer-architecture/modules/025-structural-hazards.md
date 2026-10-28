---
module_id: CA-025
program: Computer Architecture
level: 1
module_number: 25
title: Structural Hazards
status: complete
last_verified: 2026-09-04
---

# Structural Hazards

## One-Page Review

### Governing question

When overlapping instructions demand the same finite hardware capability, how can a processor detect the conflict, choose a correct winner, preserve every losing token, and decide whether stalling, scheduling, pipelining, banking or duplication is the best remedy?

### Essential definitions

- A **structural hazard** occurs when concurrent operations require more of a resource capability than the implementation can provide in that cycle.
- A **resource** is a unit, port, path, queue entry, bandwidth budget or protocol opportunity with finite capacity.
- **demand** is the set of resource uses requested by live operations in a cycle.
- **capacity** is the compatible number/type of uses the resource contract can accept in that cycle.
- A **conflict** exists when compatible demand cannot be mapped within capacity.
- **arbitration** selects which eligible requester receives capacity now.
- **backpressure** preserves losing requesters until capacity becomes available.
- A **port** is an independently usable access interface under a specified operation/timing contract.
- A **bank** serves addresses mapped to it; different banks may operate concurrently while same-bank requests conflict.
- A **pipelined unit** may accept a new operation before an older one completes if initiation interval permits.
- **latency** is cycles from acceptance to result; **initiation interval** (`II`) is cycles between accepted operations.
- **replication** creates additional resource instances; **multiporting** adds simultaneous access capability to one logical resource.
- A **structural stall** is a delay caused by unavailable implementation capacity, not by a data or control dependency.
- A **resource reservation** records future or outstanding occupancy.
- **work conservation** means arbitration does not leave usable capacity idle while a compatible eligible request waits.

### Central model, mechanism, or theorem

For resource `r` in cycle `t`, let live requests be `D_r(t)` and legal service slots be `K_r(t)`. Allocation `A_r(t)` must map at most one accepted request to each compatible slot, grant no nonexistent request, and preserve each ungranted live token. If no legal injective mapping covers all demand, a structural hazard exists. Correct handling either changes the schedule/capacity or stalls selected operations; it must not drop, duplicate, reorder beyond policy, or partially issue a multi-resource operation. Performance follows the distribution of conflicts, not merely the presence of a shared block.

### Critical invariants

- Every grant names a live eligible request and a compatible resource slot.
- No slot accepts more operations than its port/initiation contract permits.
- An operation requiring several resources advances only when its grant set is atomic or safely reserved.
- Ungranted tokens remain valid and stable under backpressure.
- Arbitration priority cannot overwrite age, exception or commit ordering rules.
- Requests accepted once are not recreated as duplicate architectural effects.
- Responses return to the correct token through tags or unambiguous ordering.
- Bank/port selection uses the definitive address and operation type.
- Fairness claims state assumptions and bound or measure starvation.
- Resource remedies are validated for timing, area, power and workload behavior.

### Common failures

Typical failures include calling every pipeline stall structural, counting memory boxes instead of ports, assuming two reads and one write from a register file are free, ignoring same-bank conflicts, confusing unit latency with initiation interval, granting a multi-resource operation halfway, changing arbiter selection while stalled, dropping a losing requester, duplicating a store after re-arbitration, returning an untagged result to the wrong instruction, starving low priority traffic, adding a bypass that becomes the new critical resource, duplicating a unit without duplicating routing/writeback capacity, and comparing ideal capacity without representative conflict traces.

### Compact example

In an invented five-stage scalar pipeline running 200 instructions, a unified single-port instruction/data memory conflicts on each of 60 data accesses. Base fill/drain is 204 cycles; serialization gives 264 cycles, CPI 1.32 and 505.05 MIPS at 1.50 ns. Split instruction/data memories take 204 cycles and 653.59 MIPS at the same period. A hypothetical dual-port memory also avoids these stalls but lengthens the period to 1.72 ns, yielding 570.00 MIPS. The faster remedy depends on realized timing, workload, area, energy and coherence rather than port count alone.

### Connections

Structural hazards connect pipeline token flow, queues and matching, register files, caches/banks, functional-unit scheduling, arbitration fairness, synthesis/physical design, performance counters and later superscalar issue.

## Governing Question

Pipelining overlaps operations. Overlap creates simultaneous resource demand that did not exist in a single-cycle schedule. The design must decide which demands are compatible and what happens to every operation when capacity is insufficient.

The core question is contractual. A memory labelled “dual port” may support two reads but not two arbitrary writes; a multiplier with four-cycle latency may accept every cycle or only every fourth cycle. Hazards follow exact capability, not block names.

## Why This Matters

An unresolved conflict can corrupt instruction identity or cause two drivers to contend. An overconservative policy remains correct but loses throughput. An added port can improve CPI while reducing frequency or increasing energy and verification cost.

Structural hazards occur beyond textbook ALU sharing. Fetch/data memory, translation walkers, cache banks, register-file ports, operand buses, result buses, writeback ports, queues, miss-status entries and external bandwidth can all constrain overlap.

The conflict distribution is workload- and configuration-dependent. A unit that is ample for scalar code can bottleneck vector, cryptographic or memory-intensive workloads.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace valid tokens through pipeline stages;
- distinguish latency, throughput and CPI;
- interpret memory/register-file port contracts;
- reason about arbitration and backpressure;
- separate data, control and structural hazards.

Retrieve the exact pipeline/configuration; per-stage operation schedule; resource inventory; port count and allowed read/write combinations; unit latency and initiation interval; bank mapping; arbitration policy and priority; request/response tags; queue depths and admission rules; reservation/scoreboard state; multi-resource operations; register-file and bypass topology; instruction/data cache organization; TLB/walker and miss-entry capacity; writeback/commit bandwidth; exception/flush/reset interactions; clock gating; synthesis/STA/area/power reports; resource-conflict counters/traces; workloads; formal assertions; test coverage; hardware/errata; and exact RTL, memory macro, tool, library and revision identities.

## Learning Objectives

After completing this module, you should be able to:

1. define structural hazards as demand-capacity incompatibilities;
2. derive a cycle/resource reservation table from a pipeline schedule;
3. distinguish latency, throughput, port capability, banking and initiation interval;
4. design correct arbitration, grants and backpressure;
5. handle atomic multi-resource allocation and response matching;
6. compare serialization, rescheduling, pipelining, banking, replication and multiporting;
7. identify secondary bottlenecks after a resource remedy;
8. compute conflict-adjusted CPI and throughput;
9. verify safety, fairness, flush/reset and ISA refinement properties;
10. bind resource claims to implemented physical and workload evidence.

## Core Exposition

### Inventory capabilities, not boxes

Name each resource and its service contract. For a memory, state read/write combinations, latency, acceptance rate, byte enables and collision semantics. For a functional unit, state supported operations, latency, initiation interval and response path.

Include buses, muxes, queue entries and result ports. Two execution units sharing one writeback port do not provide two completions in every cycle.

### Build a reservation table

For each instruction class and relative cycle, mark resources required. Overlay instructions at possible initiation offsets. Any cell where incompatible demand exceeds capacity identifies a candidate structural hazard.

Variable latency requires stateful reservations or conservative bounds. A static table alone cannot describe cache misses or iterative division.

### Separate three hazard classes

A data hazard concerns value ordering between producer and consumer. A control hazard concerns uncertainty/redirection of the instruction stream. A structural hazard concerns insufficient compatible capacity.

One stall may have several causes. Keep counters and policies mutually interpretable so optimization targets the true limitation.

### Specify port semantics

Port count is not enough. A `2R1W` register file may serve two reads and one write each cycle, but same-address read-during-write behavior depends on its contract. FPGA memories and ASIC macros offer different modes.

Define arbitration for impossible combinations and whether bypass supplies a newly written value. Validate mapped memory inference; simulation semantics can differ from the selected macro.

### Understand latency and initiation interval

A pipelined multiplier can have latency four and `II=1`, holding four operations while accepting one each cycle. An iterative multiplier with the same latency and `II=4` conflicts on consecutive multiplies.

Track occupancy until the resource releases its reservation. Cancellation may free it immediately, at a boundary, or only after completion.

### Detect before destructive advance

Determine required resources while the token can still be held safely. A token should not leave its source stage unless downstream storage and all non-replayable resources it needs now are granted.

Late detection needs rollback/replay with preserved identity and idempotence. Simpler in-order designs usually prevent advance instead.

### Arbitrate explicitly

An arbiter computes eligibility, priority and grant. Fixed priority is small but can starve. Round-robin improves long-run fairness but needs state. Age priority preserves older-first progress and requires reliable identity.

Grant must remain consistent with any stalled payload. If selection can change before acceptance, muxed request signals must still obey stability requirements.

### Preserve losing requests

Every ungranted operation remains in a stage, queue or reservation entry. Backpressure must prevent upstream overwrite. Buffer capacity determines whether unrelated stages can continue.

Token conservation assertions catch both loss and duplication. Merely checking that one grant is asserted does not prove losers survive.

### Allocate multiple resources atomically

An operation may need a functional unit, source ports, result tag and queue slot together. Granting the unit without reserving the response slot can deadlock or drop completion.

Either allocate the set atomically or use a documented staged reservation protocol with rollback and deadlock ordering. Avoid circular hold-and-wait among arbiters.

### Match responses

If at most one ordered operation can be outstanding, position may identify it. Concurrent or variable-latency units need tags that survive stalls, flushes and wraparound.

Response arbitration is another structural resource. Several units completing together need enough writeback capacity, buffering or a guarantee that their completion times cannot collide.

### Handle unified memory conflicts

In a basic pipeline, instruction fetch and data access may demand one memory port simultaneously. The controller can stall fetch, use separate instruction/data memories, add ports, add caches, bank storage or schedule accesses on different phases if timing permits.

Separate caches can still converge on shared lower-level bandwidth or miss structures. Removing the visible first-level conflict may expose the next bottleneck.

### Handle register-file conflicts

Issue width and instruction format determine source-read demand; completion width determines write demand. Replicated read copies ease read ports but every write must update all copies coherently.

Banking by register number can conflict when operands map to one bank. Operand steering or replication adds muxing, routing and corner cases.

### Handle functional-unit conflicts

Sharing one ALU for arithmetic, branch targets and addresses may be adequate if stage schedules never overlap. Wider issue or changed staging can invalidate that assumption.

Dedicated address/branch units remove conflicts and may shorten paths, but increase area and input/result routing. Measure total implementation.

### Handle cache and translation resources

Cache banks, tag/data arrays, MSHRs, fill buffers, store buffers, TLB ports and page walkers each have separate capacity. A “cache hit” may still stall on a bank or response port.

Backpressure must extend to admission before finite tracking state is exhausted. Overcommitting miss entries loses the ability to match or recover requests.

### Handle writeback and commit bandwidth

Even if several units execute concurrently, results converge on buses, register ports and commit slots. A response buffer can absorb brief collisions; sustained arrival above service rate causes backpressure.

Precise exceptions and program-order commit may intentionally serialize terminal effects. Distinguish a correctness ordering rule from accidental structural scarcity.

### Integrate flush and exceptions

Killed requesters lose eligibility before grant. Already accepted non-cancellable work may continue physically, but its result is marked killed and cannot write or commit.

An older fault can override arbitration for younger effects. Releasing reservations on flush must not allow a late response to attach to a reused tag.

### Reset arbitration and occupancy

Reset clears or invalidates requests, arbiter state, reservations, queue validity and tags. External accepted operations follow cancellation/drain rules.

Round-robin pointers need deterministic or at least safe initialization. Fairness after reset must not depend on arbitrary unknown state.

### Serialize as the baseline remedy

Stalling one requester is often the smallest correct solution. It is attractive when conflicts are rare or resource duplication is expensive.

Quantify frequency and burst length. Average CPI can hide starvation and high-percentile latency for a disadvantaged request class.

### Reschedule work

Moving branch-target computation or address generation to another stage can avoid simultaneous ALU demand. This changes timing, forwarding, redirect and exception paths.

Scheduling uses temporal capacity rather than new hardware. Re-run the entire reservation table after any pipeline change.

### Pipeline the resource

Internal pipeline registers can reduce initiation interval without duplicating all logic. They increase latency and require tags, kill propagation and response capacity.

Not every operation pipelines cleanly; iterative recurrence and memory macro contracts may limit acceptance rate.

### Bank the resource

Banking increases parallelism for requests mapped to different banks. Same-bank conflicts remain, and skewed access patterns can concentrate demand.

Choose/measure mapping using representative addresses. Hashing can spread traffic but adds logic and complicates locality/debug.

### Replicate or multiport

Replication works well for read-mostly state. Coherent writes, area and clock/routing grow. True multiport storage can become expensive and slow as port count increases.

Compare inferred versus physical implementation. A tool may implement a small multiported array as registers and muxes rather than a memory macro.

### Measure performance correctly

Ideal pipeline cycles plus structural stall cycles provides a first model when stalls do not overlap. Real attribution needs a priority rule so simultaneous causes are not double-counted.

Compute `time = cycles*T_clk`; a remedy can lower stalls and lengthen the clock. Measure throughput, latency distribution, energy per instruction and constrained workload service.

### Verify safety and liveness

Assert grant one-hotness per slot, grant implies request, compatibility, atomic allocation, stable losers, request uniqueness, tag matching, killed-result suppression and capacity bounds.

Liveness requires assumptions that resources eventually complete and higher-priority traffic respects a declared model. Prove or measure starvation bounds for the arbitration policy.

### Gather layered evidence

Use resource-table review, lint, protocol assertions, formal arbitration/capacity/deadlock checks, directed collisions, randomized bursts/stalls/completions, flush/reset fault injection, ISA differential tests, synthesis/STA/area/power, counter validation and workload traces.

Bind results to exact configuration, memories, arbitration parameters, RTL, constraints, tools/libraries, workloads/seeds, hardware and errata. Capacity inferred from a block diagram is not verified implementation evidence.

## Definitions and Notation

- `r`: a resource capability under analysis.
- `D_r(t)`: live compatible/incompatible demands for `r` in cycle `t`.
- `K_r(t)`: legal service slots/capacity for `r` in cycle `t`.
- `A_r(t)`: allocation/grant mapping for the cycle.
- `II`: initiation interval of a resource.
- `L`: acceptance-to-result latency.
- `q`: finite queue/reservation capacity.
- `p_i`: workload fraction of instruction/event class `i`.
- `s_i`: structural stalls attributed to class `i`.
- `T_clk`: implemented clock period after a remedy.
- **eligible**: a live request permitted by age, fault, flush and protocol policy.
- **compatible**: a request whose operation/type/address can use a particular slot concurrently.
- **reservation**: state promising current/future resource capacity to an operation.
- **starvation**: an eligible continuing request is denied indefinitely.
- **deadlock**: a set of operations cannot progress because each awaits resources held by others.

## Mechanisms, Invariants, or Proof Structure

1. **Inventory obligation:** every simultaneously constrained port, path, unit, entry and bandwidth limit is represented.
2. **Demand obligation:** each live instruction class requests exactly the capabilities required by its current step.
3. **Capacity obligation:** no slot exceeds its operation, port or initiation contract.
4. **Eligibility obligation:** killed, faulting or invalid requests cannot receive ordinary grants.
5. **Grant obligation:** each grant maps one live request to one compatible real slot.
6. **Atomicity obligation:** multi-resource operations advance only with complete safe allocation/reservation.
7. **Preservation obligation:** ungranted requesters remain coherent and cannot be overwritten.
8. **Request obligation:** arbitration/replay cannot duplicate an accepted external or architectural effect.
9. **Response obligation:** each completion matches one live non-killed operation and is consumed once.
10. **Ordering obligation:** grants/results respect architectural age and precise exception constraints.
11. **Release obligation:** completion, flush, error and reset release reservations exactly once without tag aliasing.
12. **Progress obligation:** under stated demand/completion assumptions, eligible requests eventually advance or meet a declared bound.
13. **Deadlock obligation:** staged reservations obey an acyclic order or have proven recovery.
14. **Timing obligation:** arbitration, muxing, ports and remedy paths meet implemented setup/hold/interface constraints.
15. **Evidence obligation:** conflict rate and remedy benefit bind to exact workloads, hardware/configuration and raw evidence.

## Alternatives and Trade-Offs

1. **Stall versus add capacity:** stalling is small for rare conflict; capacity helps frequent demand at physical cost.
2. **Fixed versus round-robin priority:** fixed is simple; round-robin improves fairness with state.
3. **Age versus class priority:** age supports ordering; class/QoS priority serves critical traffic and risks starvation.
4. **Central versus distributed arbitration:** central policy is explicit; distributed control can scale and risks circular waits.
5. **Atomic versus staged reservation:** atomic allocation avoids partial holds; staging can shorten paths and needs rollback/order.
6. **Unified versus split memory:** unified storage shares capacity; split paths remove common conflict and add coherence/area concerns.
7. **Single versus multiport:** one port is compact; ports increase concurrency and routing/macro cost.
8. **Banking versus replication:** banking shares capacity with conflicts; replication eliminates some read conflicts and multiplies writes.
9. **Shared versus dedicated unit:** sharing saves area; dedication reduces conflicts and may simplify timing.
10. **Iterative versus pipelined unit:** iterative design is compact; pipelining lowers II and adds state/power.
11. **Backpressure versus buffering:** backpressure limits admission; buffers absorb bursts but do not fix sustained overload.
12. **Static schedule versus dynamic arbitration:** static timing is predictable; dynamic selection adapts to variability.
13. **Ordered versus tagged responses:** ordering is compact; tags allow concurrency and require lifetime/wrap proof.
14. **Replicated register reads versus true multiporting:** copies use common memories; true ports avoid duplicate state and cost more.
15. **CPI reduction versus clock margin:** extra capacity can reduce stalls while lengthening critical paths and energy.

## Failure Modes and Misconceptions

1. “Every stall is structural.” Dependencies and redirects cause different stalls.
2. “One drawn block means one use.” Its exact port contract determines capacity.
3. “Two ports allow any two accesses.” Read/write combinations and collisions may be restricted.
4. “Latency equals initiation interval.” A long pipeline can still accept each cycle.
5. “A free ALU means the operation can issue.” Response and queue resources may be unavailable.
6. “Granting one resource is progress.” Partial allocation can deadlock.
7. “One-hot grants prove correctness.” The grantee may be invalid or incompatible.
8. “Losing arbitration means insert a bubble.” The losing token normally must be held.
9. “Selection may change while waiting.” Stable interface payload may forbid it.
10. “Retrying an accepted store is safe.” It can duplicate the effect.
11. “Responses return in order.” Variable units may require tags.
12. “A flushed unit stops immediately.” Non-cancellable physical work can return late.
13. “Freeing a tag on flush is enough.” Reuse can alias a late response.
14. “Fixed priority is fair when traffic is light.” Persistent high-priority traffic can starve.
15. “Round-robin proves bounded latency.” Request and service assumptions still matter.
16. “A buffer solves bandwidth.” It absorbs bursts but not sustained overload.
17. “Banking removes conflicts.” Same-bank traffic remains.
18. “More banks guarantee balance.” Address distributions may be skewed.
19. “Replication makes writes free.” All copies must update coherently.
20. “Adding execution units doubles throughput.” Issue, operands, writeback or memory can bottleneck.
21. “Split caches remove all memory hazards.” They share lower levels and miss resources.
22. “A cache hit cannot structurally stall.” Banks and response paths may be occupied.
23. “Fewer stalls means faster execution.” Clock period may worsen.
24. “Average stall count captures QoS.” Starvation and tail latency need separate evidence.
25. “Simulation covers arbitration.” Formal corner cases expose simultaneous and persistent demand.
26. “The resource table is permanent.” Configuration and pipeline changes invalidate it.

## Worked Examples

### Example 1

Fetch and a load both request a unified single-port memory. Age/policy grants the load while fetch holds; no instruction token is lost.

### Example 2

A `2R1W` register file supports one two-source instruction plus one writeback. Two-wide issue needs four reads, so issue serializes or adds capability.

### Example 3

A four-cycle pipelined multiplier has `II=1`; four multiplies occupy it concurrently without an input conflict, but their result stream needs writeback capacity.

### Example 4

Two cache requests map to the same bank. One is granted and the other remains in its queue; requests to different banks can proceed together.

### Example 5

Two units finish simultaneously at one result bus. A completion buffer absorbs one; without buffering or backpressure, a result would be lost.

### Example 6

A store needs a store-buffer entry and memory-order tag. Atomic allocation prevents it from holding one while waiting forever for the other.

### Example 7

A flushed divide continues internally. Its killed tag consumes the completion without writeback, and tag reuse waits until late-response ambiguity ends.

### Example 8

Round-robin memory arbitration is tested with both requesters continuously valid. Each receives alternating grants under an always-ready memory assumption.

### Example 9

Adding a second ALU removes issue conflicts but makes the operand-select mux and writeback arbiter critical. STA, not unit count, determines frequency.

### Example 10

This deterministic model compares three synthetic remedies for an instruction/data-memory conflict.

<!-- bijux-verify: {"id":"structural-hazard-performance-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unified_cycles=264 effective_cpi=1.32 time_ns=396.00 throughput_mips=505.05\nsplit_cycles=204 effective_cpi=1.02 time_ns=306.00 throughput_mips=653.59\ndual_port_cycles=204 effective_cpi=1.02 time_ns=350.88 throughput_mips=570.00\n"}} -->
```python
instructions = 200
pipeline_depth = 5
data_access_fraction = 0.30
base_cycles = instructions + pipeline_depth - 1
conflict_stalls = round(instructions * data_access_fraction)

def report(name, cycles, period_ns):
    time_ns = cycles * period_ns
    print(
        f"{name}_cycles={cycles} effective_cpi={cycles / instructions:.2f} "
        f"time_ns={time_ns:.2f} throughput_mips={1000 * instructions / time_ns:.2f}"
    )

report("unified", base_cycles + conflict_stalls, 1.50)
report("split", base_cycles, 1.50)
report("dual_port", base_cycles, 1.72)
```

The inputs assume nonoverlapping stalls and invented periods. Real comparisons require conflict traces, mapped memories, lower-level contention, power and workload constraints.

## Cross-Program Connections

- **Digital Logic:** ports, muxes, arbiters and memory macros determine compatible capacity.
- **Data Structures:** queues, tags, scoreboards and free lists preserve denied or outstanding tokens.
- **Concurrent Systems:** arbitration, backpressure, fairness and deadlock mirror shared-resource protocols.
- **Operating Systems:** QoS and contention counters expose shared hardware behavior to scheduling policy.
- **Security Engineering:** starvation, timing contention and stale-tag aliasing can become attack surfaces.
- **Formal Methods:** injective allocation, conservation, fairness and deadlock freedom are precise properties.
- **Performance Engineering:** conflict distributions, CPI, frequency, tails and energy determine remedy value.
- **Systems Engineering:** macro choice, configuration, evidence and workload ownership cross organizational boundaries.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), architectural resource demands and outcomes refined by implementations; retrieved 2026-09-04.
2. lowRISC, [Ibex Pipeline Details](https://ibex-core.readthedocs.io/en/latest/03_reference/pipeline_details.html), current stalls, multicycle units and pipeline behavior; retrieved 2026-09-04.
3. lowRISC, [Ibex Instruction Decode and Execute](https://ibex-core.readthedocs.io/en/latest/03_reference/instruction_decode_execute.html), current controller and execution-resource behavior; retrieved 2026-09-04.
4. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), current integration, configuration, interfaces and verification; retrieved 2026-09-04.
5. YosysHQ, [PicoRV32](https://github.com/YosysHQ/picorv32), current compact core with configurable resource/performance trade-offs; retrieved 2026-09-04.
6. Berkeley Architecture Research, [BOOM Pipeline Overview](https://docs.boom-core.org/en/latest/sections/intro-overview/boom.html), current open wider-pipeline organization illustrating expanded resource demand; retrieved 2026-09-04.
7. YosysHQ, [Yosys Documentation](https://yosyshq.readthedocs.io/projects/yosys/en/latest/), synthesis evidence for mapped memories, arbiters, muxes and timing; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), independent ISA semantics for commit-trace comparison; retrieved 2026-09-04.

## Exercises

### Exercise 1

Build a reservation table for a five-stage scalar pipeline with unified single-port memory, one ALU and a nonpipelined four-cycle multiplier.

### Exercise 2

Design an arbiter/backpressure protocol for two requesters sharing a variable-latency unit. State safety and fairness properties.

### Exercise 3

Design atomic allocation for an operation requiring a functional unit, response-buffer slot and tag. Explain deadlock and flush behavior.

### Exercise 4

Recompute the executable comparison and identify evidence needed to choose unified, split or dual-port storage.

### Exercise 5

Write a verification and measurement plan for removing a writeback structural hazard in a configurable two-issue processor.

## Answers to the Exercises

### Answer 1

Mark instruction memory in each fetch relative cycle and data memory in the memory stage of loads/stores; overlap identifies the unified-port conflict. Mark the ALU for arithmetic/address/branch uses according to stage schedule; if all occupy distinct cycles in a scalar issue schedule, no ALU conflict exists. Mark multiplier occupancy for four cycles and prohibit a new multiply until release because `II=4`.

Include result/writeback capacity and variable memory waits. The table's assumptions name port combinations, acceptance versus latency and flush release. Changed stage or issue width requires regeneration.

### Answer 2

Eligibility requires valid, not killed, resource-compatible request. Grant at most one requester; grant implies request. On acceptance, allocate an outstanding tag and stop granting another request if the unit lacks capacity. The loser holds validity/payload under backpressure. Match one response to the outstanding tag and release once.

Round-robin priority changes only on acceptance, not merely presentation. Under persistent request, always-eventual unit readiness/completion and no reset, prove each requester is granted within a stated number of accepted intervening operations. Safety does not rely on fairness.

### Answer 3

Compute availability for unit, buffer and tag before advance; assert one atomic grant only when all are free. Alternatively reserve in one global order and provide cancellation, but prove no circular wait. Record ownership so no other operation takes a partially reserved component.

On flush, mark any accepted non-cancellable unit work killed, preserve its tag/buffer until response or use an epoch whose nonalias bound is proven, then release exactly once. A killed response cannot write back or commit.

### Answer 4

Unified storage takes 264 cycles at 1.50 ns, or 396.00 ns/505.05 MIPS. Split storage takes 204 cycles at 1.50 ns, or 306.00 ns/653.59 MIPS. The invented dual-port option takes 204 cycles at 1.72 ns, or 350.88 ns/570.00 MIPS.

Choose only after mapping exact memories and measuring instruction/data conflict bursts, lower-level contention, clock margin, area, energy, cache/coherence effects, latency tails and relevant workload constraints. Validate read/write collision semantics and tool inference.

### Answer 5

Inventory all producers, completion distributions, result buses, buffer entries, register ports and commit slots for every configuration. Add capacity or buffering with explicit eligibility, arbitration, tags, backpressure and killed-result rules. Prove no loss/duplication, correct priority/order, bounded capacity, response matching, flush/reset release, progress under assumptions and ISA commit refinement.

Test all simultaneous completion combinations, persistent traffic, randomized latency, full buffers, exceptions, redirects and reset. Run synthesis/STA/place-route/power because added ports/muxes may set frequency. Validate counters, then measure CPI attribution, throughput, tails and energy on declared workloads. Bind evidence to exact configuration and hardware; no independent certification is claimed.
