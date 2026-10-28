---
module_id: FP-002
program: Programming Languages: Functional Programming
level: 1
module_number: 2
title: Pure Functions and Explicit Inputs
status: complete
last_verified: 2026-08-29
---

# Pure Functions and Explicit Inputs

## One-Page Review

### Governing question

How can a computation expose every fact that influences its result while producing no hidden observable change?

### Essential definitions

- A **pure function** denotes a mapping from admitted input values to result values without consulting or changing hidden observable state.
- An **explicit input** is a value visible in the function's semantic interface: an argument, a component of an argument record, or an immutable value fixed when the function itself is created.
- A **hidden input** is an undeclared dependency whose current value can affect the result, such as ambient time, mutable configuration, process state, random sampling, locale, database contents, or filesystem data.
- A **side effect** is an observable interaction beyond returning the result, including mutation visible elsewhere, I/O, external calls, logging, metrics, process control, or consuming nondeterministic state.
- **Determinism** means the modeled input and environment select one modeled outcome. Determinism is necessary for a mathematical function but does not alone imply absence of effects.
- A **total function** returns a result for every value in its declared domain. A **partial function** is undefined, fails, or diverges for some apparent inputs.
- **Dependency completeness** means every varying fact needed to determine the result is represented in the input or in a separately modeled effect.
- An **effect description** is a pure value describing an interaction for an external interpreter; constructing the description does not itself perform the interaction.
- **Replayability** means retained inputs, code/policy identity, and numeric/language semantics suffice to recompute the same modeled result.

### Central model, mechanism, or theorem

For a pure total function \(f:X\to Y\),

\[
x_1=x_2\Longrightarrow f(x_1)=f(x_2),
\]

and evaluation changes no observable world state. If an apparent function depends on changing environment \(d\in D\), make that dependency explicit:

\[
g:X\times D\to Y,\qquad g(x,d)=y.
\]

Randomness can be represented as state transformation \(r:X\times Seed\to Y\times Seed\); fallible computation as \(h:X\to Result(Y,E)\); and intended commands as data \(p:X\to Y\times List(Command)\). The effectful boundary still has to obtain \(d\), execute commands, and record outcomes.

### Critical invariants

Equal complete inputs under one specified implementation and value semantics yield equal results. Evaluation does not mutate arguments, captured mutable state, globals, persistent state, or external systems. Returned mutable aliases do not let callers retroactively change a result observed elsewhere. Time, randomness, configuration, locale, identity, feature policy, and reference data are explicit when they affect meaning. Failure and unsupported inputs are part of the result model or stated domain. Purity supports local reasoning but never proves that the formula, data, or policy is correct.

### Common failures

Typical failures are calling deterministic logging pure; passing an object while reading more data through globals; accepting a clock or random-number generator and calling the whole operation pure; mutating an input “temporarily”; returning a shared mutable cache value; hiding policy in a process singleton; omitting code, model, or reference-data versions from replay; assuming exceptions make a function impure or, conversely, treating every throwing API as total; and inferring clinical, financial, or legal correctness from reproducibility.

### Compact example

`quote(subtotal, tax_policy, discount)` is locally reasoned about only if currency rounding, rate, discount, and numeric domain are fixed by those values. If it reads today's rate or mutable locale behind the same signature, repeated calls can differ. Capturing one verified policy snapshot at the boundary and passing it explicitly turns a changing environmental fact into stable input; it does not prove the policy is lawful.

### Connections

[FP-001](001-expressions-values-and-referential-transparency.md) establishes substitution and observation. [Later Block 01 modules](../ROADMAP.md) add higher-order functions, closures, composition, evaluation strategy, and immutability. Explicit state, reader-style dependencies, I/O boundaries, and pure-core architecture belong to FP-041 through FP-050. [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) turns pure laws into properties without mistaking samples for proofs.

## Governing Question

What must appear in a function's interface so that its result can be explained entirely from supplied values, and what must be excluded so that evaluation remains observationally inert?

