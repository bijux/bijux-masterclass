# Lab — Distinguish a route failure from an MTU black hole

## Goal

Locate the earliest failed transition for two incidents that both appear as timeouts.

## Safety boundary

Use only the dependency-light simulator or an isolated disposable cluster. Do not alter shared cluster networking, cloud routes, production DNS, or host firewall state.

## Baseline

The dependency-light topology has two Nodes, three API endpoints, a valid Service path, and a 1500-byte underlay. Small and large probes initially succeed.

## Hypothesis

Removing a remote Pod route will prevent all packets to that endpoint; reducing effective tunnel headroom without adjusting Pod MTU will allow small packets and fail larger packets.

## Controlled action

Run `python3 capstone/scripts/packet_path_lab.py`. Inspect the generated route candidates, packet-size outcomes, and trace ledger before reading the injected defect labels.

## Oracle

The route defect must fail both small and large probes before transport. The MTU defect must allow small transport and fail only above the calculated effective MTU.

## Required evidence

`capstone/reports/generated/module-01-packet-path.json`, including selected routes, effective MTU, first failed transition, and a written comparison.

## Interpretation

A correct diagnosis explains why application readiness and Service membership remain true in both cases and why deleting a Pod would not repair the underlying guarantee.

## Cleanup

Run `make clean` and confirm generated reports are removed.

## Completion gate

Both incidents are classified correctly, and your report names the layer, owner, falsifying evidence, and permanent repair.
