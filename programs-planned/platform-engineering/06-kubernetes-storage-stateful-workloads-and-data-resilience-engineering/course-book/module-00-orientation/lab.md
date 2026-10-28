# Orientation lab — predecessor integrity and storage-risk inventory

## Goal

Convert the Course 5 handoff into an explicit list of Course 6 obligations before creating any storage object.

## Safety boundary

This lab is read-only. Do not apply manifests or connect to a shared cluster.

## Baseline

Verify every predecessor file against its manifest. Record the inherited Kubernetes, CNI, Gateway, DNS, topology, and policy versions.

## Controlled action

For each handoff statement, classify it as guaranteed, required, deferred, or unresolved. Map each storage destination to the Course 5 egress policy. Identify every place where a stateful workload could report readiness before recovery.

## Oracle

The inventory must contain at least the following unresolved responsibilities: provisioning, binding, attachment, mount, data authority, writer fencing, snapshot consistency, backup independence, restore verification, performance, capacity, and deletion.

## Evidence

Produce `orientation-storage-risk-register.json` in your external evidence directory.

## Cleanup

No cluster resources are created. Remove only temporary parser output.

## Completion gate

The predecessor manifest passes and every deferred Course 5 storage obligation has one Course 6 owner and proof route.