“Same input, same output” is useful but incomplete. A procedure can always append the same audit record and remain deterministic. A function can receive an immutable argument while reading a changing global. A memoized function can return one mutable list that later callers alter. A pure function needs both dependency completeness and effect exclusion, interpreted under an explicit observation model.

Purity is also a semantic property rather than a language label. Haskell is designed so ordinary expression evaluation remains pure while `IO` values describe interactions. Rust, Java, Python, JavaScript, Scala, F#, and C# permit pure functions by discipline even though their type systems generally do not prove the absence of every effect. A reviewer therefore examines reachable operations, aliases, captures, runtime hooks, and foreign calls rather than trusting syntax.

## Why This Matters

Hidden dependencies enlarge the state a reader must reconstruct. A function named `price(order)` may secretly depend on exchange rates, tenant configuration, request time, feature flags, locale, inventory, and network responses. Its source signature advertises one input while its real semantic input is a changing subsystem. Tests need elaborate fixtures, production incidents cannot be replayed, cache keys are incomplete, and parallel evaluation can observe inconsistent worlds.

Explicit values turn that protocol into data. `price(order, policy_snapshot)` makes the chosen rate, rounding rule, currency, promotion, effective time, and version inspectable. Tests construct the exact case. Audit records retain it. A cache can include it in the key. A batch can pin one policy for consistent computation. The boundary that obtains the snapshot remains effectful, but the calculation stops pretending to own retrieval.

Pure functions also improve composition. A caller need not schedule locks or retries around a value calculation. Independent calls can run in any order under functional observations. Intermediate results can be named, substituted, compared, memoized, or recomputed. These benefits are conditional: resource exhaustion, divergence, floating-point modes, mutable aliases, and deliberately observed identity or timing still require separate reasoning.

Production software cannot eliminate interaction. It reads requests, clocks, random sources, files, databases, devices, and networks; writes responses and durable records; and reports operations. Functional design concentrates those activities at visible boundaries, converts observations into validated immutable values, calls a pure decision core, and then interprets returned decisions or command descriptions. FP-041 through FP-050 develop that architecture; this chapter establishes its smallest unit.

## Prerequisites and Retrieval

Retrieve FP-001's observation boundary, referential transparency, substitution accounting, and distinction between functional and cost observations. Know functions, tuples, records, sets, equality, preconditions, result variants, immutable values, and basic state-transition notation.

Remember that equality belongs to a domain. Two floating-point NaNs, two mutable objects, two normalized strings, or two function values need not have the equality a mathematical equation assumes. Also remember that an input value can contain references to mutable objects. A parameter is syntactically explicit without being a stable semantic value if another actor can mutate the reachable graph during evaluation.

No effect-system or monad knowledge is required. We use tuples and tagged results to expose dependencies, failures, state, and command descriptions. Later modules explain the abstractions that compose those patterns.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish purity, determinism, totality, referential transparency, idempotence, and thread safety;
2. reconstruct a function's real dependency set from code and runtime boundaries;
3. turn time, randomness, configuration, locale, reference data, and policy into explicit input values;
4. represent failure, state transition, and intended effects as result values;
5. identify mutable-input, mutable-output, closure-capture, cache, and foreign-call violations;
6. state the assumptions under which memoization, replay, reordering, or parallel evaluation is sound;
7. design a narrow effectful boundary around a pure calculation;
8. verify a deterministic executable example without generalizing beyond its domain; and
9. explain why purity cannot establish domain truth or high-stakes fitness.

## Core Exposition

A mathematical function assigns each element of a domain one element of a codomain. Programming functions add evaluation, representation, possible failure, and resource use. Calling a programming function **pure** asserts that its functional observation behaves like such a mapping: complete equal inputs select equal results, and evaluating the body creates no other observable change.

This definition has two halves. **Input completeness** requires every varying fact that influences the result to belong to the semantic input. **Effect freedom** requires evaluation not to modify or communicate through anything outside the returned value. A routine that reads a fixed immutable mathematical constant is still pure because the constant is part of its definition. A routine that reads a mutable “constant” whose deployment can change has a hidden input unless the version is captured in the function value and replay contract.

