---
module_id: SDRE-011
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 11
title: Continuous Integration as a Working Practice
status: complete
last_verified: 2026-09-06
---

# Continuous Integration as a Working Practice

## One-Page Review

### Governing question

How does a team make integration a frequent, low-risk feedback activity instead of a delayed event that accumulates incompatible work?

### Essential definitions

- **continuous integration (CI)** is the team practice of integrating small changes into a shared mainline at least daily and verifying each integration automatically;
- the **mainline** is the shared authoritative line of development;
- an **integration** combines a change with the current shared state and verifies their combined behavior;
- a **change batch** is the coherent set of edits admitted together;
- the **commit stage** is the fast build-and-test gate that gives developers actionable feedback on each mainline change;
- **integration latency** is time from a locally testable change to its verified presence on mainline;
- **feedback latency** is time from an integration attempt to a result the responsible people can act on;
- a **broken mainline** is shared state that fails its defined health contract;
- **work in progress** is unfinished change not yet integrated and validated;
- **flakiness** is nondeterministic test outcome under materially equivalent inputs and environment;
- **revertability** is the ability to remove or disable a change quickly without entangling unrelated work.

### Central model, mechanism, or theorem

CI is a socio-technical feedback loop:

`small change → local check → integrate → authoritative check → repair or continue`.

If changes arrive at average rate $\lambda$ and remain unintegrated for average time $T$, Little's-law reasoning gives average integration work in progress $L=\lambda T$ under stable-flow assumptions. Shortening $T$ reduces hidden inventory. For a batch of $k$ independently developed changes, there are $k(k-1)/2$ possible change pairs; this is an exposure count, not a probability of conflict.

### Critical invariants

- one shared mainline is the authoritative combined state;
- every mainline change triggers an automated, reproducible check;
- developers integrate at least daily, preferably in smaller coherent batches;
- mainline health is visible and has an explicit contract;
- a failure has a responsible responder and blocks unrelated forward change;
- repair or revert is prioritized over adding more uncertainty;
- tests are fast enough to shape behavior and reliable enough to trust;
- incomplete behavior is hidden safely by design, not isolated indefinitely;
- canonical build artifacts flow downstream without environment rebuilds;
- CI service availability, test success, deployability, and release approval remain distinct.

### Common failures

Common failures include calling any automated job “CI,” validating only feature branches, merging large batches weekly, tolerating a red mainline, adding retries around flaky tests, requiring every slow test before any feedback, allowing bypasses without evidence, depending on one specialist to repair builds, sharing mutable test state, rebuilding later environments, measuring job count instead of latency, and confusing frequent integration with continuous deployment.

### Compact example

Four developers each merge one small mainline change during a day. Every merge runs a five-minute commit stage. The third change fails; its author and a rotating build steward diagnose it immediately and revert within seven minutes. No fourth change lands while mainline is red. The team later adds the missed boundary test. Automation enabled the loop, but shared priority, small batches, clear ownership, and fast repair made it CI.

### Connections

[SDRE-010](010-designing-an-auditable-build-pipeline.md) designed the guarded evidence pipeline. [SDRE-012](../ROADMAP.md) next examines trunk-based development, while [SDRE-013](../ROADMAP.md) compares branching strategies and integration delay.

## Governing Question

Software changes interact in the shared system, not only in each developer's workspace. When integration is delayed, each person reasons against an increasingly obsolete state. Conflicts, interface mismatches, migration assumptions, and behavioral regressions accumulate in hidden batches. The eventual integration event must separate many simultaneous causes.

Continuous integration changes the economics by making integration ordinary and frequent. Small changes meet current mainline, an automated check supplies rapid evidence, and failures are repaired while context is fresh. A CI server is useful machinery, but installing one does not create the practice. The team must organize work, ownership, testing, and priorities around the feedback loop.

## Why This Matters

Martin Fowler's current treatment defines CI as team members merging to a shared codebase at least daily, with each integration verified by an automated build including tests [1]. The 2024 revision emphasizes mainline, small work increments, immediate repair, fast builds, visibility, and safely hidden work in progress. DORA's current capability guidance likewise describes regular mainline integration, per-commit automated builds and tests, short feedback, and priority repair of broken builds [2].

