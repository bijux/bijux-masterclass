# Lab — Defend unary and streaming RPCs against identity and tenant confusion

> **Module 07:** Identity, Authorization, mTLS, and Tenant Isolation

## Objective

Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization.

## Why this lab matters

This lab turns the module’s governing question—**How do internal RPC peers establish workload and delegated user identity, enforce method and resource policy, and protect long-lived streams without treating a private network as trust?**—into a falsifiable experiment. The RPC catalogue declares every method, allowed caller workloads, required user scopes or service roles, tenant source, resource action, and whether delegation is allowed. A method absent from policy is denied. Adding a method therefore requires a security review rather than inheriting permissive defaults.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

Use fixture workload and delegated-user credentials with an injected clock. Enable the mTLS configuration check; run live certificate tests only when the required local certificate tooling is available.

## Hypothesis

The clean implementation should satisfy this claim: **Only explicitly allowed workload/delegation/method/resource combinations reach application effects. Cross-tenant and stale-attempt calls reveal no protected data. Long-lived streams obey freshness policy, and no report or status leaks credentials.** When the lab introduces this fault—**Expire and revoke credentials during WatchRun and Work sessions**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Call each method with valid workload/user combinations and record policy decisions.
2. Attempt raw user and tenant metadata forgery without valid delegation.
3. Use valid scopes against a resource in another tenant.
4. Open a worker stream with one identity and submit a result for another worker's assignment.
5. Expire and revoke credentials during WatchRun and Work sessions.
6. Exercise old/new key overlap, unknown key identifiers, and certificate-name mismatch.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Expire and revoke credentials during WatchRun and Work sessions**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

Only explicitly allowed workload/delegation/method/resource combinations reach application effects. Cross-tenant and stale-attempt calls reveal no protected data. Long-lived streams obey freshness policy, and no report or status leaks credentials.

## Required evidence

- `capstone/shared/vectors/security.json`
- `capstone/security/method-policy.yaml`
- `reports/module-07-security-proof.json`

## Interpretation and defense

1. Which state or effect is authoritative for **Identity, Authorization, mTLS, and Tenant Isolation**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Expire and revoke credentials during WatchRun and Work sessions** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

Destroy ephemeral fixture keys and certificates outside the checked-in test set, close streams, reset the injected clock and revocation set, and run the secret scan.

## Completion gate

No RPC may rely on network location or caller-supplied identity metadata, and every durable effect must be authorized by workload, delegated principal where applicable, tenant, resource, and current attempt state.

A successful command without this evidence does not complete the lab.

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Identity, Authorization, mTLS, and Tenant Isolation**. A green command without the negative case and causal explanation does not satisfy this gate.
