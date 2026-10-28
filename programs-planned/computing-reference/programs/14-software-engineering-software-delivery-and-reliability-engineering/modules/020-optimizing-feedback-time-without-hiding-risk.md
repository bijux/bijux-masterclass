---
module_id: SDRE-020
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 20
title: Optimizing Feedback Time Without Hiding Risk
status: complete
last_verified: 2026-09-06
---

# Optimizing Feedback Time Without Hiding Risk

## One-Page Review

### Governing question

How should a delivery system reduce the time from a candidate change to useful, complete evidence while preserving the risk claims required for admission?

### Essential definitions

- **feedback time** is elapsed time from a declared start event to delivery of specified evidence to a consumer;
- **time to first signal** ends at the first actionable result, while **time to decision** ends when every blocking claim has a valid outcome;
- a **critical path** is the longest dependency path that determines completion time;
- **queue time** is delay before work receives execution capacity;
- **setup time** prepares source, dependencies, environment, and tools;
- **test selection** chooses a subset believed relevant to a candidate; **prioritization** orders checks without necessarily omitting any;
- **detection yield** is observed useful failure discovery per unit of time under a stated population;
- a **soundness envelope** states the assumptions within which omitted checks are claimed irrelevant;
- **risk-based validation** maps change attributes and impact to required evidence;
- a **blocking check** must pass for admission; a **deferred check** reports later and cannot silently support that decision;
- **fail-fast** stops work after decisive failure while preserving the failed evidence;
- a **cache hit** reuses output identified by keys or content; it is not proof that the cached output is correct;
- **tail latency** describes slow outcomes such as the 95th or 99th percentile, not only the average.

### Central model, mechanism, or theorem

For sequential independent checks, let check $i$ take deterministic time $d_i$ and reveal a decisive failure with probability $p_i$ conditional on being reached. With stop-on-failure, expected time to a decision is

$$
E[T]=\sum_{i=1}^{n}d_i\prod_{k<i}(1-p_k).
$$

A pairwise interchange shows that check $a$ should precede $b$ when $p_a/d_a \ge p_b/d_b$. This ordering can improve expected time to failure without omitting checks. Its assumptions—stable conditional probabilities, deterministic duration, independence from order, equal failure value, and safe stopping—rarely hold exactly, so production ordering also considers severity, dependencies, diagnostic quality, and tail behavior.

### Critical invariants

- define start, end, subject, consumer, and evidence before measuring feedback;
- optimize first-signal and complete blocking-decision time separately;
- never relabel omitted, deferred, sampled, cancelled, unavailable, or flaky evidence as pass;
- preserve every risk claim required by the gate;
- prioritize before selecting away checks;
- give every selection rule a versioned soundness envelope and full-suite audit;
- bind cached and incremental results to complete declared inputs and tool identities;
- measure queue, setup, execution, reporting, and human response independently;
- optimize the critical path and tail, not total work or mean alone;
- shard by measured duration and resource need rather than check count;
- cancel only work made irrelevant by an already-decisive result;
- monitor detection yield, escapes, invalidations, and skipped claims alongside speed.

### Common failures

Common failures include showing only time to first green check, moving slow blockers after merge without changing policy, selecting tests from incomplete dependencies, trusting stale caches, running everything in parallel while queue time grows, balancing shards by test count, retrying flaky checks until green, cancelling diagnostics, optimizing the mean while the 99th percentile stalls, using historical failure frequency as certainty, letting small changes bypass high-impact checks, and celebrating a faster dashboard after evidence disappeared.

### Compact example

Four required sequential checks take 2, 4, 8, and 20 minutes and historically expose conditional failures with probabilities 0.30, 0.20, 0.25, and 0.15. Ordering by $p_i/d_i$ gives 2, 4, 8, 20 and an illustrative expected stop-on-failure time of $17.68$ minutes, while a passing candidate still executes all 34 minutes. No coverage was removed. If the estimates drift or the 20-minute check detects catastrophic defects, severity and policy may change the order or require parallel start.

### Connections

[SDRE-014](014-change-detection-and-selective-execution.md) defines safe change-based selection, [SDRE-015](015-parallelizing-ci-workloads.md) owns parallel scheduling mechanics, [SDRE-017](017-quality-gates.md) owns admission semantics, and [SDRE-018](018-handling-flaky-ci.md) prevents retries from manufacturing green. [SDRE-021](../ROADMAP.md) next distinguishes continuous delivery from continuous deployment.

