---
module_id: SEPAT-022
program: Software Engineering: Patterns
level: 1
module_number: 22
title: Bridge
status: complete
last_verified: 2026-08-28
---

# Bridge

## One-Page Review

### Governing question

When do two dimensions of behavior need to evolve independently, and how can delegation connect them without creating an invalid Cartesian product, a lowest-common-denominator interface, or ambiguous lifecycle ownership?

### Essential definitions

- **Bridge** decouples an abstraction from its implementation so the two can vary independently.
- The **abstraction** expresses client-facing policy and delegates primitive work.
- A **refined abstraction** varies client policy without changing the implementor contract.
- The **implementor** defines the primitive operations required by abstractions; a **concrete implementor** realizes them for one platform or mechanism.
- A **variation axis** is a dimension with its own reasons and cadence of change.
- The **cross-product problem** occurs when inheritance creates one subtype for every pair of abstraction and implementation variants.
- A **compatibility relation** identifies valid abstraction–implementor pairs; not every pair is necessarily supported.
- A **capability** advertises optional implementor behavior without pretending it is universally available.
- **Pimpl** (pointer to implementation) hides representation and can stabilize a compiled interface; it is related but not automatically a full Bridge.
- A **binding policy** chooses an implementor at construction, configuration, request, or operation time.

### Central model, mechanism, or theorem

Let abstraction variants be \(A\), implementors \(I\), and valid combinations \(C\subseteq A\times I\). A Bridge represents an abstraction \(a\) holding an implementor \(i\) and maps each high-level operation into a protocol over implementor primitives. If every combination is valid, separate families require \(|A|+|I|\) main components and wiring instead of up to \(|A||I|\) combined subclasses. This count is only structural; the design is correct only when the implementor contract is sufficient, each \((a,i)\in C\) preserves abstraction behavior, invalid pairs are rejected, and lifecycle/error/concurrency semantics compose.

### Critical invariants

- The two axes have independent stakeholders, change drivers, or release cadence supported by evidence.
- Client code depends on the abstraction; implementor-specific types do not leak through its public contract.
- Implementor primitives express stable mechanism, not one refined abstraction's workflow.
- Each supported pair satisfies behavioral, capability, lifecycle, error, and performance constraints.
- Unsupported pairs fail during explicit binding/validation, before partial work.
- One owner creates, starts, reconfigures, and closes each implementor resource.
- Concurrency and thread-affinity requirements are visible at the bridge boundary.
- Tests cover each side independently and every supported compatibility class.

### Common failures

Common failures include inventing two hierarchies for one stable variant, splitting inseparable concepts into artificial axes, exposing concrete implementors to clients, designing primitives around one abstraction, assuming all pairs work, capability checks scattered through business code, abstraction and implementor both retrying or caching, runtime swapping while operations are in flight, lifecycle leaks from shared implementors, using Bridge where Strategy or Adapter is simpler, and citing \(m+n\) class count as proof of lower complexity.

### Compact example

Two report abstractions—compact and detailed—delegate to two output implementors—plain text and structured text. Four valid combinations are created without four combined report subclasses. The abstraction owns metric policy; implementors own representation. The finite output proves composition only for those combinations.

### Connections

