# 12. Software Engineering: Software Architecture

**Program code:** `SARCH`

**Purpose:** Develop the ability to shape software-intensive systems through explicit quality attributes, boundaries, structures, deployment models, and evolutionary decisions.

**Level-II professional outcome:** Ready to act as a senior architect or technical lead who can design, document, evaluate, communicate, and evolve production architectures.

**Prerequisites:** software design experience; databases and networking basics; distributed-systems foundations; production software experience.

**Primary ownership:** architectural drivers; quality attributes; views and viewpoints; architectural styles; component and service boundaries; data and integration architecture; deployment architecture; architecture evaluation; evolution and governance; socio-technical architecture.

**Explicit exclusions:** code-level domain design (Program 09); pattern catalogues (Program 11); cloud implementation detail (Program 30); distributed algorithms (Program 27).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Architectural Thinking and Drivers

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Architecture as Significant Design Decisions** | `001-architecture-as-significant-design-decisions.md` |
| 002 | **Stakeholders and Architectural Concerns** | `002-stakeholders-and-architectural-concerns.md` |
| 003 | **Functional Scope and System Context** | `003-functional-scope-and-system-context.md` |
| 004 | **Quality Attributes as Architectural Drivers** | `004-quality-attributes-as-architectural-drivers.md` |
| 005 | **Constraints, Assumptions, and Risks** | `005-constraints-assumptions-and-risks.md` |
| 006 | **Architecturally Significant Requirements** | `006-architecturally-significant-requirements.md` |
| 007 | **Trade-Offs and Competing Objectives** | `007-trade-offs-and-competing-objectives.md` |
| 008 | **Architecture Versus Detailed Design** | `008-architecture-versus-detailed-design.md` |
| 009 | **Architecture Decision Records** | `009-architecture-decision-records.md` |
| 010 | **Framing an Architecture Problem Before Choosing Technology** | `010-framing-an-architecture-problem-before-choosing-technology.md` |

### Block 02 — Quality Attributes and Tactics

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Availability and Recovery Tactics** | `011-availability-and-recovery-tactics.md` |
| 012 | **Performance and Latency Tactics** | `012-performance-and-latency-tactics.md` |
| 013 | **Scalability and Capacity Tactics** | `013-scalability-and-capacity-tactics.md` |
| 014 | **Security and Privacy Tactics** | `014-security-and-privacy-tactics.md` |
| 015 | **Modifiability and Evolvability Tactics** | `015-modifiability-and-evolvability-tactics.md` |
| 016 | **Testability Tactics** | `016-testability-tactics.md` |
| 017 | **Interoperability Tactics** | `017-interoperability-tactics.md` |
| 018 | **Observability and Operability Tactics** | `018-observability-and-operability-tactics.md` |
| 019 | **Usability and Accessibility as System Qualities** | `019-usability-and-accessibility-as-system-qualities.md` |
| 020 | **Resolving Quality-Attribute Conflicts** | `020-resolving-quality-attribute-conflicts.md` |

### Block 03 — Views, Models, and Communication

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Context Views** | `021-context-views.md` |
| 022 | **Module and Code Views** | `022-module-and-code-views.md` |
| 023 | **Component-and-Connector Views** | `023-component-and-connector-views.md` |
| 024 | **Runtime Interaction Views** | `024-runtime-interaction-views.md` |
| 025 | **Deployment Views** | `025-deployment-views.md` |
| 026 | **Data and Information Views** | `026-data-and-information-views.md` |
| 027 | **Development and Build Views** | `027-development-and-build-views.md` |
| 028 | **Operational Views** | `028-operational-views.md` |
| 029 | **C4, UML, and Informal Diagram Semantics** | `029-c4-uml-and-informal-diagram-semantics.md` |
| 030 | **Creating an Architecture Description for Different Audiences** | `030-creating-an-architecture-description-for-different-audiences.md` |

