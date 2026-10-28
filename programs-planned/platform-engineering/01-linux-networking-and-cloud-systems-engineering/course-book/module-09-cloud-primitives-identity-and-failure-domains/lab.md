# Lab — Module 09: Cloud Primitives, Identity, and Failure Domains

## Goal

Translate Atlas host requirements into a provider-neutral cloud architecture and reject unsupported availability claims.

## Safety boundary

The default lab is architectural and read-only. Optional cloud inventory must use a least-privilege read identity and an explicit account/project/subscription boundary.

## Baseline

Review the host, network, storage, metadata, and failure-scenario files. Draw the full dependency graph including identity, DNS, load balancer, state, and backup.

## Hypothesis

A valid design maps every host guarantee to a cloud resource or managed capability and names the weakest failure domain.

## Controlled action

Create AWS, GCP, and Azure mappings for the same requirements. Evaluate single-instance, two-instance/single-zone, and multi-zone plans with the classifier. Identify quotas and cost-relevant flows.

## Oracle

No provider name is treated as semantic equivalence; static keys are rejected; single-zone dependencies block zone-tolerance claims; each resource has an owner and evidence route.

## Evidence

Provider comparison, dependency graph, failure-domain decision, IAM plan, quota snapshot, traffic/cost flows, and unresolved provider-specific questions.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Remove exported inventory containing identifiers or redact it according to policy; delete any optional temporary cloud resources and verify billing/resource inventory.

## Completion gate

Defend the availability statement using the weakest critical dependency, not the number of zones shown in a diagram.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
