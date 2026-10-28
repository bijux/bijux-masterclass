---
module_id: CA-026
program: Computer Architecture
level: 1
module_number: 26
title: Data Hazards and Forwarding
status: complete
last_verified: 2026-09-04
---

# Data Hazards and Forwarding

## One-Page Review

### Governing question

When overlapping instructions communicate through architectural names, how can a pipeline give every consumer the newest architecturally permitted value at the exact stage it needs it—forwarding when ready, stalling when not, and never using a killed or faulting producer?

### Essential definitions

- A **data dependence** is a semantic relationship in which one instruction's value or name ordering constrains another.
- A **data hazard** is an implementation timing condition that could violate a dependence if the pipeline advanced normally.
- **read after write** (`RAW`) is a true dependence: a consumer reads a value produced by an older instruction.
- **write after read** (`WAR`) is an anti-dependence: a younger write must not precede an older read of the same architectural name.
- **write after write** (`WAW`) is an output dependence: writes to one name must retain architectural order.
- **forwarding/bypassing** routes an available producer result directly to a consumer before ordinary architectural readback.
- A **producer** is an older live operation that will write the requested architectural destination.
- A **consumer** is a live operation requiring a source value at a specified use stage.
- **availability** means the definitive value exists early enough on a legal path to the consumer's capture deadline.
- A **load-use hazard** occurs when a load's data is not available soon enough for a following consumer despite ordinary ALU forwarding.
- An **interlock** automatically holds/inserts bubbles until a required value is available.
- A **scoreboard** tracks pending producers and resource/value readiness.
- **producer priority** selects the youngest older matching producer because it represents the latest program-order write.
- `x0` in RISC-V is architecturally constant zero; apparent writes must not become forwarding producers.
- A **store-data dependence** concerns the value written to memory, while a **store-address dependence** concerns address generation; their use stages may differ.

### Central model, mechanism, or theorem

For consumer source name `s`, form candidates from older tokens `p` satisfying `valid_p && !killed_p && writes_p && rd_p=s && rd_p!=0`. Let `p*` be the youngest such producer. If none exists, use the architecturally current register value. If `p*` has a definitive value available by the consumer's use-stage deadline, forward that value. Otherwise stall the consumer and preserve it. Never choose an older available producer over a younger unavailable match: that would deliver a stale value. Correctness requires the selected value equal the sequential ISA value for that source.

### Critical invariants

- Dependency comparison uses the exact source/destination names and per-operand use flags.
- Only older, valid, non-killed instructions that truly write a destination can produce.
- The youngest matching older producer dominates every older match.
- A result is forwarded only after its value and exception status are definitive for that path.
- An unavailable youngest match stalls rather than falling back to stale register or older-forwarded data.
- Each operand, store-data input and control comparator selects independently.
- `x0` reads zero and never obtains a forwarded apparent write.
- Stalled consumers retain identity, operands, controls and exception metadata coherently.
- Faults/flushes suppress killed producers and recompute readiness/selection correctly.
- Bypass timing, priority and fanout meet implemented clock constraints.

### Common failures

Common failures include treating all equal register fields as dependencies, forgetting that some instruction fields are immediates, forwarding writes to `x0`, prioritizing an older producer, forwarding a load address instead of load data, treating a faulting result as available, bypassing ALU operands but not store data or branch comparisons, comparing against an invalid destination, stalling only data bits but advancing controls, double-inserting bubbles, ignoring multicycle/variable-latency producers, assuming in-order RAW logic handles wider out-of-order WAR/WAW cases, and reducing stalls while lengthening the clock enough to lose performance.

### Compact example

For an invented 1,000-instruction run in a five-stage pipeline, suppose 300 adjacent RAW cases would each cost two cycles without forwarding. Base fill/drain is 1,004 cycles, so the no-forward design takes 1,604 cycles at 1.35 ns, or 461.81 MIPS. Full ALU forwarding removes 240 cases, leaving 60 one-cycle load-use stalls: 1,064 cycles at a longer 1.52 ns, or 618.32 MIPS. Scheduling half those load-use cases gives 1,034 cycles and 636.26 MIPS. These figures are synthetic; actual availability, cache latency, compiler schedule and bypass timing decide value.

