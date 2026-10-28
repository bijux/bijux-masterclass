# Review Engine — Course 3 capstone

The capstone supports the course-book. It exists to force cross-layer transfer after each mechanism has been understood in isolation.

## Product

**Review Engine** is a policy evaluation engine with static boundaries, a dynamic rule registry, and typestate construction.

## Ten increments

1. **Module 21:** Define the Review Engine's source, rule, and reporter contracts with behavioral laws. Separate required methods from defaults and identify what tests must enforce.
2. **Module 22:** Attach item, output, and error families to the implementations that choose them. Use associated types where callers should not select arbitrary combinations.
3. **Module 23:** Add local adapters, closure-backed rules, and sealed built-in markers without violating coherence. Record which crate owns every implementation relationship.
4. **Module 24:** Keep source and reporter boundaries statically dispatched, using the weakest sufficient bounds and opaque types only where concrete names would leak irrelevant detail.
5. **Module 25:** Introduce the ordered heterogeneous rule registry with `Box<dyn Rule>`. Document what is erased, why runtime heterogeneity is required, and how object lifetimes are owned.
6. **Module 26:** Compose parsing, policy, evaluation, and reporting through owned components and adapters. Do not invent an inheritance hierarchy for responsibilities that can be delegated.
7. **Module 27:** Build the engine through typestate so execution is unavailable until source, policy, and reporter are present. Keep the state machinery out of the finished engine's public behavior.
8. **Module 28:** Add narrow ports, production adapters, fakes, and conversion boundaries. Each trait must correspond to a real substitution need rather than a desire to mock everything.
9. **Module 29:** Review the public extension surface from both downstream perspectives: callers and implementors. Preserve evolution room with sealing, non-exhaustive data, and compatibility tests.
10. **Module 30:** Implement an unseen Review Engine extension and update the variation map first. Defend why each boundary uses an enum, generic, trait object, closure, or concrete type.

## How to use the capstone

Do not read the finished implementation before attempting an increment. Begin with the public behavior, write the failure-path test, identify the types whose invariants change, and then implement the smallest coherent change. After the change passes, inspect the finished code to compare architecture rather than copy syntax.

## Complete engineering guide

### Product contract before abstraction

Review Engine evaluates an ordered list of submissions against an ordered policy. Each policy line constructs one rule. Every submission is evaluated against every rule in policy order. A rule may emit zero or more findings. Error-severity findings reject the review; warnings and informational findings remain visible without changing acceptance. The same valid inputs must produce the same findings in the same order and the same rendered report.

The command-line product exposes four operations:

```text
review-engine check <submissions.tsv> <policy.txt>
review-engine list-rules
review-engine explain <rule-name>
review-engine demo
```

`check` exits with status `0` when evaluation completes and no error-severity finding exists, status `1` when evaluation completes with at least one rejecting finding, and status `2` when usage, source loading, policy construction, or report production fails. A malformed source or policy must not produce a partial review that looks complete.

Write this behavior down before choosing traits. Traits are not the product. They are one way to represent particular variation pressures inside the product. The architecture is correct only when each abstraction corresponds to a real choice that the application must support.

### Begin with a variation map

Before writing a trait, classify every place where behavior or data can vary.

| Pressure | Selection time | Required relationship | Mechanism |
|---|---|---|---|
| submission source | engine construction | one item and error family per source | generic `Source` with associated types |
| report destination | engine construction | one output and error family per reporter | generic `Reporter` with associated types |
| policy rule kinds | policy parsing at run time | heterogeneous ordered values behind one callable contract | `Vec<Box<dyn Rule>>` |
| severity | fixed by the product | exhaustive closed alternatives | enum |
| builder readiness | compile time | `build` only after three required components exist | typestate parameters |
| policy-line construction | registry construction plus run-time lookup | name maps to validated rule construction | `RuleFactory` trait and registry |
| ad hoc callback rule | engine construction | local closure plus stable rule identity | `RuleFn<F>` newtype adapter |
| built-in status | library-owned classification | downstream code must not claim it | sealed marker trait |

This table prevents two opposite mistakes. The first is an “everything is generic” engine whose concrete type records the entire policy. That cannot naturally represent a policy file that chooses heterogeneous rules at run time. The second is an “everything is boxed” engine that erases source errors, reporter output, and compile-time construction state even though those relationships remain useful to callers.

