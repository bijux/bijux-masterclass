---
module_id: SDRE-016
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 16
title: Merge Queues
status: complete
last_verified: 2026-09-06
---

# Merge Queues

## One-Page Review

### Governing question

How can an integration queue admit reviewed changes to a busy mainline only after validating the exact combined revision that will be committed, while preserving fairness, evidence identity, and useful throughput?

### Essential definitions

- a **candidate** is an immutable reviewed source change proposed for a target branch;
- a **target tip** is the exact current revision at the head of that branch;
- a **merge queue** orders eligible candidates and constructs revisions for pre-integration validation;
- a **merge group** is one or more queued candidates combined with a target tip for validation;
- a **speculative prefix** contains a candidate plus all candidates ahead of it that are assumed to merge;
- an **integration revision** is the exact combined source tree presented to required checks;
- **evidence binding** associates results with that revision, policy, environment, and check definitions;
- **head-of-line blocking** occurs when the first candidate delays candidates behind it;
- **batching** validates or lands multiple candidates as one group;
- **failure attribution** identifies which candidate or interaction caused a group to fail;
- **queue invalidation** makes prior evidence unusable because the target tip, candidate, order, policy, or prefix changed;
- a **bypass** integrates outside the ordinary queue policy;
- **admission latency** is time from becoming queue-eligible to integration or a terminal rejection.

### Central model, mechanism, or theorem

Let target tip be $b$ and ordered immutable candidates be $c_1,\ldots,c_n$. With deterministic merge operator $M$, the speculative prefix for position $i$ is

$$
q_i=M(b,c_1,\ldots,c_i).
$$

Candidate $c_i$ may integrate only if required evidence passes for the exact revision that will become the target tip and every preceding queue assumption remains true. If $c_j$ for $j<i$ fails, changes, or leaves the queue, evidence for $q_i$ does not validate the rebuilt prefix $M(b,c_1,\ldots,c_{j-1},c_{j+1},\ldots,c_i)$.

### Critical invariants

- freeze candidate identities when they enter the queue;
- construct and record the exact integration revision;
- trigger every required check for queue-created revisions;
- bind results to revision, policy, check, environment, and attempt;
- integrate only in an order consistent with validated prefixes;
- invalidate descendants whenever a prefix assumption changes;
- distinguish source conflict, check failure, infrastructure loss, timeout, and policy revocation;
- never treat a candidate-branch pass as evidence for a different combined tree;
- make batching and failure-attribution policy explicit;
- preserve fairness and bound priority overrides;
- recheck eligibility when approval, authorization, or candidate content changes;
- record queue transitions, cancellations, removals, and bypasses;
- keep the target branch recoverable even when required checks are imperfect.

### Common failures

Common failures include checking a proposal against an old target tip, trusting branch-only CI, reusing results after queue reorder, accepting a status reported for the wrong commit, missing the queue-specific CI trigger, merging a whole failed batch without attribution, cancelling descendants without rebuilding them, allowing unbounded priority jumps, retrying deterministic integration failures, bypassing without revalidation, and claiming that a green target branch proves every queued interaction safe.

### Compact example

Base configuration is `load=5, limit=10`. Candidate A changes load to 7 and passes. Candidate B changes limit to 6; B alone against the base passes, but prefix A+B violates `load <= limit`. Candidate C is validated in prefix A+B+C, so its result becomes stale when B is removed. The queue preserves A, removes or repairs B, rebuilds A+C, and validates that exact revision before C lands.

### Connections

[SDRE-015](015-parallelizing-ci-workloads.md) schedules the checks run for speculative revisions. [SDRE-017](../ROADMAP.md) next defines the claims and policies enforced by quality gates; [SDRE-018](../ROADMAP.md) distinguishes flaky outcomes from deterministic queue failures.

## Governing Question

A proposal can pass every check on its own branch and still break the target after another proposal integrates first. The source tree that was reviewed, the source tree that was tested, and the source tree that will land may differ. A merge queue closes that gap by serializing the integration decision while optionally evaluating future prefixes in parallel.

The engineering challenge is not merely “merge in order.” It is to maintain a proof obligation: the committed tree must be the tree for which current required evidence was accepted. Throughput optimizations—speculation, batching, selective checks, caching, and priority—are legitimate only while that binding remains intact.

## Why This Matters

