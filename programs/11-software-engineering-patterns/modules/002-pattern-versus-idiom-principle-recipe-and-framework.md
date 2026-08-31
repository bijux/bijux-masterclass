---
module_id: SEPAT-002
program: Software Engineering: Patterns
level: 1
module_number: 2
title: Pattern Versus Idiom, Principle, Recipe, and Framework
status: complete
last_verified: 2026-08-28
---

# Pattern Versus Idiom, Principle, Recipe, and Framework

## One-Page Review

### Governing question

How can engineers classify reusable guidance accurately enough to know what it explains, what it executes, and what judgment remains?

### Essential definitions

- A **pattern** is contextual design knowledge: a recurring problem, forces, an adaptable solution configuration, and consequences.
- An **idiom** is a low-level, language- or platform-specific way to express an implementation concern competently.
- A **principle** is a broad normative proposition that guides choices across many contexts without prescribing one participant structure.
- A **recipe** is an ordered procedure for achieving a bounded result under stated preconditions.
- A **framework** is reusable executable software that supplies a partial application structure and calls extension code at defined points.
- A **library** is reusable executable software whose operations application code normally calls while retaining control of the larger flow.
- A **mechanism** is a facility that makes behavior possible; it carries no automatic claim that using it is appropriate.
- An **instance** is a concrete realization of a pattern; an **embodiment** is software, such as a framework, whose design incorporates one or more patterns.

### Central model, mechanism, or theorem

Classify an artifact (a) along independent dimensions rather than by one label:

$$
Classify(a)=(scope,form,executable,control,variability,rationale).
$$

A pattern primarily preserves contextual rationale and an adaptable design relationship. An idiom narrows scope to language or platform expression. A principle broadens scope and weakens structural prescription. A recipe strengthens procedural order. A framework is executable and owns part of the control flow. These categories overlap: a framework can embody patterns, expose idioms, recommend principles, and document recipes.

### Critical invariants

- The label must match the claim: code reuse is not automatically design-knowledge reuse.
- A principle does not determine one pattern; several designs can honor the same principle.
- An idiom's guarantees are bounded by its language, runtime, and toolchain semantics.
- A recipe is safe only under its preconditions and recovery assumptions.
- A framework's lifecycle, extension points, and control ownership are part of its contract.
- A pattern remains distinct from a product that embodies it.
- Classification should expose remaining judgment, not inflate an artifact's authority.

### Common failures

Common failures include calling a framework a pattern, treating a slogan as a principle, presenting a code sample as a reusable pattern, using a recipe outside its preconditions, assuming a language idiom is portable, claiming a library owns control because it accepts callbacks, and debating labels while ignoring scope, rationale, and consequences.

### Compact example

“Release resources on every exit path” is a principle. Python's `with` protocol and C++ automatic object lifetime offer different idioms that can support it. “Wrap acquisition and release around an operation” can be described as a pattern when context, forces, structure, and consequences are documented. A web framework may execute the lifecycle and call user hooks. “Add `with open(...)` around these three lines” is a recipe for one edit.

### Connections