These sources describe a working system, not a vendor category. A repository can run thousands of branch jobs while developers integrate only monthly. Conversely, a small team can practice CI with modest automation if every mainline change is integrated and verified frequently. The decisive properties are batch size, feedback time, shared-state health, and response behavior.

CI is foundational for continuous delivery because downstream confidence depends on a continuously validated candidate. It does not imply deployment or release. A mainline build may be deployable while business, safety, regulatory, or rollout policy decides when users receive it.

## Prerequisites and Retrieval

Retrieve version control, commit, branch, merge, mainline, change set, build, dependency lock, artifact, automated test, regression, deterministic input, failure signal, queue, work in progress, latency, throughput, rollback, revert, feature flag, branch by abstraction, observability, ownership, service-level objective, and release decision.

From SDRE-001 through SDRE-010 retrieve immutable source identity, locked inputs, reproducible-build limits, caching, artifact repositories, release identity, provenance, SBOMs, signing, guarded pipeline transitions, and audit evidence. This chapter owns the team feedback practice. STQE owns deep test strategy; SEME owns broader lifecycle choice; SDRE-012 and SDRE-013 own detailed source-branching patterns.

## Learning Objectives

After completing this module, you should be able to:

1. define CI as a working practice rather than a product feature;
2. explain why small frequent integrations shorten discovery and diagnosis;
3. define a mainline health contract and a fast commit stage;
4. distinguish pre-merge checking from post-integration verification;
5. organize repair ownership when shared state breaks;
6. keep unfinished behavior safe without long-lived isolation;
7. manage slow, flaky, stateful, and environment-sensitive checks;
8. preserve canonical artifacts for downstream delivery;
9. select measures that reveal integration and feedback delay;
10. diagnose workflows that automate builds but do not achieve CI.

## Core Exposition

**Define the unit of integration.** A useful change batch is coherent, reviewable, testable, and reversible. Small does not mean one arbitrary line or one commit at any cost. It means the batch introduces one bounded intent and avoids coupling its release to weeks of unfinished work. Refactoring, compatibility layers, feature flags, and incremental migrations let a large outcome arrive through safe slices.

Frequent integration exposes assumptions while few variables changed. If a five-file change breaks one test, the search space is narrower than after fifty unrelated changes. Small batches also reduce time between creating an incorrect assumption and receiving contradictory evidence. They do not guarantee fewer defects; they make many defects cheaper to localize and reverse.

**Make mainline authoritative.** CI requires a shared state that represents the team's latest integrated work. Developers update from it, submit changes to it, and treat its health as a collective constraint. A branch job answers whether one proposed combination passes. Only a check on the resulting mainline revision answers whether the authoritative combined state passed.

Pre-merge queues can serialize proposed changes against a recent base and reduce avoidable breakage. They must account for mainline movement: test the exact merge result or revalidate after admission. Passing a stale branch commit and later merging a different result is not verified integration.

**Specify mainline health.** “Green” must have a contract: source resolves; build completes from declared inputs; fast deterministic tests pass; required static checks and policy gates pass; the canonical artifact and evidence are produced; and known quarantine rules are explicit. The contract varies by system risk, but it must be written, observable, and owned.

A passing commit stage is bounded evidence. It does not prove all behavior correct, production available, security complete, or release authorized. Longer performance, resilience, compatibility, and exploratory checks may run later. Their findings must feed back into mainline repair and future commit-stage design.

**Optimize time to actionable feedback.** Total feedback time includes queue wait, environment provisioning, dependency retrieval, build, tests, result publication, and human notification. Parallelizing tests helps only if queueing, setup, or a serial build dominates. Measure the distribution, not only the average, and separate time-to-first-useful-failure from time-to-complete.

Keep the commit stage fast by removing redundant work, using correct caches, selecting tests with known risk limits, parallelizing independent work, and improving architecture. Do not obtain speed by silently dropping the only check for a critical invariant. Put slower checks in later stages and make their ownership and response explicit.

