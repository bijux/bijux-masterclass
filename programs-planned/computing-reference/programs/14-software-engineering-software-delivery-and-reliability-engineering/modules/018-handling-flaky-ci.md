---
module_id: SDRE-018
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 18
title: Handling Flaky CI
status: complete
last_verified: 2026-09-06
---

# Handling Flaky CI

## One-Page Review

### Governing question

How should a delivery system detect, classify, contain, and repair nondeterministic CI outcomes without hiding regressions or teaching developers to ignore failures?

### Essential definitions

- a **flaky test** produces different outcomes under executions intended to have the same relevant subject and conditions;
- a **flaky CI job** varies because of tests, the system under test, runner, orchestration, dependency, network, or another uncontrolled input;
- **reproduction** recreates a recorded failing execution closely enough to investigate it;
- **rerun** executes again and provides another observation, not a replacement outcome;
- a **seed** controls one source of pseudorandom choice;
- an **order-dependent test** changes outcome according to tests that execute before it;
- a **polluter** leaves state that affects another test; a **victim** observes that state;
- a **heisenbug** changes manifestation when observation changes timing or state;
- **quarantine** temporarily removes an unreliable test from blocking policy while continuing visible execution, ownership, and repair;
- a **flake signature** groups outcomes by test, failure, environment, order, seed, and relevant diagnostics;
- **flake rate** is observed variable-outcome frequency under a stated population and window;
- **determinization** exposes or controls time, randomness, scheduling, state, and external dependencies;
- **infrastructure failure** prevents valid test evidence and is not automatically test flakiness.

### Central model, mechanism, or theorem

If independent executions fail with constant probability $p$, the probability that $n$ executions reveal at least one failure is

$$
1-(1-p)^n.
$$

For $p=0.1$, ten runs detect a failure with probability about $0.6513$; even ten passes occur with probability about $0.3487$. This model explains why a few reruns cannot prove stability. Real executions are often correlated and $p$ changes with load, order, and environment, making the simple model optimistic or inapplicable.

### Critical invariants

- preserve the first failure and every rerun as separate observations;
- bind outcomes to exact subject, test identity, environment, order, seed, attempt, and time;
- never convert fail-then-pass into an original pass;
- classify product failure, test defect, environment defect, and infrastructure loss separately;
- reproduce in isolation and in relevant orders;
- replace sleeps with condition-based synchronization and bounded timeouts;
- isolate mutable state, clocks, randomness, ports, files, databases, and accounts;
- quarantine only with owner, rationale, scope, issue, expiry, and visible non-blocking execution;
- preserve the coverage claim lost by quarantine;
- prevent flaky evidence from silently satisfying a quality gate;
- measure both test-level and fleet-level instability;
- prioritize repair by risk, frequency, reach, and diagnostic cost.

### Common failures

Common failures include rerunning until green, deleting the original failure, assuming all intermittent failures are test bugs, adding longer sleeps, fixing one seed while ignoring order, sharing mutable fixtures, using wall-clock time, depending on public networks, quarantining forever, measuring only final job status, and declaring a test stable after a small number of passes.

### Compact example

Test B expects an empty cache. Test A populates the cache but does not clean up. Order B,A passes; A,B fails. Rerunning B alone passes and can mislead triage. Record the failing order, reproduce A,B, give each test isolated state or restore the fixture, and add randomized-order detection. A retry is evidence of variability; it is not the repair.

### Connections

[SDRE-017](017-quality-gates.md) defines incomplete and waived outcomes. Flaky evidence must use those states honestly. [SDRE-019](../ROADMAP.md) next protects CI secrets and untrusted contributions, and [SDRE-020](../ROADMAP.md) balances feedback time against hidden risk.

## Governing Question

CI is valuable because a failure directs attention toward a candidate defect and a pass supports admission. Flakiness weakens both meanings. Developers waste time on failures unrelated to their changes, while retry-to-green workflows admit revisions after discarding contrary evidence.

