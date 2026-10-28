---
module_id: CA-038
program: Computer Architecture
level: 1
module_number: 38
title: DRAM Timing and Controllers
status: complete
last_verified: 2026-09-04
---

# DRAM Timing and Controllers

## One-Page Review

### Governing question

How does a memory controller transform concurrent reads, writes, refreshes and power/RAS work into legal DRAM commands that preserve data and ordering, meet every timing/retention constraint, use banks and buses efficiently, prevent starvation and produce latency behavior that software can trust?

### Essential definitions

- **ACTIVATE** (`ACT`) opens a selected row into a bank's row buffer.
- **READ** and **WRITE** select columns of an open row and schedule data-bus bursts.
- **PRECHARGE** (`PRE`) closes a bank's active row so another may be activated.
- **REFRESH** (`REF`) restores charge in required rows/banks within a retention interval.
- `tRCD` is the minimum activate-to-column-command delay under the applicable specification.
- `tCL` is a read column latency convention; command/data timing must use the exact standard/device definition.
- `tRP` is the minimum precharge-to-activate delay.
- `tRAS` is a minimum active-row time before precharge.
- `tRC` constrains successive activates to a bank and commonly relates to `tRAS+tRP` under stated bins.
- `tRRD`, `tFAW`, `tCCD`, `tWTR` and `tRTW` represent activate-rate, column-spacing and bus-turnaround families with generation/group variants.
- A **row hit** targets the row already active in its bank; a **row conflict** targets a different row; an **empty-bank access** finds no row active.
- **open-page policy** keeps a row active in hope of reuse; **close-page policy** precharges early.
- **FR-FCFS** prioritizes ready (often row-hit) commands, then older requests, subject to legality and fairness.
- A **write drain** batches queued writes to amortize read/write bus turnarounds.
- **refresh postponement/pull-in** reschedules refresh within the exact permitted window, not indefinitely.

### Central model, mechanism, or theorem

At cycle `t`, the controller may issue command `c` only when bank/rank state, all relevant timing scoreboards, data-bus reservations, refresh/power obligations and ordering rules say `legal(c,t)`. Scheduling selects among legal commands but cannot relax legality. A request completes only after its full required command/data/error path. Optimization seeks useful bandwidth and bounded latency through bank parallelism, row locality and batching, while data safety requires every accepted write to remain owned until committed and every refresh deadline to be met.

### Critical invariants

- No command issues before every applicable same-bank, bank-group, rank, channel and bus timing constraint is satisfied.
- ACT/RD/WR/PRE target the request's exact decoded channel/rank/bank/row/column and beat lanes.
- A column command targets the currently active matching row; conflicting rows are precharged/activated first.
- Data-bus bursts and direction turnarounds never overlap illegally.
- Every accepted read/write retains identity, ordering, mask, data and response state until one terminal result.
- Posted/merged writes preserve byte values and ordering; reads forward from older buffered writes as required.
- Refresh is neither lost nor postponed beyond the device/platform retention contract.
- Scheduling optimizations cannot violate coherence, atomic, fence or device-memory order.
- Demand, writes, refresh and RAS traffic have a conditional progress guarantee under stated fairness.
- Timing/performance results bind exact speed bin, clock/data-rate conversion, topology, mapping, policy and workload.

### Common failures

Common failures include comparing nanosecond timings as if they were cycles, rounding cycle minima down, issuing RD to a closed/wrong row, enforcing only `tRCD/tRP` while missing rank/group constraints, double-booking the data bus, indefinitely favoring row hits, draining writes until reads starve, acknowledging a write before retaining its data, merging across fences/device attributes, forwarding the wrong byte version, postponing refresh beyond limits, treating refresh as average bandwidth only, using queue arrival order as architectural order, confusing command clock with transfers/s, and claiming controller throughput from a zero-contention trace.

### Compact example

In an invented one-bank fixed-time model with `tRCD=tCL=tRP=4` time units and rows `[1,1,2,2,1]`, an open-page schedule takes 60 units: three row openings, two row hits and two conflict precharges. A close-page schedule takes 76 units when it performs 12 units of activate/read service per request plus four 4-unit inter-request precharges. Average modeled service is 12.0 versus 15.2 units. The model omits `tRAS`, bursts, arrivals, ranks/banks, refresh, writes and overlap and therefore teaches accounting only.

