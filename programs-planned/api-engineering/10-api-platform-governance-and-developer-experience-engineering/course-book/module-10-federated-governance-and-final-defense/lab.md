# Lab 10 — Defend Analysis API Platform 1.0

## Setup

Run all focused proofs and inspect the final rubric. Start the loopback platform
laboratory.

## Controlled action

Perform two journeys:

1. A new consumer discovers Analysis HTTP API 1.2, creates a sandbox, reaches
   first success, and finds support.
2. An owner proposes a new API surface, generates the golden path, publishes a
   contract candidate, receives policy results, and attempts activation.

Then attempt an immutable-release overwrite, an expiry-free exception, unsafe
retirement, untraceable SDK publication, and gateway-owned domain policy.

## Oracle

Valid journeys complete with bounded evidence. Every unsafe candidate is rejected
at the earliest authoritative gate. Review-required evidence remains review; it
is not silently promoted.

## Required evidence

Produce `reports/module-10-final-defense.json` and a short architecture decision
record covering platform boundaries, residual risk, platform SLOs, adoption
measures, and the next operating review.

## Cleanup

Stop the network laboratory, remove sessions and generated outputs, run `make
clean`, then execute `make core-proof` and `make manifest-proof` from the clean
tree.

## Completion gate

You can defend the platform from all five perspectives—consumer, owner, reviewer,
operator, and platform product owner—and every claim names its evidence class.
