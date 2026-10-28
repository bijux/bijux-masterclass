# Lab — Stage default deny without erasing dependencies

## Goal

Introduce ingress and egress isolation while preserving only declared Atlas flows.

## Safety boundary

Use only the dependency-light simulator or an isolated disposable cluster. Do not alter shared cluster networking, cloud routes, production DNS, or host firewall state.

## Baseline

Atlas API, internal client, gateway, worker, DNS, and external dependency simulators are reachable. No Pods are isolated.

## Hypothesis

Explicit allow rules followed by default deny will preserve declared flows and reject an undeclared lateral connection; applying deny first will create a wider outage.

## Controlled action

Run `python3 capstone/scripts/network_policy_lab.py`. Compare staged rollout with the planted deny-first sequence and inspect both IPv4 and IPv6 cases.

## Oracle

Gateway/internal-client to API, DNS, and approved dependency flows succeed; lateral attacker and undeclared egress fail. The deny-first mutant loses required dependencies before allows exist.

## Required evidence

Policy selection trace, isolation status, ingress/egress rule matches, denied-flow list, rollout order, and rollback result.

## Interpretation

A safe rollout proves both allowed and denied populations. “The application still works” is not enough because unintended lateral access may remain.

## Cleanup

Run `make clean` and verify generated policy reports are removed.

## Completion gate

All declared dependencies survive, all planted unauthorized flows fail, dual-stack behavior is explicit, and rollback restores the baseline without deleting unrelated policy.