[SEPAT-001](001-recurring-problems-context-forces-and-consequences.md) supplies the pattern form used here. [SEPAT-003](../ROADMAP.md) develops pattern reading and writing. Retrieve [PLS-001's distinction among model, mechanism, guarantee, implementation, and policy](../../01-programming-languages-and-semantics/modules/001-programs-languages-and-observable-behavior.md). Framework boundaries connect to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) and language idioms to the relevant programming-language programs.

## Governing Question

When an engineer says “use this pattern,” are they offering contextual design judgment, a broad value, a language technique, a sequence of actions, or executable infrastructure?

All five forms can be useful. Confusing them creates false authority. A principle can inspire several incompatible solutions. An idiom can implement one role within a pattern but say nothing about whether the pattern fits. A recipe can reliably produce a file or migration under narrow assumptions without teaching a reusable design relationship. A framework can embody years of design experience, yet adopting it also accepts concrete dependencies, lifecycle rules, and upgrade obligations.

Accurate classification is not taxonomy for its own sake. It tells the reader what kind of evidence to seek. Patterns need recurrence, force fit, and consequence analysis. Idioms need language-semantic and toolchain evidence. Principles need interpretation and conflict resolution. Recipes need preconditions, ordering, idempotence, and recovery. Frameworks need executable verification, lifecycle knowledge, compatibility review, and operational ownership.

## Why This Matters

Software vocabulary often compresses different levels of reasoning into the same word. “Dependency injection” may mean a principle of explicit dependency supply, a construction pattern, a language idiom using constructor parameters, or a container framework. “Model-view-controller” may mean a pattern family, a framework's required directory layout, or a local naming convention. Without qualification, teams can agree verbally while planning different systems.

The distinction affects portability. A pattern can survive a change from objects to functions when its essential responsibilities remain. An idiom such as deterministic destruction depends on language lifetime semantics. A framework is more concrete still: it brings APIs, threading behavior, deployment constraints, and release cadence.

The distinction also affects critique. Rejecting a heavyweight framework does not reject the patterns it embodies. Following a good principle does not prove that every supporting abstraction is necessary. A correct recipe does not justify repeating the procedure manually if a durable mechanism should enforce it. Classification lets engineers retain useful intent while changing implementation.

## Prerequisites and Retrieval

You should understand functions, modules, interfaces, dependencies, callbacks, and basic program control flow. Retrieve these facts:

1. A design claim can be more general than the mechanism used to implement it.
2. Code can satisfy a compiler while violating an architectural or domain intent.
3. Control flow includes who decides when extension behavior runs, not merely who calls an initialization function.
4. Portability claims require a declared language, runtime, operating-system, or protocol boundary.
5. Procedures can fail between steps and therefore need recovery semantics.
6. Reusable code, reusable configuration, and reusable judgment are different assets.

## Learning Objectives

After completing this module, you should be able to:

- distinguish patterns, idioms, principles, recipes, frameworks, libraries, and mechanisms;
- classify ambiguous artifacts along scope, form, executability, control, variability, and rationale;
- explain how one principle can motivate several patterns and idioms;
- identify patterns embodied by a framework without equating product and pattern;
- locate inversion of control and extension ownership in framework designs;
- state the evidence appropriate to each guidance form;
- reclassify hybrid artifacts without forcing exclusive labels;
- choose the least binding reusable form adequate to a problem.

## Core Exposition

### Pattern: reusable contextual reasoning

A pattern explains why a recurring solution configuration is useful in a context. Its central asset is the relationship among problem, forces, solution, and consequences. A pattern instance may be handwritten, generated, or supplied by a framework. The same pattern can have different language representations, provided the mechanism that resolves the forces remains.

Patterns are not source-code components. Strategy may be implemented through interface objects, first-class functions, a dispatch table, or language modules. The pattern description helps a designer recognize runtime algorithm variation and accept the cost of another role. A reusable `Strategy` base class is merely one implementation option.

### Idiom: competent use of a concrete language or platform

An idiom addresses implementation at a lower, technology-bound level. It uses features and semantics of a particular language or platform: resource lifetime through C++ automatic storage duration, iteration through Python generators, error propagation through Rust's `?` operator, or asynchronous cleanup through a runtime's context protocol.

Calling idioms “low-level patterns” is common in pattern literature. The boundary is graded, not absolute. An idiom can realize a design pattern, and a widely recurring language technique can be written in pattern form. The useful question is whether the claim survives a technology change. If changing languages removes the problem or solution mechanism, the guidance is idiomatic.

An idiom must be verified against exact semantics. A double-checked initialization idiom that is safe under one memory model may be invalid under another. A cleanup idiom that depends on prompt finalization may fail under a garbage collector with nondeterministic reclamation. Familiar syntax is not portable evidence.

### Principle: directional judgment at broad scope

A principle states a desirable relationship or decision direction: hide information likely to change, keep authority least-privileged, separate policy from mechanism, or depend on stable abstractions. Principles help evaluate designs across many contexts. They are normally broader than patterns and underdetermine structure.

Principles can conflict. “Avoid duplication” may support shared abstraction, while “keep independent concerns independent” may support two similar implementations. “Fail fast” may conflict with “preserve availability.” The local context determines priority. A principle without assumptions and countervailing concerns can decay into a slogan.

A pattern often operationalizes a principle under specific forces. Adapter can support information hiding by containing external incompatibility. Strategy can support separation of policy and mechanism. Those principles do not imply that Adapter or Strategy is always required.

### Recipe: repeatable procedure

A recipe orders actions: create a migration, deploy backward-compatible readers, backfill data, verify counts, switch writers, and remove the old field. Its value is procedural reliability. Good recipes declare inputs, preconditions, checkpoints, failure handling, rollback or roll-forward behavior, expected outputs, and postconditions.

A recipe can instantiate a pattern or enforce a principle. It differs from a pattern because it tells the operator what to do in an order, often for a narrower environment. It differs from an algorithm because steps may involve human judgment, external systems, and non-atomic effects; termination and correctness may not be mathematically established.

Recipes are dangerous when cargo-culted. A zero-downtime migration recipe for a transactional database may fail for an eventually consistent store. A cleanup recipe that deletes an old artifact after one health check may ignore delayed consumers. The preconditions are part of the procedure.

### Framework: executable skeleton with extension points

A framework is reusable software that provides a partial application architecture. It defines stable and variable parts, coordinates a lifecycle, and invokes application-supplied behavior through callbacks, subclass hooks, plugins, configuration, or registered components. This inversion of control is characteristic: the application may start or configure the framework, but the framework decides when extension code participates in its larger algorithm.

A library usually provides operations the application calls while the application owns overall sequencing. This distinction also forms a continuum. An event-loop library owns control after `run`; a library function can call a user comparator temporarily; a framework exposes callable utility libraries. Classify the relevant interaction, not the product's marketing category.

Frameworks embody patterns. A web framework may combine Front Controller, Template Method, Observer, Dependency Injection, and middleware Chain of Responsibility. Adoption obtains executable implementations and integration, but it also accepts chosen variants. The framework may fix ordering, scope, concurrency, and error policies that a pattern description leaves adaptable.

### Mechanism: capability without appropriateness

A callback, reflection API, interface, annotation, queue, transaction, or code generator is a mechanism. Mechanisms enable designs but do not carry contextual justification. “The language supports decorators” does not show that layered decoration is readable. “The broker supports retries” does not show that repeating a non-idempotent operation is safe.

Mechanism documentation answers what the facility does. Pattern reasoning answers why a relationship resolves forces. Principle reasoning evaluates direction. A recipe sequences use. A framework integrates mechanisms into executable structure.

### Classification dimensions

Scope asks whether guidance applies to one language feature, a component collaboration, an application, or a system family. Form asks whether the artifact is an argument, proposition, procedure, or executable. Control asks who sequences behavior. Variability asks what the adopter may change. Rationale asks whether context, forces, and consequences are preserved.

No single dimension is decisive. A detailed pattern can include sample code; that does not turn the whole pattern into a framework. A framework manual can contain recipes. A language idiom can be documented with pattern sections. Multiple labels are acceptable when each is attached to the relevant aspect.

### Choose by the kind of reuse needed

Use a principle when a broad decision direction should survive many technologies. Use a pattern when teams repeatedly face the same force configuration and need adaptable structural guidance. Use an idiom when correctness or clarity depends on concrete language semantics. Use a recipe when ordered execution and recovery dominate. Adopt or build a framework when repeated applications benefit from an executable skeleton and can accept its control model.

The stronger the embodiment, the stronger the coupling. Principles and patterns demand more local design but preserve freedom. Recipes constrain process. Frameworks accelerate construction but become dependencies. Select the least binding form that reliably carries the needed knowledge.

## Definitions and Notation

For reusable artifact (a), define a descriptive profile

$$
D(a)=(S,F,E,C,V,R),
$$

where:

- (S) is scope, from language expression to system structure;
- (F) is primary form: proposition, contextual argument, ordered procedure, or executable software;
- (E\in\{0,1\}) records whether the artifact executes;
- (C) describes control ownership;
- (V) describes permitted variation and extension points; and
- (R) records rationale, including context, forces, and consequences.

This is a multi-axis description, not a partition. Let labels be predicates over the profile:

$$
Pattern(a),\ Idiom(a),\ Principle(a),\ Recipe(a),\ Framework(a).
$$

More than one predicate may be informative for different parts of one artifact. A framework (w) can embody a set of patterns:

$$
Embodies(w)=\{\Pi_1,\ldots,\Pi_n\},
$$

but (w\ne\Pi_i). The executable framework has implementation identity, versions, and concrete policy; the pattern is reusable design knowledge.

For control, write (calls(x,y,t)) when component (x) invokes (y) at time (t). A library interaction is commonly initiated and sequenced by application (A):

$$
A\rightarrow Library\rightarrow A.
$$

In a framework lifecycle, application configuration precedes a longer interval in which framework (W) invokes extension (X):

$$
A\rightarrow W;\quad W\rightarrow X\rightarrow W.
$$

These are schematic relations; real systems can mix both.

## Mechanisms, Invariants, or Proof Structure

### Identify the primary claim

Ask what the artifact promises. “This relationship repeatedly balances these forces” is pattern-shaped. “Prefer this property” is principle-shaped. “Express this construct this way in language L” is idiom-shaped. “Perform these actions in order” is recipe-shaped. “Extend these hooks and the runtime coordinates execution” is framework-shaped.

### Locate technology dependence

Replace the language or platform mentally. If the advice becomes meaningless, it is likely an idiom or product procedure. If the roles and force resolution remain, it may be a pattern. Technology independence is not proof of pattern status; recurrence and full contextual rationale remain required.

### Trace control ownership

Draw the runtime call sequence. Initialization by application code does not prevent inversion of control. The decisive question is who owns the lifecycle and decides when extension behavior runs. Also identify cancellation, error propagation, concurrency, and shutdown authority.

### Separate embodiment from explanation

List the patterns a framework appears to embody, then inspect its concrete variant. Does middleware short-circuit? Are dependencies singleton-, request-, or call-scoped? Are callbacks serialized? The pattern name cannot substitute for framework documentation and tests.

### Verify evidence by category

- For a pattern, check independent occurrences, context fit, force resolution, and consequences.
- For an idiom, check language specification, runtime versions, boundary cases, and compiler or interpreter behavior.
- For a principle, surface assumptions, conflicts, and measurable design effects.
- For a recipe, test preconditions, ordering, interruption, idempotence, recovery, and postconditions.
- For a framework, test lifecycle, extension contracts, compatibility, performance, security, and operations.

### Observe inversion of control

The following model contrasts a library call with a small framework lifecycle. The application calls both entry points, but the framework owns the sequence in which registered extension behavior runs.

<!-- bijux-verify: {"id":"library-and-framework-control","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"library: READY\nframework: before validate\nextension: validate order-7\nframework: after validate -> accepted\nresult: accepted\n","stderr":""}} -->
```python
def normalize(text):
    return text.strip().upper()


class CheckFramework:
    def __init__(self, extension, extension_name):
        self.extension = extension
        self.extension_name = extension_name

    def run(self, value):
        name = self.extension_name
        print("framework: before", name)
        result = self.extension(value)
        print(f"framework: after {name} -> {result}")
        return result


def validate(value):
    print("extension: validate", value)
    return "accepted" if value.startswith("order-") else "rejected"


print("library:", normalize(" ready "))
outcome = CheckFramework(validate, "validate").run("order-7")
print("result:", outcome)
```

This code demonstrates call direction only. A production framework also owns documented lifecycle, compatibility, resource, threading, diagnostic, and extension guarantees.

## Alternatives and Trade-Offs

**Use a decision record.** A design record captures one decision and its local rationale. It need not claim recurrence. It can cite a pattern while documenting why this instance differs.

**Publish a reference implementation.** Code clarifies feasibility and edge cases. It is more concrete than a pattern and may accidentally freeze incidental choices. Pair it with rationale and conformance tests.

**Provide a template or scaffold.** A template generates initial structure but may not control runtime. It accelerates setup while risking stale copied code. It is neither automatically a recipe nor a framework.

**Create a standard.** A standard specifies required conformance for interoperability or governance. It can use patterns internally but has normative authority different from experiential pattern guidance.

**Adopt a library.** Libraries preserve application control and can be easier to introduce incrementally. They may require every application to assemble lifecycle and policy consistently.

**Adopt a framework.** Frameworks remove repeated assembly and enforce common extension boundaries. They constrain architecture, create upgrade work, and can make exceptional flows difficult.

**Teach a principle only.** Principles survive technology changes and encourage judgment. Without patterns, idioms, or examples, learners may agree with the value yet fail to realize it.

**Teach a recipe only.** Recipes accelerate routine work and incident response. Without rationale, operators cannot safely adapt when assumptions change.

## Failure Modes and Misconceptions

1. **A framework and a pattern are interchangeable.** The framework is versioned executable software; the pattern is contextual design knowledge it may embody.
2. **An idiom is merely personal style.** A strong idiom exploits specific semantics to solve a recurring implementation concern and has concrete correctness boundaries.
3. **A principle determines one implementation.** Principles underdetermine structure and can conflict with other principles.
4. **A recipe transfers to every environment.** Its preconditions, authority, failure model, and postconditions bound it.
5. **Any callback means framework inversion of control.** A library may call a comparator briefly while the application still owns the larger lifecycle.
6. **Executable sample code is a pattern.** Code demonstrates an instance; it normally omits recurrence, forces, alternatives, and consequences.
7. **A framework removes design work.** It resolves some decisions and makes others—extension scope, data ownership, failures, upgrades—more consequential.
8. **Language-independent means pattern.** A vague maxim can be language-independent without documenting a recurring solution.
9. **One artifact needs exactly one label.** A framework guide can contain principles, pattern explanations, idioms, and operational recipes.
10. **Classification determines quality.** A bad pattern description and a dangerous recipe remain bad despite correct labels.

## Worked Examples

### Example 1

**Question:** Is “depend on abstractions, not concrete volatile details” a pattern?

**Reasoning:** It gives a broad direction across many designs but does not identify one recurring participant structure or collaboration. Ports and Adapters, Strategy, Abstract Factory, and ordinary parameter injection can all support it in different contexts.

**Conclusion:** It is a principle; particular patterns can operationalize it under narrower forces.

### Example 2

**Question:** How should C++ automatic cleanup and Python context managers be classified?

**Reasoning:** Both can realize the broad principle that resource release should follow acquisition across exceptional exits. Their mechanisms depend on different language semantics: deterministic object destruction versus explicit context protocols. A cross-language resource-management pattern can describe ownership and cleanup forces, while each syntax is an idiom.

**Conclusion:** One principle and pattern intent can have multiple language-specific idioms.

### Example 3

**Question:** Is a runbook for rotating a database credential a pattern?

**Reasoning:** The runbook lists environment-specific steps, checks, failure recovery, and expected results. It may embody principles such as least privilege and patterns such as overlapping credential validity. Its primary reusable form is an ordered operational procedure.

**Conclusion:** It is a recipe or runbook, even when patterns explain parts of its design.

### Example 4

**Question:** Does a web framework “implement MVC” exactly?

**Reasoning:** MVC names a family of responsibility separations and collaborations. A framework chooses concrete request lifecycle, controller discovery, view rendering, model integration, and extension rules, often combining Front Controller, Template Method, and middleware patterns. Those decisions are versioned software behavior.

**Conclusion:** The framework embodies a particular pattern composition; it is not identical to the abstract pattern family.

### Example 5

**Question:** A module exports one configured object. Is it a Singleton pattern?

**Reasoning:** Exporting one object is a language-level technique and deployment choice. Singleton as a pattern claims controlled single-instance identity and access under specific forces. The module may permit replacement, reload, multiple processes, or alternative instances in tests.

**Conclusion:** One exported instance is evidence of an idiom or configuration, not sufficient evidence of the Singleton pattern.

### Example 6

**Question:** What does the executable control-flow example prove?

**Reasoning:** It shows application code directly calling `normalize`, while `CheckFramework.run` controls when the registered `validate` extension executes and wraps it with before/after behavior. The exact output verifies this trace. It does not establish that the tiny class has the completeness, stability, or recurrence expected of a production framework.

**Conclusion:** Inversion of one call sequence is a mechanism and framework characteristic, not a quality certificate.

### Example 7

**Question:** Is constructor injection a principle, pattern, idiom, or framework feature?

**Reasoning:** “Make dependencies explicit and supply them from outside” is a principle or design approach. Constructor parameters are a common object-language idiom. A composition-root construction design can instantiate dependency-injection patterns. A container can automate discovery and lifecycle as a framework.

**Conclusion:** Qualify which layer is meant; the phrase can refer to related artifacts in all four categories.

### Example 8

**Question:** How does a retry recipe differ from the Retry pattern?

**Reasoning:** A pattern explains transient-failure context, attempt and deadline forces, idempotence, backoff, jitter, overload, and consequences. A service recipe may say “for this read API, retry these status codes at 20 and 60 ms, never beyond the 150 ms deadline.” The recipe binds the reasoning to one operation and procedure.

**Conclusion:** The pattern supports adaptation; the recipe operationalizes one reviewed instance.

### Example 9

**Question:** Is “create `controllers/`, `services/`, and `repositories/` directories” an architecture pattern?

**Reasoning:** The directory layout is a scaffold or convention. It neither proves responsibility separation nor documents context, forces, runtime dependencies, and consequences. A generated skeleton may even place coupled code under cosmetically separate names.

**Conclusion:** File structure is an implementation convention unless it participates in an enforced, contextual architectural design.

### Example 10

**Question:** A team standard says, “Use the platform framework's transaction annotation on every command handler.” What artifacts are combined?

**Reasoning:** Atomic command execution is a principle or requirement. Unit of Work and transaction-boundary patterns provide design rationale. The annotation is a platform idiom and mechanism. The container interpreting it is a framework. “Annotate every handler and verify rollback with this test” is a recipe. The word “every” still requires review for long-running, nested, or nontransactional commands.

**Conclusion:** Decomposing a hybrid rule reveals which claims need design, semantic, procedural, and executable evidence.

## Cross-Program Connections

- **Programming Languages & Semantics:** idiom claims rely on language guarantees; mechanisms must not be mistaken for policy.
- **Object-Oriented Programming:** interfaces, callbacks, inheritance, and composition realize patterns and framework extension points.
- **Functional Programming:** higher-order functions and algebraic data types often replace object-specific idioms while retaining pattern intent.
- **Metaprogramming:** annotations and code generation can enforce recipes or framework conventions but add another execution stage.
- **Software Design & Domain Modeling:** principles guide dependency direction; patterns respond to recurring solution-domain forces.
- **Software Architecture:** frameworks embody architectural commitments, while principles and patterns guide their evaluation.
- **Testing & Quality Engineering:** each category implies different evidence: conformance, language boundary, recovery, lifecycle, or consequence tests.
- **Platform Engineering:** approved frameworks and recipes can standardize operations but should preserve contextual rationale and escape paths.
- **Security Engineering:** framework authority, recipe preconditions, and idiom semantics determine attack surface and failure consequences.
- **Technical Writing:** the information form must tell readers whether to reason, implement, execute, or follow a procedure.

## References

1. Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, [“Chapter 4: Idioms,” *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*](https://www.oreilly.com/library/view/pattern-oriented-software-architecture/9781118725269/9781118725269_c04.xhtml), Wiley, 1996. Defines idioms as low-level, programming-language-specific patterns and explains their overlap with style and design patterns.
2. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780321700698), Addison-Wesley, 1994, ISBN 978-0-201-63361-0. Distinguishes patterns, reusable designs, toolkits, and frameworks and documents framework consequences.
3. Ralph E. Johnson and Brian Foote, “Designing Reusable Classes,” *Journal of Object-Oriented Programming* 1(2), pp. 22–35, 1988. A foundational account of white-box and black-box reuse, frameworks, protocols, and inversion of control.
4. Martin Fowler, [“Inversion of Control”](https://martinfowler.com/bliki/InversionOfControl.html), 26 June 2005, accessed 2026-08-28. Explains framework-controlled extension calls and contrasts the characteristic with application-controlled library calls.
5. Kent Beck, *Smalltalk Best Practice Patterns*, Prentice Hall, 1996, ISBN 978-0-13-476904-2. A language-specific collection illustrating idioms as communicable implementation practice.
6. Christopher Alexander, Sara Ishikawa, Murray Silverstein, et al., *A Pattern Language: Towns, Buildings, Construction*, Oxford University Press, 1977, ISBN 978-0-19-501919-3. Establishes patterns as contextual, connected, adaptable guidance rather than fixed components.
7. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), pp. 1053–1058, 1972. DOI: [10.1145/361598.361623](https://doi.org/10.1145/361598.361623). A primary source for information hiding as a broad design principle rather than a single pattern.

## Exercises

### Exercise 1

Classify the primary form of each artifact and justify the answer: (a) “separate policy from mechanism,” (b) a Rust example using `?` to propagate an error, (c) a deployment runbook, (d) a GUI toolkit that runs an event loop and invokes callbacks, and (e) a documented recurring collaboration for swapping algorithms at runtime.

### Exercise 2

Trace the executable example's call ownership. List calls in order from the first `print` through the final result, and identify the exact interval in which control is inverted. State one change that would make `normalize` participate as framework extension code instead of an ordinary library function.

### Exercise 3

A team describes “wrap every third-party SDK behind our own interface” as a universal pattern. Diagnose the classification and reasoning errors. Write a principle, a contextual pattern problem, an idiom, and a recipe that might legitimately exist around one third-party SDK.

### Exercise 4

Compare a library and a framework for scheduled background jobs. Evaluate control, lifecycle, extension variability, failure handling, testing, upgrades, and escape cost. Give a context favoring each.

### Exercise 5

An unfamiliar organization has a document called “Service Resilience Pattern” containing product-specific YAML, five shell commands, a circuit-breaker diagram, and the slogan “fail fast.” Decompose it into appropriate durable artifacts, state the evidence required for each, and propose a repository structure that prevents the product configuration from becoming the definition of the pattern.

## Answers to the Exercises

### Answer 1

(a) is a principle because it gives broad direction without one participant structure. (b) is a Rust idiom: its correctness and meaning depend on Rust's expression, conversion, and return semantics. (c) is a recipe or runbook because ordered actions, preconditions, recovery, and postconditions are primary. (d) is a framework because it supplies executable lifecycle and calls application extensions under inversion of control. (e) is Strategy or a related pattern description because it preserves recurring context, forces, an adaptable collaboration, and consequences. Each artifact may contain secondary forms, but the classification follows its primary claim.

### Answer 2

The sequence is: application calls `normalize`; `normalize` returns `READY`; application calls `print`; application constructs `CheckFramework`; application calls `run`; `run` prints its before event; `run` invokes the registered `validate` extension; `validate` prints and returns `accepted`; `run` prints its after event and returns; application prints the final result.

Control is inverted inside `run`: the framework method, not the application's top-level sequence, chooses when `validate` executes and surrounds it. To make normalization an extension, the framework could accept a normalization hook and invoke it before validation. That would add an extension contract and require decisions about hook order, errors, and whether normalization can reject input.

### Answer 3

The universal statement lacks context, forces, and consequences and confuses a principle with a mandatory interface pattern. Wrapping a stable, trivial SDK can add no useful insulation while duplicating its API. A defensible decomposition is:

- **Principle:** contain dependencies on volatile external contracts at owned boundaries.
- **Pattern problem:** when a required provider exposes incompatible concepts and replacement or independent testing is valuable, how can domain services depend on a stable local capability without erasing provider-specific semantics?
- **Idiom:** in a particular language, define a narrow protocol and translate provider exceptions into a closed local error type.
- **Recipe:** add the provider client to the composition root, implement the protocol adapter, run the shared conformance suite, record unsupported semantics, switch one caller, and verify telemetry before broader migration.

The team should use direct SDK access within a controlled boundary when the local interface would merely mirror every provider method and no independent contract exists.

### Answer 4

With a scheduling library, application code usually builds the timing loop, invokes library calculations or timers, owns shutdown, and decides how job failures propagate. This favors bespoke lifecycle, incremental adoption, and easy escape, but repeats assembly and operational policy. It is appropriate for one process with unusual scheduling semantics and a team prepared to own the loop.

A scheduling framework owns registration, triggering, concurrency, retries, persistence, shutdown, and callback invocation. It standardizes operations and supports many jobs, but jobs must accept its lifecycle, serialization, compatibility, and upgrade model. It is appropriate when multiple applications share stable scheduling needs and the framework's failure semantics meet them.

Tests for either must cover time, cancellation, duplicate triggers, overlap, clock changes, recovery, and shutdown. Framework tests additionally need extension compatibility and upgrade migration; library designs need application-level lifecycle and policy tests.

### Answer 5

Split the document by claim:

- A **resilience principle** document states bounded resource use, deadline propagation, and failure containment, including conflicts and exceptions.
- A **Circuit Breaker pattern** document states context, failure problem, forces, state-transition solution, applicability, and consequences without product keys.
- A **product idiom/configuration reference** defines the YAML schema and exact runtime semantics for one implementation and version.
- An **operational recipe** orders the five commands with permissions, preconditions, checkpoints, rollback, and postconditions.
- An **instance decision record** explains why one service adopted the product and which force evidence supported it.

Pattern evidence requires independent occurrences and force/consequence review. Principle evidence requires conflict analysis and outcome measures. Product configuration requires authoritative versioned documentation plus executable validation. The recipe requires interruption and recovery drills. The instance requires service-specific load and failure experiments.

A durable repository can place technology-neutral rationale under `patterns/circuit-breaker.md`, broad rules under `principles/resilience.md`, product semantics under `platforms/<product>/configuration.md`, runbooks under `operations/`, and instance decisions under the owning service's decision records. Cross-links connect them, while no copied YAML becomes the canonical pattern definition. The slogan “fail fast” should be expanded into conditions: fail before consuming more budget when success is implausible, while preserving required recovery and availability behavior.
