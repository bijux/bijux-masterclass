---
module_id: CA-008
program: Computer Architecture
level: 1
module_number: 8
title: Timing, Critical Paths, and Frequency
status: complete
last_verified: 2026-09-04
---

# Timing, Critical Paths, and Frequency

## One-Page Review

### Governing question

How can an architect convert a target clock frequency and interface latency into complete setup, hold, I/O and clock constraints, identify the true limiting paths, and close timing without masking invalid assumptions?

### Essential definitions

- A **timing path** connects a launch point to a capture or observation point through cells and interconnect under a declared clock relationship.
- A **startpoint** launches data; an **endpoint** captures data or defines an output requirement.
- **arrival time** is when data can reach a point; **required time** is the latest or earliest time permitted by the timing check.
- **slack** is required time minus arrival time under the tool's max/min convention; negative slack indicates a violated modeled obligation.
- A **critical path** is a path with the least slack for a specific analysis view, not necessarily the path with the most logic gates.
- A **setup check** constrains latest data arrival before capture; a **hold check** constrains earliest data change after capture.
- **clock skew** is the difference in clock arrival at launch and capture; **jitter** is event-time variation relative to a clock model.
- **clock uncertainty** reserves margin for specified jitter, skew uncertainty and modeling effects under a documented methodology.
- A **timing corner** combines process, voltage, temperature, extraction and variation assumptions.
- A **false path** is functionally impossible or intentionally untimed under a proved contract; a **multicycle path** is allowed more than the default launch-to-capture interval.
- **static timing analysis**, or STA, propagates bounds through a timing graph without enumerating input vectors.

### Central model, mechanism, or theorem

For a simplified same-clock register path with maximum clock-to-output `t_cq,max`, maximum combinational delay `t_comb,max`, setup time `t_setup` and setup uncertainty `U_setup`, require

`T_clk >= t_cq,max + t_comb,max + t_setup + U_setup`.

For minimum delay, require

`t_cq,min + t_comb,min >= t_hold + U_hold`.

Real STA incorporates actual launch/capture clock arrival, edge relationships, derates, generated clocks and common-path effects. Setup and hold are separate obligations: lengthening the period can repair some setup failures but generally does not repair a too-fast hold path.

### Critical invariants

- Every synchronous endpoint is reached by a defined clock with correct waveform, phase, uncertainty and source relationship.
- Every input and output has a timing contract relative to an external clock or an explicit asynchronous protocol.
- Maximum and minimum delays are analyzed across all required modes, corners, voltages and temperatures.
- Timing exceptions correspond to proved functional behavior and are reviewed as design claims, not optimization hints.
- CDC and reset-domain paths use correct protocols even when ordinary timing paths are excluded.
- Pipelined data, validity, tags, controls and exceptions cross identical logical stage boundaries.
- Timing fixes preserve architecture, reset, test, power and security behavior.
- Reports, constraints, netlists, parasitics, tool versions and waivers identify the exact implementation analyzed.

### Common failures

Frequent failures are dividing one by a nominal gate delay to claim frequency, calling the longest source-code expression critical, analyzing setup but not hold, double-counting or omitting skew, using typical rather than sign-off corners, ignoring interconnect and fanout, leaving clocks unconstrained, declaring unrelated clocks false without a CDC protocol, applying multicycle setup without the matching hold intent, fixing hold by lowering frequency, overconstraining paths until tools optimize the wrong objective, relying on pre-layout estimates after routing, and reporting worst negative slack without checking unconstrained endpoints or path coverage.

### Compact example

A register path has `t_cq,max=70 ps`, `t_comb,max=530 ps`, `t_setup=80 ps` and `U_setup=50 ps`. The simplified minimum period is 730 ps, or about 1.370 GHz. Its minimum delays are `t_cq,min=25 ps` and `t_comb,min=20 ps`, while hold plus uncertainty is `35+20=55 ps`; hold slack is `45-55=-10 ps`. The path can meet the calculated setup target yet fail hold. Reducing clock frequency does not add minimum path delay.

### Connections

