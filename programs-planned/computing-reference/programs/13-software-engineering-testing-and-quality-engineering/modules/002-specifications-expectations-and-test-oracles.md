---
module_id: STQE-002
program: Software Engineering: Testing & Quality Engineering
level: 1
module_number: 2
title: Specifications, Expectations, and Test Oracles
status: complete
last_verified: 2026-08-29
---

# Specifications, Expectations, and Test Oracles

## One-Page Review

### Governing question

Given an execution and its observations, what trustworthy information lets a tester decide whether behavior is acceptable, and how should that oracle’s scope, independence, ambiguity, and fallibility constrain the verdict?

### Essential definitions

- A **test basis** is the body of knowledge used to derive test objectives, models, cases, and expectations: requirements, contracts, standards, designs, risks, user needs, prior behavior, or domain knowledge.
- A **specification** states required, permitted, or forbidden properties of a test item or its environment. It may be formal, executable, structured, or natural language, and it can be incomplete or wrong.
- An **expected result** is predicted observable behavior under specified conditions, derived from a specification or another justified source.
- An **actual result** is the observation produced by executing a particular test item in a particular environment.
- A **test oracle** is a source of information used to determine whether a test passes or fails.
- The **oracle procedure** extracts and compares observations; the **oracle information** is the trusted knowledge on which that comparison relies.
- The **oracle problem** is the difficulty of determining the correct verdict for given input and state.
- A **partial oracle** checks only selected properties and can miss other incorrect effects.
- A **pseudo-oracle** or **reference oracle** compares the item with another implementation/model whose relevant behavior is assumed more trustworthy or sufficiently independent.
- A **metamorphic relation** constrains how outputs should relate across transformed inputs when exact expected outputs are unavailable.
- An **inconclusive** result means available evidence cannot support pass or fail under the test’s decision rule.

### Central model, mechanism, or theorem

For test item $P_v$, case $t$, environment $e$, observation function $obs$, accepted-behavior set $A(t,e)$, and oracle procedure $O$,

$$
y=obs(P_v,t,e),\qquad O(y,A)\in\{pass,fail,inconclusive,error\}.
$$

A pass establishes only that observed $y$ satisfied the predicates encoded by $O$, relative to the basis, item, environment, and observation boundary. It does not establish that $A$ captures stakeholder intent, that unobserved effects are correct, or that the oracle is independent and defect-free.

### Critical invariants

- Name the versioned test item, input/prestate, environment, dependencies, observation boundary, and test basis.
- Derive expectations before or independently from the observed result where practical; never silently bless current output.
- State what the oracle observes and what it ignores: values, state, events, side effects, non-events, timing, resources, authorization, and degradation.
- Distinguish required, permitted, forbidden, approximate, nondeterministic, and unspecified behavior.
- Define pass, fail, inconclusive, and oracle/infrastructure error separately.
- Keep tolerances, normalization, time windows, statistical thresholds, and comparison rules domain-justified rather than convenient.
- Test the oracle with positive, negative, boundary, ambiguity, and self-failure cases.
- Avoid common-mode reasoning between implementation and expected-result calculation; seek independent derivations for critical claims.
- Version specifications, fixtures, models, reference data, and oracle code with provenance.
- Require named qualified human authority for clinical, safety, legal, financial, rights-impacting, or other high-consequence judgments.

### Common failures

Common failures include treating “no exception” as functional correctness; comparing only status codes; copying production output into golden files; implementing expected results with the same algorithm as the test item; asserting internal calls rather than required behavior; using exact equality for approximate semantics; adding arbitrary tolerances until tests pass; accepting either outcome of a race; confusing nondeterministic with unspecified; trusting a reference implementation without independence analysis; majority-voting correlated implementations; assuming human review is infallible; collapsing ambiguity into pass; ignoring forbidden side effects and missing events; and failing to version the oracle basis.

### Compact example

A transfer API returns `200`. A status-only oracle passes. A claim-specific oracle also checks authenticated authority, debit and credit amounts, conservation, exactly one durable ledger event, idempotency under retry, no cross-account disclosure, and response time in the stated environment. If the balance snapshot is missing, conservation cannot be evaluated: the honest verdict is inconclusive or oracle error, not pass.

### Connections

[STQE-001](./001-why-software-testing-cannot-prove-absence-of-defects.md) bounds what finite passing evidence proves. [TPROG-001](../../07-programming-languages-theory-of-programming/modules/001-propositions-predicates-and-formal-specifications.md) supplies predicates and counterexamples. [SDDM-002](../../09-software-engineering-software-design-and-domain-modeling/modules/002-stakeholders-goals-and-observable-outcomes.md) links expectations to stakeholder outcomes. [STQE-003](../ROADMAP.md) separates verification against specifications from validation of fitness for purpose.

