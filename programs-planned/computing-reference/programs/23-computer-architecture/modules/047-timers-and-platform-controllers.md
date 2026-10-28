---
module_id: CA-047
program: Computer Architecture
level: 1
module_number: 47
title: Timers and Platform Controllers
status: complete
last_verified: 2026-09-04
---

# Timers and Platform Controllers

## One-Page Review

### Governing question

How should free-running counters, compare timers, real-time/alarm clocks, watchdogs and clock/reset/power controllers provide monotonic scheduling and safe platform lifecycle transitions despite finite width, asynchronous domains, frequency changes, interrupts, low-power states, failures and software races?

### Essential definitions

- A **counter** is hardware state that advances at a documented rate/source and wraps at its width.
- A **clock source** is a counter used to measure elapsed time.
- A **clock event device** generates one-shot or periodic events, often by comparing a counter with a deadline.
- A **compare register** holds a tick value whose relation to the counter asserts an interrupt/event.
- A **prescaler** divides a source clock before incrementing a counter.
- **monotonic time** never decreases within its promised observation domain, though rate adjustment may change slope.
- A **real-time clock** (`RTC`) maintains calendar/wall-clock time, often in an always-on domain.
- A **watchdog** resets, interrupts or escalates when software fails to service it within a programmed policy.
- A **windowed watchdog** rejects service that is too early as well as too late.
- A **reset controller** sequences reset assertion/deassertion across components and clock/power domains.
- A **clock controller** selects, divides, gates and observes clocks, including source-switch handshakes.
- A **power controller** sequences domain isolation, retention, power switches, clocks and reset.
- An **always-on domain** remains powered/clocked across selected low-power states to retain wake/time/watchdog logic.
- A **wake source** requests transition from low-power state to active processing.
- **drift** is accumulated phase error relative to an intended schedule; **jitter** is event-time variation.

### Central model, mechanism, or theorem

For a `W`-bit counter with modulus `M=2^W` and rate `f`, a deadline `d=(now+ceil(delay*f)) mod M` is compared using a wrap-safe relation valid only within a documented horizon smaller than half the modulus or by extended epochs. One-shot software programs compare, orders the write, rechecks counter/pending state and handles already-passed deadlines without losing an interrupt. Periodic schedules advance from the prior ideal deadline (`next += period`), not handler completion, to avoid accumulating service delay. Platform controllers execute dependency-ordered clock/reset/power state machines with acknowledgments and safe rollback/containment.

### Critical invariants

- Counter reads yield a coherent value across width, clock-domain and split-register interfaces.
- Tick/time conversions use the current documented rate, round in the safe direction and do not overflow silently.
- Deadlines and wrap comparisons stay within their proven horizon; no event is lost around wrap.
- Compare updates cannot clear, mask or miss a simultaneously due event without software-visible recovery.
- Timer interrupts remain pending until the programmed condition is moved/cleared according to exact semantics.
- Periodic event accounting handles late/missed periods explicitly without cumulative relative-delay drift.
- Watchdog service occurs only in the authorized window/path and cannot be disabled accidentally after lock.
- Clock source/divider/gating changes follow safe handshakes and update time conversion atomically.
- Reset/power sequencing preserves isolation, retention and dependency order; unpowered outputs never propagate unknown state.
- Wake/error paths have always-on resources and conditional progress independent of the domain they must revive.

### Common failures

Common failures include reading a split counter high/low once and accepting a torn value, converting nanoseconds with integer overflow, rounding a minimum timeout down, comparing unsigned deadlines with ordinary greater-than across wrap, scheduling beyond half-modulus without epochs, writing compare after the deadline then sleeping without recheck, clearing a level timer interrupt without moving the compare, adding periods to handler completion and accumulating drift, servicing watchdog from an unrelated periodic interrupt, switching clocks without readiness/lock, gating the clock needed to ungate itself, deasserting reset before clocks/power stabilize, omitting isolation around powered-off logic and trusting RTC as monotonic time.

### Compact example

An invented 10 MHz 32-bit counter has 100 ns ticks. A 250 microsecond delay requires 2,500 ticks. Starting at `0xffffff00`, the modular deadline is `0x000008c4` and forward modular delta is still 2,500. For five 1 ms periods (10,000 ticks each) with handler delays totaling 1,000 ticks, absolute-deadline scheduling ends at ideal tick 50,000 while relative completion-based scheduling drifts to 51,000. The arithmetic excludes interrupt and hardware write latency.

