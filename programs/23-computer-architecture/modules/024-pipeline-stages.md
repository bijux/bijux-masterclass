---
module_id: CA-024
program: Computer Architecture
level: 1
module_number: 24
title: Pipeline Stages
status: complete
last_verified: 2026-09-04
---

# Pipeline Stages

## One-Page Review

### Governing question

How should instruction work be partitioned across clocked stages so multiple instructions overlap without losing identity, violating dependencies, duplicating effects, or mistaking a higher clock frequency for higher useful throughput?

### Essential definitions

- A **pipeline** overlaps different portions of multiple instruction executions.
- A **stage** is a clock-to-clock region with a defined input/output contract, not merely a label on a diagram.
- A **pipeline register** captures data, control, identity and validity between stages.
- A **pipeline token** is the implementation record for one instruction or operation moving through stages.
- A **valid bit** states that a stage entry contains a live token.
- **ready** states that the receiving stage can accept a token under the chosen flow-control convention.
- A **stall** prevents selected tokens from advancing while preserving their state.
- A **bubble** is an invalid stage entry that consumes capacity but has no architectural instruction effect.
- A **flush** invalidates tokens that must not complete, usually after redirection or fault.
- **latency** is time from an instruction boundary to its completion; **throughput** is the completion rate.
- **fill time** is the initial delay before the first token exits an empty pipeline.
- **drain time** is the time for remaining live tokens to leave after admission stops.
- A **balanced pipeline** has similar worst-case stage delays after register overhead and physical effects.
- A **stage-local invariant** describes the token, valid state, inputs, outputs and allowed effects at one boundary.
- **retirement/commit** is the ordered architectural completion boundary; it need not coincide with a stage named writeback.

### Central model, mechanism, or theorem

Let stage `j` hold `(v_j, x_j)`, where `v_j` is validity and `x_j` contains instruction identity, operands, decoded controls, results, exception metadata and prediction context. On a normal transfer, token `x_j` advances exactly once when `v_j && ready_{j+1}`; if it cannot advance, every required field remains stable. Bubbles have `v_j=0` and cannot cause architectural effects. A redirect or fault invalidates precisely the younger token set selected by age/identity. Correctness requires that the surviving terminal token refine the ISA step in program order, while timing requires every register-to-register path plus clock overhead to fit `T_clk`.

### Critical invariants

- Every valid token carries enough identity and metadata for all downstream decisions.
- A token advances, stalls, flushes or completes once per cycle; it is never silently duplicated or lost.
- Stalled stage contents and outward payload remain stable unless the protocol explicitly permits change.
- Invalid entries cannot write registers, issue side effects, redirect fetch or retire.
- Flush selection is age-correct and dominates ordinary younger-token advancement.
- Exceptions remain attached to the faulting token and suppress its prohibited effects.
- Commit occurs in the declared order with exactly the ISA-permitted result.
- Pipeline registers capture coherent data/control bundles on the same transfer event.
- Each implemented stage satisfies setup/hold, clocking and interface timing at all declared corners.
- Performance conclusions include fill/drain, hazards, cache/memory waits, redirects and workload mix.

### Common failures

Frequent failures are assuming every pipeline has five physical stages, moving data without its control bits, dropping instruction identity, treating a stall as inserting a bubble everywhere, allowing upstream overwrite while downstream is blocked, issuing the same request twice, flushing the redirecting instruction, retaining a younger store, losing an exception during replay, writing from an invalid entry, forwarding from a killed producer, splitting a path without registering every dependent signal, ignoring pipeline-register overhead, comparing clock frequency without CPI, and claiming balanced timing from block names instead of STA.

### Compact example

For invented stage logic delays of 0.90, 1.15, 1.30, 1.55 and 0.75 ns plus 0.20 ns register/clock overhead, `T_clk=1.75 ns`. One hundred instructions without stalls need `100+5-1=104` cycles, 182.00 ns, or 549.45 MIPS. Eighteen stall cycles raise effective CPI to 1.22 and take 213.50 ns, or 468.38 MIPS. Splitting the 1.55 ns memory stage into 0.80 and 0.75 ns produces six stages at 1.50 ns; absent new stalls, 105 cycles take 157.50 ns. Real retiming changes hazards, physical paths, power and cache behavior.

### Connections

Pipeline stages connect synchronous timing, datapath/control partitioning, hazards and forwarding, memory protocols, branch prediction, precise exceptions, formal token reasoning, synthesis/physical design, performance counters and later superscalar/out-of-order execution.

