---
module_id: SEPAT-001
program: Software Engineering: Patterns
level: 1
module_number: 1
title: Recurring Problems, Context, Forces, and Consequences
status: complete
last_verified: 2026-08-28
---

# Recurring Problems, Context, Forces, and Consequences

## One-Page Review

### Governing question

How does a software pattern preserve reusable design judgment without turning a contextual response into a universal recipe?

### Essential definitions

- A **pattern** is a named, documented configuration that repeatedly resolves a design problem in a stated context by balancing forces and accepting consequences.
- A **recurring problem** is a design tension observed in multiple independent situations, not merely a duplicated code fragment.
- **Context** states the circumstances and preconditions under which the problem arises and the pattern may apply.
- A **force** is a relevant, often competing pressure that makes one design property desirable at the expense of another.
- A **solution** describes essential relationships and responsibilities, leaving incidental implementation choices open.
- A **consequence** is a beneficial, harmful, or uncertain result of applying the solution; consequences create the resulting context.
- **Applicability** is the condition under which the pattern's benefits plausibly justify its costs.
- A **contraindication** is evidence that the context or dominant forces do not support the pattern.
- A **pattern instance** is one concrete realization. The pattern is the reusable design knowledge, not that realization's classes or syntax.

### Central model, mechanism, or theorem

Represent a pattern as

$$
\Pi=(N,C,P,F,S,K,R),
$$

where (N) names it, (C) is context, (P) is the recurring problem, (F) is the set of forces, (S) is the solution structure, (K) is the set of consequences, and (R) records relationships to other patterns. Selection is conditional reasoning:

$$
ContextMatch(C_s,C_\Pi)\land ProblemMatch(P_s,P_\Pi)
\land Resolves(S_\Pi,F_s)
\land Acceptable(K_\Pi,F_s).
$$

This is a review model, not an algorithm that proves a pattern is correct. A pattern becomes useful when its form lets a designer trace each important force to a structural decision and then to positive and negative consequences.

### Critical invariants

- The problem and forces must be expressible without assuming the named solution.
- Recurrence concerns the design problem and force configuration, not identical code.
- The solution records essential relationships, not a frozen implementation.
- Each claimed benefit should resolve a stated force; each introduced cost should appear among the consequences.
- Context and contraindications bound the claim.
- Evidence from known uses supports recurrence and practicality but does not guarantee success in a new context.
- Applying a pattern changes the context and can introduce new problems requiring different patterns or removal.

### Common failures

Typical failures are starting from a fashionable name, treating a class diagram as the pattern, inventing a pattern from one design, hiding negative consequences, restating a requirement as a force, scoring unlike forces as if they had objective units, assuming old examples prove current fit, and adding indirection before the recurring pressure exists.

### Compact example

A service needs to notify a changing set of optional in-process listeners. Runtime subscription and loose publisher knowledge favor Observer; strict call order, immediate error propagation, and easy traceability oppose it. Observer trades direct coupling for registration lifecycle, ordering, reentrancy, and failure-policy complexity. If the listener set is fixed and the operation is critical, explicit calls may resolve the actual forces better.

### Connections

Retrieve [OOP-001's separation of state, behavior, and identity](../../02-programming-languages-object-oriented-programming/modules/001-objects-as-state-behavior-and-identity.md) and [SDDM-001's separation of problem and solution domains](../../09-software-engineering-software-design-and-domain-modeling/modules/001-distinguishing-the-problem-domain-from-the-solution-domain.md). [SEPAT-002](../ROADMAP.md) distinguishes patterns from idioms, principles, recipes, and frameworks. Pattern-level decisions feed [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) but do not replace system-wide architectural reasoning.

## Governing Question

What must a pattern say so that another engineer can recognize the same design problem, understand why the solution works, and know when not to use it?

A catalog name such as Adapter, Observer, or Circuit Breaker is compressed design knowledge. Compression helps teams communicate, but only if the shared meaning includes the context, competing forces, mechanism, and consequences. Otherwise the name becomes a slogan: “use Observer for events” or “add a circuit breaker for resilience.” Those statements erase the reasoning that determines whether the pattern improves this system.

