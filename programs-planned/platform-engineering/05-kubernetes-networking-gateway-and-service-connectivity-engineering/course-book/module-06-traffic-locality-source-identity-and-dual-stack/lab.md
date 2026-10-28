# Lab — Survive a zone-local endpoint loss

## Goal

Measure preference, hard locality, and stale-hint behavior during one-zone endpoint loss.

## Safety boundary

Use the dependency-light model or an isolated disposable cluster. Do not alter shared load balancers, DNS zones, cloud routes, certificates, or production egress policy.

## Baseline

Two zones have clients and API endpoints for IPv4 and IPv6. Locality preference is enabled with healthy fallback.

## Hypothesis

Preference will fall back to remote endpoints; hard Local policy will reject; a stale-hint mutant will continue selecting removed local endpoints.

## Controlled action

Run `python3 capstone/scripts/locality_failure_lab.py` and compare the three policies by address family.

## Oracle

The report must distinguish intended rejection from implementation staleness and show bounded fallback for preference policy.

## Required evidence

Selected endpoint, excluded population, family, zone, source-address observation, failure reason, and transition time.

## Interpretation

A faster local path is acceptable only when failure behavior is part of the contract. Stale hints and hard-local rejection are different incidents.

## Cleanup

Run `make clean` and remove generated locality reports.

## Completion gate

Both families are tested, fallback is bounded, hard policy is reported honestly, and stale selection is rejected.