## Governing Question

Fast CI shortens the interval during which a developer builds further work on a defect and reduces the number of competing changes that complicate diagnosis. But “faster” is easy to counterfeit: skip a test, defer a security scan, display the first pass, ignore queueing, or retry a failure until it disappears. The number improves while the decision becomes weaker.

The governing question therefore has two parts. Which elapsed interval and evidence consumer are we optimizing? Which risk claims must remain satisfied at the endpoint? A valid improvement reduces delay while preserving or explicitly renegotiating those claims.

## Why This Matters

Continuous integration depends on feedback arriving while the candidate and its intent remain cognitively and technically close. Fowler's account of CI emphasizes rapid feedback and describes a fast commit build followed by slower staged testing rather than one undifferentiated suite [1]. Google SRE guidance likewise recommends prompt notification when a change breaks a project and relates test coverage uncertainty to release cadence [2]. These sources establish the value of short loops, not permission to hide incomplete evidence.

Some checks are naturally small and isolated; others cross databases, networks, processes, or packaged-system boundaries. Google's published test-size model uses observable resource and time constraints and notes that isolation enables parallel execution [3]. The durable design is a portfolio of evidence with explicit timing and authority: fast checks answer narrow claims early, while slower checks complete the claims the gate actually requires.

Test prioritization has a research basis. Elbaum, Malishevsky, and Rothermel define prioritization as ordering cases to increase a suite's rate of fault detection and report empirical studies across techniques and programs [4]. Their results support measurement and experimentation, not a universal ordering algorithm. Historical data can be biased by prior selection, changing code, flaky failures, and sparse severe defects.

## Prerequisites and Retrieval

Retrieve elapsed time, percentile, probability, conditional probability, expectation, dependency graph, critical path, throughput, utilization, queue, cache, hash, incremental computation, partition, false negative, test oracle, risk, severity, confidence, sampling, admission, cancellation, artifact, and revision.

From SDRE-011 retrieve candidate-triggered CI. From SDRE-013 retrieve integration delay and small changes. From SDRE-014 retrieve change detection and selective execution. From SDRE-015 retrieve dependencies, shards, capacity, and critical paths. From SDRE-016 and SDRE-017 retrieve exact-candidate evidence and gate states. From SDRE-018 retrieve attempt preservation and flake semantics; from SDRE-019 retrieve trust-separated runners and caches.

## Learning Objectives

After completing this module, you should be able to:

1. define feedback intervals with exact start, end, subject, evidence, and consumer;
2. decompose latency into queue, setup, execution, reporting, and response;
3. distinguish first-signal latency from complete-decision latency;
4. derive the sequential stop-on-failure expectation and its ordering condition;
5. optimize a dependency graph's critical path and tail behavior;
6. use caching, incrementality, sharding, and selection without overstating evidence;
7. design risk-based lanes whose deferred checks have honest authority;
8. preserve diagnostics under failure, cancellation, retry, and infrastructure loss;
9. evaluate changes using speed, detection, escape, and cost measures together;
10. recognize metric gaming and reverse optimizations that reduced assurance.

## Core Exposition

**Name the feedback contract.** “CI takes eight minutes” is incomplete. Does timing begin when a developer saves, pushes, opens review, enters a merge queue, or receives a runner? Does it end at the first failure, first green check, all required checks, merge admission, or human acknowledgment? Is the subject the head revision, synthetic merge candidate, built artifact, or deployed version?

Define an interval as `(start event, end event, subject, evidence class, consumer)`. Useful families include local-edit feedback, presubmit first signal, presubmit blocking decision, merge-queue decision, post-merge regression discovery, and production observation. Do not combine them into one average.

First-signal time answers “how soon might I learn something actionable?” Complete-decision time answers “when may policy admit this exact candidate?” A fast lint result is valuable but cannot stand in for a missing migration or compatibility check.

**Decompose the delay.** For one check, observed latency can be written

$$
T=T_q+T_s+T_x+T_r,
$$

where $T_q$ is queueing, $T_s$ setup, $T_x$ execution, and $T_r$ result processing and delivery. A human response interval can be measured separately. Each component has different remedies.

