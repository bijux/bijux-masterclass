---
module_id: OS-098
program: Operating Systems
level: 2
module_number: 98
title: Energy-Aware Operating Systems
status: complete
last_verified: 2026-09-04
---

# Energy-Aware Operating Systems

## One-Page Review

### Governing question

How should an operating system observe demand and platform state, choose placement, frequency, idle, device and sleep actions, and enforce thermal and power constraints while preserving latency, throughput, fairness, correctness and recoverability?

### Essential definitions

- **Power** is the rate of energy use, measured in watts; **energy** is accumulated work-related consumption, measured in joules.
- **Dynamic power** is activity-dependent switching power; **static or leakage power** persists with powered circuitry and varies with voltage and temperature.
- A CPU **performance state** changes delivered capacity and power through hardware- or software-coordinated voltage and frequency control.
- A CPU **idle state** saves power while no task executes and has entry, target-residency and exit-latency properties.
- A **performance domain** is a group of CPUs whose performance choice is coordinated because they share hardware controls.
- An **energy model** estimates cost at supported performance states for scheduler or platform decisions.
- **race to idle** runs work quickly to reach a low-power state; it saves energy only when the platform, workload and idle interval make that path cheaper.
- **energy proportionality** describes how closely system power falls with useful load.
- A **thermal zone** represents temperature observation and policy; a **cooling device** exposes actions that reduce heat generation or increase cooling.
- **power capping** constrains energy or average power over a window, often allowing hardware to select lower-level actions.
- **runtime power management** suspends an idle device while the rest of the system continues; system sleep coordinates a broader platform transition.

### Central model, mechanism, or theorem

Energy-aware control is a constrained feedback loop:

`observe workload + deadlines + topology + temperature + power + residency -> estimate feasible costs -> choose placement/state/batching -> enforce -> measure service and energy -> update or fall back`.

For a predicted idle interval `t`, a deeper state with extra transition energy `E_tr`, power `P_deep`, and exit latency `L_exit` is attractive relative to a shallow state using `P_shallow` only when `t >= E_tr/(P_shallow-P_deep)` and `L_exit` fits the wakeup-latency budget. This break-even model is conditional: entry time, state coupling, prediction error, leakage, temperature and hardware-specific behavior can change the result.

### Critical invariants

- Optimization has a declared objective and hard service, safety, thermal and battery constraints.
- Energy comparisons measure completed correct work over equivalent workload and time boundaries.
- Scheduler capacity, frequency, idle and thermal models identify the exact hardware, firmware and topology generation.
- Control actions respect performance-domain, clock-domain, package, device-dependency and wakeup constraints.
- Required deadlines and recovery paths retain enough capacity during caps, low-battery modes and thermal emergencies.
- Feedback loops use stable sampling, hysteresis, rate limits and conservative fallback when sensors or models fail.
- Device and system suspend preserve state, dependency order, wakeup sources and rollback across every error path.

### Common failures

Frequent failures are optimizing instantaneous power instead of energy per correct completion, comparing unequal work, trusting nominal frequency as delivered capacity, assuming race-to-idle is universal, using utilization without accounting for heterogeneous capacity, selecting deep idle from predicted duration while ignoring exit latency, oscillating frequency and placement controllers, spreading work so no package sleeps, packing work until thermal throttling defeats it, treating an energy model as a calibrated meter, ignoring devices and memory, suspending a supplier before consumers, accepting wakeup storms, confusing runtime suspend with system sleep, hiding throttling in global averages, and disabling recovery capacity during a power or thermal emergency.

### Compact example

A core is predicted to be idle for 10 milliseconds. Remaining shallow consumes 4 watts. A deeper state consumes 0.5 watts, adds 10 millijoules of transition energy and exits in 2 milliseconds. The simple break-even interval is `10 mJ / 3.5 W = 2.857 ms`; the deep-state estimate is `10 mJ + 0.5 W * 10 ms = 15 mJ`, versus `40 mJ` shallow. If the workload allows 3 milliseconds of wakeup latency, the state is eligible in this toy model. If the latency budget is 1 millisecond or the predicted gap is shorter than break-even, it is not.

### Connections