### Connections

DRAM timing/controllers connect synchronous protocols, constraint scheduling, queueing, bank/channel mapping, cache misses/writebacks, refresh/retention, ECC, power/thermal management, coherence ordering, fairness/QoS, simulation validation and physical-interface training.

## Governing Question

DRAM exposes parallel banks but imposes many minimum delays and shared-resource constraints. A controller observes requests at cache-line granularity, decodes them into array locations and schedules commands over time.

Correctness comes before policy: a scheduler chooses only legal actions. Performance then depends on when rows remain open, how requests are reordered, when writes/refreshes drain and whether workloads expose parallelism.

## Why This Matters

Main-memory latency is not a constant. Row state, queue position, refresh, bus direction, bank conflicts and other requesters create a distribution. Dependent misses often experience its tail.

Controllers can improve throughput by prioritizing ready row hits, but unbounded preference starves conflicts. Write batching saves turnarounds but delays reads and durable visibility. Refresh protects data while interrupting service.

Timing parameters also change with data rate, device bin, topology and temperature. A plausible but wrong unit conversion can violate silicon constraints.

## Prerequisites and Retrieval

Before studying this module, be able to:

- identify channels, ranks, banks, rows, columns and bursts;
- decode a physical address into main-memory fields;
- distinguish latency, throughput, queueing and parallelism;
- explain cache writebacks, ordering and ECC at a basic level;
- convert time minima into clock cycles conservatively.

Retrieve exact memory standard/device/rank/module/PHY and speed bin; command clock and data rate; topology and address map; timing tables including same/different bank-group variants; mode-register settings; burst length and data-bus timing; controller queue/entry depths; read/write/atomic/device ordering; write merge/forward rules; page policy; scheduler/age/QoS policy; bank/rank/channel arbitration; refresh mode, interval, temperature multiplier and allowed postponement; power-down/self-refresh; ECC/retry/poison; row-hammer/repair mitigations; calibration/training; counters and timestamps; simulator/RTL/firmware/OS/hardware revisions, workloads, seeds, environmental conditions and errata.

## Learning Objectives

After completing this module, you should be able to:

1. trace ACT, RD, WR, PRE and REF command sequences;
2. convert documented time constraints to conservative cycle constraints;
3. distinguish row hit, row conflict and empty-bank access;
4. compare open-, close- and adaptive-page policies;
5. explain FR-FCFS, age/QoS controls and starvation risks;
6. integrate read/write queues, merging, forwarding and bus turnarounds;
7. schedule refresh and power transitions without data loss;
8. model bank parallelism, queueing, bandwidth and latency distributions;
9. verify command legality, data refinement, ordering and progress;
10. validate a controller using reference models, RTL and hardware evidence.

## Core Exposition

### Separate requests from commands

A cache-line read may require PRE, ACT, RD and multiple data beats. A write may wait in a buffer, merge, acquire ordering permission and issue WR after bus turnaround.

Keep request identity across commands and response completion. Command issue is not request completion.

### Decode before scheduling

Translate the physical line address into channel, rank, bank group, bank, row and column. The controller must use the same mapping as firmware and diagnostic models.

Mapping determines which requests can overlap and which share a row. Scheduler results are meaningless if decode differs from the evaluated system.

### Track bank state

Each bank records whether it is closed, active on row `r`, precharging, refreshing or unavailable. Column commands require the intended row to be active.

Transitions must reflect command acceptance and timing, not optimistic request selection.

### Activate a row

ACT selects a closed bank row and begins sensing/restoring it into the row buffer. RD/WR cannot follow until the relevant activate-to-column minimum.

Activation also participates in rank/bank-group power constraints such as minimum gaps and rolling windows.

### Read a column

RD schedules a future data burst from the active row. Reserve the channel data bus at the correct future beats, including generation-specific latency conventions.

Read completion includes integrity/error handling and delivery to the requester, not merely command issue.

### Write a column

WR schedules controller-to-DRAM data beats and establishes write-recovery constraints before precharge. Retain data/masks until the interface accepts the entire obligation.

If the external protocol acknowledges earlier, controller state becomes the owner of pending data and must survive required faults/reset semantics.

### Precharge safely