Queue time calls for capacity, admission control, fair scheduling, or demand reduction. Setup may improve through smaller images, local mirrors, prefetching, or reusable immutable layers. Execution may improve through algorithmic work, smaller fixtures, better test boundaries, incrementality, parallelism, or faster hardware. Reporting improves through streaming, bounded artifacts, and prompt notification.

Segment by repository area, change class, runner pool, check, cache state, and time. A global mean can hide one team waiting an hour or a p99 queue incident. Report median for typical experience and upper percentiles for reliability; preserve sample counts and censored or cancelled runs.

**Reduce demand at the source.** Small, coherent changes usually touch fewer dependencies, are easier to review, and localize failures. Google's engineering practices recommend self-contained small changes and cite quicker review, easier reasoning, fewer conflicts, and simpler rollback [5]. This is qualitative guidance, not a line-count law.

Give developers cheap local or pre-push checks identical in logic and version to CI where practical. Early local feedback saves shared queue demand, but CI still supplies controlled, recorded evidence. Avoid requiring every developer to reproduce a large hosted environment merely to discover formatting or type errors.

Remove redundant work only after identifying the repeated claim. Build once per exact subject when downstream checks can safely share an immutable artifact. Combine repeated dependency resolution under complete keys. Do not fuse checks whose isolation or distinct environments are part of the evidence.

**Order for information.** Place cheap, high-yield, high-diagnostic checks early when dependencies permit. Compilation, schema validation, static checks, and narrow affected tests often provide fast actionable failures. A deterministic failure with a clear owner is more useful early than a noisy signal requiring an hour of triage.

The $p_i/d_i$ rule formalizes one narrow case. Compare two checks. Running $a$ then $b$ has expected time $d_a+(1-p_a)d_b$; running $b$ then $a$ has $d_b+(1-p_b)d_a$. The first is no slower when $p_a d_b\ge p_b d_a$, equivalent to $p_a/d_a\ge p_b/d_b$ for positive durations.

Production order changes when failures have unequal severity, checks share setup, outcomes correlate, durations vary, one result invalidates another, or all results must finish before decision. A catastrophic five-minute safety check may start immediately despite low historical frequency. Prioritization reorders evidence; it does not erase it.

**Optimize the dependency graph.** In a parallel workflow, completion is controlled by the longest dependent path, not the sum of all job durations. Speeding a job off the critical path may reduce compute cost but not decision latency. Draw or derive the graph using measured queue and execution distributions, then target the path and recurring stragglers.

Start independent required checks concurrently within safe capacity. Pipeline artifact creation and consumers only when consumers can validate complete immutable outputs; do not read partially written state. Move reusable setup into trusted immutable images or content-addressed layers while preserving input identity.

Unlimited parallel launch can make every candidate slower by saturating runners, databases, registries, networks, or external quotas. Optimize end-to-end latency at expected load and failure modes. Reserve capacity for short presubmit work, prevent giant jobs from starvation, and define priority without allowing low-priority correctness evidence to disappear indefinitely.

**Balance shards by work and variance.** Ten shards with equal test counts can have radically unequal duration. Use recent robust duration estimates, resource class, setup affinity, and isolation constraints. Rebalance periodically and limit the effect of one pathological test.

Static partitioning is predictable but drifts. Dynamic work stealing reduces tail idle time but requires stable test identity, isolation, and result aggregation. Speculative duplicate execution may reduce rare stragglers at additional cost; count one logical result and preserve both attempts for diagnosis.

A shard failure must identify exact contained tests and completed versus unexecuted work. “Shard 7 failed” is not sufficient evidence for selective retry. Rerun only invalid or interrupted work when policy allows, and never overwrite the first failure.

**Cache with complete identity.** A cache saves computation only if its key or content identity captures every relevant input: source, dependency locks, toolchain, flags, platform, environment, and policy-defined configuration. An incomplete key yields a fast wrong answer. Bazel's current remote-cache documentation, for example, warns that inputs modified during a build can cause invalid results to be uploaded [6]; the general lesson is to control inputs and upload authority.

Separate caches by trust domain as established in SDRE-019. Verify downloaded content, record hit and miss, and provide a clean-build sampling lane. Compare clean and cached results to detect unsound keys. Cache service unavailability should degrade under explicit policy—perhaps recompute—not silently accept missing work.