Fast review and parallel CI can create a race. Candidates A and B both pass against base $b$. A lands first, producing $b_A$. B then lands using evidence for $M(b,B)$ even though the committed result is $M(b_A,B)$. If A and B interact, mainline breaks despite two green proposal runs.

Current GitHub documentation describes a merge queue that tests a proposal with the latest target branch and queued proposals ahead of it, and requires CI to report checks for queue-created merge-group revisions [1]. Current GitLab merge-train documentation similarly describes prefix pipelines—A, A+B, and A+B+C—and rebuilding successors after a failed candidate is removed [2]. These product behaviors illustrate the durable prefix model; the chapter does not prescribe either vendor.

Humble and Farley emphasize keeping the deployment pipeline and mainline in a releasable state [3]. A queue is one admission mechanism toward that objective. It cannot guarantee correctness: tests may be incomplete, flaky, compromised, or environment-specific. Its bounded guarantee is that stated policy was evaluated for a recorded combined revision before integration.

## Prerequisites and Retrieval

Retrieve commit, branch, target tip, merge base, three-way merge, conflict, source tree, content digest, immutable identifier, pull request, code review, approval, status check, CI pipeline, queue, FIFO, priority, starvation, batch, throughput, latency, timeout, retry, cancellation, artifact, idempotence, and audit log.

From SDRE-011 through SDRE-013 retrieve continuous integration, trunk-based flow, branch topology, and integration delay. From SDRE-014 retrieve exact change and evidence subjects; from SDRE-015 retrieve scheduling, fail-fast, cancellation, and fleet-level trade-offs. Testing & Quality Engineering owns whether checks support their claims; this chapter owns admission against combined revisions.

## Learning Objectives

After completing this module, you should be able to:

1. explain the stale-base race that merge queues address;
2. construct sequential and speculative integration prefixes;
3. state the exact evidence-binding invariant;
4. invalidate downstream evidence after a prefix mutation;
5. distinguish conflicts, deterministic failures, flaky outcomes, and infrastructure loss;
6. compare sequential, speculative, and batched queue strategies;
7. design fair priority and emergency-bypass policy;
8. preserve approval and authorization semantics through queue residence;
9. measure queue latency, throughput, waste, and mainline outcomes;
10. diagnose unsafe or misleading merge-queue configurations.

## Core Exposition

**Define queue eligibility.** A candidate becomes eligible only after its immutable revision, target branch, review approvals, ownership rules, preliminary checks, and policy metadata satisfy an entry contract. Queue entry is not integration approval forever. Record the revision digest and reject silent source updates; a changed candidate is a new evidence subject and ordinarily re-enters eligibility evaluation.

Separate candidate checks from integration checks. Candidate checks provide early feedback against a known base or merge result. Queue checks validate the exact proposed integration context. Some work may be reused if its full input key matches, but a green badge associated only with a proposal number is insufficient.

**Construct the integration tree explicitly.** Resolve an exact target tip $b$, combine the candidate using the configured merge method, and materialize the source tree to be checked. Record base, candidate revisions, order, merge method, resulting revision, and content-tree digest. A symbolic branch name can move and cannot serve as durable evidence identity.

The merge method matters. Merge commits, rebases, and squashes produce different commit identities even when content is equivalent. Policy may bind checks to content plus configuration or require the exact commit object. State the equivalence rule; never assume it.

Source conflicts are a construction failure, not a test failure. Report conflicted paths and the two exact inputs. Do not run downstream checks on a partially resolved or tool-dependent workspace and call the result integration evidence.

**Understand the stale-base race.** Suppose A and B each pass against $b$. This establishes evidence for $M(b,A)$ and $M(b,B)$, not for $M(M(b,A),B)$. Textual non-conflict does not imply behavioral compatibility: one candidate can change a default, schema, feature flag, policy, dependency, or timing assumption consumed by the other.

Requiring authors to update branches can reduce the race but creates repeated manual rebases and still permits target movement after the last check. The queue moves synchronization into one admission controller and decides integration only from current combined evidence.

**Choose sequential or speculative evaluation.** A sequential queue constructs and validates only the head candidate. If it passes, integrate it, advance the target, and evaluate the next. This minimizes wasted CI and makes failure attribution simple, but total throughput is bounded by one integration check at a time.

A speculative queue evaluates several prefixes concurrently: $q_1=M(b,c_1)$, $q_2=M(b,c_1,c_2)$, and so on. If all earlier prefixes pass, several candidates can advance quickly. GitLab's current merge-train description uses this prefix pattern [2]. The cost is speculative work and invalidation: removing $c_1$ changes every later prefix.