PRE closes the active row after minimum active time and write recovery. Another ACT waits the required precharge interval.

An auto-precharge flag couples the close to a column command but does not eliminate timing constraints.

### Refresh on time

Refresh restores rows whose charge leaks. The controller tracks due work and blocks/conflicts with normal commands as the device mode specifies.

Allowed postponement or pull-in is bounded. Average refresh rate is insufficient if a particular window exceeds retention rules.

### Convert units correctly

Standards commonly give constraints as a minimum time, a minimum cycle count or the maximum of both. Convert using the actual command clock and round upward.

Data transfers/s and command cycles are different units. Publish the formula and selected mode registers.

### Enforce all timing scopes

Some delays apply within one bank, others across banks, bank groups, ranks or the shared channel. Maintain scoreboards or next-legal timestamps at each scope.

Checking only the target bank misses activation-power and data-bus constraints.

### Reserve the data bus

RD and WR commands cause bursts later than command issue. A reservation calendar prevents overlapping beats and enforces read/write turnarounds.

Ranks may share the same bus, so independent bank legality does not imply burst compatibility.

### Classify row state

A row hit targets the active matching row. A conflict requires closing the current row; an empty access needs activation but no conflict precharge.

Counter definitions vary: some classify at arrival, scheduling or issue. Record the point, because intervening commands can change state.

### Use open-page policy

Open-page leaves a row active after access, favoring future locality. It saves PRE/ACT on hits but makes a conflicting access pay close/open latency.

It can also let ready hits dominate scheduling, so pair it with age/fairness controls.

### Use close-page policy

Close-page precharges after an access, reducing conflict penalty when reuse is unlikely. It wastes locality when the next request targets the same row.

Auto-precharge timing and command opportunity must be modeled, not assumed free.

### Adapt page policy

Predictors can learn row reuse or queue visibility can reveal pending hits/conflicts. Adaptive policy chooses when to close based on evidence.

Misprediction changes latency/energy but must never violate minimum active/recovery timing.

### Schedule ready commands

FR-FCFS-like scheduling favors commands that are legal now, often row hits, then uses request age. This raises throughput/row locality under many loads.

Readiness is a command property, not permission to reorder architecturally constrained requests.

### Prevent starvation

Continuous row hits can delay an old conflict indefinitely. Age caps, batching limits, QoS deadlines or periodic oldest-first modes bound unfairness.

State the bound and downstream fairness assumptions. Average latency cannot prove individual progress.

### Exploit bank parallelism

While one bank waits for activation or precharge, commands to another may issue if rank/channel constraints allow. Address mapping and queue diversity expose this opportunity.

Bank count is an upper structural opportunity, not a guarantee of parallel demand.

### Exploit rank and channel parallelism

Ranks can overlap some array work but share buses; channels provide more independent paths. Arbitration should balance utilization and QoS.

Rank switches and channel crossing/interconnect routes add delay and energy.

### Queue reads

Read entries carry address, request ID, ordering class, arrival age, dependent destinations and completion state. Compatible same-line reads may merge.

Reserve response capacity or backpressure admission so returned data is never dropped.

### Queue and merge writes

Write buffers decouple upper acceptance and combine compatible byte masks. Merge only when memory type, address, ordering, atomicity and error semantics permit.

Loads search older buffered writes and forward newest applicable bytes before using DRAM data.

### Drain writes deliberately

Switching the bus to writes has turnaround cost, so controllers often drain a batch when high watermark is reached and return to reads at a low watermark.

Bound write latency and read starvation. Persistent or fence operations may force earlier drain under platform rules.

### Preserve ordering

Physical scheduling may reorder independent normal-memory operations, but coherence, atomics, fences, releases/acquires and device accesses constrain observable results.

Track dependency/order domains explicitly rather than assuming queue FIFO or unrestricted address reordering.

### Integrate coherence

Dirty cache writebacks and reads arrive after coherence decisions; controllers still must preserve same-address order and responses. Home/directory traffic can share interconnect resources.

Memory completion does not itself authorize a stale cache copy. The coherent hierarchy defines visibility.

### Handle ECC and retries

Read data passes integrity checking; corrected/uncorrectable outcomes follow platform reporting, poison and retry policy. Write ECC may require merged complete codewords.