The variation map is also a change-impact tool. When a new requirement arrives, ask whether the selection time or relationship changed. Only then reconsider the mechanism.

### Domain types own the invariant

The core domain does not begin with traits. It begins with values whose invalid states are difficult or impossible to construct.

`SubmissionId` accepts one to sixty-four ASCII letters, digits, hyphens, or underscores. `RuleId` uses lowercase ASCII letters, digits, and hyphens. These newtypes prevent raw strings from crossing boundaries after validation and stop unrelated identifiers from being interchanged accidentally.

`Submission` owns its identifier, owner, score, normalized tags, and title. Fields remain private. Construction rejects an empty owner and titles containing tab or line-break characters because the input and output protocols are tabular. Tags are trimmed, normalized to lowercase, sorted, and deduplicated once. `has_tag` can then use binary search without repeating normalization policy in every rule.

`Severity` is an enum because the product defines a closed set with an explicit order. A trait would add extension complexity without product value. `Finding` records stable domain identity—submission ID, rule ID, severity, and message—rather than storing a reference to the concrete rule object. The report therefore remains valid after rule evaluation and does not need downcasting.

`Review` owns the final findings and derives acceptance from the presence of error-severity findings. It does not cache a separate mutable `accepted` flag that could disagree with the findings. Derived facts should remain derived unless measurement proves recomputation is a problem.

### `Rule` is a small behavioral contract

A rule needs two operations: stable identity and evaluation.

```rust
pub trait Rule {
    fn id(&self) -> &RuleId;

    fn evaluate(
        &self,
        context: &EvaluationContext<'_>,
        findings: &mut Vec<Finding>,
    );
}
```

The trait is intentionally smaller than a typical class-shaped interface. Construction does not belong in `Rule`; policy factories own construction. Rendering does not belong in `Rule`; reporters own rendering. Cloning, equality, serialization, and downcasting are not requirements, so the contract does not demand them.

The method is dyn-compatible: it has a receiver, no generic type parameters, no `Self` return, and no associated type that callers must name through the object. The borrowed context makes the submission lifetime explicit without storing it. A caller-owned output vector gives all implementations one concrete output surface and preserves append order.

The type system checks the method shape, but several semantic laws remain your responsibility:

1. `id` is stable for the lifetime of the rule.
2. Evaluation is deterministic for the same context.
3. Evaluation appends findings and does not remove or reorder earlier findings.
4. Every emitted finding names the current submission and the evaluating rule.
5. A successfully constructed rule does not panic on valid domain input.
6. Evaluation does not mutate the submission.

Test these laws against every built-in rule. A trait without laws is only a shared spelling.

`RuleExt` demonstrates a derived convenience method. It is blanket-implemented for every `Rule + ?Sized`, so concrete rules and trait objects gain `findings`. The extension trait remains separate because adding convenience to the required object-safe contract would unnecessarily freeze the public trait surface.

### Associated types preserve implementation families

A source chooses one item type and one error type for each implementation:

```rust
pub trait Source {
    type Item;
    type Error;

    fn load(self) -> Result<Vec<Self::Item>, Self::Error>;
}
```

The engine constrains `Item = Submission` but preserves the concrete error family. `MemorySource<Submission>` can use `Infallible`; a file source returns contextual `InputError`. The caller does not repeatedly choose a different item type for one source value, so associated types express the relationship better than method-level generic parameters.

A reporter similarly chooses one output and error family:

```rust
pub trait Reporter {
    type Output;
    type Error;

    fn report(&self, review: &Review) -> Result<Self::Output, Self::Error>;
}
```

A text reporter and TSV reporter both return `String` today, but the trait does not force that forever. A future writer-backed reporter may return a byte count or unit. The engine’s `RunOutcome<R::Output>` preserves this concrete output for static callers.

These traits remain statically dispatched because one source and one reporter are selected for an engine. There is no requirement to place different source types in one collection. Erasing them would lose useful output and error information without solving a real heterogeneity problem.

### Coherence determines where adapters live

Policy parsing needs to turn a textual rule name and arguments into a boxed rule. `RuleFactory` is local, so the crate can implement it for local factory types. A registry owns factories and resolves names. Each factory validates its own argument grammar and returns a fully constructed rule; invalid configuration never reaches the execution registry.

