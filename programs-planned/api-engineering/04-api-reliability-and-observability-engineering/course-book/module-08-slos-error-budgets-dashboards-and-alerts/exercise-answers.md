# Worked Answers — Module 08: SLOs, Error Budgets, Dashboards, and Alerts

Use these solutions to audit your reasoning for **SLOs, Error Budgets, Dashboards, and Alerts**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What is the error budget for a 99.9% objective?

0.1% of eligible events over the objective window, calculated from exact counts or equivalent duration only when the SLI is time-based.

The chapter’s decisive distinction is this: Apply Objective, Error budget, Rolling window to this module’s capstone increment: Calculate rolling SLOs and error budgets, implement multiwindow burn-rate alerts, build a journey-first dashboard, link alerts to tested runbooks, and reject an unobservable release. State one misleading green signal and the durable observation that would overrule it.

## 2. What does burn rate 1 mean?

Errors are being consumed at exactly the average rate that would exhaust the entire budget over the objective window.

In the cumulative capstone, the rule becomes concrete: result = evaluate burn rate alert( SLODefinition("api", 0.999, 28 86400), BurnRateAlert("fast", "page", 3600, 300, 14.4, minimum events=100), long window=SLOWindow(good=9 980, total=10 000), short window=SLOWindow(good=980, total=1 000), ) assert result.firing is True ```

## 3. Why use two alert windows?

A short window detects urgent change while a longer window confirms sustained impact and reduces transient noise.

A useful way to reason about the boundary is: Begin with the failure Raw error-rate page . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Compute burn relative to the SLO and require paired short/long windows. Keep separate immediate alerts for hard safety invariants. , and rerun the focused regression in both languages.

## 4. How should no SLI data be displayed?

As missing/stale or insufficient data with instrumentation freshness, never automatically green.

**Common mistake.** Describing a procedure for “How should no SLI data be displayed?” without a falsifiable completion condition.

The implementation consequence is: An SLO is a versioned decision about an SLI over a window. Its error budget governs risk, dashboards explain current state, and alerts page only when timely human action can protect a critical journey.

**Evidence.** Recompute good, bad, eligible, excluded, and missing populations from durable outcomes; then validate burn-rate windows, alert linkage, and the user-journey dashboard.

## 5. What belongs at the top of a reliability dashboard?

Critical journey SLO status, eligible volume, good/bad counts, error-budget remaining, burn, and data freshness.

The important nuance is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=08 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Recompute good, bad, eligible, excluded, and missing populations from durable outcomes; then validate burn-rate windows, alert linkage, and the user-journey dashboard.

## 6. When is an alert page-worthy?

When a critical journey is at material risk, timely human action exists, and automation alone is insufficient.

Under concurrency or failure, the distinction becomes: An SLO is a versioned decision about an SLI over a window. Its error budget governs risk, dashboards explain current state, and alerts page only when timely human action can protect a critical journey.

**Evidence.** Recompute good, bad, eligible, excluded, and missing populations from durable outcomes; then validate burn-rate windows, alert linkage, and the user-journey dashboard.

## 7. Should every SLO violation page?

No. Slow-burn or reporting objectives may create tickets or review work; paging depends on urgency and actionability.

**Common mistake.** Giving an unconditional answer to “Should every SLO violation page?” without classifying responsibility and failure semantics.

The design remains honest only if: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=08 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 8. How should low traffic be handled?

Use explicit insufficient-data policy, longer windows, or representative synthetic transactions without pretending synthetic traffic equals all users.

**Common mistake.** Describing a procedure for “How should low traffic be handled?” without a falsifiable completion condition.

The consumer-facing consequence is: Apply Objective, Error budget, Rolling window to this module’s capstone increment: Calculate rolling SLOs and error budgets, implement multiwindow burn-rate alerts, build a journey-first dashboard, link alerts to tested runbooks, and reject an unobservable release. State one misleading green signal and the durable observation that would overrule it.

## 9. What is a repair-release exception?

A documented controlled change allowed during budget exhaustion because it plausibly reduces current risk, with focused proof, owner, and rollback.

The operational consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=08 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 10. Why include eligible volume on dashboards?

A percentage without denominator can be misleading and low-volume outcomes have different uncertainty.

The strongest engineering interpretation is: result = evaluate burn rate alert( SLODefinition("api", 0.999, 28 86400), BurnRateAlert("fast", "page", 3600, 300, 14.4, minimum events=100), long window=SLOWindow(good=9 980, total=10 000), short window=SLOWindow(good=980, total=1 000), ) assert result.firing is True ```

**Evidence.** Recompute good, bad, eligible, excluded, and missing populations from durable outcomes; then validate burn-rate windows, alert linkage, and the user-journey dashboard.

## 11. Trace SLO and alert mathematics in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/slo.py` and `capstone/tracks/typescript-fastify/src/reliability/slo.ts`. The required invariant is that objectives operate on exact eligible populations and multiwindow burn alerts require both fast and slow evidence with no-data handling.

The defect-oriented view is: Begin with the failure Raw error-rate page . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Compute burn relative to the SLO and require paired short/long windows. Keep separate immediate alerts for hard safety invariants. , and rerun the focused regression in both languages.

## 12. Compare SLO and alert mathematics across Python and TypeScript

Both tracks must preserve this invariant: objectives operate on exact eligible populations and multiwindow burn alerts require both fast and slow evidence with no-data handling. The intentional difference is that query syntax differs from pure model code; computed compliance, budget, and alert state must match.

Across the Python and TypeScript tracks, the invariant is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=08 TRACK=typescript and explain why the same public and durable outcome holds in the other language.