Timing analysis connects combinational logic, registers and clocks, arithmetic structures, pipelines, clock-domain crossings, physical design, voltage/temperature, power, test modes, architecture performance and sign-off governance.

## Governing Question

A synchronous design behaves like a discrete recurrence only when physical data reaches each endpoint inside its valid sampling window. Logic gates, wires and clocks all take time. Their delays vary across manufacturing, voltage, temperature and local conditions.

The governing question is how to turn the abstraction into a complete timing contract. A frequency target alone is incomplete: inputs, outputs, generated clocks, minimum delays, asynchronous interfaces, reset, test and low-power modes all need constraints.

## Why This Matters

Timing failure can produce incorrect state without any Boolean design error. A late arithmetic result violates setup; a very short path can violate hold; a runt clock pulse can update only part of a bank. Failures may appear only on one process corner or during a voltage droop.

Frequency is also an architectural resource. Pipelining can raise throughput while adding latency and hazard state. Retiming can move registers without changing steady-state function but can change reset, debug or interface observability.

STA gives scalable conditional evidence. It does not prove the clocks and exceptions were specified correctly, and it does not model every analog or dynamic effect. Constraint review and silicon validation remain essential.

## Prerequisites and Retrieval

Before studying this module, be able to:

- distinguish combinational and sequential logic;
- explain clock-to-output, setup, hold, skew and jitter;
- read register-transfer and pipeline diagrams;
- distinguish latency, throughput and frequency;
- reason about worst-case bounds and assumptions.

Retrieve clock sources, periods, waveforms, phase relationships, jitter and uncertainty; generated and gated clocks; launch/capture endpoints; I/O board delays; asynchronous interfaces; reset/test/power modes; false, multicycle, max/min-delay and case constraints; target frequency and latency; library cells and timing arcs; PVT corners; voltage domains; on-chip variation model; extraction corner; floorplan and placement; routed parasitics; clock-tree data; signal integrity; path groups; unconstrained endpoints; exceptions and waivers; synthesis and route reports; ECO history; silicon measurements; and exact netlist, constraints, library, parasitic and tool identities.

## Learning Objectives

After completing this module, you should be able to:

1. construct a timing path from launch clock through capture requirement;
2. calculate simplified setup and hold slack;
3. distinguish logic depth from path delay and critical slack;
4. define clock, generated-clock and I/O constraints;
5. review false and multicycle paths safely;
6. explain PVT, on-chip variation and clock uncertainty;
7. diagnose cell, wire, fanout, slew and congestion delay;
8. choose restructuring, buffering, pipelining or retiming fixes;
9. separate STA claims from dynamic simulation and silicon evidence;
10. build reproducible multi-mode, multi-corner timing sign-off.

## Core Exposition

### Model timing as a graph

STA represents pins or events as nodes and timing arcs as directed edges. Cell arcs model library behavior; net arcs model interconnect. Clocks define launch and capture events.

Analysis propagates earliest and latest arrivals without enumerating functional data. The graph and constraints determine which paths exist and which checks apply.

### Identify startpoints and endpoints

Register clock pins launch data through clock-to-output arcs. Primary inputs can launch under input-delay constraints. Capture endpoints include register data pins and primary outputs.

Memory macros, latches, generated clocks and asynchronous controls add specialized arcs. Unconstrained endpoints are missing claims, not free paths.

### Compute arrival time

Latest arrival accumulates launch-clock arrival, maximum clock-to-output, cell delays and net delays along a path. Earliest arrival uses minimum values and appropriate early clock assumptions.

Reconvergent paths and multiple arcs produce several candidates. STA retains the limiting bound for each relevant transition and analysis view.

### Compute required time

For setup, required time derives from the intended capture edge minus setup and uncertainty. For hold, it derives from the relevant capture edge plus hold and minimum-delay margin.

Generated phase, multicycle definitions and I/O requirements alter the edge pair. Never infer required time from frequency alone.

### Interpret slack

Slack measures margin within the model. Positive slack means the analyzed bound meets the constraint; zero sits at the modeled boundary; negative slack violates it.

Slack is not probability of failure. A path with 5 ps positive slack may have insufficient guardband if the model omits variation; a path with negative slack must be fixed or its constraint corrected with evidence.