Determinism is weaker. A routine that always writes the same line to a log and returns 7 is deterministic under a full trace, but effectful. A routine that mutates a private local object and discards it can remain observationally pure if allocation identity, memory use, and mutation are outside the selected functional observation. Purity is not a ban on machine instructions that store bytes; it is a semantic noninterference claim.

Totality is independent. Integer division modeled only for nonzero divisors can be a pure partial function. A pure recursive definition can diverge. A function can deterministically raise the same exception without mutating external state, though exceptions complicate equational reasoning because control transfer is an observable outcome. Production APIs often improve the model by narrowing the input type or returning `Result`/`Either` so failure is an ordinary explicit value.

Idempotence is also different. An effectful `set_status("closed")` operation may be idempotent because repeating it has the same final external state, yet it performs I/O and can emit distinct logs. A pure function need not satisfy \(f(f(x))=f(x)\); negation is pure but applying it twice differs from once. Thread safety means concurrent calls avoid invalid races; a synchronized global counter can be thread-safe and impure.

An apparent parameter list rarely captures the whole dependency set. Follow every read reachable from the body: module globals, singleton configuration, environment variables, locale, timezone database, system clock, random generator, process identity, filesystem, database, network, mutable closure cells, caches, object properties, dynamic dispatch targets, callbacks, and foreign code. A dependency audit asks whether each item is immutable and fixed by the function definition, part of the supplied value graph, or an effect.

Explicitness is semantic, not merely syntactic. Passing `context` is not enough if the object lazily reaches a database or clock. Passing a `Clock` interface exposes authority to perform an effect, not a timestamp value. That can be excellent dependency injection for the effectful shell, but the called operation remains effectful. Passing `request_time: Instant` to the core supplies a stable value.

Time illustrates the boundary. The shell reads a trusted clock once and obtains an instant plus clock-quality metadata if relevant. It validates and passes that snapshot. The core compares dates and deadlines as values. If a long operation needs current time again, that second observation is another boundary event and should not be disguised as the same pure calculation.

Randomness can be made explicit in two ways. The shell can sample random values and pass them to the core. Or a pure generator can transform an explicit seed/state: \(next:Seed\to Value\times Seed\). The latter is deterministic and replayable for a pinned algorithm. It is not cryptographic safety merely because the state transition is pure; seed secrecy, entropy acquisition, algorithm suitability, state compromise, and versioning remain security obligations.

Configuration should be a validated value, not an ambient bag. Read environment files and feature services at the edge, resolve precedence, validate cross-field constraints, attach version/digest and effective scope, freeze the snapshot, and pass only fields the core needs. This prevents a single calculation from observing half of one rollout and half of another. It also reveals when two tenants or jurisdictions require different policies.

Reference data follows the same pattern. Tax tables, exchange rates, sanctions lists, clinical terminology, model artifacts, and routing maps have provenance, version, effective interval, and freshness. Passing only the extracted number can be sufficient for a narrow calculation but insufficient for audit. The input design should retain the evidence needed to explain why that value applied.

Mutable inputs create a subtle violation. A function can receive a list explicitly and still observe concurrent mutation or modify it in place. Copying on entry yields a snapshot only if the copy is deep enough and atomic relative to writers. Prefer immutable data or ownership that excludes aliases during evaluation. State the equality used for input keys.

Mutable outputs can invalidate caching and reasoning. If a pure-looking function returns a shared mutable list, one caller can change what another later observes for the same input. Return immutable values, unique owned values, or defensive copies with a documented identity policy. Internal memoization may remain observationally pure when cache hits do not change results or expose identity, ordering, timing, errors, or resource exhaustion under the selected observation.

Closures can be pure. A function created by `make_converter(rate)` may capture an immutable rate; semantically the produced function is parameterized by the captured value even though later calls show fewer arguments. Capturing a mutable rate cell makes future results depend on hidden state. FP-004 develops closure semantics; here the rule is to freeze or expose changing captures.