## Governing Question

How can a tester move from “the program produced something” to a defensible pass, fail, inconclusive, or error verdict when specifications are incomplete, outputs are complex, behavior may be nondeterministic, and the oracle itself can be defective?

Test generation asks what to execute. Oracle design asks what the result means. Automated execution without an adequate oracle can produce a large quantity of green output that says almost nothing about correctness. Conversely, a strong oracle with poor case selection checks the right property too rarely. Test design needs both.

## Why This Matters

Many costly failures pass tests because observations were too narrow. An endpoint returned the expected body but exposed another tenant’s data. A transaction produced the correct balance but emitted a duplicate event. A scheduling algorithm met average latency while starving a protected class. A medical calculation matched a reference implementation that shared the same unit error.

Oracle weakness also wastes engineering effort. Over-specified snapshot tests fail on harmless formatting or ordering changes. Arbitrary timing thresholds create intermittent failures. A human review queue can make feedback unusably slow. A test that cannot distinguish product failure from missing evidence sends investigators toward the wrong component.

The core engineering problem is epistemic: what is the source of truth for this claim, how does it map to observable behavior, and why should it be trusted? The answer may be an exact table, a state model, an invariant, an independent calculation, a relation across executions, an operational distribution, a domain expert, or a portfolio of partial oracles. Each brings assumptions and blind spots.

## Prerequisites and Retrieval

Retrieve:

- predicate, relation, set membership, universal/existential claim, implication, counterexample, precondition, postcondition, and invariant;
- test item, case, suite, prestate, input, environment, actual result, failure, defect, and residual risk;
- functional behavior, quality attribute, requirement, constraint, assumption, and specification;
- deterministic, nondeterministic, stochastic, approximate, concurrent, stateful, and time-dependent behavior;
- independent implementation, common-mode failure, provenance, version, and configuration;
- false positive/false negative in a stated decision context.

You should be able to explain why `assert response.status == 200` is a partial oracle, why two implementations agreeing does not prove either correct, and why a missing observation should not automatically become a pass.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish test basis, specification, expected result, actual result, oracle information, oracle procedure, and verdict;
2. formalize accepted behavior as predicates or sets relative to preconditions and environment;
3. design exact, predicate, model, metamorphic, differential, statistical, implicit, and human oracles;
4. expose observation boundaries and forbidden side effects;
5. represent nondeterministic, approximate, temporal, and concurrent expectations without arbitrary looseness;
6. diagnose under-specified, over-specified, circular, stale, ambiguous, and non-independent oracles;
7. assign pass, fail, inconclusive, and oracle-error outcomes correctly;
8. verify oracle code and expected data with mutation, negative controls, independent recomputation, and provenance;
9. choose an economical oracle portfolio from risk and consequence;
10. define human review and release authority for unfamiliar high-stakes oracle decisions.

## Core Exposition

### Separate basis, expectation, observation, and verdict

A requirement such as “authorized users can transfer funds” is a test basis, not a complete expected result. Test design must specify authority, source account, destination, currency, prestate, amount, dependency behavior, response, state transition, events, failure behavior, timing, and observation method. The expected result is conditional:

$$
pre(t,e)\Rightarrow post(prestate,input,observed\ state,e).
$$

Execution yields observations, not truth. The oracle procedure maps those observations and its information source into a verdict. If a telemetry collector failed, the absence of a duplicate event may be unknowable. If a specification is ambiguous, the discrepancy may expose a specification defect rather than a product defect.

Keep at least four outcomes:

- **pass:** every required checked predicate holds and no checked forbidden predicate holds;
- **fail:** at least one valid checked expectation is violated;
- **inconclusive:** evidence is insufficient or the basis admits unresolved interpretations;
- **error:** the test/oracle mechanism did not perform as required.

Some systems merge inconclusive/error into failure for pipeline safety, but preserve the semantic cause for diagnosis and governance.

### Specifications define accepted sets, not always one value

For input and prestate $x$, a deterministic exact specification may define a singleton accepted set $A(x)=\{y^*\}$. Nondeterministic specifications define several permitted outcomes. Approximate specifications define a region. Protocol specifications may define permitted histories and forbidden transitions.

