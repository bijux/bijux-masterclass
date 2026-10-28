# 30. Cloud & Infrastructure Engineering

**Program code:** `CLOUD`

**Purpose:** Develop provider-independent command of compute, networking, storage, identity, automation, resilience, governance, and economics in public, private, hybrid, and multi-cloud infrastructure.

**Level-II professional outcome:** Ready to design, provision, secure, operate, migrate, and optimize production cloud infrastructure using infrastructure as code and modern managed services.

**Prerequisites:** operating systems and networking basics; security fundamentals; scripting and version control; software architecture basics.

**Primary ownership:** cloud operating models; compute and virtualization; cloud networking; storage and managed data services; IAM and security foundations; infrastructure as code; resilience and disaster recovery; observability and cost; hybrid and multi-cloud; infrastructure governance and migration.

**Explicit exclusions:** internal developer-platform product design (Program 29); software release and SRE practice ownership (Program 14); application API design (Program 28); network protocol depth (Program 24).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Cloud Models and Global Infrastructure

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Cloud Service and Deployment Models** | `001-cloud-service-and-deployment-models.md` |
| 002 | **Shared Responsibility** | `002-shared-responsibility.md` |
| 003 | **Regions, Availability Zones, and Points of Presence** | `003-regions-availability-zones-and-points-of-presence.md` |
| 004 | **Accounts, Projects, Subscriptions, and Resource Hierarchies** | `004-accounts-projects-subscriptions-and-resource-hierarchies.md` |
| 005 | **Cloud Control Planes and Data Planes** | `005-cloud-control-planes-and-data-planes.md` |
| 006 | **Elasticity and On-Demand Provisioning** | `006-elasticity-and-on-demand-provisioning.md` |
| 007 | **Managed Services and Operational Trade-Offs** | `007-managed-services-and-operational-trade-offs.md` |
| 008 | **Quotas, Limits, and Service Boundaries** | `008-quotas-limits-and-service-boundaries.md` |
| 009 | **Cloud Failure Domains** | `009-cloud-failure-domains.md` |
| 010 | **Translating Workload Requirements into Cloud Constraints** | `010-translating-workload-requirements-into-cloud-constraints.md` |

### Block 02 — Compute and Runtime Infrastructure

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Virtual Machines and Machine Images** | `011-virtual-machines-and-machine-images.md` |
| 012 | **Instance Families and Workload Sizing** | `012-instance-families-and-workload-sizing.md` |
| 013 | **Autoscaling Groups** | `013-autoscaling-groups.md` |
| 014 | **Load Balancing** | `014-load-balancing.md` |
| 015 | **Container Runtime Services** | `015-container-runtime-services.md` |
| 016 | **Managed Kubernetes Positioning** | `016-managed-kubernetes-positioning.md` |
| 017 | **Serverless Functions** | `017-serverless-functions.md` |
| 018 | **Managed Application Runtimes** | `018-managed-application-runtimes.md` |
| 019 | **Batch and High-Throughput Compute** | `019-batch-and-high-throughput-compute.md` |
| 020 | **Selecting Compute from Isolation, Control, Scale, and Cost** | `020-selecting-compute-from-isolation-control-scale-and-cost.md` |

### Block 03 — Cloud Networking

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Virtual Networks and Address Planning** | `021-virtual-networks-and-address-planning.md` |
| 022 | **Subnets and Routing Tables** | `022-subnets-and-routing-tables.md` |
| 023 | **Internet and NAT Gateways** | `023-internet-and-nat-gateways.md` |
| 024 | **Security Groups and Network Policies** | `024-security-groups-and-network-policies.md` |
| 025 | **Private Service Connectivity** | `025-private-service-connectivity.md` |
| 026 | **Virtual Private Network Connections** | `026-virtual-private-network-connections.md` |
| 027 | **Dedicated Private Connectivity** | `027-dedicated-private-connectivity.md` |
| 028 | **DNS and Service Discovery** | `028-dns-and-service-discovery.md` |
| 029 | **Cloud Load-Balancer Layers** | `029-cloud-load-balancer-layers.md` |
| 030 | **Designing a Segmented Cloud Network** | `030-designing-a-segmented-cloud-network.md` |

