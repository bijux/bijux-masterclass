---
module_id: STQE-001
program: Software Engineering: Testing & Quality Engineering
level: 1
module_number: 1
title: Why Software Testing Cannot Prove Absence of Defects
status: complete
last_verified: 2026-08-29
---

# Why Software Testing Cannot Prove Absence of Defects

## One-Page Review

### Governing question

What does a passing or failing test logically establish, why can ordinary testing not demonstrate that arbitrary software has no defects, and how should engineers build honest confidence from finite evidence?

### Essential definitions

- A **test item** is the software/system under evaluation in a specified version and configuration.
- A **test case** defines preconditions, inputs/actions, expected results or relations, execution conditions, and a comparison rule.
- A **test suite** is a selected finite collection of test cases; a **test run** executes a particular suite against a particular item and environment.
- A **test oracle** determines whether observed behavior is acceptable; it can be a specification, model, reference implementation, invariant, human judgment, metamorphic relation, or partial check.
- A **defect** (fault) is a flaw in an artifact; an **error state** is an incorrect internal state; a **failure** is externally observed behavior that violates an applicable expectation.
- A defect is **dormant** when execution has not reached/propagated it into an observable failure under the tested conditions.
- **verification** asks whether a work product satisfies specified requirements; **validation** asks whether it fulfills intended use in context. Testing contributes evidence to both but does not settle every claim.
- **coverage** measures which selected model elements—requirements, inputs, code, branches, states, combinations—were exercised; it does not by itself establish correct outcomes.
- **exhaustive testing** evaluates every member of a precisely bounded finite test domain under specified conditions and oracle.
- **residual risk** is the uncertainty/consequence remaining after prevention, analysis, testing, correction, and acceptance.

### Central model, mechanism, or theorem

Let implementation (P), specification/property (S), possible cases (X), environment/schedule set (E), oracle (O), and executed tests (T\subseteq X\times E). A passing run establishes at most

\[
\forall t\in T:\ O(P,t)=pass.
\]

The universal claim requires

\[
\forall t\in X\times E:\ P\models_t S.
\]

When (T) is only a subset, the first statement does not entail the second. A valid failing test supplies a counterexample to a stated property. Exception: if the relevant domain/environment is finite, completely enumerated, execution faithful, and the oracle/specification correct and complete for the claim, exhaustive testing can establish that scoped property over that model. It still cannot prove absence of unspecified requirements defects, unmodeled environments, tool faults, or different builds.

### Critical invariants

- State the exact item/build, configuration, dependencies, data, environment, schedule/control and observation boundary.
- State the property and oracle; “no exception” or process exit zero may be too weak.
- Distinguish no observed failures from no defects, and test failure from confirmed product defect.
- Preserve counterexamples and enough provenance to reproduce or characterize nondeterminism.
- Make selection model and coverage explicit: partitions, boundaries, risks, states, paths, combinations, histories or distributions.
- Treat coverage as evidence about exploration, not correctness.
- Qualify statistical claims with population, sampling process, independence/stationarity assumptions, confidence method and consequence.
- Test the test system: oracle, fixtures, generators, environment, instrumentation and result reporting can fail.
- Combine prevention, review, static analysis, formal reasoning, testing, runtime controls and monitoring according to risk.
- Keep human/domain authorization for safety, clinical, legal, financial and public-impact claims.

### Common failures

Common failures include saying “all tests pass, therefore correct”; assuming 100% statement/branch coverage means all behaviors are correct; testing the implementation against itself; asserting only non-crash; selecting only happy examples; ignoring invalid, empty, maximum, concurrent, temporal and failure conditions; treating nondeterministic failure as “flaky noise”; confusing a test-code defect with a product defect; extrapolating from convenience samples; claiming a probability of zero failures without a usage model; believing formal proof removes specification/model risk; and using testing’s limits as an excuse for weak testing.

### Compact example