Energy-aware operating systems connect scheduling, heterogeneous architecture, feedback control, timers, memory and device lifecycle, real-time guarantees, thermal engineering, batteries, virtualization, observability, sustainability accounting and fleet policy.

## Governing Question

The operating system sits where application intent meets hardware controls. It knows which work is runnable, which deadlines matter, which CPUs share capacity controls, which devices are active, and when the next timer may fire. Hardware knows electrical and thermal details that software models only approximately.

The governing question is how to combine these partial views without violating service. The system must decide when to run, where to run, how much capacity to request, which components may sleep, and how to respond when heat, battery, power supply or workload invalidate the forecast.

## Why This Matters

Energy affects battery life, cooling, density, cost, noise, reliability and environmental impact. Reducing power can extend a mobile session or keep a rack within its electrical budget. Reducing energy per useful result can increase total fleet capacity without new hardware.

But energy actions change time. Lower frequency lengthens execution and can keep memory or devices active longer. Deep idle saves more power but delays wakeup. Packing tasks may free an entire package to sleep or may create thermal concentration and tail latency. A cap can contain facility demand while making a deadline infeasible.

The goal is therefore constrained optimization, not minimum watts. Correct output, latency, throughput, fairness, availability and safe recovery remain part of the objective. The OS must make conflicts visible and preserve evidence about which controller caused a service change.

## Prerequisites and Retrieval

Before studying this module, be able to:

- distinguish power, energy, performance, utilization and capacity;
- explain scheduler placement, CPU affinity, timers and idle execution;
- reason about device dependencies, suspend and resume;
- interpret feedback-loop sampling, delay, hysteresis and saturation;
- design controlled performance experiments with equivalent work.

Retrieve platform topology; CPU capacity and performance domains; supported performance and idle states; energy-model generation; frequency driver and governor; scheduler utilization clamps and boosts; idle driver and governor; timer and wakeup sources; package and uncore behavior; memory and device power states; runtime-PM dependencies and autosuspend; system sleep modes; thermal zones, trip points and cooling bindings; power-cap zones and windows; battery state and limits; firmware and microcode; virtual-machine exposure; workload arrivals, deadlines and throughput; QoS constraints; counters and sensor calibration; temperatures; throttling reasons; ambient and cooling state; controller configuration; baseline and experiment boundaries; errors; and rollback behavior.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish power reduction from energy-efficiency improvement;
2. define constrained energy objectives with comparable work boundaries;
3. explain CPU frequency, idle, scheduler and thermal control interactions;
4. apply a conditional idle-state break-even calculation;
5. reason about heterogeneous placement and performance domains;
6. design stable policies for batching, consolidation and race-to-idle;
7. manage device runtime power and system sleep dependencies safely;
8. diagnose energy, thermal and service regressions with causal evidence;
9. handle caps, sensor faults, low battery and thermal emergencies;
10. govern energy policy across exact platform and workload generations.

## Core Exposition

### Define the objective before tuning

Choose an objective such as joules per completed request, battery life for a representative session, energy-delay product, facility power under a throughput floor, or thermal headroom under a deadline constraint. State which constraints are hard.

No scalar is universally sufficient. Energy-delay product weights time once; energy-delay-squared weights it more. Carbon or price optimization adds time and location signals but cannot silently move work across deadlines, data boundaries or availability requirements.

### Measure equivalent useful work

An energy reduction caused by completing fewer requests is not efficiency. Compare equal offered and admitted load, correctness, quality, completion count and observation interval. Account for queued work left after measurement.

Warm-up, cache state, battery charge, ambient temperature and thermal history affect results. Run through representative steady state and report both total energy and service distributions.

### Understand the power stack

CPU cores, shared caches, interconnect, memory, storage, network, accelerators, display, radios, fans and power conversion all contribute. Optimizing core power alone can increase total-system energy if work takes longer or shifts activity to another component.

Some domains are independently controllable; others share voltage rails, clocks or package states. Discover coupling from platform interfaces and experiments rather than assuming each logical CPU is autonomous.

### Treat capacity as state-dependent

Delivered capacity depends on microarchitecture, frequency, simultaneous multithreading, cache and memory behavior, power limits, temperature and interference. A nominal frequency value is not a universal work rate.

Scheduler utilization signals must be interpreted against capacity. Heterogeneous CPUs doing equal wall-clock runtime may complete different work and consume different energy.