Incremental builds and tests have the same obligation. A dependency graph establishes what may be reused only within its declared model. Generated files, reflection, runtime discovery, environment reads, and hidden network dependencies can violate that model. Audit clean-versus-incremental equivalence on representative and adversarial changes.

**Select checks under a soundness envelope.** Test selection maps a change to a subset. It is more aggressive than prioritization because selected-away checks produce no evidence for that candidate. The selection rule must state what dependencies it observes, what kinds of changes it cannot model, which checks are never selectable, and what happens on ambiguity.

Default to broader execution when mappings are missing, parsers fail, generated or build logic changes, shared schemas or interfaces change, dependency graphs are stale, or policy cannot classify the subject. Run periodic full suites, random holdout checks, and clean builds; compare defects found only outside selection. Version the selector and bind its decision to the candidate.

Historical “this test never fails for these files” is correlation, not proof of irrelevance. Tests that rarely fail may protect severe invariants. Maintain mandatory suites for authentication, authorization, money, data migration, compatibility, signing, and other high-impact boundaries as risk requires.

**Build explicit feedback lanes.** A fast presubmit lane can include deterministic compile, type, lint, schema, and affected-test evidence. A complete admission lane adds every claim required before merge or release. Post-merge, nightly, and production lanes find broader or environment-specific problems, but their results cannot retroactively make an earlier gate complete.

Deferring a check is a policy decision. State the risk accepted during the gap, blast-radius controls, detection latency, rollback or disablement mechanism, owner, and escalation. A slow check may move after merge only when the organization explicitly accepts that containment model; changing dashboard placement alone is not optimization.

Risk-based validation maps candidate properties to lanes. Changes to comments might avoid expensive behavioral suites when parsers establish non-executable scope. Changes to dependency locks, build rules, security policy, schemas, concurrency, persistence, or deployment should expand evidence. An emergency fix may prioritize speed, but records the waiver and receives follow-up review rather than being labeled ordinary pass.

**Fail fast without losing evidence.** When one blocking check decisively fails, later expensive work may be cancelled. Preserve the failure, logs, subject, environment, and attempt before cancellation. Do not cancel independent diagnostics needed to distinguish product, test, or infrastructure cause.

Cancellation itself consumes time and capacity. Tasks must honor signals, release resources, and report cancelled rather than pass. A new revision may supersede an old candidate, but retain enough evidence to investigate failures that might also affect the new revision.

Flaky retries are not a feedback optimization. They add latency and can select a passing observation. If a retry is used diagnostically, show initial and later outcomes and preserve unstable gate semantics. Repair the source of variability.

**Improve the tests, not just orchestration.** Replace real sleeps with bounded condition waits. Use narrow fixtures, explicit clocks, deterministic seeds, local controlled dependencies, and independent state. Split a slow multipurpose scenario into focused claims only if their composition still covers the original risk. Move expensive setup to suite scope only when tests cannot corrupt it and isolation remains valid.

Profile test and build code. An accidental quadratic fixture, repeated database migration, serial dependency fetch, debug logging flood, or oversized container context can dominate. Performance work on CI code receives tests and review like product performance work.

Some large end-to-end checks remain necessary because narrower doubles do not establish deployment, compatibility, or service interaction. Optimize their environments, start them earlier, and reduce redundant cases rather than pretending unit checks are equivalent.

**Measure information, risk, and cost together.** Track time to first actionable failure, time to all blocking evidence, queue and setup percentiles, critical-path distribution, check detection yield, diagnostic precision, flake transitions, selector fallback, cache correctness audits, cancellation effectiveness, compute, and human wait.

Pair these with escaped defects, rollback or incident linkage, failures found only by deferred or full-suite lanes, and waived claims. A latency improvement is suspect if escapes or unexecuted evidence rise. Because severe escapes are sparse and delayed, retain qualitative review and safety invariants rather than waiting for statistically decisive harm.

Use controlled rollouts for optimizer changes. Shadow a new selector without granting it gate authority, compare old and new schedules on the same candidate population, and stratify by change class. Avoid survivorship bias: cancelled checks and rejected candidates belong in the analysis. Reassess when code ownership, architecture, tests, runner fleet, or workload changes.

## Definitions and Notation

For one check, define $T_q,T_s,T_x,T_r\ge0$ as queue, setup, execution, and reporting time. Total machine feedback latency is

$$
T=T_q+T_s+T_x+T_r.
$$

