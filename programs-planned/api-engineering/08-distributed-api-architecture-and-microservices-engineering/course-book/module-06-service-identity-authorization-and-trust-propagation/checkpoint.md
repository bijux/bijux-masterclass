# Checkpoint — Module 06: Service Identity, Authorization, and Trust Propagation

## Required result

Introduce workload identities, audience-bound service credentials, delegated user context, short-lived artifact capabilities, and explicit authorization at every trust boundary.

## Demonstrate

- [ ] Separate workload identity, end-user identity, tenant context, and delegated authority.
- [ ] Design service-to-service authentication without treating network location as trust.
- [ ] Prevent confused-deputy and privilege-amplification failures.
- [ ] Mint and verify narrow, short-lived capability tokens for artifact transfer.
- [ ] Propagate only bounded non-sensitive context across services.
- [ ] Define network policy as defense in depth rather than application authorization.

## Commands

```bash
make core-proof
```

## Evidence to retain

- [ ] `capstone/architecture/security-policy.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-06-security-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/topology/kubernetes/network-policy.yaml` exists, is reproducible, and you can explain its oracle.

## Defend the design

1. Answer the central question in one paragraph: How do services authenticate workloads, preserve end-user intent, and avoid confused-deputy failures without trusting caller-supplied identity headers?
2. Name the authoritative owner and smallest counterexample.
3. State what the available evidence does not prove.

## Continue only when

Continue only after you can demonstrate the **Service Identity, Authorization, and Trust Propagation** increment, preserve the controlled counterexample as a regression, keep inherited checkpoints green, and explain which stronger claim remains outside the evidence you collected.
