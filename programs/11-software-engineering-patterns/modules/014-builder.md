---
module_id: SEPAT-014
program: Software Engineering: Patterns
level: 1
module_number: 14
title: Builder
status: complete
last_verified: 2026-08-28
---

# Builder

## One-Page Review

### Governing question

When should construction become an explicit staged protocol so a complex product can be assembled readably, validated atomically, and returned only when complete?

### Essential definitions

- A **Builder** separates construction of a complex product from its final representation and exposes operations for accumulating construction decisions.
- A **Concrete Builder** implements construction operations and owns intermediate state for one representation.
- A **Product** is the completed result returned only after final validation succeeds.
- A **Director** owns a reusable construction sequence; it is optional when clients legitimately control sequencing.
- A **construction protocol** defines legal operations, ordering, multiplicity, defaults, and finalization.
- A **mandatory field** must be supplied before completion; an **optional field** has an explicit absence or default policy.
- A **cross-field invariant** relates multiple accumulated values and often cannot be checked by individual setters.
- A **fluent interface** returns the builder from configuration operations to support readable chaining; fluency is an API style, not the Builder pattern itself.
- A **typestate builder** encodes some construction states in types so illegal sequences cannot compile.
- **single-use**, **resettable**, and **persistent** builders have different reuse and aliasing contracts.

### Central model, mechanism, or theorem

Model construction as a state machine

$$
B_0\xrightarrow{o_1}B_1\xrightarrow{o_2}\cdots\xrightarrow{o_n}B_n\xrightarrow{build}Result(P,E).
$$

Each operation preserves builder-state invariant (I_B). `build` is permitted only when completion predicate (Complete(B_n)) holds; success requires

$$
build(B_n)=Ok(p)\implies I_P(p)\land corresponds(p,B_n).
$$

Failure returns no partial Product and leaves builder reuse behavior explicit. A Director is correct only if its sequence satisfies the same protocol for every compatible Concrete Builder.

### Critical invariants

- No Product escapes before all mandatory and cross-field invariants hold.
- Every default is explicit, deterministic, and valid in the current context.
- Repeated operations have documented replace, append, merge, or reject semantics.
- The builder owns mutable intermediate state; completed Products do not alias it accidentally.
- Validation errors identify safe actionable causes without leaking secrets.
- Resource acquisition is delayed or cleaned up transactionally if finalization fails.
- Builder reuse, thread safety, cancellation, and ownership are documented.
- A fluent chain never hides illegal ordering or effectful work.

### Common failures

Common failures include using Builder for two obvious constructor arguments, returning a half-built Product, validating fields independently while missing cross-field contradictions, silent last-write-wins behavior, mutable Products sharing builder collections, reusing a single-use builder, calling `build` repeatedly with unclear identity, doing remote I/O in fluent setters, treating a fluent interface as proof of Builder, using telescoping optional methods without required-state enforcement, and allowing a Director to depend on Concrete Product details.

### Compact example

An HTTP request has method, path, headers, and body. Individual setters accumulate values; `build` checks that method and path exist, the path is absolute, and GET has no body. Success returns a Product snapshot. The client can construct GET and POST representations through the same protocol, while a preset Director could encode a health-check request.

### Connections