### Block 04 — Storage and Managed Data Services

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Object Storage** | `031-object-storage.md` |
| 032 | **Block Storage** | `032-block-storage.md` |
| 033 | **Network File Storage** | `033-network-file-storage.md` |
| 034 | **Archive and Lifecycle Tiers** | `034-archive-and-lifecycle-tiers.md` |
| 035 | **Managed Relational Databases** | `035-managed-relational-databases.md` |
| 036 | **Managed Key-Value and Document Stores** | `036-managed-key-value-and-document-stores.md` |
| 037 | **Managed Caches** | `037-managed-caches.md` |
| 038 | **Managed Messaging and Event Services** | `038-managed-messaging-and-event-services.md` |
| 039 | **Backup, Snapshot, and Replication Options** | `039-backup-snapshot-and-replication-options.md` |
| 040 | **Mapping Data Requirements to Managed Services** | `040-mapping-data-requirements-to-managed-services.md` |

### Block 05 — Identity, Secrets, and Infrastructure Security

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Human and Workload Identities** | `041-human-and-workload-identities.md` |
| 042 | **Roles, Policies, and Permission Evaluation** | `042-roles-policies-and-permission-evaluation.md` |
| 043 | **Federation and Single Sign-On** | `043-federation-and-single-sign-on.md` |
| 044 | **Short-Lived Credentials** | `044-short-lived-credentials.md` |
| 045 | **Managed Cloud Secrets Services** | `045-managed-cloud-secrets-services.md` |
| 046 | **Encryption and Key Management** | `046-encryption-and-key-management.md` |
| 047 | **Resource Policies** | `047-resource-policies.md` |
| 048 | **Organization-Level Guardrails** | `048-organization-level-guardrails.md` |
| 049 | **Audit Logs and Configuration History** | `049-audit-logs-and-configuration-history.md` |
| 050 | **Designing Least-Privilege Cloud Access** | `050-designing-least-privilege-cloud-access.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Infrastructure as Code and Automation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Declarative and Imperative Infrastructure** | `051-declarative-and-imperative-infrastructure.md` |
| 052 | **Resource Graphs and Dependency Ordering** | `052-resource-graphs-and-dependency-ordering.md` |
| 053 | **State and Drift** | `053-state-and-drift.md` |
| 054 | **Modules and Reusable Components** | `054-modules-and-reusable-components.md` |
| 055 | **Environment Composition** | `055-environment-composition.md` |
| 056 | **Testing Infrastructure Code** | `056-testing-infrastructure-code.md` |
| 057 | **Infrastructure Policy as Code** | `057-infrastructure-policy-as-code.md` |
| 058 | **Secrets in Automation** | `058-secrets-in-automation.md` |
| 059 | **Safe Plan, Apply, and Rollback Workflows** | `059-safe-plan-apply-and-rollback-workflows.md` |
| 060 | **Designing a Maintainable Infrastructure Repository** | `060-designing-a-maintainable-infrastructure-repository.md` |

### Block 07 — Resilient and Recoverable Cloud Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Multi-Zone Application Design** | `061-multi-zone-application-design.md` |
| 062 | **Stateless and Stateful Failover** | `062-stateless-and-stateful-failover.md` |
| 063 | **Health Checks and Traffic Shifting** | `063-health-checks-and-traffic-shifting.md` |
| 064 | **Queue-Based Decoupling** | `064-queue-based-decoupling.md` |
| 065 | **Backup and Restore Architecture** | `065-backup-and-restore-architecture.md` |
| 066 | **Cross-Region Replication** | `066-cross-region-replication.md` |
| 067 | **Active-Passive Regional Recovery** | `067-active-passive-regional-recovery.md` |
| 068 | **Active-Active Multi-Region Design** | `068-active-active-multi-region-design.md` |
| 069 | **Recovery Testing** | `069-recovery-testing.md` |
| 070 | **Choosing Resilience from Business RTO and RPO** | `070-choosing-resilience-from-business-rto-and-rpo.md` |

### Block 08 — Cloud Operations, Observability, and Economics

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Resource Inventory and Tagging** | `071-resource-inventory-and-tagging.md` |
| 072 | **Metrics, Logs, and Traces in Cloud Environments** | `072-metrics-logs-and-traces-in-cloud-environments.md` |
| 073 | **Configuration and Drift Detection** | `073-configuration-and-drift-detection.md` |
| 074 | **Patch and Image Management** | `074-patch-and-image-management.md` |
| 075 | **Capacity and Quota Management** | `075-capacity-and-quota-management.md` |
| 076 | **Cost Allocation** | `076-cost-allocation.md` |
| 077 | **Commitment Discounts and Spot Capacity** | `077-commitment-discounts-and-spot-capacity.md` |
| 078 | **Storage, Network, and Egress Economics** | `078-storage-network-and-egress-economics.md` |
| 079 | **FinOps Feedback Loops** | `079-finops-feedback-loops.md` |
| 080 | **Reviewing a Cloud Estate for Reliability, Security, and Waste** | `080-reviewing-a-cloud-estate-for-reliability-security-and-waste.md` |

### Block 09 — Hybrid, Multi-Cloud, and Edge Infrastructure

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Hybrid Connectivity** | `081-hybrid-connectivity.md` |
| 082 | **Identity Across On-Premises and Cloud** | `082-identity-across-on-premises-and-cloud.md` |
| 083 | **Hybrid DNS and Naming** | `083-hybrid-dns-and-naming.md` |
| 084 | **Data Movement and Synchronization** | `084-data-movement-and-synchronization.md` |
| 085 | **Workload Portability** | `085-workload-portability.md` |
| 086 | **Multi-Cloud Motivations and Costs** | `086-multi-cloud-motivations-and-costs.md` |
| 087 | **Provider Abstraction and Lowest-Common-Denominator Risk** | `087-provider-abstraction-and-lowest-common-denominator-risk.md` |
| 088 | **Edge Compute and Content Distribution** | `088-edge-compute-and-content-distribution.md` |
| 089 | **Sovereign and Regulated Cloud** | `089-sovereign-and-regulated-cloud.md` |
| 090 | **Designing Hybrid Architecture Without Duplicating Every Platform** | `090-designing-hybrid-architecture-without-duplicating-every-platform.md` |

### Block 10 — Cloud Governance, Migration, and Advanced Design

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Landing Zones** | `091-landing-zones.md` |
| 092 | **Account and Subscription Vending** | `092-account-and-subscription-vending.md` |
| 093 | **Centralized and Federated Network Models** | `093-centralized-and-federated-network-models.md` |
| 094 | **Organization Policies and Compliance** | `094-organization-policies-and-compliance.md` |
| 095 | **Cloud Security Posture Management** | `095-cloud-security-posture-management.md` |
| 096 | **Migration Discovery and Dependency Mapping** | `096-migration-discovery-and-dependency-mapping.md` |
| 097 | **Rehost, Replatform, Refactor, Repurchase, Retain, and Retire** | `097-rehost-replatform-refactor-repurchase-retain-and-retire.md` |
| 098 | **Data and Cutover Migration** | `098-data-and-cutover-migration.md` |
| 099 | **Cloud Architecture Decision Reviews** | `099-cloud-architecture-decision-reviews.md` |
| 100 | **Defending a Cloud Infrastructure Strategy Under Cost and Risk Constraints** | `100-defending-a-cloud-infrastructure-strategy-under-cost-and-risk-constraints.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
