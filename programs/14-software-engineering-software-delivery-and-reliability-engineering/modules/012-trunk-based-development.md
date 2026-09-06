---
module_id: SDRE-012
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 12
title: Trunk-Based Development
status: complete
last_verified: 2026-09-06
---

# Trunk-Based Development

## One-Page Review

### Governing question

How can many developers keep one shared line of development continuously coherent while delivering large changes in small, reversible increments?

### Essential definitions

- **trunk-based development (TBD)** is a source-control practice in which developers integrate small changes into one shared trunk at least daily and avoid long-lived development branches;
- **trunk**, **main**, and **mainline** name the authoritative integrated development line;
- a **short-lived branch** exists for hours rather than becoming an alternative integration line;
- **branch age** is elapsed time since divergence; **branch distance** is the change between its base and current trunk;
- a **merge queue** serializes and verifies candidate changes against an admissible trunk state;
- **branch by abstraction** introduces a stable seam so old and new implementations can coexist during incremental replacement;
- **parallel change** evolves a contract through expand, migrate, and contract steps;
- a **feature flag** separates integration of code from exposure of behavior;
- a **release branch** is a narrowly governed maintenance line for an already selected release, not a second feature-development trunk;
- **forward integration** returns a release-line fix to trunk so future versions do not regress;
- **revertability** means one change can be removed or disabled without undoing unrelated work.

### Central model, mechanism, or theorem

TBD minimizes divergent development state:

`slice → review → verify exact result → integrate to trunk → observe → repeat`.

For branch $b$ at time $t$, define distance $D(b,t)$ as trunk changes since its base and age $A(b,t)$. Neither predicts conflict alone, but increasing either enlarges the set of assumptions needing revalidation. Policy therefore bounds age and requires exact-result verification before admission.

### Critical invariants

- there is one authoritative development line;
- every developer integrates at least daily in small coherent batches;
- any branch is short-lived and disposable, not a hidden shared integration line;
- review and required checks finish quickly enough to preserve short lifetime;
- the admitted merge result, not a stale branch head, is verified;
- trunk remains buildable and its health response is immediate;
- incomplete behavior is isolated with compatible designs and governed flags;
- schema, API, and event changes tolerate mixed versions during migration;
- release branches accept only bounded maintenance and return fixes to trunk;
- access controls and queues constrain admission without creating multi-day inventory;
- temporary abstractions, flags, and compatibility paths have owners and removal criteria;
- history shape never substitutes for tests, observability, or release evidence.

### Common failures

Common failures include renaming week-long feature branches “short-lived,” batching changes behind slow review, testing against a stale base, sharing feature branches between teams, making flags permanent, merging incompatible schema changes, using release branches for new development, forgetting to forward-integrate a hotfix, allowing queues to become release trains, measuring commit count rather than integration delay, and assuming direct commits remove the need for review.

### Compact example

A payment migration is split into four trunk changes: add a compatible adapter; deploy dual-read telemetry; switch a bounded cohort behind a release flag; remove the old path after evidence and rollback windows pass. Each change lives on a branch for under four hours, is reviewed synchronously, and enters through a queue that tests the exact merge result. The large outcome takes weeks, but source divergence never does.

### Connections

[SDRE-011](011-continuous-integration-as-a-working-practice.md) defined the team feedback loop. [SDRE-013](../ROADMAP.md) next compares branching strategies and integration delay. [SDRE-014](../ROADMAP.md) later selects work safely after a change is admitted.

## Governing Question

Version-control branches are cheap to create, but divergent understanding is not. While a branch is isolated, trunk, dependencies, interfaces, tests, and neighboring work continue to change. Pulling trunk into the branch demonstrates one private combination; it does not integrate that branch with other private branches. The risk becomes visible only when a result enters the shared line.

Trunk-based development keeps this divergence window deliberately short. It is not “everyone edits production without controls.” Teams may commit directly, use short pull requests, or use a merge queue. The invariant is one development line, small batches, rapid review, exact-result verification, and frequent admission.

## Why This Matters

DORA's current capability guidance defines TBD through small batches integrated to trunk at least daily, with short-lived branches and no long integration or stabilization periods [1]. Its cited operational indicators—few active branches, daily merging, and rare code freezes—are diagnostic signals, not universal numeric laws.

