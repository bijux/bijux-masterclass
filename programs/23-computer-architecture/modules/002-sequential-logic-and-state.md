---
module_id: CA-002
program: Computer Architecture
level: 1
module_number: 2
title: Sequential Logic and State
status: complete
last_verified: 2026-08-29
---

# Sequential Logic and State

## One-Page Review

### Governing question

How can a digital circuit remember enough about its history to produce correct future behavior, and what evidence connects an ideal clocked-state model to physical hardware?

### Essential definitions

- **State** is the minimal retained information needed, together with future inputs, to determine future modeled behavior.
- A **sequential circuit** has outputs or future behavior that depend on stored state as well as current inputs.
- A **latch** is level-sensitive: while its enable level is active, changes can propagate into stored state.
- A **flip-flop** is edge-triggered in the architectural model: it samples an input at a designated clock edge and presents the captured value afterward.
- A **synchronous sequential circuit** uses a clocked discipline so state elements conceptually observe one old-state snapshot and commit their next values together.
- **Setup time** and **hold time** bound the interval before and after a sampling event in which the input must remain stable.
- **Metastability** is a physical state in which a bistable element takes an unbounded-in-principle time to resolve to a valid logical level after its sampling assumptions are violated.
- **Reset** establishes a specified initial or recovery state; its assertion, release, scope, and timing are part of the interface.

### Central model, mechanism, or theorem

Model a synchronous circuit by a recurrence:

`S_{k+1}=F(S_k,X_k)` and `Y_k=G(S_k,X_k)` or `Y_k=G(S_k)`.

At clock event `k`, every state element samples next-state data computed from the same pre-edge state `S_k`. After clock-to-output delay, the new state `S_{k+1}` becomes observable. This discrete model is valid only when clock, setup, hold, reset, and electrical assumptions hold.

### Critical invariants

- State has one declared owner, width, encoding, initialization rule, and update event.
- Next state is computed from the same logical old-state snapshot.
- Every legal old state and input has a defined next state or an explicitly handled illegal-state policy.
- Maximum path delay satisfies the clock-period obligation; minimum path delay satisfies the hold obligation.
- Asynchronous inputs and clock-domain crossings use a reviewed synchronization or protocol mechanism.
- Reset release cannot leave related state elements in an incoherent combination.
- Simulation, synthesis, static timing, formal properties, and physical validation support distinct claims and are never treated as interchangeable.

### Common failures

Common errors include calling any feedback “memory,” confusing latches and flip-flops, updating modeled registers sequentially in software instead of simultaneously, omitting a next-state branch, treating reset as a Boolean afterthought, assuming a two-flop synchronizer eliminates metastability, synchronizing each bit of a bus independently, and claiming that RTL simulation proves timing or hardware safety.

### Compact example

Two edge-triggered state bits form a shift relation: `a_{k+1}=x_k` and `b_{k+1}=a_k`. If the old state is `(a,b)=(0,0)` and `x=1`, the committed next state is `(1,0)`. Computing `a=1` and then `b=a` in an ordinary sequential program would incorrectly produce `(1,1)`. Hardware-description semantics and review must preserve the common old-state snapshot.

### Connections

[CA-001](001-boolean-logic-and-combinational-circuits.md) supplies the next-state combinational functions. [CA-003](../ROADMAP.md) develops registers, memories, and clocking structures; [CA-004](../ROADMAP.md) develops finite-state control. Timing and physical limits connect to later architecture modules, while concurrency and hardware-description-language semantics connect to programming-language and verification programs.

## Governing Question

Combinational logic maps present inputs to present outputs. A processor, protocol engine, counter, cache controller, or interrupt unit must also remember what happened. How can that memory be represented precisely enough to design, implement, and verify, without pretending the physical circuit is an instantaneous mathematical recurrence?

The answer separates three layers. The behavioral layer defines a state-transition system. The synchronous implementation layer places combinational next-state logic between clocked state elements. The physical layer supplies transistors, wires, clocks, voltage margins, and timing behavior. Correct engineering connects the layers with explicit assumptions and evidence.

## Why This Matters

State is where time enters digital architecture. Instruction progress, pipeline occupancy, cache coherence, branch prediction, memory transactions, and device protocols are histories compressed into finite representations. A missing state bit can make two materially different histories indistinguishable. A redundant or poorly encoded state can waste area or complicate recovery. A timing failure can invalidate an otherwise perfect transition table.

