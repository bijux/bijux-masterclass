# Lab 09 — Reconcile runtime state and product outcomes

## Setup

Run `make runtime-proof`, `make analytics-proof`, and `make support-proof`.

## Controlled action

Add an undocumented gateway route, change domain authorization to the gateway,
and simulate continued traffic on a deprecated version. Then route one contract
question and one portal failure through support.

## Oracle

Runtime drift is visible. Gateway-owned domain authorization is rejected.
Deprecated use appears in migration impact. Support reaches the domain owner for
semantics and the platform owner for portal failure.

## Required evidence

Create `reports/module-09-runtime-product.json` with drift, policy boundary,
consumer outcome metrics, deprecated impact, support owner, and privacy notes.

## Cleanup

Restore desired and current route parity, remove synthetic usage, and rerun
proofs.

## Completion gate

Runtime state, release identity, owner, support, and product outcomes can be
connected without moving business policy or collecting unnecessary personal
data.
