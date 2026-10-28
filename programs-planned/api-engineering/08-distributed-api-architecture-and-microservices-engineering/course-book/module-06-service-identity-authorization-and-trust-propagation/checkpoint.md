# Checkpoint — Service Identity, Authorization, and Trust Propagation

Do not continue until every item is satisfied.

## Required evidence

- [ ] `capstone/architecture/security-policy.yaml` exists, is reproducible, and you can explain its oracle.
- [ ] `reports/module-06-security-proof.json` exists, is reproducible, and you can explain its oracle.
- [ ] `capstone/topology/kubernetes/network-policy.yaml` exists, is reproducible, and you can explain its oracle.

## Required explanation

- [ ] Answer the governing question: **How do services authenticate workloads, preserve end-user intent, and avoid confused-deputy failures without trusting caller-supplied identity headers?**
- [ ] Identify one tempting but rejected design and the failure it creates.
- [ ] State what the dependency-light proof does not establish.
- [ ] Compare Python and TypeScript behavior without demanding identical internals.

## Non-compensable gate

All hostile capability cases are rejected and owner-side authorization remains decisive.