## Governing Question

Pipelining seeks throughput by overlapping work. It does not reduce the logical work of an instruction, and extra boundaries can increase individual latency. The central design problem is a correct partition, not drawing fetch/decode/execute/memory/writeback boxes.

Each boundary becomes a contract: which token may enter, what fields cross, what makes the fields valid, when they must remain stable, and how kill/stall/exception events affect them. A missing bit at a boundary often becomes a distant architectural bug.

## Why This Matters

Pipeline depth influences frequency, latency, branch cost, bypass complexity, energy, verification state space and physical placement. Deeper is not automatically faster; shorter logic paths compete with register overhead and higher misspeculation or communication cost.

Commercial and open cores vary widely. Some combine decode and execute, split memory access, add queues, or let long operations leave the primary stage chain. The five-stage model is a useful teaching decomposition, not an implementation law.

Correct flow control matters whenever any stage can wait. Memory, multipliers, exceptions, debug and downstream backpressure turn a neat conveyor diagram into a network of conditional transfers.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace single-cycle and multicycle datapaths;
- distinguish architectural and microarchitectural state;
- compute setup/hold timing and clock period;
- interpret valid/ready or request/response protocols;
- explain ISA commit, faults and control flow.

Retrieve the exact ISA/profile/extensions; instruction classes and variable-latency operations; stage/block diagram and generated configuration; stage-boundary bundles; valid/ready/stall/kill equations and priorities; token/age identifiers; decode timing; register-file read/write timing; ALU/multiplier/divider placement; address generation; cache/TLB/memory interfaces; request replay rules; bypass and scoreboard paths; branch prediction/resolution and redirect scope; exception/interrupt/debug entry; commit order; reset; pipeline-register implementation; clocking/gating; CDC/RDC boundaries; synthesis/STA/physical reports; workload traces and counters; formal assertions/refinement; test coverage; power/thermal results; hardware/errata; and exact RTL/tool/library/revision data.

## Learning Objectives

After completing this module, you should be able to:

1. define stages as clocked token-transfer contracts;
2. derive a pipeline partition from logic, interfaces and timing rather than labels;
3. carry coherent data, controls, identity and exception metadata across boundaries;
4. distinguish advance, hold, bubble insertion, flush and completion;
5. integrate variable-latency stages without token duplication or loss;
6. define age-correct redirects and precise exceptions;
7. compute clock period, fill/drain, CPI, latency and throughput;
8. evaluate deeper, shallower and elastic pipeline trade-offs;
9. verify stage-local safety, global ordering, liveness and ISA refinement;
10. bind performance and correctness claims to implemented evidence.

## Core Exposition

### Begin with the architectural transition

The ISA defines an instruction's permitted state change. Pipelining creates overlapping partial implementations, but must preserve the architectural trace. Define instruction acceptance, commit and trap events before choosing stage names.

For an in-order scalar core, tokens normally commit in program order. If some operation completes off the main path, its result still needs ordering and exception rules.

### Partition by dependencies and timing

List the work and dependencies: fetch address, instruction access, alignment/decompression, decode, register read, immediate creation, execute, address translation, data access, result selection and architectural completion.

Candidate cuts must capture every value needed later. Use synthesis and physical estimates iteratively; source-level operation count is a weak proxy for placed delay.

### Treat the five-stage pipeline as a model

The familiar IF, ID, EX, MEM and WB stages reveal basic overlap and hazards. It assumes particular memory, register-file and operation timing that may not hold in an FPGA, SRAM macro, high-frequency ASIC or variable-length front end.

Name stages by durable responsibility, while documenting actual contained work and boundaries. Two designs using “execute” may have very different contracts.

### Define the token bundle

A token may carry instruction address and bits, sequence/epoch identity, decoded source/destination indices, immediate, operand values, operation controls, prediction metadata, effective address, result, memory attributes, exception cause and debug information.

Carry only necessary fields, but prove reconstruction is exact if a field is omitted. Re-decoding or rereading can see changed state and create new timing paths.

### Make validity explicit

After reset or a bubble, data bits may contain arbitrary old values. Valid gates their interpretation. Every side effect and forwarding eligibility depends on live, un-killed validity.

Validity itself must advance under the same transfer event as the associated bundle. Advancing valid without data or data without valid destroys token coherence.

### Specify advance and hold

