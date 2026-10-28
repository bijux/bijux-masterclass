# Lab — Remove implicit trust from the service network

> **Module 06:** Service Identity, Authorization, and Trust Propagation

## Objective

Enforce workload identity, delegated user intent, tenant isolation, and narrow artifact capabilities.

## Why this lab matters

This lab turns the module’s governing question—**How do services authenticate workloads, preserve end-user intent, and avoid confused-deputy failures without trusting caller-supplied identity headers?**—into a falsifiable experiment. Workload identity — the calling process or service instance. End-user identity — the human or client application whose intent initiated the action. Tenant context — the isolation domain in which the resource exists. Delegated authority — the exact action the caller may perform on the user’s behalf.

It advances the cumulative Analysis Runs Platform by requiring this result: **Introduce workload identities, audience-bound service credentials, delegated user context, short-lived artifact capabilities, and explicit authorization at every trust boundary**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Load the Course 3 security profile, Course 7 RPC method policy, and Course 8 service ownership map.

## Hypothesis

The clean implementation should satisfy this claim: **Only the intended workload and tenant can perform the bounded action; network location and unsigned headers never establish authority.** When the lab introduces this fault—**Remove any authorization dependency on caller-supplied identity headers**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Mint a run-attempt-scoped upload capability with audience, tenant, checksum, size, and expiry.
2. Attempt wrong audience, wrong tenant, expired, tampered, oversized, and wrong-checksum use.
3. Remove any authorization dependency on caller-supplied identity headers.
4. Compare network-policy reachability with owner-side resource authorization.
5. Run `make security-proof` and inspect the shared Python/TypeScript vectors.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove any authorization dependency on caller-supplied identity headers**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Enforce workload identity, delegated user intent, tenant isolation, and narrow artifact capabilities**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Only the intended workload and tenant can perform the bounded action; network location and unsigned headers never establish authority.

## Required evidence

- `capstone/architecture/security-policy.yaml`
- `reports/module-06-security-proof.json`
- `capstone/topology/kubernetes/network-policy.yaml`

## Interpretation and defense

1. Which state or effect is authoritative for **Service Identity, Authorization, and Trust Propagation**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove any authorization dependency on caller-supplied identity headers** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Revoke fixture capabilities, clear one-time consumption state, and restore canonical policies.

## Completion gate

All hostile capability cases are rejected and owner-side authorization remains decisive.

A successful command without the required evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Service Identity, Authorization, and Trust Propagation**. A green command without the negative case and causal explanation does not satisfy this gate.