Speculation is valid only when integration order respects dependencies among its assumptions. A passing $q_3$ cannot justify landing $c_3$ before $c_1$ and $c_2$ if its evidence was obtained with both present. Conversely, if $q_2$ is exactly the new mainline after $q_1$ lands, its evidence may remain relevant under the queue's declared identity rule.

**Invalidate precisely but conservatively.** Any change to target tip, candidate content, prefix membership, order, merge method, required checks, policy version, environment contract, or material check definition may invalidate evidence. Rebuild affected integration revisions and cancel redundant work.

When B fails in A+B, remove or repair B and rebuild C as A+C. Do not simply subtract B's status from the old A+B+C result; execution is not algebraically decomposable. A failed predecessor can also contaminate generated artifacts or caches, so subsequent work must bind immutable inputs and safe caches.

**Classify outcomes.** A merge conflict means the integration revision could not be constructed. A deterministic check failure means the constructed revision violated a required claim. An infrastructure loss means evidence was not obtained. A timeout may be either product behavior or capacity failure and needs explicit classification. A flaky result is nondeterministic evidence and is addressed in SDRE-018.

Only deterministic candidate-caused or interaction-caused outcomes justify a code repair conclusion. Infrastructure loss can be retried under bounded policy against the same revision. Rebuilding after any subject change is not a retry; it is a new evaluation.

**Bind status reports.** Accept a status only from an authorized producer for the expected integration revision, check identity, policy version, and attempt. Protect callback and API paths from confused-deputy errors. A check named `ci` on an old commit must not satisfy a requirement named `ci` on the queue revision.

Current GitHub documentation requires workflows using its Actions integration to trigger on the distinct merge-group event, and third-party CI to recognize queue-created temporary branches [1]. The general lesson is to test the actual queue subject. A missing trigger leaves the queue waiting or tempts operators to weaken requirements; it must not be interpreted as success.

Artifacts inherit the same binding. Sign or digest manifests containing source tree, producer job, environment, dependencies, and result. A later prefix may reuse an artifact only when the artifact's declared inputs equal what the later check requires.

**Design batching deliberately.** A batch combines multiple candidates into one group, amortizing expensive setup and increasing landing throughput. If it passes, the queue may integrate the group under its configured order and merge method. If it fails, the queue needs an attribution policy: test candidates individually, bisect the batch, use dependency information, or reject the whole group for repair.

A green batch proves the combined group passed stated checks; it does not prove each candidate would pass independently. That may be acceptable because the combined tree is what lands. A red batch does not identify a culprit: two individually good candidates can interact, and one failing candidate can mask others.

Large batches increase diagnosis cost, rollback coupling, and change impact. Small candidates reduce these costs. Google Engineering Practices currently recommends self-contained small changes for review, integration, and rollback reasons [4]; this is operational guidance rather than a universal numeric threshold.

**Prevent head-of-line pathologies.** FIFO is predictable and limits arbitrary favoritism, but one slow or resource-specialized candidate can block the line. Parallel speculative prefixes hide some latency but consume more capacity. Separate queues by truly independent target branch or resource class only when their integrations do not share the same serialization point.

Define maximum residence, check timeout, stale-candidate handling, and owner notification. Allow a stuck candidate to leave without losing its diagnostic history. Re-entry occurs under current policy and current target; it does not reclaim obsolete evidence.

Priority should be bounded and auditable. An emergency security fix may move ahead, but reordering invalidates affected prefixes and consumes rebuild capacity. Current GitHub documentation explicitly warns that jumping to the front rebuilds in-progress queue work [1]. Frequent exceptions can reduce rather than improve delivery speed.

**Govern bypasses.** A bypass changes the mainline without ordinary combined evidence and invalidates queued prefixes. Require explicit authorization, reason, exact candidate, risk assessment, narrower emergency checks where possible, rollback plan, and post-integration verification. Automatically rebuild the queue from the new target.

“Documentation only” is not an inherent safe-bypass class: documentation may drive builds, packaging, generated sites, compliance, or runtime configuration. Use the change-impact model from SDRE-014 rather than filenames alone.

**Preserve approval semantics.** Queue waiting can outlive approvals, security attestations, dependency scans, or policy versions. Re-evaluate expiration, dismissed reviews, ownership changes, new conversations if policy makes them blocking, and newly discovered vulnerabilities. Tools differ, so encode required behavior in repository governance and test it.