This distinction prevents two common errors. First, nondeterminism does not mean “accept any output”; the allowed set still has boundaries. Second, an exact snapshot may over-specify behavior when ordering, identifiers, timestamps, or formatting are intentionally unconstrained.

Classify properties:

- **required:** must be observed under stated conditions;
- **forbidden:** must not occur;
- **permitted:** may occur but is not required;
- **unspecified:** the basis makes no claim; tests should not freeze it accidentally;
- **conditional:** applies only when a precondition/environment predicate holds.

Specifications can conflict or be incomplete. Preserve source hierarchy and authority: law, protocol, contract, safety constraint, product rule, design decision, operational expectation, and historical behavior do not have equal status. Escalate rather than inventing precedence in test code.

### The observation function determines visibility

An oracle cannot judge what the harness does not observe. Output values are only one channel. Observe as the claim requires:

- externally visible responses and error semantics;
- persistent state transitions and invariants;
- emitted, suppressed, duplicated, reordered, or delayed events;
- calls to irreversible external effects;
- authorization decisions and information disclosure;
- timing, throughput, resource consumption, and degradation;
- logs, metrics, traces, audit records, and provenance;
- state after retry, rollback, restart, timeout, and partial failure;
- absence of an event over a justified window.

Instrumentation can perturb behavior or lie. Direct database inspection may bypass the public consistency semantics; mocked calls may show intent but not actual effect. Record observation method and uncertainty. For negative claims such as “no event occurred,” define observation completeness and time horizon.

### Exact expected-value oracles

An exact oracle compares actual output with a precomputed value. It works well for arithmetic with an independently derived result, finite tables, standard test vectors, serialization fixtures with canonical representation, and stable protocol examples.

Trust depends on provenance. An expected tax amount copied from the implementation is circular. Better sources include an authoritative table, hand derivation with review, independently implemented model, or published standard vector. For large golden files, review generation method and semantic diff. Do not update snapshots merely because a change is intentional; verify that new behavior is correct.

Exact comparison can be too strict. If order is unspecified, compare multisets or a property. If timestamps are permitted in a range, assert the interval and clock conditions. Normalization must remove only irrelevant variation; deleting all whitespace could hide a significant distinction in a language or signature.

### Predicate, contract, and invariant oracles

Predicates accept a set of outcomes: a balance remains nonnegative, authorization implies a valid grant, total inventory is conserved, a response schema holds, or a state transition preserves an invariant. They scale beyond enumerating exact results and make forbidden effects visible.

A partial predicate does not imply full correctness. Schema validity does not establish semantic correctness. Conservation can hold while money moves to the wrong account. Combine claim-specific predicates and state what remains unchecked.

Runtime assertions, type refinements, database constraints, and design-by-contract can supply oracle information. Their code can share implementation defects and may be disabled or scoped differently in production. Test them with negative controls that violate each condition and confirm detection.

### Model-based and stateful oracles

A reference model maps input histories and states to permitted transitions. It can be simpler and more declarative than the item: a set-based model for a cache, a ledger model for transfers, or a finite-state machine for a protocol. Execute commands against model and item, compare observable states, and retain the smallest divergence.

Model fidelity is the central risk. If the model repeats the production algorithm line for line, agreement offers little independence. Prefer different representation, abstraction, algorithm, language, data source, or author where consequence justifies it. Define correspondence between model state and system state; an abstraction can intentionally omit performance or internal layout.

For concurrency, a correct result may be any history satisfying a consistency condition. The oracle may search for a permitted sequential explanation, check happens-before constraints, or evaluate invariants. Bounds and checker assumptions must be explicit; a checker timeout is inconclusive/error, not pass.

### Metamorphic and relational oracles

When exact answers are unavailable, relate multiple executions. If a sorting function receives a permutation of the same input, sorted output should remain equal. Scaling every geometric length by $k>0$ should scale area by $k^2$ under the model. Adding a zero-weight item should not change a valid weighted sum.

A metamorphic relation is itself a specification fragment and can be wrong or too weak. A constant-output defect satisfies many invariance relations. Use diverse relations, validate their preconditions, and combine them with direct oracles where possible. The relation reveals disagreement with the stated property; it may not identify which execution is wrong.

Round-trip properties are relational: decode(encode(x)) = x for supported values. They can pass when encoder and decoder share a compatible defect. Add authoritative vectors, canonical-form checks, cross-implementation cases, and rejection tests.

### Differential and pseudo-oracles

Differential testing compares implementations, versions, configurations, or execution engines. Disagreement is valuable because it produces a concrete question. Agreement is weaker: systems can share specifications, libraries, code, algorithms, training data, or misconceptions.

