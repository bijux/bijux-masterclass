# Checkpoint — Identity, Authorization, mTLS, and Tenant Isolation

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/shared/vectors/security.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/security/method-policy.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-07-security-proof.json` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do internal RPC peers establish workload and delegated user identity, enforce method and resource policy, and protect long-lived streams without treating a private network as trust?**
- [ ] Identify one tempting but incorrect implementation and the failure it causes.
- [ ] State which property is not established by the dependency-light proof.
- [ ] Compare Python and TypeScript boundary behavior without demanding identical internals.

## Non-compensable gate

No RPC may rely on network location or caller-supplied identity metadata, and every durable effect must be authorized by workload, delegated principal where applicable, tenant, resource, and current attempt state.

Record the result in your learning journal before proceeding.