### Define the critical path precisely

The critical path is the least-slack path in a named path group, mode, corner and check. The design has many critical paths across setup, hold, recovery, removal, pulse width and I/O.

“The critical path” without analysis view is ambiguous. A hold-critical path can be the shortest data path.

### Relate period and frequency

Frequency is `1/T`. Convert units carefully: 1000 ps is 1 ns and corresponds to 1 GHz. Clock waveform and duty cycle can impose half-cycle or pulse-width constraints.

Maximum frequency inferred from one path is conditional on every other path, clock, mode and corner meeting its obligation.

### Distinguish latency and throughput

Adding a pipeline register can shorten stage delay and raise clock frequency, but it increases cycle latency. Once full, the pipeline can still accept or complete one item per cycle.

Compare time latency, cycle latency and initiation interval. Higher frequency does not guarantee faster application completion if stalls and control overhead grow.

### Analyze setup

Setup checks latest data arrival before a future capture event. Slow cells, long wires, high fanout, adverse voltage/temperature and late launch clocks can reduce margin.

Fixes include logic restructuring, faster cells, buffering, placement, replication, pipelining, retiming or relaxing a genuinely overstrict architectural requirement.

### Analyze hold

Hold checks that new data does not reach an endpoint too soon after the capture event. Fast cells, short wires, clock skew and aggressive useful-skew choices can cause violations.

Insert delay, adjust routing or clock balance under the physical methodology. Period length generally does not change the same-edge minimum-delay relationship.

### Include clock arrival

Launch and capture clocks travel through different physical branches. Capture later than launch can help setup while hurting hold under a common convention; the inverse can do the opposite.

STA models early and late clock paths per analysis type. Do not add a scalar skew margin on top of propagated clocks without understanding the methodology.

### Model jitter and uncertainty

Source period jitter, PLL phase jitter and clock distribution variation reduce safe edge separation. Uncertainty can reserve for these and selected unmodeled effects.

Use evidence-based components. Excessive uncertainty wastes area and power; missing uncertainty creates optimistic closure. Document whether skew is propagated or included.

### Define primary clocks

A primary clock constraint defines period, waveform and source object. Virtual clocks can express external interface timing without driving internal pins.

Verify clocks actually reach all intended sequential endpoints. A misspelled port that matches nothing can leave a whole domain untimed.

### Define generated clocks

PLL outputs, dividers, muxes and gates derive edges from sources. Generated-clock constraints state division, multiplication, phase, waveform and source path.

Incorrect source selection can analyze the right period with the wrong phase. Inspect reported clock trees and relationships.

### Constrain input timing

Input delay represents external launch clock-to-output, board delay and uncertainty relative to a reference clock. Maximum and minimum input delays support setup and hold checks.

Setting both to zero claims an ideal external source at the package boundary. Use the board and neighbor-device budget instead.

### Constrain output timing

Output delay represents time reserved for board and receiving-device setup/hold relative to its clock. It turns an internal arrival into an interface obligation.

Include clock relationship and flight-time variation. A fast internal path can still violate external hold.

### Handle asynchronous interfaces

For unrelated clocks, ordinary setup/hold closure across arbitrary phase cannot create a safe logical transfer. Use synchronizers, handshakes or asynchronous FIFOs.

Exclude only the specific cross-domain timing after the protocol exists, then time synchronizer settling, bus skew or pointer constraints separately.

### Review false paths

A false path can never be sensitized under permitted operation or is intentionally covered by a different asynchronous contract. Declaring it removes checks and optimization pressure.

Prove the condition structurally or formally, scope the exception narrowly and test configuration modes. A broad wildcard can hide real paths added later.

### Review multicycle paths

A multicycle setup exception allows a later capture edge because destination logic will not sample earlier. The source data and enable protocol must enforce that assumption.

Hold behavior must be set deliberately because changing the setup edge can also change the tool's default hold edge. Review both reports and functional enables.

### Use max/min delay constraints carefully

Explicit maximum delay can bound an asynchronous handshake or datapath independently of a clock. Minimum delay can enforce skew or settling conditions.