Retry retains unique request identity and cannot duplicate a write. A dirty/newest value cannot be discarded on error.

### Schedule scrub and repair work

Patrol scrub, row sparing and diagnostic commands compete with demand and refresh. Give them deadlines/quotas appropriate to reliability goals.

Coordinate corrective writes with caches/coherence and preserve error telemetry.

### Manage power states

Idle ranks/channels may enter power-down or self-refresh. Entry waits for legal quiescence; exit adds wake latency and retraining where required.

Power policy trades background energy against bursts/tails. Unsupported loss of retained state must not be exposed as valid.

### Account for temperature

Refresh requirements and timing margins may vary with temperature. Sensor policy needs conservative failure behavior when readings are absent or out of range.

Thermal throttling changes rate/latency; bind measurements to environmental conditions.

### Address disturbance risks

Repeated activation patterns can create retention/disturbance risk in susceptible devices. Controllers/platforms may use increased refresh, tracking or vendor mechanisms.

Mitigation effectiveness is device- and threat-dependent. It consumes commands/capacity and needs validation beyond functional timing.

### Model latency as a distribution

Break request latency into queue, row preparation, column/data, turnarounds, refresh and response components. Report percentiles and by-class results.

Dependent reads and real-time clients care about tails; bulk streams may care more about sustained bandwidth.

### Model bandwidth honestly

Count useful payload and bus beats plus command utilization, refresh, retries and idle/conflict causes. Peak data rate is a ceiling.

Separate read and write bandwidth and note whether write acknowledgment or media-array completion defines the endpoint.

### Validate timing models

Cross-check parameter parsing, units and command traces against authoritative specs/device models. Directed sequences should hit every minimum boundary and one-cycle-too-early rejection.

Differential testing between independent simulators can find bugs but agreement is not proof if parameters share mistakes.

### Verify controller safety

Assert legal command issue, active-row match, no bus collision, retained accepted requests/writes, response matching and refresh deadlines.

Stress full queues, simultaneous events, same-address races, errors, resets, mode changes and long adversarial row-hit streams.

### Gather layered evidence

Use hand traces and executable schedules, then reference models, randomized timing checkers and formal bounded properties. Run cycle simulation on microbenchmarks/applications.

Validate RTL with PHY/model interfaces and hardware counters/analyzers where authorized. Bind speed bin, topology, mapping, firmware, temperature and errata.

## Definitions and Notation

- `tCK`: command clock period under the configured mode.
- `ceil(T/tCK)`: minimum whole cycles satisfying a time minimum `T`.
- `tRCD`, `tCL`, `tRP`, `tRAS`, `tRC`: representative activate/read/precharge cycle constraints under exact definitions.
- `tRRD` and `tFAW`: representative activate-rate constraints across banks/windows.
- `tCCD`: representative column-to-column spacing.
- `tWTR`, `tRTW`: representative write/read direction turnaround constraints.
- `tREFI`: nominal interval family for refresh scheduling.
- `tRFC`: refresh-cycle unavailability family.
- `open[b]`: active row or closed state for bank `b`.
- `legal(c,t)`: all state, timing, bus, refresh and ordering predicates permit command `c` at time `t`.
- `arrival(r)`, `complete(r)`: request timestamps under stated endpoints.
- `latency(r)=complete(r)-arrival(r)`.
- `row_hit_rate`: row hits divided by classified requests under a documented classification point.

Names are mnemonic families, not universal numeric meanings. DDR generations, bank groups, modes and vendors define variants; use the exact authoritative parameter set.

## Mechanisms, Invariants, or Proof Structure

