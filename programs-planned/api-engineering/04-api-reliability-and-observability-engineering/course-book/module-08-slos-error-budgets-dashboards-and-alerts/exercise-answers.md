# Reference Answers — Module 08: SLOs, Error Budgets, Dashboards, and Alerts

Read after attempting all twelve SLOs, Error Budgets, Dashboards, and Alerts exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. What is the error budget for a 99.9% objective?

**Answer.** 0.1% of eligible events over the objective window, calculated from exact counts or equivalent duration only when the SLI is time-based.

## 2. What does burn rate 1 mean?

**Answer.** Errors are being consumed at exactly the average rate that would exhaust the entire budget over the objective window.

## 3. Why use two alert windows?

**Answer.** A short window detects urgent change while a longer window confirms sustained impact and reduces transient noise.

## 4. How should no SLI data be displayed?

**Answer.** As missing/stale or insufficient data with instrumentation freshness, never automatically green.

**Common mistake.** Describing a procedure for “How should no SLI data be displayed?” without a falsifiable completion condition.

## 5. What belongs at the top of a reliability dashboard?

**Answer.** Critical journey SLO status, eligible volume, good/bad counts, error-budget remaining, burn, and data freshness.

## 6. When is an alert page-worthy?

**Answer.** When a critical journey is at material risk, timely human action exists, and automation alone is insufficient.

## 7. Should every SLO violation page?

**Answer.** No. Slow-burn or reporting objectives may create tickets or review work; paging depends on urgency and actionability.

**Common mistake.** Giving an unconditional answer to “Should every SLO violation page?” without classifying responsibility and failure semantics.

## 8. How should low traffic be handled?

**Answer.** Use explicit insufficient-data policy, longer windows, or representative synthetic transactions without pretending synthetic traffic equals all users.

**Common mistake.** Describing a procedure for “How should low traffic be handled?” without a falsifiable completion condition.

## 9. What is a repair-release exception?

**Answer.** A documented controlled change allowed during budget exhaustion because it plausibly reduces current risk, with focused proof, owner, and rollback.

## 10. Why include eligible volume on dashboards?

**Answer.** A percentage without denominator can be misleading and low-volume outcomes have different uncertainty.

## 11. Trace SLO and alert mathematics in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/slo.py` and `capstone/tracks/typescript-fastify/src/reliability/slo.ts`. The required invariant is that objectives operate on exact eligible populations and multiwindow burn alerts require both fast and slow evidence with no-data handling.

## 12. Compare SLO and alert mathematics across Python and TypeScript

Both tracks must preserve this invariant: objectives operate on exact eligible populations and multiwindow burn alerts require both fast and slow evidence with no-data handling. The intentional difference is that query syntax differs from pure model code; computed compliance, budget, and alert state must match.