The solution is not to demand metaphysical determinism. Distributed systems, schedulers, hardware, and external services vary. The solution is to make relevant variation observable and controlled, preserve contradictory outcomes, classify causes, contain unreliable evidence, and repair the responsible boundary.

## Why This Matters

A flaky test creates false rejections when good candidates fail and false acceptance pressure when teams normalize retries. Trust decays nonlinearly: once developers expect red builds to be noise, real regressions receive slower investigation.

Bell et al.'s DeFlaker study treats flaky failures as outcomes not caused by the current change and evaluates differential-coverage detection against reruns [1]. Lam et al.'s iDFlakies work distinguishes order-dependent from other flaky tests and uses reordered executions to expose them [2]. These are detection techniques with empirical limits, not universal classifiers.

Google's public flakiness guidance separates causes across tests, test frameworks, systems under test and dependencies, and OS, hardware, and network [3]. Current pytest documentation likewise warns that flakiness may emerge under parallel execution and points to order and state isolation [4]. The durable lesson is to investigate the whole execution system rather than blame test code by default.

## Prerequisites and Retrieval

Retrieve deterministic function, nondeterminism, probability, independence, conditional probability, random seed, clock, timeout, race, data race, scheduling, shared state, fixture, setup, teardown, process, environment variable, network, retry, idempotence, log, trace, artifact, percentile, false positive, false negative, and test oracle.

From SDRE-006 through SDRE-010 retrieve test layers, automation, and evidence. From SDRE-015 retrieve parallel scheduling and isolation; from SDRE-016 retrieve invalidation and retry identity; from SDRE-017 retrieve pass, fail, incomplete, waiver, and gate semantics. Concurrent & Parallel Programming owns race mechanisms; Testing & Quality Engineering owns oracle and test-design depth.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish flaky tests, flaky jobs, and infrastructure failures;
2. explain why a passing retry does not erase a failure;
3. calculate simple rerun detection probabilities and state their assumptions;
4. capture enough execution identity for reproduction;
5. diagnose order, time, random, state, concurrency, and external-dependency causes;
6. replace timing guesses with observable synchronization;
7. design bounded quarantine with retained risk visibility;
8. prioritize repairs using impact and evidence;
9. test the flake-handling system itself;
10. report uncertainty without weakening quality gates.

## Core Exposition

**Define sameness before calling an outcome flaky.** “The same test failed once and passed later” omits relevant inputs. Record source revision, built artifact, test binary, test data, configuration, dependency versions, runner image, architecture, resource limits, locale, timezone, clock, seed, suite order, shard, parallelism, network endpoints, retries, and attempt time.

Some differences are intended experimental factors. Running with many seeds or schedules deliberately explores behavior; a failure found there can be a real product defect, not a flaky test. Flakiness describes unreliable test evidence under the intended contract, not any nondeterministic program behavior.

**Preserve the outcome sequence.** Model attempts as an ordered record: initial fail, retry pass, later fail. Never overwrite it with final pass. The quality gate can return unstable or incomplete, apply a declared retry policy, or consult quarantine. The developer needs the first logs because reruns can alter state and timing.

Name attempts under one logical check and exact subject. Distinguish rerunning the same subject from rebuilding after code, environment, or policy changes. The latter is new evidence, not another sample from the same population.

**Classify before acting.** At least four categories matter. A product defect is real behavior exposed intermittently, such as a race. A test defect has an invalid oracle, timing assumption, or leaked fixture. An environment defect supplies uncontrolled state or unavailable dependency. Infrastructure loss prevents a valid execution, such as a terminated runner or artifact-transfer failure.

Categories can overlap. A test that waits 100 ms for an asynchronous product event may contain a bad timing assumption and expose a product latency regression. Preserve observations and narrow hypotheses rather than immediately labelling “flake.”

