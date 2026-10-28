# Checkpoint — Services and EndpointSlices

## Required evidence

- Service/EndpointSlice/Pod join table
- service data-plane implementation inventory
- new versus existing connection evidence
- NodePort/LoadBalancer source-address map
- endpoint-convergence timeline
- completed stale-data-plane lab

## Decision defense

Defend why a healthy Service object and EndpointSlice population still do not prove every Node can translate traffic correctly.

## Progression gate

You may progress only when every required artifact is reproducible from a clean checkout and your explanation separates intent, controller observation, data-plane behavior, and protocol evidence.