Such constraints do not define data coherency by themselves. State start/end points and why the bound implements a protocol requirement.

### Avoid unconstrained paths

Reports should enumerate unconstrained startpoints, endpoints, clocks and loops. Zero violations with many unconstrained registers is not closure.

Set a policy that unexpected unconstrained sequential endpoints fail sign-off. Review intentional asynchronous and constant paths individually.

### Understand timing libraries

Liberty-like cell models tabulate delay and output slew as functions of input slew, load and conditions. Sequential cells include setup, hold, recovery, removal and pulse-width arcs.

The library is characterized for specified voltage, process and temperature. Using the wrong library invalidates numbers even if the netlist is correct.

### Account for slew and load

Slow input slew changes cell delay and short-circuit current. Large capacitive load slows output and may violate transition limits.

Buffer trees, gate sizing and replication manage fanout. Oversizing can increase upstream load and congestion, moving the problem.

### Account for interconnect

At advanced scales, wire resistance, capacitance and coupling can dominate gate delay. Placement and routing determine length, layers and neighbors.

Pre-layout wire estimates guide architecture but cannot replace extracted post-route analysis. Congestion can force detours that change the critical set.

### Model process, voltage and temperature

Slow process, low voltage and high temperature often challenge setup, but relationships are technology-dependent. Fast conditions often challenge hold.

Voltage droop and temperature vary spatially and dynamically. Sign-off corners approximate required envelopes; silicon monitoring and guardband address remaining behavior.

### Model on-chip variation

Launch clock, capture clock and data paths can see different local variation. OCV derates or statistical models avoid assuming every element varies identically.

Advanced methods use stage or path depth, spatial correlation and common-path pessimism removal. Understand what correlation the tool assumes.

### Analyze multiple modes and corners

Functional, scan, at-speed test, low-power, reset and boot modes activate different clocks and case values. Each relevant mode combines with required corners.

Multi-mode, multi-corner analysis shares data while keeping views distinct. A path fixed in one corner may regress another.

### Consider voltage domains and power state

Level shifters, isolation cells, retention and power sequencing add arcs. A powered-down source needs isolation before its output becomes unknown.

Dynamic voltage/frequency scaling requires legal voltage-frequency pairs and transition policy. Timing at nominal voltage does not cover undervolted operation.

### Diagnose path composition

Break delay into launch clock, clock-to-output, logic, nets, endpoint and uncertainty. Count logic levels, but also inspect one dominant wire, high fanout, poor slew, congestion and clock path.

Compare several near-critical paths. Fixing one path may expose a family sharing the same structure.

### Restructure logic

Boolean factoring, parallel carry, balanced trees and precomputation can reduce depth. Duplicating logic can localize fanout and shorten nets.

Verify functional equivalence and glitch/power consequences. An algebraically smaller network can time worse physically.

### Insert pipeline stages

Partition combinational work across registers so each stage fits the period. Choose cuts that balance logic and routing rather than equal gate counts.

Update latency, valid/control flow, hazards, exception timing and interfaces. A timing fix that changes architectural sequencing silently is a functional bug.

### Use retiming with constraints

Retiming moves registers across combinational logic while preserving a defined sequential relation. It can balance stages automatically.

Reset values, enables, test visibility, CDC boundaries and external latency can restrict legal moves. Verify equivalence under the actual initialization contract.

### Apply useful skew cautiously

Clock-tree design can intentionally shift capture arrival to borrow margin between paths. This does not create time globally; it redistributes it and can hurt hold or adjacent stages.

Use automated multi-corner optimization and review resulting sensitivity. Avoid relying on fragile skew that disappears under variation.

### Fix hold without breaking setup

Delay cells, buffers and routing detours can increase minimum delay. They also add maximum delay and power.

Perform hold fixing across modes and corners after a representative clock tree, then recheck setup and signal integrity. Broad manual delay insertion ages poorly.

### Avoid overconstraint

Unrealistically short periods or excessive uncertainty can force large cells, buffers and congestion, worsening real critical paths and power.

Use separate exploratory targets from sign-off requirements. Record the architectural need and guardband rationale.