### Connections

Data hazards connect ISA sequential semantics, pipeline identity, mux/compare timing, register-file behavior, cache/load latency, scheduling, scoreboards, renaming, formal refinement and performance attribution.

## Governing Question

An in-order program observes the latest older write to each source. A pipeline may read the register file before that write reaches its ordinary writeback point. Forwarding changes the physical route, not the sequential meaning.

The core design question is therefore not simply whether register numbers match. It is which live older instruction is the architecturally latest producer, whether its correct value is available at this consumer's use point, and what state must hold if it is not.

## Why This Matters

Incorrect forwarding silently computes with stale or wrong-path data. Overconservative stalling preserves correctness but sacrifices much of pipelining's throughput. The forwarding network itself can become a critical timing and energy surface.

Loads, long arithmetic, CSR operations, link values and exceptions make “the ALU result” an incomplete model. Different result classes become definitive at different stages.

Wider and out-of-order designs add multiple producers, renaming and wakeup/select. The simple in-order rules remain a useful foundation, but their assumptions must be named.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace valid instructions through pipeline stages;
- distinguish architectural names from physical values;
- explain register-file read/write timing;
- identify pipeline stalls, bubbles and flushes;
- reason about program order and precise exceptions.

Retrieve the exact ISA/profile; instruction source/destination fields and conditional use; `x0`/special-register semantics; pipeline stage contracts; decode and register-read timing; producer result classes and availability stage; exception-definitive point; consumer use stage per operand; register-file read-during-write behavior; forwarding sources/destinations; comparator/mux priority equations; load/cache response timing; store address/data paths; branch/indirect-target comparator inputs; CSR/link/multiply/divide paths; scoreboard/reservation state; stall/bubble/flush priority; reset; synthesis/STA/power/area; hazard/stall counters; compiler/workload traces; formal properties/refinement; tests/coverage; hardware/errata; and exact RTL/configuration/tool/library/revision data.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish semantic dependencies from implementation hazards;
2. classify RAW, WAR and WAW relationships and state when each can occur;
3. derive producer-match and youngest-priority equations;
4. build a forwarding network for ALU, load, link, CSR, branch and store operands;
5. detect unavailable values and generate a correct interlock;
6. integrate variable-latency and faulting producers;
7. preserve correctness across stalls, bubbles, flushes and reset;
8. compute stall-adjusted CPI, time and bypass trade-offs;
9. verify operand selection against sequential architectural values;
10. identify when scoreboarding or renaming supersedes simple comparators.

## Core Exposition

### Begin with sequential value semantics

For each source operand, the required value is the result of the latest older architectural write to that name, or the initial architectural value if none exists. This definition is independent of pipeline structure.

Forwarding is correct only when it returns that value earlier than register-file write/read would. It cannot invent a different ordering.

### Separate dependence from hazard

`add x5,x1,x2` followed by `sub x6,x5,x3` has a RAW dependence. Whether it hazards depends on when the add result becomes available and when the subtract needs it.

A dependence may require no stall because forwarding satisfies timing. Conversely, a variable-latency producer creates a hazard whose duration depends on runtime readiness.

### Classify RAW, WAR and WAW

Simple single-issue in-order pipelines read operands and write results in order, so RAW is the primary register hazard. WAR and WAW cannot reorder if all reads/writes occur in fixed order.

Multiple issue, variable completion or out-of-order execution can expose WAR/WAW. Register renaming removes false name dependences by assigning different physical destinations; later modules develop that machinery.

### Decode actual operand use

Instruction bit positions can resemble register fields while encoding immediates or suboperations. Generate `uses_rs1`, `uses_rs2`, `writes_rd` and result-class metadata from validated decode.

Illegal instructions do not create ordinary producers. Optional extension and privilege rules affect whether a decoded field participates.

### Carry producer identity

Every possible producer stage carries valid, killed/fault state, destination name, write intent, result class and instruction age. Destination zero is excluded where the ISA defines it constant.