[SEPAT-021](021-adapter.md) reconciles an existing mismatch; Bridge designs two variation axes together. [SEPAT-023](../ROADMAP.md) represents recursive part-whole structures, and [SEPAT-024](../ROADMAP.md) adds responsibilities while preserving one interface. Bridge also connects to [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

Which client-facing policies and underlying mechanisms change independently enough to justify separate contracts, and what evidence shows their valid combinations can be composed safely?

Bridge is not “composition over inheritance” in the abstract. It is a specific response to two dimensions that would otherwise be entangled. The abstraction hierarchy and implementation family remain independently understandable, testable, and selectable.

## Why This Matters

A rendering library may vary shapes and device backends; a database API may vary access abstractions and drivers; a control application may vary domain policy and hardware transport. Combining both axes in subclasses multiplies code and makes a change in one dimension repeat across the other.

Delegation reduces duplication only if the implementor contract captures stable primitives. An overly broad implementor becomes another platform API leak; an overly narrow one forces chatty calls, poor performance, and abstraction-specific escape hatches.

## Prerequisites and Retrieval

You should understand interfaces, delegation, inheritance, substitutability, Abstract Factory, Adapter, Strategy, lifecycle, and compatibility testing. Retrieve these facts:

1. Independent variation means more than “there are two lists of classes.”
2. Public abstraction results and errors must not reveal concrete implementor types.
3. A shared implementor can have concurrency and lifetime obligations beyond a single abstraction.
4. Optional capabilities make the valid pair set smaller than a full Cartesian product.
5. Runtime replacement is harder than construction-time selection because operations may retain old state.
6. Binary-interface hiding, platform portability, and behavioral abstraction are related but distinct goals.

## Learning Objectives

After completing this module, you should be able to:

- identify evidence for two independent variation axes;
- derive abstraction and implementor contracts from responsibilities;
- model and validate supported compatibility pairs;
- distinguish Bridge from Adapter, Strategy, Abstract Factory, Pimpl, and plugins;
- specify binding time, capability negotiation, lifecycle, and concurrency;
- test abstraction policy and implementor conformance separately;
- evolve either axis without leaking platform detail;
- contract a Bridge when one axis disappears or no longer varies.

## Core Exposition

### Discover axes from change history

List changes by reason and owner. If report policy changes with product requirements while output backends change with platform deployments, the axes may be independent. If every new report requires a bespoke backend protocol, they are coupled and a Bridge may create fiction.

Start from direct composition. Extract the implementor only when duplicated mechanism or an imminent supported variant makes the boundary useful.

### Design the abstraction

The abstraction owns client vocabulary, invariants, orchestration, and result semantics. It should not return backend handles, driver exceptions, device buffers, or transport-specific status codes.

Refined abstractions change high-level policy: compact versus detailed report, interactive versus batch drawing, transactional versus read-only session. Keep the family cohesive; unrelated use cases may need separate abstractions.

### Design implementor primitives

Implementor operations should be sufficient and stable across abstractions: draw line, emit metric, allocate surface, begin/commit operation. Primitive granularity affects performance and expressiveness.

Too fine-grained creates round trips and prevents backend optimization. Too coarse encodes one abstraction workflow and blocks refinement. Permit batched commands or an intermediate representation when backends need whole-operation optimization.

### Compatibility is a relation

Do not assume \(C=A\times I\). A detailed report may require units and metadata unsupported by a minimal backend. A hardware renderer may have fixed color depth. A transaction abstraction may require isolation a driver cannot provide.

Bind through a validated factory/composition root that compares required and offered capabilities. Prefer typed capability sets or distinct implementor interfaces over string flags. Reject before serving traffic.

### Binding time

Construction-time binding is easiest to reason about. Configuration-time binding supports deployment choice. Per-request binding supports tenant/platform routing but increases compatibility and resource complexity.

Runtime rebinding requires a generation protocol: create and validate the new implementor, route new work, let old operations finish, then close the old one. Mutating the delegate pointer during an operation can mix mechanisms.

### Lifecycle and ownership

The composition root usually owns implementors and injects them into abstractions. If several abstractions share one resource, none should close it independently. A scope owner starts and closes it after dependent abstractions drain.

If abstractions create implementors internally, the bridge becomes hidden construction policy and tests lose control. Use a factory only at the owned boundary.

### Error semantics

Implementors return mechanism errors in a controlled internal taxonomy. The abstraction maps them into client-facing outcomes without erasing retry/indeterminate/unsupported distinctions.

Avoid retry at both levels. Decide whether mechanism handles transport retries and abstraction handles semantic retries, then bound attempts under one deadline and idempotency policy.

### Concurrency and affinity

Document whether implementors are immutable, thread-safe, confined, pooled, or single-operation. A GUI backend may require one event thread; a database connection may be transaction-confined; a renderer may accept concurrent immutable command buffers.

The abstraction must schedule accordingly. Delegation does not make an implementor safe for concurrent refined abstractions.

### Performance

Virtual dispatch is rarely the only cost. Measure allocation, batching, data conversion, calls across process/device boundaries, synchronization, cache locality, and backend pipeline utilization.

Expose performance-sensitive capabilities through stable contracts rather than downcasts. If one backend needs batch submission, consider making batches the primitive for all valid implementations or defining a separate capability boundary.

### Evolution

Adding an abstraction should not edit implementors unless it needs a new primitive. Adding an implementor should not edit abstractions except compatibility declarations/tests. If every change touches both sides, revisit the split.

Version implementor contracts deliberately. Default methods can mask unsupported semantics; explicit version/capability negotiation is safer for distributed or plugin boundaries.

### Testing

Test abstractions against small recording implementors to verify command protocol and client behavior. Run conformance contracts for each concrete implementor. Then test every compatibility class, not necessarily every instance, including failure, concurrency, lifecycle, and performance thresholds.

Recording fakes must enforce ordering and capability limits rather than accepting impossible calls. High-risk backends need hardware/system evidence beyond interface tests.

### Contraction

If only one implementor remains and no credible variation exists, inline it behind the abstraction or remove the delegation. If only one abstraction remains but multiple mechanisms persist, the design may be Strategy, driver interface, or ordinary port.

Preserve client contracts during contraction and delete obsolete capability matrices, factories, and tests.

## Definitions and Notation

Let \(A\) be abstraction variants, \(I\) implementors, \(C\subseteq A\times I\) supported pairs, \(req(a)\) required capabilities, and \(cap(i)\) provided capabilities:

\[
(a,i)\in C\Longrightarrow req(a)\subseteq cap(i).
\]

Let abstraction operation \(op_a\) translate into implementor protocol \(\pi_i=(p_1,\ldots,p_k)\). Refinement requires observable trace \(trace(\pi_i)\) to satisfy the abstraction contract for every supported pair. If there are \(m\) abstractions and \(n\) implementors with full compatibility, a combined-subclass design can require up to \(mn\) pair classes, while a Bridge has roughly \(m+n\) primary classes plus binding and compatibility logic. This is a structural estimate, not a complexity theorem.

## Mechanisms, Invariants, or Proof Structure

### Decomposition argument

If abstraction changes require no implementor changes unless primitives change, implementor changes preserve the primitive contract, and supported pairs are validated, then each axis can evolve locally for those changes. The conclusion fails when hidden knowledge, performance assumptions, or capability downcasts cross the boundary.

### Compatibility validation

At binding, compute required and offered capability sets plus version, lifecycle, and environment constraints. Reject the pair with a causal diagnostic if any requirement is missing. Do not begin partial output before validation.

### Protocol conformance

For each refined abstraction, specify allowed implementor call sequences and result mapping. For each implementor, verify every allowed sequence, error, cancellation, and lifecycle state. Pair tests verify interactions that separate contracts cannot capture.

### Executable two-axis bridge

<!-- bijux-verify: {"id":"report-output-bridge","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"compact-text=cpu: 72\ndetailed-text=cpu | value=72 | unit=percent\ncompact-structured={metric:cpu,value:72}\naxes=2x2\n","stderr":""}} -->
```python
class TextOutput:
    def compact(self, metric, value):
        return f"{metric}: {value}"

    def detailed(self, metric, value, unit):
        return f"{metric} | value={value} | unit={unit}"


class StructuredOutput:
    def compact(self, metric, value):
        return f"{{metric:{metric},value:{value}}}"

    def detailed(self, metric, value, unit):
        return f"{{metric:{metric},value:{value},unit:{unit}}}"


class CompactReport:
    def __init__(self, output):
        self.output = output

    def render(self, metric, value, unit):
        return self.output.compact(metric, value)


class DetailedReport:
    def __init__(self, output):
        self.output = output

    def render(self, metric, value, unit):
        return self.output.detailed(metric, value, unit)


text = TextOutput()
structured = StructuredOutput()
compact_text = CompactReport(text)
detailed_text = DetailedReport(text)
compact_structured = CompactReport(structured)
detailed_structured = DetailedReport(structured)

print(f"compact-text={compact_text.render('cpu', 72, 'percent')}")
print(f"detailed-text={detailed_text.render('cpu', 72, 'percent')}")
print(f"compact-structured={compact_structured.render('cpu', 72, 'percent')}")
print(f"axes={len((compact_text, detailed_text))}x{len((text, structured))}")

assert detailed_structured.render("cpu", 72, "percent") == "{metric:cpu,value:72,unit:percent}"
```

The run constructs all four finite combinations and verifies representative representation/policy outputs. It does not prove escaping, schema validity, localization, arbitrary metrics, concurrency, performance, or that the axes will evolve independently.

## Alternatives and Trade-Offs

**Direct composition** is best for one stable abstraction and implementation. Extract only when change evidence appears.

**Strategy** varies an algorithm used by one context; Bridge emphasizes two independently extensible structural families. A one-abstraction Bridge may simply be Strategy.

**Adapter** makes an existing incompatible interface satisfy a target. An adapter can implement the Bridge implementor contract for a legacy backend.

**Abstract Factory** chooses compatible product families. It can construct Bridge pairs but does not itself define their delegation relationship.

**Pimpl** hides representation and stabilizes ABI for one abstraction. It becomes Bridge-like when multiple implementors and refined abstractions are first-class variation axes.

**Plugins/drivers** support independently deployed implementations and add discovery, versioning, trust, isolation, and unload concerns.

**Conditional dispatch** may be clearer for two tiny stable mechanisms. Replace it when change diffusion and testing cost become material.

## Failure Modes and Misconceptions

- **“Any delegation is Bridge.”** Two evidence-backed variation axes are required.
- **“All combinations come free.”** Compatibility, lifecycle, and performance need validation.
- **“The implementor is low-level only.”** Its primitives must be stable across real abstractions, not merely small methods.
- **“Capabilities can be downcast.”** Downcasts leak implementations and scatter compatibility policy.
- **“Runtime swapping is a setter.”** In-flight work and resource ownership require generations/drain.
- **“m+n classes prove simplicity.”** Binding, contracts, tests, and interactions also contribute complexity.
- **“Bridge and Adapter are synonyms.”** Bridge is designed for independent evolution; Adapter reconciles mismatch.
- **“One shared implementor is safe.”** Sharing introduces concurrency and closure obligations.
- **“Every backend error is the same.”** Abstractions still need actionable and honest outcomes.
- **“The bridge must remain forever.”** Contract when an axis disappears.

## Worked Examples

### Example 1

Shapes vary independently from raster, vector, and remote drawing backends. A batch primitive avoids one network call per line. **Conclusion:** Primitive granularity must respect implementation economics.

### Example 2

Compact and detailed reports target text and structured output as in the executable example. Escaping and schema validation are added to real implementors. **Conclusion:** Representation remains an implementor responsibility.

### Example 3

A database access abstraction uses multiple drivers, but transaction isolation requirements restrict valid pairs. The root rejects unsupported isolation before opening work. **Conclusion:** Driver interfaces need compatibility validation.

### Example 4

A C++ library uses Pimpl solely to stabilize ABI with one private implementation. It is not presented as a two-family Bridge. **Conclusion:** Representation hiding and independent variation are distinct claims.

### Example 5

A notification abstraction varies urgent and digest policies over email and SMS transports. SMS lacks attachment capability, so attachment-requiring digests are invalid pairs. **Conclusion:** Capability relations prevent false Cartesian products.

### Example 6

A GUI abstraction delegates to an event-thread-confined backend. Background refined abstractions enqueue immutable commands rather than calling it directly. **Conclusion:** Bridge does not erase thread affinity.

### Example 7

A storage abstraction swaps generation 8 driver for generation 9 during rollout. New sessions bind to 9 while existing transactions pin 8 until close. **Conclusion:** Runtime rebinding is lifecycle versioning.

### Example 8

Both abstraction and transport implement retries, multiplying attempts. Policy is centralized under one deadline: transport handles safe connection establishment; abstraction handles only domain reconciliation. **Conclusion:** Cross-layer mechanisms need one owner.

### Example 9

A product once supported five deployment backends, now only one. The implementor hierarchy and capability matrix are removed while the client API remains. **Conclusion:** Contraction can preserve value and delete ceremony.

### Example 10

A surgical robot proposes high-level motion modes bridged to interchangeable actuator backends. Not all actuators meet force, timing, calibration, or fail-safe requirements, so generic interchangeability is rejected pending named multidisciplinary evidence. **Conclusion:** Compatibility is a safety case, not an interface checkbox.

## Cross-Program Connections

- **Object-Oriented Programming:** delegation, interface segregation, substitutability, and inheritance shape both axes.
- **Software Design:** information hiding and change drivers determine the abstraction/implementor boundary.
- **Software Architecture:** drivers, platforms, compatibility, binding time, and quality attributes broaden Bridge consequences.
- **Programming Languages:** traits, generics, existential types, modules, and Pimpl offer different realizations.
- **Concurrent Programming:** sharing, affinity, rebinding, and draining require synchronization and ownership.
- **Database Engineering:** stable access abstractions and heterogeneous drivers demonstrate constrained compatibility.
- **Platform Engineering:** runtime selection, deployment versions, capabilities, readiness, and rollback govern binding.
- **Security Engineering:** implementors hold platform capabilities; abstraction contracts should narrow authority.
- **Testing and Quality:** recording fakes, conformance suites, pair tests, and hardware evidence cover different claims.
- **Systems Engineering:** physical backend compatibility depends on units, timing, calibration, and safety invariants.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Bridge intent, participants, structure, and consequences.
2. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), 1972, DOI 10.1145/361598.361623. Grounds decomposition in independent change and information hiding.
3. Bjarne Stroustrup and Herb Sutter, editors, [*C++ Core Guidelines*](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines), rule I.27, accessed 2026-08-28. Documents Pimpl as a technique for stable library ABI and its indirection/allocation costs.
4. Oracle, [`java.sql.Driver`](https://docs.oracle.com/en/java/javase/21/docs/api/java.sql/java/sql/Driver.html), Java SE 21 API, accessed 2026-08-28. Defines the interface implemented by multiple JDBC drivers and selection/connection behavior.
5. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, fourth edition, Addison-Wesley, 2021, ISBN 978-0-13-688609-9. Provides quality-attribute, variability, interface, and architecture tradeoff context.
6. John Lakos, *Large-Scale C++ Software Design*, Addison-Wesley, 1996, ISBN 978-0-201-63362-7. Develops physical design, dependencies, levels, and insulation relevant to implementation boundaries.
7. Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices*, Prentice Hall, 2002, ISBN 978-0-13-597444-5. Provides dependency, interface, and package-design principles for separating reasons to change.

## Exercises

### Exercise 1

Formalize the executable Bridge: enumerate abstraction and implementor sets, all pairs, protocols, and outputs. Identify why the structured output is not production JSON evidence.

### Exercise 2

Given three document policies and four renderer backends with partial capabilities, design the compatibility relation, binding diagnostics, conformance tests, and change procedure.

### Exercise 3

Compare Bridge, Strategy, Adapter, Abstract Factory, and Pimpl for a stable client API over two database engines. State which evidence changes the choice.

### Exercise 4

Design generation-safe runtime rebinding of a shared implementor under concurrent operations, startup failure, rollback, resource limits, and shutdown.

### Exercise 5

An unfamiliar autonomous-drone platform proposes bridging flight modes to swappable actuator/sensor stacks. Produce a graduate-level compatibility and evidence plan without claiming flight safety.

## Answers to the Exercises

### Answer 1

Let \(A=\{CompactReport,DetailedReport\}\) and \(I=\{TextOutput,StructuredOutput\}\). The example treats \(C=A\times I\), giving four pairs. Compact protocol is one `compact(metric,value)` call and ignores unit by declared policy. Detailed protocol is one `detailed(metric,value,unit)` call. Expected representative outputs match the four formatting rules; the assertion covers the fourth pair.

The structured form is not valid general JSON: keys and string values are unquoted, escaping is absent, arbitrary Unicode/control characters are untested, numeric type/range and schema are unspecified, and no JSON parser validates it. Rename it structured text, as the chapter does, or implement a real encoder with an executable parser/schema test. The run also says nothing about localization, concurrent sharing, failures, capability subsets, or independent future evolution.

### Answer 2

Define each document policy's required set—for example text, images, transparency, color profile, accessibility tags, pagination control, and streaming—and each backend's provided set plus limits such as page size, color depth, thread affinity, and maximum resource budget. Pair membership requires set inclusion and limit compatibility, but behavioral contracts may add constraints not expressible as flags.

The root selects a pair from typed deployment configuration, reports every missing capability with policy/backend/version provenance, and performs no output before success. Test policies against recording implementors for legal command sequences; run a shared implementor conformance suite; then choose pair classes by capability profile and test representative plus boundary pairs, including cancellation, partial output, resource cleanup, concurrency, and golden/schema/accessibility validation. Adding a policy changes implementors only if the stable protocol is insufficient; adding a backend runs conformance and compatibility classification without editing policies. A primitive change versions the contract and migration plan.

### Answer 3

Start with one narrow database port and two implementations. This is ordinary dependency inversion or Strategy if one client policy chooses an algorithmic implementation. It becomes Bridge when multiple refined access abstractions and multiple drivers have independent supported evolution and a stable primitive protocol. Adapter is used when an existing database client has an incompatible interface and can implement the port through faithful translation. Abstract Factory is useful if selecting an engine must create a coherent family—connection, transaction, dialect, migration, and type mapper. Pimpl is appropriate when the primary need is C++ ABI/representation insulation with no public implementor family.

Evidence includes actual change history, number and ownership of abstraction/backend variants, compatibility constraints, supported dynamic deployment, ABI commitment, driver performance, transaction/consistency contracts, and test/operational cost. One stable abstraction favors direct port/Strategy; legacy mismatch favors Adapter; coherent product families favor Abstract Factory; cross-product change favors Bridge; one hidden C++ representation favors Pimpl. These mechanisms may compose at owned boundaries.

### Answer 4

Use immutable implementor generations behind an acquisition handle. Build generation \(g+1\) within an overlap capacity budget, validate configuration/capabilities, start it with deadlines, and pass readiness checks. Atomically publish it for new acquisitions; each operation pins its chosen generation and cannot switch mid-protocol. Mark \(g\) draining, reject new acquisitions, await holder count zero to a deadline, then close it exactly once.

If new startup/readiness fails, close its partial resources in reverse and leave \(g\) published. After publication, rollback republishes a still-valid prior or newly rebuilt generation through the same protocol; it never mutates delegates inside existing abstractions. Track generation, holders, start/drain/close, errors, capacity, and rollback. Shutdown stops publication, rejects new work, drains all generations, and reports/handles stragglers by resource policy. Test handoff races, long operations, failed start, failure after publish, capacity exhaustion, repeated rollback, cancellation, and idempotent close.

### Answer 5

Do not model every flight mode–stack pair as valid. Define abstraction requirements per mode: sensor types/rates/latency/accuracy, actuator authority/range/rate, coordinate frames, units, timing jitter, redundancy, failure detection, control-loop stability margins, compute/network budgets, calibration, and fail-safe behavior. Each stack supplies evidence-backed capabilities and limitations. Compatibility is a reviewed relation tied to aircraft hardware, mass/inertia, environment, software/configuration generation, and mission envelope—not runtime interface discovery alone.

Bind only while disarmed at an approved lifecycle boundary. Authenticate configuration and devices, validate calibration and topology, run self-tests, and keep actuation inhibited until the complete safety state is ready. Use generation/epoch fencing; never swap stacks mid-flight through a delegate setter. Independent flight-envelope, actuator, geofence, lost-link, and emergency controls must fail safely if higher-level policy fails. Unknown capability or timing is infeasible, not a default.

Evidence includes requirements/hazard traceability, dimensional analysis, control-theory and stability analysis by qualified engineers, formal/state analysis where tractable, worst-case execution/network timing, sensor/actuator calibration, static analysis and independent code review, simulation across envelope, software/hardware-in-the-loop, fault injection for loss/delay/reorder/stuck/noisy/restart/spoofing, endurance/environmental tests, cybersecurity, human-factors, flight-test progression, and applicable certification. Named aeronautical, flight-controls, embedded/real-time, hardware, functional-safety, cybersecurity, human-factors, operations, test-pilot, quality, regulatory/certification, and independent verification authorities must approve. This chapter and example establish no airworthiness or flight safety.