### Avoid underconstraint

Missing input minimums, generated clocks, test modes or low-voltage corners can leave hardware vulnerable despite green reports.

Constraint lint, coverage reports, independent review and known-path spot checks help find omissions.

### Compare STA and simulation

Gate-level timing simulation applies selected vectors and delay models; it can reveal reset or dynamic interactions. STA analyzes path bounds without vector enumeration and scales to coverage.

Neither validates incorrect exceptions or analog phenomena automatically. Use each for its strongest claims.

### Correlate with silicon

Ring oscillators, critical-path monitors, scan tests and workload frequency sweeps provide silicon distributions. On-chip sensors add voltage and temperature context.

Measurement includes sample and instrument limits. Correlate failing chips with sign-off views without tuning away unexplained outliers.

### Govern timing closure

Freeze netlist, constraints, libraries, parasitics, modes, corners and tool version for a sign-off receipt. Record worst slack, total negative slack, violation counts and coverage.

Every exception and waiver names owner, rationale, evidence and expiry. ECOs trigger affected functional, timing, power and physical revalidation.

## Definitions and Notation

- `T_clk`: period between relevant launch and capture edges.
- `f_clk = 1/T_clk`: clock frequency.
- `t_cq,max`, `t_cq,min`: latest and earliest clock-to-output delays.
- `t_comb,max`, `t_comb,min`: maximum and minimum data-path delays.
- `t_setup`, `t_hold`: endpoint setup and hold requirements.
- `U_setup`, `U_hold`: uncertainty terms under a declared methodology.
- `A_max`, `A_min`: latest and earliest data arrival.
- `R_setup`, `R_hold`: setup and hold required times.
- **setup slack:** margin between latest arrival and latest permitted capture.
- **hold slack:** margin between earliest permitted change and earliest arrival under tool convention.
- **path group:** related set of timing paths reported or optimized together.
- **analysis view:** one mode/corner/check combination.
- **WNS:** worst negative slack in a view or group.
- **TNS:** sum of negative slacks over reported endpoints under tool rules.
- **timing exception:** constraint modifying default graph or edge analysis.

## Mechanisms, Invariants, or Proof Structure

1. **Architecture claim:** define frequency, cycle latency, throughput and I/O budgets.
2. **Clock invariant:** create every source/generated clock with correct edges and uncertainty.
3. **Coverage invariant:** constrain every sequential endpoint and external interface.
4. **Setup invariant:** latest data meets every required capture edge.
5. **Hold invariant:** earliest new data does not corrupt the captured value.
6. **Crossing invariant:** asynchronous transfers use a proved protocol plus appropriate timing bounds.
7. **Exception invariant:** false and multicycle paths correspond to verified functional conditions.
8. **Corner invariant:** cover process, voltage, temperature, extraction, variation and mode requirements.
9. **Physical invariant:** include actual slew, load, fanout, routing, coupling and clock tree.
10. **Pipeline invariant:** timing transformations preserve data/control/tag/reset relationships.
11. **ECO invariant:** fixes do not regress other views, function, power, test or reliability.
12. **Report invariant:** review coverage, violations, near-critical families and assumptions.
13. **Evidence invariant:** bind results to exact netlist, constraints, libraries and parasitics.
14. **Correlation claim:** compare analysis with silicon while preserving measurement uncertainty.
15. **Change invariant:** re-run affected views after any design, constraint or environment change.

## Alternatives and Trade-Offs

