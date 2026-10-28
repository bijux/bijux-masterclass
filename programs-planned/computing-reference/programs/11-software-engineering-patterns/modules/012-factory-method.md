---
module_id: SEPAT-012
program: Software Engineering: Patterns
level: 1
module_number: 12
title: Factory Method
status: complete
last_verified: 2026-08-28
---

# Factory Method

## One-Page Review

### Governing question

When should a creator preserve an algorithm while delegating one product-construction decision to subclasses or equivalent override points?

### Essential definitions

- **Factory Method** is the GoF creational pattern in which a creator declares a product-creation operation and derived creators decide which concrete product supplies that role.
- The **Creator** owns stable workflow that uses a product through a contract.
- A **Concrete Creator** overrides the factory method to construct a compatible Concrete Product.
- The **Product** contract is the behavior required by the creator workflow; a **Concrete Product** implements it.
- An **extension point** is the controlled variation point represented by the creation operation.
- **deferred binding** means the concrete product choice is made by the selected concrete creator rather than hard-coded in the base workflow.
- A **hook method** customizes a step of an algorithm; a factory method is a hook specifically responsible for product creation.
- A **parallel hierarchy** occurs when each creator subtype corresponds to a product subtype; it can clarify paired variants or multiply classes mechanically.
- A **parameterized factory method** accepts a discriminant and may create several products, combining override and key-based selection.

### Central model, mechanism, or theorem

Let Creator workflow (T) call creation operation (m) and use only Product contract (P):

\[
T_C(x)=use_P(m_C(x),x).
\]

Each Concrete Creator (C_i) supplies (m_{C_i}:X\to P_i) with (P_i\preceq P). Correct substitution requires the returned product satisfy every precondition, postcondition, invariant, effect, ownership, and failure assumption used by (T). Variation is localized to creation; if subclasses must replace most of (T), the pattern boundary is misplaced.

### Critical invariants

- The creator's stable workflow depends only on the Product contract.
- Every override returns a fully valid substitutable product.
- Creation is invoked only when subclass state required by the override is initialized.
- Ownership, failure, side effects, and lifetime remain compatible across products.
- The extension point is narrow; concrete creators do not duplicate the stable workflow.
- Product-specific branching does not leak back into Creator clients.
- Creator selection remains explicit at a composition boundary.
- The subclass hierarchy is removed or replaced when inheritance no longer carries meaningful variation.

### Common failures

Common failures include calling any object-returning function Factory Method, confusing it with a static factory or simple switch, invoking overridable creation from a base constructor, returning products with incompatible error or ownership semantics, overriding the whole workflow instead of creation, mirroring every product with a needless creator subclass, hiding creator selection in globals, adding parameters until the factory method becomes another universal switch, and forcing inheritance where a passed creation function would be simpler.

### Compact example

A report job owns `run`: create formatter, format the record, attach delivery metadata. `JsonReportJob` and `LinesReportJob` override only `make_formatter`. The workflow is inherited unchanged and sees one formatter contract. If runtime configuration rather than creator subtype chooses the format, injecting a creation function or using a simple factory is likely clearer.

### Connections

