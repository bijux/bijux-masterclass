# Reference — Provider Comparison Map

The program uses AWS as the executable lane, but the engineering responsibilities are provider-neutral. This map helps translate concepts without pretending that similarly named products have identical scope or failure behavior.

| Responsibility | AWS reference | Google Cloud comparison | Azure comparison |
|---|---|---|---|
| Organization hierarchy | Organizations, accounts, OUs | organization, folders, projects | tenant, management groups, subscriptions |
| Workforce federation | IAM Identity Center / external IdP federation | Cloud Identity / Workforce Identity Federation | Microsoft Entra ID |
| Workload identity on VM | IAM role + instance profile | attached service account | managed identity |
| IaC remote state object | S3 | Cloud Storage | Blob Storage |
| Key management | KMS | Cloud KMS | Key Vault / Managed HSM |
| Virtual network | regional VPC | global VPC network with regional subnets | regional VNet |
| Public L7 edge | Application Load Balancer | external Application Load Balancer | Application Gateway or Front Door depending scope |
| Private service access | VPC endpoints / PrivateLink patterns | Private Service Connect / private Google access patterns | Private Link / service endpoints |
| Block storage | EBS | Persistent Disk / Hyperdisk | Managed Disks |
| Object storage | S3 | Cloud Storage | Blob Storage |
| VM metadata | IMDSv2 | metadata server with required header and controls | instance metadata service with required header |
| Audit logs | CloudTrail and service logs | Cloud Audit Logs | Azure Activity Log and resource logs |
| Account/project policy ceiling | SCPs and related organization policies | organization policies | Azure Policy / management-group policy plus RBAC scope |

## Differences that matter

### Network scope

AWS VPCs are regional. Google Cloud VPC networks are global with regional subnets. Azure VNets are regional. A module interface that assumes the same network-to-region relationship across providers is misleading.

### Zone identity

AWS availability-zone names are account-relative; stable zone IDs are important for cross-account architecture. Other providers have different naming and placement semantics. Preserve the architectural concept—stable failure-domain selection—rather than copying one identifier format.

### Identity attachment

AWS attaches a role through an instance profile. Google Cloud attaches a service account and scopes/API permissions interact differently. Azure managed identities have system- and user-assigned forms. The common requirement is short-lived workload authority with bounded resource access and auditable issuance.

### Load balancing and health

Products differ in global/regional scope, anycast behavior, TLS ownership, backend models, health-check source ranges, failover, and pricing. “Public load balancer” is not a portable guarantee.

### Private connectivity

Endpoint products vary by service support, DNS integration, route behavior, consumer/provider ownership, and cost. Replacing NAT with private endpoints requires a dependency inventory in every provider.

### State backend semantics

Object storage products differ in locking integrations, consistency history, key management, retention controls, and identity models. The course’s S3 lockfile profile should not be copied to another backend without reading that backend’s own locking documentation.

## How to use this map

For each Atlas requirement, translate five dimensions:

```text
resource/control-plane scope
identity and authority
network/data path
failure and recovery behavior
cost and quota model
```

For example, “private workload storage” is not solved by selecting each provider’s block-disk product. Verify zone attachment, encryption authority, snapshot consistency, restore behavior, expansion, deletion, and replacement.

## What should remain stable

Across providers, preserve:

- one accountable owner per state root and durable object;
- explicit target identity before apply;
- short-lived human and workload credentials;
- non-overlapping network allocation;
- explicit ingress and egress flows;
- immutable release inputs;
- tested backup restoration;
- state locking and recovery;
- policy-governed destructive changes;
- data-plane verification after control-plane change.

Provider portability means carrying these responsibilities into the selected product, not pretending the products are interchangeable.