Define the comparison domain and permitted variation. A new version may intentionally change formatting while preserving semantics. Majority vote is not truth when implementations are correlated. Investigate provenance and seek an authoritative or independently derived tie-breaker.

A previous version can be a regression oracle only for behavior intended to remain stable. It must not freeze a defect or block a deliberate change. Record compatibility policy and migration expectations.

### Implicit, heuristic, and crash oracles

An implicit oracle recognizes generic symptoms: crash, sanitizer finding, uncaught exception, deadlock, memory violation, resource leak, or malformed output. These are powerful for fuzzing and broad exploration because they require little domain-specific expected data.

They are partial. A program can return a confidently wrong answer without crashing. “No exception” is often a precondition for deeper checking, not a functional verdict. Heuristic oracles—suspicious log pattern, visual anomaly, unusual distribution—should usually produce candidate/inconclusive findings for investigation unless their decision rule has been validated.

### Approximate and floating-point oracles

Exact binary equality is often inappropriate for numerical algorithms, but `abs(actual-expected) < 0.01` is not automatically sound. Choose absolute, relative, unit-in-last-place, interval, or problem-specific error based on scale, conditioning, algorithm, units, and consequence.

A combined comparison can be

$$
|a-e|\le \epsilon_{abs}+\epsilon_{rel}|e|.
$$

This is a policy, not a universal formula. Near zero, absolute tolerance matters; at large magnitude, relative tolerance may dominate. NaN, infinities, signed zero, overflow, underflow, discontinuities, and units require explicit cases. Independently recompute critical values at higher precision or with interval/error bounds.

### Temporal and nondeterministic oracles

Wall-clock assertions such as “sleep 100 ms and expect completion” mix behavior with scheduler/load noise. Prefer controlled clocks, explicit synchronization, event observation, and eventually-within predicates with justified bounds. A time window needs a start event, clock source, environment/load, percentile or worst-case interpretation, and consequence of late completion.

For stochastic systems, expectations may concern distributions rather than individual outputs. Define population, sample process, seed/control, statistic, threshold, confidence method, power, multiple comparisons, stationarity, and drift. A single surprising output may be permitted; a biased distribution may fail. Statistical acceptance never establishes safety for rare unmodeled modes.

### Human oracles

Humans judge usability, visual quality, clinical meaning, legal interpretation, harm, and novel output where automation is incomplete. They bring tacit knowledge and can revise the basis, but they are variable, fatigued, biased, costly, and sometimes unauthorized.

Define reviewer qualifications, materials, task, rubric, blinding/independence, disagreement resolution, evidence retention, and decision authority. Separate expert observation from formal acceptance. Human review can be sampled and tested for consistency, but a consensus count does not make an incorrect standard correct.

### Build and test an oracle portfolio

Start with a claim and plausible failure. Choose the least costly oracle that can detect it with adequate trust. Combine independent channels for high consequence:

1. authoritative examples or test vectors;
2. invariants and forbidden-effect checks;
3. independent model/recomputation;
4. metamorphic or differential comparison;
5. operational reconciliation and monitoring;
6. qualified human validation.

Test the oracle itself. Introduce known-invalid outputs, mutate predicates, corrupt fixtures, remove required events, duplicate effects, cross boundaries, and force missing observations. Confirm fail/inconclusive/error paths. Review oracle changes as production changes because weakening one predicate can silently make an entire suite green.

## Definitions and Notation

Let $B_v$ be the versioned test basis, $P_v$ the test item, $t=(s_0,i)$ the prestate/input, $e$ the environment, and $\Omega$ the universe of possible effects. Observation function $obs_Q:\Omega\to Q$ projects effects into observable set $Q$; effects outside $Q$ are invisible to that oracle.

Let the specification define permitted observations:

$$
A_{B_v}(t,e)=\{q\in Q\mid predicates_{B_v}(q,t,e)\}.
$$

The verdict is:

$$
O(q)=
\begin{cases}
pass & q\in A\ \text{and required evidence is complete}\\
fail & q\notin A\ \text{under a valid basis}\\
inconclusive & basis/observation cannot distinguish membership\\
error & oracle execution or evidence collection failed.
\end{cases}
$$

An oracle is **sound for rejection** relative to a model if every fail verdict is a real model violation. It is **complete for rejection** if every model violation it is intended to detect yields fail. Real oracles are often partial and neither universally sound nor complete because basis, observation, implementation, and environment can be wrong.