### Connections

Timers/platform controllers connect modular arithmetic, clock-domain crossing, interrupts, operating-system timekeeping, real-time scheduling, watchdog safety, DVFS, low-power states, reset/boot, RTC synchronization, firmware interfaces, fault management and formal state-machine verification.

## Governing Question

Time is derived from oscillators and counters, not an abstract perfect clock. Software needs stable elapsed time and future events while hardware changes frequency, sleeps and resets domains.

Platform controllers operate the dependencies that make computation possible. Their own progress and fault paths must remain available while the controlled domains are off or broken.

## Why This Matters

A lost timer interrupt can hang a scheduler; a backward clock can violate timeout/security logic; a torn counter can create a huge apparent jump. Watchdogs that are fed independently of real progress hide failures.

Clock/reset/power sequencing errors cause intermittent data loss and metastability that simulation may miss. DVFS changes can corrupt time conversion if multiplier state and counter sampling are inconsistent.

Precise contracts enable OS timekeeping, real-time workloads, suspend/resume and recoverable firmware.

## Prerequisites and Retrieval

Before studying this module, be able to:

- reason about synchronous counters and modular arithmetic;
- trace interrupt pending/claim/complete behavior;
- use clock-domain crossing and reset synchronization concepts;
- distinguish monotonic time, wall time, latency and rate;
- design state machines with acknowledgments, timeouts and safe error states.

Retrieve counter width/rate/source, reset/retention and per-core/shared scope; atomic/split read algorithm; compare count/channels and match polarity; write synchronization/delay; pending/clear/mask semantics; prescaler/frequency-change behavior; RTC frequency/calendar/alarm/battery domain; watchdog timeout/window/service/lock/escalation; oscillator/PLL sources, lock/ready/failure detection; clock mux/divider/gate rules; reset tree/assert/deassert synchrony; power domains, isolation, retention and wake sources; firmware/SBI/OS interfaces; calibration/error bounds; virtualization; counters/traces; RTL/firmware/OS revisions and errata.

## Learning Objectives

After completing this module, you should be able to:

1. convert between ticks and time with overflow and rounding control;
2. read narrow/split/asynchronous counters coherently;
3. compare deadlines safely across finite-width wrap;
4. program one-shot compares without lost-event races;
5. build drift-free periodic and missed-event policies;
6. distinguish clock source, clock event, RTC and watchdog roles;
7. design watchdog service/window/escalation that reflects real progress;
8. sequence clock, reset, power, isolation and retention safely;
9. verify timer/lifecycle safety and conditional progress;
10. measure drift, jitter, latency, power transitions and faults reproducibly.

## Core Exposition

### Identify the oscillator and counter

Trace the physical clock source through divider/prescaler to counter. State nominal/actual rate, tolerance, drift, temperature and power-state behavior.

A register labeled “time” may count cycles, fixed reference ticks or scaled units.

### Distinguish time domains

Monotonic time measures intervals; wall-clock time maps to civil/calendar time and can be adjusted. Boot/raw/reference clocks have different suspend/frequency semantics.

Use the domain whose contract matches timeout or timestamp intent.

### Convert ticks to time

For fixed rate `f`, seconds are ticks/f. Integer implementations use multiplier/shift or rational arithmetic to avoid division and overflow.

Carry enough precision and define rounding; timeout minima generally round ticks upward.

### Convert time to ticks

Compute `ceil(delay*f)` for “not earlier than” events using widened/checked arithmetic. Saturate/reject values beyond supported horizon.

Never multiply two large native-width values without overflow analysis.

### Read a single-width counter

If bus read captures the full counter atomically, one access suffices. Crossing asynchronous domains may use snapshot, Gray code or handshake.

Document staleness/coherence guarantees of the sampled value.

### Read a split counter

For high/low registers, read high, low, high and retry if highs differ (under the specified latch semantics). Some devices latch high on low read instead.

Follow the hardware contract rather than applying one generic sequence.

### Extend a narrow counter

Software can maintain wrap epochs if it samples often enough not to miss multiple wraps. Interrupt/counter extension must survive suspend/hotplug/reset rules.

State maximum safe interval between observations.

### Compare modulo deadlines

Ordinary unsigned `now>=deadline` fails across wrap. Signed-difference or modular-forward tests work only within a bounded half-range horizon.

For longer deadlines, use wider counters or explicit epochs.

