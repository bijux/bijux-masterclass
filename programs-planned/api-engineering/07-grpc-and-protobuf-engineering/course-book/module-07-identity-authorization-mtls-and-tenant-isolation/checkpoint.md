# Checkpoint — Module 07: Identity, Authorization, mTLS, and Tenant Isolation

## Required result

Implement RPC security profile 1.0 with method policy, workload and user identity binding, tenant-isolation vectors, mTLS-ready configuration, and secure worker-stream authorization.

## Demonstrate

- [ ] Distinguish server tls, mutual tls workload identity, bearer identity, and delegated end-user context.
- [ ] Authenticate callers without trusting arbitrary metadata or network location.
- [ ] Enforce method, tenant, resource, field, and attempt-level authorization.
- [ ] Bind worker sessions and completions to workload identity and lease generation.
- [ ] Protect credentials and authorization context on long-lived streams.
- [ ] Produce cross-language security vectors without leaking secrets in status, metadata, logs, reflection, or traces.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/shared/vectors/security.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/security/method-policy.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-07-security-proof.json` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do internal RPC peers establish workload and delegated user identity, enforce method and resource policy, and protect long-lived streams without treating a private network as trust?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Identity, Authorization, mTLS, and Tenant Isolation** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
