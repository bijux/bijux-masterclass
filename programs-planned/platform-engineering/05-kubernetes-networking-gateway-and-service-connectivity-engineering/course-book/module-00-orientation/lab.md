# Orientation lab — inventory the inherited connectivity contract

## Goal

Convert the Course 4 handoff into a packet-path and ownership inventory without changing the predecessor.

## Safety boundary

Use only the copied handoff, local files, and dependency-light commands. Do not apply manifests to a shared cluster.

## Baseline

Run `make predecessor-proof` and record the verified file count and manifest digest. Read every handoff file once.

## Hypothesis

The predecessor is sufficient to define the workload endpoints and readiness contract, but insufficient to claim a working CNI, Service data plane, DNS, policy, Gateway, TLS lifecycle, or egress path.

## Controlled action

Create three ledgers: direct Pod, Service, and public Gateway. For every transition record owner, desired state, observed state available now, and missing evidence.

## Oracle

The ledgers preserve all Course 4 requirements, contain no invented implementation, and label every unavailable proof as missing or not executed.

## Required evidence

- predecessor proof output;
- three path diagrams;
- address-domain inventory;
- tool/evidence matrix;
- list of Course 5 decisions still open.

## Interpretation

Explain why readiness, image integrity, and correct Kubernetes workload objects are necessary but insufficient network evidence.

## Cleanup

Remove only generated orientation reports. Re-run `make predecessor-proof` to prove the handoff is unchanged.

## Completion gate

Progress only when another learner can use your ledger to identify where CNI, Service, DNS, policy, Gateway, and TLS evidence will later attach.
