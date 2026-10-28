# Laboratory 90 — Production Readiness Review

**Course 9 · Module 90: Production Readiness, Capacity Planning, Rollouts, and Incident Learning**

[Chapter](../../course-book/module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md) · [Workbook](../../course-book/module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/workbook.md) · [MetricRail guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Production Readiness, Capacity Planning, Rollouts, and Incident Learning**: What evidence is sufficient to put this system under real load, how is risk limited during rollout, and how does operational evidence change the next design? The product must make **Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **production decision record** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a readiness decision engine that combines current review evidence with a checked capacity estimate. It replaces the simplistic question “Do tests pass?” with an explainable result across performance, reliability, observability, security, rollback, and incident practice.

Each `Evidence` item names one `Area`, describes what was reviewed, binds the reviewed revision to the current revision, and records pass/fail. `Capacity` estimates bounded active, queued, and fixed memory. `review` returns a `Review` containing the decision, missing/stale/failed areas, calculated capacity, and whether the budget is exceeded.

## Evidence invariants

Require exactly one unambiguous item per required area. Duplicate area evidence is an input error; silently choosing the latest or first can approve the wrong artifact. Descriptions must be nonempty. An item is current only when reviewed and current revision identifiers match exactly under this laboratory’s model.

Classify blockers separately:

- **missing:** no evidence for a required area;
- **stale:** evidence describes another revision;
- **failed:** the review found a defect;
- **capacity exceeded:** the checked estimate is above budget.

Failed evidence remains a failure even if stale; do not hide the stronger reason through classification order.

## Capacity model

Estimate:

```text
fixed_bytes
+ active × bytes_per_active
+ queued × bytes_per_queued
```

Use checked multiplication and addition. Zero budget is invalid. Arithmetic overflow is not “too large” by guess; it is a typed review error. Explain that this is a scoped model, not complete process RSS.

## Construction route

1. Define a stable ordered set of required areas.
2. Validate evidence identity, uniqueness, and descriptions.
3. Calculate capacity with checked arithmetic.
4. Classify every area into current pass, current fail, stale, or missing.
5. Preserve failed evidence explicitly.
6. Decide `Deploy` only when no blocker exists and capacity fits.
7. Return all blockers in stable order.
8. Test every individual blocker and combinations.

## Readiness scenarios

Create and explain:

1. complete current passing evidence within capacity;
2. one missing rollback review;
3. stale performance evidence after a code revision;
4. failed security evidence;
5. duplicate evidence input;
6. capacity arithmetic overflow;
7. capacity exactly at and one byte above budget;
8. stale-and-failed evidence.

The result should make the next action obvious without reading implementation code.

## Adversarial cases

Test empty descriptions, empty revision strings according to your declared policy, duplicate areas with conflicting results, maximum integer values, zero budget, and evidence supplied in random order. Output ordering must be deterministic.

## Transfer

Extend freshness from one revision string to a structured identity containing source revision, lockfile digest, profile, target, configuration schema, and workload/corpus version. Decide which changes invalidate which evidence areas rather than invalidating everything indiscriminately.

## Completion

The laboratory is complete when no missing, stale, failed, duplicate, or over-budget condition can be mistaken for approval; arithmetic is checked; the review explains all blockers; and a clean current input produces a deterministic deploy decision.

Inspect `solution/` only after defining your own blocker precedence. Compare explanation quality and invariants. The reference is not a universal production-readiness framework; it is a compact executable model of evidence freshness and bounded capacity.

## Readiness decision packet

Prepare a one-page go/no-go recommendation backed by separate evidence appendices. The recommendation must identify the exact artifact, target environment, forecast workload, measured sustainable capacity, latency objective, failure budget, security review state, known limitations, rollout stages, rollback trigger, and accountable owner. Every number must link to a reproducible experiment or operational source.

Run a tabletop incident involving overload during a canary while one instance is unavailable. Trace admission, terminal accounting, metrics, alerts, operator decisions, rollback, and recovery. Then identify one place where the evidence was insufficient and improve the product or runbook. The final verdict may be “no-go”; a well-supported refusal is a stronger engineering result than an unsupported approval.

## Independent challenge

Have another reader challenge the recommendation using one changed assumption: traffic is twice as bursty, one dependency is degraded, a tenant approaches the identifier limit, or rollback takes longer than expected. Recompute capacity and risk rather than defending the original answer reflexively. Record whether the verdict changes and which evidence was most sensitive. This challenge tests whether the readiness model is useful beyond the exact scenario used to create it.

## Completion question

State the narrowest truthful readiness claim you can make. It must name the artifact, environment, workload envelope, evidence date, known exclusions, and rollback condition. Rephrase any universal language such as “production ready” into a bounded statement that another operator can verify or falsify.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Production Readiness Review**.
2. Draw the smallest **production decision record** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to MetricRail so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery.
- Derive initial capacity and headroom from measured service demand, resource use, and burst policy.
- Distinguish load test, stress test, soak test, fault test, compatibility test, and rollback rehearsal.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 90 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **production decision record**. Defend why your design is simpler than one plausible alternative under the new requirements.