Patterns are neither laws of nature nor prefabricated code. They are conditional arguments based on recurring experience. A pattern says, approximately: in contexts like these, this problem tends to recur because these forces conflict; arranging responsibilities in this way has repeatedly balanced those forces, producing these benefits and liabilities. The reader must still establish that the new situation belongs to the relevant class and that its priorities make the consequences acceptable.

## Why This Matters

Software design rarely optimizes one property. A design may need fast change and stable compatibility, low latency and bounded resource use, isolation and simple debugging, or local autonomy and cross-system consistency. Such forces are not eliminated by naming a pattern. A good pattern makes the tension discussable and gives engineers a tested structural move with known trade-offs.

This vocabulary improves reviews. Instead of arguing that “a factory is cleaner,” a reviewer can ask which construction variability exists, which callers should be insulated, and whether an additional abstraction and registration mechanism are justified. Instead of copying retry code, a team can distinguish transient failures from permanent ones, define a deadline and attempt budget, and confront the possibility that retries amplify overload.

Pattern reasoning also improves removal. When the context changes—one implementation remains, runtime variation disappears, or observability costs dominate—the pattern's original forces may no longer exist. Because the design was justified through explicit forces and consequences, the team has a basis for simplifying it.

The goal is not maximal pattern density. It is a traceable relationship among problem evidence, contextual constraints, a minimal structural response, and measured consequences.

## Prerequisites and Retrieval

You should understand modules or classes, interfaces, dependencies, mutable state, and basic testing. Retrieve these facts:

1. The problem domain describes stakeholder concepts and needs; the solution domain contains technical structures chosen to address them.
2. Coupling is dependency between elements; cohesion concerns how strongly one element's responsibilities belong together.
3. An interface can stabilize a contract while implementations vary, but every interface also creates another boundary to name, test, and evolve.
4. Quality attributes such as latency, modifiability, availability, and security can conflict.
5. A passing example demonstrates one execution, not a universal design guarantee.
6. Similar code can arise from different problems, while differently shaped code can instantiate the same pattern.

## Learning Objectives

After completing this module, you should be able to:

- define a software pattern without reducing it to code or a diagram;
- distinguish recurrence of a problem from repetition of an implementation;
- state context, problem, forces, solution, consequences, and resulting context separately;
- trace structural choices to the forces they resolve and liabilities they introduce;
- identify applicability conditions and contraindications;
- distinguish pattern evidence from proof that a pattern fits a new system;
- compare candidate solutions from the actual force priorities;
- review a proposed pattern instance for necessity, proportionality, and reversibility.

## Core Exposition

### From repeated experience to reusable judgment

The software-pattern tradition adapted an idea developed in building and urban design: document a recurring problem, the system of forces around it, and an adaptable configuration that resolves those forces in context. Software patterns similarly capture design experience, but the artifact is not reusable source code. It is a reusable *reasoning structure*.

The recurrence requirement matters. One clever design can be an experiment, local convention, or candidate pattern. Calling it a pattern claims more: the problem appears across independent instances; the solution has been tried; and common consequences can be articulated. Different pattern communities use different thresholds and review customs, so recurrence evidence should be reported rather than implied by a label.

Instances need not look identical. An Observer instance can use method calls, event objects, streams, or platform callbacks. The stable center is the relationship among publisher, subscription, notification, and dependent observers under a matching set of forces. If the description requires exact class names or a specific library, it is probably documenting an implementation rather than the pattern's essential structure.

### Context bounds the claim

Context answers “where are we before applying the pattern?” It includes relevant system state, scale, lifecycle, authority, quality goals, and existing constraints. For a caching pattern, context might include repeated expensive reads, acceptable staleness, a measurable locality of reference, and a source of truth outside the cache. Without those facts, “add a cache” is not a contextual design argument.

Context is not an exhaustive system description. It selects preconditions that change the solution's fitness. Useful context statements are testable or inspectable: “clients can repeat a request after losing a response” is stronger than “the system is distributed.” The former creates a concrete duplicate-processing problem; the latter is too broad.