Do not infer write intent from nonzero `rd` alone. Stores and branches may carry bit fields in the same positions without writing a register.

### Find all matching producers

For each consumer operand, compare its source name with every older in-flight destination that could still provide the latest write. Mask matches by validity, age, kill/fault policy, write intent and zero-register semantics.

Stage position gives age in a simple in-order pipeline. Queues, detached units or replay need explicit sequence/tag ordering.

### Prioritize the youngest match

Consider two older instructions both writing `x5`, followed by a consumer of `x5`. The consumer must receive the second write. Priority therefore favors the youngest older match.

Priority encoder order must reflect architectural age, not mux layout convenience. Assert that no selected producer has a younger matching predecessor.

### Never bypass an unavailable youngest producer

If the youngest match is a load still awaiting data while an older ALU write to the same register is ready, the older value is stale. Stall until the load produces or faults.

This rule separates match from availability. Choosing “any ready match” is incorrect for in-order name semantics.

### Define value availability precisely

An ALU value may be available after execute. A link value may be known from the instruction PC/length. A load value is available only after successful memory response and alignment/extension. A CSR value may depend on serialized access.

Availability also requires exception status sufficiently resolved. Forwarding a speculative value can be safe only under an explicit recovery model that prevents wrong architectural effects.

### Define consumer use stages

ALU operands and branch comparisons may be needed in execute; address base may be used there; store data may not be consumed until memory. A later use stage can avoid a stall if a dedicated bypass reaches it.

Record deadlines per operand rather than assigning one “instruction readiness” bit to all uses.

### Build operand-select logic

Each operand mux can select register-file value, immediate/PC constant, and results from relevant stages or completion buffers. Dependency control decides only among semantically valid sources.

Mux encoding and priority must be total. Invalid combinations enter safe behavior/assertions rather than synthesizer don't-cares that might enable a wrong source.

### Forward ALU results

Back-to-back arithmetic commonly forwards the older execute result to the next execute input. If the producer advances to a later stage while the consumer stalls, selection must track its new location.

Either recompute matches from current stage metadata or hold a stable producer reference. Do not freeze a mux code that no longer points to the token.

### Handle load-use hazards

In a classic five-stage organization, load data returns near the end of memory, later than the following instruction's execute-input deadline. One interlock cycle may be required even with forwarding.

Cache misses extend the wait. The consumer remains held until matched data or error is definitive; fixed one-cycle assumptions are insufficient for variable latency.

### Forward store address and data independently

A store may depend on one producer for its base address and another for data. Address is often needed in execute; data may be forwarded later into the memory/request stage.

If only address forwarding exists, adjacent producer-to-store-data sequences can write stale memory. Include byte mask and value identity in checks.

### Forward branch and indirect-target operands

Branch comparison and indirect jump targets consume register values. Resolving branches early can require bypass paths into decode; otherwise stall or resolve later.

An early comparator creates new compare/mux/fanout timing. Measure whether reduced redirect penalty outweighs its clock cost.

### Handle writeback-to-read timing

Some register files write early and read late in a cycle; others return old or undefined data on same-address read/write. A local writeback bypass makes behavior explicit and portable.

Validate the synthesized or macro-specific collision mode. RTL simulation ordering is not a physical contract.

### Integrate multicycle units

Multiply/divide or accelerator results may complete after variable cycles. A scoreboard marks destination pending and wakes consumers only when the youngest producer value is ready.

If younger independent instructions can pass, simple stage-position comparisons no longer suffice for all ordering. Define completion and precise-fault rules.

### Integrate exceptions and kills

A faulting producer cannot supply an ordinary architectural value to a consumer that will commit. In an in-order precise pipeline, the producer triggers trap and younger consumers are killed.

Wrong-path producers lose eligibility immediately on flush. Already computed bits may remain physically present but cannot forward to a live post-redirect token.

### Generate the interlock

Stall a consumer when its youngest required producer exists but cannot meet the operand's use deadline. Hold the consumer and upstream state; inject or maintain downstream flow so older work can progress.

The interlock must not repeatedly create copies of the consumer. Valid/data/control must remain coherent across the hold.