### Program a one-shot timer

Compute deadline, mask/clear stale state as required, write compare, order synchronization, re-read time/pending and handle already-due condition.

If write crosses clock domains, include its acceptance latency/acknowledgment.

### Avoid lost compare races

Time can pass deadline between reading now and programming compare. Hardware may assert immediately, only on equality, or after synchronized update.

Use minimum delta, recheck and software-trigger/earliest fallback defined by platform.

### Handle level compare interrupts

Many timer interrupts remain asserted while `counter>=compare`. Handler programs a future compare before completing the interrupt.

Merely clearing controller pending can cause immediate redelivery or loss depending on source semantics.

### Handle equality-only compare

Equality-only hardware can miss a value if compare is written too late or counter skips. Prefer greater-or-equal semantics or explicit past-deadline recovery.

Formal tests should hit write/equality simultaneous cases.

### Schedule periodic events

Maintain ideal deadline `next=next+period`; after lateness, deliver/count missed ticks or skip forward by whole periods under policy.

Adding period to handler completion accumulates handler/scheduling delay.

### Account missed periods

Compute forward distance from ideal schedule and number of elapsed periods using checked modular/extended arithmetic. Decide whether to catch up, coalesce or report overruns.

Real-time clients need explicit overrun counts.

### Measure interrupt latency

Separate programmed deadline-to-source assertion, controller delivery, handler entry and callback execution. Clock-domain/write latency affects the first segment.

Report distributions and simultaneous higher-priority interference.

### Use clocksource quality

OS rates counters by stability, resolution, width, read cost and suspend behavior. Unstable sources can be demoted.

Cross-check reference clocks and detect backward/jump anomalies.

### Use clock event devices

Per-CPU one-shot devices support tickless scheduling; broadcast timers wake CPUs whose local timer stops in deep idle.

CPU hotplug and migration move pending deadlines safely.

### Virtualize timers

Guests see virtual time offsets/scales and virtual timer interrupts. Hypervisor must preserve monotonicity across scheduling/migration under contract.

Physical timer multiplexing needs efficient earliest-deadline and injection state.

### Understand RTC behavior

RTC may run from low-frequency/battery-backed oscillator and expose calendar registers plus alarms. Reads can cross second rollover and use BCD/calendar formats.

RTC is often less precise and can be set backward; do not use it as raw monotonic clock.

### Read RTC coherently

Use snapshot/freeze/status or repeat-read algorithm to avoid mixed fields from adjacent seconds. Validate calendar ranges and oscillator-valid/battery status.

Treat uninitialized RTC as untrusted input.

### Program alarms

Validate future time, enable/mask order and pending clear semantics. Always-on alarm routes through wake controller and then interrupt path.

Test alarm occurring during programming/suspend entry.

### Design watchdog timeouts

Select timeout longer than worst-case healthy progress including stalls, interrupt masking and low-power states, but short enough for safety/recovery target.

Feed only after checking real subsystem progress invariants.

### Use windowed watchdogs

A service window detects loops that kick too quickly. Software coordinates scheduling jitter and clock tolerance so healthy service stays inside window.

Early/late violations have explicit interrupt/reset escalation.

### Lock watchdog configuration

Safety/security systems may make enable, timeout or service key immutable until reset. Unlock sequences prevent accidental writes.

Privilege/firewall restricts service and configuration paths.

### Escalate watchdog failures

First stage can interrupt/NMI for evidence, next resets a domain/system, later platform action may power cycle. Evidence retention survives the chosen reset.

Do not depend on failed clocks/domains to execute escalation.

### Select clock sources safely

Clock mux switches only when source is enabled/stable and hardware provides glitch-free handshake. Wait for acknowledgment before disabling old source.

Failure detection falls back to a known safe source.

### Program dividers and PLLs

Respect divider legal encodings and PLL lock/ramp sequencing. Consumers may need temporary safe clock and voltage coordination.

Lock indication has filtering/timing semantics, not instantaneous proof of quality.

### Gate clocks

Integrated clock gates close only when safe phase/enable protocol prevents runt pulses. Functional logic quiesces first.

Never gate the controller/wake path needed to re-enable itself.

### Coordinate DVFS

Raise voltage before frequency and reduce frequency before voltage under platform constraints. Update timer/timekeeping conversion atomically around rate changes.

Fixed-reference counters simplify monotonic time despite core frequency changes.

### Assert reset safely