For multiple oracle predicates $o_1,\ldots,o_n$, conjunction means pass only if every required predicate passes. Do not aggregate non-compensable predicates into an average score. Missing evidence should propagate according to declared three-/four-valued logic rather than coercing unknown to true.

## Mechanisms, Invariants, or Proof Structure

Use this oracle-design mechanism:

1. **State the claim:** exact property, item/version, conditions, and risk.
2. **Select the basis:** authoritative sources, precedence, provenance, ambiguity, and change policy.
3. **Define accepted behavior:** required, permitted, forbidden, conditional, approximate, and unspecified outcomes.
4. **Define observation:** values, state, events, absences, timing, resources, identity, and evidence completeness.
5. **Choose oracle sources:** exact, predicate, model, relational, differential, implicit, statistical, or human.
6. **Analyze independence:** shared algorithms, code, data, people, specification, and infrastructure.
7. **Define verdict logic:** pass, fail, inconclusive, error, severity, and escalation.
8. **Challenge the oracle:** positive/negative controls, boundaries, ambiguity, mutation, missing evidence, and self-failure.
9. **Version evidence:** basis, expected data, oracle code, toolchain, environment, and result.
10. **Review and evolve:** respond to requirement, incident, domain, implementation, and environment changes.

The invariants are claim-to-oracle traceability, explicit observation boundaries, no unknown-to-pass coercion, source provenance, common-mode analysis, and authority proportional to consequence.

This deterministic example combines three predicates for a transfer. A missing observation produces `INCONCLUSIVE`, not pass. It demonstrates only verdict propagation for declared fields; it does not validate financial rules, authorization, concurrency, durability, accounting, regulation, or production architecture.

<!-- bijux-verify: {"id":"transfer-oracle-verdicts","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid-transfer PASS\nmissing-audit FAIL[audit_count]\nunknown-balance INCONCLUSIVE[balance_after]\nsummary PASS=1 FAIL=1 INCONCLUSIVE=1\n","stderr":""}} -->
```python
cases = [
    {
        "name": "valid-transfer",
        "balance_before": 100,
        "amount": 30,
        "balance_after": 70,
        "audit_count": 1,
        "authorized": True,
    },
    {
        "name": "missing-audit",
        "balance_before": 100,
        "amount": 30,
        "balance_after": 70,
        "audit_count": 0,
        "authorized": True,
    },
    {
        "name": "unknown-balance",
        "balance_before": 100,
        "amount": 30,
        "balance_after": None,
        "audit_count": 1,
        "authorized": True,
    },
]

counts = {"PASS": 0, "FAIL": 0, "INCONCLUSIVE": 0}
for case in cases:
    unknown = [
        field
        for field in ("balance_before", "amount", "balance_after", "audit_count", "authorized")
        if case[field] is None
    ]
    failures = []
    if not unknown:
        if not case["authorized"]:
            failures.append("authorized")
        if case["balance_after"] != case["balance_before"] - case["amount"]:
            failures.append("balance_after")
        if case["audit_count"] != 1:
            failures.append("audit_count")

    if unknown:
        verdict = "INCONCLUSIVE"
        detail = f"[{','.join(unknown)}]"
    elif failures:
        verdict = "FAIL"
        detail = f"[{','.join(failures)}]"
    else:
        verdict = "PASS"
        detail = ""
    counts[verdict] += 1
    print(f"{case['name']} {verdict}{detail}")

print("summary " + " ".join(f"{key}={counts[key]}" for key in counts))
```

The order of checks is intentional: missing required evidence prevents evaluation. In a real transfer oracle, multiple independent state and event sources, retry histories, concurrency, identifiers, currency/rounding rules, and failure atomicity would be required.

## Alternatives and Trade-Offs

**Exact expected values** are clear and diagnostic but expensive to author and brittle when behavior is legitimately flexible. **Predicate oracles** accept meaningful variation and scale well but may omit properties. Use exact values for canonical cases and predicates for wider semantic space.

**Golden/snapshot testing** detects unreviewed change cheaply. Large snapshots hide semantics and encourage automatic approval. Prefer focused semantic assertions or reviewed canonical artifacts; retain snapshots where whole-output compatibility is the claim.

**Reference implementations** can generate many expectations. They risk common-mode faults and version drift. Increase diversity of algorithm, author, source, and representation; treat disagreement as investigation rather than automatic blame.

**Metamorphic testing** works without exact answers and expands exploration. Relations can be weak and produce ambiguous blame. Combine diverse relations with direct anchors.