### Order stall, advance and flush controls

Flush generally dominates holding a younger doomed token. Older completion and fault priority may still proceed while front stages stall.

Write equations per stage and event combination. Informal phrases such as “stall the pipe” hide which entries hold, clear or advance.

### Consider compiler scheduling

A compiler can place independent work between a load and its consumer, reducing exposed latency. Hardware interlocks remain necessary unless the ISA explicitly specifies architecturally visible delay slots.

Scheduling opportunity depends on instruction mix and register pressure. Treat compiler version/options and binary as performance evidence.

### Evaluate the bypass network physically

Comparators, priority encoders, wide muxes and long result buses consume delay, routing, area and dynamic power. More stages/issue lanes grow the candidate set.

Place and pipeline choices can make partial forwarding faster overall than a logically maximal network. Compare instruction time, not stalls alone.

### Compute performance

For finite work, start with ideal pipeline fill/drain cycles and add nonoverlapped stalls. `CPI_eff=cycles/instructions`; time is `cycles*T_clk`; throughput is completed instructions/time.

Attribute simultaneous structural, data and control causes using a documented priority or opportunity-cost method. Hardware counters need validation against known traces.

### Verify source-value correctness

For each accepted consumer, derive expected operand from an architectural shadow model or symbolic latest-writer tracking. At use, assert selected bits and producer identity match expectation.

Also assert youngest priority, unavailable-youngest stall, no invalid/killed/zero producer, stable holds, correct store/branch paths and eventual progress under producer readiness.

### Gather layered evidence

Use decode tables, dependency matrices, directed chains, double-writer tests, load misses/errors, store/branch cases, random instruction streams/stalls/flushes, symbolic-token assertions, ISA differential tests, formal safety/liveness/refinement, synthesis/STA/area/power, counters and workload binaries.

Bind evidence to exact pipeline/configuration, register file/memories, RTL, constraints, tools/libraries, compiler/binary, workload/seeds, hardware and errata. A bypass proof for one stage organization does not automatically cover another.

## Definitions and Notation

- `s`: architectural source name requested by one consumer operand.
- `p`: an older candidate producer token.
- `p*`: youngest matching older producer.
- `rd_p`: producer architectural destination name.
- `valid_p`, `killed_p`, `writes_p`: producer qualification predicates.
- `available(p,u)`: producer value can meet consumer use point `u`.
- `value(p)`: definitive result bits for producer `p`.
- `RF[s]`: architecturally current register-file value absent an in-flight producer.
- `uses_rs1/uses_rs2`: decoded operand-use predicates.
- `T_clk`: implemented period including bypass paths.
- **latest writer:** youngest older instruction writing an architectural name.
- **interlock:** hardware rule that stalls until a dependence can be satisfied.
- **wake-up:** transition marking a pending value ready for consumers.
- **false dependence:** ordering caused by name reuse rather than value flow.
- **shadow model:** independent expected architectural writer/value tracking used for verification.

## Mechanisms, Invariants, or Proof Structure

1. **Decode obligation:** source/destination names and use/write predicates exactly match each legal instruction.
2. **Qualification obligation:** only older, valid, non-killed, true writers with legal destinations become candidates.
3. **Match obligation:** every in-flight latest writer relevant to each source/use point is considered.
4. **Priority obligation:** the selected candidate is the youngest matching older producer.
5. **Availability obligation:** forwarded bits are definitive and meet the consumer capture deadline.
6. **Stale-value obligation:** an unavailable youngest match forces a stall, never selection of an older/register value.
7. **Operand obligation:** ALU, address, store-data, branch and indirect-target operands each select correctly.
8. **Zero-register obligation:** the constant-zero architectural source cannot be overridden by apparent writes.
9. **Hold obligation:** a stalled consumer and all metadata remain coherent without duplication.
10. **Flush obligation:** killed/faulting producers and consumers cannot forward, write or commit ordinary effects.
11. **Variable-latency obligation:** pending/wakeup/tag state matches multicycle and memory completions once.
12. **Commit obligation:** resulting register/memory/control effects equal sequential ISA execution.
13. **Progress obligation:** under stated producer/resource fairness, every live non-killed consumer eventually advances or traps.
14. **Timing obligation:** compare, priority, mux, bus and register-file collision paths meet all implemented constraints.
15. **Evidence obligation:** correctness and performance bind to exact stage/configuration, physical and workload artifacts.

