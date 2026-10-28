# Worked Answers — Module 09: Fault Injection, Troubleshooting, and Game Days

Use these solutions to audit your reasoning for **Fault Injection, Troubleshooting, and Game Days**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What makes a fault experiment scientific enough for this course?

A prewritten falsifiable hypothesis, controlled fault, baseline, bounded scope, authoritative oracle, stop condition, cleanup, and repeatable evidence.

The chapter’s decisive distinction is this: A reliability experiment begins with a steady-state claim and falsifiable hypothesis, injects one bounded fault, observes authoritative and diagnostic evidence, stops safely, cleans up, and retains a regression. Chaos without an oracle is disruption, not engineering.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 2. Why test latency separately from failure?

They exercise different timeout, pool, cancellation, retry, and circuit paths. Immediate failure cannot reveal blocked-resource behavior.

In the cumulative capstone, the rule becomes concrete: Begin with the failure Database 500 instead of latency . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Use a latency or connection-hold fault with bounded duration and observe remaining budgets, pool acquisition, cancellation, and request outcome. , and rerun the focused regression in both languages.

## 3. What is a safe blast radius?

The minimum synthetic tenant/operation/dependency/duration/concurrency needed to test the claim without affecting real data or unrelated journeys.

A useful way to reason about the boundary is: Apply Steady-state hypothesis, Fault model, Blast radius to this module’s capstone increment: Build deterministic fault profiles, an evidence-first troubleshooting method, a controlled game day, stop conditions, cleanup verification, and planted defects proving the checks are sensitive. State one misleading green signal and the durable observation that would overrule it.

## 4. When should an experiment abort?

When integrity, resource, security, or unrelated-journey thresholds are exceeded or the fault cannot be controlled/observed.

The implementation consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=09 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 5. Why use an unaffected journey as a control?

It tests isolation and helps distinguish system-wide ambient change from the injected fault.

The important nuance is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=09 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 6. What is the first troubleshooting question?

Which critical journey is failing and what public/durable evidence defines the failure?

Under concurrency or failure, the distinction becomes: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=09 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 7. Should operators trust the first correlated metric?

No. Correlation guides hypotheses; durable state, controlled reproduction, and counterfactual evidence test mechanism.

**Common mistake.** Giving an unconditional answer to “Should operators trust the first correlated metric?” without classifying responsibility and failure semantics.

The design remains honest only if: Apply Steady-state hypothesis, Fault model, Blast radius to this module’s capstone increment: Build deterministic fault profiles, an evidence-first troubleshooting method, a controlled game day, stop conditions, cleanup verification, and planted defects proving the checks are sensitive. State one misleading green signal and the durable observation that would overrule it.

## 8. What cleanup evidence is required after a worker-kill test?

No active fault, expired/recovered leases resolved, no stale worker commit, no duplicate terminal effect, and bounded queue/permits.

The consumer-facing consequence is: A reliability experiment begins with a steady-state claim and falsifiable hypothesis, injects one bounded fault, observes authoritative and diagnostic evidence, stops safely, cleans up, and retains a regression. Chaos without an oracle is disruption, not engineering.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 9. How should a discovered failure be retained?

As the smallest deterministic regression test/vector plus updated requirement, alert, dashboard, or runbook where appropriate.

**Common mistake.** Describing a procedure for “How should a discovered failure be retained?” without a falsifiable completion condition.

The operational consequence is: Begin with the failure Database 500 instead of latency . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Use a latency or connection-hold fault with bounded duration and observe remaining budgets, pool acquisition, cancellation, and request outcome. , and rerun the focused regression in both languages.

## 10. When are compound faults appropriate?

After single-fault paths are understood and the interaction itself is a named risk with tighter stop conditions.

The strongest engineering interpretation is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=09 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 11. Trace bounded fault injection and diagnosis in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/faults.py` and `capstone/tracks/typescript-fastify/src/reliability/faults.ts`. The required invariant is that faults have hypotheses, blast-radius guards, abort conditions, cleanup, and an oracle that distinguishes the intended failure.

The defect-oriented view is: Apply Steady-state hypothesis, Fault model, Blast radius to this module’s capstone increment: Build deterministic fault profiles, an evidence-first troubleshooting method, a controlled game day, stop conditions, cleanup verification, and planted defects proving the checks are sensitive. State one misleading green signal and the durable observation that would overrule it.

## 12. Compare bounded fault injection and diagnosis across Python and TypeScript

Both tracks must preserve this invariant: faults have hypotheses, blast-radius guards, abort conditions, cleanup, and an oracle that distinguishes the intended failure. The intentional difference is that injection hooks differ; seed, target, fault decision, and cleanup evidence are shared.

Across the Python and TypeScript tracks, the invariant is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=09 TRACK=python and explain why the same public and durable outcome holds in the other language.
