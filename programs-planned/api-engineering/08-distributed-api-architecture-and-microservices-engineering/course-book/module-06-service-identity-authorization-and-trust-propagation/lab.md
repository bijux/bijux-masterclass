# Lab — Remove implicit trust from the service network

**Module:** Service Identity, Authorization, and Trust Propagation

## Objective

Enforce workload identity, delegated user intent, tenant isolation, and narrow artifact capabilities.

## Setup

Load the Course 3 security profile, Course 7 RPC method policy, and Course 8 service ownership map.

## Controlled actions

1. Mint a run-attempt-scoped upload capability with audience, tenant, checksum, size, and expiry.
2. Attempt wrong audience, wrong tenant, expired, tampered, oversized, and wrong-checksum use.
3. Remove any authorization dependency on caller-supplied identity headers.
4. Compare network-policy reachability with owner-side resource authorization.
5. Run `make security-proof` and inspect the shared Python/TypeScript vectors.

## Correctness oracle

Only the intended workload and tenant can perform the bounded action; network location and unsigned headers never establish authority.

## Required evidence

- `capstone/architecture/security-policy.yaml`
- `reports/module-06-security-proof.json`
- `capstone/topology/kubernetes/network-policy.yaml`

## Cleanup

Revoke fixture capabilities, clear one-time consumption state, and restore canonical policies.

## Completion gate

All hostile capability cases are rejected and owner-side authorization remains decisive.

A successful command without the required evidence does not complete the lab.