A function is tested for inputs `0..15`; all results match `3*x mod 256`. The actual domain is `0..255`, and input 173 returns one too high. Sixteen passes establish only those sixteen observations under that build/oracle. Exhaustively evaluating all 256 values reveals the counterexample. If the finite byte domain, deterministic semantics, exact oracle, and complete enumeration are all justified, the repaired implementation can be shown to satisfy this one property over those 256 cases—not to be universally defect-free.

### Connections

[TPROG-001](../../07-programming-languages-theory-of-programming/modules/001-propositions-predicates-and-formal-specifications.md) distinguishes satisfiability, countermodels and proof. [SARCH-001](../../12-software-engineering-software-architecture/modules/001-architecture-as-significant-design-decisions.md) connects evidence to quality risks. [SEME-001](../../10-software-engineering-methods-and-evolution/modules/001-software-products-projects-services-and-platforms.md) separates output from outcome. The successor [STQE-002](../ROADMAP.md) develops specifications and test oracles.

## Governing Question

How can engineers reason rigorously from finite, fallible executions to useful confidence without turning “no failures observed” into the unsupported claim “no defects exist”?

Testing is an empirical intervention: arrange a case, execute an item in an environment, observe selected behavior, and compare it with an expectation. Its great strength is concreteness. A valid counterexample can overturn a broad correctness claim immediately. Its central limitation is induction: success on selected cases does not logically cover unexecuted cases, unobserved effects, alternate schedules, future environments, or mistakes shared by implementation and oracle.

## Why This Matters

Overclaiming passing tests causes unsafe releases, weak reviews and misleading governance. Underclaiming them is also harmful. Tests discover real defects, protect known behavior, make specifications executable, accelerate change, evaluate integrations, expose regressions, support experiments, and produce operationally relevant evidence. The goal is calibrated confidence, not cynicism.

Software’s case space is large and structured. Inputs interact with state histories, time, concurrency, dependencies, configuration, resources, faults, permissions, locale, hardware and prior versions. A function accepting two signed 32-bit values already has (2^{64}) pairs before histories/environments. Tests must select intelligently because brute-force enumeration is usually infeasible.

Quality engineering therefore asks two questions continuously: “Which important failure could this evidence reveal?” and “Which failure remains invisible?” The second question drives better models, oracles, designs, observability and complementary assurance.

## Prerequisites and Retrieval

Retrieve these concepts:

- universal and existential quantification, implication and counterexample;
- input domain, equivalence class, boundary, state and transition;
- deterministic versus nondeterministic behavior;
- precondition, postcondition, invariant and observable behavior;
- probability population, sample, distribution, independence and confidence interval;
- static analysis versus dynamic execution;
- specification, implementation, environment, dependency and version identity;
- risk as uncertainty combined with consequence.

You should be able to explain why one counterexample refutes “for all inputs,” why a thousand successes do not necessarily cover the next case, and why a correct output comparison can still miss an unauthorized side effect.

## Learning Objectives

After completing this module, you should be able to:

1. formalize what one passing and one failing test run establish;
2. distinguish defect, error state, failure, symptom, oracle failure and test-infrastructure failure;
3. explain the gap between a finite test set and a universal behavior claim;
4. state the strict conditions under which finite exhaustive testing establishes a scoped property;
5. identify input, state, schedule, environment and observation dimensions omitted by a suite;
6. diagnose weak or circular oracles and misleading coverage claims;
7. reason carefully about statistical operational testing and its assumptions;
8. combine example, property, model, metamorphic, differential and production evidence without overstating it;
9. design a risk-based assurance portfolio using testing and complementary techniques;
10. communicate residual uncertainty and human-review requirements for high-consequence systems.

## Core Exposition

### Start with quantifiers

Suppose property (S(x)) says implementation (P) behaves correctly for every admissible case (x\in X). The desired claim is (\forall x\in X.S(x)). A suite executes finite (T\subseteq X). If every test passes, we know (\forall x\in T.S_O(x)) relative to oracle (O) and observations. Unless (T=X) or a justified argument generalizes beyond (T), universal correctness does not follow.

A failing case is asymmetric. If (x\in X), environment is valid, observation is faithful, and oracle expectation is correct, (\neg S(x)) refutes the universal claim. But failure initially means a discrepancy in the test system. Root cause may be product code, requirement, test, fixture, stale expected data, dependency, environment or instrumentation. Preserve evidence before classifying.

