---
module_id: CA-004
program: Computer Architecture
level: 1
module_number: 4
title: Finite-State Control
status: complete
last_verified: 2026-09-04
---

# Finite-State Control

## One-Page Review

### Governing question

How can an architect turn a temporal control requirement into a complete finite-state machine whose transitions, outputs, handshakes, recovery and physical implementation remain correct under every permitted input sequence?

### Essential definitions

- A **finite-state machine**, or FSM, is a finite set of states with an initial state, inputs, a transition function and an output function.
- A **state** is a sufficient summary of relevant history for predicting future modeled behavior.
- A **Moore output** depends only on current state; a **Mealy output** depends on current state and current input.
- A **transition guard** is the condition under which an edge from one state to another is taken.
- A **reachable state** occurs on some permitted input trace from reset; an **illegal state** violates the specified encoding or invariant.
- **state encoding** maps abstract states to stored bit patterns, such as binary, one-hot or Gray-like codes.
- A **control/datapath decomposition** separates sequencing decisions from registers, arithmetic and bulk data movement.
- A **handshake** coordinates transfer through signals such as valid and ready, with an explicit acceptance event.
- A **safety property** says a bad state or event never occurs; a **liveness property** says required progress eventually occurs under stated assumptions.
- A **timeout** converts prolonged absence of an expected event into an explicit transition and recovery policy.
- **state minimization** merges behaviorally equivalent states under the declared observation model.

### Central model, mechanism, or theorem

An FSM is the tuple `(S, X, Y, F, G, s0)`, with recurrence `s_(k+1)=F(s_k,x_k)` and output `y_k=G(s_k)` for Moore or `y_k=G(s_k,x_k)` for Mealy behavior. A complete design defines `F` and `G` for every reachable state and permitted input combination, plus a policy for illegal encodings and environmental assumption violations.

Correctness is argued by induction: establish invariant `I(s0)`, then show `I(s) -> I(F(s,x))` for every permitted input. Progress requires a separate ranking, bounded-response or fairness argument; proving an unsafe output unreachable does not prove the controller eventually finishes.

### Critical invariants

- Every distinguishable protocol history maps to a state or explicitly retained datapath value.
- Every reachable state and permitted input has exactly one defined next state and output.
- Handshake side effects occur exactly on the declared acceptance event, never merely because one signal is high.
- Outputs that control writes, requests or hazards are stable and glitch-safe for their consumers.
- Reset establishes one coherent state; illegal encodings reach a safe response without unsafe transient output.
- Timeouts count the intended interval and cannot wrap, pause or restart accidentally.
- State encoding, synthesis optimization and recovery logic preserve abstract-machine behavior.
- Safety, liveness, timing, CDC and physical-fault evidence are stated separately.

### Common failures

Frequent failures are naming states after code locations instead of durable protocol meaning, omitting a history distinction, leaving a transition implicit, inferring latches through incomplete assignments, mixing old and next state, asserting valid for one cycle regardless of ready, consuming input without acceptance, generating a combinational loop between ready and valid, treating Moore as always safe and Mealy as always fast, adding a default transition that masks illegal states, using one-hot without checking multiple-hot or zero-hot faults, timing out one cycle early, assuming reset reaches every domain coherently, and calling simulation coverage a proof of safety or progress.

### Compact example

A transaction controller has `IDLE`, `ISSUE`, `WAIT`, `DONE` and `ERROR`. `start` moves `IDLE` to `ISSUE`; `ISSUE` asserts one request then moves to `WAIT`; a successful or failed response moves to `DONE` or `ERROR`; acknowledgment returns either terminal state to `IDLE`. Outputs derive from state. A trace with delayed success is `IDLE -> ISSUE -> WAIT -> WAIT -> DONE -> IDLE`. The model is complete only after specifying simultaneous response flags, cancellation, timeout, reset and illegal-state behavior.

### Connections

Finite-state control connects sequential logic, registers, instruction sequencing, bus and cache protocols, pipeline hazards, device controllers, handshakes, temporal logic, formal verification, fault recovery and hardware-description semantics.

## Governing Question

Digital systems perform actions over time: issue a memory request, wait for a response, update state, report completion and recover from error. A truth table for one instant cannot represent the relevant history. An FSM compresses that history into a finite state.

