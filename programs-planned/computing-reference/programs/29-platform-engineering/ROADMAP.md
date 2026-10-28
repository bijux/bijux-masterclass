# 29. Platform Engineering

**Program code:** `PLAT`

**Purpose:** Develop the product, architecture, and implementation skills needed to create safe self-service platforms that reduce cognitive load and enable teams to deliver and operate software independently.

**Level-II professional outcome:** Ready to design, build, operate, and evolve internal developer platforms, paved roads, control planes, developer portals, and shared runtime capabilities.

**Prerequisites:** cloud and infrastructure foundations; containers and Kubernetes basics; software architecture; delivery and reliability basics.

**Primary ownership:** platform as product; developer experience and cognitive load; self-service interfaces; containers and Kubernetes as platform substrate; control planes and operators; golden paths; developer portals; multi-tenancy and policy; platform observability and reliability; platform adoption and economics.

**Explicit exclusions:** cloud resource and network architecture (Program 30); software delivery practice ownership (Program 14); service API design ownership (Program 28); general software architecture (Program 12).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Platform Engineering Foundations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Platform Engineering as Complexity Management** | `001-platform-engineering-as-complexity-management.md` |
| 002 | **Platform Consumers and Jobs to Be Done** | `002-platform-consumers-and-jobs-to-be-done.md` |
| 003 | **Developer Cognitive Load** | `003-developer-cognitive-load.md` |
| 004 | **Platform as Product** | `004-platform-as-product.md` |
| 005 | **Self-Service and Guardrails** | `005-self-service-and-guardrails.md` |
| 006 | **Paved Roads and Escape Hatches** | `006-paved-roads-and-escape-hatches.md` |
| 007 | **Platform Capabilities Versus Tool Catalogs** | `007-platform-capabilities-versus-tool-catalogs.md` |
| 008 | **Internal Platforms and External Cloud Services** | `008-internal-platforms-and-external-cloud-services.md` |
| 009 | **Platform Team Boundaries** | `009-platform-team-boundaries.md` |
| 010 | **Defining a Platform's Value Proposition** | `010-defining-a-platform-s-value-proposition.md` |

### Block 02 — Developer Experience and Platform Interfaces

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Developer Journeys** | `011-developer-journeys.md` |
| 012 | **Time to First Successful Deployment** | `012-time-to-first-successful-deployment.md` |
| 013 | **Command-Line Interfaces** | `013-command-line-interfaces.md` |
| 014 | **Web Portals** | `014-web-portals.md` |
| 015 | **APIs and Declarative Resources** | `015-apis-and-declarative-resources.md` |
| 016 | **Templates and Scaffolding** | `016-templates-and-scaffolding.md` |
| 017 | **Documentation and Discoverability** | `017-documentation-and-discoverability.md` |
| 018 | **Feedback and Error Diagnostics** | `018-feedback-and-error-diagnostics.md` |
| 019 | **Golden-Path Versioning** | `019-golden-path-versioning.md` |
| 020 | **Measuring Developer Experience Without Vanity Metrics** | `020-measuring-developer-experience-without-vanity-metrics.md` |

### Block 03 — Container and Kubernetes Substrate

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Container Images as Platform Artifacts** | `021-container-images-as-platform-artifacts.md` |
| 022 | **Runtime Isolation and Resource Controls** | `022-runtime-isolation-and-resource-controls.md` |
| 023 | **Kubernetes Declarative Resources** | `023-kubernetes-declarative-resources.md` |
| 024 | **Pods, Workloads, and Controllers** | `024-pods-workloads-and-controllers.md` |
| 025 | **Services and Ingress** | `025-services-and-ingress.md` |
| 026 | **Configuration and Secrets** | `026-configuration-and-secrets.md` |
| 027 | **Storage and Stateful Workloads** | `027-storage-and-stateful-workloads.md` |
| 028 | **Scheduling and Placement** | `028-scheduling-and-placement.md` |
| 029 | **Health, Readiness, and Lifecycle** | `029-health-readiness-and-lifecycle.md` |
| 030 | **Mapping Application Needs to Kubernetes Primitives** | `030-mapping-application-needs-to-kubernetes-primitives.md` |

### Block 04 — Core Platform Capabilities

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Application Build Capability** | `031-application-build-capability.md` |
| 032 | **Artifact and Image Management** | `032-artifact-and-image-management.md` |
| 033 | **Environment Provisioning** | `033-environment-provisioning.md` |
| 034 | **Deployment Capability** | `034-deployment-capability.md` |
| 035 | **Configuration Management** | `035-configuration-management.md` |
| 036 | **Secret Delivery** | `036-secret-delivery.md` |
| 037 | **Service Connectivity** | `037-service-connectivity.md` |
| 038 | **Observability Provisioning** | `038-observability-provisioning.md` |
| 039 | **Database and Data-Service Access** | `039-database-and-data-service-access.md` |
| 040 | **Designing a Coherent Minimum Viable Platform** | `040-designing-a-coherent-minimum-viable-platform.md` |