Reset assertion may be asynchronous for fault response, but state/outputs must enter containment deterministically. Stop new transactions and preserve required evidence.

Reset scope should match dependencies and shared resources.

### Deassert reset safely

Ensure power, isolation, clock and PLL/PHY readiness, then deassert synchronized to each destination clock. Release components in dependency order.

Asynchronous deassert can metastabilize divergent state bits.

### Sequence power down

Quiesce transactions, save/confirm retention, assert isolation, gate clocks, then remove power in platform order. Nonretained state becomes invalid.

Timeout leads to safe abort/forced containment with explicit data-loss policy.

### Sequence power up

Apply power, wait good, enable safe clock, restore retained state, release reset, initialize, then remove isolation and advertise availability.

Wake source and controller remain alive throughout.

### Handle retention

Retention registers need save/restore controls, power coverage and integrity/version. Software cannot assume every register survives.

Validate restored configuration before enabling side effects/DMA.

### Route wake sources

Timers, GPIO, network and watchdog events reach always-on logic that records cause and requests power-up. Mask/polarity/debounce and lost-wakeup races are defined.

Clear wake cause only after software records it and source is quiesced.

### Manage platform registers

Clock/reset/power controls are privileged MMIO with write-one, key/lock and status/ack fields. Use generated maps and ordered accessors.

Do not infer completion from control write; poll/interrupt on status with timeout.

### Handle oscillator failure

Monitor stopped/out-of-range clocks using independent reference where possible, switch safe source and record fault. Time uncertainty becomes explicit.

A monitor clocked by the failed source cannot detect its own stoppage.

### Handle brownout and reset causes

Always-on detectors assert reset/power action and latch cause. Cause registers survive enough reset to diagnose but are protected from spoofing.

Software records before clearing and correlates watchdog/power evidence.

### Calibrate clocks

Measure oscillator against reference and adjust conversion or trim. Calibration uncertainty, temperature and aging define accuracy bounds.

Never step monotonic time backward; slew/offset wall clock separately.

### Secure time and controllers

Attackers can manipulate timers, watchdogs, clocks or resets to bypass limits/fault analysis. Restrict controls, lock critical state and attest/configure early.

Virtual time/RTC inputs should not authorize security expiration without trust model.

### Verify counter/timers

Test wrap, minimum/maximum deadlines, split reads, clock changes and simultaneous compare writes/events. Assert monotonic extension and eventual interrupt.

Use formal modular properties and randomized CDC/timing simulation.

### Verify platform sequencing

Assert dependency order, acknowledgment, isolation while off, retained-state rules and eventual wake/fault fallback. Inject missing lock/power-good/ack.

Run gate-level/CDC/reset-domain analysis plus firmware tests.

### Gather layered evidence

Start with executable modular arithmetic, then RTL/formal/CDC, firmware/SBI/OS integration, low-power/reset fault injection and lab clock/power measurement.

Bind oscillator/controller/core RTL, firmware, OS, board, voltage/temperature and errata.

## Definitions and Notation

- `W`: counter width; `M=2^W` modulus.
- `f`: counter ticks/second under a specified source/divider.
- `tick_seconds=1/f`.
- `ticks(delay)=ceil(delay*f)` for a not-earlier-than event.
- `deadline=(now+ticks) mod M`.
- `forward(a,b)=(b-a) mod M`.
- `before(a,b)`: modular ordering valid only inside documented horizon, commonly `<M/2`.
- `period`: ideal tick spacing between recurring events.
- `lateness=actual-ideal` in an extended/unambiguous time domain.
- `jitter`: variation of event timing relative to reference schedule.
- `clock_ready`, `power_good`, `reset_done`, `isolation`: platform state predicates.
- `retained(x)`: state `x` is guaranteed/restored across the named power transition.
- `watchdog_window=[earliest,latest]`: allowed service interval under exact counter semantics.

Rate may vary; fixed-rate formulas require stable `f` or versioned conversion epochs. Wrap-safe comparisons require an explicit maximum interval.

## Mechanisms, Invariants, or Proof Structure

