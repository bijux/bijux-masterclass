# Module 09 — Cloud Primitives, Identity, and Failure Domains

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** Which cloud resources and trust boundaries are required to preserve the host guarantees without copying one provider’s vocabulary into the architecture?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Publish provider-neutral compute, identity, network, storage, DNS, load-balancing, metadata, quota, and failure-domain requirements for Course 2.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Use the NIST cloud characteristics and service models without reducing cloud to “someone else’s server.”
- Map regions, zones, virtual networks, subnets, routes, security controls, and managed services across providers.
- Use workload identity and metadata services without storing static cloud keys on the host.
- Separate block, object, and ephemeral storage guarantees.
- Reason about quotas, control-plane APIs, eventual observation, cost, and shared responsibility.
- Reject single-zone and single-instance designs that claim unsupported availability.

## Capstone increment

Publish provider-neutral compute, identity, network, storage, DNS, load-balancing, metadata, quota, and failure-domain requirements for Course 2.

## Cloud is an operating model, not only remote virtualization

NIST characterizes cloud computing through on-demand self-service, broad network access, resource pooling, rapid elasticity, and measured service, together with service and deployment models. A manually created VM in someone else's datacenter may use cloud infrastructure, but a useful platform design also accounts for APIs, identity, quotas, automation, elasticity, and metering.

Course 1 uses provider-neutral requirements. Course 2 selects a primary provider lane and encodes resources in infrastructure as code.

## Regions and zones are failure and placement boundaries

A region is a provider-defined geographic or control boundary. A zone is an isolated location within a region, but the exact power, network, and service dependencies are provider-specific. Placing two instances in one zone protects against one instance failure, not zone loss. Placing instances in two zones does not protect a database if the only durable copy remains in one zone.

Availability claims need an explicit dependency graph:

```text
client
→ DNS
→ load balancer
→ compute instances
→ durable state
→ identity/KMS
→ backup/restore
```

A single regional dependency can dominate the claim even when compute spans zones.

## Virtual networks are policy domains

AWS VPCs, Google Cloud VPC networks, and Azure VNets expose different resource models, but all provide logical networking, subnets, routes, interfaces, addresses, and security controls. Important differences include regional versus zonal subnet semantics, default routes, firewall attachment, and transitive connectivity.

A provider map helps translation but does not assert identical behavior. Course 2 must read the selected provider's current documentation and test the actual route and firewall state.

## Identity should be attached, short-lived, and scoped

Static access keys copied to a host create distribution, rotation, leakage, and attribution problems. A cloud workload identity attaches authority to the instance or workload and provides short-lived credentials through a metadata or identity endpoint.

The host still needs protection: any compromised process that can request those credentials may use the identity's permissions. Least privilege and metadata access controls remain necessary.

The Atlas API does not need permission to alter networks or create instances. A backup process may need write-only or append-oriented access to one backup destination. Separate identities may be justified when responsibilities differ.

## Storage choices express different APIs and failure boundaries

- **block storage** presents addressable blocks, usually attached to one or a bounded set of instances;
- **object storage** presents objects through a service API, not a POSIX filesystem;
- **ephemeral/local storage** is tied to an instance or host;
- **managed database storage** is owned through a higher-level service contract.

Mounting object storage through FUSE does not turn object semantics into a local block filesystem. Applications that require atomic rename, locking, or `fsync` must validate the adapter's actual guarantees.

## Managed services transfer work, not all responsibility

A managed load balancer, database, DNS zone, or certificate service reduces undifferentiated operation. The consumer still owns configuration, identities, data, compatibility, recovery objectives, cost, and integration. The provider's shared-responsibility model describes where responsibility moves; it does not make the consumer's part optional.

A managed service can also create control-plane dependency and quota limits. Record provisioning latency, API rate limits, maintenance behavior, backup/restore policy, and regional availability.

## Control plane and data plane fail differently

The data plane serves traffic or storage operations. The control plane creates and changes resources. A control-plane API outage may prevent scaling or replacement while existing instances continue serving. Conversely, a data-plane outage can stop requests while the resource still appears `ACTIVE` in the control plane.

Runbooks and health models should not use one plane as proof of the other.

## Quotas and cost are architecture inputs

Cloud resources are subject to service quotas, regional availability, API rate limits, and account policy. A design requiring one thousand instances is not deployable when the account quota is twenty. A cross-zone architecture may incur transfer cost. Public IPv4 addresses may be scarce or billed.

Course 1 does not optimize cost, but the handoff records quantities and cost-relevant flows so Course 2 can plan and review them.

## Provider metadata comparison

The three provider profiles differ:

- AWS IMDSv2 requires a session token obtained through a `PUT` request and can require token use at the instance/account level.
- GCP metadata requests require `Metadata-Flavor: Google` and use a provider hostname or link-local address.
- Azure IMDS requests require a metadata header and expose instance and maintenance information.

These mechanisms evolve. The course records a standards snapshot date and links to official documentation. Never copy metadata response fields across providers by name alone.

## Worked investigation: “multi-zone” service loses writes

Two Atlas instances run in two zones behind a regional load balancer. Both attach to one zonal persistent disk through an unsupported or single-writer arrangement. The zone holding the disk fails. The compute topology was multi-zone; the durable system was not.