For a dependency directed acyclic graph $G=(V,E)$, each vertex $v$ has duration $d(v)$. Ignoring resource contention, workflow duration is at least the weighted longest path

$$
L(G)=\max_{P\in Paths(G)}\sum_{v\in P}d(v).
$$

Queueing and limited resources can make observed duration exceed $L(G)$.

For sequential stop-on-failure checks, $d_i>0$ is deterministic duration and $p_i\in[0,1]$ is conditional probability that check $i$ decisively fails given all earlier checks passed. Then

$$
E[T]=\sum_{i=1}^{n}d_i\prod_{k<i}(1-p_k).
$$

For a passing candidate, every required check runs, so elapsed sequential execution remains $\sum_i d_i$. Expected-time improvement does not reduce required evidence.

Let $R(c)$ be risk claims required for candidate $c$ and $E(c)$ claims supported by valid completed evidence. Admission requires

$$
R(c)\subseteq E(c).
$$

Skipped, deferred, unavailable, cancelled, and unstable checks do not enter $E(c)$ unless explicit policy supplies a distinct waiver state rather than pretending they passed.

## Mechanisms, Invariants, or Proof Structure

**Pairwise ordering proof.** For checks $a,b$, order $a,b$ costs $d_a+(1-p_a)d_b$ in expectation; order $b,a$ costs $d_b+(1-p_b)d_a$. Subtracting and rearranging shows $a,b$ is no slower exactly when $p_a d_b\ge p_b d_a$, hence $p_a/d_a\ge p_b/d_b$ for positive durations. Repeated adjacent exchanges yield descending ratio order under the stated assumptions.

**Coverage-preservation invariant.** Prioritization changes when a required check runs, not whether it runs for a passing candidate. Therefore all required evidence remains available at the admission boundary. Selection or deferral requires a separate justification because it changes $E(c)$.

**Critical-path lower bound.** Every vertex on a dependency path must wait for its predecessor. Thus the sum along each path lower-bounds completion, and the maximum path is a lower bound for the workflow. More workers cannot reduce below it without changing durations or dependencies.

**Measurement anti-gaming invariant.** A reported latency distribution includes queued, failed, cancelled, superseded, and infrastructure-lost candidates under declared classifications. Excluding slow unsuccessful observations can improve the metric without improving developer experience.

**Executable scheduling model.** This model verifies the narrow ratio ordering and expected stop-on-failure calculation. It does not estimate any real check's failure probability.