For an elastic boundary, a receiver can accept when empty or when its current token will advance. A transfer occurs only when sender valid and receiver ready.

If blocked, the sender holds required payload and validity stable. Upstream backpressure propagates according to registered or combinational ready design; long ready chains can become critical paths.

### Distinguish stalls and bubbles

A stall holds at least one valid token in place. A bubble is an invalid entry. To delay a dependent instruction while an older instruction advances, hold the younger/front state and inject invalidity into the next stage.

Global enables are simple but may freeze a stage that must accept a response. Per-stage enables are flexible and require careful coordination.

### Define kill and flush priority

A redirect typically preserves the resolving instruction and older tokens while invalidating younger wrong-path tokens. Exception handling may kill the faulting token's ordinary effects plus all younger tokens, then create a trap transition.

Priority among reset, integrity error, exception, redirect, response, stall and normal advance must be explicit. A flush that loses to a stall can retain a doomed token.

### Preserve age and identity

Stage position may imply age only in a simple full pipeline. Bubbles, queues, replays and detached units weaken that inference. Sequence numbers, epochs or tags can make matching and kill scope explicit.

Wraparound is safe only if the live window cannot confuse old and new identities. Prove the bound rather than relying on a wide-looking counter.

### Place instruction fetch deliberately

Fetch may include PC selection, prediction, instruction memory/cache, translation, alignment and buffering. Variable-length instructions can cross fetch blocks and need precise address/byte identity.

Redirect must invalidate or epoch-tag outstanding wrong-path responses. A returned line is not automatically a live instruction token.

### Partition decode and register read

Decode establishes legality, sources, destination, immediate and operation class. Register read may be in the same stage or separated depending on file timing and bypass design.

Early hazard checks reduce wasted work but add decode paths. Late checks may require replay or wider metadata. Ensure illegal instructions cannot initiate privileged or memory effects before resolution.

### Place execute operations

Integer ALU and branch comparison commonly occupy execute work. Address generation may share the ALU or use a dedicated adder. Multiplication/division may be pipelined, iterative or detached.

If a unit accepts a token and completes later, specify backpressure, tag, cancellation, exception and result arbitration. “EX” no longer means one-cycle completion.

### Place memory work

Memory work can include address generation, translation, permission/alignment, cache lookup, tag/data selection, refill interaction and response alignment. These often require multiple stages.

Stores create externally visible effects. Define when address/data become irrevocable, how faults suppress the request, and how a flushed/replayed token cannot duplicate it.

### Separate result availability from writeback

An ALU result may be available for forwarding before architectural register write. A load result may arrive late. Track availability, validity and destination identity separately.

Writeback arbitration must handle coincident results from main and detached units. Commit policy decides whether writeback itself is architectural or remains speculative/internal.

### Define commit, not just WB

In a simple core, writeback may coincide with commit. Stores, exceptions, control/status changes and debug transitions show why the general definition must cover all architectural effects.

Commit must exclude invalid, killed and faulting ordinary tokens. Count retired instructions at this boundary, not merely fetched or executed tokens.

### Handle precise exceptions

Attach detected fault cause and required metadata to the token. Older permitted tokens complete; the faulting token does not perform prohibited ordinary effects; younger tokens are killed; trap state records the exact architectural boundary.

Faults discovered in different stages need a priority/age policy. “Later stage wins” may work for strict in-order flow, but prove behavior with detached or replaying operations.

### Handle interrupts and debug

Interrupts are asynchronous requests sampled into a synchronous policy. Choose an instruction boundary, drain/flush behavior, saved PC and priority relative to synchronous faults.

Debug halt, single-step and trigger behavior also interact with tokens in flight. A halt acknowledgement needs a documented quiescent state and treatment of outstanding requests.

### Reset the pipeline coherently

Reset invalidates every stage and disables side effects. External requests already accepted follow their protocol's cancellation, drain or tag-discard rule.

Reset release and clock gating must meet recovery/removal and CDC/RDC requirements. Functional simulation alone does not establish safe deassertion.

### Balance logic after overhead

For stage logic delays `L_j`, a simple bound is `T_clk >= max_j(L_j + t_cq + t_setup + uncertainty_j)`. Local skew, hold fixes, muxing and routing matter.

A new boundary reduces only the divided logic portion. It adds a register, clock load, control/valid/kill propagation and often new muxing. Extremely fine stages approach an overhead floor.

### Calculate latency and throughput