The architecture does not attempt to implement a foreign trait for a foreign type. When an external closure must behave as a rule, the local `RuleFn<F>` newtype owns the implementation:

```rust
pub struct RuleFn<F> {
    id: RuleId,
    function: F,
}
```

The newtype supplies stable identity and permits a lawful local `Rule` implementation. This is not boilerplate to eliminate blindly. It is the point where the application adds semantics that the closure alone does not carry.

A sealed `BuiltInRule` marker communicates a library-owned classification. Downstream crates may implement the open `Rule` contract, but they cannot claim that their type is a built-in rule. Sealing is appropriate because built-in status is not an extension point. Do not seal `Rule` itself: third-party rule implementations are a deliberate requirement.

Blanket implementations require special restraint. An implementation that is legal today may overlap with a downstream implementation tomorrow or prevent the library from adding a more specific implementation. Before adding a blanket impl, describe the complete set of types it covers and the implementation space it consumes.

### Erase rules only at the heterogeneity boundary

`Policy` owns `Vec<Box<dyn Rule>>`. The vector is not a default “OOP” container; it is the direct representation of two product requirements: rule kinds are heterogeneous, and policy order is runtime data.

Concrete rule construction happens before erasure. After a factory validates configuration, the rule is boxed and inserted. Execution requires only `id` and `evaluate`, so the erased contract is sufficient. The registry never downcasts during ordinary execution. If the engine needed variant-specific reporting, serialization of concrete configuration, or exhaustive matching over a closed rule set, an enum could be better.

Maintain an erasure ledger:

| Information | Kept after erasure? | Why |
|---|---:|---|
| stable rule ID | yes | findings and diagnostics require it |
| evaluation behavior | yes | virtual dispatch calls it |
| concrete rule type | no | execution does not need it |
| constructor arguments | not necessarily | validated state is stored inside the concrete object |
| factory name | registry only | construction concern, not evaluation concern |
| source error type | not erased | source remains generic |
| reporter output type | not erased | reporter remains generic |

This ledger turns “use a trait object” into an explicit information decision.

### Typestate applies only to a short local protocol

An engine cannot run until it has a source, reporter, and validated policy. `EngineBuilder<S, R, P>` represents those three readiness dimensions with `Missing` and `Present<T>` marker states. Each setter consumes the builder and changes one type parameter. `build` is implemented only for:

```rust
EngineBuilder<Present<S>, Present<R>, Present<Policy>>
```

The compiler therefore rejects an incomplete construction before runtime. No Boolean readiness flags can drift out of sync, and `build` does not need to return “missing source” errors.

Typestate is bounded deliberately. Optional formatting settings do not become state parameters. File existence and source validity remain runtime errors because they depend on external data. A public typestate design is justified only when invalid operation order is a frequent programmer error, the state graph is small, and consuming transitions are natural.

The builder is not inheritance. It is a generic state machine whose method set changes with its type parameters.

### Error architecture follows responsibility

`InputError` preserves a path for I/O failures and physical line numbers for invalid or duplicate submissions. `PolicyError` preserves policy line and rule name. `ReportError` belongs to the reporting boundary. `RunError<S, R>` preserves the concrete source and reporter error families instead of flattening them into strings.

Rule evaluation is infallible after construction. This is a product decision, not a universal trait pattern. Built-in rules inspect already validated domain data and append findings; expected policy violations are findings, not engine failures. If a future rule must call an unreliable service, the contract has changed. Possible responses include a versioned fallible rule trait, an explicit operational-failure finding category, or a separate effectful rule boundary. Do not silently smuggle operational failure into a message string.

The application must preserve failure atomicity at its own boundary. Source or policy construction errors occur before a `Review` exists. A reporting failure may occur after evaluation, so `RunError::Report` must not be confused with policy rejection. Exit status `1` means a valid completed review rejected submissions; exit status `2` means the command could not complete its contract.

### Determinism is an architectural law

Deterministic output follows from explicit order at every layer:

1. source parsing preserves physical submission order;
2. the policy vector preserves policy-file order;
3. the engine loops over submissions outside and rules inside;
4. each rule appends findings without reordering prior output;
5. reporters iterate the final vector directly;
6. registry names use registration order rather than hash-map order.