- **Lower frequency versus redesign:** lower frequency adds setup margin; redesign preserves performance and costs engineering.
- **Gate sizing versus buffering:** sizing strengthens a driver; buffering partitions load and adds stages and power.
- **Logic duplication versus shared logic:** duplication localizes fanout; sharing saves area and can lengthen wires.
- **Restructuring versus pipelining:** restructuring preserves cycle latency; pipelining raises throughput and adds state.
- **Manual pipeline versus retiming:** manual cuts preserve intent visibly; retiming explores placements and complicates reset/debug constraints.
- **Balanced logic versus physical locality:** balanced depth reduces logical delay; locality may dominate wire delay.
- **Useful skew versus balanced clocks:** useful skew redistributes margin; balance is more uniform and can be robust.
- **Delay cell versus route detour:** cells are characterized; detours consume routing and can vary.
- **Broad uncertainty versus detailed variation model:** broad margin is simple and pessimistic; detailed models need characterization.
- **False path versus timed synchronizer:** false paths remove checks; synchronizer paths still need settling and placement analysis.
- **Multicycle versus clock enable pipeline:** multicycle reuses logic; explicit stages make timing and data ownership visible.
- **Pre-layout versus post-route analysis:** early estimates guide architecture; extraction supports implementation sign-off.
- **STA versus timing simulation:** STA covers graph bounds; simulation exercises selected dynamic scenarios.
- **Worst-case corners versus statistical timing:** corners are auditable; statistical methods model distributions and need data.
- **Aggressive target versus realistic constraint:** stretch goals explore design space; sign-off constraints express actual obligations.

## Failure Modes and Misconceptions

1. **“Gate count determines the critical path.”** wires, slew, load, clocks and constraints matter.
2. **“The longest path is unique.”** each mode, corner and check has a critical set.
3. **“Positive slack proves the chip.”** it proves a conditional timing model.
4. **“Frequency is one divided by combinational delay.”** clock-to-Q, setup, clocks and uncertainty remain.
5. **“Setup and hold use the same corner.”** required worst views can differ.
6. **“Lowering frequency fixes hold.”** same-edge minimum delay is generally unchanged.
7. **“Capture skew always helps.”** help for setup can harm hold and adjacent paths.
8. **“Uncertainty should include everything twice.”** double-counted pessimism distorts closure.
9. **“A generated clock needs only its period.”** phase and source relationship matter.
10. **“Input delay zero is conservative.”** it can be optimistic for setup or wrong for hold.
11. **“Output delay is board propagation only.”** receiver setup/hold and clock relation belong.
12. **“False path means safe CDC.”** it only removes ordinary checks.
13. **“Multicycle setup automatically fixes hold intent.”** hold edges need explicit review.
14. **“No violations means every path is timed.”** unconstrained endpoints can disappear from results.
15. **“Typical libraries are good enough.”** sign-off covers required extremes and variation.
16. **“Cell delay dominates modern paths.”** interconnect often dominates.
17. **“Upsizing always speeds a path.”** upstream load and congestion can worsen.
18. **“More buffers always fix fanout.”** placement, load and power determine benefit.
19. **“Pipelining only changes timing.”** latency, control and architectural behavior change.
20. **“Retiming preserves every reset behavior.”** initial-state semantics can restrict it.
21. **“Hold fixing cannot hurt setup.”** added delay affects maximum paths too.
22. **“Overconstraint is harmless margin.”** it can increase congestion, area and power.
23. **“Pre-layout closure survives routing.”** extracted wires can reorder critical paths.
24. **“TNS measures application performance.”** it aggregates modeled violations, not workload time.
25. **“Timing simulation replaces STA.”** vectors cannot cover every structural path efficiently.
26. **“One silicon sample validates all corners.”** process and environment distributions remain.

## Worked Examples

### Example 1

A path with six small gates is slower than one with eight because its long high-capacitance net dominates. Logic levels alone misidentify the bottleneck.

### Example 2

A 730 ps setup requirement permits about 1.370 GHz in the simplified model, while the same path has -10 ps hold slack.

### Example 3

A primary clock is constrained on the wrong port. Reports look clean because thousands of registers are unconstrained; coverage review catches it.

### Example 4

An input delay is set to zero although an external device launches 400 ps late. Internal setup slack is overstated by that omitted budget.

### Example 5

A broad false-path wildcard removes a new functional crossing. Narrow endpoint scoping and CDC inventory prevent the silent escape.

### Example 6

A two-cycle datapath receives a setup multicycle constraint but no reviewed hold relation. The tool shifts edges differently than the designer intended.

### Example 7

Upsizing a cell speeds its output but overloads the preceding gate. Buffering and placement provide better total path delay.

### Example 8