Applicability conditions are positive context matches. Contraindications identify conditions that reverse or erase the argument. A cache is contraindicated when data changes frequently, stale reads are unacceptable, invalidation is unavailable, and the underlying read is already cheap. Listing contraindications prevents the pattern from masquerading as a default.

### The problem is a tension, not a solution-shaped request

A weak problem statement says, “How do we add an Observer?” It assumes the conclusion. A stronger statement says, “How can one publisher notify a varying set of dependents without compiling direct knowledge of every dependent?” The latter can be evaluated against alternative solutions.

The problem should name the unresolved tension at the same abstraction level as the proposed solution. “We need scalability” is too vague for a class-level pattern. “One process must serve many mostly idle connections without allocating one operating-system thread per connection” is specific enough to motivate event-driven concurrency patterns.

Separate symptoms from the recurring problem. Duplicate conditionals may signal variation, but they may also reflect genuinely different domain rules. A pattern proposal should explain the causal pressure, not only the visible code smell.

### Forces explain why the problem is difficult

Forces are considerations that pull the design in competing directions. They may include variability, coupling, latency, memory, ordering, consistency, security, operability, team knowledge, compatibility, or migration cost. A requirement can constrain the solution, but it becomes useful in pattern reasoning when its interaction with other concerns is made explicit.

Forces do not share natural units. Five milliseconds of latency, two weeks of migration effort, and risk of unauthorized access cannot be added objectively. Teams may use rankings or decision matrices to expose assumptions, but the numbers are elicitation aids, not measurements unless a valid measurement model exists.

Priority belongs to the local context. The same pattern can be appropriate in one subsystem and harmful in another. A Proxy that adds remote access transparency may be convenient for coarse operations; it can conceal network latency and partial failure where callers need to reason explicitly about both.

### The solution states essential structure and dynamics

A pattern solution identifies participating responsibilities, relationships, information flow, lifecycle, and important collaboration steps. It should be specific enough to implement yet general enough to admit context-sensitive variants. “Use indirection” is too abstract. A library-specific API listing is too concrete.

Structure alone is insufficient. Observer requires not only a publisher-to-observer relation but subscription, unsubscription, notification timing, and failure behavior. Circuit Breaker requires state transitions and probes, not just a wrapper class. Unit of Work requires tracking changes and coordinating persistence within a transactional boundary, not merely naming an object `UnitOfWork`.

The solution should connect to forces. If runtime substitution is a dominant force, identify the seam that enables it. If strict resource bounds matter, show where admission is limited. A participant with no force-based justification may be accidental complexity.

### Consequences complete the argument

Consequences describe the resulting context. Positive consequences show which forces are better resolved. Negative consequences reveal new coupling, state, latency, indirection, failure modes, operational work, or skills required. Neutral consequences describe shifts whose value depends on the situation.

Every pattern redistributes complexity. Adapter localizes incompatibility but creates an additional contract to maintain. Observer reduces direct publisher knowledge but adds registration lifecycle, ordering, reentrancy, and failure-policy decisions. Retry can mask transient faults but consumes deadline and capacity and can duplicate effects. A pattern description that lists only benefits is marketing, not engineering guidance.

Consequences are predictions until observed in the new instance. Record them as hypotheses that can be checked: build time should remain below a budget; queue depth should remain bounded; adding a provider should require changes only in one registration boundary. After implementation, measurement may confirm, qualify, or refute the expected result.

### Names compress complete arguments

A strong pattern name lets experienced collaborators retrieve the full argument. It does not excuse them from checking fit. Names create a design vocabulary, support comparison, and reveal relationships: Adapter can surround a legacy component; Facade can provide a stable subsystem entry; Strategy can vary policy behind that entry.

Names also anchor cognitive bias. Once a proposal is called “CQRS,” reviewers may debate whether it is a correct CQRS implementation instead of asking whether independent read and write models solve a measured problem. Begin a review with context and forces. Introduce the name after the problem is understood.

### Patterns are generative, not prescriptive

