# Worked Answers — Module 09: Cloud Primitives, Identity, and Failure Domains

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — Cloud characteristics

Cloud also involves self-service, pooled resources, elasticity, measured service, identity, quotas, automation, and managed control planes. One VM may use cloud infrastructure without a reproducible or scalable platform. Course 2 turns requirements into governed state and reviewable changes.

## Exercise 2 — Zone claim

It can tolerate one instance process or VM failure if the other can access required state and traffic. It cannot claim tolerance of the disk's zone loss. The durable dependency remains single-zone. Availability claims follow the weakest critical dependency.

## Exercise 3 — Provider map

The names describe analogous virtual-network concepts but differ in scope, subnet regionality, route behavior, firewall attachment, peering, defaults, and service integration. Use the map to locate documentation, then model provider-specific semantics and test live state. Portability is requirements-level, not name-level equivalence.

## Exercise 4 — Workload identity

The platform issues short-lived credentials to a named workload identity, reducing distribution and rotation burden and improving attribution. It does not protect against a compromised process using the identity. Scope permissions and restrict metadata access.

## Exercise 5 — Block versus object

Object storage exposes an object API with its own consistency, conditional update, and naming semantics. FUSE adapters may emulate files but cannot universally reproduce local filesystem locking, atomic rename, or durability. Design to the native API or verify the adapter's exact guarantees.

## Exercise 6 — Managed responsibility

The consumer still owns schema and data correctness, access policy, network exposure, configuration, capacity class, backup retention, restore testing, compatibility, cost, and incident response. Managed operation transfers tasks but does not eliminate application or governance responsibility.

## Exercise 7 — Control-plane outage

Existing data-plane resources—VMs, load balancer, disks—may continue operating while provisioning or modification APIs are unavailable. The incident limits scaling, replacement, or policy changes. Monitor both planes and maintain capacity/recovery headroom.

## Exercise 8 — Quota failure

Replacement or scale-out can fail exactly when demand or failure requires it. Account and regional quotas may differ from theoretical service capacity. Record required headroom and automate quota evidence. A design with no allocatable capacity is not recoverable.

## Exercise 9 — Metadata boundary

If the service can be induced to fetch arbitrary URLs, it may reach the link-local metadata endpoint and return short-lived workload credentials. Require provider-specific metadata protections, restrict egress/proxying, and avoid broad instance permissions. Application URL validation alone may be insufficient.

## Exercise 10 — Cost flow

Cross-zone service-to-service traffic and internet/object-storage egress can be billed. Load balancer processing, public IPv4, logs, snapshots, and NAT gateways also matter. Course 1 records flows; Course 2 estimates provider costs and tests architecture alternatives.

## Exercise 11 — Shared responsibility

Providers secure defined infrastructure layers; consumers configure identities, data, networks, workloads, and service options. The boundary differs by service model. A platform engineer must map each control to an owner and evidence source rather than cite the slogan.

## Exercise 12 — Handoff test

It states observable requirements—replaceable compute, private API, TLS edge, workload identity, durable state, backup boundary, metadata restrictions, zone-claim evidence—without prescribing resource names. Course 2 can map each requirement to the selected provider and prove it, while unsupported changes require explicit revision.
