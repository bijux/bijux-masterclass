# Guide — How to Read an Infrastructure Plan

Do not review a plan by scanning only the summary line. `12 to add, 1 to change, 0 to destroy` says nothing about whether the target is correct, whether one “change” replaces a durable object, or whether the resulting service will work.

A serious review proceeds in layers.

## 1. Establish plan identity

Before reading actions, verify:

```text
source commit or digest
root stack
input-set digest
backend key and workspace
state lineage and serial
target account and region
caller identity class
OpenTofu version
provider lock digest
module versions
plan creation time and expiry
```

If these facts are missing, the plan is not reviewable. A correct plan for another account is still the wrong plan.

## 2. Read resource addresses as identities

For every action, ask whether the resource address is stable. Address changes caused by renaming, moving into a module, changing `count` indices, or replacing semantic map keys can create destroy/create actions even when the intended remote object is unchanged.

Classify address transitions:

- intentional new object;
- intentional retirement;
- identity-preserving move;
- import/adoption;
- accidental churn;
- transfer to another state owner.

A state move should have an explicit mapping and migration evidence. Do not accept replacement merely because it is easy to apply.

## 3. Explain the action mechanism

For each create, update, replacement, delete, read, import, move, or forget operation, record the cause. Replacement deserves special attention:

- Which attribute is force-new?
- Is it provider behavior or a deliberate lifecycle choice?
- Does create-before-destroy actually fit quota and dependency constraints?
- Can the old and new generations coexist?
- Is durable state attached to only one generation?
- What happens if the new object never becomes ready?

The answer “OpenTofu says it must replace” is incomplete. The provider schema and remote API semantics determine why.

## 4. Inspect unknown values

Unknown values are expected when an object does not yet exist. They become review blockers when they control:

- public exposure;
- principal or resource authority;
- encryption or key selection;
- destructive behavior;
- routing destination;
- retention or deletion;
- cost-bearing quantity.

Ask whether the design can make the value known earlier. If not, define an apply-time policy or post-apply gate and state the residual risk.

## 5. Follow dependency consequences

A broad `depends_on` can serialize unrelated work and propagate unknown values. A hidden dependency can allow a resource to be created before a required policy or data path exists.

Trace:

```text
resource changed
→ dependants recreated or delayed
→ temporary coexistence or outage
→ quota and cost impact
→ rollback path
```

A narrow plan can have a wide operational consequence.

## 6. Review authority

Which identity will execute the apply? Does the reviewed plan require permissions beyond the intended apply role? Does it create or modify identities that could later exceed the foundation boundary?

Inspect separately:

- role trust;
- permission policy;
- resource policy;
- KMS key policy;
- organization ceiling;
- session or permission boundary;
- endpoint policy where relevant.

A plan that introduces wildcard authority or allows the workload to mutate its own foundation should fail even if no immediate exploit is visible.

## 7. Review network behavior as flows

For route, security, DNS, load-balancer, or endpoint changes, write the affected flows:

```text
source identity/address
source subnet and route table
destination name/address
gateway or endpoint
security decisions
TLS authority
expected response
```

Flag new default routes, public addresses, internet gateways, broad CIDRs, unrestricted egress, DNS-zone changes, and certificate changes. A new endpoint can change both routing and authorization.

## 8. Review durable data and recovery

For buckets, databases, volumes, snapshots, audit logs, state, and keys, ask:

- Is this create, replace, transfer, or destroy?
- What protects it from accidental deletion?
- Does a backup exist, and has restore been tested?
- Does the recovery identity still have key access?
- Does lifecycle expiration match the retention requirement?
- Can rollback read the new schema or data format?

A destroy followed by recreation is not harmless because the resource name is the same.

## 9. Review cost and quota

Record new fixed costs, traffic costs, retention, and temporary replacement capacity. Verify quotas for the maximum overlap during rollout, not only steady state.

A plan that requires one extra public address or volume can fail after the old object has begun draining if quota headroom was assumed.

## 10. Define post-apply evidence

A plan is a proposal. Approval should name the observations required after apply:

- provider/control-plane state;
- route and security behavior;
- target health and readiness;
- DNS and TLS correctness;
- successful Atlas job;
- negative reachability;
- backup and restore evidence;
- cleanup or retained-resource ownership.

The apply is not complete until those gates pass or the release is explicitly classified as failed or incomplete.

## A compact review table

| Address | Action | Cause | Risk | Required approval | Post-apply oracle |
|---|---|---|---|---|---|
| `module.network.aws_route.private_default["private-a"]` | update | NAT target changes | egress interruption | network owner | S3 and required external dependency checks |
| `module.data.aws_ebs_volume.atlas` | replace | AZ changes | data loss/attachment gap | data owner | restore and result-integrity proof |
| `module.identity.aws_iam_role_policy.runtime` | update | prefix widened | privilege expansion | security owner | positive and forbidden API calls |

A plan review is complete when every material action has an owner, mechanism, acceptable risk, and observable outcome—not when the summary contains zero destroys.