A pattern does not command identical output. It provides a configuration and a sequence of reasoning that designers adapt. Local names, language facilities, lifecycle, concurrency, error semantics, and operational constraints shape the instance. Faithfulness means preserving the mechanism that resolves the forces, not copying a diagram.

This adaptability creates an evaluation burden. A variant must explain which parts are essential, which are optional, and how its consequences differ. Saying “our version of Observer has no unsubscribe operation” is not a harmless omission when subscribers outlive publishers or retain resources. The changed lifecycle must be justified.

## Definitions and Notation

Let a situation be

$$
X=(C_x,P_x,F_x,Q_x,E_x),
$$

where (C_x) is observed context, (P_x) the design problem, (F_x=\{f_1,\ldots,f_n\}) the forces and their local priorities, (Q_x) non-negotiable constraints, and (E_x) current evidence.

Let a pattern be

$$
\Pi=(N,C_\Pi,P_\Pi,F_\Pi,S_\Pi,K_\Pi,R_\Pi,O_\Pi),
$$

where (O_\Pi) records known occurrences. Applying the pattern constructs an instance (I=adapt(S_\Pi,X)). The resulting situation is

$$
X'=apply(I,X).
$$

Fitness is not a scalar theorem. A review may define a partial order (\succeq_X) over candidates: (I_a\succeq_X I_b) means the evidence supports (I_a) as no worse than (I_b) on every mandatory constraint and better on at least one locally prioritized force, without an unacceptable consequence. Incomparable candidates are normal.

For traceability, define a relation

$$
T\subseteq F_x\times Decisions(I)\times K(I).
$$

Each important force should relate to at least one decision, and each important decision should have anticipated consequences. This relation is a review device, not a formal proof of design quality.

**Known use** means a documented occurrence that supports practical recurrence. **Evidence** includes measurements, incidents, change history, experiments, and reviewed occurrences. **Guarantee** means a property enforced by a mechanism under stated assumptions. Pattern history alone is evidence, not a guarantee.

## Mechanisms, Invariants, or Proof Structure

### Establish recurrence

Collect independent occurrences of the problem, not copies descended from one codebase. Record what remained stable across contexts: the tension, force interaction, structural response, and consequences. Variation among instances helps separate the pattern's essence from incidental technology.

### Preserve problem independence

Write the context, problem, and forces before naming a candidate. Review them for solution vocabulary. If the problem mentions “visitors,” rewrite it in terms of operations that must vary over a stable object structure. This makes competing designs visible and reduces confirmation bias.

### Build a force-to-decision trace

For each dominant force, identify the solution decision intended to resolve it. Then ask what liability that decision creates. Runtime subscriber variation may motivate a subscription registry; the registry introduces lifecycle and synchronization state. This trace is the pattern's causal core.

### Check mandatory constraints first

A candidate that violates a safety, legal, protocol, or hard resource constraint is inadmissible even if it scores well elsewhere. Separate constraints from optimizable forces. Do not average a security violation against developer convenience.

### Evaluate the resulting context

The pattern solves one problem by changing the system. Inventory new responsibilities, states, dependencies, failure modes, and operational signals. Decide who owns them. A consequence without an owner is deferred risk.

### Make consequences falsifiable

Translate important expected consequences into checks. If Strategy is intended to localize algorithm variation, inspect whether adding a new algorithm avoids edits to existing clients. If a bounded queue should contain overload, test admission and monitor saturation. If an Adapter should preserve a contract, run shared conformance tests against both implementations.

### Keep the instance removable

Record the force that justifies each seam. Avoid leaking pattern machinery across unrelated code. A localized instance can be removed when variability disappears; a pattern vocabulary embedded in every domain type is costly to unwind.

### Use scoring only as an elicitation aid

The following executable example makes assumptions visible. Scores mean “worse, neutral, better” for one workshop; they are not measurements and cannot override mandatory constraints.