[SEPAT-013](013-abstract-factory.md) creates coherent families; Builder assembles one complex Product. [SEPAT-015](../ROADMAP.md) copies configured exemplars. Construction-state modeling connects to [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), typestate to [Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md), and validation to [Software Engineering: Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

What construction complexity justifies a stateful protocol rather than one constructor, named creation function, parameter object, or factory?

Builder earns its cost when a Product has many optional or repeated parts, staged input, multiple representations, cross-field validation, or a reusable construction sequence. It converts a long ambiguous call into named decisions and reserves Product publication for an atomic completion point.

The pattern is not synonymous with method chaining. A builder can use ordinary commands; a fluent API can mutate an already valid Product or describe a query. Analyze lifecycle and invariants before terminology.

## Why This Matters

Complex construction concentrates defects. Optional arguments are swapped, required fields are omitted, incompatible settings are combined, mutable input leaks into an allegedly immutable Product, and resource failure leaves partial state. A builder can make these states explicit and testable.

Builder also separates construction sequence from representation. A parser or Director can issue `start_section`, `add_item`, and `finish_section` to builders producing an object tree, text, or events. The sequence is reused without coupling to concrete output.

The cost is another stateful object and protocol. Poor builders merely move constructor complexity into time, creating more invalid intermediate states. Production-grade use specifies the state machine, error semantics, ownership, and reuse.

## Prerequisites and Retrieval

You should understand constructors, mutable and immutable values, state machines, exceptions or result types, and creational patterns. Retrieve these facts:

1. An object can be invalid during assembly even if each field value is locally valid.
2. Cross-field constraints need an atomic view of accumulated state.
3. Mutable collection references can violate completed Product immutability.
4. Fluent return values do not define construction semantics.
5. A reusable sequence and a configurable Product are separate variation axes.
6. Resource acquisition adds rollback, cancellation, and ownership obligations.

## Learning Objectives

After completing this module, you should be able to:

- distinguish Builder from constructors, parameter objects, factories, Abstract Factory, and fluent interfaces;
- specify builder states, legal operations, repetition, defaults, and completion;
- enforce mandatory and cross-field invariants at the appropriate boundary;
- design immutable Product snapshots without alias leakage;
- choose client-driven, Director-driven, and typestate variants;
- define single-use, reusable, and persistent semantics;
- test construction sequences, invalid states, cleanup, and concurrency;
- refactor away from Builder when construction becomes simple.

## Core Exposition

### Start from construction pressure

A constructor with ten same-typed arguments is hard to read. A document assembled from a parse stream cannot exist all at once. A deployment plan has optional probes, repeated routes, and cross-field constraints. These are distinct forces that can support Builder.

Do not count parameters mechanically. A value with three required coordinates is clearer as a constructor. A parameter object can solve naming without introducing staged mutable state.

### Define the Product boundary

The Product should become observable only after successful finalization. Decide whether it is immutable, owns resources, or has a later lifecycle. The builder may hold incomplete data; ordinary Product methods should never encounter that state.

Copy mutable collections or transfer ownership irreversibly during `build`. If Product and builder share a list, a later builder call can mutate a published Product.

### Specify the protocol

For every operation state preconditions, effect, repetition, and error. `header(name,value)` might append duplicate HTTP fields, replace by normalized name, or reject duplicates. Each behavior is valid in some domain; silence is not.

Ordering can matter. A streaming archive builder may require `begin_entry` before bytes and `end_entry` before another entry. Represent the ordering as a state machine and reject invalid transitions close to their source.

### Validate locally and globally

Reject a negative timeout when supplied. Delay cross-field checks—start before end, mutually exclusive authentication modes, GET with body—until enough information exists. `build` performs complete validation and returns all useful safe errors when practical.

Do not let defaults bypass validation. A context-dependent default such as production region, encryption suite, or clinical unit must come from an explicit policy, not ambient global state.

### Director is optional

The GoF structure includes a Director that applies a construction sequence to a Builder. Use it when named recipes recur or an input processor owns order. A `HealthCheckRequestDirector` may configure a known request while different builders produce wire, test, or documentation representations.

When each caller owns a unique configuration, the client can direct the builder. Adding a ceremonial Director that forwards every method creates no separation.

### Multiple representations

A construction protocol can drive an object graph, serialized form, validation report, or test double. Each Concrete Builder must interpret operations coherently. If operations expose representation-specific concepts, the abstraction is false.

Representation may affect what can be streamed. An in-memory tree can backtrack; a network writer may not. The common protocol must honor the strictest ordering or declare capabilities.

### Fluent interfaces

Fluent methods can make a construction sentence readable, especially when names reflect domain grammar. They also obscure mutation, encourage long chains with poor error locations, and can mix queries and commands.

Return `self` only when it improves the whole expression. Provide useful error context, formatting, and discoverability. Do not make setters perform invisible remote acquisition merely to preserve fluency.

### Typestate builders

A typestate builder represents states such as `MissingMethod`, `MissingPath`, and `Ready` with distinct types. Only `Ready` exposes `build`. This moves some errors to compile time and documents order.

The number of types can grow combinatorially when many independent optional fields exist. Use typestate for safety-critical ordering or a few essential transitions, and runtime validation for data-dependent invariants.

### Reuse semantics

A single-use builder consumes itself on successful `build`; this best prevents aliasing and accidental reuse. A resettable builder clears to a documented initial state. A persistent builder returns a new builder for every operation and shares immutable structure safely.

If repeated `build` calls are allowed, specify whether they return equal snapshots, the same object, or incrementally different Products. Thread safety follows from these choices, not from the pattern name.

### Resource-producing builders

Prefer building a configuration Product, then acquiring resources separately. If finalization must acquire files, sockets, GPU memory, or transactions, `build` owns every partial resource until success and releases on failure or cancellation.

Setters should normally remain cheap and deterministic. This makes retries, validation, and tests tractable.

### Evolution

Adding an optional operation can preserve old clients if its default is valid. Adding a mandatory field changes the completion protocol. Version builders and serialized recipes carefully; old Directors may otherwise produce invalid Products.

When Product construction simplifies, replace Builder with a constructor or named creation function. Do not retain an API of `with_x().build()` around one required value.

## Definitions and Notation

Let builder state be (B=(q,d)), with protocol state (q\in Q) and accumulated data (d). Each operation (o) is a partial transition

$$
\delta_o:Q\times D\rightharpoonup Q\times D.
$$

Illegal operations are outside the domain and must produce a defined error rather than corrupt state. Completion states are (Q_F\subseteq Q). Finalization is

$$
build:B_F\to Result(P,E),\qquad B_F=Q_F\times D_{valid}.
$$

For immutable Product snapshot (p) and mutable builder state after completion (B'), non-aliasing requires

$$
mutate(B')\not\Rightarrow mutate(p).
$$

A Director sequence (s=o_1\cdots o_n) is compatible with a Concrete Builder when every prefix transition is defined and the terminal state belongs to (B_F). This is a protocol claim, not proof that the resulting domain Product is universally correct.

## Mechanisms, Invariants, or Proof Structure

### Identify states and completion

List missing required data, ordered phases, repeatable parts, defaults, and cross-field constraints. Define when Product publication is legal.

### Accumulate without leaking

Keep intermediate state private. Copy or transfer mutable data at completion and prevent ordinary clients from observing partial Product state.

### Finalize atomically

Validate the full snapshot, acquire resources transactionally if unavoidable, and return either one valid Product or bounded errors.

### Verify a compact request builder

The executable example creates two valid requests and rejects one invalid cross-field combination.

<!-- bijux-verify: {"id":"validated-request-builder","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"GET /health headers=accept:application/json body=0\nPOST /events headers=content-type:text/plain body=5\ninvalid: GET request cannot have a body\n","stderr":""}} -->
```python
class Request:
    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = path
        self.headers = tuple(headers)
        self.body = body

    def summary(self):
        header_text = ",".join(f"{name}:{value}" for name, value in self.headers)
        return (
            f"{self.method} {self.path} headers={header_text} "
            f"body={len(self.body)}"
        )


class RequestBuilder:
    def __init__(self):
        self.method = None
        self.path = None
        self.headers = []
        self.body = ""

    def with_method(self, method):
        self.method = method
        return self

    def with_path(self, path):
        self.path = path
        return self

    def add_header(self, name, value):
        self.headers.append((name, value))
        return self

    def with_body(self, body):
        self.body = body
        return self

    def build(self):
        if self.method not in {"GET", "POST"}:
            raise ValueError("method must be GET or POST")
        if not self.path or not self.path.startswith("/"):
            raise ValueError("path must be absolute")
        if self.method == "GET" and self.body:
            raise ValueError("GET request cannot have a body")
        return Request(self.method, self.path, self.headers, self.body)


health = (
    RequestBuilder()
    .with_method("GET")
    .with_path("/health")
    .add_header("accept", "application/json")
    .build()
)
event = (
    RequestBuilder()
    .with_method("POST")
    .with_path("/events")
    .add_header("content-type", "text/plain")
    .with_body("ready")
    .build()
)
print(health.summary())
print(event.summary())

try:
    RequestBuilder().with_method("GET").with_path("/x").with_body("bad").build()
except ValueError as error:
    print(f"invalid: {error}")
```

The run proves three selected paths. It does not establish HTTP standards compliance, header normalization, security, Unicode byte length, immutability of every field, or safe network transmission.

### Test the protocol surface

Cover every operation in every legal state, invalid transitions, repeated calls, defaults, complete cross-field partitions, failure state, aliasing, reuse, concurrency, and cancellation.

### Compare simpler alternatives

If named parameters or one validated creation function express the Product clearly, remove the staged protocol.

## Alternatives and Trade-Offs

**Constructor with named parameters.** Simple and atomic. It becomes unwieldy with repeated parts, staged input, or many optional values.

**Parameter object.** Names configuration without mutable sequencing. It may itself need validation or construction help.

**Named creation function.** Encapsulates one complete recipe. It does not expose client-controlled staged variation.

**Builder.** Makes complex construction readable and validates at completion. It adds mutable state, protocol, and possible aliasing.

**Typestate builder.** Prevents selected illegal sequences statically. It increases type/API complexity and cannot encode every data invariant.

**Abstract Factory.** Creates related separate Products. Builder assembles one Product, though a factory can create builders.

**Prototype.** Starts from a configured exemplar and copies it. Builder starts from explicit construction state.

**Fluent Product API.** Convenient when every intermediate Product is valid. It risks mixing construction and normal mutation.

## Failure Modes and Misconceptions

1. **Fluent chaining means Builder.** Fluency is syntax; staged Product construction is the mechanism.
2. **Every long constructor needs Builder.** Named parameters or a parameter object may be smaller.
3. **Setters guarantee validity.** Cross-field and completion invariants remain.
4. **`build` can return a partial Product.** Publication must be atomic or incompleteness explicit in the type.
5. **Last write always wins.** Repetition semantics must follow the domain.
6. **Products may share builder collections.** Later builder mutation can corrupt published state.
7. **Builders are reusable by default.** Single-use, reset, persistent, and repeated-build behavior differ.
8. **Fluent setters may hide I/O.** Effects, deadlines, cancellation, and cleanup must be visible.
9. **A Director is mandatory.** It is useful only for reusable sequences or external construction ownership.
10. **Builder is permanent API.** Contract it when Product construction becomes simple.

## Worked Examples

### Example 1

**Question:** What does the executable builder verify?

**Reasoning:** It accumulates required and optional data, snapshots headers into a tuple, accepts GET without body and POST with body, and rejects one cross-field violation.

**Conclusion:** Completion validation and snapshotting are visible, but the HTTP claim is tightly bounded.

### Example 2

**Question:** Builder or named parameters for a rectangle?

**Reasoning:** Width and height are required and atomic; a constructor with named arguments is clearer. A builder adds invalid missing-dimension states.

**Conclusion:** Simple required values do not justify staged construction.

### Example 3

**Question:** Why build an immutable deployment plan?

**Reasoning:** Routes, probes, resources, and rollout policy accumulate from several sources. Finalization checks unique routes, resource bounds, and rollout/probe compatibility, then freezes collections.

**Conclusion:** Repeated parts plus cross-field validation support Builder.

### Example 4

**Question:** When is a Director useful for documents?

**Reasoning:** A parser owns the sequence of headings, paragraphs, and links while object-tree and HTML builders produce different representations. The parser does not inspect their Products.

**Conclusion:** Reusable sequence and variable representation justify Director plus Builder.

### Example 5

**Question:** What should duplicate headers do?

**Reasoning:** Some fields permit repetition; others require combination or rejection. The builder needs normalized names and field-specific policy rather than accidental append.

**Conclusion:** Repetition semantics are part of the construction contract.

### Example 6

**Question:** When does typestate pay for itself?

**Reasoning:** A cryptographic session must select an approved algorithm and key before accepting plaintext. A small set of ordered safety states can prevent misuse at compile time.

**Conclusion:** Encode critical protocol order, not every optional combination.

### Example 7

**Question:** Can `build` acquire a database connection?

**Reasoning:** It can, but then it needs deadline, cancellation, classified failure, and exact cleanup of partial resources. Building immutable connection configuration first is often safer.

**Conclusion:** Separate configuration construction from resource acquisition where practical.

### Example 8

**Question:** How should repeated `build` behave?

**Reasoning:** A persistent builder may return equal independent snapshots; a consuming builder rejects reuse. Returning Products that share mutable lists is unsafe.

**Conclusion:** Identity and reuse semantics must be deliberate and tested.

### Example 9

**Question:** How does Builder differ from Abstract Factory?

**Reasoning:** Abstract Factory returns separate compatible role Products from one family. Builder accumulates steps into one Product. An Abstract Factory may create family-specific builders.

**Conclusion:** Family selection and staged assembly are orthogonal forces.

### Example 10

**Question:** When should Builder be removed?

**Reasoning:** If evolution leaves one required field and one stable optional default, replace the mutable builder with a validated named constructor and migrate callers.

**Conclusion:** Remove construction protocol when it no longer protects meaningful complexity.

## Cross-Program Connections

- **Object-Oriented Programming:** encapsulation separates invalid intermediate state from valid Product behavior.
- **Systems Programming:** typestate, ownership, and RAII strengthen ordered resource construction.
- **Functional Programming:** persistent builders and folds assemble Products without shared mutation.
- **Programming Languages:** named arguments, records, algebraic data types, and dependent types change applicability.
- **Software Design:** parameter objects, immutability, and information hiding are close alternatives and complements.
- **Testing & Quality Engineering:** state-machine and property tests cover construction protocols systematically.
- **Security Engineering:** safe defaults, secret hygiene, and fail-closed completion constrain configuration builders.
- **Cloud Engineering:** deployment, request, and client configuration commonly require repeated parts and validation.
- **Database Engineering:** query builders must distinguish structured construction from unsafe string concatenation.
- **Human-Computer Interaction:** readable APIs and actionable validation errors affect developer usability.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Builder intent, participants, collaborations, consequences, and implementation discussion.
2. Joshua Bloch, [*Effective Java*, 3rd ed.](https://www.pearson.com/en-gb/subject-catalog/p/effective-java/P200000000138), Addison-Wesley, 2018. Develops Builder as an alternative to telescoping constructors and JavaBeans for complex object construction.
3. Martin Fowler, [“Construction Builder”](https://martinfowler.com/dslCatalog/constructionBuilder.html), accessed 2026-08-28. Describes incremental creation of immutable objects through stored constructor arguments.
4. Martin Fowler, [“Fluent Interface”](https://martinfowler.com/bliki/FluentInterface.html), 2005, accessed 2026-08-28. Defines fluent API intent and its design cost, clarifying that fluency is not identical to Builder.
5. Martin Fowler, [“Expression Builder”](https://martinfowler.com/dslCatalog/expressionBuilder.html), accessed 2026-08-28. Separates a fluent expression layer from a conventional command-query API.
6. Eric Evans, [*Domain-Driven Design: Tackling Complexity in the Heart of Software*](https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217), Addison-Wesley, 2003. Supplies valid aggregate construction, lifecycle, and domain-language context.

## Exercises

### Exercise 1

Specify the executable RequestBuilder as a state machine, including every operation, repetition policy, completion state, error, aliasing rule, and reuse decision.

### Exercise 2

Extend the request design with query parameters and duplicate header semantics. Define deterministic encoding and list at least twelve partitions that the current run does not verify.

### Exercise 3

Design a typestate builder for an encrypted message requiring algorithm, key, and plaintext before completion. Separate statically enforceable order from runtime policy checks.

### Exercise 4

Refactor a mutable builder whose `build` opens a socket into configuration construction plus explicit acquisition. Preserve errors, deadlines, ownership, observability, and caller behavior.

### Exercise 5

An unfamiliar implantable-device platform builds treatment programs from staged clinical parameters. Produce a graduate-level Builder design covering units, ordering, cross-field invariants, immutable output, provenance, concurrency, evidence, rollback, and human authorization.

## Answers to the Exercises

### Answer 1

States track method absent/present, path absent/present, and accumulated headers/body. `with_method` replaces once or rejects a second call; choose and document one—production design should reject conflicting replacement. `with_path` likewise. `add_header` appends under field-aware duplicate policy. `with_body` replaces only if the API states that explicitly. Completion requires allowed method and absolute path; GET plus nonempty body is invalid.

Errors distinguish missing/unsupported method, missing/nonabsolute path, invalid header, duplicate conflict, and method/body contradiction. `build` returns a Product snapshot with copied immutable header storage. A single-use design consumes the builder on success and rejects all later operations and repeated `build`; failure leaves it inspectable but not silently repaired unless the protocol permits correction. The example currently permits reuse, so a durable implementation must tighten or document that behavior. It is not thread-safe.

### Answer 2

Represent query parameters as ordered key/value pairs or a multimap with a documented canonical sort. Percent-encode names and values under a specified character encoding; never concatenate raw input. Define which HTTP headers may repeat, which combine in order, and which reject duplicates after case-insensitive normalization. Product output preserves the declared canonical policy.

Unverified partitions include missing method, unsupported method, missing path, relative path, empty path, fragment, existing query, empty name/value, repeated query key, reserved characters, spaces, Unicode, invalid surrogate/input encoding, duplicate case-variant header, appendable header, forbidden duplicate, control-character injection, GET body, empty POST body, large body, mutable input alias, repeated build, builder reuse, and concurrent calls. Wire-byte length differs from character count and requires separate evidence.

### Answer 3

Use types `NeedAlgorithm`, `NeedKey<A>`, `NeedPlaintext<A,K>`, and `Ready<A,K>`. Selecting an algorithm transitions to the key state parameterized by algorithm family; supplying a structurally compatible key transitions to plaintext; adding plaintext produces Ready; only Ready exposes `build`. The API prevents omission and gross order errors.

Runtime checks still enforce approved algorithm policy, key provenance/revocation, key size and usage, nonce uniqueness, plaintext bounds, associated-data rules, provider availability, and authorization. Construction returns an immutable encryption request, not ciphertext, unless effectful finalization has explicit deadline, failure, and secret-cleanup contracts. Typestate does not prove cryptographic security or policy approval.

### Answer 4

Define immutable `ConnectionConfig` built from endpoint, TLS policy, authentication reference, timeouts, and proxy settings. Its builder performs syntax and cross-field validation without I/O and snapshots secret handles rather than secret bytes. Replace effectful `build` with `build_config`. Add explicit async `connect(config, deadline, cancellation)` at the infrastructure boundary.

Map old errors to classified configuration versus acquisition failures, preserving caller-visible behavior through an adapter during migration. `connect` owns DNS, socket, TLS, and authentication resources until success; every failure/cancellation closes partial state exactly once. Propagate one deadline, record safe stage/duration telemetry, and transfer one closable connection on success. Characterization, fault injection after every stage, leak checks, timeout/cancel races, and compatibility tests prove the bounded migration before removing the old method.

### Answer 5

Define typed stages for patient/treatment identity, approved device/calibration family, dosage or stimulation parameters with explicit units, timing envelope, delivery sequence, monitoring limits, and clinician attestations. Normalize units at entry while retaining source value, unit, author, device, timestamp, and rule-set provenance. Reject duplicate/conflicting settings by policy; never silently overwrite a safety-relevant value.

Cross-field invariants cover device capability, calibration version, patient-specific bounds, rate-times-duration totals, sequence order, mutually exclusive modes, monitoring thresholds stricter than delivery limits, and temporal validity of approvals. `build` runs a versioned deterministic ruleset and produces a signed immutable program plus complete provenance and validation report, or bounded errors with no executable partial program. Builder collections cannot alias the Product. Use one builder per authorized session; no concurrent mutation or reuse after signing.

Evidence includes unit/property and state-machine tests, boundary-value analysis, independent recomputation, dimensional analysis, formal invariant review where tractable, simulation, hardware-in-the-loop, fault injection, provenance verification, concurrency rejection, and audit/replay. Deployment verifies signature, patient/device/calibration binding, expiry, and exact ruleset; rollback selects a previously approved compatible program only at a safe clinical boundary and never a revoked calibration. Named clinicians, safety engineers, medical physicists or domain specialists, security, regulatory, device, verification, and operations reviewers must authorize the program and platform. Repository validation grants no treatment authority.