Effect descriptions separate decision from execution. A pure function can return `SendEmail(message)`, `Reserve(amount)`, or an audit-event record as data. No email is sent and no reservation occurs during that calculation. An interpreter validates authority, performs the interaction, handles retries, and records actual outcomes. The command value does not guarantee successful execution or make the interpreter pure.

The following program computes a quote from three integer values. Integer cents and basis points make rounding policy explicit. It returns a tuple and performs no I/O; the surrounding demonstration prints evidence.

<!-- bijux-verify: {"id":"explicit-quote-inputs","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"tax=949\ntotal=12449\nrepeat_equal=True\ninputs=12500,825,1000\n","stderr":""}} -->
```python
def quote(subtotal_cents, tax_basis_points, discount_cents):
    discounted = subtotal_cents - discount_cents
    tax_cents = (discounted * tax_basis_points + 5000) // 10000
    return tax_cents, discounted + tax_cents


inputs = (12500, 825, 1000)
first = quote(*inputs)
second = quote(*inputs)

print(f"tax={first[0]}")
print(f"total={first[1]}")
print(f"repeat_equal={first == second}")
print(f"inputs={inputs[0]},{inputs[1]},{inputs[2]}")
```

Execution establishes the annotated results for one valid integer input under the recorded Python toolchain. It does not prove purity for arbitrary Python callbacks or values, validate negative/overflowing inputs, establish legal tax policy, handle currencies, show thread safety, verify a production pricing system, or prove universal functional laws.

A useful pure-function contract names the input domain, output type, equality, numeric semantics, failure model, termination expectations, resource bounds when relevant, and absence of effects. A replay contract additionally names code, policy, schema, dependency versions, and canonical serialization. A test contract lists partitions and properties; it never replaces the semantic argument.

## Definitions and Notation

Let \(W\) be observable world states, \(X\) admitted inputs, \(Y\) results, and \(T\) observable traces. Model a general procedure as

\[
P:X\times W\to Outcome(Y,W,T).
\]

It is pure under the chosen functional observation when there exists \(f:X\to Y\) such that for every admitted \(x\) and world \(w\),

\[
P(x,w)=Success(f(x),w,\epsilon),
\]

where \(\epsilon\) is the empty observable trace. This strong total model can be extended with explicit error or divergence outcomes, but must not hide world changes.

If result depends on environmental value \(d\in D\), expose

\[
g:X\times D\to Y.
\]

For deterministic state threading,

\[
s:X\times S\to Y\times S.
\]

For explicit failure,

\[
v:X\to Result(Y,E).
\]

For a pure decision plus intended interactions,

\[
q:X\to Y\times List(Command).
\]

Define the **semantic dependency set** \(Dep(f)\) as all varying values whose substitution can change the functional result. Dependency completeness requires \(Dep(f)\subseteq Inputs(f)\), where captured immutable values are considered inputs to function creation. The claim is relative to a specified code and value semantics.

## Mechanisms, Invariants, or Proof Structure

**Extensionality.** For a pure function, equal complete inputs imply equal outputs. This does not say distinct inputs must yield distinct outputs and does not establish an implementation from finite tests.

**World noninterference.** In the model above, input world \(w\) equals output world and trace is empty. If logs, metrics, cache identity, allocation, timing, or energy are admitted observations, the proof must include them or weaken the purity claim to functional observations.

**Dependency extraction.** Start from the body and compute the transitive closure of reads and calls. Classify each leaf as supplied immutable data, fixed language/definition, or environmental effect. Any varying environmental leaf falsifies dependency completeness until it is passed as data or isolated outside.

**Explicit state equivalence.** A hidden counter procedure \(next:W\to Int\times W\) becomes a pure state transformer \(next:S\to Int\times S\) when the counter state is an ordinary immutable input/output value. The caller now sequences state explicitly; the computation no longer updates ambient storage.

**Replay sufficiency.** Equal business fields are not enough when policy or code changed. A valid replay key includes every meaning-relevant input and version. If two executions use identical serialized inputs but different rounding semantics, model artifact, Unicode table, timezone database, or code, equality is not promised.

**Memoization obligation.** Cache key \(k(x)\) is sound only when \(k(x_1)=k(x_2)\Rightarrow f(x_1)=f(x_2)\) under the output equality and implementation version. Returned values must not permit mutation that changes cached observations. Eviction may change cost, not functional result.

**Parallelism qualification.** Pure independent evaluations commute under functional observations. They may still contend for CPU/memory and fail under resource bounds. Parallel safety therefore follows for values, not automatically for performance, termination, or availability.

**Domain-proof boundary.** Reproducibility establishes that a formula maps recorded input to recorded output. It does not establish that inputs are truthful, units correct, policy applicable, formula validated, or decision safe. High-consequence acceptance requires separate domain evidence.

## Alternatives and Trade-Offs

**Many scalar arguments versus an input record.** Scalars expose dependencies directly but become unwieldy. An immutable named record groups related values, versions, and provenance. A vague service context hides capabilities and defeats the purpose.

**Snapshot value versus capability.** A timestamp, configuration, or reference snapshot supports pure calculation. A clock, repository, or random source capability supports controlled effects and testing but remains effectful when invoked. Use capabilities in the shell and values in the core.

**Explicit result variants versus exceptions.** Result variants make admitted failure visible and composable. Exceptions integrate with host control flow and can be appropriate at boundaries, but hide outcomes from simple types in many languages. A pure throwing function can still be partial; total interfaces are easier to compose.

**Explicit state passing versus local mutation.** State tuples are transparent and replayable. Encapsulated local mutation can implement the same pure result efficiently when aliases cannot observe it. Expose the value semantics, then choose an implementation whose optimization preserves it.

**Command data versus direct effects.** Returning commands enables inspection, testing, batching, authorization, and alternative interpreters. It adds an intermediate language and does not guarantee execution. Direct effects are simpler for small edges but couple decision and interaction.

**Memoization versus recomputation.** Memoization can improve repeated pure computation, while consuming memory and exposing timing if observed. Recompute when cheap, cache only with complete keys and immutable results, and version or invalidate across semantic changes.

## Failure Modes and Misconceptions

- **“Same input, same output means pure.”** Deterministic logging and mutation are counterexamples.
- **“No assignment means no effects.”** Reads of time, randomness, environment, files, databases, and networks are effects.
- **“Dependency injection makes code pure.”** Injected capabilities make authority explicit; invoking them still interacts.
- **“A context object is an explicit input.”** Not if its methods reach mutable or external state.
- **“Local mutation is always impure.”** Unobservable owned mutation can refine a pure value computation.
- **“Exceptions prove impurity.”** Deterministic failure can be effect-free but makes the function partial under a value-only type.
- **“Purity implies termination.”** A pure recursion can diverge.
- **“Purity implies idempotence.”** \(f(f(x))=f(x)\) is a separate algebraic property.
- **“Pure calls are automatically cheap and parallel.”** Resource consumption and scheduling remain real.
- **“A seed makes cryptography safe.”** It makes generator behavior explicit; entropy and algorithm security remain separate.
- **“A successful replay proves current correctness.”** It proves reproducibility under captured semantics, not truth or applicability.
- **“Pure core means the system is pure.”** The shell still performs every real-world interaction and must be engineered rigorously.

## Worked Examples

### Example 1

**Question:** Is `square(x) = x * x` pure?

**Reasoning:** Over a fixed numeric domain, if it reads only \(x\), returns the product, and performs no observable interaction, equal inputs yield equal results. For bounded or overloaded multiplication, the result/failure semantics must still be specified.

**Conclusion:** The definition is pure under its declared numeric and failure model, not by name alone.

### Example 2

**Question:** A function always returns 7 and always writes `called` to a log. Is it pure?

**Reasoning:** The returned value is deterministic, but evaluating twice produces two observable log events while replacing calls with 7 produces none. World state and trace change.

**Conclusion:** Determinism is insufficient; the function is effectful when logging is observable.

### Example 3

**Question:** How should a deadline calculation use current time?

**Reasoning:** An effectful shell reads a clock once, producing `observed_at` with clock-source metadata. A pure core receives deadline and observed instant and returns `Before`, `At`, or `After`. Passing a clock object would make access explicit but not pure.

**Conclusion:** Observe time at the boundary and pass a stable value to the calculation.

### Example 4

**Question:** Can a random shuffle be replayable and pure?

**Reasoning:** Define it as a deterministic transformation of collection, seed/state, and pinned algorithm version, returning shuffled collection and next state. Same complete inputs reproduce the output. Obtaining an unpredictable seed remains effectful.

**Conclusion:** Explicit generator state supports purity and replay without establishing security or statistical suitability.

### Example 5

**Question:** Is a function pure if it sorts its list argument in place and returns a tuple?

**Reasoning:** Another alias can observe the changed list, so world state differs despite the immutable return. Sorting an owned copy can be observationally pure if allocation, cost, and object identity are not functional observations.

**Conclusion:** Explicit parameters do not authorize mutation of caller-owned reachable state.

### Example 6

**Question:** When is memoizing `convert(amount, rate)` sound?

**Reasoning:** Amount, exact rate, currency/rounding policy, numeric semantics, and implementation version must determine the result and the key. A mutable returned object or hidden current rate invalidates reuse. Cache eviction may change cost only.

**Conclusion:** Memoization follows from dependency-complete value semantics and a sufficient key, not from function syntax.

### Example 7

**Question:** Is a closure returned by `make_taxer(policy)` pure?

**Reasoning:** If it captures an immutable policy value and later maps invoices without effects, yes; policy is semantically an input at closure creation. If it captures a mutable cell updated during rollouts, later calls have a hidden time-varying input.

**Conclusion:** Captured immutable values can define a pure function; mutable captures cannot be ignored.

### Example 8

**Question:** Can a pure function request an email?

**Reasoning:** It can return an immutable `SendEmail` command description along with its decision. That return is data. A separate interpreter authorizes, sends, retries, and records the actual outcome.

**Conclusion:** Describing an effect is pure; executing it is not.

### Example 9

**Question:** A renal-dose function receives patient weight, age, laboratory value, drug, unit, and guideline version and is pure. Is its recommendation clinically safe?

**Reasoning:** Purity enables exact replay but cannot validate patient identity, sampling time, assay, formula population, contraindications, interactions, guideline applicability, units, rounding, device/workflow, or clinical judgment. Acceptance requires named pharmacists, prescribers, nurses, clinical informaticians, laboratory and medication-safety specialists, human-factors/accessibility/localization experts, security engineers, regulators, affected clinicians, and independent clinical/technical reviewers. No external review is claimed.

**Conclusion:** Reproducible computation is necessary evidence, never clinical authorization.

### Example 10

**Question:** Should a service pass a repository interface into its pricing core?

**Reasoning:** Doing so makes dependency authority visible and testable, but calling it still couples calculation to I/O, timing, failure, and changing snapshots. The shell should load and validate one versioned pricing snapshot, then call a core over values.

**Conclusion:** Dependency injection improves boundaries; value extraction creates the pure boundary.

## Cross-Program Connections

[Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies evaluation, observation, equality, and effect models. [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) uses immutable explicit inputs for deterministic parallel work while retaining resource analysis.

[Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) decides which policy and evidence values belong in the model. [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) applies example, property, metamorphic, mutation, and differential testing to pure cores.

[Data Engineering](../../19-data-engineering/ROADMAP.md) versions snapshots, schemas, lineage, and replay inputs. [Security Engineering](../../25-security-engineering/ROADMAP.md) distinguishes explicit capability authority from immutable input and evaluates random-state secrecy and provenance.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) shows why remote reads cannot be hidden as ordinary local values. [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) separates request parsing and dependency acquisition from deterministic decision logic.

## References

- Amr Sabry, [“What Is a Purely Functional Language?”](https://doi.org/10.1017/S0956796897002943), *Journal of Functional Programming* 8(1), 1998, pp. 1–22. Formal analysis of proposed purity definitions and parameter-passing independence.
- Simon Marlow, ed., [*Haskell 2010 Language Report*](https://www.haskell.org/onlinereport/haskell2010/), 2010. Normative expression, function, type, `IO`, state, exception, and library semantics; checked 2026-08-29.
- John Hughes, [“Why Functional Programming Matters”](https://doi.org/10.1093/comjnl/32.2.98), *The Computer Journal* 32(2), 1989, pp. 98–107. Functions, modularity, higher-order composition, and lazy evaluation.
- Philip Wadler, [“The Essence of Functional Programming”](https://doi.org/10.1145/143165.143169), *POPL 1992*, pp. 1–14. Structuring errors, state, output, and choice while reflecting effects in program structure.
- Eugenio Moggi, [“Notions of Computation and Monads”](https://doi.org/10.1016/0890-5401(91)90052-4), *Information and Computation* 93(1), 1991, pp. 55–92. Formal distinction between values and computations.
- John Launchbury, [“A Natural Semantics for Lazy Evaluation”](https://doi.org/10.1145/158511.158618), *POPL 1993*, pp. 144–154. Heap-based operational semantics for sharing in lazy pure evaluation.
- John Backus, [“Can Programming Be Liberated from the von Neumann Style?”](https://doi.org/10.1145/359576.359579), *Communications of the ACM* 21(8), 1978, pp. 613–641. Functional style, combining forms, and algebraic program reasoning.
- Simon Peyton Jones, [“Tackling the Awkward Squad”](https://simon.peytonjones.org/Tackling-the-awkward-squad/), in *Engineering Theories of Software Construction*, IOS Press, 2001. Pure functional cores with I/O, concurrency, exceptions, and foreign calls at typed boundaries.

## Exercises

### Exercise 1

Classify pure, deterministic, total, idempotent, and thread-safe independently for: integer negation; an infinite pure recursion; a synchronized global counter increment; and a command that sets an external flag to true.

### Exercise 2

Transform a hidden-state function `draw(limit)` that reads a process PRNG into a pure state transformer. Give its type, two sequential transitions from seed \(s_0\), invariants, and the claims that still require security/statistical evidence.

### Exercise 3

Audit `shipping_total(order)` when it reads global rates, current promotion, locale, and a mutable cache. Design an immutable input and result model, a complete memoization key, failure variants, and adversarial tests.

### Exercise 4

Compare passing a `Clock`, `Repository`, and `RandomSource` capability with passing timestamp, versioned snapshot, and sampled/random-state values. Allocate each responsibility between an effectful shell and pure core, including retries and audit outcomes.

### Exercise 5

A hospital service calculates infusion limits from patient, laboratory, medication, device, terminology, and policy data. Design a replayable pure decision core and effectful shell. Specify inputs, results/commands, invariants, failure behavior, retained evidence, adversarial verification, and named human review before clinical use.

## Answers to the Exercises

### Answer 1

Integer negation is pure and deterministic under a fixed integer semantics; it is total for mathematical integers but may overflow or trap for a bounded minimum value. It is not idempotent because negating twice returns the original while one negation usually differs. It is thread-safe because calls share no mutable state.

An infinite recursion can be pure and deterministic in its divergence but is not total; idempotence is inapplicable without a result, and concurrent evaluations do not race although they can exhaust resources. A synchronized global counter increment can be deterministic only relative to a fully specified schedule, is effectful, may be total under operational assumptions, is not idempotent, and can be thread-safe. Setting an external flag to true is effectful and can be idempotent in final-state semantics; determinism, totality, and thread safety depend on the external system. None of these labels implies the others.

### Answer 2

Use `draw : Limit × Seed → Result((Value, Seed), Error)` with a pinned generator algorithm/version. First compute \((v_1,s_1)=draw(limit,s_0)\); then \((v_2,s_2)=draw(limit,s_1)\). For valid positive limit, require \(0\le v_i<limit\), deterministic transition from equal inputs, progress to the specified next state, and no ambient generator mutation. Invalid limits return an explicit error without consuming state.

Retain initial seed, algorithm/version, limit sequence, and code identity for replay. Purity does not establish unpredictability, uniformity, independence, resistance to state recovery, safe seeding, forward/backward secrecy, concurrency partitioning, or suitability for cryptography, lotteries, simulations, or regulated decisions. Those require domain-specific analysis and empirical/statistical or cryptographic evidence.

### Answer 3

The real input includes immutable order lines/currency/destination, a versioned exchange-rate table, promotion rules and effective interval, locale/rounding/currency policy, and relevant tax/shipping policy. Validate them into a `ShippingInput` with source IDs/digests and return `Result(ShippingQuote, QuoteError)`. Errors distinguish invalid order, missing rate, inapplicable/ambiguous promotion, unsupported currency/locale, overflow, and stale or conflicting snapshots.

The memoization key covers canonical input plus code/policy/schema versions and exact numeric/rounding semantics. Cached results are immutable. Tests vary empty/large orders, currency and rate boundaries, promotion overlap/expiry, locale separators that must not alter numeric meaning, rounding ties, overflow, negative data, stale/tampered snapshots, equal inputs with different versions, mutable-source changes after snapshot, and concurrent requests. The shell loads and authenticates snapshots and operates the cache; the core never reads either.

### Answer 4

Capabilities expose authority: calling `Clock.now` observes time, `Repository.load` performs I/O and may return changing data, and `RandomSource.sample` consumes external/nondeterministic state. They belong in the shell, where timeouts, authentication, retries, cancellation, consistency, entropy, telemetry, and actual audit writes are handled.

The shell reads one timestamp, loads and validates one versioned immutable repository snapshot, and samples required random values or obtains an explicit generator state. The core receives only those values and returns a decision plus command/audit descriptions. Retries of reads or writes remain shell behavior; a retry must not silently combine snapshots. The core can recompute the same description, but the shell records each actual attempt and outcome. Passing mocked capabilities improves tests yet does not change the semantic effect category.

### Answer 5

Define an immutable `InfusionDecisionInput` containing authenticated patient/order identifiers; demographics and weight with units/source/time; laboratory values with assay, unit, specimen time and quality; medication/route/concentration; device model/firmware/capabilities/calibration status; terminology and unit-system versions; approved clinical policy/guideline version, effective scope and digest; request time; site/jurisdiction; and core implementation/schema versions. The core returns `RejectInput(errors)`, `Escalate(reasons)`, or `WithinLimits(min,max,units,rationale)` plus immutable audit and proposed-device-command descriptions. It never contacts a record system or device.

Invariants require unit dimensional consistency, no implicit conversion, authenticated provenance references, policy applicability, freshness bounds, conservative handling of missing/conflicting data, numeric range/rounding rules, explicit contraindication/escalation paths, deterministic output, and no command for rejected input. The shell authenticates users/devices, obtains consistent snapshots, validates signatures/freshness, invokes the core, requires workflow approvals, rechecks command freshness, sends through an authenticated fail-safe channel, observes acknowledgement, and durably audits every attempt. It fails closed on ambiguity, timeout, version mismatch, replay, revocation, partial data, device disagreement, or lost acknowledgement.

Verification covers unit confusions, decimal and rounding boundaries, stale/mislabeled laboratory data, patient/order mismatch, duplicate/replayed messages, unsupported firmware, malicious/tampered policy artifacts, contraindications/interactions, extreme physiology, concurrent order changes, clock skew, partitions, retries, restart, safe shutdown, accessibility/localization and simulator-only device tests. Named review includes pharmacists, prescribers, nurses, medication-safety officers, clinical informaticians, laboratory and terminology experts, biomedical/device and integration engineers, human-factors/accessibility/localization specialists, cybersecurity/safety engineers, quality/regulatory and legal/privacy staff, vendor and operations/training representatives, affected clinical users, and independent clinical/technical assurance. No pure-function proof or automated test establishes clinical correctness, regulatory approval, or authority to deliver medication; no external review is claimed.