**Capture replay inputs.** On failure, retain command, subject and artifact digests, seed, order, shard manifest, concurrency, timing events, stdout, stderr, structured logs, traces, screenshots where relevant, resource metrics, dependency responses or safe identifiers, and cleanup results. Redact credentials while preserving diagnostic structure.

Prefer event timelines and monotonic clocks for durations. Wall-clock jumps can manufacture negative or excessive elapsed times. Record timeout origin: test framework, process supervisor, CI job, load balancer, or external service.

**Investigate order dependence.** Run the test alone, in its failing prefix, after suspected polluters, and under randomized or reversed orders. An isolated pass does not clear the test; it supports a shared-state hypothesis. Minimize the failing prefix while preserving environment.

Zhang et al. formalize test dependence using ordered test sequences and explicit environments and show that dependence can mask product faults or create spurious reports [5]. Repair by owning setup and teardown, using unique namespaces, resetting global registries, restoring environment variables, closing processes, and avoiding reliance on another test's initialization.

Parallel execution changes partial order and resource contention. A suite stable serially may race on files, ports, accounts, database rows, or singletons. Do not solve this only by forcing serial execution unless the resource is genuinely exclusive; doing so can preserve hidden coupling and lose feedback speed.

**Control time and asynchronous behavior.** Fixed sleeps assert that an event completes before an arbitrary duration. Under a faster or slower machine, both false passes and false failures remain possible. Wait for an observable condition with a bounded timeout, report the final observed state, and make polling interval and deadline explicit.

Inject clocks where practical. Test deadlines, expiration, retry backoff, and daylight transitions against controlled time. Distinguish monotonic duration from civil time. Preserve real-clock integration tests for system boundaries, but run them with broader tolerances and diagnostic evidence.

**Control randomness.** Seed pseudorandom generators and record the seed, generator, and version. A fixed seed aids replay but exercises one path; run a governed seed set or property-based exploration and minimize failing cases. Hidden randomness can exist in hash iteration, generated identifiers, sampling, or dependency libraries.

A passing rerun with a different undisclosed seed is not a reproduction. A failure that repeats only with seed 91 is still actionable if seed 91 lies inside the supported input contract.

**Isolate external state.** Give each test unique files, databases, tenants, accounts, topics, ports, and object names. Setup should establish the full precondition; teardown should be idempotent and observable. Prefer ephemeral local dependencies or controlled fakes for narrow behavior, then retain bounded real integration tests for contracts fakes cannot establish.

Public networks, mutable registries, shared staging services, rate limits, certificate rotation, and clock skew create failures outside candidate control. Classify them, record dependency identity and response, and avoid letting an external outage silently pass a release gate. Use contract snapshots or service virtualization where it preserves the tested claim.

**Use reruns as experiments.** Rerun to reproduce, estimate, or classify—not to make the dashboard green. Hold relevant inputs constant for one experiment; vary one suspected factor for another. Compare fresh process versus same process, isolated versus suite order, serial versus parallel, fixed versus varied seed, and controlled versus external dependency.

The independent constant-$p$ model gives intuition but rarely proves stability. Runs on one host can share cache, load, order, and network conditions. Correlation reduces information. Report sample construction, not just “passed 100 times.”

If independent failure probability is $p>0$, $n$ all-pass runs occur with probability $(1-p)^n$. To obtain at least confidence $q$ of observing one failure, solve $1-(1-p)^n\ge q$. This assumes known, constant $p$ and independent executions; those assumptions are usually estimates.

**Quarantine without erasure.** Quarantine can restore signal to a blocking suite while repair proceeds, but it removes a coverage claim from admission. Keep the test running in a visible non-blocking lane, record every result, and show the lost claim in gate output.

A quarantine record contains test identity, subject scope, owner, issue, first and recent signatures, reason, risk, entry and expiry, repair target, compensating checks, and exit criteria. Expiry should block renewal without review. Delete obsolete tests or repair valuable ones; do not accumulate a permanent shadow suite.