This is the durable meaning behind Dijkstra’s testing aphorism: sampling is effective at showing defects through failures, not establishing their universal absence. It is not a claim that tests are useless or that no bounded exhaustive test can prove a scoped proposition.

### Follow defect activation and propagation

A defect does not fail on every execution. A faulty expression must be reached; input/state must activate the difference; erroneous state must propagate to an observed output/effect; and the oracle must recognize it. A swallowed incorrect value can later corrupt data without immediate visible failure. Conversely, an observed timeout may originate in infrastructure rather than product logic.

Model the chain:

\[
defect \xrightarrow{reach/activate} error\ state
\xrightarrow{propagate} observable\ discrepancy
\xrightarrow{oracle} detected\ failure.
\]

Tests can miss at every arrow. Structural coverage helps with reach, boundary/value selection with activation, observability with propagation, and strong oracles with detection. None alone is sufficient.

### Input is only one dimension

A “case” includes more than function arguments:

- initial persistent and in-memory state;
- sequence/history of prior operations;
- concurrent interleaving and memory visibility;
- clocks, time zones, timers and expiry;
- random choices/seeds;
- dependency responses, delays and partial failures;
- resource pressure, process restart and network topology;
- identity, permission, tenant and policy state;
- language/runtime/compiler/hardware/configuration versions;
- deployment, data schema and feature flags.

Even finite values compose combinatorially. A stateful protocol with ten operations and histories up to length 20 has many sequences before payloads or schedules. Intelligent selection uses models, partitions, boundaries, pairwise combinations, properties, coverage, risk, failures and production evidence.

### Oracles are part of the epistemic system

A test detects only discrepancies its oracle observes. `assert status == 200` misses wrong body, leaked tenant data, duplicate charge, stale write, excessive latency and forbidden side effects. Snapshot tests may faithfully preserve an incorrect output. A reference implementation may share the same misunderstanding. “Does not crash” is useful robustness evidence but weak functional evidence.

Oracles can be:

- exact expected values from a trusted specification/model;
- predicates/invariants, such as conservation or authorization;
- metamorphic relations between transformed inputs and outputs;
- differential comparison among independent implementations;
- round-trip or inverse relations;
- runtime assertions and reconciliation;
- human/domain judgment where intent cannot be automated.

Every oracle has a domain and trust base. Avoid deriving expected results with the same algorithm as the item. Test oracle code, use independent recomputation for critical mathematics, and include negative cases that prove the oracle can fail.

### Coverage is a map, not a verdict

Coverage answers “what selected structural/model elements were exercised?” Statement coverage can leave branch outcomes untested; branch coverage leaves conditions/combinations/data relations untested; path coverage is often infeasible or infinite with loops; requirement coverage can map to weak assertions; production coverage reflects only observed traffic.

Even 100% coverage establishes reach, not correctness. A test can execute every statement while asserting nothing. Conversely, unreachable defensive code can prevent an arbitrary percentage without reducing practical confidence. Use coverage to find exploration gaps, compare risk models and review tests—not as a universal quality score.

Mutation testing asks whether tests detect intentional changes and can expose weak oracles. Surviving mutants may reveal gaps, equivalent behavior, infeasible states or poor mutation operators. A high mutation score remains evidence about selected mutations, not absence of real defects.

### Exhaustive testing has a legitimate bounded role

If the claim domain is truly finite and fully enumerable, exhaustive testing can establish a property under strong assumptions. For an 8-bit pure function, enumerate all 256 inputs. For a small truth table or state machine, enumerate all modeled valuations/transitions. Conditions include:

1. domain and environment boundary are complete for the claim;
2. every member is executed (not merely generated or counted);
3. implementation/build/configuration matches the claim;
4. behavior is deterministic or every relevant nondeterministic outcome/schedule is covered;
5. observations capture every relevant effect;
6. oracle/specification is correct, complete and independently trusted;
7. runner/instrumentation/reporting are faithful.

