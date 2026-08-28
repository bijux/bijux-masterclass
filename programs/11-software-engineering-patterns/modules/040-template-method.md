---
module_id: SEPAT-040
program: Software Engineering: Patterns
level: 1
module_number: 40
title: Template Method
status: complete
last_verified: 2026-08-28
---

# Template Method

## One-Page Review

### Governing question

How can a base abstraction own an invariant algorithm sequence while subclasses customize only declared steps, without exposing partial-state hazards, fragile inheritance coupling, ambiguous hooks, or unsafe failure and cleanup behavior?

### Essential definitions

- A **template method** defines the fixed skeleton/order of an algorithm.
- A **primitive operation** is a required subclass step invoked by the skeleton.
- A **hook** is an optional extension point with a documented default behavior.
- An **invariant step** is owned by the base and must not be bypassed or reordered.
- The **Hollywood Principle** summarizes control inversion: the framework calls extension code at declared points.
- A **non-virtual interface (NVI)** exposes a stable public method that delegates to non-public overridable primitives.
- The **fragile base-class problem** arises when subclass behavior depends on undocumented base implementation details that later change.
- A **variation axis** is one independently changing decision; inheritance binds all hooks into one subclass combination.

### Central model, mechanism, or theorem

Let template (T) sequence invariant base steps (b_i), required primitives (p_j), and optional hooks (h_k):

\[
T(x)=b_{post}(h_2(p_2(b_2(h_1(p_1(b_{pre}(x))))))).
\]

If precondition (P) holds, every override satisfies its hook contract, and failures/cleanup follow the skeleton, then template postcondition (Q) and invariant (I) may be derived compositionally. Inheritance and call order alone do not prove override correctness, exception safety, resource release, or transactional effects.

### Critical invariants

- The public template method owns validation, ordering, invariant checks, failure mapping, and cleanup; subclasses cannot bypass it where the language permits enforcement.
- Each primitive/hook documents inputs, output, allowed effects, exceptions, cancellation, idempotency, and base state visible at the call point.
- Required primitives are abstract/fail-fast; optional hooks have safe narrow defaults rather than silently incomplete behavior.
- Constructors/destructors do not dispatch into subclass behavior before/after subclass invariants and resources are valid.
- The base invokes overridable code only while its own state satisfies a documented callback invariant and without unsafe locks/resources.
- Cleanup executes for success, failure, cancellation, and partial acquisition in a documented order.
- Subclasses preserve base pre/postconditions and do not depend on undocumented call counts/order/state.
- Multiple independent variation axes trigger composition/policies rather than subclass combinatorial explosion.

### Common failures

Common failures include an overridable public skeleton, hooks named `before`/`after` without contracts, empty defaults for required behavior, subclasses calling steps out of order, overrides strengthening preconditions, base changes adding/reordering calls, constructor virtual dispatch, callbacks while holding locks, half-initialized base fields, hook reentrancy, swallowing exceptions, cleanup only on success, double cleanup, remote calls inside a local transaction, async hooks with mismatched cancellation, subclass-specific type checks, deep inheritance, and tests that only cover the base happy path.

### Compact example

A tokenization template validates nonblank input, prepares it, calls one format-specific split primitive, normalizes every token through a shared hook, and validates the result. Whitespace and CSV subclasses produce the same lowercase tuple; blank input fails before any primitive is called.

### Connections

[SEPAT-039](039-strategy.md) varies the whole algorithm through composition; [SEPAT-041](../ROADMAP.md) adds operations over stable object structures. Template Method connects to [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), and [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md).

## Governing Question

Which parts of an algorithm are invariant and must remain under base-class control, which steps may vary, and what exact contract makes third-party subclass code safe at each callback point?

Template Method is inheritance-based control inversion. It is appropriate when the sequence is stable and subclass identity naturally bundles the intended variation—not merely to remove duplicated lines.

## Why This Matters

Framework lifecycles, parsers, importers, test fixtures, serializers, request handlers, and resource protocols often require a fixed sequence with limited customization. Centralizing the sequence prevents subclasses from omitting validation or cleanup.

The base class also becomes a behavioral framework whose internal changes can break subclasses. A small protected method is still an API: call order, frequency, state, threads, errors, and resource ownership matter.

## Prerequisites and Retrieval

You should understand inheritance, dynamic dispatch, contracts, exception safety, resource management, concurrency, asynchronous cancellation, and composition. Retrieve these facts:

1. Derived construction is not complete while base constructors run; virtual-dispatch rules vary by language and can expose partial objects.
2. A callback may re-enter, block, throw, cancel, mutate shared state, or retain references.
3. `finally`/RAII/resource scopes are mechanisms for cleanup; normal control flow alone is insufficient.
4. Behavioral subtypes cannot demand stronger inputs or promise weaker outcomes than the base contract.
5. Adding one hook call can be a breaking behavioral change even if signatures are unchanged.
6. Independent choices composed by inheritance produce cross-product subclasses.

## Learning Objectives

After completing this module, you should be able to:

- identify a genuinely invariant skeleton and cohesive variation points;
- write contracts for primitives, hooks, callback state, failure, and cleanup;
- apply NVI/final-template design where supported;
- avoid constructor/destructor dispatch and reentrancy/locking hazards;
- reason compositionally about preconditions, postconditions, and exception safety;
- evolve framework/subclass protocols compatibly;
- replace inheritance with Strategy/policies/pipelines when variation axes multiply;
- test base skeleton, every subclass, adversarial overrides, faults, cancellation, and resources.

## Core Exposition

### Begin with the invariant sequence

Write the algorithm as concrete steps and mark only decisions that truly vary. Validation, authorization, invariant restoration, metrics boundaries, transaction ownership, and cleanup normally stay fixed in the base.

If subclasses routinely need to skip/reorder invariant steps, the abstraction is wrong or the “invariant” is not invariant. Do not compensate with Boolean hook flags.

### Use a stable non-overridable entry point

Expose one public template method and make it final/non-virtual where the language supports it. Required variation points are protected/private virtual/abstract methods; external clients cannot call them out of lifecycle order.

Languages without enforcement rely on convention, module boundaries, composition, or metaprogramming checks. Document the limit rather than claiming the skeleton cannot be overridden.

### Distinguish primitives and hooks

A required primitive has no meaningful general default; declare it abstract and fail at construction/type-checking or immediately. An optional hook has a complete safe default such as identity transformation or no additional validation.

Do not make security, persistence, cleanup, or required output optional via empty hook. Hook names express responsibility: `split_records`, `normalize_token`, `after_commit_audit`—not `customize`.

### Contract each callback point

For every hook specify:

- base state/invariants visible on entry and after return;
- argument ownership, mutability, lifetime, and sensitivity;
- return relation and validation;
- allowed base/external mutations and reentrancy;
- invocation thread, count, order, concurrency, and repeat possibility;
- allowed failures, cancellation, timeout, and resource behavior.

Subclasses must not infer more from current source code. Treat protected APIs with the same compatibility discipline as public APIs.

### Preserve behavioral substitution

The base template promises a pre/post/error/resource contract. Each primitive implementation must fit the local obligation so their composition establishes the whole. An override cannot reject valid base inputs because its parser is narrower unless the subclass type advertises a narrower separate contract.

Validate cheap postconditions after hooks. If a split primitive returns empty tokens where the family forbids them, reject before later stages.

### Avoid dispatch during construction/destruction

Calling overridable methods from constructors can reach subclass code before subclass fields are initialized, or language rules may dispatch only to a base implementation unexpectedly. Destruction has the reverse partial-object problem.

Construct inert valid objects, then invoke the template through a factory/start method after full initialization. Cleanup uses base-owned resource scopes rather than virtual calls from destructors.

### Maintain callback invariants

Before calling extension code, establish a documented stable base state. Do not expose a mutable half-transition. After return, validate result and restore/commit invariant before publication.

Never hold an internal lock across unknown hook code unless the contract and reentrancy are rigorously controlled. Prefer compute-plan under stable snapshot, call outside lock, then validate/versioned commit.

### Define exception safety

State the guarantee for each step: no-throw, basic (object remains valid), strong (no observable change on failure), or commit/no-return. Acquire resources in scopes, record which steps completed, and run cleanup in reverse dependency order where appropriate.

Cleanup failures need policy: preserve primary failure, aggregate, log/alert, or make cleanup retryable. Avoid masking the original error. Idempotent cleanup tolerates repeated attempts but still needs identity and ownership.

### Handle transactions and effects

A local template cannot atomically wrap independent databases/services. Keep owned transactional changes inside one boundary and emit durable intent for external steps. Model later completion/failure rather than holding a transaction while a hook calls a network.