1. **Decode obligation:** commands carry the request's exact channel/rank/bank/row/column/beat identity.
2. **State obligation:** ACT/RD/WR/PRE/REF transitions match current bank/rank/power state.
3. **Timing obligation:** every issued command satisfies all applicable next-legal timestamps and rolling windows.
4. **Bus obligation:** future read/write bursts and turnarounds never collide.
5. **Retention obligation:** accepted reads/writes retain ID/data/mask/order until one terminal outcome.
6. **Forwarding obligation:** reads observe newest older buffered bytes where required.
7. **Merge obligation:** combined writes preserve byte values and do not cross prohibited ordering/attribute boundaries.
8. **Refresh obligation:** every required refresh occurs within exact permitted scheduling windows.
9. **Ordering obligation:** reordering refines architectural/coherent/atomic/device rules.
10. **Integrity obligation:** ECC/retry/poison never returns corrupt data as valid or duplicates writes.
11. **Lifecycle obligation:** mode, power, reset and training changes expose only supported trustworthy state.
12. **Fairness obligation:** age/QoS/batching prevents indefinite starvation under stated downstream fairness.
13. **RAS obligation:** scrub/repair/disturbance work meets safety deadlines without losing requests.
14. **Accounting obligation:** latency, row classification, traffic and queue counters use exact endpoints.
15. **Evidence obligation:** claims bind timing units, device bin, controller policy, mapping, workload and environment.

Prove command legality from state/scoreboard invariants and data refinement from retained queue/write-forward state. Compose ordering at the coherence interface and liveness with explicit fairness/deadline assumptions. Performance scheduling remains empirical after safety constraints are established.

## Alternatives and Trade-Offs

1. **Open versus close page:** open favors row reuse; close reduces predicted conflict cost.
2. **Static versus adaptive page policy:** static is simple; adaptive follows phases with predictor cost.
3. **FCFS versus ready-first:** FCFS improves fairness; ready-first increases row/bank efficiency.
4. **Throughput versus age priority:** throughput exploits locality; age caps bound tails/starvation.
5. **Separate versus unified read/write queues:** separate queues ease batching; unified age comparison is direct.
6. **Long versus short write drains:** long drains amortize turns; short drains protect read latency.
7. **Fine versus coarse address interleaving:** fine exposes banks; coarse can preserve row locality.
8. **Aggressive versus conservative reordering:** aggressive raises utilization; conservative simplifies ordering/QoS.
9. **Deep versus shallow queues:** deep exposes choice/parallelism; shallow bounds delay/state/energy.
10. **All-bank versus per-bank refresh:** all-bank simplifies control; per-bank can retain service opportunity.
11. **Postpone versus immediate refresh:** postponement avoids busy periods; immediate work reduces deadline risk.
12. **Performance versus power-down:** staying active avoids wake cost; low-power states save idle energy.
13. **Demand versus scrub priority:** demand lowers visible latency; scrub deadlines protect reliability.
14. **Analytical versus cycle models:** analytical models explain bounds; cycle models capture command interactions.
15. **Peak throughput versus tail guarantees:** peak policies maximize average service; QoS reservations bound clients.

## Failure Modes and Misconceptions

1. “A memory request is one DRAM command.” It can require close, activate, column and data phases.
2. “RD can open a row.” ACT establishes active row state first.
3. “PRE is free after a read.” Minimum active/recovery/precharge constraints apply.
4. “Timing values are all cycles.” Specifications mix times and cycle minima.
5. “Round-to-nearest is safe.” Minimum delays require upward rounding.
6. “GT/s is the command clock.” Data transfers and command clocks differ.
7. “Checking target-bank timing is sufficient.” Rank/group/channel/bus constraints also apply.
8. “Different banks mean simultaneous bursts.” They can share one data bus.
9. “Row hit means immediate response.” Queueing, column spacing and bus reservations remain.
10. “Open page always wins on locality.” Conflicts, fairness and energy alter results.
11. “Close page precharge costs nothing.” It uses timing/commands even when coupled automatically.
12. “FR-FCFS is fair because age breaks ties.” A stream of ready hits can keep conflicts unready.
13. “Deep queues only reduce latency.” They can increase choice and throughput while worsening tails.
14. “Write queues may acknowledge without capacity.” Accepted data must be retained.
15. “Same-address writes may always merge.” Fences, atomics, attributes and error semantics constrain merging.
16. “Reads can ignore buffered writes.” They may need byte-wise forwarding.
17. “Long write drains always improve bandwidth.” They can starve reads and violate QoS.
18. “Refresh is a constant percentage loss.” Placement creates bursts and latency tails.
19. “Refresh may be deferred while demand exists.” Postponement is strictly bounded.
20. “Self-refresh means no retained power.” DRAM retention still requires specified power/conditions.
21. “ECC correction ends the transaction.” Reporting, scrub/rewrite, poison or retry may follow.
22. “Retrying a write is automatically safe.” Identity/acceptance must prevent duplication.
23. “Controller order is architectural order.” Only required dependencies/order domains constrain observation.
24. “Peak pin bandwidth validates a scheduler.” Useful sustained traffic and latency distributions are needed.
25. “Two simulators agreeing proves timing.” Shared parameter/unit errors can agree.
26. “Passing random tests proves refresh/liveness.” Deadline and adversarial starvation properties need targeted proof/tests.