The conclusion is scoped: no violation of property (S) exists in bounded model (M) for tested item (P_v). It is not “the system has no defects.” Missing requirement, wrong model, compiler/hardware fault, side channel or different deployment remains possible.

Goodenough and Gerhart’s theory highlights this nuance: suitably reliable and valid criteria could support absence claims, while demonstrating that practical criteria such as executing all statements, predicates or paths are generally reliable is hard. The obstacle is not the word “test”; it is justified completeness and validity.

### Nondeterminism weakens replay and enumeration

Concurrent/distributed systems can produce different outcomes for identical visible inputs. One hundred passes may repeat one schedule. Random seeds help replay generated choices but not every scheduler, timing, kernel or dependency event. Stress increases opportunities without defining coverage.

Use controlled schedulers/model checking for bounded interleavings, deterministic simulation, fault injection, history-based consistency checkers, repeated runs, causal traces and invariants. Still state bounds: process count, operations, faults, time and model correspondence. A “flaky” failure is evidence of nondeterminism, isolation failure or observation instability—not a reason to discard it without diagnosis.

### Statistical operational testing needs a probability model

Testing can estimate failure rates when cases are sampled from a defined operational distribution and assumptions are defensible. Observing zero failures in (n) independent Bernoulli trials does not prove probability zero. Under a simple binomial model, the rough 95% “rule of three” upper bound is about (3/n), but only for the sampled population and assumptions.

Real executions may be dependent, nonstationary, censored, clustered by user/version and shifted after release. Rare catastrophic modes may be absent from normal traffic. Report population, sampling, exposure units, time, versions, failures, confidence method and model limitations. Statistical reliability evidence does not validate requirement correctness or ethically acceptable risk.

### Tests are strongest as counterexample search and regression memory

Design tests to challenge claims: boundaries, equivalence classes, invalid inputs, state transitions, interaction combinations, resource/failure conditions, adversarial behavior, historical incidents and changed code. A failure yields a concrete investigation artifact. After repair, a regression test preserves the specific learned distinction—provided it remains readable and valid.

Property-based testing searches generated cases against general relations and shrinks failures; it samples unless its domain is exhausted. Model-based testing derives sequences from a model; it is limited by model/bounds/oracle. Metamorphic testing works when exact outputs are hard but relations are known. Differential testing finds disagreement, not which implementation is right. Fuzzing explores robustness/security surfaces and may optimize structural novelty; it does not establish semantic completeness.

### Build an assurance argument, not a test-count argument

Start from risks and claims. For each, identify prevention, observability, oracle, test design, environment, coverage model, complementary analysis and residual uncertainty. Examples:

- types/contracts prevent classes of invalid states;
- review/static analysis inspect paths without execution;
- formal proof/model checking establishes defined properties under a model;
- tests connect implementation to concrete environments and dependencies;
- canaries/monitoring/reconciliation detect deployment and world-model failures;
- operational controls limit blast radius and recover;
- human/domain review validates intent and acceptable risk.

These techniques have different blind spots. Diversity is valuable only when evidence is sufficiently independent; five tools sharing the same specification mistake do not provide five confirmations.

### A small executable counterexample search

This toy example contrasts a passing convenience sample with exhaustive enumeration of a declared byte domain.

<!-- bijux-verify: {"id":"stqe-001-counterexample-search","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sampled=16 failures=0\nunobserved=240\nexhaustive=256 failures=1\ncounterexample input=173 expected=7 actual=8\n","stderr":""}} -->
```python
def expected(value):
    return (3 * value) % 256

def implementation(value):
    result = expected(value)
    if value == 173:
        return (result + 1) % 256
    return result

def failures(cases):
    return [
        (value, expected(value), implementation(value))
        for value in cases
        if implementation(value) != expected(value)
    ]

sample = range(16)
sample_failures = failures(sample)
all_bytes = range(256)
all_failures = failures(all_bytes)

print(f"sampled={len(sample)} failures={len(sample_failures)}")
print(f"unobserved={256 - len(sample)}")
print(f"exhaustive={len(all_bytes)} failures={len(all_failures)}")
value, wanted, actual = all_failures[0]
print(f"counterexample input={value} expected={wanted} actual={actual}")
```

