# Guide — Cost and Quota Safety

Cloud cost and service quotas are part of architecture. They influence which designs are affordable, which replacements are possible, and which failure responses remain available.

## Cost has a shape

A monthly estimate hides the mechanism. Break a design into cost dimensions:

| Dimension | Atlas examples |
|---|---|
| Time-based fixed cost | NAT gateway hours, load-balancer hours, public IPv4 hours |
| Capacity | EBS GiB-month, snapshot GiB-month, object storage |
| Requests | S3 operations, KMS calls, log-delivery requests |
| Data processing | NAT bytes, load-balancer capacity units, log ingestion |
| Data transfer | cross-zone, internet egress, inter-region replication |
| Compute duration | EC2 instance hours, temporary replacement capacity |
| Retention | state versions, audit logs, backups, snapshots |

A “small” instance behind a NAT gateway and load balancer can cost less because of compute than because of the surrounding fixed infrastructure. Conversely, an endpoints-only network can reduce NAT cost but increase endpoint fixed cost and operational complexity. Cost is therefore a design comparison, not a final calculator step.

## Estimate before apply

For each cost-bearing resource, record:

```text
resource class
quantity
region
billing dimension
expected duration
expected traffic or storage
unit-price source date
low / expected / high estimate
owner
cleanup trigger
```

Use a range. Traffic, log volume, snapshots, and retries are uncertain. The course does not turn a local fixture into a provider billing claim; real prices must be checked in the chosen region at execution time.

## Observe after apply

The plan describes intended quantities, not necessarily final charges. After apply:

- enumerate created resources;
- confirm public IPv4 allocation;
- inspect actual volume sizes and snapshot creation;
- confirm whether NAT or endpoint paths carry traffic;
- inspect log destinations and retention;
- record cross-zone placement;
- compare the observed topology with the estimate.

A cost variance can reveal an architecture defect: unexpected cross-zone traffic, duplicate log delivery, a failed replacement leaving both generations active, or an orphaned volume.

## Quotas are preconditions for recovery

Quota analysis is often postponed until scaling. That is too late. A safe replacement can require temporary capacity above steady state:

```text
old instance remains ready
+ new instance boots and becomes healthy
+ both are registered during drain
```

The relevant quota is not only instance count. It can include:

- elastic IPs or public IPv4 addresses;
- load balancers, listeners, target groups, and targets;
- network interfaces;
- EBS volumes and aggregate storage;
- KMS requests or grants;
- route-table or security-group rules;
- API request rate;
- NAT gateways or interface endpoints;
- DNS records and certificate limits.

The capacity record should state current usage, service quota, required temporary addition, and whether the margin is sufficient.

## Cost and quota gates

A release should be classified, not merely annotated:

- **pass** — estimate and quota headroom are within approved bounds;
- **review** — cost grows materially or a quota increase is pending;
- **fail** — the change exceeds budget, has no owner, or cannot fit during safe replacement;
- **not-executed** — cost or quota evidence was unavailable; this is not a pass.

The course release model uses these categories so that a fast or syntactically correct plan cannot conceal unaffordable or unrecoverable infrastructure.

## Cleanup economics

Destroy operations can themselves be delayed or blocked. Examples include non-empty buckets, deletion protection, final snapshots, KMS deletion windows, retained log groups, and dependencies created outside state.

A cleanup plan should distinguish:

- immediate deletion;
- retained evidence with a bounded retention rule;
- resources pending provider-enforced deletion;
- deliberately preserved shared foundation;
- orphaned resources requiring incident ownership.

Every retained cost-bearing object needs a named owner and expiry. “We may need it later” is not a retention policy.

## Useful engineering questions

Before choosing a topology, ask:

1. What is the fixed cost before one request is served?
2. Which costs scale with traffic, data, tenants, or environments?
3. Which failure or retry behavior can amplify cost?
4. Does zonal independence add cross-zone transfer?
5. Can a cheaper design still meet the recovery target?
6. Which quota becomes the first limit during replacement or incident response?
7. Can the platform detect and attribute unexpected spend?

The objective is not minimum cost. It is a justified cost envelope that preserves correctness, recovery, and ownership.