A correct availability statement must include durable data placement, write ownership, replication, recovery, and the load balancer's own regional behavior. Course 1's `FailureDomainPlan` rejects a zone-tolerance claim unless compute and durable copies span at least two zones and traffic can select surviving instances. It is a teaching classifier, not a proof of one provider design.

## The Course 2 requirements package

The outgoing files specify:

- replaceable compute and supported architectures;
- workload identity and static-key prohibition;
- public TLS edge and private internal API;
- durable state independent of the root image;
- backup in an independent failure domain;
- metadata-service restrictions;
- health separation and replacement runbook;
- explicit evidence required for zone-tolerance claims.

Course 2 will translate these into actual resources, state, modules, tests, and provider evidence.

## Atlas implementation bridge

The provider map translates concepts without claiming equivalence. The handoff requirements are intentionally independent of AWS, GCP, or Azure resource names. Course 2 will select a primary lane and record provider-specific semantics.

Use the failure-domain classifier to reject unsupported claims, then produce a real dependency diagram that includes state, identity, DNS, load balancing, and backup.

## Design review prompts

- Which resource is the authoritative workload identity?
- Which dependency remains single-zone?
- Can the control plane be unavailable while service continues?
- Which quota blocks replacement during an incident?
- Which cost grows with cross-zone or internet traffic?

## Boundary case: regional services with zonal dependencies

A load balancer may be regional while its backends or storage are zonal. A managed database may present a regional endpoint but have failover modes, maintenance windows, or replica lag that constrain the claim. Read the service's failure and consistency model rather than inferring it from endpoint scope.

## Boundary case: account and organization policy

Cloud resources can be denied by organization policies, service-control policies, allowed-location rules, encryption requirements, or tagging policy even when IAM permits the API action. Course 2 must model these inherited controls and expose them in plan evidence.

## Cloud requirement worksheet

```text
capability required:
portable behavior:
provider resource candidate:
region/zone scope:
identity owner:
network path:
data durability:
quota:
cost dimension:
control-plane dependency:
live proof command:
```

Provider-neutral design ends at required behavior; provider-specific engineering begins with these rows.

## Field method: model cloud scope and control-plane dependencies

Cloud architecture starts with required behavior, then maps that behavior to provider resources whose semantics are verified. Similar product names do not imply the same scope, consistency, maintenance, identity, or failure model. A subnet, firewall rule, load balancer, disk, managed identity, and DNS zone each have a scope and control plane.

Build a dependency graph that includes the components often omitted from availability diagrams:

- organization/account/project/subscription policy;
- identity issuance and token exchange;
- DNS authority and resolver path;
- load-balancer control and data planes;
- compute capacity and image availability;
- network routes, NAT, and egress dependencies;
- durable state and backup restore source;
- KMS or secret access;
- quotas, regional capacity, and billing controls.

A multi-zone compute group does not support a zone-failure claim when its only durable disk, NAT gateway, identity dependency, or operator access path is single-zone. State the weakest critical dependency and the recovery action when it fails.

Workload identity is preferable to static credentials because authority can be bound to the instance or service and rotated by the platform. It is not automatically safe. Metadata services are link-local but still reachable from workloads unless policy blocks them. AWS, GCP, and Azure require different request headers or session mechanisms and expose different identity documents. SSRF defenses, hop limits, proxy bypass, and least-privilege IAM remain part of the design.

Cloud quotas are availability inputs. Replacement can fail because an instance family, IP address, disk attachment, certificate, load balancer, or API rate quota is exhausted. Record current quota, required headroom, increase lead time, and fallback. Cost is also architectural evidence: cross-zone traffic, NAT processing, public egress, retained snapshots, and idle load balancers can dominate the small workload's compute cost.

Provider-neutral requirements should be precise enough to test but not so abstract that important semantics disappear. “Durable disk” is insufficient; state required size, performance class, encryption, attachment mode, zone scope, snapshot/restore behavior, deletion policy, and evidence route. Course 2 will convert these rows into OpenTofu modules and real provider proofs.


## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| A zone-tolerance claim requires all critical dependencies to tolerate the zone loss. | Atlas availability policy | failure-domain dependency review |
| Workload identity is preferred over static cloud keys on hosts. | Atlas identity policy/provider mechanisms | credential source and IAM evidence |
| Provider product mappings do not imply identical semantics. | course portability rule | provider-specific documentation and live proof |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### Provider-name portability

VPC, VNet, subnet, firewall, and load-balancer products differ in scope and behavior despite similar names.

### Control-plane green

A resource marked active does not prove the data plane serves correct traffic.

### Multi-zone compute only

Spreading VMs across zones does not make single-zone state or identity dependencies resilient.


## Module synthesis

Return to the central question: **Which cloud resources and trust boundaries are required to preserve the host guarantees without copying one provider’s vocabulary into the architecture?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**The architecture calls a single-zone VM and attached disk “highly available” because the cloud provider itself operates multiple zones.**—fails for the predicted reason.

## Continue

Module 10 integrates the full host into an operable release and exports the cloud-foundation handoff.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