The governing question is how to choose sufficient state, define every transition and output, and connect the mathematical machine to synthesizable and physically timed hardware. The answer must cover normal sequences, stalled partners, simultaneous inputs, reset, illegal encodings and faults.

## Why This Matters

Controllers coordinate side effects. A duplicated write, missed acknowledgment or early grant can corrupt data even when the datapath arithmetic is perfect. A controller that waits forever can deadlock a processor or device.

FSM diagrams often look convincing because the happy path is visually simple. The missing behavior lives at boundaries: what if cancel and completion arrive together, ready falls, reset releases asynchronously, a counter wraps, or a state bit flips?

Good FSM design turns those questions into an executable contract, assertions and implementation constraints. It also separates safety from progress: “never writes twice” and “eventually completes” need different arguments and environmental assumptions.

## Prerequisites and Retrieval

Before studying this module, be able to:

- write Boolean expressions and truth tables;
- model synchronous state with old-state/next-state recurrence;
- explain registers, enables, reset, setup and hold;
- distinguish combinational and sequential hardware;
- read a basic timing trace.

Retrieve the temporal requirement; actors and ownership; accepted inputs; input stability and clock domains; outputs and side effects; handshake acceptance; ordering; cancellation; retry; timeout and maximum latency; reset and initialization; illegal-state and fault policy; datapath operations; resource conflicts; state and output encodings; target technology; synthesis settings; timing and CDC constraints; safety and liveness properties; environmental assumptions; coverage; counterexamples; mapping report; physical evidence; and recovery validation.

## Learning Objectives

After completing this module, you should be able to:

1. derive sufficient states from distinguishable protocol histories;
2. specify complete Moore and Mealy transition/output functions;
3. design valid/ready and request/response control correctly;
4. separate controller sequencing from datapath state;
5. choose and verify state encodings;
6. handle reset, illegal states, timeout, cancellation and errors;
7. state safety and liveness properties with assumptions;
8. avoid combinational loops, glitches and inferred latches;
9. verify refinement from abstract FSM to RTL and mapped hardware;
10. build assurance evidence for consequential controllers.

## Core Exposition

### Start from temporal requirements

Write scenarios as event sequences with acceptance points and forbidden outcomes. Identify which past events affect the next legal action. Those distinctions determine state.

Do not begin by drawing bubbles named `STATE1`. Name states by durable protocol meaning such as `waiting_for_response` or `draining_error`.

### Derive sufficient state

Two histories may share one state only if every permitted future input produces equivalent future observations. If one request has been issued and another has not, merging them is wrong when a later response must be interpreted differently.

Some history belongs in datapath registers rather than control state: an address, count or transaction ID. The controller still tracks whether that value is valid and who owns it.

### Define the machine formally

List finite state set `S`, input alphabet or predicates `X`, output set `Y`, initial state `s0`, transition `F` and output `G`. A table is often easier to audit than a picture.

For each row, state current state, relevant inputs, next state and outputs. Combine input cases only when they truly have identical consequences.

### Choose Moore or Mealy outputs

Moore outputs depend on registered state, which can simplify timing and glitch reasoning. They may add a state or cycle when an immediate input response is required.

Mealy outputs can react within the current cycle and reduce states or latency. They create input-to-output combinational paths and may glitch when inputs change. Register consequential outputs or constrain their consumers.

### Avoid false dichotomies

Real controllers mix styles. Busy status may be Moore, while `ready` depends on state and downstream readiness. The right question is whether each output's dependency, timing and sampling contract are safe.

Do not label an entire module “Moore” and stop reviewing paths. Inspect each output cone.

### Use complete combinational defaults

Next-state logic commonly begins with `next_state = state` and default outputs inactive, then overrides them in each case. This prevents unintended latches while making hold behavior explicit.

A default assignment is not an illegal-state policy. An unknown or corrupted encoding needs deliberate detection and recovery, not silent self-hold.

### Preserve old-state semantics

Combinational logic reads current registered state and computes next state. The state register commits once at the active edge. Do not update state with blocking procedural order that changes later decisions in the same modeled edge.

Keep `state` and `next_state` distinct in code and review. Derive registered outputs from the same old-state snapshot unless the specification says otherwise.

### Separate control and datapath

The controller selects operations: load, add, compare, shift, issue, commit. The datapath stores and transforms operands. Status such as zero, equal or complete returns to control.