<!-- bijux-verify: {"id":"force-decision-aid","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"direct-calls: 5\nobserver: 9\nselected for discussion: observer\nmandatory checks still required: ordering, failure policy, lifecycle\n","stderr":""}} -->
```python
weights = {
    "runtime_subscriber_change": 4,
    "traceability": 3,
    "simple_lifecycle": 2,
}

ratings = {
    "direct-calls": {
        "runtime_subscriber_change": 0,
        "traceability": 1,
        "simple_lifecycle": 1,
    },
    "observer": {
        "runtime_subscriber_change": 2,
        "traceability": -1,
        "simple_lifecycle": 2,
    },
}

scores = {
    candidate: sum(weights[force] * rating for force, rating in values.items())
    for candidate, values in ratings.items()
}

for candidate in sorted(scores):
    print(f"{candidate}: {scores[candidate]}")
print("selected for discussion:", max(scores, key=scores.get))
print("mandatory checks still required: ordering, failure policy, lifecycle")
```

The model deliberately cannot conclude that Observer is correct. The ratings are judgments, force independence is not established, and ordering or failure semantics may disqualify the candidate.

## Alternatives and Trade-Offs

**Start from a principle.** Principles such as information hiding or dependency inversion guide many situations at a higher abstraction level. They can narrow choices but usually do not supply a recurring participant structure and collaboration. SEPAT-002 develops this distinction.

**Use a local design rule.** A repository convention can standardize error translation or construction. It may be valuable without recurrence outside that repository or the richer explanatory form of a pattern.

**Adopt a framework.** A framework supplies executable architecture and extension points. It may embody patterns, but adoption also accepts its lifecycle, dependencies, and constraints. A pattern can be implemented without that framework.

**Refactor after pressure appears.** Delaying a pattern preserves simplicity and produces concrete evidence about variation. It can make migration expensive if the future pressure is both highly probable and difficult to accommodate. Use reversible seams where uncertainty is high.

**Design the pattern in advance.** Anticipatory structure can be justified by contractual variability, known platform families, or migration obligations. Speculative extensibility based only on imagined reuse usually creates unused abstractions.

**Copy a known implementation.** A reference instance accelerates construction but carries its original context assumptions. Re-derive the force fit and adapt lifecycle, error, concurrency, and operational semantics.

**Create a new pattern.** New pattern writing is appropriate when independent occurrences reveal a stable problem–force–solution relationship not adequately captured elsewhere. A single successful implementation should remain a candidate or case study until recurrence is established.

## Failure Modes and Misconceptions

1. **A pattern is a class diagram.** The diagram omits context, forces, dynamics, and consequences; it can depict only one solution shape.
2. **Repeated code proves a recurring design problem.** Duplication is a symptom. The underlying reasons may differ or be simpler to remove directly.
3. **A named pattern is automatically better than an unnamed design.** Names improve communication only when the complete argument fits.
4. **Known uses guarantee local success.** They establish plausibility and reveal consequences; local context and implementation still matter.
5. **Forces are a feature wish list.** Forces must explain tensions and priorities that discriminate among solutions.
6. **Consequences are optional documentation.** Without costs and resulting context, reviewers cannot judge proportionality or ownership.
7. **A numerical decision matrix makes selection objective.** Ordinal judgments, correlated forces, and hard constraints limit the model.
8. **Patterns should be installed early to show good design.** Premature indirection can obscure the actual domain and make change harder.
9. **Every variation deserves an interface.** Stable, local, inexpensive variation may be clearer as direct code.
10. **Once applied, a pattern should remain.** Patterns answer forces; when forces disappear or invert, simplification is responsible design.

## Worked Examples

### Example 1

**Question:** Does duplicated object construction justify Factory Method?

**Reasoning:** Three callers repeat two constructor arguments, but the product type never varies and construction has no caller-specific policy. The recurring symptom is code duplication, while the force is simply keeping defaults consistent. A creation function or direct refactoring resolves it without subclass-controlled construction.

**Conclusion:** Repeated syntax alone does not establish the recurring problem Factory Method addresses.

### Example 2

**Question:** When does Adapter fit a payments integration?

**Reasoning:** The application owns a stable `charge` contract, while a required provider exposes incompatible request and error shapes. The application should not absorb provider vocabulary, and replacement is plausible. An Adapter translates calls and errors at the boundary. It adds mapping code and must be conformance-tested; it cannot erase provider-specific semantics such as asynchronous settlement.

**Conclusion:** Adapter fits when incompatibility is real and a locally owned contract is valuable, with semantic differences kept explicit.

### Example 3

**Question:** Is process-wide configuration automatically a Singleton pattern?

**Reasoning:** “Only one is convenient” is not the same as “the domain permits exactly one identity and all access must share it.” Global access hides dependencies, complicates test isolation, and prevents multiple configurations in one process. Constructing one object at the composition root and injecting it supplies one current instance without enforcing global identity.

**Conclusion:** Cardinality in one deployment does not by itself justify Singleton's global access and lifecycle consequences.

### Example 4

**Question:** Why might Observer be worse than direct calls for a safety-critical workflow?

**Reasoning:** The workflow has two fixed dependents, requires a visible call sequence, and must abort on the first failure. Runtime subscription is not a force. Observer would introduce hidden registration, ordering policy, and ambiguous failure propagation while resolving no dominant variability.

**Conclusion:** A recognized pattern is contraindicated when its motivating forces are absent and its liabilities oppose required behavior.

### Example 5

**Question:** How do consequences change the evaluation of Retry?

**Reasoning:** A remote read sometimes fails transiently, favoring bounded retry. But requests share an overloaded dependency and have a 200 ms deadline. Each attempt consumes time and capacity; synchronized retries can amplify failure. A valid instance needs retriable-error classification, deadline-aware attempt limits, jittered backoff, and observability.

**Conclusion:** Retry is a budgeted load decision, not merely a loop around an unreliable call.

### Example 6

**Question:** What does the force-scoring program actually establish?

**Reasoning:** Given its declared weights and ratings, it recomputes `direct-calls` as (4\cdot0+3\cdot1+2\cdot1=5) and `observer` as (4\cdot2+3\cdot(-1)+2\cdot2=9). This checks arithmetic and exposes assumptions. It does not validate the ratings, independence of forces, or mandatory lifecycle behavior.

**Conclusion:** A decision aid structures discussion; it does not prove design fitness.

### Example 7

**Question:** Can two different implementations be instances of the same pattern?

**Reasoning:** One Strategy instance stores objects implementing a common interface; another stores first-class functions. Both let a context delegate a varying algorithm through a stable role. If their selection, lifecycle, state, and error consequences differ, those variations still require documentation.

**Conclusion:** Pattern identity follows the force-resolving relationship, not one language mechanism.

### Example 8

**Question:** What resulting context does a Facade create?

**Reasoning:** A Facade gives clients a stable, narrower entry to a complex subsystem and can normalize errors. It also becomes a compatibility boundary and potential bottleneck for unrelated operations. The team must own its API evolution and retain escape hatches for capabilities that should not be flattened.

**Conclusion:** The solution resolves client coupling by introducing a new interface with ongoing ownership.

### Example 9

**Question:** When is a proposed pattern only a local technique?

**Reasoning:** One team batches a particular vendor's records in groups of 37 because of a current endpoint limit. The technique works, but no independent recurrence or stable force relationship is known, and the number is vendor policy. Document it as an integration rule with its source and expiry condition.

**Conclusion:** A useful local solution need not be promoted to a pattern.

### Example 10

**Question:** How should a review evaluate a new message-routing abstraction?

**Reasoning:** First state the context: three message types, one current destination, regulated audit requirements, and likely addition of destinations. Then state forces: routing variability, visible decisions, deterministic tests, and low operational burden. Compare direct dispatch, a table, and a pluggable router. Trace every participant to a force, enumerate configuration and failure consequences, prototype the simplest viable option, and record evidence from change scenarios.

**Conclusion:** Review begins with observed context and forces, then tests whether the smallest candidate resolves them with acceptable consequences.

## Cross-Program Connections

- **Object-Oriented Programming:** polymorphism, identity, composition, and dispatch are mechanisms used by many object patterns, not reasons to apply them.
- **Functional Programming:** higher-order functions and algebraic data types can realize pattern intents without class structures.
- **Concurrent and Parallel Programming:** scheduling, ownership, cancellation, and ordering forces determine concurrency-pattern fitness.
- **Software Design & Domain Modeling:** design problems must not be confused with domain problems or incidental code structure.
- **Software Architecture:** architectural decisions aggregate forces across systems, teams, deployment, and evolution; individual patterns contribute but do not decide the architecture.
- **Testing & Quality Engineering:** consequence hypotheses become conformance, property, load, failure, and change tests.
- **Database Engineering:** transaction, consistency, identity, and persistence forces shape enterprise data patterns.
- **Distributed Systems:** partial failure, duplicated messages, time, and coordination make context statements essential for resilience patterns.
- **Security Engineering:** a pattern can redistribute authority and attack surface; security constraints cannot be averaged away.
- **Engineering Management:** team ownership and cognitive load are forces with operational consequences, not afterthoughts.

## References

1. Christopher Alexander, Sara Ishikawa, Murray Silverstein, Max Jacobson, Ingrid Fiksdahl-King, and Shlomo Angel, *A Pattern Language: Towns, Buildings, Construction*, Oxford University Press, 1977, ISBN 978-0-19-501919-3. The originating pattern-language treatment of recurring contexts, systems of forces, adaptable solutions, and connections among patterns.
2. Christopher Alexander, *The Timeless Way of Building*, Oxford University Press, 1979, ISBN 978-0-19-502402-9. The conceptual foundation for patterns as generative, context-sensitive design knowledge rather than copied forms.
3. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780321700698), Addison-Wesley, 1994, ISBN 978-0-201-63361-0. The canonical software design-pattern catalog and pattern template.
4. Frank Buschmann, Regine Meunier, Hans Rohnert, Peter Sommerlad, and Michael Stal, [*Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*](https://www.oreilly.com/library/view/pattern-oriented-software-architecture/9781118725269/), Wiley, 1996, ISBN 978-0-471-95869-7. A systematic treatment of pattern categories, descriptions, relationships, and architectural consequences.
5. Gerard Meszaros and Jim Doble, [“A Pattern Language for Pattern Writing”](https://hillside.net/language-for-pattern-writing), in *Pattern Languages of Program Design 3*, Addison-Wesley, 1998. Guidance derived from recurring experience writing and reviewing pattern forms.
6. The Hillside Group, [“Patterns Definition”](https://hillside.net/patterns-definition) and [“Patterns Information”](https://hillside.net/46-patterns-library/patterns-information?start=4), accessed 2026-08-28. Community reference material emphasizing proven solutions, context, conflicting forces, and resulting consequences.
7. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002, ISBN 978-0-321-12742-6. A catalog that makes applicability and consequences explicit across domain logic, data sources, object-relational behavior, web presentation, and distribution.

## Exercises

### Exercise 1

Rewrite this solution-shaped statement as a context, problem, and at least three forces: “We need a Repository pattern because database calls are scattered.” Do not name a solution in the rewritten problem.

### Exercise 2

For the `observer` candidate in the executable decision aid, change the `simple_lifecycle` rating from `2` to `-2`. Recompute both scores by hand, state the selected candidate under the toy rule, and explain why the result still does not decide the design.

### Exercise 3

A team applied a cache to a product catalog. Reads are faster, but customers sometimes see old prices and operations cannot explain which value was served. Diagnose the missing context, forces, and consequences. Propose three evidence checks before retaining the cache.

### Exercise 4

Compare Strategy implemented with objects, Strategy implemented with first-class functions, and a direct conditional. Use the forces of runtime variation, per-strategy state, static discoverability, debugging, and number of alternatives. Give one context in which each is preferable.

### Exercise 5

An unfamiliar warehouse-control system proposes an event bus so scanners, inventory, routing, safety alarms, and analytics can “stay decoupled.” Produce a pattern-review brief containing context questions, a solution-independent problem, dominant forces, mandatory constraints, at least two alternatives, expected positive and negative consequences, and a reversible experiment.

## Answers to the Exercises

### Answer 1

One defensible rewrite is:

- **Context:** Several application services perform persistence operations against one database. Query details and transaction handling appear in service code, and a second storage implementation is being evaluated.
- **Problem:** How can application services obtain and persist domain objects without each service depending on storage-specific query and mapping details?
- **Forces:** services need domain-focused interfaces; storage features and query capabilities differ; transaction and identity semantics must remain visible; an additional boundary adds mapping and testing cost; and direct database access may be simpler for storage-shaped reporting queries.

This formulation permits Repository, Data Mapper, query services, direct access at a controlled boundary, or another design. Before selecting Repository, the team must verify that domain-oriented collection semantics match actual use and that the abstraction will not conceal required database capabilities.

### Answer 2

`direct-calls` remains (4\cdot0+3\cdot1+2\cdot1=5). The revised `observer` score is

$$
4\cdot2+3\cdot(-1)+2\cdot(-2)=8-3-4=1.
$$

The toy rule therefore selects `direct-calls`. The result remains non-decisive because weights and ratings are subjective ordinal judgments, forces may overlap, mandatory constraints are outside the sum, and the model omits implementation evidence. Its value is exposing that lifecycle simplicity changes the recommendation, not manufacturing objectivity.

### Answer 3

The original context omitted price-change frequency, allowed staleness, invalidation authority, and the regulatory or customer impact of displaying an old price. The forces include read latency and origin load on one side, and price correctness, explainability, invalidation complexity, memory, and operational ownership on the other. Missing consequences include stale reads, new cache state, invalidation failures, and loss of provenance for served values.

Before retention, measure: (1) latency and origin-load improvement at representative traffic, including misses; (2) stale-price frequency and maximum age against an explicit business bound; and (3) observability and invalidation behavior through tests and telemetry that identify cache hit/miss, value version, source timestamp, and purge outcome. If the correctness constraint forbids stale prices or the performance gain is negligible, remove the cache or change what is cached.

### Answer 4

Object strategies suit multiple algorithms with substantial per-strategy state, lifecycle, or several related operations; an interface makes those responsibilities explicit. Function strategies suit one behavioral operation with little state; functions reduce ceremony and remain easy to inject and test. A direct conditional suits two or three stable, short alternatives local to one cohesive operation; extracting a new role would add navigation without meaningful variability isolation.

For runtime variation, both strategy forms beat a hard-wired conditional when clients select behavior dynamically. Objects can improve static discoverability in class-oriented languages but add allocation and type surface. Functions often improve local debugging but may need closures or explicit records for state. The number of alternatives is not a mechanical threshold: expected independent evolution and ownership matter more.

### Answer 5

A strong brief begins with questions: Are components in one process or across failure domains? Which events are facts versus commands? What ordering, latency, delivery, replay, and audit guarantees exist? Who can publish and subscribe? Can safety decisions be asynchronous? How are schema and subscriber lifecycle governed?

The solution-independent problem could be: “How should producers communicate facts to a changing set of optional consumers while preserving required ordering, safety response, auditability, and bounded resource use?” Dominant forces include subscriber variability, producer knowledge, timing, failure isolation, traceability, backpressure, schema evolution, and operational complexity. Mandatory constraints might require safety alarms to be delivered synchronously within a fixed deadline and inventory mutations to be durably auditable.

Alternatives include explicit direct calls through narrow ports, an in-process typed dispatcher, and a durable broker-backed event channel. An event bus may reduce direct knowledge and ease optional analytics, but introduces hidden topology, delivery semantics, queue state, schema governance, duplicate handling, and difficult end-to-end debugging. Direct calls preserve visible control and failure flow but couple producers to an orchestration boundary.

A reversible experiment routes only noncritical analytics events through a typed in-process dispatcher behind one port. It records end-to-end traces, queue depth, failure behavior, subscriber changes, and maintenance effort. Safety and inventory-critical paths remain explicit. The team promotes or removes the bus based on measured subscriber-change benefits and acceptable operability, not on the word “decoupled.”

The answer is complete when every mandatory constraint can disqualify a candidate, every expected benefit has evidence, every new failure mode has an owner, and the experiment can be removed without spreading event-bus types throughout the domain.