An ideal depth-`k` scalar pipeline processes `N` independent instructions in `N+k-1` cycles from empty, assuming one admission/completion per cycle and no stalls. Steady ideal CPI approaches one as `N` grows.

Actual cycles add structural/data/control stalls, cache/TLB misses, replays, variable operations, interrupts and drain/fill events. Mean instruction time is `CPI*T_clk`; tail latency and energy may dominate throughput.

### Evaluate stage splitting

Split the critical stage only if both resulting paths and boundary signals fit. The extra stage can delay branch resolution, load forwarding or exception discovery and thereby increase penalties.

Retiming may move registers without changing architectural behavior, but boundaries at memories, macros, protocols or clock domains constrain freedom. Re-run all hazards and flush proofs.

### Consider elastic versus rigid flow

A rigid pipeline uses coordinated enables under predictable latency. An elastic pipeline gives boundaries independent valid/ready storage, accommodating variable latency and local backpressure.

Elasticity improves composition but adds state and ready/valid correctness obligations. Combinational ready loops are forbidden; registered backpressure adds buffering/latency decisions.

### Control power and clocking

Pipeline registers toggle and load the clock tree even for bubbles unless gated. Fine staging can increase clock and mux energy. Operand isolation and clock gating must preserve valid/flush/reset behavior.

Power control cannot prevent a stage from accepting a required response or clearing a killed token. Verify gate enables and wake latency under all flow events.

### Verify locally and globally

Local assertions cover stable holds, coherent transfers, invalid-side-effect suppression and legal controls. Interface assertions cover request stability, single acceptance and response matching.

Global checks cover uniqueness, ordering, flush age, precise faults, progress and commit refinement. Token scoreboards and symbolic identities expose loss/duplication that ordinary directed tests miss.

### Gather implementation evidence

Run lint, CDC/RDC, protocol checks, instruction/exception tests, differential ISA simulation, random stalls, reset/fault injection, formal safety/liveness/refinement, synthesis, STA, place/route, power analysis and workload measurements. Review counters and traces against known events.

Bind evidence to RTL/configuration, memories, predictor/cache parameters, constraints, tools/libraries, workload, seeds, hardware revision and errata. Stage claims from one configuration do not automatically transfer to another.

## Definitions and Notation

- `j`: stage index; depth is `k`.
- `v_j`: validity of stage `j`.
- `x_j`: coherent token bundle held in stage `j`.
- `ready_j`: stage `j` can accept a token under the flow-control contract.
- `advance_j`: transfer event moving a valid token across boundary `j`.
- `kill_j`: event invalidating a token without architectural completion.
- `L_j`: implemented combinational delay assigned to stage `j`.
- `T_clk`: clock period including boundary and uncertainty terms.
- `N`: number of admitted instructions in a measured finite run.
- `k`: pipeline depth for the modeled path.
- **epoch/tag**: identity used to reject stale or wrong-path responses.
- **backpressure**: inability of a receiver propagating toward senders.
- **redirect**: control-flow event choosing a different fetch stream.
- **drain**: stop admission while allowing live tokens to complete or be killed.
- **stuttering refinement**: internal cycles may leave architectural state unchanged before one permitted terminal transition.

## Mechanisms, Invariants, or Proof Structure

1. **Bundle obligation:** each boundary carries coherent data, controls, identity, validity and fault metadata.
2. **Transfer obligation:** a live token advances exactly once only on its defined transfer event.
3. **Hold obligation:** blocked live tokens and required outward payload remain stable.
4. **Bubble obligation:** invalid entries cannot forward, request, write, redirect or commit.
5. **Uniqueness obligation:** accepted tokens are neither duplicated nor silently lost.
6. **Ordering obligation:** surviving architectural effects occur in the declared program order.
7. **Dependency obligation:** every consumer receives the architecturally correct producer value.
8. **Request obligation:** memory/unit requests are accepted at most once per logical operation and matched to responses.
9. **Flush obligation:** redirects and faults kill exactly the intended younger/ordinary effects with correct priority.
10. **Exception obligation:** the oldest selected fault produces precise trap state and suppresses prohibited effects.
11. **Commit obligation:** every terminal normal token equals one ISA step and no nonterminal token commits.
12. **Reset obligation:** all validity/effect state reaches safe reset and late responses cannot revive stale tokens.
13. **Progress obligation:** under declared fairness, every accepted non-killed token commits or traps.
14. **Timing obligation:** every data/control/ready/kill/clock path meets declared setup, hold and interface constraints.
15. **Evidence obligation:** structure, hazards, timing and performance claims bind to exact implementation/configuration artifacts.

