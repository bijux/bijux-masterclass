# Lab 07 — Onboard a consumer without private help

## Setup

Run `make docs-proof` and `make sandbox-proof`. Use a fresh sandbox session and
the checked-in documentation source.

## Controlled action

Act as a consumer who knows only the goal “submit an analysis and retrieve its
artifact.” Use search, interface-selection guidance, the quickstart, sandbox, and
support route. Then break one example version and attempt to import production
data into the sandbox.

## Oracle

The normal path reaches a defined first success. The stale example fails quality
checks. Production data import is rejected. The owner and support path remain
discoverable at every step.

## Required evidence

Write `reports/module-07-onboarding.json` with timestamps, selected interface,
contract version, failure points, first-success duration, search results, and
support handoff.

## Cleanup

Destroy the sandbox session, revoke credentials, restore the example, and rerun
proofs.

## Completion gate

A new consumer can complete the task without undocumented credentials, private
contacts, or production data.
