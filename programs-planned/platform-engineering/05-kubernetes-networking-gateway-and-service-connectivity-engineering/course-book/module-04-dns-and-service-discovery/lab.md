# Lab — Diagnose a negative-cache outage

## Goal

Separate authoritative record publication from node and process cache behavior.

## Safety boundary

Use only the dependency-light simulator or an isolated disposable cluster. Do not alter shared cluster networking, cloud routes, production DNS, or host firewall state.

## Baseline

The authoritative model initially has no `atlas-api` record. A client and node cache both query and retain NXDOMAIN.

## Hypothesis

Creating the Service will fix authoritative answers immediately, but the original client will remain broken until the negative entry expires or is invalidated.

## Controlled action

Run `python3 capstone/scripts/dns_cache_lab.py` and query with the original client, a fresh client, and the authoritative server at controlled times.

## Oracle

Fresh authoritative/fresh-client queries succeed after creation; the original cached client fails until its own negative TTL expires.

## Required evidence

Query expansion trace, cache layers and expiries, authoritative records, and a remediation decision that does not rely on restarting every DNS component.

## Interpretation

The incident demonstrates that “DNS is down” is not a diagnosis. Identify the stale cache owner and the startup or retry behavior that made the stale answer harmful.

## Cleanup

Run `make clean`; verify generated cache snapshots are removed.

## Completion gate

The report identifies authoritative, node-cache, and process-cache truth separately and proposes a bounded permanent repair.