High-risk tests may be non-quarantinable. If an unreliable test is the only check for payment integrity or migration safety, the appropriate response may be to stop admission, add a trustworthy replacement, or require manual controlled evidence.

**Repair root causes.** Common repairs include explicit initialization, independent fixtures, unique state, deterministic clocks, recorded seeds, condition waits, synchronized access, stable resource allocation, hermetic dependencies, idempotent cleanup, bounded retries in the product, and stronger observability. Verify the repair against the original failing signature and adversarial variants.

Removing the assertion, widening every timeout, serializing the suite, or retrying repeatedly may hide symptoms. A good repair restores the intended claim and remains stable under varied order, load, and schedule appropriate to that claim.

**Measure instability honestly.** Track initial failures, final outcomes, fail-pass and pass-fail transitions, attempts per logical run, quarantined inventory and age, repeated signatures, affected candidates, wasted compute, diagnosis time, repair time, and escaped defects linked to ignored outcomes. Segment by test, suite, runner, image, dependency, shard, order, and time.

Flake rate needs a denominator and population. `fail-pass transitions / logical runs` differs from `variable outcomes / attempts`. Report confidence or sample size, and avoid ranking a test with two runs above one with ten thousand without uncertainty.

Test the handling system with seeded unstable fixtures, simulated lost workers, malformed reports, quarantine expiry, and wrong-subject retries. Audit that initial failures remain visible and that quarantined tests cannot satisfy blocking claims.

## Definitions and Notation

Let $Y_i\in\{pass,fail\}$ be outcome of execution $i$ under a defined population of conditions. In the simple model, executions are independent and $\Pr(Y_i=fail)=p$ is constant. Then

$$
\Pr(\text{all }n\text{ pass})=(1-p)^n
$$

and

$$
\Pr(\text{at least one failure})=1-(1-p)^n.
$$

For target detection probability $q$, the smallest integer $n$ satisfies

$$
n\ge \frac{\log(1-q)}{\log(1-p)},\qquad 0<p<1,\ 0<q<1.
$$

For $p=0.1$ and $q=0.95$, the ratio is about $28.43$, so at least 29 independent runs are required. This does not establish that a real test has $p=0.1$ or that runs are independent.

Let an execution record be $e=(s,t,a,o,z,r)$ for subject $s$, test $t$, attempt $a$, order $o$, seed $z$, and relevant environment $r$. Comparing outcomes without comparing these fields can conflate changed inputs with nondeterminism.

## Mechanisms, Invariants, or Proof Structure

**Detection derivation.** Independence makes the probability of $n$ passes the product $(1-p)^n$. Its complement is at least one failure. Solving $1-(1-p)^n\ge q$ yields the logarithmic bound; division preserves the final direction after accounting for negative $\log(1-p)$.

**Contradictory-evidence invariant.** If one accepted execution fails and another passes for the same intended subject and conditions, the record contains variability. Selecting only the last observation loses evidence and cannot support a faithful gate decision.

**Order counterexample.** A populating test A followed by victim B fails, while B followed by A passes. Each test's code and subject remain fixed; ordered environment state changes. Therefore isolated reruns alone cannot exclude dependence.

**Quarantine invariant.** A quarantined test remains in inventory and execution but its result cannot satisfy the blocking claim it formerly supported. The gate reports that claim as waived, replaced, or incomplete under explicit policy.

**Executable flake model.** The model recomputes detection probabilities and an order-dependent state leak. It does not estimate any production test's failure probability.