Do not let administrators silently become universal bypass identities. Separate configuration authority, queue admission, CI status production, and emergency override where the risk requires it. Audit both successful and rejected mutations.

**Recover the target branch.** A queue reduces stale-base integration failures but cannot make checks complete. If mainline breaks, stop ordinary admissions, identify the exact first bad revision, revert or correct with minimal delay, invalidate affected queue evidence, and rebuild from the recovered tip. Do not preserve throughput statistics by leaving a known-bad target open.

Direct pushes, force updates, automated dependency changes, and other writers must participate in the same branch policy or trigger queue invalidation. A queue guarding only one UI path is not the serialization boundary it claims to be.

**Measure the queue as a system.** Track arrival rate, eligibility-to-entry delay, residence time, time at head, validation time, integration rate, queue length, age percentiles, removals by reason, conflict rate, deterministic failures, infrastructure loss, flaky outcomes, cancellation waste, speculative rebuilds, batch sizes, priority jumps, bypasses, and mainline failures after admission.

Segment by candidate size, subsystem, required resource, and risk class. A high integration rate can coexist with starvation or excessive speculative cost. A low mainline failure count does not alone prove the queue: failures may be rare, checks weak, or recovery unrecorded.

## Definitions and Notation

Let $b$ be an immutable target revision and $C=(c_1,\ldots,c_n)$ an ordered tuple of immutable candidate revisions. Let $M(x,c)$ apply the repository's configured integration operation to base $x$ and candidate $c$, either returning a new immutable revision or a typed conflict.

Define prefixes recursively:

$$
q_0=b,\qquad q_i=M(q_{i-1},c_i).
$$

Equivalently, where every application succeeds, $q_i=M(b,c_1,\ldots,c_i)$. Let $R(q,p,e)$ mean every check required by policy version $p$ produced an accepted result for revision $q$ under evidence environment contract $e$. Integration of $c_i$ requires $R(q_i,p,e)$ plus unchanged prior-prefix assumptions and current eligibility.

If candidate $c_j$ is removed, a rebuilt later prefix is

$$
q_i'=M(b,c_1,\ldots,c_{j-1},c_{j+1},\ldots,c_i).
$$

In general $q_i'\ne q_i$, so $R(q_i,p,e)$ says nothing about $R(q_i',p,e)$ without an explicit, justified equivalence proof.

For candidate $c$, admission latency is $L(c)=t_{terminal}(c)-t_{eligible}(c)$. Decompose it only with non-overlapping intervals such as eligibility wait, queue wait, evaluation, invalidation rework, and integration transaction. Throughput over window $[t_0,t_1]$ is the number of integrated candidates divided by $t_1-t_0$; define how batches are counted.

## Mechanisms, Invariants, or Proof Structure

**Exact-subject argument.** Checks are functions or observations over a subject revision plus environment and policy. When subject $q$ changes to $q'$, the prior result remains evidence about $q$, not $q'$. Equal proposal labels or similar diffs do not establish subject equality.

**Prefix-order invariant.** If $q_i$ was validated assuming candidates $c_1,\ldots,c_i$, then it may become the target only through an integration sequence whose resulting tree is exactly $q_i$ under the accepted identity rule. Landing $c_i$ before an assumed predecessor violates the premise.

**Invalidation argument.** Removing $c_j$ changes the recursive input to every successor $q_k$ for $k\ge j$. Even when source text happens to match, policy requires recomputing identity or proving equivalence. Cancellation and reconstruction therefore preserve evidence binding; they are not wasted correctness work.

**Failure-attribution counterexample.** Candidate A raises load from 5 to 7 under limit 10. Candidate B lowers limit to 6. Each passes alone against the base, but A+B fails. A red group cannot be attributed to B alone or A alone without further evaluation.

**Executable prefix model.** This deterministic model constructs configuration prefixes and demonstrates interaction failure and descendant invalidation. It does not execute version control, reviews, or CI.