Sequential logic also exposes a recurring systems principle: an abstraction works only under a contract. The clocked model lets engineers reason as though updates are simultaneous, but physical propagation is not simultaneous. Setup, hold, skew, jitter, metastability, reset release, and clock-domain crossings define when the abstraction is justified.

## Prerequisites and Retrieval

From [CA-001](001-boolean-logic-and-combinational-circuits.md), retrieve Boolean functions, propagation delay, acyclic combinational networks, exhaustive finite-domain checks, and the distinction between logical and physical correctness. You should understand binary vectors, recurrence notation, basic probability, and the idea of an invariant.

Recall that a function has no memory by itself. Feedback creates a dynamical system, but only a deliberately designed state element with timing and electrical constraints provides a reviewable storage abstraction.

## Learning Objectives

After completing this module, you should be able to:

- distinguish history, state, output, next-state logic, and physical storage;
- derive a minimal sufficient state for a bounded behavior;
- write and trace synchronous recurrence equations;
- explain bistability, SR and D latches, and edge-triggered D flip-flops;
- preserve simultaneous-update semantics in an executable or HDL model;
- derive setup and hold obligations for a register-to-register path;
- explain metastability without claiming it can be eliminated;
- choose and qualify reset, enable, and clock-crossing strategies;
- compare simulation, assertions, static timing, formal analysis, and measurement;
- construct an assurance plan for sequential logic used in a consequential system.

## Core Exposition

### From history to state

A system's complete history can be arbitrarily long. Useful state is a sufficient summary. If two histories produce the same state, then for every allowed future input sequence they must produce indistinguishable modeled future behavior. Otherwise the representation has forgotten relevant information.

A parity accumulator need not retain every input bit; one bit recording even or odd parity is sufficient. A saturating two-bit counter needs four distinguishable values. A request protocol may need `idle`, `waiting`, and `acknowledged` states because the same current input has different meaning in each. “State” is therefore relative to an observation model and requirement.

Sequential behavior is written as a transition function `F`. Let `S_k` be state immediately after sampling event `k` and `X_k` the inputs sampled for that transition. Then `S_{k+1}=F(S_k,X_k)`. Output can depend only on state, `Y_k=G(S_k)`, or also on current input, `Y_k=G(S_k,X_k)`. [CA-004](../ROADMAP.md) later develops those finite-state-machine styles.

### Feedback and bistability

Cross-coupled inverting structures can have two stable operating points. That bistability allows one bit of information to persist after the initiating input is removed. An SR latch exposes set and reset controls, but certain combinations are forbidden or technology-dependent. A D latch adds gating so one data value determines the stored result and removes the ordinary need to command set and reset independently.

A D latch is transparent while enabled. That can support efficient time borrowing, but it means values may propagate across more than one logical stage during the active level unless a disciplined multi-phase design prevents races. A D flip-flop presents an edge-triggered abstraction, commonly implemented from latch or pulse structures: the input is sampled around a clock edge, then appears at the output after clock-to-Q delay.

The abstract symbol does not reveal transistor topology, internal nodes, power-up state, scan features, asynchronous controls, or library-specific timing. Those properties come from the selected cell and technology documentation.

### The synchronous discipline

Consider a bank of state elements whose outputs feed combinational next-state logic, which feeds state-element inputs. During a clock interval, old state propagates through the combinational network. At the active edge, all destination elements conceptually sample their inputs. After the edge, their outputs change and begin computation for the next interval.

“All together” is a logical contract, not literal simultaneity. Clock edges arrive at different elements at slightly different times; data paths have minimum and maximum delays. The timing methodology proves that these variations remain within bounds where the discrete recurrence is valid.

An enable should ordinarily select between retaining old state and loading next state: `S_{k+1}=E_k?F(S_k,X_k):S_k`. This expresses ownership directly. Generating ad hoc clocks with ordinary combinational logic can create glitches, skew, and unrecognized clock paths; dedicated clock-gating cells and tool flows exist for designs that truly gate clocks.

### Simultaneous update semantics

Suppose `a_{k+1}=x_k` and `b_{k+1}=a_k`. Both right-hand sides refer to old state. In SystemVerilog, nonblocking assignments are the conventional sequential-RTL mechanism because updates are scheduled so a clocked block reads the pre-update values. Blocking assignments used carelessly for modeled state can make simulation depend on statement order.