If hooks may have effects, define stable operation identity, authorization, timeout, retry, compensation, and indeterminate outcomes. Prefer hooks return plans/data and the base applies effects centrally.

### Support asynchronous templates explicitly

Mixing synchronous skeletons with async hooks causes blocking, lost cancellation, or cleanup races. Define one async template whose steps are awaited in order, with one deadline/cancellation context and cleanup shield policy.

Cancellation can occur between any two steps or during a hook. Specify which commits are irreversible, what cleanup runs, and whether abandoned hook work can still complete.

### Prevent subclass explosion

If parsing format, validation policy, persistence target, retry, and output format vary independently, subclasses create a Cartesian product. Extract Strategy/policy objects for independent axes and let one template coordinate them—or build an explicit pipeline.

Inheritance is strongest when one cohesive subtype identity supplies a small set of correlated primitives and the base skeleton is genuinely stable.

### Evolve the base safely

Adding/reordering/repeating a hook is behaviorally breaking if subclasses have effects or call-count assumptions. Adding an abstract primitive breaks all implementations; adding an optional hook with a truly safe default can be compatible but still changes timing/state.

Version the framework contract, publish call-sequence guarantees, maintain compatibility fixtures/third-party test kits, deprecate before removal, and test old subclasses against new bases and new subclasses against supported bases.

### Secure extension points

Subclass/plugin code runs with process privileges unless isolated. Allowlist implementations, validate provenance/signatures as required, restrict capabilities/data, bound CPU/memory/time/output, and avoid passing secrets or broad service locators.

In-process language access modifiers are not a security sandbox. Untrusted extensions require process/container/WASM-style isolation plus an authenticated protocol, and even isolation needs resource and side-channel review.

### Test the framework as a protocol

Instrument a probe subclass to record exact call order/arguments/state. Test base validation before hooks, normalization/postvalidation, zero/one/many items, each required primitive, optional defaults, adversarial returns, exceptions at every step, reentrancy, concurrent calls, cancellation, timeout, partial acquisition, cleanup order/failure, and repeat invocation.

Run the common contract suite against every production subclass. Mutation testing is useful for confirming tests detect skipped validation/cleanup or reordered steps. Load/soak and leak tests cover resource-owning templates.

## Definitions and Notation

Let base invariant (I(z)), input precondition (P(x)), final postcondition (Q(x,y)), and step contracts (K_i=(P_i,Q_i,F_i,R_i)) for pre/post, failure, and resource behavior.

For sequence (f_n\circ...\circ f_1), compositional proof requires (Q_i\Rightarrow P_{i+1}), each step preserves the required invariant, and failure edges satisfy the cleanup relation (C_i). Success is

\[
P(x)\Rightarrow Q(x,T(x))\land I(z_{final}).
\]

Call trace (	au=[validate,prepare,primitive,normalize,postvalidate,commit,cleanup]) is part of the behavioral contract only where explicitly promised. Undocumented trace details are not subclass rights.

## Mechanisms, Invariants, or Proof Structure

### Template Method design procedure

1. Write the stable algorithm and identify base-owned invariants.
2. Expose one non-overridable public entry point where possible.
3. Define minimal required primitives and safe optional hooks.
4. Contract callback state, data, calls, effects, failure, cancellation, and resources.
5. Validate hook results and centralize commit/cleanup/effects.
6. Avoid construction/destruction dispatch and unsafe locks/reentrancy.
7. Extract independent variation axes into composition/policies.
8. Test call protocol, every subclass, faults/cancellation/resources, and base/subclass compatibility.

### Executable mechanism

This token template owns validation, preparation, normalization, and result checks; subclasses vary only splitting. Python does not enforce `run` as final, so non-overridability is a documented limitation of this example.