1. **Sample obligation:** counter/RTC reads correspond to one coherent instant under documented staleness.
2. **Conversion obligation:** tick/time arithmetic rounds safely and cannot overflow silently.
3. **Wrap obligation:** every comparison/extension stays within proven modulus horizon/epoch.
4. **Compare obligation:** programmed deadlines eventually assert or receive explicit past-deadline recovery.
5. **Pending obligation:** simultaneous set/clear/reprogram cannot lose an event.
6. **Periodic obligation:** ideal schedule and missed-event accounting avoid unintended drift/loss.
7. **Watchdog obligation:** authorized service proves progress and meets window/escalation policy.
8. **Clock obligation:** mux/divider/gate changes are glitch-free, acknowledged and conversion-aware.
9. **Reset obligation:** assertion/deassertion establishes deterministic contained state in dependency order.
10. **Power obligation:** quiescence, retention, isolation and power/clock ordering preserve live domains.
11. **Wake obligation:** always-on cause/path can revive the target without circular dependency.
12. **Fault obligation:** oscillator/lock/power/timeout failures reach safe fallback and retained evidence.
13. **Security obligation:** privilege/locks prevent unauthorized time/watchdog/lifecycle control.
14. **Progress obligation:** timer delivery and platform transitions complete under stated healthy dependencies.
15. **Evidence obligation:** claims bind clock sources/rates, RTL/firmware/OS, environment and endpoints.

Prove modular counter/deadline correctness within a bounded horizon, then timer interrupt refinement including write/pending races. Platform state machines use assume-guarantee dependencies: each domain promises quiescence/ack under live control clocks; always-on controller enforces safe order/fallback. CDC/reset proofs establish signal integrity.

## Alternatives and Trade-Offs

1. **Wide versus narrow counters:** wide avoids frequent wrap; narrow costs less area/read bandwidth.
2. **Fixed versus variable-rate counter:** fixed simplifies time; variable can reuse core clocks with conversion complexity.
3. **Per-core versus shared timer:** per-core scales scheduling; shared timer centralizes state/routing.
4. **One-shot versus periodic hardware:** one-shot supports tickless operation; periodic is simple.
5. **Equality versus greater-or-equal compare:** equality is small; greater-or-equal tolerates late programming.
6. **Direct versus firmware-mediated timers:** direct lowers latency; mediation virtualizes/policies hardware.
7. **RTC step versus slew:** step corrects quickly; slew preserves continuity.
8. **Simple versus windowed watchdog:** simple detects missing service; windowed also detects too-fast loops.
9. **Single versus staged watchdog:** single is compact; staged captures evidence/escalates.
10. **Clock gating versus frequency reduction:** gating maximizes idle savings; frequency retains responsiveness.
11. **PLL versus oscillator clock:** PLL offers performance; oscillator provides simple safe fallback.
12. **Synchronous versus asynchronous reset assertion:** synchronous is analyzable; asynchronous responds without clock.
13. **Retention versus reinitialization:** retention lowers wake latency; reinit simplifies state trust.
14. **Fine versus coarse power domains:** fine control saves energy; coarse domains simplify dependencies.
15. **Polling versus interrupt status:** polling is simple/bounded software; interrupts reduce active waiting.

## Failure Modes and Misconceptions

1. “Counter value is time in seconds.” Rate/conversion defines units.
2. “Counter frequency equals CPU frequency.” It may use an independent reference/prescaler.
3. “One high/low read is coherent.” Rollover can tear split values.
4. “Unsigned deadline comparison works across wrap.” Ordinary ordering fails near modulus.
5. “Signed-difference works for any interval.” It needs a half-range bound.
6. “Round-to-nearest schedules a minimum timeout.” Minimum deadlines round upward.
7. “Programming compare before sleep guarantees wake.” Past-deadline/write synchronization races require recheck.
8. “Clearing interrupt clears timer condition.” Level source may remain until compare moves.
9. “Periodic means add period to handler finish.” That accumulates service-delay drift.
10. “Missed periods should always all fire.” Catch-up/coalescing/overrun policy is explicit.
11. “RTC is monotonic.” It can be set, drift or lose validity.
12. “Wall clock is safe for timeouts.” Monotonic clocks are normally required.
13. “Watchdog feed proves health.” An unrelated timer ISR can feed while work is deadlocked.
14. “Shortest watchdog is safest.” Healthy worst-case latency/tolerance matters.
15. “Clock mux can switch anytime.” Glitch-free readiness/handshake is required.
16. “PLL lock is immediate proof.” Lock indication/timing/margin have semantics.
17. “Clock gating cannot affect state.” It affects handshakes/timers/CDC/progress.
18. “A domain can ungate its own only clock.” Wake control must remain live.
19. “Reset deassertion can be asynchronous.” It can metastabilize/diverge state.
20. “Reset erases all cause evidence.” Always-on retained cause should survive intentionally.
21. “Power off only requires a switch.” Quiescence/isolation/clock/reset/retention sequence matters.
22. “Retention covers every register.” Explicit retention lists and integrity are required.
23. “Wake cause may be cleared immediately.” Record and quiesce source first.
24. “DVFS only changes performance.” Time conversion and interface timing may change.
25. “Nominal oscillator rate proves accuracy.” Tolerance, temperature and aging create error.
26. “Simulation of nominal paths proves lifecycle.” CDC, gate-level and injected-failure evidence is needed.