Fowler's branching-pattern catalog separates integration frequency from mechanics and emphasizes that pulling mainline into a feature branch performs only partial integration; peer branches remain mutually untested until admitted [2]. This distinction explains why many green branch builds can coexist with a painful final merge.

TBD also changes architecture and planning. Work must be sliced so trunk remains coherent before an entire feature is exposed. Compatibility, toggles, observability, test speed, and review responsiveness become design concerns. The payoff is not absence of coordination but earlier, smaller coordination.

## Prerequisites and Retrieval

Retrieve repository, commit, parent, branch, base, head, merge, rebase, conflict, mainline, patch, cherry-pick, pull request, code review, status check, merge queue, revert, feature flag, abstraction, interface compatibility, schema migration, release line, hotfix, integration latency, and canonical artifact.

From SDRE-011 retrieve continuous integration, exact admitted state, mainline health, small batches, feedback latency, stop-the-line response, flags, and canonical artifacts. This chapter focuses on one branching practice. SDRE-013 owns broad comparison of branching strategies; STQE owns test design; Security Engineering owns deeper repository and identity threats.

## Learning Objectives

After completing this module, you should be able to:

1. define TBD independently of a particular version-control product;
2. distinguish direct-to-trunk, short-branch, and long-lived feature-branch workflows;
3. explain why regularly merging trunk into a branch is not full integration;
4. design rapid review and exact-result admission controls;
5. slice large features into compatible trunk changes;
6. use branch by abstraction, parallel change, and feature flags appropriately;
7. evolve database, API, and event contracts across mixed versions;
8. govern release branches and return hotfixes to trunk;
9. measure divergence without turning heuristics into guarantees;
10. adapt TBD controls to high-risk and large-scale environments.

## Core Exposition

**Define one development line.** Trunk is where development work becomes mutually visible and testable. It is not necessarily the production branch, and every commit need not be exposed to users. Tags and release branches can identify supported releases, but new feature development returns to one mainline.

Direct commit is the simplest topology for a small trusted team with strong pairing, tests, and revert discipline. Short-lived branches can support asynchronous tools and required reviews. A branch lasting three hours is compatible with TBD; a branch lasting three weeks is not rescued by its name.

**Understand integration completeness.** Suppose Alice and Bob branch from trunk at `t0`. Both later merge updated trunk into their own branches. Alice has tested her change with trunk but not Bob's unmerged change; Bob has the symmetric gap. Only admission to trunk, followed by testing of the combined state, completes integration between them.

This is why branch freshness helps but does not suffice. Rebase and merge mechanics may simplify history or conflict resolution; neither proves behavioral compatibility. The exact resulting revision needs its own checks.

**Bound branch lifetime and inventory.** Age is easy to measure but incomplete. A four-hour branch can diverge across a highly coupled refactor; a two-day documentation branch may have little semantic risk. Track age, commits or diff size, touched ownership areas, base distance, review wait, and failed rebases. Use these as prompts for slicing and collaboration, not automated claims of safety.

An open pull request is inventory. Waiting for a reviewer while starting more work increases concurrent state and makes the original context stale. Prioritize small reviews, pair or mob on risky changes, and establish response expectations. A policy requiring many serial approvals can be safe only if staffing makes them timely; otherwise it structurally prevents TBD.

**Verify the admissible result.** In a busy trunk, branch checks can finish after their base is obsolete. A merge queue constructs a candidate against current or ordered trunk, runs required checks, and admits only that result. If an earlier candidate changes trunk, later candidates must be reconstructed or validated under a sound batching model.

Queues trade parallel submission for controlled serialization. Monitor queue time, invalidation rate, throughput, starvation, and bypasses. Scaling runners cannot fix a serial dependency in the build, and batching unrelated candidates can make failure attribution harder.

**Slice by compatibility.** Large work belongs on trunk as a sequence of states that are independently buildable, testable, and reversible. Add before removing. Preserve old consumers while new producers appear. Introduce a seam before replacing its implementation. Carry both representations while migrating data. Observe actual use before contraction.

