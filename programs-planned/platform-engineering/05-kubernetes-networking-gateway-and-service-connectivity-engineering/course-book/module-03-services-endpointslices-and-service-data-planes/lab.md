# Lab — Find the stale Service data plane

## Goal

Prove whether stale traffic is caused by readiness, EndpointSlice generation, or one node’s programmed backend set.

## Safety boundary

Use only the dependency-light simulator or an isolated disposable cluster. Do not alter shared cluster networking, cloud routes, production DNS, or host firewall state.

## Baseline

Three Ready API endpoints are programmed on three nodes. The model exposes desired and observed generations.

## Hypothesis

When one endpoint is withdrawn, a deliberately paused node agent will keep sending new connections to the old endpoint while other nodes converge.

## Controlled action

Run `python3 capstone/scripts/service_convergence_lab.py`, then inspect per-node generations and new versus existing connections.

## Oracle

The controller and EndpointSlice must converge first; exactly one node remains stale; resuming its agent updates only new connection selection.

## Required evidence

Service and slice snapshots, per-node programmed generations, selected endpoint traces, and convergence timeline.

## Interpretation

The repair targets the data-plane reconciler. Recreating the Service or weakening readiness would broaden impact and obscure the actual owner.

## Cleanup

Run `make clean` and confirm generated convergence state is removed.

## Completion gate

The stale node is identified from evidence, existing connections are not misclassified as stale programming, and the permanent repair is defended.