The run exhausts exactly 256 integer inputs for two deterministic pure Python functions and reveals one discrepancy. It does not validate the `expected` function against a real requirement, other types, side effects, resource behavior, Python/toolchain correctness, hostile environments, or any changed implementation.

## Definitions and Notation

Let test item (P_v) identify implementation plus version/configuration; input/state/history/environment space (X); specification/property (S); test-selection criterion (C); suite (T_C\subseteq X); observation function (Obs); oracle (O); and outcome (pass/fail/unresolved).

Detection for defect (d) requires reachability (R_d), activation (A_d), propagation (P_d), observation (V_d), and oracle discrimination (O_d). This conjunction is a reasoning model, not an assumption of statistical independence. Coverage function (cov(T,M)) reports exercised elements of model (M). It has meaning only with the model and criterion named.

For statistical tests let (n) be exposures, (k) observed failures and (p) failure probability under a stated sampling model. Never infer a universal (p) without defining population and assumptions.

## Mechanisms, Invariants, or Proof Structure

1. State the quality claim, affected population, consequences and acceptable decision threshold.
2. Freeze/identify test item, configuration, dependencies, data and environment.
3. Define input, state, history, schedule, failure and observation spaces.
4. Build oracles independently enough to distinguish relevant behavior.
5. Select cases from risk, partitions, boundaries, models, structure, changes, incidents and distributions.
6. Include negative controls proving tests and oracles detect known deviations.
7. Execute reproducibly where possible; capture exact provenance and counterexamples.
8. Interpret passes only for executed cases and observation/oracle scope.
9. Diagnose failures across product, specification, test, fixture, environment and instrumentation.
10. Use coverage/mutation/fuzzing/properties/models to expose gaps without treating scores as correctness.
11. Combine complementary prevention, static, formal, dynamic and operational evidence.
12. Report residual risks, untested dimensions, unavailable evidence and authorized acceptance.

A release argument should say “these claims have this evidence under these conditions, with these limitations,” not “QA approved.” Decision owners accept residual risk; testers produce and challenge evidence.

## Alternatives and Trade-Offs

**Example-based tests** are concrete/readable and excellent for known cases; sparse examples miss interactions. **Property-based tests** broaden generated search and shrink counterexamples; generators/properties are fallible and usually sampled.

**White-box selection** targets branches/data flow/changes; it can mirror implementation and miss omitted behavior. **Black-box selection** derives from external specification; it can miss structural risk. Combine them.

**Model-based testing** covers modeled states/transitions systematically; model validity and state explosion limit it. **Exploratory testing** adapts skilled investigation to observations; reproducibility and coverage communication need discipline.

**Differential testing** is powerful with independent implementations; consensus can be shared error. **Metamorphic testing** avoids exact oracle for known relations; an incorrect relation misclassifies behavior.

**Simulation/fakes** give control and speed; fidelity gaps hide integration failures. **Production/canary evidence** is realistic; it exposes users and cannot safely explore every failure.

**Formal proof/static analysis** generalizes over modeled paths without dynamic sampling; specification, abstraction and tool trust remain. **Runtime testing/monitoring** sees concrete integration/world behavior; it is incomplete. Use complementary scopes.

## Failure Modes and Misconceptions

- **“All tests passed.”** Name suite, item, environment, oracle and omissions.
- **“No defects exist.”** Usually unsupported; say no violations observed in covered scope.
- **“One failure proves product bug.”** First establish valid case, oracle and environment.
- **“100% coverage means correct.”** Exercise is not discrimination.
- **“Exhaustive is impossible.”** Often true broadly, false for well-bounded finite models.
- **“Exhaustive means defect-free.”** It establishes only specified properties and boundaries.
- **“More cases always add confidence.”** Redundant weak-oracle cases can add little.
- **“Random testing is statistical evidence.”** Only with a defined sampling/usage model.
- **“Flaky failures do not count.”** They expose uncontrolled conditions or real races.
- **“A reference output is truth.”** Reference and item may share defects.
- **“Mutation score is quality.”** It measures sensitivity to selected mutations.
- **“Formal methods replace testing.”** Implementation/environment/model correspondence remains.
- **“Testing late assures quality.”** Prevention and testability begin in requirements/design.
- **“QA owns quality.”** Decision/design/implementation/operation stakeholders share it.
- **“Testing limits excuse release risk.”** Limits demand better evidence and explicit acceptance.

