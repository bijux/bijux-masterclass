# Reference — Plan Review Checklist

Use this checklist after establishing plan identity and before approval. It is a prompt for reasoning, not a replacement for architecture judgment.

## Target and dependency identity

- [ ] source commit or tree digest is recorded;
- [ ] root stack and input digest are recorded;
- [ ] target account, region, and caller identity match the declared environment;
- [ ] backend key, workspace, lineage, and serial are expected;
- [ ] OpenTofu and provider versions match the lock and release policy;
- [ ] module versions and sources are immutable or otherwise governed;
- [ ] the saved-plan digest and expiry are recorded.

Reject a plan whose target or dependency identity cannot be established.

## Resource identity and lifecycle

- [ ] every new address represents an intended new object;
- [ ] address renames have `moved` mappings;
- [ ] imported objects have complete configuration and ownership;
- [ ] `count`/`for_each` key changes do not create accidental churn;
- [ ] every replacement has an identified force-new cause;
- [ ] durable data is not destroyed or transferred without owner approval;
- [ ] create-before-destroy fits coexistence, quota, and dependency constraints;
- [ ] ignored attributes have an explicit external owner;
- [ ] prevent-destroy is not treated as the only retention control.

## Identity and security

- [ ] no workload role gains foundation mutation authority;
- [ ] role trust and permissions are reviewed separately;
- [ ] wildcard actions/resources are justified or rejected;
- [ ] encryption and key policies remain enabled;
- [ ] secret values do not enter HCL, plans, state, or user data;
- [ ] IMDSv2/token requirements remain enforced;
- [ ] public exposure expansion is explicit;
- [ ] account, tenant, environment, and resource-prefix conditions remain bounded;
- [ ] audit and log-delivery authority remains outside workload control.

## Network and edge

- [ ] CIDRs are contained and non-overlapping;
- [ ] zone identities map correctly in the target account;
- [ ] every subnet has an explicit route table;
- [ ] new default routes and gateways are explained;
- [ ] data tiers do not gain unintended internet access;
- [ ] security-group rules match named source/destination flows;
- [ ] DNS and certificate authority changes have owners;
- [ ] health checks reflect readiness, not every optional dependency;
- [ ] draining and timeout budgets remain compatible;
- [ ] IPv4 and IPv6 policy changes are reviewed independently.

## Data, backup, and recovery

- [ ] state backend locking, versioning, encryption, and recovery remain intact;
- [ ] bucket/object/volume/snapshot retention matches policy;
- [ ] KMS key deletion or policy changes receive explicit review;
- [ ] backup manifests and restore paths remain usable;
- [ ] RPO/RTO claims are supported by observation or labelled targets;
- [ ] state/data migrations have an expand–transition–contract plan;
- [ ] a rollback or forward-repair decision exists before destructive transition.

## Cost, quota, and operations

- [ ] cost-bearing resource quantity and duration are estimated;
- [ ] cross-zone and internet-transfer implications are known;
- [ ] temporary replacement capacity fits quotas;
- [ ] cleanup and retained-resource ownership are defined;
- [ ] unknown values in policy-critical fields are blocked or gated;
- [ ] partial-apply and recovery runbooks cover the change;
- [ ] monitoring/audit evidence will reveal success or failure.

## Post-apply gates

Approval names the required observations:

- [ ] provider/control-plane objects match the approved design;
- [ ] DNS and TLS resolve to the intended edge;
- [ ] target health and Atlas readiness pass;
- [ ] required flows succeed and forbidden flows fail;
- [ ] workload identity succeeds only on required API calls;
- [ ] durable data survives the intended replacement;
- [ ] backup restore and integrity proof pass where affected;
- [ ] costs/quotas/cleanup are reconciled;
- [ ] state serial advances and no unexplained drift remains.

## Decision

Classify the plan:

```text
pass              evidence and ownership are complete
review            bounded issue needs named expert/owner decision
fail              non-compensable safety or correctness condition
not-executed      required evidence was unavailable; never counted as pass
```

A plan with zero deletes can still fail. A plan with a deliberate, recoverable replacement can pass. The decision follows the mechanism and evidence, not the action count.
