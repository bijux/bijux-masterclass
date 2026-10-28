# Lab — Connectivity release game day

## Goal

Use the evidence map to diagnose seven failures without random restarts or broad policy removal.

## Safety boundary

Use the dependency-light model or an isolated disposable cluster. Do not alter shared load balancers, DNS zones, cloud routes, certificates, or production egress policy.

## Baseline

Atlas semantic and local network lanes are green. Each fault has a bounded injector and a known cleanup action.

## Hypothesis

The earliest-failed-transition method will identify route, service-programming, DNS cache, policy, route attachment, TLS, and egress failures from distinct evidence.

## Controlled action

Run `python3 capstone/scripts/final_game_day.py`. Diagnose each scenario before revealing its injected fault label.

## Oracle

Each scenario maps to one earliest failed transition and one owning component. Cleanup restores the exact baseline after every scenario.

## Required evidence

Incident timeline, evidence queries, first failed transition, owner, repair, cleanup proof, and residual evidence boundary for all seven scenarios.

## Interpretation

The exercise is failed if the learner uses deletion/restart as the primary diagnosis, weakens default deny, disables TLS, or classifies unavailable cluster evidence as passed.

## Cleanup

Run `make clean`, execute `make core-proof`, and verify manifests.

## Completion gate

All seven incidents are correctly located, all planted shortcuts are rejected, the release candidate is classified, and the Course 6 handoff verifies exactly.