## Alternatives and Trade-Offs

1. **Stall versus forward:** stalls simplify paths; forwarding improves CPI with mux/compare cost.
2. **Full versus partial forwarding:** full coverage minimizes common waits; partial networks can improve frequency/energy.
3. **Central versus distributed detection:** central logic exposes priority; distributed controls can shorten local paths and complicate consistency.
4. **Stage-index versus explicit age:** stage order is compact in simple pipes; tags handle queues/replay and need wrap proof.
5. **Early versus late register read:** early read exposes more RAW distance; late read may increase decode/execute timing.
6. **Early versus late branch comparison:** early reduces redirect cost; late reuses execute forwarding.
7. **Execute versus memory store-data bypass:** early path is uniform; later path can avoid a stall and needs request-stage muxing.
8. **Fixed load stall versus readiness interlock:** fixed is small for fixed memory; readiness handles variable latency.
9. **Register-file collision mode versus explicit bypass:** macro behavior can be cheap; explicit mux is portable/auditable.
10. **Comparator matrix versus scoreboard:** matrices suit shallow in-order pipes; scoreboards manage variable producers.
11. **Interlock versus compiler scheduling:** hardware is correct for all binaries; scheduling reduces common exposed latency.
12. **Speculative versus definitive forwarding:** speculation can reduce waits; recovery and exception proof expand.
13. **Wide result bus versus local bypasses:** shared routing is uniform; local paths can reduce fanout and add cases.
14. **Renaming versus name interlocks:** renaming removes WAR/WAW and expands concurrency; maps/free lists/recovery add state.
15. **Fewer stalls versus shorter clock:** maximal bypass may reduce CPI while losing frequency or energy efficiency.

## Failure Modes and Misconceptions

1. “A dependence always causes a stall.” Forwarding may satisfy it.
2. “A hazard is an ISA property.” It depends on implementation timing.
3. “In-order pipelines have every hazard type.” Simple fixed-order pipelines primarily expose RAW register hazards.
4. “Equal bit fields mean a dependence.” Decode must say whether fields are sources/destinations.
5. “Nonzero `rd` proves a write.” Instruction class and legality also matter.
6. “Writes to `x0` can forward their computed bits.” Architectural reads remain zero.
7. “Any matching producer is acceptable.” The youngest older match is required.
8. “Any ready producer is acceptable.” An older ready value is stale behind a younger pending writer.
9. “Execute output is always definitive.” Loads, faults and variable units differ.
10. “Load address can satisfy load use.” The consumer needs returned data.
11. “One load-use bubble handles every load.” Cache/memory latency can vary.
12. “Forwarding two ALU inputs completes coverage.” Store data, branches and indirect targets also consume values.
13. “A stalled mux selection stays correct.” The producer may advance to another stage.
14. “Forwarding from invalid data is harmless.” It can corrupt live results if validity does not gate selection.
15. “Wrong-path values are safe if never written back.” They must not influence live post-redirect work.
16. “A faulting producer may feed younger instructions.” Precise handling normally kills them and suppresses ordinary value use.
17. “Register-file simulation defines collision behavior.” The mapped macro contract governs hardware.
18. “Scoreboard pending means value location.” Readiness, tag and source selection are separate.
19. “Fixed stage position always proves age.” Detached/replayed operations need explicit identity.
20. “Stalling one register is enough.” The entire consumer bundle/control must hold coherently.
21. “Flush and stall commute.” Wrong priority can retain a killed consumer.
22. “Compiler scheduling removes interlocks.” Correctness cannot depend on optional scheduling absent ISA delay slots.
23. “More bypasses always help performance.” Timing, routing and power can dominate.
24. “Lower data-stall counter proves speedup.” Period and other stalls may change.
25. “Directed chains prove priority.” Double-writer and adversarial latency cases are essential.
26. “One configuration's forwarding proof generalizes.” Stage/result timing changes with options.