This separation reduces state explosion and clarifies ownership. It can introduce long status-to-control-to-datapath paths, so pipeline or register boundaries remain architectural choices.

### Define handshake acceptance

For valid/ready, a transfer occurs on a sampled edge when both are asserted. The producer holds valid and payload stable until acceptance; the consumer asserts ready according to its capacity contract.

Never treat valid alone as consumption. If ready stalls, do not advance payload or controller state. Count side effects only on `valid && ready`.

### Avoid combinational handshake loops

If a producer makes valid depend combinationally on ready and a consumer makes ready depend on valid, their composition can loop or settle poorly.

Break the path with registered state or impose an interface rule. Analyze the composed modules, not each interface in isolation.

### Design request/response protocols

Track whether a request is unissued, presented, accepted, outstanding, completed or failed. If multiple transactions can be outstanding, a small FSM may need IDs and queues rather than one waiting bit.

Define response without request, duplicate response, response after timeout and simultaneous cancel. Do not assume the environment never violates protocol without an assertion and containment policy.

### Make side effects one-shot

A state held for several cycles can accidentally repeat a write or interrupt. Define whether output is a level valid throughout the state or a pulse on entry, exit or acceptance.

Entry detection compares current and next state or uses a dedicated transition. Verify stalls do not duplicate and a zero-cycle path does not omit the effect.

### Define priority among simultaneous inputs

Completion, cancel, timeout and reset can coincide. A source-code `if/else` creates priority whether intended or not.

Specify the ordering from semantics. If completion committed an external effect, cancellation may be too late. Test every meaningful combination.

### Add bounded timeout

A timeout counter begins at a named event, advances under named clock/enable conditions and transitions at a precise threshold. Define whether the bound counts acceptance, elapsed cycles or opportunities.

Choose width to prevent wrap before detection. Reset the counter at transaction boundaries, not merely when returning to an idle-looking state.

### Handle errors as states

An error flag with no control transition can leave resources owned or outputs active. Model drain, rollback, report, quarantine and acknowledgment where they require distinct future behavior.

Terminal error need not mean permanent halt. Define which state and evidence permit retry or reset.

### Specify reset semantics

Reset selects an initial abstract state and establishes datapath validity. Outputs during assertion and release must be safe for their consumers.

Coordinate reset across clock and power domains. A controller must not issue work before dependencies and retained data are valid.

### Handle illegal encodings

Binary encoding can leave unused patterns. One-hot encoding can become zero-hot or multiple-hot. Synthesis may optimize unreachable encodings under assumptions.

Define whether illegal state causes safe shutdown, diagnostic error, reset request or controlled recovery. Verify the path survives synthesis and does not assert unsafe outputs before recovery.

### Choose binary encoding

Binary encoding uses approximately `ceil(log2 |S|)` bits and may require more decode logic. It is compact and commonly chosen automatically.

Unused codes need policy. Bit faults can transform one legal state into another, so Hamming distance matters when faults are in scope.

### Choose one-hot encoding

One-hot uses one state bit per abstract state. Decode can be shallow and fast in FPGA fabrics, but storage and clock load grow.

Assert exactly one bit active, including after reset. A `case` style that assumes one-hot without checking can interpret multiple active states with accidental priority.

### Consider Gray and safe encodings

Gray-like assignment changes one bit along selected transitions, which can reduce decode hazards or help particular crossings. A general FSM graph may not permit every edge to be one-bit.

Fault-tolerant encodings maximize distance or reserve detectable codes. The tool's “safe FSM” option has specific behavior; inspect what it implements rather than relying on the name.

### Minimize states cautiously

Behaviorally equivalent states can be merged when no permitted future distinguishes them. Fewer states can reduce storage or logic.

Separate states can improve timing, observability, fault containment and one-cycle output control. Optimize under the full implementation objective, not abstract count alone.

### Account for output glitches

Combinational decoded outputs can glitch as state bits change at different physical times, even when abstract state updates together. One-hot transitions can briefly appear zero-hot or multiple-hot.

Register outputs controlling clocks, writes, resets or asynchronous consumers, or design hazard-free structures under a physical methodology. RTL zero-delay simulation is insufficient evidence.

### Cross domains at interfaces

An FSM can be correct inside its clock and still consume incoherent asynchronous inputs. Synchronize levels, handshake events and use asynchronous FIFOs for streams as appropriate.