**Human review** can judge intent and qualities that resist automation. It is slow, variable, and difficult to reproduce. Automate preparation and obvious checks, then reserve qualified attention for irreducible judgment with a rubric and audit trail.

**Strict oracles** catch deviations but over-specification raises maintenance cost and blocks harmless change. **Permissive oracles** tolerate evolution but miss faults. Specify semantic compatibility boundaries and deliberately leave irrelevant details unspecified.

**Production comparison/reconciliation** uses realistic data and dependencies but detects problems after exposure and may raise privacy or contamination risks. Use shadowing, redaction, bounded rollout, reversible actions, authorization, and offline reconciliation appropriate to consequence.

## Failure Modes and Misconceptions

- **“The specification is the oracle.”** It is oracle information; comparison still needs case conditions, observations, interpretation, and verdict logic.
- **“Actual equals expected, so correct.”** The expected result, observation, or basis may be wrong or incomplete.
- **“A human expected it, so it is valid.”** Qualification, authority, rubric, independence, and evidence matter.
- **“A snapshot is objective.”** Its origin and update process determine trust; it may preserve a defect.
- **“The old version is truth.”** It is useful only for behavior intended to remain compatible.
- **“Two implementations agree.”** Agreement can arise from shared code, data, standards misunderstanding, or correlated design.
- **“No crash means pass.”** A crash oracle checks robustness symptoms, not semantic correctness.
- **“Nondeterministic means either result is fine.”** The permitted set and probability/history constraints still need specification.
- **“Add a tolerance to remove flakes.”** Tolerance must follow numerical/time semantics and environment evidence.
- **“Logs prove the side effect.”** A log may be emitted without durable effect or omitted after success; correlate authoritative observations.
- **“Missing observation means no failure.”** It means inconclusive/error unless absence itself is reliably observable.
- **“A strong oracle compensates for weak test data.”** Oracle and selection address different gaps.
- **“Passing the oracle proves fitness.”** It verifies encoded expectations; stakeholder validation remains separate.
- **“Oracle code is just tests.”** It is decision-critical software and needs review, negative tests, provenance, and change control.

## Worked Examples

### Example 1

**Question:** Is `status == 200` an adequate oracle for a money transfer?

**Reasoning:** It checks one response field but not authorization, balances, currency, ledger event, idempotency, disclosure, or failure atomicity. It may serve as one predicate in a larger oracle portfolio.

**Conclusion:** An oracle’s adequacy is relative to the claim and failure risks, not its syntactic correctness.

### Example 2

**Question:** A list API may return records in any order. Should a snapshot compare exact JSON?

**Reasoning:** Exact comparison freezes unspecified order and incidental formatting. Compare schema, record identity/content, multiplicity, authorization, pagination, and perhaps a multiset. Preserve exact order only if the contract specifies it.

**Conclusion:** Accepted sets should exclude defects without specifying irrelevant variation.

### Example 3

**Question:** Production and a rewritten calculator agree on every generated case. Is the rewrite correct?

**Reasoning:** Agreement finds no divergence but both may share the same formula, table, rounding library, or mistaken requirement. Add authoritative examples, independent derivation, boundary cases, and property checks.

**Conclusion:** Differential agreement is evidence whose strength depends on independence.

### Example 4

**Question:** How can sorting be tested when expected results are costly to enumerate?

**Reasoning:** Check nondecreasing order, output is a permutation of input, length preservation, idempotence, and invariance under input permutation. A constant empty output might satisfy order/idempotence but fails permutation and length.

**Conclusion:** Multiple independent properties constrain a partial oracle more strongly.

### Example 5

**Question:** Is `abs(actual-expected) < 0.01` a correct floating-point oracle?

**Reasoning:** Not without units, scale, conditioning, and consequence. It is too loose around tiny safety thresholds and too strict for huge magnitudes. Choose absolute/relative/error-bound policy, address NaN/infinity, and independently recompute.

**Conclusion:** A tolerance is a domain decision, not a generic repair for numerical tests.

### Example 6

**Question:** A message is not visible after 500 ms. Should an eventual-consistency test fail?

**Reasoning:** Define the guarantee: clock, start event, load, percentile/worst case, retry and observation completeness. If the SLA is two seconds, continue controlled observation; if the observer failed, return error/inconclusive.

**Conclusion:** Temporal oracles need justified windows and trustworthy event observation.

### Example 7

**Question:** A protocol permits either `RETRY` or `REJECT` after a timeout. Can the test accept every response?

**Reasoning:** No. The permitted set contains two values only under stated preconditions, and each may impose state/event obligations. `COMMIT` or silent corruption remains forbidden.

