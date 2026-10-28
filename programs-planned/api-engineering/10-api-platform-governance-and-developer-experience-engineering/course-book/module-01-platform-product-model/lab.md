# Lab 01 — Decide what the platform should own

## Setup

Read `capstone/predecessor/handoff/platform-boundary-brief.yaml` and inspect the
current catalog, registry, runtime policy, and support routes.

## Controlled action

Evaluate six proposed capabilities: contract digest publication, project-owner
authorization in the gateway, documentation search, domain-state repair, sandbox
creation, and consumer retirement tracking. For each, identify the user problem,
authority, repeated cost, central operating cost, and outcome metric.

## Oracle

Digest publication, search, sandbox control, and consumer retirement tracking may
belong to the platform. Project-owner authorization and domain repair remain with
the owning services.

## Required evidence

Create `reports/module-01-platform-product.json` with one decision record per
capability and a reason that names the authority boundary.

## Cleanup

Remove scratch proposals. Rerun `make module-01-proof`.

## Completion gate

Every accepted capability improves a named user journey, and every rejected
capability protects a domain boundary rather than merely reflecting preference.