The language is richer than this convention. Multiple processes, event regions, unknown values, initialization, and synthesis restrictions matter. IEEE 1800-2023 defines SystemVerilog semantics; a style rule or simulator warning is not a substitute for the standard and project-specific linting.

### Timing obligations

For a path from source flip-flop to destination flip-flop, define:

- `t_{cq,max}` and `t_{cq,min}`: maximum and minimum clock-to-output delay;
- `t_{comb,max}` and `t_{comb,min}`: maximum and minimum data-path delay;
- `t_{setup}` and `t_{hold}`: destination setup and hold requirements;
- `U_{setup}` and `U_{hold}`: conservative terms covering relevant skew, jitter, and analysis uncertainty under a declared sign convention.

A simplified setup obligation is

`T_{clk} ≥ t_{cq,max}+t_{comb,max}+t_{setup}+U_{setup}.`

A simplified hold obligation is

`t_{cq,min}+t_{comb,min} ≥ t_{hold}+U_{hold}.`

Setup limits the maximum useful clock frequency. Hold is a minimum-delay obligation and cannot generally be repaired merely by lengthening the clock period. Real static-timing analysis uses launch/capture relationships, corners, generated clocks, reconvergence, variation, exceptions, and library arcs. The equations are review scaffolding.

### Metastability

If input changes too near the sampling event, a bistable element can enter an analog metastable condition and take unusually long to resolve. No finite waiting time guarantees resolution in every physical instance. A synchronizer increases available resolution time and reduces the probability that unresolved or late behavior reaches downstream logic; it does not abolish the phenomenon.

For a single asynchronous control bit, a destination-domain chain of dedicated registers is common. Its mean-time-between-failure estimate depends on technology characterization, available settling time, destination clock frequency, input toggle rate, implementation, and operating conditions. AMD's current methodology documentation emphasizes design-dependent MTBF and careful review of asynchronous clock-domain crossings.

Independently synchronizing every bit of a multi-bit word can yield a combination that never existed at the source because bits resolve on different cycles. Multi-bit transfer needs an appropriate protocol: handshake, Gray-coded pointer under proved transition assumptions, bundled data with stable-window rules, asynchronous FIFO, or another reviewed clock-domain-crossing structure. A narrow pulse can also disappear between destination edges; pulse capture needs its own design.

### Reset and initialization

Reset is a state transition with system consequences. A synchronous reset is sampled at a clock edge and fits ordinary timing, but it requires a running clock. An asynchronous reset can assert without a clock, which may be necessary for safety or power sequencing, but deassertion near an edge can violate recovery/removal constraints or release related elements inconsistently.

A common strategy asynchronously asserts and synchronously releases reset within each clock domain. That slogan still requires a real reset-tree, domain, power, test, and failure analysis. Some state need not reset if the design prevents observation before valid initialization; resetting every bit can cost routing, power, timing, and implementation flexibility. The specification must distinguish don't-care power-up state from required architectural state.

### Verification layers

Transition-table or executable-model checks establish behavior in a discrete model. RTL simulation checks language-level event semantics for chosen stimuli. Assertions can state invariants such as “reset implies idle on the next sampled edge” or “a counter never exceeds its maximum.” Formal model checking can explore all modeled input sequences within assumptions. Equivalence checking can compare transformed representations.

Static timing analysis checks path constraints under characterized models and constraints. Clock-domain-crossing analysis identifies structural patterns and suspicious crossings. Gate-level simulation can expose some initialization and delay interactions, though it is not universal physical proof. Silicon measurement, environmental qualification, fault injection, and production test address additional layers.

Every method is conditional. A formal proof with an unconstrained reset, a timing report with a false-path mistake, or a simulation that never crosses clocks adversarially can pass while the hardware fails.

## Definitions and Notation

Let the finite state space be `\mathcal{S}`, input space `\mathcal{X}`, and output space `\mathcal{Y}`. A deterministic sequential model is a tuple `(\mathcal{S},\mathcal{X},\mathcal{Y},F,G,S_0)` with initial state `S_0`, transition `F:\mathcal{S}\times\mathcal{X}\to\mathcal{S}`, and output `G`.

A state representation is **sufficient** when equal represented state implies equal future observations for every permitted future input sequence. It is **reachable** if some permitted input trace from `S_0` produces it. An **invariant** `I(S)` holds initially and is preserved by every permitted transition:

`I(S_0) ∧ ∀S,X: I(S)⇒I(F(S,X)).`

This induction rule is a proof obligation inside the model. It does not prove that fabricated hardware satisfies timing, reset, electrical, or environmental assumptions.

A **clock domain** is state governed by a defined clock relationship and timing analysis. A **clock-domain crossing (CDC)** transfers information between domains without a safely timed common sampling relationship. **Recovery** and **removal** constraints play reset roles analogous to setup and hold for asynchronous control release and assertion, with cell-specific definitions.

## Mechanisms, Invariants, or Proof Structure

A reviewable sequential design follows this chain:

1. Define observations and the histories that must remain distinguishable.
2. Choose state sufficient for future behavior; identify reset and illegal states.
3. Specify `F` and `G` for every legal state/input pair.
4. Encode state and derive combinational next-state/output logic.
5. Implement storage with explicit clock, enable, reset, and crossing rules.
6. Prove model invariants and compare implementation semantics with the transition model.
7. constrain and close setup, hold, reset, CDC, power, and test obligations.
8. preserve tool versions, assumptions, reports, counterexamples, waivers, and physical evidence.

The executable model demonstrates simultaneous state updates, enable-as-hold, reset priority, and bounded counting. It computes every next-state tuple before committing it.

<!-- bijux-verify: {"id":"synchronous-state-recurrence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"shift_trace=[(1, 0), (0, 1), (1, 0)]\ncounter_trace=[0, 1, 2, 2, 3, 0]\ninvariant=all_states_in_range\n","stderr":""}} -->
```python
def shift_step(state, input_bit):
    old_a, old_b = state
    next_a = input_bit
    next_b = old_a
    return next_a, next_b


def counter_step(state, *, reset=False, enable=True):
    if reset:
        return 0
    if not enable:
        return state
    return (state + 1) % 4


shift = (0, 0)
shift_trace = []
for bit in (1, 0, 1):
    shift = shift_step(shift, bit)
    shift_trace.append(shift)

counter = 3
counter_trace = []
for control in (
    {"reset": True},
    {},
    {},
    {"enable": False},
    {},
    {},
):
    counter = counter_step(counter, **control)
    counter_trace.append(counter)

assert all(a in (0, 1) and b in (0, 1) for a, b in shift_trace)
assert all(0 <= value < 4 for value in counter_trace)
print(f"shift_trace={shift_trace}")
print(f"counter_trace={counter_trace}")
print("invariant=all_states_in_range")
```

This run establishes only the listed finite Python traces and range assertion. It has no clock, propagation delay, four-state values, synthesis semantics, setup/hold behavior, metastability, reset network, CDC, power, or physical faults. It cannot validate an RTL implementation or silicon.

## Alternatives and Trade-Offs

**Latch versus flip-flop.** Latches can enable time borrowing and efficient pipelines but require careful phase and race reasoning. Flip-flop-based design offers simpler edge-based composition at possible area, power, or timing cost.

**Synchronous versus asynchronous design.** Synchronous design creates global timing boundaries and mature tool flows. Asynchronous circuits can avoid a global clock and exploit local completion, but require different protocols, libraries, verification, and physical methodology. “No clock” does not mean “no timing.”

**Binary, one-hot, and other state encodings.** Binary uses fewer state bits; one-hot may simplify next-state logic and increase speed while using more storage. Gray-like encodings can limit bit changes for particular crossings. Fault detection, illegal-state recovery, power, physical placement, and tool optimization affect the choice.

**Reset every element versus valid-state tracking.** Comprehensive reset can make initialization obvious but burdens routing and timing. Valid bits or controlled initialization can reduce reset load, while demanding proof that uninitialized state is never observed or used unsafely.

**Enable multiplexing versus clock gating.** Data-path enable retains state through an input multiplexer and keeps clocking the element. Proper clock gating can reduce clock power but requires dedicated cells, glitch control, test integration, and timing constraints.

**Simulation versus formal exploration.** Simulation handles detailed environments and long realistic traces but samples. Formal analysis can cover all modeled traces or prove inductive properties, but abstractions and assumptions must be audited. Both need independent requirements and physical sign-off.

**Reliability versus latency at crossings.** Additional synchronizer stages give more resolution time but add cycles. Handshake and FIFO protocols add logic and latency while preserving events or data coherency. The right target derives from measured device parameters, rates, consequences, and system requirements.

## Failure Modes and Misconceptions

1. **State is all past input.** State is a sufficient summary relative to future observations, not necessarily the full history.
2. **Feedback always stores a stable bit.** Arbitrary combinational feedback can oscillate, race, or settle unpredictably.
3. **A latch and flip-flop differ only in name.** A latch is level-sensitive; a flip-flop presents an edge-triggered abstraction.
4. **Registers update in source-code order.** Correct synchronous modeling reads a common old state and commits next values together.
5. **Longer clock periods fix every timing failure.** They can help setup but generally do not repair minimum-delay hold violations.
6. **Two synchronizer stages eliminate metastability.** They reduce propagation probability under characterized assumptions; residual risk remains.
7. **Synchronize each bus bit independently.** The destination may observe an incoherent combination.
8. **Reset is instantaneous and global.** Distribution, assertion, release, clock domains, power domains, and cell constraints matter.
9. **An unreachable state needs no policy.** Faults, initialization, formal abstraction, or encoding upset may make it reachable.
10. **RTL simulation proves hardware timing.** RTL ordinarily abstracts the physical timing behavior that static analysis and measurement address.
11. **Static timing proves functionality.** Timing analysis checks constrained paths, not whether `F` and `G` implement the right behavior.
12. **An MTBF number is universal.** It depends on technology, placement, settling time, rates, conditions, model, and the set of crossings aggregated.

## Worked Examples

### Example 1

**Question:** What state is needed to output whether the number of received 1 bits is odd?

**Reasoning:** Future parity depends only on whether previous parity is even or odd. The transition toggles on input 1 and holds on 0.

**Conclusion:** One bit is sufficient; retaining the entire input history is unnecessary.

### Example 2

**Question:** Old state is `(a,b)=(1,0)` and equations are `a'=x`, `b'=a` with `x=0`. What is next state?

**Reasoning:** Both right-hand sides use old values: `a'=0` and `b'=1`.

**Conclusion:** Next state is `(0,1)`; statement-order evaluation that yields `(0,0)` violates synchronous semantics.

### Example 3

**Question:** A D latch is enabled high and its input changes twice while enable remains high. What happens in the ideal model?

**Reasoning:** The latch is transparent during the active level, so output follows those changes subject to delay. It retains the final sampled value after disable.

**Conclusion:** Treating the latch as edge-triggered hides race and time-borrowing behavior.

### Example 4

**Question:** A path has `t_{cq,max}=80` ps, `t_{comb,max}=620` ps, `t_{setup}=70` ps, and `U_{setup}=50` ps. What simplified minimum clock period follows?

**Reasoning:** Sum the maximum launch, combinational, setup, and uncertainty terms: `80+620+70+50=820` ps.

**Conclusion:** The simplified bound is 820 ps, about 1.22 GHz before other analysis obligations; it is not a sign-off result.

### Example 5

**Question:** The same path fails hold by 25 ps. May the designer slow the clock?

**Reasoning:** Hold concerns data arriving too soon after the capture event. The next clock period does not normally move that same-edge minimum path enough to solve it.

**Conclusion:** Fix minimum delay, clock relationship, cell choice, routing, or constraints through the physical methodology.

### Example 6

**Question:** Why can an asynchronous push button not feed ordinary synchronous logic directly?

**Reasoning:** Its transition has no guaranteed relation to the sampling edge and may violate setup/hold; it can also bounce. A synchronizer addresses metastability probability, while debouncing addresses repeated transitions.

**Conclusion:** Synchronization and semantic filtering are distinct mechanisms.

### Example 7

**Question:** Can an eight-bit asynchronous status word use eight independent two-flop synchronizers?

**Reasoning:** Bits can be captured on different destination cycles, producing a word never emitted by the source.

**Conclusion:** Use a coherent transfer protocol such as handshake, stable bundled data, or asynchronous FIFO suited to the contract.

### Example 8

**Question:** Why might reset assertion be asynchronous but release synchronized?

**Reasoning:** Assertion can force a safe state without a clock. Synchronized release gives each domain a controlled edge relationship and reduces incoherent recovery.

**Conclusion:** The pattern is useful but still needs domain-specific recovery/removal, distribution, and power analysis.

### Example 9

**Question:** A formal tool proves `counter<4` for all cycles. What remains unproved?

**Reasoning:** The proof depends on modeled width, reset, inputs, transition semantics, and assumptions. It says nothing by itself about timing, CDC, synthesis mapping, radiation, or the correctness of the requirement.

**Conclusion:** Preserve the model and assumptions and add implementation and physical evidence.

### Example 10

**Question:** A watchdog's state machine is used to place an infusion pump into a safe state. Does exhaustive RTL state exploration authorize deployment?

**Reasoning:** It can prove modeled transition properties. Safety also depends on clock and reset faults, sensor/actuator interfaces, independent shutdown paths, timing bounds, common-cause failures, power behavior, physical effects, requirements, manufacturing, and operations.

**Conclusion:** A named functional-safety and clinical authority must review the hazard analysis, traceability, independence, evidence, and residual risk. This chapter claims no certification or external review.

## Cross-Program Connections

[Programming Languages: Theory of Programming](../../07-programming-languages-theory-of-programming/ROADMAP.md) contributes induction, transition systems, invariants, and model checking. [Programming Languages: Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) studies state, ordering, and races in software; synchronous hardware has different execution semantics but shares the need for explicit transitions.

[Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) contributes oracles, property checks, coverage, and evidence limits. [Security Engineering](../../25-security-engineering/ROADMAP.md) examines fault injection and state corruption. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns system requirements, interface contracts, hazards, verification, validation, and lifecycle assurance.

Within this program, [CA-003](../ROADMAP.md) develops storage structures and clocking, [CA-004](../ROADMAP.md) develops finite-state control, and [CA-008](../ROADMAP.md) deepens critical-path and frequency analysis.

## References

- IEEE, [*IEEE 1800-2023 — SystemVerilog Unified Hardware Design, Specification, and Verification Language*](https://standards.ieee.org/ieee/1800/7743/), active standard published 2024 and official record checked 2026-08-29. Current primary language semantics for RTL, assertions, simulation, and verification constructs.
- Sarah L. Harris and David Money Harris, [*Digital Design and Computer Architecture: RISC-V Edition companion resources*](https://pages.hmc.edu/harris/ddca/ddcarv.html), official author site checked 2026-08-29. Sequential logic, state elements, synchronous design, timing, metastability, synchronizers, and HDL.
- Thomas J. Chaney and Charles E. Molnar, [*Anomalous Behavior of Synchronizer and Arbiter Circuits*](https://doi.org/10.1109/T-C.1973.223730), `IEEE Transactions on Computers` C-22(4), 1973. Primary experimental account of metastable and oscillatory behavior.
- AMD, [*UltraFast Design Methodology Guide: Constraining Asynchronous Clock Groups and Clock Domain Crossings*](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology/Constraining-Asynchronous-Clock-Groups-and-Clock-Domain-Crossings), release 2026.1 checked 2026-08-29. Current vendor methodology for CDC review and the limits of default timing analysis.
- AMD, [*UltraFast Design Methodology Guide: Optimizing for MTBF*](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology/Optimizing-for-MTBF), release 2026.1 checked 2026-08-29. Current vendor guidance on design-dependent synchronizer MTBF.
- Intel, [*Quartus Prime Standard Edition User Guide: Metastability Analysis*](https://www.intel.com/content/www/us/en/docs/programmable/683068/18-1/metastability-analysis.html), official documentation checked 2026-08-29. Vendor treatment of synchronization chains, characterized parameters, and MTBF reporting.
- Neil H. E. Weste and David Money Harris, [*CMOS VLSI Design: A Circuits and Systems Perspective*, fourth edition](https://www.pearson.com/en-us/subject-catalog/p/cmos-vlsi-design-a-circuits-and-systems-perspective/P200000003427/9780321547743), Pearson. Circuit-level state elements, sequential timing, clocking, and physical implementation.

## Exercises

### Exercise 1

Design a one-bit running parity state model. Give `S_0`, `F`, an invariant, and the trace for inputs `1,1,0,1`. Explain why one state bit is sufficient.

### Exercise 2

For a register path with `t_{cq,max}=90` ps, `t_{comb,max}=710` ps, `t_{setup}=80` ps, and `U_{setup}=70` ps, compute the simplified minimum period and maximum frequency. Then evaluate hold when `t_{cq,min}=35` ps, `t_{comb,min}=20` ps, `t_{hold}=30` ps, and `U_{hold}=35` ps.

### Exercise 3

Review this intended shift behavior: on each rising edge, `a` receives `input` and `b` receives the old `a`. Explain why ordinary in-order assignment can be wrong, write the recurrence, and give the trace from `(0,0)` for inputs `1,0,1`.

### Exercise 4

Choose a transfer mechanism for (a) a slowly changing single-bit alarm, (b) a one-cycle pulse, (c) a 32-bit configuration word, and (d) a continuous data stream between unrelated clocks. State the invariants and failure evidence needed for each.

### Exercise 5

A rail-braking controller uses sequential logic to detect stale commands and enter a safe state. Construct an assurance plan covering transition completeness, illegal states, timing, reset, CDC, clock and power faults, synthesis, physical evidence, fault injection, configuration control, and named human review.

## Answers to the Exercises

### Answer 1

Let `S∈{0,1}` denote even and odd parity, with `S_0=0`. Define `F(S,X)=S⊕X` and output `Y=S`. For inputs `1,1,0,1`, post-edge states are `1,0,0,1`. The invariant is that `S` equals the XOR of all accepted input bits so far. Initially both are zero; each transition XORs the new bit into both sides, so induction preserves the invariant. Two histories with equal parity respond identically to every future input sequence, so one bit is sufficient for this observation.

### Answer 2

The setup sum is `90+710+80+70=950` ps. Its reciprocal is approximately `1.053` GHz, so the simplified upper frequency is about 1.05 GHz before other paths and sign-off effects. For hold, earliest data arrival is `35+20=55` ps; the requirement plus uncertainty is `30+35=65` ps. The path misses the simplified hold obligation by 10 ps. Increasing the period is not the general repair; the physical flow must correct minimum delay or the clock/constraint relationship and rerun all corners.

### Answer 3

The recurrence is `a_{k+1}=x_k` and `b_{k+1}=a_k`. Both right-hand sides use old state. An in-order program that writes `a` first and then assigns `b=a` observes the new `a` and collapses the pipeline. From `(0,0)`, inputs `1,0,1` produce `(1,0)`, `(0,1)`, and `(1,0)`. Compute next values separately, then commit together; in sequential RTL use the project's reviewed nonblocking-assignment convention.

### Answer 4

For a slowly changing single bit, a destination-domain synchronizer chain may be suitable if its characterized MTBF meets the consequence target; the value must remain long enough to be observed. For a one-cycle pulse, use pulse stretching plus synchronization, toggle encoding with acknowledgement, or a handshake so no event is silently lost. For a 32-bit configuration word, use a handshake with bundled data held stable across acknowledgement, or a versioned mailbox; independent per-bit synchronizers are incoherent. For a continuous stream, use an asynchronous FIFO with reviewed pointer encoding, full/empty logic, reset coordination, and memory semantics.

Evidence covers source/destination frequency relationships, toggle/event rates, stability windows, no-loss/no-duplication rules, coherency, ordering, backpressure, overflow/underflow, reset in either domain, simultaneous reset release, wraparound, metastability containment, reconvergence, implementation placement, and device-specific MTBF. Structural CDC reports require reviewed waivers; adversarial simulation/formal checks and post-layout timing complement them.

### Answer 5

Define the accepted command, stale threshold, safe state, clock assumptions, braking response deadline, degraded modes, and observation boundary. Enumerate every legal state/input transition and an explicit policy for illegal encodings. Prove invariants for deadline tracking, monotonic transition into safe state under stated faults, and prohibition of unsafe output combinations. Verify the RTL against an independent transition model and review synthesis equivalence.

Constrain maximum and minimum paths, reset recovery/removal, generated clocks, and every CDC. Analyze oscillator drift/loss, reset assertion and release, brownout, power-domain sequencing, memory upset, sensor and communication faults, common-cause failure, and actuator feedback. Review independent watchdog or physical shutdown paths so the same clock, power, or logic defect cannot defeat detection and braking. Use static timing across required corners, CDC/reset analysis, gate/netlist checks where useful, fault injection, hardware-in-loop tests, environmental and EMC qualification, and representative end-to-end stopping tests.

Preserve tool versions, constraints, waivers, netlists, device lots, configuration, test results, and traceability from hazard to requirement to evidence. Named digital-design, physical-design, clock/reset, power, rail-domain, braking, cybersecurity, verification, manufacturing, operations, and independent functional-safety authorities must review their scopes. The authorized assessor and accountable operator must decide residual-risk acceptance under applicable standards. This course chapter supplies no field authorization, certification, or external review.