## Alternatives and Trade-Offs

1. **Shallow versus deep:** shallow pipelines reduce boundaries/penalties; deeper pipelines can shorten logic stages.
2. **Fixed five-stage versus tailored:** standard decomposition teaches clearly; tailored stages match actual memories and timing.
3. **Rigid versus elastic:** global flow is compact; local valid/ready handles variability with more control state.
4. **Combined versus split fetch:** fewer stages reduce redirect depth; split front ends accommodate access/alignment timing.
5. **Combined versus split decode/read:** combination reduces latency; separation eases file/decode timing.
6. **Shared versus dedicated address adder:** sharing saves area; dedication removes contention and paths.
7. **Inline versus detached long unit:** inline backpressures simply; detached execution needs tags/arbitration and permits overlap.
8. **Early versus late branch resolution:** early resolution reduces penalty; later resolution may simplify timing/operand availability.
9. **Early versus late fault detection:** early detection avoids work; later detection may use definitive data and increases kill scope.
10. **Global stall versus per-stage backpressure:** global hold is easy to reason about; local flow improves utilization.
11. **Combinational versus registered ready:** combinational ready reduces buffering latency; registered ready breaks long paths and needs capacity.
12. **Writeback-as-commit versus separate commit:** coincidence is compact; separation handles stores/faults/complex completion explicitly.
13. **Forward versus stall:** bypassing improves CPI; interconnect/comparison paths cost area, power and timing.
14. **Clock gating versus free-running registers:** gating saves dynamic power; enable/reset/flush correctness becomes critical.
15. **Frequency versus useful work:** shorter periods help only when added CPI, penalties, power and workload limits do not dominate.

## Failure Modes and Misconceptions

1. “Every CPU has five stages.” Actual organizations depend on goals and technology.
2. “A stage is one logical function.” Functions may span stages or share one stage.
3. “Pipelining makes one instruction faster.” It often improves throughput while increasing latency.
4. “More stages always raise performance.” Register overhead and penalties can dominate.
5. “Equal block names mean balanced timing.” Only implemented path analysis supports balance.
6. “The slowest RTL operator sets frequency.” Routing, control and physical macros also matter.
7. “Data alone crosses a boundary.” Controls, identity, validity and faults must remain coherent.
8. “Old bits are zero after a bubble.” Invalid data is irrelevant only if every effect is gated.
9. “Stall and bubble are synonyms.” A stall holds a token; a bubble is invalid capacity.
10. “Holding valid is enough.” Payload stability is also required.
11. “Backpressure can stop anywhere.” Accepted responses and protocol obligations may still require progress.
12. “A flush clears every stage.” Older/resolving tokens often must survive.
13. “Stall should beat flush.” That can retain wrong-path state.
14. “Stage position always proves age.” Queues, replay and detached units complicate age.
15. “A killed producer can still forward.” That leaks wrong-path or faulting data into live computation.
16. “Writeback always equals commit.” Stores and exceptions show otherwise.
17. “A memory request is harmless before legality.” It can create visible or security effects.
18. “Reset cancels the bus.” Only the interface contract determines cancellation.
19. “Splitting memory guarantees a shorter clock.” New boundary and macro timing may not permit it.
20. “Registered ready cannot lose data.” Capacity/ready equations must still be correct.
21. “Ideal CPI is one.” Fill, drain, hazards and waits make finite/real CPI larger.
22. “Frequency alone ranks pipelines.” Use workload instruction time, latency, power and constraints.
23. “Retirement count can be inferred from fetch.” Wrong-path and faulting tokens inflate fetch.
24. “Directed instruction tests prove flow control.” Random stalls and symbolic tokens expose different bugs.
25. “No assertion failure proves liveness.” Infinite waiting can satisfy safety.
26. “One configuration validates the design.” Stage structure and paths change with options and memories.

## Worked Examples

### Example 1

A five-stage teaching core carries PC, instruction, source identities, decoded controls and valid from decode to execute. A bubble has valid false, so stale destination bits cannot trigger forwarding.

### Example 2

A downstream memory stage waits. Its token and request payload remain stable, execute cannot overwrite it, and backpressure prevents decode/fetch from advancing unless separate buffers have capacity.

### Example 3