### Coordinate CPU frequency selection

CPUFreq presents policy objects for CPUs sharing a control interface. A scaling governor chooses requested performance within policy limits; a driver translates requests to hardware semantics. Hardware-coordinated drivers may make rapid internal choices beyond OS visibility.

The scheduler-informed `schedutil` path derives performance requests from utilization and capacity signals. Boosts, clamps, I/O-wait behavior, rate limits and thermal pressure can modify the result. Always inspect effective rather than merely requested state.

### Avoid frequency-control oscillation

Sampling too slowly misses bursts; sampling too quickly chases noise and consumes energy. Delayed measurements, workload phase changes and multiple controllers can cause repeated up/down transitions.

Use hysteresis, asymmetric rise/fall behavior, bounded integrators and rate limits. Test step loads, bursts and alternating phases. A conservative maximum-capacity fallback may be safer than an unstable controller when deadlines matter.

### Understand idle-state selection

CPUIdle exposes states with increasing power savings and generally increasing entry/exit costs. An idle governor predicts the idle interval and selects a state whose constraints fit. The next timer is evidence, not certainty, because interrupts and remote wakeups can arrive earlier.

Target residency approximates how long a state should last to repay transition costs. Exit latency constrains service. State descriptions and firmware tables are inputs to validate, not guarantees of application-visible timing.

### Calculate break-even conditionally

Against a shallow state, a deeper state's simple energy advantage begins after transition cost is recovered by its lower power. The ratio `E_tr/(P_shallow-P_deep)` expresses that threshold when powers are constant and `P_shallow>P_deep`.

Reject the state when predicted idle is shorter or required wakeup latency is below its exit latency. Refine the model for entry time, coupled domains, leakage, timer migration and prediction error. A favorable energy estimate never overrides a hard latency constraint.

### Control timer and wakeup density

Periodic timers prevent deep residency even when their callbacks do little. Convert polling to event-driven work, use bounded timer slack, batch maintenance and place noncritical timers on housekeeping CPUs.

Coalescing adds latency and burst demand. Classify timers by deadline and jitter tolerance. Observe actual wakeup sources because one misconfigured service can dominate an otherwise careful policy.

### Evaluate race to idle

Running at higher capacity can finish sooner and enable deep component or package states. It helps when static power is significant, performance scales well, and the resulting idle interval is long enough.

It can lose when voltage raises dynamic power sharply, the workload is memory-bound, background work prevents deep idle, turbo reduces efficiency, or concentrated heat causes throttling. Compare end-to-end energy under matched work instead of relying on the slogan.

### Place work on heterogeneous CPUs

Energy-aware scheduling estimates placement cost using CPU capacity, utilization and an energy model across performance domains. It seeks lower estimated energy while respecting capacity, affinity and scheduling-class constraints.

Placing a small task on an efficient CPU may avoid raising a high-capacity domain. Moving it can cost cache locality or wake another cluster. Energy-model cost values support relative decisions; they are not necessarily direct calibrated power readings.

### Choose packing or spreading by domain

Packing work can leave whole cores, clusters or packages idle. Spreading can reduce queueing, use lower per-core frequency and avoid thermal concentration. The best boundary depends on shared domains and workload parallelism.

Model the state transition caused by placement, not only the destination core's current utilization. Include migration, cache refill, NUMA access and the likelihood that a newly emptied domain reaches a useful sleep state.

### Incorporate thermal constraints

Thermal frameworks connect sensors, trip points, governors and cooling devices. Cooling actions can reduce CPU capacity, throttle devices or increase fan power. Firmware may impose additional controls invisible to the scheduler.

Temperature is delayed state, not instantaneous power. Prevent oscillation around trip points, preserve critical service and log the requested and effective cooling action. Test at supported ambient and sustained load until thermal equilibrium.

### Use power caps deliberately

Power-capping frameworks expose zones, constraints and time windows where supported. A package cap can bound facility or thermal demand while hardware chooses frequency or activity responses.

A cap is not a guaranteed application allocation. Workloads within the domain compete, counters may wrap, and short windows permit bursts. Validate throughput and tail latency at the cap and reserve capacity for safety and management.

### Manage devices at runtime