## Worked Examples

### Example 1

Closed bank, row A: issue ACT, wait `tRCD`, issue RD and receive data after the configured column/burst timing.

### Example 2

Active row A, request row A: it is a row hit but still waits for column spacing and a free future data-bus slot.

### Example 3

Active row A, request row B: wait minimum active/recovery constraints, PRE, wait `tRP`, ACT B, then wait `tRCD` before RD.

### Example 4

A 13.75 ns minimum with 1.25 ns `tCK` needs 11 cycles exactly; a 14 ns minimum at the same clock needs 12 cycles after upward rounding.

### Example 5

Four activates to different banks can still violate a rolling activation window; per-bank checks alone miss the rank power limit.

### Example 6

A write buffer merges disjoint byte masks to one line. A younger read forwards updated lanes and obtains remaining lanes from cache/DRAM state.

### Example 7

The write queue reaches its high watermark, drains until low watermark, then switches to reads while an age limit prevents either class from indefinite starvation.

### Example 8

Refresh becomes due during a row-hit stream. The deadline policy closes/prepares the rank and issues refresh rather than preserving throughput until retention is violated.

### Example 9

Two banks overlap ACT delays, but RD bursts serialize on the shared channel bus; bank parallelism hides array latency without doubling bus width.

### Example 10

This deterministic single-bank model compares simplified open- and close-page service for repeated/conflicting rows.

<!-- bijux-verify: {"id":"dram-page-policy-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requests=5 row_hits=2 row_openings=3 conflict_precharges=2\nopen_page_total=60 open_page_average=12.00\nclose_page_total=76 close_page_average=15.20 modeled_reduction_pct=21.05\n"}} -->
```python
rows = [1, 1, 2, 2, 1]
t_rcd = 4
t_cl = 4
t_rp = 4
burst = 4

open_row = None
open_total = 0
row_hits = 0
row_openings = 0
conflict_precharges = 0
for row in rows:
    if open_row == row:
        row_hits += 1
        open_total += t_cl + burst
    else:
        if open_row is not None:
            open_total += t_rp
            conflict_precharges += 1
        open_total += t_rcd + t_cl + burst
        row_openings += 1
        open_row = row

close_total = len(rows) * (t_rcd + t_cl + burst) + (len(rows) - 1) * t_rp
reduction = 100 * (close_total - open_total) / close_total

print(f"requests={len(rows)} row_hits={row_hits} row_openings={row_openings} conflict_precharges={conflict_precharges}")
print(f"open_page_total={open_total} open_page_average={open_total / len(rows):.2f}")
print(f"close_page_total={close_total} close_page_average={close_total / len(rows):.2f} modeled_reduction_pct={reduction:.2f}")
```

The timing values and trace are invented. The model serializes one bank and omits `tRAS`, `tRC`, group/rank constraints, actual burst reservation, arrivals, writes, refresh, ECC and overlap; it verifies only stated arithmetic.

## Cross-Program Connections

- **Algorithms:** constrained online scheduling chooses among legal commands with uncertain future arrivals.
- **Concurrent Systems:** queues, scoreboards, credits and arbitration require safety and progress.
- **Operating Systems:** NUMA placement, QoS and error reporting shape controller demand.
- **Real-Time Systems:** deadlines and interference bounds matter beyond average throughput.
- **Reliability Engineering:** refresh, ECC, scrub, repair and thermal policy preserve data.
- **Security Engineering:** bank/row contention and disturbance create leakage and integrity risks.
- **Performance Engineering:** row state, turns, occupancy, percentiles and bandwidth explain behavior.
- **Formal Methods:** command legality, retained writes, refresh deadlines and fairness support proofs.

## References