[SEPAT-011](011-simple-factory-and-creation-functions.md) provides direct and key-based creation baselines. [SEPAT-013](../ROADMAP.md) creates related families; [SEPAT-020](../ROADMAP.md) studies Template Method, whose algorithm hooks often include factory methods. Substitution connects to [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), dependency design to [Software Engineering: Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), and behavior contracts to [Software Engineering: Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

What forces justify coupling product creation to creator subtype while keeping the creator's product-using workflow stable and verifiably substitutable?

Factory Method is not merely “put `new` in a method.” Its value comes from a relationship: the base creator knows when and how a product participates, while a derived creator knows which compatible product to supply. The product decision varies along the same axis as creator specialization.

The inheritance is a cost. If the only goal is to avoid importing a concrete type, an injected function or simple factory usually provides less structure. Factory Method earns its place when creator polymorphism already exists or subclass-controlled construction coherently completes the creator role.

## Why This Matters

Frameworks often own control flow while applications supply components. A document framework owns opening, parsing, editing, and saving; an application subtype supplies the document. A test harness owns setup and execution; a specialized fixture creates the system under test. Factory Method gives the framework a narrow construction hook without exposing the whole algorithm.

Used well, it protects a stable workflow from concrete products. Used mechanically, it produces parallel hierarchies, subclass explosion, fragile initialization, and obscure selection. Correctness depends on behavioral product contracts, not only a common base class.

The pattern also teaches a broader design principle: separate who owns the algorithm from who owns one variable collaborator. Later patterns generalize or replace the inheritance mechanism.

## Prerequisites and Retrieval

You should understand inheritance, overriding, dynamic dispatch, contracts, constructors, creation functions, and dependency inversion. Retrieve these facts:

1. An override is selected from the runtime creator type.
2. Subtype compatibility includes behavior, effects, errors, and ownership—not only method signatures.
3. Base construction may run before derived state is initialized.
4. An abstract operation forces subclasses to provide behavior; a default operation allows optional override.
5. Composition can parameterize behavior without subclassing.
6. Stable workflow and variable creation must vary on genuinely different rates or ownership axes.

## Learning Objectives

After completing this module, you should be able to:

- identify Creator, factory method, Product, Concrete Creator, and Concrete Product roles;
- distinguish Factory Method from simple factory, static factory, Abstract Factory, and arbitrary creation helpers;
- derive the pattern from creator-owned workflow and subtype-owned product selection;
- specify behavioral, effect, failure, and ownership contracts for product substitution;
- choose abstract, default, and parameterized factory-method variants;
- avoid unsafe virtual calls during construction;
- test creators with a shared product contract suite;
- refactor between Factory Method and injected creation functions as forces change.

## Core Exposition

### The collaboration, not the spelling

Names differ across languages: `create_document`, `new_product`, `make`, or an overridable property. The collaboration defines the pattern. A stable Creator operation invokes a dynamically selected creation operation and consumes the result through a Product contract.

A static `Widget.of(config)` may be excellent creation design but has no Concrete Creator override. A function switch from key to type is a simple factory. Precision matters because their extension, testing, and coupling consequences differ.

### Derive it from workflow ownership

Start with a workflow that is stable across variants: load input, create parser, parse, validate, report; or open application, create document, register, display. Product choice changes with creator specialization, but the surrounding sequence and invariants remain.

Extract direct construction into a protected or abstract factory method. Replace concrete use with the Product contract. Move only the selection/construction decision to Concrete Creators. If each subclass duplicates the workflow, extraction has failed.

### Creator and Product contracts

The Product contract must include every observation the Creator relies on: callable operations, accepted inputs, outputs, failure classes, idempotency, ordering, latency class, thread safety, resource ownership, and shutdown. A subtype returning the correct interface but blocking indefinitely violates the workflow's deadline assumption.

Creator invariants cover call order and multiplicity. Does it call the factory once per workflow, lazily, or repeatedly? May it retain the product? Can a product refer back to the Creator? These choices affect lifetime and cycles.

### Abstract versus default creation

An abstract factory method forces every concrete creator to choose a product. This fits when no safe universal product exists. A default implementation supplies a common product while allowing specialization, reducing subclasses but risking accidental inheritance of an unsuitable default.

Document the default's applicability. Prefer explicit override when silently selecting the default could violate security, persistence, or compatibility.

### Parameterized factory methods

A factory method can accept a product kind. The base creator may handle common kinds while subclasses extend or replace selection. This supports multiple creation sites but mixes two axes: creator subtype and key.

Define whether unknown keys delegate to the base, fail, or use a default. Uncoordinated fall-through can create surprising products. If a growing switch dominates the method, use a closed simple factory, registry, or Abstract Factory as forces indicate.

### Creator selection remains a decision

Factory Method defers product choice to Concrete Creator, but something still selects the creator. Put that decision at a composition root, framework registration point, or explicit caller. Do not conceal it behind global state.

If runtime key selection chooses among creator subclasses merely to obtain products, the hierarchy may be redundant: select products directly with a factory function.

### Initialization hazards

Avoid invoking overridable methods from a base constructor. Dynamic dispatch may reach a Concrete Creator before its fields exist, producing invalid configuration or resource acquisition. Construct the full creator first, then call the stable workflow or a separate initialization operation.

Some languages suppress dynamic dispatch during construction; others permit it with different rules. The durable invariant is that factory-method preconditions must hold before invocation.

### Product ownership and effects

Specify whether the Creator owns a fresh product, borrows it, or shares it. If one override returns a new closable stream and another a shared singleton, the base workflow cannot release both correctly without a richer contract.

Creation failures should be compatible. Subclasses may refine diagnostics, but the Creator must know whether to retry, compensate, propagate, or abort. Secret-bearing configuration never belongs in generic error text.

### Parallel hierarchies

Parallel creator/product families can be coherent: each operating-system dialog creates its matching button, or each storage job creates a corresponding transaction. They become brittle when every new product demands a creator subclass containing only one return statement.

Audit whether variation truly belongs to creator subtype. Abstract Factory handles coherent product families; a creation-function field handles independent product substitution; registration handles external extension.

### Test the protocol

Test the stable workflow once against a controllable product double to verify call order, inputs, retention, failures, and cleanup. Run a shared Product contract suite against every Concrete Product. Then test each Concrete Creator returns the intended product with compatible configuration.

Avoid assertions on private method dispatch when public workflow behavior suffices. Test the extension boundary directly when its contract is part of subclass API.

### Refactor away when needed

If creator subclasses differ only in the factory method and subtype selection is configuration-driven, replace the override with an injected creation callable. The base workflow becomes one concrete class parameterized by a function. This retains separation without inheritance.

Conversely, when a framework already specializes creators and a repeated product choice follows each subtype, extracting Factory Method can remove duplication safely.

## Definitions and Notation

Let creator types be (C_i\preceq C), product types (P_i\preceq P), stable workflow (T), and factory method (m). Dynamic dispatch gives

\[
m(c_i,x)=m_i(x)\in P_i.
\]

The base workflow is

\[
T(c_i,x)=U(m(c_i,x),x),
\]

where (U) uses only Product contract (P). Behavioral compatibility requires, for Creator-reachable inputs (X_T),

\[
pre_T(x)\implies post_P(m_i(x),x)\land effects_i(x)\subseteq effects_T(x).
\]

For ownership mode (o) expected by (T),

\[
ownership(m_i(x))=o
\quad\forall i,
\]

unless the Product contract exposes a uniform lease or release abstraction. If the workflow calls (m) exactly once, a valid override must not rely on repeated creation to establish invariants.

These conditions specify review obligations; ordinary type checking rarely proves all of them.

## Mechanisms, Invariants, or Proof Structure

### Locate stable workflow and variable product

Show that surrounding control, policy, and observations remain shared while product selection follows creator specialization.

### Define Product behavior first

State operations, effects, errors, timing, concurrency, ownership, and cleanup. Concrete return types alone are insufficient.

### Extract one creation hook

Make the workflow call the factory method at a safe lifecycle point. Choose abstract or documented default behavior.

### Override without duplicating workflow

The executable example has two creators sharing `run` and varying only `make_formatter`.

<!-- bijux-verify: {"id":"report-job-factory-method","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"json-job: {\"id\":7,\"state\":\"ready\"}\nlines-job: id=7|state=ready\n","stderr":""}} -->
```python
class JsonFormatter:
    def format(self, record):
        return f'{{"id":{record["id"]},"state":"{record["state"]}"}}'


class LinesFormatter:
    def format(self, record):
        return "|".join(f"{key}={record[key]}" for key in sorted(record))


class ReportJob:
    def make_formatter(self):
        raise NotImplementedError("concrete creator must supply a formatter")

    def run(self, record):
        formatter = self.make_formatter()
        return formatter.format(record)


class JsonReportJob(ReportJob):
    def make_formatter(self):
        return JsonFormatter()


class LinesReportJob(ReportJob):
    def make_formatter(self):
        return LinesFormatter()


record = {"state": "ready", "id": 7}
print(f"json-job: {JsonReportJob().run(record)}")
print(f"lines-job: {LinesReportJob().run(record)}")
```

This run confirms two finite dispatch paths and exact output for one record. It does not prove arbitrary serialization, substitution under every effect, or safe base-constructor dispatch.

### Verify shared and variant behavior

Use one workflow suite, a Product contract suite for every product, and creator-specific selection tests. Add failure, ownership, concurrency, and lifecycle cases.

### Reassess inheritance cost

Compare an injected creation function. Retain Factory Method only when creator subtype is a meaningful owner of the choice.

## Alternatives and Trade-Offs

**Direct construction.** Clear and local for one stable product. It couples shared workflow to a concrete type.

**Creation function or simple factory.** Supports key-based or explicit selection without creator subclasses. It does not align product choice with creator polymorphism automatically.

**Injected callable.** Parameterizes one workflow instance flexibly and simplifies tests. It may lose a named subtype that carries other coherent creator policy.

**Factory Method.** Gives a framework or base creator a narrow subclass hook. It adds inheritance, lifecycle hazards, and possible hierarchy proliferation.

**Abstract Factory.** Produces multiple related products under one family contract. It is heavier when the workflow needs one product role.

**Template Method with hooks.** Varies several algorithm steps. Too many hooks weaken the claim that workflow is stable.

**Registry.** Allows external providers without modifying a selector. It adds trust, collision, version, and lifecycle obligations.

## Failure Modes and Misconceptions

1. **Any method that creates is Factory Method.** Dynamic creator-controlled override is the distinguishing collaboration.
2. **Static factory method is the GoF pattern.** Static association alone provides no Concrete Creator dispatch.
3. **Returning the Product type proves substitutability.** Effects, failures, ownership, latency, and invariants also matter.
4. **Call the hook from the base constructor.** Derived state may be uninitialized.
5. **Override the entire operation.** This duplicates workflow and defeats the narrow extension point.
6. **One creator subclass per product is always clean.** Parallel hierarchies can become mechanical class inflation.
7. **A default product is always safe.** Silent defaults can violate context-specific security or compatibility.
8. **Factory Method eliminates selection.** Another boundary still chooses the Concrete Creator.
9. **Parameters can grow without changing the pattern.** A universal switch signals mixed variation axes.
10. **Inheritance must be permanent.** Injected creation can preserve the useful separation after creator subtypes lose meaning.

## Worked Examples

### Example 1

**Question:** Why is the executable design Factory Method rather than simple factory?

**Reasoning:** `ReportJob.run` owns stable use; dynamic dispatch on the Concrete Creator selects `make_formatter`. No key switch in one function chooses both products.

**Conclusion:** The creation decision follows creator subtype.

### Example 2

**Question:** Should an application subtype create its document?

**Reasoning:** If the framework owns document lifecycle and each application specialization owns one compatible document subtype, `create_document` is a coherent hook. Document behavior and ownership must match framework assumptions.

**Conclusion:** Framework-owned workflow plus application-owned product is a canonical force.

### Example 3

**Question:** Is `Money.from_minor_units` Factory Method?

**Reasoning:** It is a valuable named or static creation operation, but no Creator hierarchy defers construction to a Concrete Creator override.

**Conclusion:** Creation terminology should describe mechanism, not merely return type.

### Example 4

**Question:** Abstract or default factory method?

**Reasoning:** Use abstract when every platform must choose explicitly and a wrong default is unsafe. Use a default when one product is correct for most creators and specialization is optional and tested.

**Conclusion:** Default safety and subclass burden determine the variant.

### Example 5

**Question:** Why avoid the factory hook in a base constructor?

**Reasoning:** A Concrete Creator may require endpoint, schema, or policy fields initialized only after the base constructor runs. Dynamic dispatch can observe absent state or acquire resources before ownership is ready.

**Conclusion:** Invoke override points only after their preconditions hold.

### Example 6

**Question:** Can two products share a type but violate the Creator?

**Reasoning:** Yes. One formatter may mutate records, perform network I/O, or require closing while the other is pure. The nominal method matches, but effect and ownership contracts differ.

**Conclusion:** Product substitutability is behavioral and operational.

### Example 7

**Question:** When does a parameterized factory method become awkward?

**Reasoning:** If subclasses interpret dozens of keys, fall through inconsistently, and duplicate switches, two variation axes are entangled. Centralize closed selection or use family/registry mechanisms.

**Conclusion:** Keep the override focused on creator-owned variation.

### Example 8

**Question:** Does Factory Method require class inheritance in every language?

**Reasoning:** The GoF form uses creator subclassing. Languages can reproduce deferred creation through records of functions, traits, prototypes, or module functors, but the trade-offs and terminology should state the actual dispatch mechanism.

**Conclusion:** Preserve the collaboration while respecting language semantics.

### Example 9

**Question:** How should a product-creation failure affect the workflow?

**Reasoning:** The Creator defines whether failure aborts, retries, falls back, or compensates. Overrides return compatible classified failures and clean partial resources; they cannot silently substitute an unsafe default.

**Conclusion:** Failure behavior belongs to the extension contract.

### Example 10

**Question:** When should creator subclasses become an injected callable?

**Reasoning:** If subclasses differ only by one return statement and callers select them from runtime configuration, one `ReportJob(make_formatter)` expresses the same variability with fewer types. Preserve subclasses only if they own additional cohesive policy.

**Conclusion:** Refactor away when inheritance no longer represents a domain or framework role.

## Cross-Program Connections

- **Object-Oriented Programming:** overriding, dynamic dispatch, substitutability, and construction order are foundational.
- **Functional Programming:** higher-order functions encode creation variation without class inheritance.
- **Programming Languages:** initialization and dispatch rules determine whether construction hooks are safe.
- **Software Design:** dependency inversion and protected variation explain why workflow sees a Product contract.
- **Software Architecture:** frameworks invert control and expose application-supplied construction points.
- **Testing & Quality Engineering:** shared contract suites validate every returned product and creator workflow.
- **Systems Programming:** ownership and partial resource acquisition constrain overrides.
- **Security Engineering:** defaults, plugin selection, and error hygiene can become enforcement boundaries.
- **Delivery Engineering:** creator/product compatibility must remain coordinated across versioned components.
- **Engineering Management:** hierarchy ownership and extension policy determine review responsibility.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Factory Method intent, structure, participants, collaborations, consequences, and implementation guidance.
2. Craig Larman, [*Applying UML and Patterns*, 3rd ed.](https://www.pearson.com/en-us/subject-catalog/p/applying-uml-and-patterns-an-introduction-to-object-oriented-analysis-and-design-and-iterative-development/P200000000422), Prentice Hall, 2004. Places GoF patterns within responsibility-driven object design and iterative development.
3. Martin Fowler, [“Inversion of Control Containers and the Dependency Injection Pattern”](https://martinfowler.com/articles/injection.html), 2004, accessed 2026-08-28. Compares constructor assembly, factory services, injection, service location, and configuration/use separation.
4. Joshua Bloch, [*Effective Java*, 3rd ed.](https://www.pearson.com/en-gb/subject-catalog/p/effective-java/P200000000138), Addison-Wesley, 2018. Its static-factory guidance supplies an important contrast with the GoF subclass collaboration.
5. Martin Fowler, [*Refactoring: Improving the Design of Existing Code*, 2nd ed.](https://www.pearson.com/en-us/subject-catalog/p/refactoring-improving-the-design-of-existing-code/P200000000254/9780134757599), Addison-Wesley, 2018. Provides small behavior-preserving transformations for extracting and replacing creation logic.
6. Alan Shalloway and James R. Trott, [*Design Patterns Explained: A New Perspective on Object-Oriented Design*, 2nd ed.](https://www.pearson.com/en-us/subject-catalog/p/design-patterns-explained-a-new-perspective-on-object-oriented-design/P200000000605/9780321630049), Addison-Wesley, 2004. Discusses commonality/variability analysis and Factory Method in object-oriented languages.

## Exercises

### Exercise 1

Identify every role and dispatch event in the executable example. State Product behavioral, effect, error, ownership, and lifecycle contracts that the short code leaves implicit.

### Exercise 2

Add a `CsvReportJob` in design form. Specify which workflow and contract tests are reused, and list CSV-specific cases that one successful record cannot verify.

### Exercise 3

Refactor three creator subclasses that differ only in `make_formatter` into an injected creation function. State which properties are preserved and which extension semantics change.

### Exercise 4

Design a safe parameterized Factory Method for a cross-platform dialog that creates buttons and text fields. Explain when the design should become Abstract Factory instead.

### Exercise 5

An unfamiliar spacecraft telemetry framework lets mission-specific creators instantiate packet decoders. Produce a graduate-level Factory Method design covering initialization order, binary compatibility, untrusted input, timing, allocation, failure containment, evidence, and human authorization.

## Answers to the Exercises

### Answer 1

`ReportJob` is Creator, `make_formatter` the factory method, `JsonReportJob` and `LinesReportJob` Concrete Creators, the implicit formatter protocol Product, and the two formatter classes Concrete Products. Calling `run` on each concrete creator dispatches the inherited workflow, then dynamically dispatches `make_formatter`, then invokes `format` through the common behavior.

The Product contract should define accepted record schema, deterministic output, mutation prohibition, error taxonomy, thread safety, latency/effect class, and whether the result owns resources. Current products are fresh, hold no external resource, require no close, and should not mutate input. The code does not encode those claims in a nominal protocol or validate arbitrary values. Creator lifecycle must also state one factory call per `run` and no invocation during construction.

### Answer 2

`CsvReportJob.make_formatter` returns a `CsvFormatter` satisfying the same Product contract. Reuse the `ReportJob.run` workflow tests for factory-call multiplicity, record forwarding, result propagation, product failure, and no retention. Run shared formatter tests for accepted schema, nonmutation, deterministic output, error shape, and concurrency if promised.

CSV-specific tests cover declared column order, missing/extra fields, commas, quotes, embedded newlines, Unicode, null policy, encoding, spreadsheet-formula injection, multirow header consistency, streaming failure, and large records. One record proves neither standards compliance nor safe spreadsheet consumption. If CSV requires streaming ownership unlike the other formatters, enrich the Product contract or use a different workflow rather than violate substitution.

### Answer 3

Create one `ReportJob` with a constructor parameter `make_formatter`; `run` calls that callable and uses the returned Product. At the composition root, pass `JsonFormatter`, `LinesFormatter`, or another zero-argument creation function. Preserve one creation per run, record forwarding, output, failure propagation, fresh ownership, and the shared Product contract through characterization and contract tests.

Dynamic selection changes from creator-subtype dispatch to instance composition. Clients can vary factories without defining types; class-level override protection and framework subclass registration disappear. If Concrete Creators carried identity, additional policy, privileged protected access, or lifecycle hooks, those are not preserved automatically and require explicit collaborators. Remove the hierarchy only when those semantics are absent or deliberately migrated.

### Answer 4

The Creator owns dialog layout and event wiring. Its parameterized method `create_control(kind)` accepts a closed enum and returns a Control contract. Each platform creator maps `button` and `text_field` to compatible native controls, rejects unknown values, and preserves ownership, UI-thread, accessibility, event, and disposal contracts. Do not call it until platform state and UI thread are initialized. Test every kind for every platform plus shared control behavior.

When controls must form a coherent platform family across many independent workflows, repeated parameterized switches scatter family completeness. Introduce an Abstract Factory with named `create_button` and `create_text_field` operations, selected once at composition. It makes family consistency explicit and fails construction if a platform cannot supply the complete required family. Retain Factory Method when dialog subtype itself owns the platform/product decision and one narrow hook remains sufficient.

### Answer 5

The framework Creator owns bounded packet receipt, framing, decoder creation, decode, validation, telemetry accounting, and failure isolation. A mission Concrete Creator overrides `create_decoder(packet_version)` and returns a decoder satisfying a versioned Product ABI and behavioral contract. Finish mission configuration, memory arenas, tables, and clock initialization before invoking the hook; never dispatch it from base construction.

The decoder accepts bounded untrusted bytes, performs length and checksum checks before indexed access, has a proven maximum allocation and worst-case execution budget, cannot perform network or filesystem I/O, and returns classified errors without exposing stale data. Unsupported versions fail closed. Ownership uses preallocated or scoped memory; partial creation leaves no resource or registered handler. A fault cannot escape the containment boundary or delay subsequent critical processing beyond budget.

Verify ABI/API compatibility, shared decoder contracts, static analysis, fuzz/property tests, malformed/truncated/oversized packets, bit flips, version confusion, resource exhaustion, worst-case timing on flight-representative hardware, concurrency schedules, restart, and fault injection. Formal analysis may cover bounds and state invariants under stated assumptions; tests remain sampled. Signed mission packages, allowlisted versions, deterministic creator selection, rollback to an approved compatible decoder, and audit records govern deployment. Named mission, systems, real-time, safety, security, verification, and operations authorities must approve evidence; internal module validation grants no flight authorization.