## Worked Examples

### Example 1

**Situation.** Sixteen small integer examples pass the multiplier from the executable model.

**Reasoning.** They cover 6.25% of a declared byte domain and omit input 173. No generalization principle links tested to untested values. Exhaustive enumeration reveals expected 7 versus actual 8.

**Conclusion.** Passing samples establish observations; a counterexample refutes universality.

### Example 2

**Situation.** Suite achieves 100% branch coverage for `is_eligible(age,country)` but asserts only result is Boolean.

**Reasoning.** Every branch can execute while country/age policy is inverted. Coverage confirms reach; oracle accepts both true/false. Add policy-derived decision cases and boundary/negative assertions.

**Conclusion.** Coverage without a discriminating oracle cannot establish correctness.

### Example 3

**Situation.** Tax calculation and test both copy the same mistaken rounding table.

**Reasoning.** Every example agrees because oracle shares the defect. Independently derive boundary values from authoritative rule, have domain expert review, and use invariant/reconciliation against assessed totals.

**Conclusion.** Agreement is weak when evidence sources are not independent.

### Example 4

**Situation.** Concurrent transfer test passes 999 times and loses money once.

**Reasoning.** Failure demonstrates at least one reachable bad schedule if environment/oracle valid. Quarantining it as flaky discards crucial evidence. Capture schedule/trace, add conservation invariant and controlled interleaving/fault tests.

**Conclusion.** Nondeterministic rarity does not reduce consequence or validity.

### Example 5

**Situation.** Firmware lookup maps every 4-bit input to an expected safe code.

**Reasoning.** Enumerate all 16 inputs on the exact binary/hardware interface and compare independently reviewed table, including side effects/timing if relevant. This can establish mapping property for bounded conditions; it cannot validate table intent or other firmware behavior.

**Conclusion.** Exhaustive testing supports scoped absence claims under explicit completeness.

### Example 6

**Situation.** Distributed lock passes tests with three nodes and one crash.

**Reasoning.** Claim remains bounded by nodes, operations, partitions, delays, clock, storage and fault patterns explored. Search histories for mutual-exclusion violations and verify checker. Passing bound does not cover two failures or production storage semantics.

**Conclusion.** Model/schedule bounds belong in every distributed assurance claim.

### Example 7

**Situation.** Property test generates 100,000 lists and verifies sorting/order plus multiset preservation.

**Reasoning.** Stronger oracle excludes empty-return cheat; generator may still underproduce huge, duplicate, pathological comparator or memory cases. Seed/counterexample improves reproduction, not exhaustive proof.

**Conclusion.** Properties improve search and discrimination while remaining scoped by generation.

### Example 8

**Situation.** Mutation testing leaves replacement `>` to `>=` alive.

**Reasoning.** It may expose missing equality boundary, an equivalent mutant under precondition, unreachable state, or bad operator. Inspect semantics before adding a test solely to raise score.

**Conclusion.** Surviving mutants are investigation prompts, not automatic defects.

### Example 9

**Situation.** Canary has no errors in 10,000 requests.

**Reasoning.** Verify routing population, duration, feature use, observability and delayed effects. A rare admin workflow or data corruption may be absent. Canary supports sampled deployment compatibility, not universal safety.

**Conclusion.** Production realism does not eliminate selection and oracle limits.

### Example 10

**Situation.** Insulin-dose software passes unit, integration, simulation and hardware tests.

**Reasoning.** Evidence covers selected requirements, devices, patient profiles and faults. Review units, rounding, sensor validity, stale data, occlusion, manual override, updates, cybersecurity, usability, alarm response and extreme physiology. Use independent recomputation, hazard analysis, traceability, formal reasoning where justified and clinical validation.