Branch by abstraction wraps the old dependency behind a stable interface, adds a new implementation, switches selection, then removes the old implementation and temporary seam [3]. It costs temporary complexity but keeps integration frequent. If the abstraction is poorly chosen, it can conceal semantic differences; tests and telemetry must compare the paths.

**Use parallel change for contracts.** A safe contract change generally has three stages. Expand: accept old and new forms without breaking existing consumers. Migrate: move producers and consumers while observing both. Contract: remove the old form only after evidence shows no supported use. This applies to APIs, events, function signatures, and database schemas.

Destructive schema change and application change in one commit assume atomic deployment across all instances and rollback paths. In distributed delivery, mixed versions are normal. Compatibility windows must cover deploy, rollback, queued messages, caches, and offline clients where applicable.

**Separate integration from exposure.** A release toggle can keep an incomplete path unavailable while code integrates. Toggle identity, owner, purpose, default, scope, creation date, expected removal, and tested states should be explicit. Long-lived permission or operational controls differ from temporary release toggles and need different governance [4].

Flags increase state space. Two Boolean flags allow four configurations; $n$ independent Boolean flags allow $2^n$. Not every combination needs equal testing, because constraints and risk differ, but unmanaged interaction grows quickly. Prefer flags at stable decision points, decouple routing from behavior, and remove expired toggles.

**Preserve reversibility.** A change is operationally small only if its effects can be contained. Avoid combining code, irreversible data deletion, external side effects, and broad configuration changes into one admission. Use additive migrations, idempotent jobs, feature disable paths, and explicit roll-forward or rollback decisions.

Reverting source does not undo a sent message, charged card, deleted column, or changed external contract. Record these boundaries during review. A revert can restore trunk build health while domain repair follows separately.

**Govern release branches narrowly.** A supported version may need a branch after trunk advances. Create it from an identified trunk revision. Permit only bounded fixes and release metadata under explicit policy. Verify and release artifacts from that branch with distinct identity.

Every applicable fix must also reach trunk, usually by applying the conceptual correction there rather than blindly replaying a patch into changed code. Track direction: trunk-to-release for selected fixes and release-to-trunk for defect knowledge. A permanent release branch accepting new features becomes another development trunk and restores divergence.

**Adapt review without creating delay.** Code review can be synchronous pairing, immediate peer review, or a fast pull-request process. High-risk changes may need specialist or separation-of-duty approval. The constraint is to resource those controls so small changes do not wait days. Smaller patches reduce reviewer cognitive load and make precise questions possible.

Repository protection should authenticate actors, prevent unauthorized history changes, require applicable checks, and record bypasses. Emergency admission needs limited scope, independent evidence, and follow-up. “Direct to trunk” never means anonymous or unaudited.

**Handle scale through ownership and queues.** Large repositories may receive many changes per minute. Use ownership routing, affected-target analysis, parallel checks, speculative queue execution, and deterministic merge ordering. Preserve the central invariant that every admitted revision is an evaluated shared state. Do not create subsystem branches that integrate only at quarterly boundaries.

Multiple repositories can still use TBD within each repository. Cross-repository compatibility then needs contract testing, versioning, staged rollout, and consumer observability. A single physical monorepo is neither required nor sufficient.

**Measure outcomes and constraints.** Track branch-age distribution, time from first commit to trunk, review wait, queue time, batch size, active branches, merge conflicts, post-admission failures, revert time, code-freeze duration, and stale flags. Segment generated changes, dependencies, docs, and risky migrations.

Numbers need interpretation. A low branch count can mean healthy flow or suppressed contribution. Tiny commits can be coherent slices or review-hostile fragments. Inspect samples and incidents before changing policy.

## Definitions and Notation

Let $base(b)$ be the trunk revision from which branch $b$ currently diverges, and let $head_T(t)$ be trunk head at time $t$. Define:

$$
A(b,t)=t-created(b)
$$

as branch age, and

$$
D(b,t)=Changes(base(b),head_T(t))
$$

as a vector of intervening trunk changes. A scalar commit count is only a lossy projection of $D$.

For independent Boolean flags $f_1,\ldots,f_n$, the unconstrained configuration set has cardinality

$$
|C|=2^n.
$$

