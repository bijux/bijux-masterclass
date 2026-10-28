# Guide — Cloud Account Safety

A real-cloud laboratory begins with authority, cost, and reversibility—not with a resource block. The safest plan can still be dangerous when it targets the wrong account, a shared production region, or an identity with authority far beyond the exercise.

## The minimum sandbox contract

Before a cloud command is run, write down:

| Property | Required evidence |
|---|---|
| Account purpose | A disposable learning or engineering sandbox, not production |
| Account identity | Exact 12-digit account ID observed from the active session |
| Region | One declared region; additional regions are denied or explicitly reviewed |
| Operator | Named federated identity with a short session |
| Owner | Person or team responsible for resources left behind |
| Budget | Expected maximum cost, low-threshold alert, and stop condition |
| Teardown deadline | Absolute date and time, including timezone |
| Naming boundary | Prefix and tags that distinguish course resources |
| Recovery path | Who can regain access if the ordinary operator session fails |

A shell profile name such as `sandbox` is not evidence. Profiles are local aliases and can be misconfigured. The preflight must query the active cloud identity and compare it with the declared account ID.

## Prefer short-lived federation

Use IAM Identity Center or another approved federation mechanism. Do not create a long-lived access key merely to make a provider work. Short-lived credentials reduce persistence after accidental disclosure and make session identity visible in audit records. They do not eliminate risk: a short session with organization-administrator authority can still cause severe damage.

Keep credentials out of:

- HCL and variable files;
- backend configuration committed to source;
- shell history;
- saved plans and state;
- user data and machine images;
- lab evidence bundles;
- screenshots and copied terminal transcripts.

The provider should obtain credentials from the normal credential chain. Course scripts may inspect caller identity, but they never print secret material.

## Bound the authority, not only the resources

A prefix and tags help inventory and cleanup. They are not authorization controls unless a policy explicitly evaluates them and the tag cannot be changed by the same principal to escape the boundary.

A course apply role should normally be unable to:

- create IAM users or access keys;
- alter the organization or management account;
- disable authoritative audit delivery;
- modify unrelated DNS zones or certificates;
- create unrestricted administrator policies;
- change state-backend or recovery-key ownership;
- launch unbounded compute fleets;
- use regions outside the declared lane.

Some modules legitimately create workload roles or KMS keys. That authority should be limited to the sandbox account and governed naming/resource patterns, and it should be exercised only by the apply identity—not by the Atlas runtime role.

## Separate planning from applying

Planning often needs read access plus the ability to resolve data sources. Applying needs mutation authority. Using one broad identity for both stages makes review evidence weaker: the reviewer cannot distinguish the code that proposed a change from the identity that executed it.

A stronger path is:

```text
source review
→ read-oriented planning identity
→ saved plan bound to account, region, state, and provider lock
→ approval
→ narrowly scoped apply identity
→ post-apply observation
```

The apply identity should be usable only in the intended pipeline or controlled operator path, and its session should expire quickly.

## Cost and quota guardrails

Safety includes economic damage. NAT gateways, public IPv4 addresses, load balancers, log ingestion, snapshots, and forgotten block volumes can continue charging after the exercise appears complete. Before apply, estimate quantities and duration. During cleanup, enumerate actual resources rather than assuming a successful destroy removed everything.

Quotas are safety boundaries too. A replacement may need temporary duplicate instances, addresses, targets, or volumes. A plan that cannot fit inside quota may fail after disrupting the old resource.

## DNS and certificate boundaries

Do not use a production DNS zone, certificate, or public hostname for a course lab. DNS records can redirect real traffic; certificate validation can affect domain ownership workflows. Use a dedicated subdomain or a private/local test name, and record who owns removal.

## Teardown is a verified operation

A cleanup command is not proof of cleanup. The teardown record should include:

1. the destroy or deletion result;
2. a provider inventory query for resources with the course prefix/tags;
3. checks for detached volumes, snapshots, elastic IPs, load balancers, NAT gateways, log groups, object buckets, and KMS keys pending deletion;
4. a cost-bearing-resource exception list, each with owner and expiry;
5. confirmation that state and evidence retained for learning contain no credentials or secrets.

A failed teardown is an incident, not an administrative inconvenience. Stop creating new resources until ownership is restored.

## Decision rule

Do not enter the real-cloud lane unless you can answer all five questions:

- Which account and region will receive the change?
- Which identity will plan and which will apply?
- What is the maximum credible blast radius?
- What continuing cost can remain after failure?
- Who can recover or delete the resources if the normal path stops working?

If any answer is unknown, remain in the dependency-light or local OpenTofu lane. That is an honest evidence boundary, not incomplete learning.