**Conclusion.** Named endocrinologists/pharmacists, biomedical and safety engineers, human-factors/accessibility experts, cybersecurity/privacy specialists, software/hardware/operations engineers, quality/regulatory representatives and independent assessors must approve claims and residual risk. Passing automation cannot authorize patient dosing.

## Cross-Program Connections

- **Theory of Programming:** proof and model checking can generalize beyond sampled executions under formal assumptions.
- **Architecture:** testability, observability and fault containment determine which failures can be exposed.
- **Methods and Evolution:** testing supplies feedback throughout discovery, delivery, operation and maintenance.
- **Delivery and Reliability:** CI, canaries, monitoring, rollback and incident evidence extend but do not universalize tests.
- **Algorithms:** combinatorial growth and selection strategies determine feasible exploration.
- **Distributed Systems:** schedules, partial failure and consistency require history/model-aware evidence.
- **Security Engineering:** adversarial search invalidates benign usage distributions and demands abuse cases.
- **Systems Engineering:** verification, validation, hazards and operational context extend beyond software outputs.
- **Data Engineering:** reconciliation and data-quality oracles expose silent pipeline failures.
- **Formal Specifications:** precise properties strengthen oracles but can encode wrong intent.

## References

- ISO/IEC/IEEE, [ISO/IEC/IEEE 29119-1:2022 — Software testing: General concepts](https://www.iso.org/standard/81291.html), second edition, 2022, retrieved 2026-08-29. Current international testing concepts and vocabulary.
- IEEE Computer Society, [Guide to the Software Engineering Body of Knowledge, Version 4.0](https://www.computer.org/education/bodies-of-knowledge/software-engineering), 2024, retrieved 2026-08-29. Current software-testing knowledge-area context.
- Edsger W. Dijkstra, [Notes on Structured Programming (EWD249)](https://www.cs.utexas.edu/~EWD/transcriptions/EWD02xx/EWD249/EWD249.html), 1970. Primary source for the presence-versus-absence argument and infeasibility example.
- John B. Goodenough and Susan L. Gerhart, “Toward a Theory of Test Data Selection,” *IEEE Transactions on Software Engineering*, 1975. Foundational analysis of reliable/valid test criteria and scoped absence claims.
- Glenford J. Myers, Corey Sandler, and Tom Badgett, *The Art of Software Testing*, third edition, Wiley, 2011. Durable testing psychology, economics and case-design foundations.
- Paul Ammann and Jeff Offutt, *Introduction to Software Testing*, second edition, Cambridge University Press, 2016. Coverage, graph, logic, input-space and model-based foundations.
- Earl T. Barr et al., “The Oracle Problem in Software Testing: A Survey,” *IEEE Transactions on Software Engineering*, 2015. Comprehensive treatment of test-oracle limitations and techniques.
- Elaine J. Weyuker, “On Testing Non-Testable Programs,” *The Computer Journal*, 1982. Foundational work on testing where exact expected results are unavailable.
- Richard Hamlet, “Testing Programs with the Aid of a Compiler,” *IEEE Transactions on Software Engineering*, 1977, and later probable-correctness work. Foundations for fault seeding/mutation and statistical limits.
- Bev Littlewood and Lorenzo Strigini, “Validation of Ultra-High Dependability for Software-Based Systems,” *Communications of the ACM*, 1993. Statistical and epistemic limits of demonstrating extremely low failure rates.

## Exercises

### Exercise 1

Formalize what is and is not established when 200 tests pass for a parser build.

### Exercise 2

Construct a reach-activation-propagation-observation-oracle trace for a defect that is covered but undetected.

### Exercise 3

Diagnose “100% branch coverage, zero failures, therefore release is defect-free” and propose a stronger evidence plan.

### Exercise 4

Compare exhaustive finite testing, property-based testing, model checking, formal proof and operational statistical testing for a 12-bit access-control function with state.

### Exercise 5

Design a test and assurance argument for an unfamiliar autonomous emergency-braking controller, including named human review.

## Answers to the Exercises

### Answer 1

Let item be exact parser binary/configuration, suite (T) the 200 source/environment cases, observations token/AST/diagnostics/resource facts actually checked, and oracle (O). Passing establishes (\forall t\in T.O(P,t)=pass) for that run, subject to runner/report fidelity. It does not establish correctness for untested syntax, encodings, sizes, nesting, recovery contexts, resource limits, concurrency, platforms or future builds; it does not establish oracle/specification correctness; and it may miss side effects not observed. Report selection rationale and coverage—grammar productions, boundaries, malformed classes, differential/property relations—plus limitations. If the 200 cases exhaust a rigorously defined finite subdomain, make only that scoped claim.

### Answer 2

Example: statement coverage reaches a discount condition with customer tier `gold`. Defect uses `total > 100` instead of `>= 100`. Test input has total 101, so defective and correct predicates both choose discount: reached but not activated. To show propagation stages too, use total 100 to activate wrong branch, then downstream cap overwrites both results to same final total: error does not propagate. If internal trace observes wrong branch but test asserts only HTTP 200, propagation to an observation exists but oracle does not discriminate. Repair with equality boundary, independent expected amount, assertion of final and ledger effects, and negative controls. Coverage alone reported execution of the condition, not the semantic distinction.

### Answer 3

The conclusion commits quantifier and oracle errors. Branch coverage says both outcomes of measured branches executed; unmeasured conditions, combinations, data/state histories, omitted code/requirements and environments remain. Zero observed failures can reflect weak assertions. Strengthen from risk/specification: requirements and quality scenarios, equivalence/boundary/decision/state-transition cases, negative/failure/concurrency/resource cases, independent oracles for values and effects, mutation analysis, changed-code review, static analysis, integration/system tests, representative environments, fault/recovery evidence, and production guardrails. Inspect unreachable code and coverage instrumentation. Report evidence per claim and residual risk; do not replace one universal score with a larger dashboard.

### Answer 4

Twelve-bit input alone has 4,096 values, so exhaustive input enumeration is feasible for a pure stateless deterministic function and exact oracle; add state/history and schedules and the domain grows. Property-based testing can search generated states/actions and shrink violations, but is sampled unless exhaustive. Model checking can explore all states/transitions within an abstract finite model and produce traces; correspondence and bounds remain. Formal proof can establish access invariant for all modeled inputs/histories relative to definitions/axioms/tool trust; implementation refinement and requirement validity remain. Operational statistical testing estimates behavior under a defined usage distribution, valuable for reliability but weak for rare adversarial unauthorized cases. Combine: human-reviewed policy/specification; exhaustive 12-bit decisions for relevant state snapshots; model/proof for state-transition authorization invariant; implementation/property/differential tests; adversarial security tests; production audit/reconciliation. State every bound and oracle.

### Answer 5

Define claims: under specified speed, friction, sensor, obstacle, actuator, driver and system states, controller detects hazard, commands bounded braking within deadline, avoids unsafe command in defined false-positive cases, enters safe degraded mode on invalid/disagreeing data, preserves manual authority and records decisions. Build requirements/hazard traceability and independent physical/reference models. Test equivalence/boundary combinations, units/rounding/overflow, stale/missing/spoofed sensors, time/clock, actuator lag/failure, road/weather extremes, restart/update/rollback, resource exhaustion, cybersecurity and human interaction. Use simulation with scenario coverage, property/model-based sequences, formal review of key state-machine invariants, fault injection, software/hardware-in-loop, controlled track tests, production monitoring with safety constraints and regression from incidents. Validate models against physical evidence and preserve counterexamples.

Named vehicle dynamics and braking engineers, safety assessors, drivers/fleet operations, human-factors/accessibility experts, cybersecurity/privacy specialists, sensor/hardware/software/ML engineers where applicable, quality/configuration managers, emergency responders, regulators and independent validation representatives review hazards, populations, assumptions, evidence, residual risk and deployment authority. No test count, simulation coverage or formal model alone authorizes road use.