Constraints can make configurations invalid or unreachable, so a risk-based test plan should enumerate meaningful equivalence classes and interactions rather than claim exhaustive safety from one default configuration.

## Mechanisms, Invariants, or Proof Structure

**Single-line invariant.** All new development becomes part of one authoritative trunk within the bounded integration interval. Release lines do not accept independent feature evolution.

**Exact-result invariant.** Checks authorize a content-identified merge result. If trunk movement changes that result, the authorization does not transfer automatically.

**Compatibility invariant.** During a parallel change, every deployed mixture within the supported window can communicate and preserve required data. Expansion precedes migration; contraction follows observed completion.

**Hotfix closure.** A release-line fix is not complete until affected supported release lines and trunk have an explicit disposition. This prevents the next trunk-derived release from reintroducing the defect.

**Executable admission model.** This model evaluates branch and release-line metadata. It does not merge source, evaluate semantic conflict, run tests, or enforce repository permissions.

<!-- bijux-verify: {"id":"evaluate-trunk-admission","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"fresh_feature=accepted\nstale_feature=rejected\nstale_base=rejected\nfailed_checks=rejected\nrelease_feature=rejected\nrelease_hotfix=accepted\nmissing_forward_fix=rejected\nflag_configurations=8\n","stderr":""}} -->
```python
def admit(change):
    if not change["checks_passed"] or not change["exact_base"]:
        return "rejected"
    if change["line"] == "trunk":
        return "accepted" if change["age_hours"] <= 24 else "rejected"
    if change["kind"] != "hotfix":
        return "rejected"
    return "accepted" if change["forward_disposition"] else "rejected"

base = {
    "line": "trunk", "kind": "feature", "age_hours": 3,
    "checks_passed": True, "exact_base": True, "forward_disposition": False,
}
print(f"fresh_feature={admit(base)}")
print(f"stale_feature={admit(base | {'age_hours': 49})}")
print(f"stale_base={admit(base | {'exact_base': False})}")
print(f"failed_checks={admit(base | {'checks_passed': False})}")
release = base | {"line": "release-2", "age_hours": 1}
print(f"release_feature={admit(release)}")
print(f"release_hotfix={admit(release | {'kind': 'hotfix', 'forward_disposition': True})}")
print(f"missing_forward_fix={admit(release | {'kind': 'hotfix'})}")
print(f"flag_configurations={2 ** 3}")
```

The 24-hour threshold illustrates one daily-integration policy. It is not a universal safety boundary.

## Alternatives and Trade-Offs

**Direct commit versus short pull request.** Direct commit minimizes delay and works with pairing and strong checks. Short pull requests provide an explicit review object and admission control but can create queues. Both can satisfy TBD when integration remains frequent.

**Merge versus rebase.** Merge preserves branch topology; rebase produces a linearized history. Either can construct a valid result. Choose for traceability and collaboration, then verify the exact content rather than treating history aesthetics as correctness.

**Queue serialization versus optimistic admission.** A queue reduces stale-base races but adds latency and a control-plane dependency. Optimistic admission is fast at low contention but can expose more post-merge failures. Scale the queue and checks to repository change rate.

**Branch by abstraction versus long-lived branch.** The abstraction adds temporary production complexity and requires compatible intermediate states. A long-lived branch keeps temporary code away from trunk but defers integration and feedback. Prefer the smallest risk across both code and coordination.

**Release branch versus release from trunk.** A release branch supports long maintenance and selective patches but creates another line to govern. Releasing directly from trunk simplifies flow when releases are frequent and rollback or roll-forward is strong.

## Failure Modes and Misconceptions

- **“TBD forbids every branch.”** It forbids long-lived alternative development lines.
- **“Pulling trunk daily is integration.”** Private branches remain unintegrated with one another.
- **“Rebase proves compatibility.”** It changes ancestry and content construction, not behavioral evidence.
- **“Direct commit means no review.”** Review can be synchronous or pre-admission.
- **“Required review may take as long as needed.”** Unstaffed delay structurally creates large batches.
- **“A merge queue cannot become a bottleneck.”** Serial admission and invalidation need capacity design.
- **“Feature flags eliminate risk.”** They add configurations, control paths, and cleanup debt.
- **“Disabled code does not matter.”** It still builds, ships, and may affect dependencies and security.
- **“Schema and code can change atomically.”** Mixed versions and rollback usually require compatibility.
- **“A source revert reverses every effect.”** External and destructive effects need domain repair.
- **“Release branches are extra trunks.”** They are bounded maintenance lines.
- **“Cherry-picking the hotfix closes it.”** Trunk also needs an explicit disposition.
- **“Few branches prove healthy flow.”** Participation or review may be blocked.
- **“Many tiny commits prove small batches.”** Coherence and independent validation matter.
- **“A monorepo guarantees integration.”** Process and compatibility still determine feedback.

## Worked Examples

### Example 1

**Situation.** Alice and Bob both merge trunk into their week-old branches each morning. **Reasoning.** Each sees trunk but neither sees the other's unmerged work. Their shared interface changes meet only in the final merge. **Conclusion.** Updating from trunk is partial synchronization, not full team integration.

### Example 2

**Situation.** A branch passes checks, waits six hours, and merges after 40 trunk changes. **Reasoning.** The tested object differs from the admitted merge result. A queue must reconstruct and recheck it, or a sound affected-check policy must authorize the exact result. **Conclusion.** Fresh evidence binds content, not branch names.

### Example 3

**Situation.** A new pricing engine needs one month. **Reasoning.** Add a stable pricing interface, route default traffic to the old engine, implement and compare the new engine behind a flag, switch bounded cohorts, then remove old code and the temporary seam. **Conclusion.** Large outcomes can use short source divergence through branch by abstraction.

### Example 4

**Situation.** A service wants to rename required JSON field `customerId` to `customer_id`. **Reasoning.** First accept both while emitting the new form, migrate consumers with telemetry, then remove the old form after the compatibility window. One breaking commit would fail mixed versions. **Conclusion.** Expand, migrate, and contract on trunk.

### Example 5

**Situation.** Three independent Boolean release flags exist. **Reasoning.** There are $2^3=8$ unconstrained configurations. Test default and enabled paths, then prioritize interactions by dependency and exposure; remove flags after rollout. **Conclusion.** Flags trade branch divergence for runtime state that must be governed.

### Example 6

**Situation.** A trunk change sends duplicate invoices and is reverted. **Reasoning.** Revert stops future executions but cannot unsend messages. Disable the path, identify affected operations idempotently, issue corrections, and preserve incident evidence. **Conclusion.** Source revertability and domain reversibility differ.

### Example 7

**Situation.** Version 2.1 needs an urgent parser fix while trunk targets 3.0. **Reasoning.** Apply and verify the bounded fix on `release-2.1`, then implement or confirm the conceptual fix on trunk. Track both dispositions. **Conclusion.** Maintenance lines require hotfix closure across future development.

### Example 8

**Situation.** Policy requires two reviewers, but median wait is two days. **Reasoning.** Developers batch more work and start new tasks, defeating daily integration. Add reviewer rotation, synchronous review windows, ownership routing, and escalation while retaining required independence. **Conclusion.** A control must be operationally staffed to coexist with TBD.

### Example 9

**Situation.** A merge queue batches ten unrelated changes to improve throughput; one fails. **Reasoning.** The batch obscures attribution and may require repeated partitioning. Speculative individual candidates or bounded batches with deterministic isolation trade more compute for faster diagnosis. **Conclusion.** Queue throughput must not recreate large integration batches.

### Example 10

**Situation.** A team reports only two active branches but has a three-week code freeze. **Reasoning.** Low branch count hides accumulated uncommitted or queued work. Inspect integration latency, review inventory, freeze duration, and actual admitted batches. **Conclusion.** Metrics need causal context; branch count alone is not TBD.

## Cross-Program Connections

- Software Engineering Methods & Evolution owns broader change processes; TBD supplies a frequent integration topology.
- Software Design & Domain Modeling enables coherent slices and seams for branch by abstraction.
- Software Architecture owns compatibility and coupling that determine whether independent changes can enter trunk safely.
- Testing & Quality Engineering owns evidence adequacy; merge queues bind selected evidence to exact candidates.
- Database Engineering owns transactional and schema mechanisms; parallel change governs their mixed-version delivery.
- API & Service Engineering owns contract compatibility and idempotent effects across service versions.
- Platform Engineering owns repository automation, queues, identity, runner capacity, and developer experience.
- Security Engineering owns repository threats, privileged bypass, and separation-of-duty requirements.

## References

1. DORA, [Trunk-Based Development](https://dora.dev/capabilities/trunk-based-development/), current capability guidance. Retrieved 2026-09-06.
2. Martin Fowler, [Patterns for Managing Source Code Branches](https://martinfowler.com/articles/branching-patterns.html), 28 May 2020. Retrieved 2026-09-06.
3. Martin Fowler, [Branch By Abstraction](https://martinfowler.com/bliki/BranchByAbstraction.html), practice description. Retrieved 2026-09-06.
4. Pete Hodgson, [Feature Toggles (aka Feature Flags)](https://martinfowler.com/articles/feature-toggles.html), 9 October 2017. Retrieved 2026-09-06.
5. Jez Humble and David Farley, *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*, Addison-Wesley, 2010.
6. Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate: The Science of Lean Software and DevOps*, IT Revolution, 2018.

## Exercises

### Exercise 1

Define trunk-based development and explain why a short pull-request branch can satisfy it while a regularly updated long-lived feature branch does not.

### Exercise 2

Three developers branch from `t0`. Alice merges at `t3`; Bob and Chen each merge `t3` into their branches but not Alice's later correction at `t4`. Trace which combinations have and have not been integrated.

### Exercise 3

A branch was checked at base `b7`, but two candidates entered trunk before it reached the head of a merge queue. Diagnose what the queue must do and what it must record.

### Exercise 4

Design a trunk-compatible migration from database column `full_name` to separate `given_name` and `family_name`, assuming old and new application versions overlap and rollback is required.

### Exercise 5

A medical-device team requires independent safety review and a six-hour hardware test, yet wants daily trunk integration. Design a workflow that preserves those controls without creating month-long branches.

## Answers to the Exercises

### Answer 1

TBD keeps one authoritative development line and integrates each developer's small batches into it at least daily, avoiding long-lived development branches. A pull-request branch lasting hours can provide review and exact-result checks before admission while keeping divergence bounded. Pulling trunk into a month-long feature branch synchronizes that branch with already integrated work but does not expose its changes to other private branches or the authoritative system. It remains a deferred integration line.

### Answer 2

Before `t3`, no developer change is integrated with another. When Alice enters at `t3`, trunk contains Alice plus prior trunk. Bob and Chen updating from `t3` each integrate privately with Alice's admitted state, but Bob and Chen remain unintegrated with each other. Alice's correction at `t4` is absent from both unless they update again or their queue constructs candidates on `t4`. Only each candidate's eventual exact trunk result completes integration with all work admitted before it.

### Answer 3

The evidence for the `b7` result is stale because admission would create different content. The queue should construct the candidate on the current ordered trunk head and rerun required checks, or apply a documented sound reuse rule based on exact unaffected inputs. It records original and new bases, candidate digest, included predecessors, checks and policy, invalidations, actor, result, and admitted revision. It must not transfer a green status based only on the branch head.

### Answer 4

Expand by adding nullable new columns while retaining `full_name`; deploy code that can read the old representation and dual-write or derive the new one with explicit precedence. Backfill idempotently in bounded batches and observe mismatches. Migrate readers and writers to the new fields, retaining rollback compatibility and accounting for replicas, caches, and queued work. After telemetry shows no supported old readers or writers and the rollback window closes, stop writing `full_name`, then contract by removing it in a separate migration. Each state is buildable, testable, observable, and reversible within its stated boundary.

### Answer 5

Develop in small trunk slices behind stable interfaces and disabled release flags. Run fast deterministic safety models, unit checks, static analysis, and exact-result merge checks on every candidate. Produce a digest-addressed artifact, then run the six-hour hardware suite against that exact digest. Independent reviewers approve the same digest and evidence; merge or exposure policy can distinguish “integrated but disabled” from “qualified for use.” If regulation requires review before source admission, staff a rapid safety-review rotation and keep patches small; if review may occur before exposure, integrate disabled code and block flag activation and release until review and hardware evidence pass. Preserve bypass prohibition and audit records.
