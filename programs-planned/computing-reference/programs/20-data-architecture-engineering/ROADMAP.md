# 20. Data Architecture Engineering

**Program code:** `DARCH`

**Purpose:** Develop the ability to shape organization-wide data structures, ownership, flows, platforms, governance, and evolution across operational, analytical, and AI use cases.

**Level-II professional outcome:** Ready to work as a data architect who can define target architectures, domain boundaries, integration strategies, governance mechanisms, migration plans, and decision records.

**Prerequisites:** database and data-engineering foundations; software architecture fundamentals; business-domain modeling; security and governance basics.

**Primary ownership:** enterprise data architecture; data domains and ownership; conceptual and logical models; integration architecture; master and reference data; metadata and semantics; governance architecture; data mesh and fabric; privacy and lifecycle architecture; data modernization.

**Explicit exclusions:** pipeline implementation (Program 19); cluster and engine internals (Program 21); database engine design (Program 18); general software architecture ownership (Program 12).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Data Architecture Scope and Principles

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Data Architecture as Structure, Flow, Ownership, and Policy** | `001-data-architecture-as-structure-flow-ownership-and-policy.md` |
| 002 | **Business Strategy and Data Outcomes** | `002-business-strategy-and-data-outcomes.md` |
| 003 | **Current-State Data Landscape** | `003-current-state-data-landscape.md` |
| 004 | **Systems of Record, Engagement, and Insight** | `004-systems-of-record-engagement-and-insight.md` |
| 005 | **Operational, Analytical, and Shared Data** | `005-operational-analytical-and-shared-data.md` |
| 006 | **Data Principles and Decision Rules** | `006-data-principles-and-decision-rules.md` |
| 007 | **Architecture Drivers and Constraints** | `007-architecture-drivers-and-constraints.md` |
| 008 | **Data Risk and Criticality** | `008-data-risk-and-criticality.md` |
| 009 | **Architecture Views and Stakeholders** | `009-architecture-views-and-stakeholders.md` |
| 010 | **Writing a Data Architecture Charter** | `010-writing-a-data-architecture-charter.md` |

### Block 02 — Conceptual, Logical, and Canonical Models

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Conceptual Data Models** | `011-conceptual-data-models.md` |
| 012 | **Logical Data Models** | `012-logical-data-models.md` |
| 013 | **Physical Models and Their Separation** | `013-physical-models-and-their-separation.md` |
| 014 | **Entities, Relationships, and Business Keys** | `014-entities-relationships-and-business-keys.md` |
| 015 | **Shared Vocabulary and Business Glossaries** | `015-shared-vocabulary-and-business-glossaries.md` |
| 016 | **Canonical Models and Their Trade-Offs** | `016-canonical-models-and-their-trade-offs.md` |
| 017 | **Event Schemas and Information Models** | `017-event-schemas-and-information-models.md` |
| 018 | **Temporal and Historical Modeling** | `018-temporal-and-historical-modeling.md` |
| 019 | **Model Versioning** | `019-model-versioning.md` |
| 020 | **Reconciling Conflicting Models Across Systems** | `020-reconciling-conflicting-models-across-systems.md` |

### Block 03 — Domains, Ownership, and Data Products

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Business Capabilities and Data Domains** | `021-business-capabilities-and-data-domains.md` |
| 022 | **Domain Boundaries** | `022-domain-boundaries.md` |
| 023 | **Data Ownership and Accountability** | `023-data-ownership-and-accountability.md` |
| 024 | **Stewardship Roles** | `024-stewardship-roles.md` |
| 025 | **Source-Aligned, Aggregate, and Consumer-Aligned Data** | `025-source-aligned-aggregate-and-consumer-aligned-data.md` |
| 026 | **Data Products and Service Expectations** | `026-data-products-and-service-expectations.md` |
| 027 | **Producer and Consumer Contracts** | `027-producer-and-consumer-contracts.md` |
| 028 | **Cross-Domain Dependencies** | `028-cross-domain-dependencies.md` |
| 029 | **Domain Metadata and Discoverability** | `029-domain-metadata-and-discoverability.md` |
| 030 | **Evaluating Whether a Data Domain Is Cohesive** | `030-evaluating-whether-a-data-domain-is-cohesive.md` |

### Block 04 — Integration and Movement Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Point-to-Point Integration and Its Costs** | `031-point-to-point-integration-and-its-costs.md` |
| 032 | **Hub-and-Spoke Integration** | `032-hub-and-spoke-integration.md` |
| 033 | **Enterprise Service Bus** | `033-enterprise-service-bus.md` |
| 034 | **API-Led Data Access** | `034-api-led-data-access.md` |
| 035 | **Event-Driven Data Integration** | `035-event-driven-data-integration.md` |
| 036 | **Change Data Capture Architecture** | `036-change-data-capture-architecture.md` |
| 037 | **Batch and File Exchange** | `037-batch-and-file-exchange.md` |
| 038 | **Federation and Virtualization** | `038-federation-and-virtualization.md` |
| 039 | **Replication and Synchronization** | `039-replication-and-synchronization.md` |
| 040 | **Choosing an Integration Style from Semantics and Latency** | `040-choosing-an-integration-style-from-semantics-and-latency.md` |