Do not synchronize an encoded state bus bitwise for remote observation. Export a protocol-level status or snapshot with a coherent transfer.

### State safety properties

Examples include “grant A and grant B are never both asserted,” “commit implies an accepted request,” and “the FIFO is never read empty.” State assumptions explicitly.

Prove initialization and preservation by induction or model checking. Assertion syntax does not make a false environmental assumption true.

### State liveness properties

Examples include “every accepted request eventually completes or errors” and “a continuously requesting client is eventually granted.” Such claims need fairness or bounded-response assumptions about partners.

If a memory may never respond, the controller needs a timeout to prove bounded local progress. A liveness proof that assumes the desired response is circular.

### Use ranking and bounded response

A ranking function decreases on each progress step toward a terminal state and cannot decrease forever. For bounded protocols, counters can establish an explicit maximum latency.

Stutter states require a fairness assumption or timeout. Document which environment action enables progress.

### Verify reachability and coverage

Reachability analysis finds states and transitions possible from reset under assumptions. Unreachable design intent may indicate redundant state or overconstrained verification.

Simulation coverage reports exercised bins, not correctness. Review unhit arcs: they may be impossible by proof, missing stimulus or hidden dead code.

### Verify refinement to RTL

Compare an independent executable or formal transition model with RTL state and outputs. Check every input combination, simultaneous condition and reset sequence.

Equivalence after synthesis confirms a declared relation under tool assumptions. Inspect encoding and illegal-state transformations when recovery is part of the requirement.

### Close timing and physical behavior

Analyze input-to-output Mealy paths, state decode, datapath status, clock-to-output, setup, hold and pulse width. Constrain generated clocks and CDCs.

Post-layout evidence must cover skew, glitches, voltage, temperature and variation. For high-consequence control, include fault injection and hardware validation.

### Preserve diagnostic meaning

Expose state or event codes for debugging without turning internal encoding into a permanent external ABI. Stable semantic trace events survive encoding changes better than raw state bits.

Record request, acceptance, transition, timeout and error with correlation IDs. Trace loss and sampling perturbation limit conclusions.

## Definitions and Notation

- `S`: finite set of abstract states.
- `X`: set of permitted input valuations or symbols.
- `Y`: set of observable outputs.
- `s0`: initial state after the declared reset protocol.
- `F: S x X -> S`: next-state function.
- `G: S -> Y`: Moore output function.
- `G: S x X -> Y`: Mealy output function.
- `I(s)`: state invariant intended to hold for every reachable state.
- **guard:** Boolean condition selecting a transition.
- **acceptance event:** sampled condition at which a transfer or side effect becomes owned.
- **terminal state:** state that ends one modeled transaction, not necessarily all operation.
- **stutter step:** transition that preserves abstract state while awaiting an event.
- **ranking function:** well-founded measure used to argue progress.
- **state encoding:** mapping from abstract states to stored bit vectors.
- **illegal encoding:** vector outside the allowed encoded-state invariant.

## Mechanisms, Invariants, or Proof Structure

1. **Requirement claim:** define actors, events, side effects, ordering and completion.
2. **State sufficiency:** distinguish every history that changes future permitted behavior.
3. **Completeness invariant:** define next state and outputs for every reachable state/input pair.
4. **Acceptance invariant:** advance ownership and side effects only on declared handshakes.
5. **Priority invariant:** resolve simultaneous completion, cancel, timeout, error and reset.
6. **Datapath invariant:** controls and status preserve operand validity and transaction identity.
7. **Encoding claim:** map states without changing abstract transitions or outputs.
8. **Fault invariant:** illegal encodings and partner violations enter a safe bounded response.
9. **Reset invariant:** establish coherent control and datapath validity across domains.
10. **Safety proof:** establish initialization and inductive preservation of forbidden-state properties.
11. **Liveness proof:** state fairness or timeout assumptions and demonstrate required progress.
12. **Timing invariant:** close every registered and combinational control path at required corners.
13. **Crossing invariant:** synchronize or handshake all cross-domain information coherently.
14. **Evidence invariant:** separate model, RTL, synthesis, timing, physical and fault claims.
15. **Change invariant:** revalidate after requirement, encoding, synthesis or interface changes.

## Alternatives and Trade-Offs