Runtime power management suspends an idle device independently of system sleep. Drivers and the PM core coordinate usage counts, callbacks, autosuspend delays and dependency ordering.

Too-short autosuspend intervals cause transition thrashing. Too-long delays waste idle power. A consumer must not access a suspended supplier without a valid resume path. Handle I/O arriving during transition, cancellation, errors and device removal.

### Account for wakeup energy

A sleeping device may require clocks, regulators, links, firmware and parent buses to resume. The apparent device transition can wake an entire package. Attribute full dependency-chain energy and latency.

Wakeup storms from polling, link chatter or broken drivers can dominate. Count resumes by reason, duration and successful work, then correct the source rather than merely increasing delays everywhere.

### Distinguish runtime and system sleep

Runtime suspend leaves the system operating. System suspend coordinates tasks, devices, CPUs and platform firmware into states such as suspend-to-idle or deeper platform sleep. Hibernation writes memory state to storage and later restores it.

These modes have different latency, energy, security and failure properties. A platform-advertised state may not achieve expected savings if a wake source or device blocks entry. Verify actual residency and complete resume behavior.

### Preserve suspend and resume invariants

Freeze or quiesce work, order consumers before suppliers on suspend, reverse dependencies on resume, save required state and prevent new I/O from crossing the transition incorrectly. Every failed callback needs a coherent unwind.

Test wakeup at each boundary, repeated cycles, partial failure, device removal, low battery and power loss. A system that saves energy but occasionally loses a device or corrupts storage is incorrect.

### Include memory and storage

Memory bandwidth and residency consume energy; remote NUMA traffic activates interconnect and controllers. Compression can reduce I/O and increase CPU work. Page migration can improve locality or spend more energy than it saves.

Storage batching may enable device sleep but creates queues and writeback bursts. Respect durability deadlines and thermal behavior. Measure the whole request path, including controller caches and background garbage collection.

### Include networks and accelerators

Interrupt moderation, batching and offload change CPU and device energy together. Radio or link setup costs can make grouped transfer efficient, while added waiting violates interactive latency.

Accelerator offload is useful only after including data movement, synchronization, idle leakage and fallback. Keep device-specific admission and timeout policy because an accelerator at low utilization can be less efficient than the CPU path.

### Coordinate independent controllers

Scheduler placement, CPU frequency, idle selection, thermal control, power capping, fan control and application adaptation can all react to the same symptom. If each assumes the others are fixed, their combined loop may oscillate.

Document controller hierarchy, actuators, sample periods and ownership. Correlate decisions in one timeline. Use arbitration or separated time scales where possible and define which safety controller wins.

### Handle low battery and constrained supply

Battery state of charge, voltage, temperature, age and discharge rate affect available energy and peak power. A low-battery policy should degrade optional quality, background work and refresh frequency before essential monitoring or shutdown capacity.

Persist data and enter a safe state before the supply becomes unreliable. Test sensor disagreement, rapid voltage collapse, charger changes and battery replacement. Remaining-percentage estimates are not hard energy guarantees.

### Design safe degradation

When temperature or power crosses a protected limit, reduce optional demand, lower concurrency, cap domains or stop accelerators according to criticality. Keep telemetry, control and authenticated recovery runnable.

If constraints make required service infeasible, surface that state rather than silently violating every objective. A controlled safe shutdown may be more correct than indefinite throttled operation.

### Measure with multiple evidence sources

Use hardware energy counters, external meters, battery telemetry, frequency and idle residency, scheduler traces, thermal sensors, throttling reasons and application completions. Each has resolution, scope, delay, calibration and wraparound limits.

Cross-check counters against a meter where practical. Align clocks and boundaries. Report sampling overhead and missing data. Energy attribution to a process or tenant is a model unless hardware measures that boundary directly.

### Govern platform-specific policy

Version kernel, drivers, firmware, microcode, topology, energy model, governor, limits, workload and ambient conditions. A policy tuned for one laptop revision or server cooling zone may regress another.

Roll out through representative canaries with automatic service, thermal and energy guardrails. Keep a conservative fallback and record the controller decision that preceded every regression.

## Definitions and Notation