<!-- bijux-verify: {"id":"flaky-ci-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ten_all_pass=0.3487\nten_detect=0.6513\nruns_for_95pct_detection=29\norder_dependent_detected=True\nfixed_sleep_is_proof=False\nretry_pass_is_original_pass=False\nquarantine_count=2\n","stderr":""}} -->
```python
p = 0.1
all_pass = (1 - p) ** 10
n = 1
while 1 - (1 - p) ** n < 0.95:
    n += 1
print(f"ten_all_pass={all_pass:.4f}")
print(f"ten_detect={1 - all_pass:.4f}")
print(f"runs_for_95pct_detection={n}")

def run_order(order):
    state = {"cache": set()}
    outcomes = {}
    for test in order:
        if test == "A":
            state["cache"].add("entry")
            outcomes[test] = True
        else:
            outcomes[test] = len(state["cache"]) == 0
    return outcomes

a_then_b = run_order(["A", "B"])
b_then_a = run_order(["B", "A"])
print(f"order_dependent_detected={a_then_b['B'] != b_then_a['B']}")
print("fixed_sleep_is_proof=False")
print("retry_pass_is_original_pass=False")
quarantine = {"test-clock", "test-shared-cache"}
print(f"quarantine_count={len(quarantine)}")
```

## Alternatives and Trade-Offs

**Immediate block versus quarantine.** Blocking preserves a claim but lets noise halt delivery. Quarantine restores signal but removes coverage. Choose by risk and require visible expiry and replacement.

**Same-condition rerun versus perturbation.** Same-condition reruns seek reproduction. Changed order, seed, load, or process seeks causal factors. Both are useful, but their evidence answers different questions.

**Fake versus real dependency.** Fakes provide control and speed but can drift from reality. Real services expose integration behavior but add variability. Use contract checks and bounded real tests alongside controlled narrower tests.

**Serial versus parallel tests.** Serial order reduces concurrency variation but hides races and costs time. Parallel execution exposes coupling but demands isolation. Serialize only genuinely exclusive resources.

**Fixed versus varied seeds.** Fixed seeds reproduce one path. Varied recorded seeds explore more behavior. Preserve failures and minimize cases.

**Long sleeps versus condition waits.** Sleeps are simple but slow and load-sensitive. Condition waits express intent and yield diagnostics, while still requiring bounded timeouts.

**Automatic versus human classification.** Automation clusters signatures and experiments quickly. Humans assess semantics and risk. Record uncertainty instead of granting an automatic flaky label unchecked authority.

**Test repair versus product repair.** A weak test may need isolation; intermittent behavior may be a real product race. Classification evidence determines ownership, and some incidents require both.

## Failure Modes and Misconceptions

- **“Pass on retry means pass.”** It means contradictory outcomes were observed.
- **“Intermittent means test bug.”** Product races and external failures can be intermittent.
- **“One rerun reproduces the conditions.”** state, order, seed, load, and dependency may differ.
- **“A hundred passes prove stability.”** Finite samples cannot prove zero failure probability.
- **“Reruns are independent.”** shared hosts and time windows often correlate them.
- **“A fixed seed removes nondeterminism.”** clocks, order, threads, and services remain.
- **“Run alone is the best reproduction.”** It can remove the polluter.
- **“Longer sleep fixes timing.”** It moves the failure boundary and slows tests.
- **“Timeout is one cause.”** framework, job, service, and product timeouts differ.
- **“Serial execution fixes shared state.”** It may preserve hidden order dependence.
- **“Infrastructure failures are flaky tests.”** No valid test outcome may exist.
- **“Quarantine means skip and forget.”** it requires visible execution, ownership, and expiry.
- **“Quarantined coverage still protects the gate.”** Its unreliable result cannot support that claim.
- **“Delete flaky assertions.”** This removes detection without fixing behavior.
- **“Final job status is enough to measure.”** transitions and attempts disappear.
- **“Low observed rate means low impact.”** rare flakes on high-frequency tests can dominate.
- **“Exact reproduction is always possible.”** some schedules are difficult; preserve bounded evidence.
- **“All nondeterminism is bad.”** deliberate varied schedules and inputs can find real defects.

## Worked Examples

### Example 1

**Situation.** A test fails, then passes on one automatic retry. **Reasoning.** Preserve both attempts with identical subject and differing runtime facts. Mark the logical result unstable or incomplete; do not overwrite failure. **Conclusion.** Retry is diagnostic evidence, not erasure.