<!-- bijux-verify: {"id":"template-token-pipeline","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"spaces=('alpha', 'beta', 'alpha')\ncsv=('alpha', 'beta', 'alpha')\ninvalid=empty token sequence\n","stderr":""}} -->
```python
class TokenTemplate:
    def run(self, text):
        source = self.prepare(text)
        parts = self.split(source)
        tokens = tuple(self.normalize(part) for part in parts)
        if not tokens or any(not token for token in tokens):
            raise ValueError("empty token sequence")
        return tokens

    def prepare(self, text):
        return text.strip()

    def split(self, source):
        raise NotImplementedError("split is required")

    def normalize(self, token):
        return token.strip().lower()


class WhitespaceTokens(TokenTemplate):
    def split(self, source):
        return source.split()


class CsvTokens(TokenTemplate):
    def split(self, source):
        return source.split(",")


print(f"spaces={WhitespaceTokens().run(' Alpha beta ALPHA ')}")
print(f"csv={CsvTokens().run(' Alpha, Beta,ALPHA ')}")
try:
    WhitespaceTokens().run("   ")
except ValueError as error:
    print(f"invalid={error}")
```

### Compositional argument

Both concrete splitters return finite sequences for shown strings. Base normalization strips/lowercases every part. Postvalidation requires a nonempty tuple with every token nonempty. Both valid inputs yield identical three-token tuples; blank whitespace prepares to empty, splits to empty, and fails postvalidation.

This argument covers only finite pure strings and shown subclasses. It assumes terminating hooks and no override of `run`; Python does not enforce that assumption.

### Evidence layers

Review skeleton/step contracts, every override, failure/resource behavior, concurrency/async execution, extension security, and framework evolution independently. A happy-path subclass test is not proof of the framework protocol.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation | Prefer when |
|---|---|---|---|
| Duplicated concrete algorithms | Local clarity | Invariant sequence drifts | Few tiny stable cases |
| Template Method | Base controls skeleton | Inheritance/fragile-base coupling | Stable sequence, cohesive subtype variation |
| Strategy/composition | Runtime choice, independent axes | More wiring/interfaces | Whole step/algorithm varies independently |
| Higher-order pipeline | Explicit functional composition | Effects/state contracts still needed | Pure transformations and language support |
| Middleware/chain | Extensible ordered stages | Ordering/short-circuit complexity | Open stage set and request processing |
| Workflow engine | Durable state/timers/recovery | Infrastructure/determinism constraints | Long-running cross-boundary sequence |
| Code generation | Uniform skeleton, static output | Generator/tooling/debug complexity | Many mechanical variants |

## Failure Modes and Misconceptions

- **“Template Method removes duplication.”** Its purpose is controlled variation under one invariant sequence.
- **“Protected means internal.”** Protected hooks are subclass-facing APIs with compatibility obligations.
- **“Empty hooks are always safe.”** Required security, persistence, or cleanup must not default to omission.
- **“Subclasses can call primitives directly.”** That bypasses validation/order/cleanup and defeats the pattern.
- **“Constructor hooks initialize subclasses.”** They can observe partial objects or language-specific dispatch.
- **“A final method makes overrides safe.”** Primitive contracts and base callback state still require proof/testing.
- **“Catching exceptions completes cleanup.”** Resources/effects require scoped, ordered, failure-aware cleanup.
- **“One template transaction covers remote calls.”** Independent authorities require durable coordination/reconciliation.
- **“Async hooks fit a sync skeleton.”** Awaiting, cancellation, deadlines, and cleanup change the protocol.
- **“More hooks mean flexibility.”** They expand the behavioral API and fragile-base surface.
- **“Inheritance handles independent options.”** It creates combination subclasses; use composition.
- **“Base tests cover subclasses.”** Every implementation and adversarial behavior needs the common contract suite.

## Worked Examples

### Example 1

Whitespace and CSV splitters share preparation, normalization, and postvalidation and return the same tuple for equivalent input. **Conclusion:** Vary one primitive under one semantic result contract.

### Example 2

A required persistence primitive has an empty default; a subclass “succeeds” while storing nothing. Making it abstract exposes incompleteness. **Conclusion:** Required work must fail fast, not default away.

### Example 3

A base constructor calls `validate`, which reads a derived field initialized only afterward. Factory construction followed by explicit `run` avoids partial-object dispatch. **Conclusion:** Do not invoke overridable behavior during construction/destruction.

### Example 4

A base holds a lock and a hook calls back into the public template, deadlocking or recursing. Snapshot/commit base state and invoke hooks outside unsafe locks with a reentrancy policy. **Conclusion:** Callback boundaries need stable state and lock discipline.

### Example 5

The third step fails after opening two resources. Scoped acquisitions close in reverse order and preserve the primary error while reporting cleanup failure separately. **Conclusion:** Failure paths are part of the skeleton.

### Example 6

A new base release calls a hook twice for batching; a subclass charges per call. The “optimization” duplicates effects. **Conclusion:** Hook call count/order changes can break subclasses.

### Example 7

Format, validator, storage, and retry each have three choices, implying (3^4=81) subclasses. Four injected policies reduce the cross-product type explosion. **Conclusion:** Compose independent variation axes.

### Example 8

An async hook ignores cancellation and finishes writing after the template reports cancelled. One propagated deadline plus shielded/awaited cleanup and explicit commit boundary repairs semantics. **Conclusion:** Async cancellation is an end-to-end protocol.

### Example 9

An untrusted plugin hook receives a database/session service locator. Access modifiers cannot contain it; narrow data/capabilities or process isolation are required. **Conclusion:** Inheritance is not a security sandbox.

### Example 10

A surgical workflow template enforces call order but lacks clinical evidence, team roles, exceptions, timing, and independent safety controls. **Conclusion:** Algorithm skeleton correctness is not clinical safety.

## Cross-Program Connections

- **Object-Oriented Programming:** inheritance, protected APIs, dispatch, construction, and behavioral subtyping implement the pattern.
- **Programming Languages and Semantics:** pre/postconditions, effect systems, exception safety, and evaluation order formalize hooks.
- **Software Design and Domain Modeling:** invariants and ownership decide the stable skeleton and variation points.
- **Testing and Quality Engineering:** fixture lifecycles, protocol probes, fault injection, mutation tests, and compatibility kits apply.
- **Concurrency and Parallel Programming:** locks, reentrancy, async cancellation, and thread confinement constrain callbacks.
- **Security Engineering:** plugin provenance, capability minimization, isolation, resource limits, and data protection govern extensions.
- **Database Engineering:** transactions, outboxes, idempotency, and cleanup define durable template boundaries.
- **Cloud and Platform Engineering:** framework versioning, plugin rollout, quotas, telemetry, and rollback operate extensions.
- **API Engineering:** protected hooks behave like versioned APIs despite limited visibility.
- **Systems Engineering:** high-consequence sequences require domain, timing, hazard, and independent assurance evidence.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Template Method intent, structure, applicability, and consequences.
2. Barbara Liskov and Jeannette Wing, [“A Behavioral Notion of Subtyping”](https://doi.org/10.1145/197320.197383), *ACM TOPLAS* 16(6), 1994. Primary behavioral-subtyping and contract foundation.
3. David L. Parnas, [“On the Criteria To Be Used in Decomposing Systems into Modules”](https://doi.org/10.1145/361598.361623), *Communications of the ACM* 15(12), 1972. Primary information-hiding/changeability foundation.
4. Joshua Bloch, *Effective Java*, third edition, Addison-Wesley, 2018, ISBN 978-0-13-468599-1. Provides design/document-for-inheritance, construction, and API practice.
5. Bjarne Stroustrup and Herb Sutter, [C++ Core Guidelines: class hierarchy rules](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-virtual), living document updated 2026-06-14, accessed 2026-08-28. Provides virtual-interface, NVI, constructor/destructor, and hierarchy guidance with stated guideline limitations.
6. Oracle, [Java Language Specification §12.5: Creation of New Class Instances](https://docs.oracle.com/javase/specs/jls/se25/html/jls-12.html#jls-12.5), Java SE 25, accessed 2026-08-28. Defines initialization order and dynamic dispatch during construction for Java.
7. Python Software Foundation, [Python Data Model](https://docs.python.org/3/reference/datamodel.html), Python 3.14.7, accessed 2026-08-28. Defines class, method, inheritance, descriptor, and customization semantics relevant to the executable example.
8. Martin Fowler, *Refactoring: Improving the Design of Existing Code*, second edition, Addison-Wesley, 2018, ISBN 978-0-13-475759-9. Provides refactoring mechanics around extracting functions/classes and replacing inheritance/conditionals with composition where appropriate.

## Exercises

### Exercise 1

Trace the executable template and derive its step contracts and proof limits.

### Exercise 2

Design a failure-safe resource-processing template with acquisition, primitive processing, commit, and cleanup.

### Exercise 3

Diagnose a base framework that calls hooks in constructors, under locks, and after partial mutation; redesign its callback protocol.

### Exercise 4

Compare Template Method, Strategy, higher-order pipelines, middleware, and workflow engines for an importer family.

### Exercise 5

Review a high-stakes operational procedure encoded as Template Method without claiming domain safety.

## Answers to the Exercises

### Answer 1

Whitespace input prepares to `Alpha beta ALPHA`, splits into three parts, normalizes to lowercase stripped tokens, and passes nonempty/all-nonempty postvalidation. CSV input prepares similarly, splits on commas, then shared normalization yields the same tuple. Blank input prepares to empty, whitespace split returns no parts, and postvalidation raises `empty token sequence`.

Step contracts: prepare accepts string and returns stripped string; split must return a finite iterable of token-like strings without external effects; normalize maps each part to stripped lowercase; postvalidation requires at least one nonempty token. The argument covers shown pure strings/subclasses under terminating hooks and non-overridden `run`. Python does not enforce finality; it proves no arbitrary subclass, Unicode/domain tokenization, resource, concurrency, or production property.

### Answer 2

Public final `process(input,ctx)` validates/authenticates and creates an operation scope. It acquires resources one by one into scoped owners, recording acquisition; calls required `read/transform` primitives on owned immutable data; validates output; performs one owned transactional commit; records durable post-commit intent; then returns. Cleanup executes in reverse dependency order in `finally`/RAII for success, primitive failure, cancellation, validation failure, and partial acquisition. Commit makes a clear irreversible boundary.

Each hook declares no hidden commit/external effect, deadline/cancellation checks, memory/output limits, and typed errors. Cleanup is idempotent where repeated, bounded, and cannot mask primary failure; failures aggregate/alert with operation identity. External post-commit work uses outbox/idempotent workers rather than open transaction hooks. Test failure/cancel at every before/during/after step, acquisition 0..n, commit ambiguity, cleanup failure/double-call, reentrancy, concurrent calls, leaks, and crash recovery.

### Answer 3

Constructor hooks observe incomplete derived fields and make construction fail through overridable behavior. Hooks under locks can block/re-enter/deadlock. Hooks after partial mutation observe or publish broken base invariants. Replace with inert construction/factory validation, then a final public operation. Under lock/ownership, validate input/version, snapshot immutable hook input, and mark no externally visible half-state; release lock, invoke hook with narrow capabilities/deadline; reacquire and validate result/current version; atomically commit or conflict. Queue/reject nested calls explicitly.

Do not call hooks from destructor; base-owned resource scopes clean up. Document thread, call count/order, input lifetime, allowed effects/errors, cancellation, and callback base-state invariant. If hook must decide under lock, use a pure bounded function over copied state. Add adversarial subclasses that block, throw, recurse, retain/mutate input, return invalid data, and race; test construction/destruction, state visibility, lock order, conflict, cancellation, and cleanup.

### Answer 4

Use Template Method when all importers share a stable lifecycle—validate, parse, normalize, validate result, commit, cleanup—and format-specific primitives are cohesive. Use Strategy for independently selectable parser/normalizer/validator/persistence algorithms, especially runtime choice and combinable axes. Use higher-order pipelines for pure transformations where sequence itself is explicit data/code and inheritance adds little.

Use middleware when an open ordered set of cross-cutting request stages needs short-circuiting, while specifying order/errors/reentrancy. Use a durable workflow engine when import spans long time/processes, external effects, timers, retries, restart/operator recovery. A robust design may use a small local template coordinating injected pure strategies inside one transaction, then a durable workflow outside. Avoid multiplying subclasses for format×validation×storage×retry and never imply local cleanup rolls back remote effects.

### Answer 5

Define purpose, domain authority, actors/competence, inputs/provenance, preconditions, allowed variation, timing, resources, handoffs, exception/escalation, stop/abort, independent controls, outputs, and exact safety claim. Map every invariant step and hook to authoritative requirements; ensure optional hooks cannot omit required protection and overrides cannot weaken constraints. Model human, device, environment, and external-system state—not only software sequence.

Evidence requires hazard/risk analysis, requirements traceability, domain review of each step/hook, formal sequence/state/timing analysis where tractable, simulation/reference cases, fault injection at every boundary, hardware/workflow/human-factors trials, cybersecurity/privacy review, resource/overload/degraded-mode tests, audit/configuration/version controls, drills, and controlled release/rollback. Named domain/clinical or controls, safety, verification, human-factors, security, quality/regulatory, and operations reviewers approve. Template ordering and software tests alone establish no clinical/functional safety or regulatory fitness.