**Conclusion:** Nondeterministic specifications still constrain accepted behavior.

### Example 8

**Question:** A golden file changes after an intended UI redesign. May it be regenerated?

**Reasoning:** Re-establish the basis: approved design, accessibility semantics, localization, critical content, and supported viewports. Review a semantic/visual diff and targeted assertions, then regenerate with provenance. Intentional change does not prove correct change.

**Conclusion:** Update oracle artifacts only after validating the new expectation.

### Example 9

**Question:** Can a learned model judge whether an intensive-care dose recommendation is correct?

**Reasoning:** A model may flag disagreement, but its training data, target labels, population, calibration, shifts, correlated errors, and clinical authority limit it. No external academic, clinical, regulatory, safety, or practitioner review is claimed. Named qualified clinicians, pharmacists, clinical-safety, data/model, human-factors, cybersecurity/privacy, quality, independent-assurance, and regulatory authorities must define claims, reference evidence, failure actions, residual risk, and release authority.

**Conclusion:** An automated high-stakes oracle can assist qualified judgment but cannot manufacture ground truth or authorization.

### Example 10

**Question:** Mutation testing changes `audit_count == 1` to `audit_count >= 0`, and all oracle tests pass. What follows?

**Reasoning:** The tests do not prove the oracle rejects missing/duplicate audit effects. Add negative controls for zero and two, verify diagnostic verdicts, and review whether exactly-once is truly the required property.

**Conclusion:** Test the test oracle’s sensitivity, including its own specification.

## Cross-Program Connections