### Example 2

**Situation.** A test with estimated independent $p=0.1$ passes ten times. **Reasoning.** Ten passes still have probability $0.9^{10}=0.3487$ under the model. Correlation can make them less informative. **Conclusion.** Small passing samples do not establish stability.

### Example 3

**Situation.** B passes alone but fails after A. **Reasoning.** Reproduce A,B and B,A, inspect shared files and registries, minimize the polluting prefix, then isolate or reset state. **Conclusion.** Test order is an input.

### Example 4

**Situation.** A UI test sleeps two seconds before reading a status. **Reasoning.** Under load the event takes 2.1 seconds. Poll for the target state with a deadline, capture the last state, and inspect product latency separately. **Conclusion.** Synchronize on conditions rather than guessed duration.

### Example 5

**Situation.** A property test fails under seed 91 and passes under default seed. **Reasoning.** Record generator version and seed 91, replay it, minimize the input, and keep varied-seed runs. **Conclusion.** A seed-specific failure is actionable, not noise.

### Example 6

**Situation.** Parallel shards update the same customer account. **Reasoning.** Their identifiers collide and outcomes depend on timing. Allocate per-test tenants or unique data and verify cleanup. **Conclusion.** Logical independence requires environmental isolation.

### Example 7

**Situation.** Artifact download fails because a runner loses network. **Reasoning.** No test ran, so classify infrastructure loss and retry transfer or attempt under bounded policy. Do not count a test failure or pass. **Conclusion.** Evidence availability differs from test outcome.

### Example 8

**Situation.** A flaky payment-integrity test blocks half of releases. **Reasoning.** Because it is the only evidence for a critical claim, silent quarantine is unsafe. Stop admission or add a trustworthy replacement and controlled manual evidence while repairing. **Conclusion.** Quarantine authority depends on lost risk coverage.

### Example 9

**Situation.** Quarantine contains 80 tests with no expiry. **Reasoning.** Restore owners, issues, age, signatures, risk, and exit criteria; delete obsolete checks and prioritize high-impact repairs. Block new unowned entries. **Conclusion.** Permanent quarantine is unmanaged policy erosion.

### Example 10

**Situation.** A repair makes 500 repeated runs pass on one runner image. **Reasoning.** Replay the original signature, vary relevant order, concurrency, seed, load, and supported platforms, and retain finite-sample language. **Conclusion.** Verify the causal repair without claiming universal determinism.

## Cross-Program Connections

- Testing & Quality Engineering owns test oracles, fixture design, coverage, mutation, and statistical evaluation.
- Concurrent & Parallel Programming owns races, schedules, memory visibility, and synchronization.
- Operating Systems owns clocks, processes, resources, signals, and scheduler variation.
- Distributed Systems owns timeouts, retries, partial failure, idempotence, and external-service uncertainty.
- Platform Engineering owns runner images, isolation, artifact transfer, fleet telemetry, and quarantine services.
- Security Engineering owns diagnostic redaction, untrusted tests, and non-waivable critical claims.
- Data Engineering owns reproducible datasets, lineage, cleanup, and shared-environment hazards.
- Algorithm Engineering owns randomized exploration, minimization, and sampling analysis.

## References