### Block 05 — Analytical and Platform Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Enterprise Data Warehouse Architecture** | `041-enterprise-data-warehouse-architecture.md` |
| 042 | **Data Lake Architecture** | `042-data-lake-architecture.md` |
| 043 | **Lakehouse Architecture** | `043-lakehouse-architecture.md` |
| 044 | **Data Mart Strategies** | `044-data-mart-strategies.md` |
| 045 | **Semantic and Metrics Layers** | `045-semantic-and-metrics-layers.md` |
| 046 | **Operational Data Stores** | `046-operational-data-stores.md` |
| 047 | **Streaming Analytics Architecture** | `047-streaming-analytics-architecture.md` |
| 048 | **Feature and Training Data Architecture** | `048-feature-and-training-data-architecture.md` |
| 049 | **Self-Service Analytics Boundaries** | `049-self-service-analytics-boundaries.md` |
| 050 | **Mapping Data Workloads to Platforms and Serving Systems** | `050-mapping-data-workloads-to-platforms-and-serving-systems.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Master, Reference, and Shared Data

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Master Data and Golden Records** | `051-master-data-and-golden-records.md` |
| 052 | **Reference Data** | `052-reference-data.md` |
| 053 | **Identity Resolution** | `053-identity-resolution.md` |
| 054 | **Match, Merge, and Survivorship** | `054-match-merge-and-survivorship.md` |
| 055 | **Registry, Consolidation, and Coexistence Styles** | `055-registry-consolidation-and-coexistence-styles.md` |
| 056 | **Hierarchy Management** | `056-hierarchy-management.md` |
| 057 | **Shared Code Sets and Controlled Vocabularies** | `057-shared-code-sets-and-controlled-vocabularies.md` |
| 058 | **Master-Data Change Propagation** | `058-master-data-change-propagation.md` |
| 059 | **Governance of Shared Data** | `059-governance-of-shared-data.md` |
| 060 | **Designing an MDM Capability Without Centralizing Every Domain** | `060-designing-an-mdm-capability-without-centralizing-every-domain.md` |

### Block 07 — Metadata, Semantics, and Knowledge Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Metadata Architecture** | `061-metadata-architecture.md` |
| 062 | **Metadata Harvesting and Synchronization** | `062-metadata-harvesting-and-synchronization.md` |
| 063 | **Business Glossaries and Term Governance** | `063-business-glossaries-and-term-governance.md` |
| 064 | **Lineage Architecture** | `064-lineage-architecture.md` |
| 065 | **Ontologies and Knowledge Graphs** | `065-ontologies-and-knowledge-graphs.md` |
| 066 | **Semantic Interoperability** | `066-semantic-interoperability.md` |
| 067 | **Schema Registries** | `067-schema-registries.md` |
| 068 | **Data Catalog Architecture** | `068-data-catalog-architecture.md` |
| 069 | **Metadata APIs and Eventing** | `069-metadata-apis-and-eventing.md` |
| 070 | **Connecting Technical Metadata to Business Meaning** | `070-connecting-technical-metadata-to-business-meaning.md` |

### Block 08 — Governance, Privacy, and Lifecycle Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Federated Data Governance** | `071-federated-data-governance.md` |
| 072 | **Policy as Code for Data** | `072-policy-as-code-for-data.md` |
| 073 | **Classification Architecture** | `073-classification-architecture.md` |
| 074 | **Consent and Purpose Limitation** | `074-consent-and-purpose-limitation.md` |
| 075 | **Data Residency and Sovereignty** | `075-data-residency-and-sovereignty.md` |
| 076 | **Retention and Legal Hold** | `076-retention-and-legal-hold.md` |
| 077 | **Deletion and the Right to Erasure** | `077-deletion-and-the-right-to-erasure.md` |
| 078 | **Masking, Tokenization, and Clean Rooms** | `078-masking-tokenization-and-clean-rooms.md` |
| 079 | **Audit and Provenance Architecture** | `079-audit-and-provenance-architecture.md` |
| 080 | **Embedding Governance into Data Flows and Products** | `080-embedding-governance-into-data-flows-and-products.md` |

### Block 09 — Data Mesh, Fabric, and Federated Architectures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Data Mesh Principles** | `081-data-mesh-principles.md` |
| 082 | **Domain-Oriented Decentralization** | `082-domain-oriented-decentralization.md` |
| 083 | **Self-Serve Data Platform Capabilities** | `083-self-serve-data-platform-capabilities.md` |
| 084 | **Federated Computational Governance** | `084-federated-computational-governance.md` |
| 085 | **Data Fabric Concepts** | `085-data-fabric-concepts.md` |
| 086 | **Active Metadata** | `086-active-metadata.md` |
| 087 | **Federated Query and Data Virtualization** | `087-federated-query-and-data-virtualization.md` |
| 088 | **Data Sharing Across Organizations** | `088-data-sharing-across-organizations.md` |
| 089 | **Interoperability Without a Universal Model** | `089-interoperability-without-a-universal-model.md` |
| 090 | **Evaluating Mesh, Fabric, Warehouse, and Hybrid Options** | `090-evaluating-mesh-fabric-warehouse-and-hybrid-options.md` |

### Block 10 — Modernization, Roadmaps, and Architecture Governance

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Assessing Data Architecture Maturity** | `091-assessing-data-architecture-maturity.md` |
| 092 | **Target-State Architecture** | `092-target-state-architecture.md` |
| 093 | **Transition Architectures** | `093-transition-architectures.md` |
| 094 | **Warehouse and Lake Modernization** | `094-warehouse-and-lake-modernization.md` |
| 095 | **Legacy Integration Retirement** | `095-legacy-integration-retirement.md` |
| 096 | **Cloud Data Migration** | `096-cloud-data-migration.md` |
| 097 | **Data Contract Migration** | `097-data-contract-migration.md` |
| 098 | **Architecture Standards and Reference Patterns** | `098-architecture-standards-and-reference-patterns.md` |
| 099 | **Data Architecture Metrics and Fitness Functions** | `099-data-architecture-metrics-and-fitness-functions.md` |
| 100 | **Defending a Multi-Year Data Architecture Roadmap** | `100-defending-a-multi-year-data-architecture-roadmap.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