**Stop the line on failure.** When mainline violates its health contract, the next priority is restore it. The responsible change author should lead because their context is fresh, with a rotating steward or whole-team support to prevent abandonment. Choose the fastest safe path: repair immediately when obvious and bounded; otherwise revert or disable the change, then diagnose off mainline.

Continuing unrelated merges while red increases uncertainty. New failures become hard to attribute, other developers base work on a known-bad state, and pressure grows to normalize bypasses. A fixed response expectation converts a red signal into a short incident rather than background noise.

**Treat flaky tests as defects.** Blind retry turns a failed observation into whichever result happens to arrive last. Track every attempt, quarantine only with an owner and deadline, and retain an independent stable gate. Diagnose uncontrolled clocks, random seeds, ordering, shared state, asynchronous completion, resource limits, external dependencies, and environment drift.

A quarantined test no longer protects mainline, so record the lost risk coverage. Fix or replace it. Reporting “green after retry” without the initial failure trains the team to distrust all signals.

**Control environments and data.** The commit stage should provision isolated, reproducible-enough environments from versioned definitions. Tests must not depend on mutable shared accounts, order-sensitive databases, or unrestricted public services. Use hermetic substitutes where they preserve the claim, and use controlled integration environments where real protocol behavior matters.

Test data needs stable construction, cleanup, privacy controls, and collision-free ownership. A test that passes only after another test warmed a cache or created a row is an order-dependent distributed program, not a reliable unit of feedback.

**Integrate incomplete work safely.** Frequent mainline integration does not require exposing unfinished behavior. Feature flags separate code integration from user release. Branch by abstraction places a stable interface around an incrementally replaced component. Expand-and-contract data changes support mixed application versions. Each technique adds temporary states that need ownership and removal criteria.

Flags are not permission to merge uncompilable or untested code. Disabled paths still affect build, dependencies, schemas, security surface, and maintenance. Test important flag combinations and avoid permanent forests of interacting toggles.

**Preserve the canonical artifact.** The authoritative CI build should create a uniquely identified artifact from the integrated revision. Downstream stages verify and promote those bytes. Rebuilding for testing, staging, and production disconnects commit-stage evidence from the released subject. Environment configuration can vary under deployment policy without changing application artifact identity.

**Create a team operating agreement.** State integration frequency, required local checks, merge mechanism, commit-stage target, red-build response, revert authority, flaky-test handling, ownership rotation, exception path, and communication channel. Ensure every contributor can run relevant checks and diagnose common failures. A process dependent on one build expert is not resilient.

**Measure flow and learning.** Useful measures include integration latency, change batch size, commit-stage queue and execution percentiles, time to first actionable result, red-mainline duration, mean time to restore the build, revert rate, flaky-test incidence, and percentage of mainline changes producing a canonical artifact. Segment measures by repository and change class.

Do not reward raw commit count or punish all failures. That encourages meaningless splitting and hidden testing. The goal is rapid, trustworthy learning and healthy shared state. Review trends with qualitative incident evidence.

## Definitions and Notation

Let $\lambda$ be the average rate of locally ready changes entering the unintegrated-work queue, $T$ their average integration latency, and $L$ the average number waiting or being integrated. Under stable arrival and completion rates and a consistent boundary, Little's law gives

$$
L=\lambda T.
$$

This is a queueing identity over long-run averages, not proof that every change takes $T$ or that halving branch lifetime alone halves defects.

For a batch containing $k$ independently developed changes, the number of unordered change pairs is

$$
P(k)=\binom{k}{2}=\frac{k(k-1)}{2}.
$$

$P(k)$ counts possible pairwise interactions: $P(4)=6$ and $P(10)=45$. It is not a conflict forecast because changes differ in dependency and overlap.

Define feedback latency for integration $i$ as

$$
F_i=t_{actionable,i}-t_{submit,i}.
$$

Record queue and execution components separately so a faster test suite does not conceal a saturated runner pool.

## Mechanisms, Invariants, or Proof Structure

**Fresh-base invariant.** The authoritative check must evaluate the exact mainline result admitted. A branch check against base $b_1$ cannot justify a merge result based on later $b_2$ unless equivalence is established or the result is rechecked.