This law is visible in the implementation and testable at public boundaries. Do not claim determinism merely because one test run happened to be stable. Add fixtures with several submissions and several rules, then assert the complete finding sequence and rendered bytes.

### Ten implementation increments

#### 1. Domain and contract vocabulary

Implement validated IDs, `Submission`, `Severity`, `Finding`, and `Review`. Keep fields private. Test normalization, rejected construction, derived acceptance, and deterministic severity rendering.

#### 2. Associated source and reporter families

Define `Source` and `Reporter`. Implement memory and text boundaries first. Write generic helper tests that demonstrate concrete error and output types remain available.

#### 3. Coherence-safe policy factories

Define `RuleFactory` and `RuleRegistry`. Add local factory types for the first built-in rule. Reject unknown names, malformed arguments, and duplicate factory registration without constructing a partial policy.

#### 4. Static engine shell

Implement an engine generic over source and reporter with a temporary concrete rule representation. This step makes the generic outer architecture work before dynamic dispatch is introduced.

#### 5. Dyn-compatible rule contract

Derive the smallest `Rule` trait from execution needs. Convert the policy to `Vec<Box<dyn Rule>>`. Add compile-fail examples for a generic rule method and an associated function without a receiver, then explain why each prevents dynamic dispatch.

#### 6. Composition and adapters

Add `EvaluationContext`, `RuleExt`, and the `RuleFn<F>` closure adapter. Verify that a closure rule carries a stable ID and obeys the same contract tests as named rule types.

#### 7. Typestate construction

Replace runtime missing-component checks with `EngineBuilder<Missing, Missing, Missing>`. Add rustdoc compile-fail examples proving that incomplete builders do not expose `build`.

#### 8. Boundary parsing and reporting

Implement TSV source parsing, file source errors, text and TSV reports, and CLI argument parsing. Keep parsing, engine execution, and output effects in separate layers.

#### 9. Public evolution review

Audit every public trait. Record who may implement it, whether it must remain dyn-compatible, which methods are required, which conveniences belong in extension traits, and what future additions would be breaking. Seal only classifications that are not intended extension points.

#### 10. Independent architectural change

Add one requirement that crosses at least three mechanisms—for example, warning-only policy mode, structured explanations, or a second reporter output family. Update the variation map before code. The mechanism may change only when the selection time or required relationship changes.

### Test the contracts, not the concrete layout

Use several layers of tests:

- **domain tests** for validation, normalization, private invariants, and derived acceptance;
- **contract tests** applied to every rule implementation;
- **factory tests** for argument grammar, duplicate IDs, and unknown names;
- **engine tests** for nested ordering and correct separation of rejection from operational failure;
- **public integration tests** that use only exported APIs;
- **process tests** for commands, standard output, standard error, and exit status;
- **compile-fail documentation tests** for incomplete typestate construction and dyn-incompatible alternatives;
- **determinism tests** that compare complete ordered output.

Avoid tests that depend on a trait-object vtable layout, concrete monomorphized symbol names, or undocumented enum representation. Test semantic contracts, not incidental compiler artifacts.

### Rejected designs and when they would become valid

#### One `Engine` trait

There is only one orchestration algorithm. A trait would create an extension point with no second implementation and would obscure the real variation boundaries. Introduce one only when distinct engine strategies must be substituted by callers.

#### An enum for every rule

An enum is excellent when the rule set is closed and exhaustive matching has value. It is rejected here because rule kinds and order are runtime-extensible. It would become preferable if third-party extension were removed and configuration serialization required exhaustive variant knowledge.

#### Trait objects for source and reporter

Erasing these boundaries would hide output and error families that callers use. It would become justified only if heterogeneous sources or reporters had to coexist in one runtime collection behind one common output contract.

#### Typestate for every option

Encoding optional formatting and policy toggles in type parameters would multiply states without removing serious misuse. Typestate is reserved for the three required construction components.

#### Downcasting rules

Downcasting reintroduces concrete type knowledge after erasure and usually signals that the erased contract omitted required behavior. Add a named contract method or reconsider an enum before adding `Any`-based branches.

#### Broad blanket implementations