- `P(t)`: instantaneous or interval-estimated power at time `t`.
- `E = integral P(t) dt`: energy across a declared measurement boundary.
- `W`: useful, correct completed work over that boundary.
- `E/W`: energy per useful completion or unit of work.
- `P_shallow`, `P_deep`: modeled steady power in two idle states.
- `E_tr`: additional entry/exit energy for the deeper state relative to the shallow baseline.
- `t_be = E_tr/(P_shallow-P_deep)`: simplified deep-state energy break-even time.
- `L_exit`: modeled exit latency of a state.
- `t_pred`: predicted idle duration.
- `C_cpu`: effective CPU capacity under current architecture and constraints.
- **performance domain:** CPUs coordinated by one performance-control interface.
- **target residency:** idle duration expected to justify a state under a platform model.
- **thermal pressure:** capacity unavailable because thermal controls restrict performance.
- **residency:** time spent in a hardware or software state.
- **energy model:** ordered capacity/cost description used to compare candidate states.
- **power-cap window:** interval over which a platform constrains or reports average demand.

## Mechanisms, Invariants, or Proof Structure

1. **Objective claim:** declare energy, power, battery or thermal metric and hard service constraints.
2. **Boundary claim:** compare equal useful work, quality, initial state and completion boundary.
3. **Topology claim:** discover CPUs, performance domains, packages, memory and device dependencies.
4. **Capability claim:** identify supported frequency, idle, device, sleep, cap and cooling states.
5. **Model claim:** bind capacity and energy estimates to exact platform and firmware identities.
6. **Feasibility invariant:** reject any action that violates deadlines, safety or required recovery capacity.
7. **Selection invariant:** account for transition energy, latency, coupling, migration and prediction error.
8. **Lifecycle invariant:** suspend and resume preserve state, I/O ordering, dependencies and rollback.
9. **Feedback invariant:** bound rate, oscillation and integral windup across interacting controllers.
10. **Thermal invariant:** sustained operation remains within limits at supported ambient and cooling states.
11. **Emergency invariant:** faults and depleted supply trigger explicit degradation or safe shutdown.
12. **Measurement claim:** record power, energy, service, residency, temperature and action on aligned clocks.
13. **Attribution claim:** distinguish measured domains from modeled task or tenant allocation.
14. **Change invariant:** revalidate after kernel, firmware, driver, hardware, workload or policy change.
15. **Residual-risk claim:** disclose sensor, model, counter and unsupported-state uncertainty.

## Alternatives and Trade-Offs

- **Minimum power versus minimum energy:** low instantaneous demand can lengthen work; higher power can finish sooner.
- **Race to idle versus pace to idle:** rapid completion can enable sleep; slower execution can avoid inefficient voltage or thermal peaks.
- **Packing versus spreading:** packing frees domains; spreading reduces queueing and frequency or thermal concentration.
- **High-capacity versus efficient CPU:** a fast CPU may finish earlier; an efficient CPU may use less energy if it meets service.
- **Deep versus shallow idle:** deep states save more steady power; shallow states wake faster and avoid transition cost.
- **Short versus long autosuspend:** short delays capture idle gaps; long delays prevent transition thrash.
- **Polling versus interrupts:** polling avoids wakeup transitions under load; interrupts allow idle during sparse events.
- **Batching versus immediate service:** batches amortize wakes and setup; immediate service lowers latency.
- **Software versus hardware frequency control:** software exposes policy; hardware reacts faster with less visibility.
- **Static cap versus adaptive cap:** static limits are predictable; adaptive limits use headroom and add control complexity.
- **Active cooling versus throttling:** fans consume energy and noise; throttling reduces service capacity.
- **Runtime suspend versus always-on device:** suspend saves idle power; always-on avoids transition latency and failures.
- **Suspend-to-idle versus deep sleep:** suspend-to-idle simplifies software coordination; deeper platform states save more and depend more on firmware.
- **On-device versus external measurement:** counters offer attribution and scale; meters better capture system boundaries.
- **Local policy versus fleet policy:** local control reacts quickly; fleet coordination can move work under site constraints and data rules.

## Failure Modes and Misconceptions