### Block 04 — Core Architectural Styles

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Layered Architecture** | `031-layered-architecture.md` |
| 032 | **Modular Monoliths** | `032-modular-monoliths.md` |
| 033 | **Hexagonal and Onion Architectures** | `033-hexagonal-and-onion-architectures.md` |
| 034 | **Pipe-and-Filter Systems** | `034-pipe-and-filter-systems.md` |
| 035 | **Event-Driven Architecture** | `035-event-driven-architecture.md` |
| 036 | **Client-Server Architecture** | `036-client-server-architecture.md` |
| 037 | **Microkernel and Plugin Architecture** | `037-microkernel-and-plugin-architecture.md` |
| 038 | **Service-Oriented Architecture** | `038-service-oriented-architecture.md` |
| 039 | **Microservices Architecture** | `039-microservices-architecture.md` |
| 040 | **Choosing a Style from Forces Rather Than Fashion** | `040-choosing-a-style-from-forces-rather-than-fashion.md` |

### Block 05 — Data, Integration, and Deployment Structure

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **System-of-Record Boundaries** | `041-system-of-record-boundaries.md` |
| 042 | **Shared Database Versus Database per Service** | `042-shared-database-versus-database-per-service.md` |
| 043 | **Synchronous Request-Response Integration** | `043-synchronous-request-response-integration.md` |
| 044 | **Asynchronous Messaging Integration** | `044-asynchronous-messaging-integration.md` |
| 045 | **Batch and File-Based Integration** | `045-batch-and-file-based-integration.md` |
| 046 | **API Gateway and Edge Architecture** | `046-api-gateway-and-edge-architecture.md` |
| 047 | **Caching Layers and Invalidation Boundaries** | `047-caching-layers-and-invalidation-boundaries.md` |
| 048 | **Deployment Units and Release Independence** | `048-deployment-units-and-release-independence.md` |
| 049 | **Configuration and Environment Topology** | `049-configuration-and-environment-topology.md` |
| 050 | **Tracing One Business Capability Across Architectural Structures** | `050-tracing-one-business-capability-across-architectural-structures.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Distributed and Cloud-Native Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Partial Failure as an Architectural Constraint** | `051-partial-failure-as-an-architectural-constraint.md` |
| 052 | **Consistency and Availability Trade-Offs** | `052-consistency-and-availability-trade-offs.md` |
| 053 | **Partitioning and Data Placement** | `053-partitioning-and-data-placement.md` |
| 054 | **Multi-Region Topologies** | `054-multi-region-topologies.md` |
| 055 | **Control-Plane and Data-Plane Architecture** | `055-control-plane-and-data-plane-architecture.md` |
| 056 | **Cell-Based Architecture** | `056-cell-based-architecture.md` |
| 057 | **Queue-Based Load Leveling** | `057-queue-based-load-leveling.md` |
| 058 | **Serverless and Event-Native Architecture** | `058-serverless-and-event-native-architecture.md` |
| 059 | **Edge and Hybrid Architectures** | `059-edge-and-hybrid-architectures.md` |
| 060 | **Evaluating a Distributed Architecture Under Failure** | `060-evaluating-a-distributed-architecture-under-failure.md` |

### Block 07 — Architecture Evaluation and Quantitative Reasoning

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Architecture Tradeoff Analysis Method** | `061-architecture-tradeoff-analysis-method.md` |
| 062 | **Quality-Attribute Scenarios** | `062-quality-attribute-scenarios.md` |
| 063 | **Risk, Sensitivity, and Trade-Off Points** | `063-risk-sensitivity-and-trade-off-points.md` |
| 064 | **Architecture Fitness Functions** | `064-architecture-fitness-functions.md` |
| 065 | **Dependency and Coupling Metrics** | `065-dependency-and-coupling-metrics.md` |
| 066 | **Performance and Capacity Models** | `066-performance-and-capacity-models.md` |
| 067 | **Availability and Reliability Models** | `067-availability-and-reliability-models.md` |
| 068 | **Threat Modeling at Architecture Scale** | `068-threat-modeling-at-architecture-scale.md` |
| 069 | **Cost Models and Unit Economics** | `069-cost-models-and-unit-economics.md` |
| 070 | **Running an Evidence-Based Architecture Review** | `070-running-an-evidence-based-architecture-review.md` |

### Block 08 — Evolutionary Architecture and Modernization

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Architectural Drift and Erosion** | `071-architectural-drift-and-erosion.md` |
| 072 | **Evolutionary Architecture Principles** | `072-evolutionary-architecture-principles.md` |
| 073 | **Versioned Contracts and Compatibility** | `073-versioned-contracts-and-compatibility.md` |
| 074 | **Incremental Decomposition** | `074-incremental-decomposition.md` |
| 075 | **Strangler and Parallel-Run Architectures** | `075-strangler-and-parallel-run-architectures.md` |
| 076 | **Data Migration Architecture** | `076-data-migration-architecture.md` |
| 077 | **Modularizing a Distributed Monolith** | `077-modularizing-a-distributed-monolith.md` |
| 078 | **Replatforming, Rehosting, Refactoring, and Rebuilding** | `078-replatforming-rehosting-refactoring-and-rebuilding.md` |
| 079 | **Decommissioning Architectural Components** | `079-decommissioning-architectural-components.md` |
| 080 | **Planning Architecture Evolution Across Multiple Releases** | `080-planning-architecture-evolution-across-multiple-releases.md` |

### Block 09 — Organization, Governance, and Platform Relationships

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Conway's Law and Team Structures** | `081-conway-s-law-and-team-structures.md` |
| 082 | **Team Topologies and Architecture** | `082-team-topologies-and-architecture.md` |
| 083 | **Architecture Governance Models** | `083-architecture-governance-models.md` |
| 084 | **Standards, Principles, and Guardrails** | `084-standards-principles-and-guardrails.md` |
| 085 | **Golden Paths and Paved Roads** | `085-golden-paths-and-paved-roads.md` |
| 086 | **Reference Architectures** | `086-reference-architectures.md` |
| 087 | **Architecture Communities and Review Forums** | `087-architecture-communities-and-review-forums.md` |
| 088 | **Federated Decision Making** | `088-federated-decision-making.md` |
| 089 | **Managing Exceptions and Technical Risk** | `089-managing-exceptions-and-technical-risk.md` |
| 090 | **Designing Governance That Preserves Team Autonomy** | `090-designing-governance-that-preserves-team-autonomy.md` |

### Block 10 — Advanced Architectural Judgment

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Architecture for Regulated and Safety-Critical Systems** | `091-architecture-for-regulated-and-safety-critical-systems.md` |
| 092 | **Architecture for High-Change Product Domains** | `092-architecture-for-high-change-product-domains.md` |
| 093 | **Architecture for Extreme Read or Write Scale** | `093-architecture-for-extreme-read-or-write-scale.md` |
| 094 | **Architecture for Machine-Learning-Enabled Products** | `094-architecture-for-machine-learning-enabled-products.md` |
| 095 | **Architecture for Multi-Tenant Platforms** | `095-architecture-for-multi-tenant-platforms.md` |
| 096 | **Architecture for Offline and Intermittently Connected Systems** | `096-architecture-for-offline-and-intermittently-connected-systems.md` |
| 097 | **Architecture for Long-Lived Scientific Systems** | `097-architecture-for-long-lived-scientific-systems.md` |
| 098 | **Architecture Under Severe Cost Constraints** | `098-architecture-under-severe-cost-constraints.md` |
| 099 | **Comparing Multiple Viable Architectures** | `099-comparing-multiple-viable-architectures.md` |
| 100 | **Defending an Architecture Before an Adversarial Technical Board** | `100-defending-an-architecture-before-an-adversarial-technical-board.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