<!-- bijux-verify: {"id":"merge-queue-prefix-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"a_alone=True\nb_alone=True\na_b_prefix=False\na_b_c_prefix=False\na_c_rebuilt=True\nold_c_evidence_reusable=False\nmerge_exact_tested_tree=True\n","stderr":""}} -->
```python
base = {"load": 5, "limit": 10, "feature": 0}
changes = {
    "A": {"load": 7},
    "B": {"limit": 6},
    "C": {"feature": 1},
}

def merge(start, candidates):
    result = dict(start)
    for candidate in candidates:
        result.update(changes[candidate])
    return result

def required_checks(revision):
    return revision["load"] <= revision["limit"]

a = merge(base, ["A"])
b = merge(base, ["B"])
a_b = merge(base, ["A", "B"])
a_b_c = merge(base, ["A", "B", "C"])
a_c = merge(base, ["A", "C"])
print(f"a_alone={required_checks(a)}")
print(f"b_alone={required_checks(b)}")
print(f"a_b_prefix={required_checks(a_b)}")
print(f"a_b_c_prefix={required_checks(a_b_c)}")
print(f"a_c_rebuilt={required_checks(a_c)}")
print(f"old_c_evidence_reusable={a_b_c == a_c}")
tested_digest = tuple(sorted(a_c.items()))
landed_digest = tuple(sorted(merge(base, ["A", "C"]).items()))
print(f"merge_exact_tested_tree={tested_digest == landed_digest}")
```

## Alternatives and Trade-Offs

**No queue versus queued admission.** Direct integration has low mechanism overhead at low contention. A queue prevents stale-base races on busy protected branches but adds residence time, state, and CI demand.

**Author-updated branches versus controller-built revisions.** Author updates distribute work and expose integration early. A controller removes repeated manual synchronization and closes the last-update race, but becomes critical infrastructure.

**Sequential versus speculative prefixes.** Sequential evaluation minimizes invalidated work and simplifies attribution. Speculation improves throughput when candidates usually pass, at the cost of parallel capacity and cascaded rebuilds.

**Single candidate versus batch.** Single-candidate groups isolate failures and rollbacks. Batches amortize setup and can raise throughput, but obscure attribution and enlarge change impact.

**FIFO versus priority.** FIFO is predictable and resistant to favoritism. Priority expedites high-value or emergency work but can starve ordinary candidates and invalidate speculative prefixes. Use bounded classes and age promotion.

**Rebuild versus evidence reuse.** Rebuilding is expensive but straightforward. Reuse is safe only with complete matching keys or a proved equivalence relation. Proposal identity alone is insufficient.

**Automatic removal versus pause for diagnosis.** Removing failures keeps the queue moving. Pausing preserves context and permits investigation. Separate deterministic candidate failures from infrastructure incidents so policy can respond differently.

**Strict enforcement versus emergency bypass.** Enforcement keeps one serialization boundary. A bypass can restore service faster but invalidates queue assumptions and raises risk; require audit, rollback, and revalidation.

## Failure Modes and Misconceptions

- **“A and B passed, so A+B passes.”** Independent evidence does not cover interaction.
- **“No text conflict means compatibility.”** Behavioral and policy conflicts need not overlap lines.
- **“The pull-request SHA is the merge SHA.”** Queue construction usually creates another subject.
- **“A branch name identifies evidence.”** Branches move; immutable revisions do not.
- **“One status name is enough.”** Check identity must include subject and authorized producer.
- **“The ordinary proposal trigger covers queue revisions.”** Queue-specific subjects may require distinct triggers.
- **“Later prefixes stay valid after removing the head.”** Their assumed source tree changed.
- **“A green batch proves every member alone.”** It proves only the checked combined group.
- **“A red batch identifies the bad candidate.”** Failure may arise from interaction.
- **“Retry all red groups.”** Deterministic failures need change; infrastructure losses may justify retry.
- **“Cancellation erases evidence.”** It must preserve reason, subject, and relevant diagnostics.
- **“FIFO eliminates unfairness.”** Specialized resources and long jobs can still cause unequal delay.
- **“Priority always accelerates emergencies.”** Reordering can trigger widespread rebuilds.
- **“Administrators may bypass safely.”** Authority does not make unchecked code compatible.
- **“Docs-only changes never need the queue.”** Repository behavior can depend on documentation inputs.
- **“The queue guarantees a healthy mainline.”** It is bounded by checks, policy, and enforcement coverage.
- **“Direct pushes are unrelated.”** They change the base and invalidate queued evidence.
- **“Throughput alone measures success.”** Tail latency, waste, fairness, and failures also matter.

## Worked Examples

### Example 1

**Situation.** A and B both pass against base `b`; A changes a default consumed by B. **Reasoning.** B's evidence is for `b+B`, while landing after A produces `b+A+B`. The queue constructs and checks the latter before B integrates. **Conclusion.** Candidate-local green results do not close the stale-base race.

### Example 2

**Situation.** A, B, and C have speculative runs for A, A+B, and A+B+C; B fails. **Reasoning.** Preserve A's run, remove or repair B, cancel the old C prefix, and construct A+C. The old C status includes B and cannot be subtracted. **Conclusion.** Prefix changes invalidate descendant evidence.

### Example 3

**Situation.** Required checks never report for queue entries, though proposal CI works. **Reasoning.** The provider did not trigger on queue-created revisions. Add and authenticate the correct queue event or temporary-reference integration; do not drop the required check. **Conclusion.** CI must observe the exact integration subject.

### Example 4

**Situation.** A five-candidate batch fails. **Reasoning.** The result identifies only a failing combination. Sequential retest costs five runs; binary partitioning can reduce diagnosis when failures are stable, but interactions can require testing combinations. **Conclusion.** Batching trades throughput for attribution complexity.

### Example 5

**Situation.** A queue callback reports `test=pass` for the proposal commit rather than the merge-group commit. **Reasoning.** Validate subject revision, check identity, producer authority, policy version, and attempt. Reject the mismatched status and keep the candidate pending. **Conclusion.** A pass without subject binding is irrelevant evidence.

### Example 6

**Situation.** A critical security repair jumps ahead of 20 candidates. **Reasoning.** Authorize and record the priority change, run required checks on the repair plus current base, land or reject it, then rebuild every affected speculative prefix. Measure the rebuild cost. **Conclusion.** Priority is an explicit correctness and capacity event.

### Example 7

**Situation.** The head candidate needs scarce hardware that is unavailable for six hours. **Reasoning.** FIFO can block the branch. Reserve bounded hardware capacity, use a resource-class queue only if ordering remains correct, or temporarily remove and later re-enter the candidate under current base and policy. **Conclusion.** Fairness and scarce-resource admission require deliberate policy.

### Example 8

**Situation.** An infrastructure worker disappears after 40 minutes. **Reasoning.** Mark the attempt lost, retain logs and subject identity, and retry under bounded infrastructure policy against the same revision. Do not ask the author to change code or count the lost run as a failing claim. **Conclusion.** Outcome classification controls recovery.

### Example 9

**Situation.** An administrator directly pushes a hotfix to mainline. **Reasoning.** The base changes, so freeze ordinary admission, record the bypass, validate or recover the new tip, invalidate all queue prefixes, and rebuild them. **Conclusion.** Every mainline writer participates in the serialization boundary.

### Example 10

**Situation.** Integration throughput rises 30%, but old low-priority candidates wait three days and speculative CI doubles. **Reasoning.** Segment age percentiles and compute cancellation and rebuild waste. Add bounded priority classes, age promotion, and concurrency tuning; do not declare success from throughput alone. **Conclusion.** Queue performance includes fairness and resource cost.

## Cross-Program Connections

- Algorithm Engineering owns queue disciplines, batching, online scheduling, and search strategies for failure attribution.
- Data Structures Engineering owns priority queues, persistent ordered state, and prefix representations.
- Concurrent & Parallel Programming owns speculation, cancellation, races, and invalidation reasoning.
- Testing & Quality Engineering owns check adequacy, flaky classification, and interaction-test design.
- Security Engineering owns protected-branch authorization, status authenticity, secrets, and bypass governance.
- Platform Engineering owns CI event delivery, queue controllers, runner capacity, and artifact identity services.
- Distributed Systems owns consensus over mutable state, idempotent events, leases, retries, and failure recovery.
- API & Service Engineering owns webhook contracts, authenticated status APIs, and idempotency keys.
- Systems Engineering owns queueing, bottlenecks, fairness, capacity, and end-to-end measurement.

## References

1. GitHub, [Managing a Merge Queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue), official documentation for merge groups, CI triggers, ordering, failure, concurrency, and priority. Retrieved 2026-09-06.
2. GitLab, [Merge Trains](https://docs.gitlab.com/ci/pipelines/merge_trains/), official documentation for combined prefix pipelines, failure removal, cancellation, reconstruction, and parallel limits. Retrieved 2026-09-06.
3. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, mainline and deployment-pipeline foundations.
4. Google Engineering Practices, [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html), current public engineering guidance. Retrieved 2026-09-06.
5. Paul M. Duvall, Steve Matyas, and Andrew Glover, *Continuous Integration: Improving Software Quality and Reducing Risk*, Addison-Wesley, 2007, integration discipline and automated-build foundations.
6. Martin Fowler, [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html), 2006, updated 2024, integration and mainline practices. Retrieved 2026-09-06.

## Exercises

### Exercise 1

Define candidate revision, target tip, integration revision, speculative prefix, and evidence binding. State the stale-base race in one precise paragraph.

### Exercise 2

For base $b$ and candidates A, B, C, and D, write the four speculative prefixes. If B is removed after its prefix fails, identify which evidence can remain and which revisions must be reconstructed.

### Exercise 3

A queue accepts required statuses by check name only, proposal workflows run but merge-group workflows do not, and administrators can push directly. Diagnose the three integrity failures and the minimum durable corrections.

### Exercise 4

Design policy for a queue with 25 candidates per hour, a 20-minute integration suite, four parallel CI slots, occasional flaky tests, and one emergency priority class. Address speculation, batching, retries, fairness, and evidence binding.

### Exercise 5

A batch of eight individually green candidates fails only when combined. Design a bounded attribution and recovery procedure that can detect both single-candidate defects and interactions without allowing untested revisions onto mainline.

## Answers to the Exercises

### Answer 1

A candidate revision is the immutable reviewed change proposed for integration. The target tip is the exact current head revision. An integration revision is the result of combining a candidate or group with that tip under a specified merge method. A speculative prefix contains the candidates up to one queue position and assumes earlier members will land. Evidence binding associates a result with the exact integration revision, check, policy, environment, and attempt. The stale-base race occurs when B passes against old base $b$, A lands first, and B is then integrated as $M(M(b,A),B)$ using evidence that covered only $M(b,B)$; interaction between A and B was never checked.

### Answer 2

The prefixes are $q_A=M(b,A)$, $q_B=M(b,A,B)$, $q_C=M(b,A,B,C)$, and $q_D=M(b,A,B,C,D)$. If B fails and is removed, evidence for A can remain if its revision and all evidence inputs are unchanged. B is rejected or repaired. C and D must be reconstructed as $q_C'=M(b,A,C)$ and $q_D'=M(b,A,C,D)$ and revalidated. Old results for A+B+C and A+B+C+D remain historical evidence about obsolete subjects, not evidence for the rebuilt prefixes.

### Answer 3

Name-only status matching permits a pass from the wrong commit, producer, policy, or attempt; require authenticated status reports keyed to the expected integration revision and check identity. Proposal-only triggers never evaluate the queue-created tree; configure the CI provider for the queue event or temporary revision and keep missing required status incomplete. Direct administrator pushes mutate the target outside the controller, invalidating every prefix and bypassing admission; enforce the protected path for all ordinary writers and define a narrowly authorized, audited emergency path that freezes and rebuilds the queue.

### Answer 4

One sequential 20-minute slot can admit at most three successful groups per hour, below arrival rate, so use the four slots for bounded speculative prefixes and measure whether pass probability makes the waste acceptable. Small batches may amortize setup, but cap batch size and retain an attribution procedure. Freeze every candidate and prefix, bind required results to exact combined revisions, and rebuild descendants after any removal or reorder. Classify flaky outcomes under a separate retry or quarantine policy; never retry arbitrary deterministic failures. Use FIFO within normal class plus age promotion, and permit a bounded emergency class with authorization and automatic rebuild accounting. Track residence percentiles, slot utilization, invalidated work, retries, failures, and mainline outcomes. If sustained safe service remains below arrival rate, reduce check span or add capacity rather than growing an unbounded queue.

### Answer 5

Keep the failed batch revision and evidence immutable, and do not merge any unvalidated replacement. First reproduce the failure once only if classification permits. Test balanced subgroups against the same current base to narrow stable failures; when a subgroup fails, continue partitioning it. Also test isolated candidates as needed because one defect may fail alone. If every isolated candidate passes, evaluate cross-subgroup combinations or use dependency and changed-interface information to search for interactions; do not infer innocence solely from isolation. Remove or repair identified candidates, reconstruct the remaining ordered prefix, and run its complete required checks. Integrate only the exact passing reconstruction. Record every tested combination, policy, environment, and result so diagnostic work is not confused with admission evidence.