1. **“Lower power means lower energy.”** longer runtime can consume more total joules.
2. **“Energy savings are valid even if throughput fell.”** compare equal useful work and service.
3. **“Frequency equals performance.”** microarchitecture, memory, caps and interference affect capacity.
4. **“Utilization is comparable across all CPUs.”** heterogeneous capacities require normalization.
5. **“Race to idle always saves energy.”** voltage, workload scaling and available idle depth determine the result.
6. **“The deepest idle state is best.”** transition cost and exit latency can dominate short gaps.
7. **“The next timer predicts the idle interval.”** interrupts and remote work can wake earlier.
8. **“Target residency is an application guarantee.”** it is a platform selection input, not an end-to-end proof.
9. **“An energy-model cost is a watt reading.”** it may be an abstract relative cost.
10. **“Packing always permits package sleep.”** devices, timers or uncore activity can keep it awake.
11. **“Spreading always lowers frequency.”** shared domains may raise together.
12. **“Thermal throttling is ordinary scheduler idle.”** it removes capacity and changes feasibility.
13. **“A power cap fairly allocates power.”** peers within the capped domain still compete.
14. **“Counters never wrap.”** narrow energy counters require modular-delta handling.
15. **“One temperature sensor describes the system.”** hotspots and delayed sensors differ.
16. **“Runtime suspend is system sleep.”** scope, ordering and wake behavior differ.
17. **“Autosuspend affects only the device.”** suppliers, buses and packages can transition too.
18. **“A suspended device cannot receive work.”** the resume protocol must handle arriving I/O.
19. **“A failed suspend is harmless.”** partial transitions require correct rollback.
20. **“Wakeup-enabled means every wake works.”** routing, firmware and state support require tests.
21. **“Compression always saves energy.”** CPU cost can exceed avoided memory or I/O cost.
22. **“Offload is automatically efficient.”** transfer and idle leakage can dominate.
23. **“Independent stable controllers remain stable together.”** coupled feedback loops can oscillate.
24. **“Battery percentage is a precise budget.”** estimation, temperature and aging add uncertainty.
25. **“Thermal emergency permits losing management.”** recovery capacity must be protected.
26. **“A policy tuned on one platform generalizes.”** topology, firmware and workload change the control plant.

## Worked Examples

### Example 1

A server uses 10 percent less power after a cap but completes 20 percent fewer requests in the same interval. Without draining the remaining queue, the result does not establish better energy per completion.

### Example 2

A compute burst scales nearly linearly with frequency and enables package sleep afterward. Race to idle wins. A memory-bound scan gains little speed at higher voltage and consumes more energy, so the same policy loses.

### Example 3

A deep idle state breaks even after 2.857 milliseconds and exits in 2 milliseconds. It is eligible for a predicted 10-millisecond gap with a 3-millisecond latency budget, but not with a 1-millisecond budget.

### Example 4

Moving a small task to an efficient cluster raises that cluster's shared frequency and wakes its cache domain. Whole-domain energy rises even though the selected CPU's isolated estimate was lower.

### Example 5

Packing batch work frees one package to sleep, but the active package reaches a thermal trip and throttles. A slightly wider placement completes sooner with lower total energy at thermal equilibrium.

### Example 6

A one-second device autosuspend delay saves no energy for requests arriving every 900 milliseconds. A 100-millisecond delay saves idle power but thrashes during bursts. Phase-aware batching and a bounded delay perform better.

### Example 7

A child device suspends successfully, but its parent bus remains active because another consumer holds a reference. Device-local residency alone overstates the system saving.

### Example 8

A power cap preserves average package demand but causes request tails when two tenants burst together. Per-service admission and service guardrails are needed in addition to the cap.

### Example 9

CPU counters show savings while an external meter shows no system improvement. Higher fan speed and longer memory activity explain the boundary mismatch.

### Example 10

A thermal sensor fails low. The controller's conservative fallback limits optional workload, preserves monitoring and initiates a safe shutdown if redundant evidence disagrees beyond a bound.

## Cross-Program Connections