- **Moore versus Mealy:** Moore outputs simplify registered-state reasoning; Mealy outputs reduce latency and add input paths.
- **Diagram versus transition table:** diagrams communicate flow; tables expose completeness and simultaneous inputs.
- **Binary versus one-hot encoding:** binary saves bits; one-hot can simplify decode and uses more clocked state.
- **Automatic versus explicit encoding:** tools optimize target cost; explicit encodings preserve selected fault or interface properties.
- **Minimal versus expanded state:** minimal machines reduce abstract state; expanded states simplify outputs and observability.
- **Controller versus microcode:** hardwired FSMs are direct and fast; microcode makes complex sequences writable and needs a control store.
- **Level versus pulse output:** levels tolerate stalls; pulses need exact capture and avoid repeated action.
- **Implicit versus explicit error state:** implicit flags save states; explicit states represent recovery history clearly.
- **Wait forever versus timeout:** waiting preserves slow partners; timeout bounds local progress and may abandon live work.
- **Cancel priority versus completion priority:** cancel-first limits unwanted action; completion-first preserves committed results.
- **Synchronous versus asynchronous reset:** synchronous reset fits clocked timing; asynchronous assertion handles missing clocks and complicates release.
- **Registered versus combinational ready:** registered paths close timing; combinational ready can reduce buffering and form loops.
- **Assertions versus reference model:** assertions target properties; models compare full transitions and can share specification defects.
- **Simulation versus formal exploration:** simulation handles realistic environments; formal explores all modeled traces under assumptions.
- **Automatic recovery versus safe halt:** recovery improves availability; halt avoids acting from uncertain state.

## Failure Modes and Misconceptions

1. **“A state diagram is a specification.”** missing guards, priorities and outputs can remain.
2. **“State names can reflect code order.”** durable names should express protocol meaning.
3. **“Fewer states always means better hardware.”** decode, timing and fault behavior matter.
4. **“Moore outputs never glitch.”** decoded state bits can transition non-simultaneously physically.
5. **“Mealy outputs are always one cycle faster.”** composition and registration determine latency.
6. **“Default next state solves completeness.”** it can hide omitted required transitions.
7. **“Incomplete assignments are don't-cares.”** they can infer unintended latches.
8. **“Valid means a transfer occurred.”** valid and ready must coincide at acceptance.
9. **“A held valid may advance payload.”** payload stays stable until accepted.
10. **“One-cycle request means one side effect.”** a stalled consumer may miss it.
11. **“Cancellation undoes completion.”** priority and external commit semantics decide.
12. **“A timeout counter is obvious.”** start, threshold, enable and wrap create boundary errors.
13. **“Error is just an output bit.”** recovery may require distinct ownership states.
14. **“Reset fixes every illegal state.”** unsafe outputs can occur before reset takes effect.
15. **“One-hot means exactly one bit is active.”** faults and reset can produce zero or many.
16. **“Gray encoding makes any transition safe.”** only selected graph edges differ by one bit.
17. **“Safe-FSM synthesis proves safety.”** tool recovery is narrower than system hazards.
18. **“Unreachable state means unnecessary state.”** verification assumptions may be too strong.
19. **“Full transition coverage proves correctness.”** it shows execution, not correct outputs or requirements.
20. **“Safety implies progress.”** a controller can remain safely stuck forever.
21. **“Liveness needs no environment assumption.”** partners may withhold required events indefinitely.
22. **“A false-path constraint fixes asynchronous input.”** a protocol is still required.
23. **“Synchronizing state bits exports state.”** the remote word can be incoherent.
24. **“RTL equivalence proves physical behavior.”** timing, glitches and faults remain.
25. **“Raw encoded state is a stable diagnostic API.”** synthesis and redesign can change it.
26. **“Simulation of the happy path is enough.”** stalls, concurrency, reset and faults own the hard cases.

## Worked Examples

### Example 1

A requester has not issued work versus has issued work and waits. Merging both as `BUSY` loses whether a response is legal, so the histories need distinct state.

### Example 2

A producer holds valid and payload for four stalled cycles. The controller advances exactly once when ready rises, preventing both loss and duplication.

### Example 3

Ready depends on valid in one module while valid depends on ready in another. Each looks combinationally reasonable; their composition creates a loop.

### Example 4

A write-enable is asserted throughout a three-cycle state. The memory receives three writes. Moving the effect to handshake acceptance makes it one-shot.

### Example 5