A pipeline cut balances gate counts but leaves one stage with a long cross-chip wire. Physical-aware partitioning moves the register near the producer.

### Example 9

Useful skew repairs one setup endpoint and creates a hold failure in a neighboring path. Multi-corner clock optimization must consider both.

### Example 10

Silicon fails only during low-voltage thermal load. Correlation reveals the sign-off set omitted the required low-voltage hot corner.

## Cross-Program Connections

- **Digital logic:** cell structure and Boolean depth establish candidate data paths.
- **Registers and clocking:** sampling windows, skew and jitter make synchronous state possible.
- **Arithmetic:** carry, multiply and normalization networks commonly create critical paths.
- **Pipelining:** stage boundaries trade frequency, latency, throughput and control complexity.
- **Physical design:** placement, routing, coupling and clock trees determine real delay.
- **Power engineering:** sizing, buffering, voltage and frequency affect energy and thermal state.
- **Verification:** functional equivalence and timing constraints support different claims.
- **Operating systems:** frequency and timing margins influence performance and real-time behavior.
- **Reliability:** variation, aging, droop and faults can consume timing margin.
- **Systems engineering:** sign-off views and waivers trace implementation evidence to requirements.

## References

1. AMD, [Vivado Design Suite User Guide: Design Analysis and Closure Techniques](https://docs.amd.com/r/en-US/ug906-vivado-design-analysis), timing reports, path analysis, constraints and closure; retrieved 2026-09-04.
2. AMD, [UltraFast Design Methodology: Timing Closure](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology/Timing-Closure), clocks, constraints, implementation and timing-closure methodology; retrieved 2026-09-04.
3. Intel, [Timing Analyzer](https://www.intel.com/content/www/us/en/docs/programmable/683243/24-1/timing-analyzer.html), STA workflow, timing netlists, reports and constraints; retrieved 2026-09-04.
4. Intel, [Timing Analysis Basic Concepts](https://www.intel.com/content/www/us/en/docs/programmable/683243/24-1/timing-analysis-basic-concepts.html), arrival, required time, slack, setup, hold and clock relationships; retrieved 2026-09-04.
5. OpenROAD Project, [OpenSTA](https://github.com/The-OpenROAD-Project/OpenSTA), open static timing engine, timing graph, delay calculation and SDC support; retrieved 2026-09-04.
6. IEEE, [IEEE 1800-2023 — SystemVerilog](https://standards.ieee.org/ieee/1800/7743/), timing controls, specify behavior, assertions and RTL semantics; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), propagation delay, sequential timing, critical paths and pipelining; retrieved 2026-09-04.
8. Neil H. E. Weste and David Money Harris, [CMOS VLSI Design: A Circuits and Systems Perspective](https://www.pearson.com/en-us/subject-catalog/p/cmos-vlsi-design-a-circuits-and-systems-perspective/P200000003427/9780321547743), cell, interconnect, clock, variation and physical timing; retrieved 2026-09-04.

## Exercises

### Exercise 1

For `t_cq,max=70 ps`, `t_comb,max=530 ps`, `t_setup=80 ps`, `U_setup=50 ps`, compute minimum period and frequency. With minimum delays 25 ps and 20 ps, hold 35 ps and uncertainty 20 ps, compute hold slack.

### Exercise 2

Build complete clock and I/O constraints for a synchronous peripheral connected over a board. State external launch/capture budgets, generated clocks, uncertainty and validation.

### Exercise 3

Review a proposed two-cycle multicycle exception. Define functional enable, setup/hold edges, reset, CDC, test-mode and proof obligations.

### Exercise 4

Diagnose a routed critical path whose delay is 20% cells, 65% interconnect and 15% clock/uncertainty. Compare four fixes and regression checks.

### Exercise 5

Construct timing assurance for a medical controller across process, voltage, temperature, aging, clock and power faults, including evidence and named review.

## Answers to the Exercises

### Answer 1

The simplified setup sum is `70+530+80+50=730 ps`, so frequency is `1/(730 ps)`, approximately `1.370 GHz`. Earliest data arrival is `25+20=45 ps`; hold requirement plus uncertainty is `35+20=55 ps`, so hold slack is `45-55=-10 ps`.

<!-- bijux-verify: {"id":"setup-hold-frequency","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"minimum_period_ps=730\nmaximum_frequency_ghz=1.370\nhold_arrival_ps=45\nhold_required_ps=55\nhold_slack_ps=-10\nsetup_status=pass_at_or_below_limit\nhold_status=fail\n"}} -->
```python
t_cq_max = 70
t_comb_max = 530
t_setup = 80
u_setup = 50
minimum_period_ps = t_cq_max + t_comb_max + t_setup + u_setup
frequency_ghz = 1000 / minimum_period_ps

hold_arrival = 25 + 20
hold_required = 35 + 20
hold_slack = hold_arrival - hold_required

print(f"minimum_period_ps={minimum_period_ps}")
print(f"maximum_frequency_ghz={frequency_ghz:.3f}")
print(f"hold_arrival_ps={hold_arrival}")
print(f"hold_required_ps={hold_required}")
print(f"hold_slack_ps={hold_slack}")
print("setup_status=pass_at_or_below_limit")
print(f"hold_status={'pass' if hold_slack >= 0 else 'fail'}")
```

The toy uses lumped same-clock delays and uncertainties. It omits propagated clock paths, edge phase, slew/load tables, derates, variation, common-path effects and physical extraction.

### Answer 2

Define a primary or virtual interface clock with period and waveform. For each input, use maximum delay from external launch clock-to-output plus board maximum and uncertainty, and minimum delay from the corresponding early values. For outputs, reserve board delay plus receiver setup for maximum and express receiver hold with the correct minimum convention. Include package and clock-board skew consistently.

Declare internal PLL/divider outputs as generated clocks with source, phase and ratio. Constrain reset and asynchronous status under their protocols, not synchronous fiction. Validate constraint object matches, clock reachability, unconstrained endpoints, setup/hold reports and interface timing against both device data sheets and board analysis. Test phase corners and measure representative hardware while preserving model limits.

### Answer 3

The destination must sample only on the second eligible capture edge, enforced by an enable or protocol stable against every permitted mode. Source data must remain unchanged through that edge. Define which launch starts the interval and whether back-to-back operations are legal.

Apply the setup multicycle narrowly, then state the intended hold edge explicitly and inspect both reports. Check reset can neither open the early capture nor leave stale data, and that clocks are actually synchronous; otherwise use CDC. Analyze scan/test and low-power modes separately because enables and clock relationships can differ. Prove the sampling invariant with assertions/formal analysis, exercise stalls and simultaneous controls, and bind the exception to exact endpoints with a reviewed owner.

### Answer 4

First inspect whether one long net, high fanout, congestion or poor placement causes the 65%. Move producer/consumer closer or guide placement; buffer the net; replicate the source logic to local sinks; or insert a pipeline register if architecture permits. Gate sizing alone targets only 20% and may increase upstream load.

For every candidate, re-run all setup and hold views, clock effects, transition/capacitance, congestion, crosstalk, area and power. Verify functional equivalence, reset, test, CDC and pipeline data/control alignment. Compare several near-critical paths so the fix does not merely move the bottleneck. Use extracted post-route data rather than the old composition estimate.

### Answer 5

Trace response deadlines into clock frequency, stage latency and I/O budgets with margin. Analyze setup, hold, recovery/removal and pulse width across required process, supply, temperature, extraction and variation views, including startup, low battery, thermal equilibrium and aging. Model oscillator tolerance, jitter, PLL lock/loss, clock switching, droop, brownout, reset sequencing and stopped clocks.

Use independent constraint review, coverage lint, STA, functional/formal pipeline verification, post-layout extraction, power-integrity analysis, fault injection and environmental hardware tests. Provide a safe state when timing or clock monitors detect invalid operation and ensure common-cause failure cannot defeat detection and control. Preserve netlists, constraints, libraries, parasitics, tools, waivers, lots and raw results. Named architecture, RTL, clock, physical, power-integrity, medical-domain, safety, cybersecurity, verification, manufacturing, quality, regulatory and independent-assurance authorities review their scopes. This module supplies no certification.