**Health invariant.** Each accepted mainline revision has a completed health decision under the commit-stage policy effective for that revision. A later discovery may change current health, but history must retain what was known and which response followed.

**Repair invariant.** Once mainline is known red, no unrelated forward changes are admitted until a repair, revert, or authorized containment restores the health contract. Exceptions must be explicit and auditable.

**Feedback argument.** Smaller, more frequent batches usually reduce the number of recently changed causes examined after a failure and reduce elapsed time since the author formed the relevant assumptions. This supports faster diagnosis; it is not a theorem that small changes are correct.

**Executable workflow model.** The model checks one operating agreement. It does not invoke version control, compile software, run tests, or estimate real defect probability.

<!-- bijux-verify: {"id":"evaluate-ci-working-agreement","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"integrations=4\nmax_batch=2\nbroken_detected_at=c3\nunrelated_after_break=0\nfeedback_minutes=5\nmainline_green=True\nhidden_work_rejected=True\n","stderr":""}} -->
```python
changes = [
    {"id": "c1", "batch": 2, "minutes": 4, "result": "pass", "unfinished_visible": False},
    {"id": "c2", "batch": 1, "minutes": 5, "result": "pass", "unfinished_visible": False},
    {"id": "c3", "batch": 1, "minutes": 5, "result": "fail", "unfinished_visible": False},
    {"id": "revert-c3", "batch": 1, "minutes": 3, "result": "pass", "unfinished_visible": False},
]

green = True
broken_at = None
unrelated_after_break = 0
for change in changes:
    if not green and change["id"] != "revert-c3":
        unrelated_after_break += 1
    green = change["result"] == "pass"
    if not green and broken_at is None:
        broken_at = change["id"]

print(f"integrations={len(changes)}")
print(f"max_batch={max(change['batch'] for change in changes)}")
print(f"broken_detected_at={broken_at}")
print(f"unrelated_after_break={unrelated_after_break}")
print(f"feedback_minutes={changes[2]['minutes']}")
print(f"mainline_green={green}")
print(f"hidden_work_rejected={not any(change['unfinished_visible'] for change in changes)}")
```

## Alternatives and Trade-Offs

**Post-merge versus pre-merge verification.** Post-merge checks minimize admission delay but briefly expose broken mainline. A merge queue can check the exact candidate before admission but adds queueing and must handle a moving base. Many teams use both fast pre-merge evidence and an authoritative post-merge check.

**Comprehensive versus fast commit stage.** More checks may catch more classes before integration but increase feedback and queue time. A layered pipeline runs the fastest high-signal checks first and later checks for slower risks, without pretending later failures are harmless.

**Repair versus revert.** Direct repair is efficient when cause and fix are clear. Revert restores shared state quickly when diagnosis is uncertain. Revertability requires small changes, compatible migrations, and no irreversible side effects.

**Feature flags versus branch isolation.** Flags permit code integration and delayed exposure but add runtime combinations and cleanup work. Branch isolation avoids dormant code in mainline but delays real integration. Use bounded flags with owners and expiry when they reduce overall risk.

**Central build team versus product ownership.** Specialists can improve infrastructure, but product teams must own their build and tests. A platform team should provide paved capabilities and evidence, not become a queue for every repair.

## Failure Modes and Misconceptions

- **“We bought a CI service, so we practice CI.”** Tooling cannot supply integration frequency or repair discipline.
- **“Branch tests are integration.”** They may omit other concurrent changes and the admitted result.
- **“A daily scheduled build is enough.”** Every admitted mainline change needs feedback.
- **“Large batches use compute efficiently.”** They enlarge diagnosis and reversal scope.
- **“Red is normal during busy periods.”** Normalized failure destroys the shared-state contract.
- **“Retry fixes flaky tests.”** It hides nondeterminism and loses risk coverage.
- **“All tests belong in the first gate.”** Layer checks by signal, risk, and latency.
- **“Fast means skip safety.”** Improve architecture and execution; preserve critical claims.
- **“Feature flags make unfinished code free.”** Flags add states, security surface, and cleanup debt.
- **“More commits means better CI.”** Measure coherent batch and feedback, not vanity counts.
- **“CI means deploy every commit.”** Integration, delivery, deployment, and release are distinct.
- **“Only the change author owns a break.”** The author leads; mainline health belongs to the team.
- **“The build expert will fix it.”** Specialist dependence creates queue and resilience risk.
- **“Green proves deployability.”** It proves only the declared gate passed for the subject.
- **“Rebuild downstream for confidence.”** Promote the canonical artifact and add evidence around it.

## Worked Examples

### Example 1

**Situation.** Five developers keep branches for two weeks while every branch job passes. **Reasoning.** Each job validates a private combination; none includes all peers. The eventual merge combines a large, stale batch, so diagnosis spans many assumptions. **Conclusion.** Automated branch testing without frequent mainline integration is not CI.

### Example 2

**Situation.** At four ready changes per day and average integration latency of five days, estimate hidden work. **Reasoning.** Under stable boundaries, $L=\lambda T=4\times5=20$ changes. Reducing latency to one day yields about four. **Conclusion.** Shorter integration delay reduces unvalidated inventory; it does not alone predict defects.

### Example 3

**Situation.** A branch passed against `b1`, but mainline advanced to `b2` before merge. **Reasoning.** The admitted merge result contains interactions absent from the check. Rebase or construct the exact queued merge result and rerun required checks. **Conclusion.** Evidence must bind the revision actually admitted.

### Example 4

**Situation.** Change `c3` breaks the commit stage and the fix may take an hour. **Reasoning.** Stop unrelated admission. If a safe repair is not immediate, revert `c3`, verify restored health, then diagnose separately. Preserve the failed result and response. **Conclusion.** Restore mainline first when the repair horizon is uncertain.

### Example 5

**Situation.** A test fails one run in fifty and passes when retried. **Reasoning.** Record all attempts, quarantine with an owner only if a stable gate remains, then control seed, time, ordering, shared state, and resources. “Pass on retry” is not clean evidence. **Conclusion.** Flakiness is a product and feedback-system defect.

### Example 6

**Situation.** The suite takes 35 minutes: 20 queueing, 5 setup, 10 tests. **Reasoning.** Halving tests saves only five minutes; capacity and provisioning dominate. Measure each component and time to first failure. **Conclusion.** Optimize end-to-end actionable feedback, not test runtime alone.

### Example 7

**Situation.** A six-month feature cannot be shown to users yet. **Reasoning.** Integrate compatible slices behind an owned flag, test enabled and disabled states, protect schema compatibility, and set removal criteria. **Conclusion.** Exposure can be delayed without delaying code integration.

### Example 8

**Situation.** CI builds artifact `a1`; staging rebuilds `a2` from the same commit. **Reasoning.** Test evidence for `a1` does not bind `a2`; environment and dependency drift may differ. Promote `a1` and inject governed configuration at deployment. **Conclusion.** CI should produce the canonical downstream artifact.

### Example 9

**Situation.** Security scanning takes four hours and sometimes finds critical defects. **Reasoning.** Keep a fast commit-stage subset for high-signal rules, run the full scan later, block promotion on its result, and feed recurring classes into faster checks. **Conclusion.** Layer feedback without erasing slow-test authority.

### Example 10

**Situation.** Management rewards number of merges per developer. **Reasoning.** People split changes artificially or avoid repairs that reduce their count. Measure integration latency, batch coherence, feedback, and red duration at team level, then review context. **Conclusion.** Incentives must support learning and shared health rather than output theater.

## Cross-Program Connections

- Software Engineering Methods & Evolution owns lifecycle fit and change evolution; CI supplies frequent empirical feedback inside those methods.
- Software Design & Domain Modeling enables coherent slices and stable seams that can integrate safely.
- Testing & Quality Engineering owns test adequacy, oracles, selection, and flakiness analysis; CI owns when that evidence enters the shared flow.
- Software Architecture owns deployability, modularity, and change coupling that bound commit-stage speed.
- Platform Engineering owns shared runners, queues, isolation, caching, and developer experience for CI execution.
- Security Engineering owns threat-informed gates and credential boundaries; CI integrates a bounded subset into fast feedback.
- API & Service Engineering owns compatibility and contract checks that allow independently changing services to integrate continuously.

## References

1. Martin Fowler, [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html), revised 18 January 2024. Retrieved 2026-09-06.
2. DORA, [Continuous Integration](https://dora.dev/capabilities/continuous-integration/), current capability guidance. Retrieved 2026-09-06.
3. Paul M. Duvall, Steve Matyas, and Andrew Glover, *Continuous Integration: Improving Software Quality and Reducing Risk*, Addison-Wesley, 2007.
4. Jez Humble and David Farley, *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*, Addison-Wesley, 2010.
5. Kent Beck with Cynthia Andres, *Extreme Programming Explained: Embrace Change*, 2nd edition, Addison-Wesley, 2004.
6. Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate: The Science of Lean Software and DevOps*, IT Revolution, 2018.

## Exercises

### Exercise 1

Define continuous integration and distinguish it from build automation and continuous deployment.

### Exercise 2

A team completes six locally ready changes per day, and changes wait an average of three working days before verified mainline integration. Estimate average unintegrated work under stable-flow assumptions, then state two limitations of the estimate.

### Exercise 3

A commit stage has p50 7 minutes and p95 48 minutes. At p95, queueing is 30 minutes, setup 8, build 4, and tests 6. Diagnose priorities and specify evidence needed before changing the test suite.

### Exercise 4

Design a working agreement for a 12-person team whose mainline is red 15% of working time and whose flaky suite is routinely retried.

### Exercise 5

A safety-relevant product has a 10-minute commit stage and a six-hour hardware qualification suite. Design a CI feedback architecture that remains fast without claiming unsafe confidence.

## Answers to the Exercises

### Answer 1

CI is the team practice of integrating small changes into a shared mainline at least daily and automatically verifying each integrated result, with rapid repair when shared health breaks. Build automation supplies repeatable machinery but can run on isolated branches or schedules without frequent integration. Continuous deployment automatically moves accepted changes into production; CI stops at integrated, verified shared state and canonical artifacts. Release to users remains a separate policy decision.

### Answer 2

Little's law gives $L=\lambda T=6\times3=18$ locally ready changes waiting or being integrated on average. The result requires stable arrival and completion rates and a consistent queue boundary. It does not describe the distribution, distinguish batch sizes, predict conflicts or defects, or prove that reducing delay alone improves quality. A surge, blocked release train, or changing definition of “ready” invalidates the simple interpretation.

### Answer 3

The tail is dominated by 30 minutes of queueing, then eight minutes of setup; tests contribute only six. First segment the distribution by time, change class, runner pool, and cache state; measure utilization, arrival bursts, scheduling fairness, provisioning failures, cache correctness, and time to first failure. Increase or reshape capacity and reduce setup before deleting tests. Confirm whether rare tests dominate actionable failures despite short runtime. Optimize the p95 end-to-end path and preserve risk coverage.

### Answer 4

Adopt one authoritative mainline, exact-result pre-merge or immediate post-merge checks, and a written health contract. Every change triggers the commit stage. When red, stop unrelated admission; the author leads while a rotating steward assists; repair quickly or revert. Record red start, cause, response, and restoration. Flaky failures retain all attempts, receive owners and deadlines, and may be quarantined only with visible lost coverage and a stable replacement gate. Track integration latency, p50/p95 feedback, red duration, restore time, and flake incidence at team level. Grant all members tools and authority to revert safely.

### Answer 5

Run deterministic high-signal unit, static, interface, simulation, and safety-invariant checks in the 10-minute commit stage on every integrated revision. Produce one digest-addressed candidate. Queue the six-hour qualification against that exact candidate with controlled hardware identity, calibration, inputs, and evidence. Do not promote or release until qualification passes; superseded candidates may be canceled under explicit policy. Feed recurring hardware failures into faster models without claiming those substitutes prove physical behavior. Keep mainline feedback fast while truthfully labeling the candidate “commit-stage verified, qualification pending.”