## Worked Examples

### Example 1

A 10 MHz counter increments every 100 ns; 250 microseconds rounds exactly to 2,500 ticks.

### Example 2

Starting `0xffffff00`, adding 2,500 modulo 32 bits yields `0x000008c4`; the forward delta remains 2,500.

### Example 3

A split 64-bit counter rolls low between high reads; high-low-high detects mismatch and retries rather than returning a torn old-high/new-low value.

### Example 4

Counter passes deadline while compare synchronizes; software recheck observes due state and triggers earliest event rather than sleeping forever.

### Example 5

Periodic ideal deadlines 10k,20k,... remain fixed despite handlers delayed by 300 and 700 ticks; relative scheduling drifts 1,000 ticks.

### Example 6

A windowed watchdog accepts feed only after worker progress sequence advances and counter lies inside `[earliest,latest]`.

### Example 7

DVFS raises voltage, waits good, switches/divides clock, updates time conversion epoch, then allows workload at higher frequency.

### Example 8

Power-down quiesces DMA, saves retention, asserts isolation, gates clock and removes power; wake reverses with readiness checks.

### Example 9

Primary oscillator fails; independent always-on monitor selects safe clock, records cause and keeps watchdog/wake controller alive.

### Example 10

This deterministic model audits tick conversion, 32-bit wrap and absolute-versus-relative periodic drift.