- [Theory of Programming](../../07-programming-languages-theory-of-programming/ROADMAP.md) provides formal specifications, refinement, proof obligations, and model limits.
- [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies domain invariants and stakeholder-grounded expected outcomes.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) connects quality scenarios and evidence to significant decisions.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) provides independent algorithms, invariants, numerical reasoning, and complexity expectations.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) contributes transactional, constraint, and state-observation oracles.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies forbidden-effect, authorization, confidentiality, and adversarial oracle requirements.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29119-1:2022, Software and systems engineering—Software testing—Part 1: General concepts](https://www.iso.org/standard/81291.html), edition 2, January 2022. Current general concepts including expected result, test basis, test oracle, oracle problem, strategy, and testing context; consulted 2026-08-29.
2. IEEE Computer Society. [SWEBOK Guide v4.0a](https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf), Software Testing knowledge area, updated September 2025. Oracle sources, inconclusive outcomes, automation, testability, and design foundations; consulted 2026-08-29.
3. Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin Yoo. [“The Oracle Problem in Software Testing: A Survey”](https://discovery.ucl.ac.uk/id/eprint/1471263/), *IEEE Transactions on Software Engineering* 41(5), 2015, pp. 507–525, DOI 10.1109/TSE.2014.2372785. Primary survey taxonomy and analysis of oracle information and automation.
4. Elaine J. Weyuker. “On Testing Non-Testable Programs.” *The Computer Journal* 25(4), 1982, pp. 465–470. Foundational pseudo-oracle and testing-without-known-answer reasoning.
5. T. Y. Chen, S. C. Cheung, and S. M. Yiu. “Metamorphic Testing: A New Approach for Generating Next Test Cases.” Technical Report HKUST-CS98-01, 1998. Foundational metamorphic-testing construction.
6. Cem Kaner, Jack Falk, and Hung Quoc Nguyen. *Testing Computer Software*, second edition, Wiley, 1999. Expected results, human judgment, test design, and practical oracle failure modes.
7. Paul Ammann and Jeff Offutt. *Introduction to Software Testing*, second edition, Cambridge University Press, 2017. Test criteria, specifications, models, coverage, mutation, and oracle construction.

## Exercises

### Exercise 1

For a function that returns unique customer IDs in unspecified order, classify required, permitted, forbidden, and unspecified behavior, then define a minimal oracle.

### Exercise 2

Derive an oracle portfolio for transferring 30 units from a balance of 100 under retry, including pass, fail, inconclusive, and oracle-error outcomes.

### Exercise 3

Diagnose a suite that copies production JSON into snapshots, ignores database/events, retries every mismatch three times, and converts persistent mismatches into warnings.

### Exercise 4

Compare exact-value, model, metamorphic, and differential oracles for a scientific numerical solver whose authoritative answers are scarce.

### Exercise 5

Design oracle assurance for unfamiliar autonomous railway braking software. Separate automation, independent recomputation, human review, and release authority.

## Answers to the Exercises

### Answer 1

Required: every eligible customer appears exactly once and every returned value is a valid customer ID for the stated snapshot/authorization scope. Forbidden: duplicates, ineligible/other-tenant IDs, malformed identifiers, omission of eligible IDs, unauthorized side effects, or errors under valid conditions. Permitted: any ordering if the contract says order is irrelevant. Unspecified details—such as internal query order—must not be frozen.

Construct an independently trusted eligible-ID set from a fixture/model; validate response schema; compare returned IDs as a set plus cardinality (set equality alone can hide duplicates); check authorization scope and relevant side effects. If the source snapshot or authorization evidence is unavailable, return inconclusive/error. Version fixture, contract, and comparison normalization.

### Answer 2

Basis: currency/unit and rounding rule, authorization policy, ledger/transfer contract, idempotency contract, and failure semantics. Observe authoritative pre/post balances, immutable ledger entries, response, idempotency key, emitted events, authorization evidence, and dependency outcome. For a successful transfer: source decreases from 100 to 70, destination increases by 30, total is conserved, one transfer identity/ledger effect exists, one permitted event is durably associated, and retry returns the same outcome without another effect. Forbidden outcomes include unauthorized change, partial debit/credit, duplicate effect, cross-tenant disclosure, and success response before required durability.

Pass requires all required observations/predicates. Fail follows a valid violation. Inconclusive applies when an authoritative balance/event cannot be observed or specification interpretations conflict. Error applies when setup, collector, model, or comparison fails. Add negative controls for missing/duplicate audit and ledger events, unauthorized actor, insufficient funds, timeout before/after commit, retry, and observer outage. Independent recomputation and reconciliation reduce common-mode risk.

### Answer 3

The snapshots are circular historical oracles unless their original behavior was independently approved. They inspect one response projection and miss persistent state, events, authorization, and forbidden effects. Retries hide nondeterminism and can multiply irreversible behavior; warnings coerce repeated failure into practical pass.

Recover the test basis and semantic claims. Replace or supplement snapshots with focused schema/value/invariant/state/event/security predicates and authoritative fixtures/models. Preserve retry histories and idempotency effects; classify first discrepancy, observer error, and nondeterminism explicitly. Add negative controls and mutations to test oracle sensitivity. Review existing snapshots before regenerating them, record provenance, and make unresolved valid mismatches fail or block according to risk rather than warning silently.

### Answer 4

Exact values give strong anchors for the scarce authoritative cases; include boundaries and published benchmarks with version/provenance. A simpler independent high-precision or interval model can generate broader expectations, but its equations, conditioning, discretization, and implementation need review. Metamorphic relations—scaling, symmetry, conservation, monotonicity, refinement convergence where mathematically valid—expand coverage without exact values; diverse relations reduce constant/wrong-model loopholes. Differential comparison across independent solvers exposes disagreement, but shared libraries, methods, tolerances, and standards can correlate errors.

Combine all four. Define units, domains, tolerances/error bounds, NaN/infinity behavior, convergence/non-convergence, resource bounds, and observation precision. Use higher precision or interval arithmetic for selected recomputation; manufacture problems with known solutions; check residuals and invariants; analyze independence; preserve inconclusive for ill-conditioned or unsupported cases. None of these validates that the mathematical model represents the physical phenomenon; domain validation remains necessary.

### Answer 5

Automated oracles can check input/schema/provenance; units and range constraints; state-machine transitions; bounded model properties; timing under declared hardware/load; sensor disagreement and failure modes; command limits; authentication/integrity; trace links; build/configuration identity; fault-injection results; logs; and evidence freshness. Independently recompute braking curves and invariants using a different implementation/representation, reviewed assumptions, dimensional analysis, boundary/adversarial cases, and defined numerical error bounds. Simulations and hardware-in-the-loop tests remain scoped empirical evidence.

No external academic, railway, regulatory, safety, or practitioner review is claimed. Named qualified railway-domain, control, safety, software, hardware, operations, human-factors, cybersecurity, quality/independent-assurance, and applicable regulatory authorities must review operational scenarios, hazards, sensor/actuator models, environmental bounds, degraded/manual modes, model correspondence, oracle independence, coverage gaps, evidence, residual risk, change control, and emergency response. Automated disagreement must move to a fail/inconclusive/escalation path; it cannot authorize risk acceptance. Release authority and safety-case acceptance must be explicitly assigned to qualified independent roles under applicable railway assurance, with unresolved critical evidence blocking deployment.