A blanket `impl<T> Rule for T where ...` can consume implementation space and create accidental semantics. Use a local adapter newtype when the application must add identity or policy to a foreign callable.

### Final architecture review

You should be able to answer these questions from the public API and a small architecture diagram:

1. Why are source and reporter generic while rules are erased?
2. Which type chooses each associated type, and when is that choice made?
3. Why is `Rule` dyn-compatible? Which plausible additions would break that property?
4. Which semantic laws are not enforced by the compiler, and where are they tested?
5. Which crate owns every implementation, and which implementation space remains open downstream?
6. What information is deliberately erased at the policy boundary?
7. Which invalid builder states are unrepresentable, and which failures correctly remain runtime concerns?
8. Why is the finding sequence deterministic?
9. Which public changes would break callers, implementors, or both?
10. Under what changed requirement would an enum, closure, ordinary function, or concrete type be simpler than the current trait?

The capstone is complete when those answers agree with the code, all public behavior is tested, an independent change can be made without collapsing boundaries, and no abstraction exists only because the course recently introduced its syntax.

## Module-to-product traceability

Review Engine is useful because each variation mechanism has one bounded responsibility. The table is an architecture contract, not a retrospective description:

| Module | Product change | Invariant introduced | Regression proof |
|---:|---|---|---|
| 21 | define the narrow `Rule` contract and law vocabulary | every rule has stable identity and deterministic evaluation for one context | run shared rule-law tests against every built-in rule and one closure adapter |
| 22 | give `Source` and `Reporter` implementation-owned item/output/error families | one implementation chooses one coherent family; callers do not select contradictory associated types | compile memory, TSV, file, text, and TSV-report combinations through the same engine shell |
| 23 | keep adapters local and register rule factories without illegal foreign implementations | the crate that owns the adapter owns the implementation and no blanket impl consumes unintended coherence space | compile a downstream-style fixture using only public adapters |
| 24 | keep source and reporter generic | concrete source/report types remain available to the compiler and no runtime erasure is paid where heterogeneity is absent | assert distinct source and report errors survive in `RunError<S, R>` |
| 25 | erase only heterogeneous rules | policy order may contain several concrete rules while source and reporter remain statically typed | parse a mixed policy and verify ordered findings |
| 26 | compose registry, policy, engine, source, and reporter rather than creating an inheritance tree | each component has one replacement reason | replace the reporter without modifying rules or source parsing |
| 27 | use typestate only while source, policy, and reporter are missing | `build` is unavailable until all three components are present | keep a documentation compile-fail example for the incomplete builder |
| 28 | translate TSV/files and output formatting at boundaries | domain types never depend on filesystem or textual layout details | unit-test parsing separately from rule evaluation and reporting |
| 29 | seal only the built-in-rule marker and keep `Rule` externally implementable | callers may add rules while the crate retains freedom over “built-in” classification | compile a public closure rule and a custom downstream-style rule |
| 30 | freeze deterministic ordering and the full variation map | input order × policy order determines finding order | run the same review twice and compare byte-for-byte reports |

If one future feature requires changing several unrelated rows, the architecture may have hidden coupling. Review the variation map before adding another trait.

## End-to-end execution trace

A complete run has six distinct phases:

1. **Source acquisition.** `S: Source<Item = Submission>` consumes its source value and either returns validated submissions or a source-specific error. File I/O and TSV parsing end here.
2. **Policy construction.** `RuleRegistry` translates policy text through local factories into an ordered `Policy`. Duplicate rule identifiers are rejected before evaluation.
3. **Engine construction.** `EngineBuilder` consumes missing/present states. Once all three components exist, `build` erases the construction protocol into `Engine<S, R>`.
4. **Evaluation.** For each submission, the engine creates a borrowed `EvaluationContext` and calls each `dyn Rule` in policy order. Rules append findings; they do not perform source I/O or reporting.
5. **Review construction.** The engine owns the complete finding vector and derives acceptance from the presence of error-severity findings.
6. **Reporting.** `R: Reporter` consumes or borrows the review according to its contract and returns an implementation-specific output or error.

Write this trace before debugging. It identifies which layer owns a failure. An invalid TSV row is not a rule failure. An unknown rule name is not a source failure. A reporter error occurs after a valid review exists, so retry policy must not accidentally rerun non-idempotent evaluation if future rules gain effects. In this course, rules remain deterministic and effect-free, keeping that concern outside the contract.