- **Computer architecture:** voltage, frequency, idle states, caches, memory, uncore and sensors define capabilities.
- **Scheduling:** placement, capacity, utilization and deadlines constrain energy decisions.
- **Control engineering:** sampling, delay, hysteresis, saturation and coupled loops determine stability.
- **Real-time systems:** exit latency, throttling and capacity changes can invalidate timing analysis.
- **Storage engineering:** queueing, writeback, durability and device state determine batching trade-offs.
- **Networking:** link setup, interrupt moderation and batching couple device and CPU energy.
- **Embedded systems:** batteries, actuators, wake sources and suspend correctness dominate mobile operation.
- **Platform engineering:** policy rollout, canaries, telemetry and rollback govern heterogeneous fleets.
- **Security engineering:** energy authority, thermal denial of service and side-channel telemetry require access control.
- **Sustainability engineering:** correct system boundaries and completed-work normalization support credible reporting.

## References

1. Linux Kernel Documentation, [Energy Aware Scheduling](https://docs.kernel.org/scheduler/sched-energy.html), energy models, performance domains, capacity and placement limitations; retrieved 2026-09-04.
2. Linux Kernel Documentation, [CPU Performance Scaling](https://docs.kernel.org/admin-guide/pm/cpufreq.html), policy objects, drivers, governors and scheduler-driven scaling; retrieved 2026-09-04.
3. Linux Kernel Documentation, [CPU Idle Time Management](https://docs.kernel.org/admin-guide/pm/cpuidle.html), idle drivers, governors, target residency, exit latency and tick effects; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Energy Model of Devices](https://docs.kernel.org/power/energy-model.html), performance states, cost representation, scale and registration; retrieved 2026-09-04.
5. Linux Kernel Documentation, [Power Capping Framework](https://docs.kernel.org/power/powercap/powercap.html), zones, constraints, time windows and energy counters; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Generic Thermal Sysfs Driver How To](https://docs.kernel.org/driver-api/thermal/sysfs-api.html), thermal zones, trip points, cooling devices and bindings; retrieved 2026-09-04.
7. Linux Kernel Documentation, [Runtime Power Management Framework](https://docs.kernel.org/power/runtime_pm.html), device state, callbacks, usage accounting and autosuspend; retrieved 2026-09-04.
8. Linux Kernel Documentation, [System Sleep States](https://docs.kernel.org/admin-guide/pm/sleep-states.html), suspend-to-idle, standby, suspend-to-RAM and hibernation; retrieved 2026-09-04.
9. Linux Kernel Documentation, [System Suspend and Device Interrupts](https://docs.kernel.org/power/suspend-and-interrupts.html), suspend phases, interrupt handling and wakeup events; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Device Power Management Basics](https://docs.kernel.org/driver-api/pm/devices.html), device dependencies, suspend/resume ordering and callback domains; retrieved 2026-09-04.
11. Linux Kernel Documentation, [Basic Power Management Debugging](https://docs.kernel.org/power/basic-pm-debugging.html), system-sleep validation, platform states and device isolation; retrieved 2026-09-04.

## Exercises

### Exercise 1

Define an energy objective and service constraints for a battery-powered video-conferencing device. Specify work boundaries, quality, thermal state, radios, display, measurement and rollback.

### Exercise 2

A shallow idle state consumes 4 watts. A deep state consumes 0.5 watts, adds 10 millijoules of transition energy and has 2 milliseconds of exit latency. Calculate break-even, shallow and deep energy for a predicted 10-millisecond gap, then decide eligibility for 3- and 1-millisecond wakeup budgets.

### Exercise 3

Design an experiment that distinguishes race-to-idle from pace-to-idle for one compute-bound and one memory-bound workload on a thermally constrained heterogeneous system.

### Exercise 4

Construct a runtime-power policy for a sensor behind a shared bus. Include dependency ordering, autosuspend, I/O during transition, wakeup, faults, hot removal and evidence.

### Exercise 5

Diagnose a fleet change that reduces CPU energy counters by 12 percent while worsening wall-meter energy, request tails and thermal throttling. State hypotheses, measurements and safe rollback criteria.

## Answers to the Exercises

### Answer 1

Optimize joules per minute of correctly delivered call at fixed resolution, frame-rate range, audio quality and loss tolerance, while enforcing interaction latency, thermal skin limit, minimum session duration and emergency-call capacity. Begin after connection establishment at a normalized battery and thermal state; end after equivalent delivered media and drained queues.

Measure battery-side or wall energy, CPU/device counters, display brightness, radio state, encode/decode work, frames delivered and dropped, audio underruns, network conditions, temperature, frequency, idle residency and throttling. Cross bright/dim display, Wi-Fi/cellular, weak signal, foreground/background work and sustained thermal state. Roll back when quality, tail latency, thermal safety or recovery regresses, even if a component counter improves.

### Answer 2

The power difference is `3.5 W`, so break-even is `0.010 J / 3.5 W = 0.002857 s`, or `2.857 ms`. Over 10 milliseconds, the shallow estimate is `4 W * 0.010 s = 0.040 J = 40 mJ`. The deep estimate is `10 mJ + 0.5 W * 0.010 s = 15 mJ`, saving 25 millijoules in the toy model.

<!-- bijux-verify: {"id":"idle-state-break-even","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"break_even_ms=2.857\nshallow_energy_mj=40.000\ndeep_energy_mj=15.000\nsavings_mj=25.000\nlatency_budget_3ms=eligible\nlatency_budget_1ms=ineligible\n"}} -->
```python
shallow_power_w = 4.0
deep_power_w = 0.5
transition_energy_j = 0.010
predicted_idle_s = 0.010
exit_latency_ms = 2.0

break_even_s = transition_energy_j / (shallow_power_w - deep_power_w)
shallow_energy_j = shallow_power_w * predicted_idle_s
deep_energy_j = transition_energy_j + deep_power_w * predicted_idle_s

print(f"break_even_ms={break_even_s * 1000:.3f}")
print(f"shallow_energy_mj={shallow_energy_j * 1000:.3f}")
print(f"deep_energy_mj={deep_energy_j * 1000:.3f}")
print(f"savings_mj={(shallow_energy_j - deep_energy_j) * 1000:.3f}")
for budget_ms in (3, 1):
    time_ok = predicted_idle_s >= break_even_s
    latency_ok = exit_latency_ms <= budget_ms
    decision = "eligible" if time_ok and latency_ok else "ineligible"
    print(f"latency_budget_{budget_ms}ms={decision}")
```

This calculation assumes constant powers, accurate prediction, a transition-energy premium independent of time, no entry-latency service effect and no coupled package or device change. It illustrates a decision condition; it does not characterize a real CPU idle state.

### Answer 3

Fix completed work, inputs, affinity eligibility and initial cache and thermal conditions. Run both workloads at several performance limits and placement policies, including high-capacity burst, moderate pacing and an efficient core. Continue through thermal equilibrium and drain queues. Repeat randomized trials.

Collect wall energy, hardware counters, completions, execution and tail latency, active and idle residency by domain, requested and effective frequency, voltage proxy where available, memory bandwidth, cache events, migrations, package state, temperature, fan power and throttling. The compute-bound case tests whether shorter active time enables valuable sleep. The memory-bound case tests whether extra CPU power produces little completion gain. Reject policies that win cold but lose after sustained heat or violate service.

### Answer 4

Represent the sensor as a consumer of the shared bus, clocks and regulators. Hold runtime-PM usage while I/O is queued or executing; suspend the sensor before unused suppliers and resume suppliers first. Choose autosuspend from measured request gaps, transition energy, latency and burst behavior, with hysteresis to prevent thrash.

During transition, serialize new I/O into a bounded queue or cancel and retry under an explicit contract. Validate wake-enabled events in every supported system state. On callback failure, unwind to one coherent active or suspended state and retain error visibility. Hot removal cancels work, disables wake, drains references and detaches dependencies before freeing state. Trace usage counts, reasons, callback duration, bus and supplier residency, energy, service latency, failures and repeated cycles.

### Answer 5

Hypotheses include longer runtimes activating memory and devices, task spreading preventing package sleep, packing causing thermal concentration, lower CPU frequency extending fan use, counter-scope changes, wrap or calibration error, and queue backlog left outside the measurement boundary. Correlate controller decisions with completions and latency, CPU/package residency, requested/effective frequency, throttling reasons, temperature, fan state, memory and device activity, system wall power and counter deltas on aligned clocks.

Repeat equivalent-work trials from matched thermal state with the old policy, new policy and isolated subfeatures. Check counter version and scope against an external meter. Roll back automatically if service tails, errors, sustained thermal margin, completed-work-normalized wall energy or recovery capacity breach declared limits. Preserve the new-policy evidence for root-cause analysis rather than treating the component counter as success.