A taken branch in execute preserves the branch and older token, invalidates younger decode/fetch tokens, changes the fetch epoch and rejects a late wrong-path response.

### Example 4

A load fault travels with its instruction identity. Older work completes; its ordinary writeback is disabled; younger work is killed; trap PC and cause commit once.

### Example 5

A multiplier accepts a detached token. Its tag and destination travel with the operation, a flush marks it killed, and completion arbitration refuses killed results.

### Example 6

Splitting decode and register read shortens a path but adds a stage to branch resolution. Workload measurement decides whether higher frequency exceeds added redirect cost.

### Example 7

An invalid pipeline entry contains all-one write controls after reset. Because validity gates every effect and forwarding source, it remains semantically a bubble.

### Example 8

A registered-ready boundary includes a one-entry skid buffer. The capacity invariant proves one token can arrive after backpressure is registered without overwrite.

### Example 9

A token scoreboard assigns symbolic IDs at acceptance and removes them only at commit/trap/kill. Assertions detect any duplicate ID, reordering or disappearance.

### Example 10

The following deterministic model computes synthetic finite-run pipeline performance and a stage-splitting comparison.

<!-- bijux-verify: {"id":"pipeline-stage-performance-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"base_period_ns=1.75 ideal_fmax_mhz=571.43\nbase_no_stall_cycles=104 time_ns=182.00 throughput_mips=549.45\nbase_with_stalls_cycles=122 effective_cpi=1.22 time_ns=213.50 throughput_mips=468.38\nsplit_period_ns=1.50 depth=6 cycles=105 time_ns=157.50 throughput_mips=634.92\n"}} -->
```python
instructions = 100
register_overhead_ns = 0.20
logic_ns = {"fetch": 0.90, "decode": 1.15, "execute": 1.30, "memory": 1.55, "writeback": 0.75}
depth = len(logic_ns)
period = max(logic_ns.values()) + register_overhead_ns
base_cycles = instructions + depth - 1
base_time = base_cycles * period
stall_cycles = 18
stalled_cycles = base_cycles + stall_cycles
stalled_time = stalled_cycles * period

split_logic_ns = {"fetch": 0.90, "decode": 1.15, "execute": 1.30, "memory_a": 0.80, "memory_b": 0.75, "writeback": 0.75}
split_depth = len(split_logic_ns)
split_period = max(split_logic_ns.values()) + register_overhead_ns
split_cycles = instructions + split_depth - 1
split_time = split_cycles * split_period

print(f"base_period_ns={period:.2f} ideal_fmax_mhz={1000 / period:.2f}")
print(f"base_no_stall_cycles={base_cycles} time_ns={base_time:.2f} throughput_mips={1000 * instructions / base_time:.2f}")
print(f"base_with_stalls_cycles={stalled_cycles} effective_cpi={stalled_cycles / instructions:.2f} time_ns={stalled_time:.2f} throughput_mips={1000 * instructions / stalled_time:.2f}")
print(f"split_period_ns={split_period:.2f} depth={split_depth} cycles={split_cycles} time_ns={split_time:.2f} throughput_mips={1000 * instructions / split_time:.2f}")
```

These invented delays omit new hazards, cache behavior, physical changes and power. They establish calculation only.

## Cross-Program Connections

- **Digital Logic:** pipeline boundaries are synchronous timing and reset structures.
- **Data Structures:** FIFOs, skid buffers, tags and scoreboards manage tokens and capacity.
- **Concurrent Systems:** stages communicate through flow-control protocols with backpressure.
- **Operating Systems:** precise traps, interrupts, debug and counters depend on pipeline boundaries.
- **Security Engineering:** wrong-path requests and stale responses can expose or corrupt state.
- **Formal Methods:** symbolic-token uniqueness, ordering, liveness and refinement express correctness.
- **Performance Engineering:** finite-run cycles, CPI, frequency, latency, throughput and power must be measured together.
- **Systems Engineering:** configuration, evidence, errata and lifecycle claims span design through hardware operation.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), architectural instruction effects refined by pipeline execution; retrieved 2026-09-04.
2. lowRISC, [Ibex Pipeline Details](https://ibex-core.readthedocs.io/en/latest/03_reference/pipeline_details.html), current pipeline organization and multicycle behavior; retrieved 2026-09-04.
3. lowRISC, [Ibex Instruction Decode and Execute](https://ibex-core.readthedocs.io/en/latest/03_reference/instruction_decode_execute.html), current decode/execute stages and controller behavior; retrieved 2026-09-04.
4. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), integrated core configuration, interfaces, security and verification; retrieved 2026-09-04.
5. YosysHQ, [PicoRV32](https://github.com/YosysHQ/picorv32), compact multi-cycle core illustrating that implementation need not follow five stages; retrieved 2026-09-04.
6. Berkeley Architecture Research, [BOOM Pipeline Overview](https://docs.boom-core.org/en/latest/sections/intro-overview/boom.html), current open out-of-order pipeline overview; retrieved 2026-09-04.
7. YosysHQ, [Yosys Documentation](https://yosyshq.readthedocs.io/projects/yosys/en/latest/), synthesis evidence for implemented registers, logic and timing inputs; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), independent executable ISA semantics for commit-boundary comparison; retrieved 2026-09-04.

## Exercises

### Exercise 1

Define the complete token bundle and stage contracts for a five-stage in-order RV32I subset supporting ALU, load, store and conditional branch instructions.

### Exercise 2

Design valid/ready equations for a variable-latency memory stage. Explain advance, hold, bubble insertion and response acceptance without token loss or duplication.

### Exercise 3

Specify redirect and exception behavior when a branch resolves while an older load reports an error. Identify surviving and killed tokens and the next architectural event.

### Exercise 4

Recompute the executable example, then evaluate whether splitting the memory stage is justified if it adds six redirect-stall cycles and twelve load-use stalls per 100 instructions.

### Exercise 5

Write a verification plan covering stage-local contracts, end-to-end token behavior, timing and workload evidence for a configurable pipeline.

## Answers to the Exercises

### Answer 1

Fetch/decode carries valid, PC, instruction and epoch. Decode/execute adds legal class, source/destination identities, immediate, operand values, ALU/branch/memory/write controls, prediction and possible decode fault. Execute/memory carries result/effective address, store data/mask, destination/write control, resolved next PC, redirect and exception metadata. Memory/writeback carries matched load/result data, destination, final exception and commit controls.

Each boundary defines transfer and hold, and validity gates every effect. Branch/store/load metadata remains attached to instruction identity. Exact bundles depend on register-file and memory timing; prove any recomputation equivalent.

### Answer 2

Let memory stage ready be empty or able to complete/transfer its current token, with capacity for any registered backpressure delay. Accept upstream only on valid-and-ready. Before request acceptance, hold valid/address/data/mask stable. After acceptance, record outstanding and suppress new request creation; wait for the matched response.

On success/error, transfer one resulting token if downstream can accept or buffer it locally. A stall holds all fields. Bubble insertion sets downstream valid false only when no token transfers. Assertions cover stable hold, capacity, one acceptance, one response consumption and token conservation.

### Answer 3

The older load error has architectural priority over the younger branch redirect. Preserve still-older permitted tokens, mark the load as the precise faulting token, suppress its ordinary destination, and kill the branch plus every younger token. The branch redirect must not select the next fetch stream.

After older completion policy is satisfied, commit the trap state with the load PC/cause. Invalidate or epoch-reject wrong/outstanding younger fetch responses. Assertions use age identity rather than stage labels alone.

### Answer 4

The base uses 122 cycles with its original 18 stalls: 213.50 ns. The split pipeline has 105 ideal finite-run cycles plus 18 existing, 6 redirect and 12 new load-use stalls, or 141 cycles. At 1.50 ns, it takes 211.50 ns and yields about 472.81 MIPS for 100 instructions.

That slight synthetic gain is not enough for a product conclusion. Compare tail latency, energy, area, physical timing margin, cache effects, hazard distribution and verification cost under representative workloads; require a predeclared acceptance margin.

### Answer 5

Locally assert coherent valid/data/control transfer, stable hold, invalid-side-effect suppression, legal controls and request/response rules at each boundary. Globally track symbolic token IDs for uniqueness, ordering, dependency values, age-correct flush, precise exceptions, reset containment and progress under fairness. Compare commit/trap traces against an independent ISA model.

Vary pipeline options, memories, long units, random stalls, redirects, simultaneous faults, reset, debug and clock gating. Run CDC/RDC, synthesis, STA/place-route and power for exact configurations. Measure fill/drain, CPI causes, latency, throughput and counters across declared workloads. Bind sources, configs, constraints, tools, seeds, raw results, hardware and errata. Internal evidence is not independent certification.
