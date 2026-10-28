# Checkpoint — DNS and discovery

## Required evidence

- Service-name matrix by namespace
- search/ndots query expansion trace
- positive and negative cache inventory
- headless versus ClusterIP decision
- dual-stack DNS evidence plan
- completed negative-cache lab

## Decision defense

Defend why restarting CoreDNS may be ineffective when an application retains a valid negative cache entry.

## Progression gate

You may progress only when every required artifact is reproducible from a clean checkout and your explanation separates intent, controller observation, data-plane behavior, and protocol evidence.