Completion and timeout arrive on the same edge. The specification gives accepted completion priority because its external write already committed.

### Example 6

A four-state binary FSM has no unused codes, yet a single-bit fault can jump between legal states. Encoding legality alone is not fault tolerance.

### Example 7

A one-hot controller enters two-hot state after an upset. An exactly-one assertion detects it and the output decoder suppresses unsafe grants before recovery.

### Example 8

An asynchronous status bus is synchronized per bit and briefly reports an impossible state. A snapshot handshake transfers one coherent semantic status.

### Example 9

A model proves grants are mutually exclusive but says nothing about starvation. A separate bounded-wait property and requester-stability assumption establish progress.

### Example 10

A mapped FSM changes encoding and removes an illegal-state branch considered unreachable. The assurance flow constrains that transformation or verifies fault recovery on the mapped netlist.

## Cross-Program Connections

- **Digital logic:** guards and output decoders are combinational functions.
- **Sequential logic:** state registers implement the recurrence and reset.
- **Processor design:** instruction, pipeline, cache and exception sequencing use FSM control.
- **Concurrency:** handshakes, arbitration and ownership encode hardware coordination.
- **Protocols:** request, response, retry, cancellation and timeout define temporal contracts.
- **Formal methods:** induction, reachability, safety, liveness and refinement support proofs.
- **Hardware languages:** event semantics and assignment completeness determine RTL behavior.
- **Security engineering:** illegal states, fault injection and diagnostic interfaces affect control integrity.
- **Testing engineering:** coverage, reference models and adversarial traces provide bounded evidence.
- **Systems engineering:** high-consequence controllers require hazards, traceability and independent acceptance.

## References