## Error architecture

Review Engine intentionally preserves separate error families:

```text
InputError   source acquisition and submission syntax
PolicyError  policy grammar, unknown factories, duplicate rule identity
RunError<S,R>
  Source(S)  concrete source implementation failed
  Report(R)  concrete reporter implementation failed
```

Do not collapse these into one string. The caller may need to distinguish an unreadable file from a policy authoring error or a report destination failure. Conversely, do not create a trait merely to unify errors that no caller handles uniformly. `RunError<S, R>` preserves the static source/reporter families without requiring a global application error hierarchy.

A rule records domain findings rather than returning ordinary control-flow errors. That distinction is deliberate: a low score or missing tag is a completed evaluation result, while inability to load submissions prevents evaluation from beginning.

## Determinism and law testing

The engine’s public behavior depends on semantic laws not expressible by method signatures:

- rule identifiers remain stable and valid;
- one rule does not remove findings produced by another;
- policy order is preserved;
- source order is preserved;
- reporters render the supplied review rather than reevaluating rules;
- repeated runs over equal values produce equal findings and output;
- validation constructors preserve their stated normalization rules.

Write reusable tests around these laws. A test for one built-in rule proves its example, not the `Rule` contract. Run contract tests against several structurally different implementations, including `RuleFn`, so a default or blanket implementation cannot hide a law violation.

## Public API evolution review

Before releasing a change, review two downstream roles separately:

| Role | Questions |
|---|---|
| caller | Do existing construction, matching, method calls, and trait-object uses still compile and preserve meaning? |
| implementor | Can existing external `Rule`, `Source`, `Reporter`, or `RuleFactory` implementations still satisfy the contract without new obligations? |

Examples:

- Adding a required `Rule` method breaks implementors even if callers are unchanged.
- Adding a default method may collide with an existing inherent or extension method.
- Strengthening `Rule: Send + Sync` would reject single-threaded implementations without Course 3 having established a concurrency requirement.
- Adding a broad blanket implementation may overlap a downstream implementation that was previously legal.
- Adding a variant to a public exhaustive enum can break callers; a private representation with accessors preserves more evolution room.

The current design keeps `Rule` small and externally implementable, seals only the `BuiltInRule` classification, and uses constructors to protect domain newtypes. Preserve that distinction.

## Independent architecture change

Add a configurable **maximum findings per submission** without copying a finished patch.

First decide where the policy belongs. It is not a new `Rule`: it controls evaluation orchestration rather than describing one domain check. It is not a reporter option: reporting occurs after findings exist. A reasonable design places the limit in engine configuration, validates nonzero values, and stops evaluating later rules for one submission after the limit is reached while preserving submission and policy order for all observed findings.

Required change analysis:

1. state whether the builder needs another typestate parameter or an ordinary optional/default field;
2. define whether reaching the limit creates a warning finding, a run error, or silent truncation—then justify the public contract;
3. update deterministic-order tests;
4. prove that a reporter cannot bypass the limit;
5. document whether external rules may observe that later rules were skipped;
6. review whether the change is source- or behavior-breaking for existing callers.

The preferred answer normally keeps the limit as ordinary validated configuration with a documented default. Typestate would be disproportionate unless the product requires every caller to choose a limit explicitly before `build`.

## Final architecture defense

Defend the finished product without reading source line by line. Draw:

- the variation map showing who chooses source, reporter, rule kind, and policy order;
- the static/dynamic dispatch boundary;
- the typestate construction graph and erasure point;
- the error-family map;
- the deterministic execution order;
- the downstream caller/implementor matrix.

For every trait, answer: why is this a shared behavioral contract rather than an inherent method, enum, free function, or closure parameter? For every trait object, answer: which heterogeneity requires erasure and what information is lost? For every generic parameter, answer: which static relationship benefits from remaining visible? If those answers are unclear, simplify the architecture before adding features.

## Acceptance route

From the course root:

```bash
cargo test -p review-engine
cargo clippy --workspace --all-targets -- -D warnings
cargo fmt --all -- --check
```

The program should also pass the manual demonstration described in [`capstone/README.md`](../capstone/README.md).