## Worked Examples

### Example 1

`add x5,...; sub ...,x5,...` forwards the add's execute result to the sub's execute input when timing permits.

### Example 2

`add x5,...; add x5,...; sub ...,x5,...` selects the second add. Selecting the older first add violates latest-writer semantics.

### Example 3

`load x5,...; add ...,x5,...` stalls while load data is unavailable, then forwards the successful extended response.

### Example 4

An older ALU write to `x5` is ready but a younger load to `x5` is pending. The consumer stalls rather than using the older value.

### Example 5

`add x7,...; store x7,0(x2)` uses a store-data bypass even if the store address itself comes from the register file.

### Example 6

`add x2,...; store x7,0(x2)` forwards the base to address generation; address and store-data dependencies are checked separately.

### Example 7

An apparent producer has destination `x0`. Qualification removes it and the consumer receives architectural zero.

### Example 8

A branch depends on a prior result. Resolve in execute using the standard bypass, or add an earlier comparator path and verify its timing.

### Example 9

A wrong-path multiply returns after redirect. Its killed tag cannot wake or forward to a live consumer, and is released only under safe tag rules.

### Example 10

This deterministic model compares synthetic stall and clock-period effects of forwarding and scheduling.

<!-- bijux-verify: {"id":"data-forwarding-performance-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"no_forward_cycles=1604 effective_cpi=1.604 time_ns=2165.40 throughput_mips=461.81\nforward_cycles=1064 effective_cpi=1.064 time_ns=1617.28 throughput_mips=618.32\nscheduled_cycles=1034 effective_cpi=1.034 time_ns=1571.68 throughput_mips=636.26\n"}} -->
```python
instructions = 1000
pipeline_depth = 5
base_cycles = instructions + pipeline_depth - 1
raw_cases = 300
forwarded_alu_cases = 240
load_use_cases = raw_cases - forwarded_alu_cases

def report(name, cycles, period_ns):
    time_ns = cycles * period_ns
    print(
        f"{name}_cycles={cycles} effective_cpi={cycles / instructions:.3f} "
        f"time_ns={time_ns:.2f} throughput_mips={1000 * instructions / time_ns:.2f}"
    )

report("no_forward", base_cycles + 2 * raw_cases, 1.35)
report("forward", base_cycles + load_use_cases, 1.52)
report("scheduled", base_cycles + load_use_cases // 2, 1.52)
```

The inputs assume nonoverlapping fixed stalls and invented periods. Real evidence needs actual result timing, caches, binaries, physical implementation and validated counters.

## Cross-Program Connections

- **ISA:** sequential latest-writer semantics define the required source value.
- **Digital Logic:** comparator matrices, priority encoders, muxes and buses implement bypassing.
- **Compilers:** instruction scheduling can hide exposed producer latency.
- **Data Structures:** scoreboards, tags and maps track pending writers/readiness.
- **Operating Systems:** counter attribution and context state affect performance observation.
- **Formal Methods:** shadow latest-writer models and refinement prove selected values.
- **Performance Engineering:** stall opportunity, CPI, clock period and power determine value.
- **Security Engineering:** wrong-path or stale-value forwarding must not cross protection/control boundaries.

## References

1. RISC-V International, [RV32I Base Integer Instruction Set](https://docs.riscv.org/reference/isa/unpriv/rv32.html), architectural register, `x0`, load/store and control-flow semantics; retrieved 2026-09-04.
2. lowRISC, [Ibex Pipeline Details](https://ibex-core.readthedocs.io/en/latest/03_reference/pipeline_details.html), current stalls, forwarding and multicycle behavior; retrieved 2026-09-04.
3. lowRISC, [Ibex Instruction Decode and Execute](https://ibex-core.readthedocs.io/en/latest/03_reference/instruction_decode_execute.html), current decode, controller and execution behavior; retrieved 2026-09-04.
4. OpenTitan, [RV Core Ibex](https://opentitan.org/book/hw/ip/rv_core_ibex/), current integrated configuration, security and verification context; retrieved 2026-09-04.
5. Berkeley Architecture Research, [BOOM Pipeline Overview](https://docs.boom-core.org/en/latest/sections/intro-overview/boom.html), current open wider/out-of-order pipeline context; retrieved 2026-09-04.
6. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), pipeline hazard/forwarding teaching resources; retrieved 2026-09-04.
7. YosysHQ, [Yosys Documentation](https://yosyshq.readthedocs.io/projects/yosys/en/latest/), synthesis evidence for implemented compare, mux, register and timing structures; retrieved 2026-09-04.
8. RISC-V International, [Sail RISC-V Model](https://github.com/riscv/sail-riscv), independent executable sequential ISA semantics; retrieved 2026-09-04.

## Exercises

### Exercise 1

Derive forwarding equations for both source operands in a five-stage in-order RV32I pipeline with producer candidates in memory and writeback stages.

### Exercise 2

Extend the design for loads, stores and branches. State every consumer use point and when a stall remains necessary.

### Exercise 3

Analyze a three-instruction sequence with two older writes to the same destination and a consumer, including the case where the youngest write is a cache-missing load.

### Exercise 4

Recompute the executable performance comparison and explain which assumptions make the result unsafe to generalize.

### Exercise 5

Write a verification plan for forwarding in a configurable pipeline with a variable-latency multiplier and random flush/reset events.

## Answers to the Exercises

### Answer 1

For each used source, qualify memory/writeback candidates by older valid, not killed/faulting, true register write, nonzero destination and destination equals source. In a simple in-order stage chain, the memory candidate is younger than writeback and has priority. If neither matches, select the register-file value.

Gate selection on value availability. If the priority match is unavailable, request an interlock rather than choose writeback/RF. Assert the selected producer is the youngest match and its bits equal a sequential shadow latest-writer value.

### Answer 2

ALU/address/branch operands are typically needed at execute. Load data may not be ready for the immediately following execute, so stall until successful response, then forward. Store base follows address timing; store data may use a separate later bypass into the memory/request stage, potentially avoiding an early stall.

Branch and indirect-target operands use the same latest-writer rule at their actual comparator/target stage. Load error marks the producer faulting and kills younger consumers; it does not forward ordinary data. Variable response latency, not a fixed opcode table alone, controls readiness.

### Answer 3

For `write1 x5; write2 x5; read x5`, both match but `write2` is the latest writer. If ready, select it regardless of `write1`. If `write2` is a cache-missing load, stall even when `write1` is available, because choosing `write1` would expose the overwritten value.

On load success, forward returned/extended data. On fault, suppress ordinary write and take precise trap, killing the younger read. On flush of both younger operations, neither may forward into the replacement path.

### Answer 4

The model gives 1,604 cycles at 1.35 ns (2,165.40 ns, 461.81 MIPS), 1,064 cycles at 1.52 ns with forwarding (1,617.28 ns, 618.32 MIPS), and 1,034 cycles with half load-use cases scheduled away (1,571.68 ns, 636.26 MIPS).

It assumes 300 fixed adjacent RAW cases, two stalls without forwarding, 60 one-cycle loads after forwarding, no overlap with other stalls, fixed cache latency, known clock penalties and unchanged code. Real workloads, misses, compiler schedules, stage configurations, physical routing, power and counter attribution can reverse conclusions.

### Answer 5

Build a decode/source-use matrix and result-availability table per configuration. Directed tests cover every producer/consumer distance and operand, double writers, zero destination, ALU/load/link/CSR/multiplier, store address/data, branches, faults and same-cycle register-file collisions. Randomize producer latency, stage stalls, flush, reset and tag reuse.

Assert candidate qualification, youngest priority, unavailable-youngest stall, selected value against a shadow model, stable holds, no killed forwarding, one wakeup, precise commit and eventual progress under fairness. Run differential ISA tests, formal safety/liveness/refinement, synthesis/STA/place-route/power and validated workload counters. Bind exact RTL/configuration, memories, tools, binaries, seeds and hardware; no external certification is claimed.