1. IEEE, [IEEE 1800-2023 — SystemVerilog](https://standards.ieee.org/ieee/1800/7743/), state variables, procedural semantics, assertions and verification constructs; retrieved 2026-09-04.
2. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), FSMs, datapaths, HDL and processor control; retrieved 2026-09-04.
3. AMD, [Vivado Synthesis: Finite State Machines](https://docs.amd.com/r/en-US/ug901-vivado-synthesis/Finite-State-Machines), recognition, encoding and synthesis behavior; retrieved 2026-09-04.
4. AMD, [UltraFast Design Methodology: Finite State Machines](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology/Finite-State-Machines), FSM timing, coding and implementation guidance; retrieved 2026-09-04.
5. Intel, [State Machine HDL Guidelines](https://www.intel.com/content/www/us/en/docs/programmable/683082/24-2/state-machine-hdl-guidelines.html), state-machine coding, encoding and recovery guidance; retrieved 2026-09-04.
6. Intel, [Avoid Unintentional Latch Generation](https://www.intel.com/content/www/us/en/docs/programmable/683082/24-2/avoid-unintentional-latch-generation.html), complete combinational assignments and synthesis behavior; retrieved 2026-09-04.
7. Neil H. E. Weste and David Money Harris, [CMOS VLSI Design: A Circuits and Systems Perspective](https://www.pearson.com/en-us/subject-catalog/p/cmos-vlsi-design-a-circuits-and-systems-perspective/P200000003427/9780321547743), sequential circuits, FSM implementation, timing and physical behavior; retrieved 2026-09-04.

## Exercises

### Exercise 1

Derive states for a one-outstanding-request controller supporting start, request acceptance, response, cancellation and acknowledgment. Explain why each history distinction matters.

### Exercise 2

Trace `IDLE`, `ISSUE`, `WAIT`, `DONE` and `ERROR` for a delayed successful response, then state safety and liveness properties and assumptions.

### Exercise 3

Design valid/ready control for a payload producer that can stall indefinitely. Cover stability, acceptance, reset and a downstream combinational-ready path.

### Exercise 4

Compare binary, one-hot and fault-detecting encodings for a six-state controller. Include area, decode, timing, illegal states and synthesis evidence.

### Exercise 5

Construct an assurance plan for a railway crossing controller FSM. Cover hazards, actors, timing, reset, CDC, faults, formal properties, physical evidence and named review.

## Answers to the Exercises

### Answer 1

Use `IDLE` before start, `PRESENTING` while request valid awaits acceptance, `OUTSTANDING` after acceptance, `DONE` after successful completion, `ERROR` after failed completion and optionally `CANCELING` if cancellation needs remote acknowledgment. `PRESENTING` preserves payload stability; `OUTSTANDING` makes responses legal; terminal states preserve outcome until acknowledged. If cancel before acceptance simply withdraws valid, it can return to `IDLE`; after acceptance it cannot pretend the remote effect never occurred.

Define simultaneous response/cancel priority, timeout, response without request and reset during ownership. A smaller machine is valid only if its outputs and datapath registers preserve every future-relevant distinction.

### Answer 2

The delayed-success trace is `IDLE -> ISSUE -> WAIT -> WAIT -> DONE -> IDLE`. The executable model produces state-derived outputs for the state visible at each step.

<!-- bijux-verify: {"id":"transaction-control-fsm","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"states=IDLE,ISSUE,WAIT,WAIT,DONE,IDLE\nissue_cycles=1\ndone_cycles=1\nerror_cycles=0\n"}} -->
```python
def step(state, event):
    if state == "IDLE":
        return "ISSUE" if event == "start" else "IDLE"
    if state == "ISSUE":
        return "WAIT"
    if state == "WAIT":
        if event == "response_ok":
            return "DONE"
        if event == "response_error":
            return "ERROR"
        return "WAIT"
    if state in {"DONE", "ERROR"}:
        return "IDLE" if event == "ack" else state
    raise ValueError("illegal state")


events = ("start", "tick", "tick", "response_ok", "ack")
states = ["IDLE"]
for event in events:
    states.append(step(states[-1], event))
print("states=" + ",".join(states))
print(f"issue_cycles={states.count('ISSUE')}")
print(f"done_cycles={states.count('DONE')}")
print(f"error_cycles={states.count('ERROR')}")
```

A safety property is that issue occurs only after start and exactly once before the modeled response. Another is that done and error are mutually exclusive. Liveness is that every start eventually reaches done or error and returns to idle after acknowledgment, assuming issue is accepted, the environment eventually supplies exactly one valid response, and acknowledgment eventually arrives. A real controller needs explicit acceptance, timeout, cancellation, reset and illegal-state rules.

### Answer 3

Register payload and assert valid when work becomes available. While `valid && !ready`, hold both unchanged. On an edge with `valid && ready`, transfer occurs exactly once; either load the next payload under a documented throughput rule or clear valid. Reset clears validity and establishes whether retained payload is unobservable.

Do not make valid combinationally depend on ready. If downstream ready is combinational, analyze the complete path from upstream state through ready and ensure no consumer-to-producer loop. Insert a skid buffer or registered-ready boundary when composition or timing requires it. Assertions cover payload stability while stalled, no acceptance without both signals, no drop, no duplication and correct reset behavior.

### Answer 4

Six-state binary needs at least three bits and leaves two unused encodings; decode may be deeper. One-hot uses six bits and often shallow decode, with illegal zero-hot and multiple-hot patterns. A fault-detecting code may use more bits or chosen Hamming distance so selected bit faults cannot become another legal state.

Compare actual mapped area, frequency, power and recovery logic on the target. Define safe outputs for illegal vectors, inject every covered state-bit fault, and verify recovery at the mapped representation. Inspect synthesis reports because automatic recoding can invalidate RTL-level fault claims. Equivalence covers normal behavior; fault-aware analysis covers behavior outside ordinary reachable-state assumptions.

### Answer 5

Define train-detection, barrier, road-signal, manual, maintenance, power and fault actors; safe state; timing from detection to road closure; and failure consequences. Derive states from ownership and physical feedback rather than command intent alone. Specify every sensor combination, simultaneous event, timeout, reset, degraded mode and illegal encoding.

Prove no unsafe road grant with an approaching train under stated sensor assumptions, one-shot actuator commands, bounded transition to safe state, and progress or alarm under component nonresponse. Analyze CDCs, clock loss, reset release, power failure, state upset, common-cause sensors, stuck actuators and communications. Add independent feedback and shutdown where the hazard requires it.

Verify the independent model, RTL, synthesis mapping, timing corners, physical glitches, environmental conditions and hardware-in-loop actuation. Fault-inject states, inputs, clocks, power and outputs. Preserve traceability and evidence identities. Named signaling, rail operations, road safety, hardware, firmware, clock/reset, functional-safety, cybersecurity, human-factors, maintenance, quality, regulator or authorized assessor and independent-assurance roles review their scopes. This chapter supplies no field authorization or certification.
