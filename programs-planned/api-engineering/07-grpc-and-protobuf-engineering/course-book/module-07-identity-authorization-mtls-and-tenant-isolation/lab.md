# Lab — Defend unary and streaming RPCs against identity and tenant confusion

**Module:** Identity, Authorization, mTLS, and Tenant Isolation

## Objective

Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization.

## Setup

Use fixture workload and delegated-user credentials with an injected clock. Enable the mTLS configuration check; run live certificate tests only when the required local certificate tooling is available.

## Controlled actions

1. Call each method with valid workload/user combinations and record policy decisions.
2. Attempt raw user and tenant metadata forgery without valid delegation.
3. Use valid scopes against a resource in another tenant.
4. Open a worker stream with one identity and submit a result for another worker's assignment.
5. Expire and revoke credentials during WatchRun and Work sessions.
6. Exercise old/new key overlap, unknown key identifiers, and certificate-name mismatch.

## Correctness oracle

Only explicitly allowed workload/delegation/method/resource combinations reach application effects. Cross-tenant and stale-attempt calls reveal no protected data. Long-lived streams obey freshness policy, and no report or status leaks credentials.

## Required evidence

- `capstone/shared/vectors/security.json`
- `capstone/security/method-policy.yaml`
- `reports/module-07-security-proof.json`

## Cleanup

Destroy ephemeral fixture keys and certificates outside the checked-in test set, close streams, reset the injected clock and revocation set, and run the secret scan.

## Completion gate

No RPC may rely on network location or caller-supplied identity metadata, and every durable effect must be authorized by workload, delegated principal where applicable, tenant, resource, and current attempt state.

A successful command without this evidence does not complete the lab.