### Block 05 — Golden Paths and Workload Standards

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Workload Archetypes** | `041-workload-archetypes.md` |
| 042 | **Service Templates** | `042-service-templates.md` |
| 043 | **Batch and Scheduled Workload Templates** | `043-batch-and-scheduled-workload-templates.md` |
| 044 | **Event-Driven Workload Templates** | `044-event-driven-workload-templates.md` |
| 045 | **Stateful Workload Standards** | `045-stateful-workload-standards.md` |
| 046 | **Runtime and Language Baselines** | `046-runtime-and-language-baselines.md` |
| 047 | **Health and Telemetry Contracts** | `047-health-and-telemetry-contracts.md` |
| 048 | **Security and Compliance Defaults** | `048-security-and-compliance-defaults.md` |
| 049 | **Upgrade and Deprecation Policies** | `049-upgrade-and-deprecation-policies.md` |
| 050 | **Designing a Golden Path That Remains Optional but Attractive** | `050-designing-a-golden-path-that-remains-optional-but-attractive.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Control Planes, Operators, and Reconciliation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Control-Plane and Data-Plane Separation** | `051-control-plane-and-data-plane-separation.md` |
| 052 | **Desired State and Reconciliation** | `052-desired-state-and-reconciliation.md` |
| 053 | **Custom Resource Definitions** | `053-custom-resource-definitions.md` |
| 054 | **Operator State Machines** | `054-operator-state-machines.md` |
| 055 | **Idempotent Reconciliation** | `055-idempotent-reconciliation.md` |
| 056 | **Finalizers and Deletion** | `056-finalizers-and-deletion.md` |
| 057 | **Status, Conditions, and Drift** | `057-status-conditions-and-drift.md` |
| 058 | **Cross-Resource Dependencies** | `058-cross-resource-dependencies.md` |
| 059 | **Control-Plane Failure and Recovery** | `059-control-plane-failure-and-recovery.md` |
| 060 | **Designing a Domain-Specific Platform API** | `060-designing-a-domain-specific-platform-api.md` |

### Block 07 — Internal Developer Platform Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Platform API Layers** | `061-platform-api-layers.md` |
| 062 | **Developer Portal Architecture** | `062-developer-portal-architecture.md` |
| 063 | **Software Catalogs** | `063-software-catalogs.md` |
| 064 | **Ownership and Metadata** | `064-ownership-and-metadata.md` |
| 065 | **Workflow and Orchestration Layers** | `065-workflow-and-orchestration-layers.md` |
| 066 | **Policy Decision and Enforcement Points** | `066-policy-decision-and-enforcement-points.md` |
| 067 | **Environment and Account Vending** | `067-environment-and-account-vending.md` |
| 068 | **Service Broker and Marketplace Models** | `068-service-broker-and-marketplace-models.md` |
| 069 | **Platform Eventing** | `069-platform-eventing.md` |
| 070 | **Integrating Platform Components Without Creating a Portal Monolith** | `070-integrating-platform-components-without-creating-a-portal-monolith.md` |

### Block 08 — Multi-Tenancy, Security, and Governance

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Tenant Models** | `071-tenant-models.md` |
| 072 | **Namespace, Account, and Cluster Isolation** | `072-namespace-account-and-cluster-isolation.md` |
| 073 | **Resource Quotas** | `073-resource-quotas.md` |
| 074 | **Identity Federation** | `074-identity-federation.md` |
| 075 | **Workload Identity** | `075-workload-identity.md` |
| 076 | **Platform Policy as Code** | `076-platform-policy-as-code.md` |
| 077 | **Admission Control** | `077-admission-control.md` |
| 078 | **Supply-Chain Policy** | `078-supply-chain-policy.md` |
| 079 | **Audit and Evidence** | `079-audit-and-evidence.md` |
| 080 | **Balancing Central Guardrails with Team Autonomy** | `080-balancing-central-guardrails-with-team-autonomy.md` |

### Block 09 — Platform Reliability, Scale, and Operations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Platform Service-Level Objectives** | `081-platform-service-level-objectives.md` |
| 082 | **Control-Plane Capacity** | `082-control-plane-capacity.md` |
| 083 | **Cluster and Fleet Management** | `083-cluster-and-fleet-management.md` |
| 084 | **Platform Dependency Mapping** | `084-platform-dependency-mapping.md` |
| 085 | **Upgrade Orchestration** | `085-upgrade-orchestration.md` |
| 086 | **Backup and Restore of Platform State** | `086-backup-and-restore-of-platform-state.md` |
| 087 | **Incident Response for Shared Platforms** | `087-incident-response-for-shared-platforms.md` |
| 088 | **Regional and Multi-Cluster Platforms** | `088-regional-and-multi-cluster-platforms.md` |
| 089 | **Cost Allocation and Efficiency** | `089-cost-allocation-and-efficiency.md` |
| 090 | **Reviewing Platform Failure Blast Radius** | `090-reviewing-platform-failure-blast-radius.md` |

### Block 10 — Adoption, Evolution, and Platform Strategy

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Platform Discovery and Product Research** | `091-platform-discovery-and-product-research.md` |
| 092 | **Adoption Funnels** | `092-adoption-funnels.md` |
| 093 | **Migration to the Platform** | `093-migration-to-the-platform.md` |
| 094 | **Support Models and Enabling Teams** | `094-support-models-and-enabling-teams.md` |
| 095 | **Platform Roadmaps** | `095-platform-roadmaps.md` |
| 096 | **Build Versus Buy** | `096-build-versus-buy.md` |
| 097 | **Capability Lifecycle and Retirement** | `097-capability-lifecycle-and-retirement.md` |
| 098 | **Measuring Platform Outcomes** | `098-measuring-platform-outcomes.md` |
| 099 | **Avoiding Platform Monopolies and Forced Abstractions** | `099-avoiding-platform-monopolies-and-forced-abstractions.md` |
| 100 | **Defending a Platform Strategy to Developers, Security, and Leadership** | `100-defending-a-platform-strategy-to-developers-security-and-leadership.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