<!-- bijux-verify: {"id":"timer-wrap-drift-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"counter_hz=10000000 tick_ns=100.000 delay_us=250 ticks=2500\nstart=0xffffff00 deadline=0x000008c4 modular_delta=2500\nperiod_hz=1000 events=5 absolute_final=50000 relative_final=51000 accumulated_drift=1000\n"}} -->
```python
counter_hz = 10_000_000
width = 32
modulus = 1 << width
delay_us = 250
ticks = (delay_us * counter_hz + 1_000_000 - 1) // 1_000_000
start = 0xffffff00
deadline = (start + ticks) % modulus
modular_delta = (deadline - start) % modulus

period_hz = 1000
period_ticks = counter_hz // period_hz
events = 5
handler_delays = [0, 300, 0, 700, 0]
absolute_final = events * period_ticks
relative_final = events * period_ticks + sum(handler_delays)

print(f"counter_hz={counter_hz} tick_ns={1e9 / counter_hz:.3f} delay_us={delay_us} ticks={ticks}")
print(f"start=0x{start:08x} deadline=0x{deadline:08x} modular_delta={modular_delta}")
print(f"period_hz={period_hz} events={events} absolute_final={absolute_final} relative_final={relative_final} accumulated_drift={relative_final - absolute_final}")
```

The rate, width and delays are invented. The model assumes a fixed exact clock, instantaneous compare writes and no interrupt latency; real systems need bounded wrap horizons, calibration and state-machine evidence.

## Cross-Program Connections

- **Operating Systems:** clocksource/clockevent, tickless scheduling, RTC and watchdog APIs consume hardware contracts.
- **Real-Time Systems:** deadline, jitter, overruns and watchdog windows determine guarantees.
- **Digital Design:** CDC, glitch-free muxes, reset synchronizers and retention implement controllers.
- **Power Engineering:** DVFS, gating and domain sequencing trade energy against wake latency.
- **Reliability Engineering:** watchdogs, clock monitors, brownout and reset cause enable recovery.
- **Security Engineering:** trusted time and locked lifecycle controls protect policy/evidence.
- **Formal Methods:** modular arithmetic, pending conservation and state-machine dependencies support proofs.
- **Performance Engineering:** read/event latency, jitter and low-power transitions determine overhead.

## References

1. RISC-V International, [Machine-Level ISA](https://docs.riscv.org/reference/isa/priv/machine.html), current counter/timer interrupt, privilege and reset context; retrieved 2026-09-04.
2. RISC-V International, [SBI Specification Repository](https://github.com/riscv-non-isa/riscv-sbi-doc), current firmware timer/service interface specification sources; retrieved 2026-09-04.
3. OpenTitan, [RISC-V Core-Local Timer](https://opentitan.org/book/hw/ip/rv_timer/), current open timer architecture, registers and verification documentation; retrieved 2026-09-04.
4. OpenTitan, [Always-On Timer](https://opentitan.org/book/hw/ip/aon_timer/), current wakeup/watchdog timer and low-power context; retrieved 2026-09-04.
5. OpenTitan, [Clock Manager](https://opentitan.org/book/hw/ip/clkmgr/), current clock gating, hints, monitoring and lifecycle documentation; retrieved 2026-09-04.
6. Linux kernel, [Clock Sources, Clock Events and sched_clock](https://docs.kernel.org/core-api/timekeeping.html), current kernel timekeeping hardware abstraction; retrieved 2026-09-04.
7. Linux kernel, [Timers](https://docs.kernel.org/timers/index.html), current timer/timekeeping documentation index; retrieved 2026-09-04.
8. Linux kernel, [Watchdog API](https://docs.kernel.org/watchdog/watchdog-api.html), current userspace watchdog contract; retrieved 2026-09-04.

## Exercises

### Exercise 1

Derive wrap-safe one-shot scheduling for 24-/32-/64-bit counters, including maximum horizon, conversion overflow and late compare programming.

### Exercise 2

Design a drift-free periodic timer with missed-period accounting, frequency changes, CPU migration and suspend/resume.

### Exercise 3

Specify a windowed multistage watchdog whose service proves application/system progress and whose evidence survives reset.

### Exercise 4

Extend the executable model with rate-change epochs, oscillator error and interrupt latency distributions.

### Exercise 5

Write a verification plan for clock/reset/power sequencing of a domain containing DMA and local timers with always-on wake/watchdog logic.

## Answers to the Exercises

### Answer 1

Use widened `ceil(delay*f)` and reject/saturate beyond the comparison horizon. Compute modular deadline and compare signed/modular difference only when forward interval is strictly below half modulus; longer events use epochs/wider reference. Program with minimum delta, synchronize write and recheck counter/pending; if passed, trigger earliest software/hardware path.

Test zero/minimum, half-range boundary, maximum supported, wrap on every field and simultaneous compare equality/write. Split counter reads follow device latch/retry semantics.

### Answer 2

Store ideal deadline in an extended stable reference domain; after each firing add fixed period, not handler completion. If now exceeds several deadlines, compute overruns and catch up/coalesce/skip by policy. On frequency change snapshot counter/time atomically, install new conversion epoch and reprogram remaining real-time delay.

Migration cancels old event only after target owns equivalent deadline; suspend uses retained/broadcast clock or records elapsed reference. Assert monotonic time, no lost event and bounded duplicate during handoff.

### Answer 3

Choose earliest/latest from measured worst-case healthy progress plus clock tolerance. A privileged monitor feeds only when worker sequence/checkpoints, scheduler/interrupt health and required I/O advance; never from an unconditional periodic ISR. Lock enable/window/service key after boot.

Stage one captures retained cause/log via independent NMI/always-on path, stage two resets domain/system, optional stage three power cycles. Test too-early/late, stalled worker with live timer, failed primary clock and reset-evidence persistence.

### Answer 4

Represent counter segments with start tick, rate and corresponding monotonic base; conversions choose the correct epoch and never step backward. Add bounded ppm error to actual tick duration and sampled interrupt latency values, then report deadline error/jitter distributions and cumulative wall versus monotonic drift.

Validate zero-error/fixed-rate outputs against the supplied model, test changes near wrap and state every synthetic distribution/seed.

### Answer 5

Verify DMA quiescence and outstanding completion before power-down; retention save/ack; isolation before power loss; clock gating/reset; always-on wake/watchdog independence. Power-up checks power-good, safe clock/PLL lock, synchronized reset release, retained integrity/reinit and isolation removal before DMA/timer enable.

Assert dependency order, no unknown off-domain output, no transaction loss, safe timeout fallback, eventual wake and retained reset causes. Run formal state-machine/CDC/reset-domain checks, gate-level timing, firmware/OS low-power stress and injected missing-ack/clock/brownout faults. Internal evidence is not external functional-safety or silicon certification.
