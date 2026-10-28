# Exercises — Module 08: SLOs, Error Budgets, Dashboards, and Alerts

Work through all twelve problems before opening the answers. In **SLOs, Error Budgets, Dashboards, and Alerts**, every response must settle this question: **How do versioned SLOs, exact error budgets, burn rates, dashboards, alerts, and runbooks drive decisions?** Use the cumulative platform, not an invented toy system. Preserve inherited guarantees and make every new assumption explicit and falsifiable.

## 1. What is the error budget for a 99.9% objective?

## 2. What does burn rate 1 mean?

## 3. Why use two alert windows?

## 4. How should no SLI data be displayed?

## 5. What belongs at the top of a reliability dashboard?

## 6. When is an alert page-worthy?

## 7. Should every SLO violation page?

## 8. How should low traffic be handled?

## 9. What is a repair-release exception?

## 10. Why include eligible volume on dashboards?

## 11. Trace SLO and alert mathematics in the primary implementation

Read `capstone/tracks/python-fastapi/src/api_reliability/slo.py` or `capstone/tracks/typescript-fastify/src/reliability/slo.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare SLO and alert mathematics across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/api_reliability/slo.py` with `capstone/tracks/typescript-fastify/src/reliability/slo.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 08 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