1. Jonathan Bell et al., [DeFlaker: Automatically Detecting Flaky Tests](https://doi.org/10.1145/3180155.3180164), ICSE 2018, pp. 433–444.
2. Wing Lam, Reed Oei, August Shi, Darko Marinov, and Tao Xie, [iDFlakies: A Framework for Detecting and Partially Classifying Flaky Tests](https://sites.utexas.edu/august/files/2020/08/ICST2019-flaky.pdf), ICST 2019.
3. George Pirocanac, [Test Flakiness—One of the Main Challenges of Automated Testing, Part II](https://testing.googleblog.com/2021/03/test-flakiness-one-of-main-challenges.html), Google Testing Blog, 2021.
4. pytest Project, [Flaky Tests](https://docs.pytest.org/en/stable/explanation/flaky.html), official documentation. Retrieved 2026-09-06.
5. Sai Zhang et al., [Empirically Revisiting the Test Independence Assumption](https://homes.cs.washington.edu/~mernst/pubs/test-independence-issta2014-abstract.html), ISSTA 2014, pp. 385–396.
6. Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, test-smell, fixture, and result-trustworthiness foundations.

## Exercises

### Exercise 1

Define flaky test, flaky CI job, rerun, order dependence, infrastructure failure, and quarantine. Explain why these categories must remain distinct.

### Exercise 2

Under the independent constant-probability model with $p=0.05$, derive the probability of detecting at least one failure in 20 runs and the probability all 20 pass. State why the result may mislead in CI.

### Exercise 3

A test passes alone, fails after `test_create_user`, uses a shared account, reads wall-clock time, and succeeds on retry. Design a diagnostic sequence and likely repairs without discarding the first failure.

### Exercise 4

Design quarantine policy for a release suite. Include admission authority, non-quarantinable claims, evidence, owner, expiry, execution, reporting, compensating controls, and exit criteria.

### Exercise 5

A team reports that flakiness fell from 4% to 0.2% after enabling three retries and showing only final status. Design an evaluation that determines whether reliability improved or evidence was hidden.

## Answers to the Exercises

### Answer 1

A flaky test varies under executions intended to share relevant subject and conditions. A flaky CI job may vary because of any job component, not only a test. A rerun is another observation. Order dependence makes outcome depend on earlier tests and shared environment. Infrastructure failure prevents valid execution rather than yielding a product assertion. Quarantine temporarily makes unreliable evidence non-blocking under governance. Keeping categories distinct preserves correct ownership, retry policy, gate semantics, and risk visibility.

### Answer 2

All-pass probability is $(1-0.05)^{20}=0.95^{20}\approx0.3585$. Detection probability is its complement, approximately $0.6415$. Thus even a genuinely 5%-flaky test passes all 20 runs more than one third of the time under the model. CI runs may also share host, load, cache, order, and network, violating independence; $p$ may change by context. The calculation is conditional intuition, not a stability certificate.

### Answer 3

Preserve initial logs, subject, account, time, order, seed, environment, and retry result. Run the failing prefix `test_create_user` then victim, reverse it, run each alone, allocate a fresh account, inject a fixed clock, and compare fresh versus reused processes. Inspect whether the first test leaves user or session state and whether wall-clock boundaries affect the oracle. Likely repairs are unique per-test accounts, complete setup and idempotent teardown, and an injected clock with explicit time cases. Replace retry-to-green with an unstable result until the original signature and varied order/time cases pass.

### Answer 4

Permit quarantine only through a test and risk owner with an issue, recorded signature, exact test scope, rationale, lost claim, compensating check, entry date, short expiry, and maximum renewals. Define critical claims—such as payment integrity or destructive migration safety—as non-quarantinable unless an approved trustworthy replacement exists. Continue every quarantined test in a visible lane, store all attempts, and show its claim as waived or incomplete rather than pass. Notify before expiry and block silent renewal. Exit requires a reviewed repair, replay of the original failure, relevant order/seed/load/platform variation, and restored blocking status; obsolete tests require an explicit deletion rationale and replacement analysis.

### Answer 5

Recover attempt-level history before and after: initial outcomes, every retry, subject, environment, failure signature, compute, latency, quarantine, and downstream escapes. Recalculate fail-pass transitions and variable logical runs rather than final red jobs. Run a shadow policy with retries disabled or non-erasing on a stratified sample, seed known flaky fixtures, and compare detection. Measure candidate delay, wasted attempts, diagnosis time, ignored real regressions, and changes in tests or infrastructure. Segment by test and runner to exclude population shifts. Reliability improved only if contradictory outcomes and relevant escapes declined under comparable observation, not merely if the UI selected the final pass.