1. gem5, [Memory System](https://www.gem5.org/documentation/general_docs/memory_system/), current memory-controller and system modeling context; retrieved 2026-09-04.
2. gem5, [gem5 Standard Library Memory Components](https://www.gem5.org/documentation/general_docs/memory_system/gem5_memory_system/), current memory component/channel configuration context; retrieved 2026-09-04.
3. SAFARI Research Group, [Ramulator 2.0](https://github.com/CMU-SAFARI/ramulator2), current modular DRAM standard/controller simulation and validation framework; retrieved 2026-09-04.
4. TU Kaiserslautern, [DRAMSys](https://github.com/tukl-msd/DRAMSys), current configurable DRAM subsystem simulation and analysis framework; retrieved 2026-09-04.
5. Linux kernel, [EDAC Documentation](https://docs.kernel.org/edac/index.html), current memory-controller error detection/correction reporting context; retrieved 2026-09-04.
6. Micron Technology, [DDR5 SDRAM](https://www.micron.com/products/memory/dram-components/ddr5-sdram), current device family, rate, density and technical-resource context; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), DRAM timing/controller teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace ACT/RD/WR/PRE commands for requests across two banks, enforcing supplied bank, rank and bus timing constraints cycle by cycle.

### Exercise 2

Design a timing scoreboard that converts time/cycle minima conservatively and supports same/different bank-group variants.

### Exercise 3

Specify an FR-FCFS-like scheduler with bounded age, read/write drain hysteresis, refresh deadlines and coherence ordering.

### Exercise 4

Extend the executable model with arrivals, two banks, bus reservations and refresh; report queue/service latency percentiles.

### Exercise 5

Write a verification and evaluation plan for a DRAM controller from parameter parsing through RTL/PHY integration and hardware counters.

## Answers to the Exercises

### Answer 1

Maintain active row and next-legal timestamps per bank plus rank activation windows and future bus slots. At each cycle enumerate commands whose request/order dependencies, state and every timing scope are satisfied; choose by the stated policy and update all affected scoreboards. RD/WR reserve future data beats and turnarounds.

Include closed-row, row-hit and conflict paths, simultaneous-bank opportunity, read/write direction changes and one-cycle-too-early attempts. Request completion follows data/error response, not command issue.

### Answer 2

Parse each authoritative parameter with unit/type and applicable scope. For a time minimum use `ceil(T/tCK)`; if the rule is `max(cycles,T)`, take the maximum after upward conversion. Store next-legal times for bank, bank group, rank and channel plus rolling ACT events and data-bus reservations.

Unit-test exact boundaries and just-early rejection for every command pair/mode. Recompute on frequency/mode changes only after legal quiescence and bind parameters to device bin/topology.

### Answer 3

Maintain separate or tagged read/write queues. Select only legal commands; normally favor ready hits, then age, but promote any request beyond an age bound. Enter write drain at a high watermark and leave at a low watermark or urgent-read threshold. Reserve refresh preparation early enough for its hard deadline.

Honor same-address/order-domain dependencies, atomics/fences/device rules and buffered-write forwarding. Give responses/refresh/RAS reserved progress paths. Prove no illegal issue/data loss and conditional bounded waiting under downstream/arrival assumptions.

### Answer 4

Represent request arrival, decoded bank/row, command stages and completion. Each cycle admit bounded work, update refresh deadlines, test legal PRE/ACT/RD, reserve future bursts and arbitrate. Collect queue wait, row preparation, data and total latency; compute sorted percentile indices with a documented convention.

Validate a single-bank/no-refresh case against the supplied arithmetic, then test alternating rows, independent banks, bus conflicts and refresh bursts. State all synthetic parameters and avoid calling the model a device result.

### Answer 5

Cross-check standard/device timing tables, mode registers, clocks/data rate, topology and address mapping. Verify upward unit conversion, every command-pair/scope constraint, bank state, rolling windows, bus reservations, retained writes, forwarding/merge, responses, ordering, ECC/retry, refresh deadlines, power/training and fairness with directed/random/formal checks.

Compare independent reference models, then validate RTL against a qualified memory/PHY model and boundary traces. Measure row classes, command/bus utilization, queue/latency distributions, bandwidth, refresh/turns, errors and power on workloads/hardware. Bind device stepping/bin, modules, controller/PHY RTL, firmware, temperature and errata; internal evidence is not external memory-interface or RAS certification.