<!-- bijux-verify: {"id":"feedback-ordering-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"order=syntax,schema,unit,integration\nexpected_stop_seconds=17.68\npassing_candidate_seconds=34\nprioritization_omits_checks=False\nsampling_is_complete_evidence=False\ncache_hit_is_validation=False\nrequired_claims_covered=True\n","stderr":""}} -->
```python
checks = [
    {"name": "integration", "seconds": 20, "failure_probability": 0.15},
    {"name": "unit", "seconds": 8, "failure_probability": 0.25},
    {"name": "schema", "seconds": 4, "failure_probability": 0.20},
    {"name": "syntax", "seconds": 2, "failure_probability": 0.30},
]
ordered = sorted(
    checks,
    key=lambda check: check["failure_probability"] / check["seconds"],
    reverse=True,
)
reach = 1.0
expected = 0.0
for check in ordered:
    expected += reach * check["seconds"]
    reach *= 1 - check["failure_probability"]

print("order=" + ",".join(check["name"] for check in ordered))
print(f"expected_stop_seconds={expected:.2f}")
print(f"passing_candidate_seconds={sum(check['seconds'] for check in ordered)}")
print("prioritization_omits_checks=False")
print("sampling_is_complete_evidence=False")
print("cache_hit_is_validation=False")
required_claims = {"build", "schema", "behavior", "integration"}
completed_claims = {"build", "schema", "behavior", "integration"}
print(f"required_claims_covered={required_claims <= completed_claims}")
```

## Alternatives and Trade-Offs

**Prioritization versus selection.** Prioritization preserves a full passing run but may save time only on failures. Selection saves passing time and compute but weakens evidence unless its soundness envelope is valid.

**Parallelism versus capacity stability.** More concurrency shortens independent work at low load. At saturation it increases queueing, contention, and tail latency. Capacity planning and admission are part of CI design.

**Cache reuse versus clean computation.** Reuse reduces setup and execution. Clean runs detect incomplete keys and contamination. Combine verified caches with sampled clean comparisons.

**Static versus dynamic sharding.** Static shards are reproducible and simple but drift. Dynamic scheduling balances tails but complicates identity, replay, and aggregation.

**Fail-fast versus diagnostic completeness.** Early cancellation saves resources after decisive failure. Continuing selected diagnostics can shorten repair. Define which evidence survives each failure class.

**Fast narrow tests versus large system tests.** Narrow tests localize failures and run cheaply. System tests cover real integration boundaries. A portfolio is stronger than pretending one substitutes universally for the other.

**Pre-merge versus post-merge evidence.** Pre-merge blockers prevent known risk from entering. Post-merge checks permit faster integration and realistic environments but accept an exposure window requiring containment and rollback.

**Dedicated capacity versus shared efficiency.** Reserved presubmit runners protect latency but may idle. Shared fleets improve utilization but need priority, fairness, and overload controls.

## Failure Modes and Misconceptions

- **“Fastest check first is optimal.”** failure yield, severity, dependencies, variance, and diagnostic value also matter.
- **“Highest historical failure rate first is optimal.”** duration and biased history matter.
- **“Parallelize everything.”** shared bottlenecks can increase queue and tail latency.
- **“Total CPU time determines feedback.”** the dependency critical path determines ideal completion.
- **“Equal test counts make equal shards.”** test duration and resource demand differ.
- **“Average duration describes experience.”** tails and segments may dominate.
- **“Cache hit means verified.”** incomplete keys can return stale or poisoned output.
- **“Incremental equals clean.”** hidden dependencies can invalidate reuse.
- **“Selection is just prioritization.”** selection omits evidence.
- **“No historical failures means no risk.”** severe defects may be rare or unobserved.
- **“Post-merge checks protect the merge gate.”** they detect after admission.
- **“First green means decision complete.”** other required claims may remain pending.
- **“Cancellation is pass.”** it is an explicit non-execution state.
- **“Retry makes feedback faster.”** it adds latency and may hide contradictory outcomes.
- **“Small change means harmless change.”** a one-line authorization or schema edit can be high impact.
- **“More hardware always fixes CI.”** redundant work, bad graphs, and unstable dependencies remain.
- **“One latency number is enough.”** start, end, population, subject, and evidence must be named.
- **“Faster dashboard proves improvement.”** detection loss and escaped defects must also be checked.

## Worked Examples

### Example 1

**Situation.** A dashboard reports “CI: 4 minutes,” measured from runner start to the first check result. Candidates wait 18 minutes in queue and require 25 minutes for all blockers. **Reasoning.** Define queue-inclusive first-signal and complete-decision intervals. The useful values are 22 and 43 minutes, not four. **Conclusion.** Endpoint definitions can expose hidden delay.

### Example 2

**Situation.** Checks A and B take 3 and 12 minutes and conditionally fail with probabilities 0.15 and 0.30. **Reasoning.** Ratios are $0.15/3=0.05$ and $0.30/12=0.025$, so A precedes B under the narrow model. Expected time is $3+0.85(12)=13.2$ rather than $12+0.70(3)=14.1$ minutes. **Conclusion.** Cheap moderate-yield evidence can beat slower high-frequency evidence.

### Example 3

**Situation.** Eight jobs run in parallel, but every one waits for a 14-minute package build. **Reasoning.** The package build lies on every critical path. Doubling workers for downstream jobs cannot cross the 14-minute lower bound; make the build incremental, faster, or safely reusable. **Conclusion.** Optimize the critical path before off-path work.

### Example 4

**Situation.** Ten shards contain ten tests each; nine finish in two minutes and one in 25. **Reasoning.** Count balance hid one expensive test. Partition by robust measured duration and resource class, isolate the pathological case, and consider dynamic work stealing. **Conclusion.** Tail balance depends on work, not item count.

### Example 5

**Situation.** A dependency cache saves six minutes but keys only on the lockfile, not compiler version or flags. **Reasoning.** A compiler upgrade can restore incompatible objects. Add toolchain, flags, platform, and relevant environment to identity; verify content and run sampled clean comparisons. **Conclusion.** A fast unsound cache is negative feedback quality.

### Example 6

**Situation.** A selector skips database tests for documentation-only changes, but a generated documentation plugin runs schema examples. **Reasoning.** The soundness envelope incorrectly classifies the path as non-executable. Model the generator dependency or fall back to broader checks whenever build, generator, or mapping inputs change. **Conclusion.** File extensions alone do not establish irrelevance.

### Example 7

**Situation.** A team moves a 40-minute migration test after merge and says presubmit is now fast. **Reasoning.** Determine whether migration safety was a blocking claim. If yes, the gate lost evidence. Either optimize or start the check earlier, or explicitly accept post-merge exposure with containment, owner, detection deadline, and rollback. **Conclusion.** Deferral is risk policy, not a free optimization.

### Example 8

**Situation.** A unit failure appears after two minutes, and the system cancels every job including the compiler trace needed to diagnose it. **Reasoning.** Preserve the failure and continue bounded diagnostic producers while cancelling expensive independent system suites. Report every cancellation explicitly. **Conclusion.** Fail-fast should shorten repair as well as conserve compute.

### Example 9

**Situation.** Mean decision time falls from 12 to 9 minutes, while p99 rises from 35 to 90 because peak queues saturate. **Reasoning.** Segment by load and runner pool, inspect queue percentiles, cap concurrency, reserve short-job capacity, and measure fairness. **Conclusion.** Mean improvement can conceal unreliable feedback.

### Example 10

**Situation.** A new selector cuts compute 45% and presubmit time 30%. **Reasoning.** Run it in shadow, execute holdout and periodic full suites, compare failure detection by change class, include rejected and cancelled candidates, and track escaped defects and selector fallbacks. Grant gate authority only within a supported envelope. **Conclusion.** Optimization needs detection evidence, not speed alone.

## Cross-Program Connections

- Algorithm Engineering owns scheduling, graph, partitioning, approximation, and optimization methods.
- Testing & Quality Engineering owns test adequacy, selection evaluation, oracles, prioritization research, and false-negative analysis.
- Data Engineering owns trustworthy duration, failure, selection, and escape datasets plus lineage and bias controls.
- Platform Engineering owns runners, queues, caches, remote execution, capacity, isolation, and result delivery.
- Software Architecture owns dependency boundaries that determine incremental invalidation and test scope.
- Distributed Systems owns queueing, retries, cancellation, stragglers, partial failure, and tail latency.
- Security Engineering owns checks that cannot be selected away casually and cache or artifact trust boundaries.
- Reliability Engineering owns risk acceptance, containment, production observation, rollback, and error-budget consequences.

## References

1. Martin Fowler, [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html), revised article, 2024, fast-build and staged-pipeline guidance.
2. Google, [Testing for Reliability](https://sre.google/sre-book/testing-reliability/), *Site Reliability Engineering*, 2016, feedback cycles, coverage uncertainty, and release-cadence discussion.
3. Simon Stewart, [Test Sizes](https://testing.googleblog.com/2010/12/test-sizes.html), Google Testing Blog, 2010, resource-bounded test classification and isolation guidance.
4. Sebastian Elbaum, Alexey G. Malishevsky, and Gregg Rothermel, [Test Case Prioritization: A Family of Empirical Studies](https://digitalcommons.unl.edu/csearticles/8/), *IEEE Transactions on Software Engineering* 28(2), 2002, pp. 159–182.
5. Google, [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html), Engineering Practices documentation, self-contained change and review guidance. Retrieved 2026-09-06.
6. Bazel Project, [Remote Caching](https://bazel.build/remote/caching), official documentation, current cache operation and correctness cautions. Retrieved 2026-09-06.
7. Dinah McNutt, [Release Engineering](https://sre.google/sre-book/release-engineering/), *Site Reliability Engineering*, 2016, continuous build, test-target, artifact, and policy foundations.
8. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, deployment-pipeline, fast-feedback, and staged-evidence foundations.

## Exercises

### Exercise 1

Define feedback time, first-signal time, decision time, queue time, critical path, selection, prioritization, soundness envelope, detection yield, and deferred check. Explain which distinctions prevent metric gaming.

### Exercise 2

Three independent sequential checks have $(d,p)$ values A $(2,0.10)$, B $(5,0.40)$, and C $(10,0.20)$. Derive the ratio order and expected stop-on-failure time. State the time for a passing candidate and every assumption.

### Exercise 3

A workflow has a 12-minute build followed by four 4-minute test shards and a 3-minute package check. Candidates wait 15 minutes in queue; one shard often takes 11 minutes. Diagnose the critical path and propose measured improvements without dropping evidence.

### Exercise 4

Design a change-based test-selection policy for a service with authentication, API, database migration, and documentation areas. Define mandatory checks, dependency inputs, ambiguity fallback, full-suite audit, clean-build comparison, and gate states.

### Exercise 5

A director offers a bonus for reducing “average green time” by 40%. Teams begin cancelling failed runs, retrying flakes, moving security checks nightly, and excluding queue time. Design a replacement objective, dashboard, experiment, and governance rule that rewards real feedback improvement.

## Answers to the Exercises

### Answer 1

Feedback time is elapsed time between declared events for a subject, evidence class, and consumer. First-signal time ends at the first actionable result; decision time ends when all blocking claims have outcomes. Queue time precedes execution capacity. The critical path is the longest dependency path controlling completion. Selection omits checks; prioritization reorders them. A soundness envelope states when omission is claimed safe. Detection yield measures useful discoveries per time under a population. A deferred check reports after the current decision and cannot silently support it. Exact endpoints prevent hidden queueing; first-signal versus decision prevents one green check from representing a gate; selection versus prioritization exposes missing evidence; envelope and yield connect speed to assurance; deferred status prevents post-decision checks from being counted as pre-decision protection.

### Answer 2

Ratios are A $0.10/2=0.05$, B $0.40/5=0.08$, and C $0.20/10=0.02$, so the narrow ordering is B, A, C. Expected time is $5+(1-0.40)2+(1-0.40)(1-0.10)10=5+1.2+5.4=11.6$ time units. A passing candidate executes all checks and takes $5+2+10=17$ units. Assumptions are deterministic positive durations, conditional probabilities stable for the candidate population, safe stop after a decisive failure, no dependency constraint, no order effect, and equal value of failures. Correlation, severity, variable tails, shared setup, and diagnostic needs can justify a different schedule.

### Answer 3

Ignoring queueing, the intended path is build 12, slowest nominal shard 4, then package 3: 19 minutes. Observed straggler behavior makes it 12+11+3=26; queueing makes user-visible decision about 41 minutes. First reduce or reserve queue capacity and segment its tail. Profile the 12-minute shared build, use correct incremental or content-addressed reuse, and start only consumers whose inputs are complete. Rebalance shards by measured robust duration rather than count, isolate the 11-minute test, or use work stealing with stable identities. Run independent setup in parallel, profile the package dependency, and preserve all four shard claims. Compare p50/p95/p99 and clean builds before and after.

### Answer 4

Always run compile, policy, authentication and authorization checks when executable or configuration code changes; never select migration compatibility away for schema, migration, persistence-library, or deployment changes. Map API code and schemas to contract, consumer, and integration tests; database code to migration, rollback, data-integrity, and service tests; documentation to rendering and link checks only when parsers prove no executable examples or generator inputs changed. Include build files, dependency locks, generators, shared libraries, schemas, configuration, and ownership rules in the dependency graph. Any parse failure, unknown path, stale graph, deleted test, shared-interface change, or policy ambiguity falls back to the full relevant suite. Version and record the selector, run periodic full suites and random holdouts, compare selected versus full failures, sample clean versus incremental builds, and track escapes. Gate states distinguish pass, fail, incomplete, unstable, waived, and unavailable; omitted evidence never becomes pass.

### Answer 5

Replace “average green time” with queue-inclusive time to first actionable signal and time to complete blocking decision, reported at p50, p95, and p99 by change and runner class. Include failed, cancelled, superseded, retried, and infrastructure-lost runs. Pair latency with initial failure detection, fail-pass transitions, required-claim completion, selection and deferral rates, full-suite-only findings, security findings, escapes, rollback linkage, compute, and diagnosis time. Shadow proposed schedulers or selectors on the same candidate population, preserve a full-run control and random holdout, and stratify results. Governance grants credit only when required claims and detection indicators are non-inferior within an explicitly reviewed envelope; moving checks, changing denominators, or excluding states is a policy change requiring risk-owner approval. Flake repair, queue reduction, correct reuse, critical-path work, and better tests qualify; retry erasure and hidden deferral do not.
