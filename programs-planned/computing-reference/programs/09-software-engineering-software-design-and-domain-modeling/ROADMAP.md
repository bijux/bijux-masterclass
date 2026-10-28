# 09. Software Engineering: Software Design & Domain Modeling

**Program code:** `SDDM`

**Purpose:** Develop the ability to turn ambiguous domain knowledge and changing requirements into precise, modular, testable software models.

**Level-II professional outcome:** Ready to lead code- and component-level design, facilitate domain discovery, define boundaries and contracts, and evolve models in business-critical software.

**Prerequisites:** programming proficiency; OOP or FP foundations; testing fundamentals; basic software construction.

**Primary ownership:** problem framing; modularity; responsibility design; domain modeling; DDD tactical and strategic modeling; contracts and invariants; state and workflow models; boundary design; model evolution; design review.

**Explicit exclusions:** pattern catalogue ownership (Program 11); system-wide architecture (Program 12); project methodology (Program 10); database physical design (Program 18).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — From Problem to Software Model

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Distinguishing the Problem Domain from the Solution Domain** | `001-distinguishing-the-problem-domain-from-the-solution-domain.md` |
| 002 | **Stakeholders, Goals, and Observable Outcomes** | `002-stakeholders-goals-and-observable-outcomes.md` |
| 003 | **Domain Language and Terminology** | `003-domain-language-and-terminology.md` |
| 004 | **Use Cases, Scenarios, and Examples** | `004-use-cases-scenarios-and-examples.md` |
| 005 | **Commands, Queries, Events, and Policies** | `005-commands-queries-events-and-policies.md` |
| 006 | **Business Rules and Decision Logic** | `006-business-rules-and-decision-logic.md` |
| 007 | **Finding Invariants** | `007-finding-invariants.md` |
| 008 | **Identifying State and Lifecycle** | `008-identifying-state-and-lifecycle.md` |
| 009 | **Modeling Failure and Exceptional Cases** | `009-modeling-failure-and-exceptional-cases.md` |
| 010 | **Testing a Model Against Real Scenarios** | `010-testing-a-model-against-real-scenarios.md` |

### Block 02 — Modularity and Responsibility

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Information Hiding as a Design Principle** | `011-information-hiding-as-a-design-principle.md` |
| 012 | **Cohesion and Reasons to Change** | `012-cohesion-and-reasons-to-change.md` |
| 013 | **Coupling and Dependency Direction** | `013-coupling-and-dependency-direction.md` |
| 014 | **Responsibility Assignment** | `014-responsibility-assignment.md` |
| 015 | **Encapsulation of Volatile Decisions** | `015-encapsulation-of-volatile-decisions.md` |
| 016 | **Interfaces and Behavioral Contracts** | `016-interfaces-and-behavioral-contracts.md` |
| 017 | **Composition and Delegation** | `017-composition-and-delegation.md` |
| 018 | **Dependency Inversion at Component Scale** | `018-dependency-inversion-at-component-scale.md` |
| 019 | **Stable and Unstable Dependencies** | `019-stable-and-unstable-dependencies.md` |
| 020 | **Restructuring a Design Around Clear Responsibilities** | `020-restructuring-a-design-around-clear-responsibilities.md` |

### Block 03 — Entities, Values, and Aggregates

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Entity Identity and Continuity** | `021-entity-identity-and-continuity.md` |
| 022 | **Value Objects and Semantic Equality** | `022-value-objects-and-semantic-equality.md` |
| 023 | **Immutability and Valid Construction** | `023-immutability-and-valid-construction.md` |
| 024 | **Aggregate Boundaries** | `024-aggregate-boundaries.md` |
| 025 | **Aggregate Roots and Access Control** | `025-aggregate-roots-and-access-control.md` |
| 026 | **Consistency Within an Aggregate** | `026-consistency-within-an-aggregate.md` |
| 027 | **Repositories as Domain-Facing Collections** | `027-repositories-as-domain-facing-collections.md` |
| 028 | **Domain Services** | `028-domain-services.md` |
| 029 | **Factories and Complex Creation** | `029-factories-and-complex-creation.md` |
| 030 | **Reviewing Aggregate Size and Transaction Boundaries** | `030-reviewing-aggregate-size-and-transaction-boundaries.md` |

### Block 04 — State, Behavior, and Workflow Modeling

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **State Machines for Domain Lifecycles** | `031-state-machines-for-domain-lifecycles.md` |
| 032 | **Transition Guards and Invariants** | `032-transition-guards-and-invariants.md` |
| 033 | **Temporal Rules and Deadlines** | `033-temporal-rules-and-deadlines.md` |
| 034 | **Long-Running Workflows** | `034-long-running-workflows.md` |
| 035 | **Compensating Actions** | `035-compensating-actions.md` |
| 036 | **Idempotent Commands** | `036-idempotent-commands.md` |
| 037 | **Domain Events** | `037-domain-events.md` |
| 038 | **Event Ordering and Causality** | `038-event-ordering-and-causality.md` |
| 039 | **Process Managers and Sagas as Domain Coordination** | `039-process-managers-and-sagas-as-domain-coordination.md` |
| 040 | **Modeling a Workflow Without Boolean-State Explosion** | `040-modeling-a-workflow-without-boolean-state-explosion.md` |

### Block 05 — Boundaries and Integration Models

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Application, Domain, and Infrastructure Boundaries** | `041-application-domain-and-infrastructure-boundaries.md` |
| 042 | **Ports and Adapters at Design Scale** | `042-ports-and-adapters-at-design-scale.md` |
| 043 | **DTOs and Boundary-Specific Representations** | `043-dtos-and-boundary-specific-representations.md` |
| 044 | **Anti-Corruption Layers** | `044-anti-corruption-layers.md` |
| 045 | **Translation Between Domain Models** | `045-translation-between-domain-models.md` |
| 046 | **External Service Contracts** | `046-external-service-contracts.md` |
| 047 | **Persistence Ignorance and Practical Limits** | `047-persistence-ignorance-and-practical-limits.md` |
| 048 | **Domain and Application Transaction Boundaries** | `048-domain-and-application-transaction-boundaries.md` |
| 049 | **Error Translation Across Boundaries** | `049-error-translation-across-boundaries.md` |
| 050 | **Designing a Replaceable Integration** | `050-designing-a-replaceable-integration.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Domain Discovery and Collaborative Modeling

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Event Storming** | `051-event-storming.md` |
| 052 | **Example Mapping** | `052-example-mapping.md` |
| 053 | **Domain Storytelling** | `053-domain-storytelling.md` |
| 054 | **Business Capability Mapping** | `054-business-capability-mapping.md` |
| 055 | **Decision Modeling** | `055-decision-modeling.md` |
| 056 | **Impact Mapping** | `056-impact-mapping.md` |
| 057 | **Modeling Uncertainty and Open Questions** | `057-modeling-uncertainty-and-open-questions.md` |
| 058 | **Reconciling Conflicting Stakeholder Models** | `058-reconciling-conflicting-stakeholder-models.md` |
| 059 | **Capturing Assumptions and Evidence** | `059-capturing-assumptions-and-evidence.md` |
| 060 | **Turning a Discovery Workshop into Design Decisions** | `060-turning-a-discovery-workshop-into-design-decisions.md` |

### Block 07 — Strategic Domain Design

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Subdomains: Core, Supporting, and Generic** | `061-subdomains-core-supporting-and-generic.md` |
| 062 | **Bounded Contexts** | `062-bounded-contexts.md` |
| 063 | **Context Maps** | `063-context-maps.md` |
| 064 | **Partnership and Shared-Kernel Relationships** | `064-partnership-and-shared-kernel-relationships.md` |
| 065 | **Customer-Supplier and Conformist Relationships** | `065-customer-supplier-and-conformist-relationships.md` |
| 066 | **Open Host Services and Published Languages** | `066-open-host-services-and-published-languages.md` |
| 067 | **Separate Ways and Deliberate Duplication** | `067-separate-ways-and-deliberate-duplication.md` |
| 068 | **Team Boundaries and Cognitive Load** | `068-team-boundaries-and-cognitive-load.md` |
| 069 | **Evaluating Context Boundary Quality** | `069-evaluating-context-boundary-quality.md` |
| 070 | **Evolving a Context Map as the Organization Changes** | `070-evolving-a-context-map-as-the-organization-changes.md` |

### Block 08 — Advanced Domain Representation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Temporal Models and Effective-Dated Facts** | `071-temporal-models-and-effective-dated-facts.md` |
| 072 | **Bitemporal Domain Information** | `072-bitemporal-domain-information.md` |
| 073 | **Rules Engines Versus Explicit Domain Logic** | `073-rules-engines-versus-explicit-domain-logic.md` |
| 074 | **Constraint-Rich Models** | `074-constraint-rich-models.md` |
| 075 | **Quantity, Units, and Dimensional Correctness** | `075-quantity-units-and-dimensional-correctness.md` |
| 076 | **Money, Rounding, and Accounting Invariants** | `076-money-rounding-and-accounting-invariants.md` |
| 077 | **Authorization as a Domain Concern** | `077-authorization-as-a-domain-concern.md` |
| 078 | **Probabilistic and Incomplete Domain Facts** | `078-probabilistic-and-incomplete-domain-facts.md` |
| 079 | **Versioned Domain Concepts** | `079-versioned-domain-concepts.md` |
| 080 | **Modeling Domains That Resist Simple CRUD** | `080-modeling-domains-that-resist-simple-crud.md` |

### Block 09 — Model Evolution and Legacy Domains

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Detecting Model Drift** | `081-detecting-model-drift.md` |
| 082 | **Renaming Concepts Safely** | `082-renaming-concepts-safely.md` |
| 083 | **Splitting an Overgrown Model** | `083-splitting-an-overgrown-model.md` |
| 084 | **Merging Duplicate Concepts** | `084-merging-duplicate-concepts.md` |
| 085 | **Introducing Value Objects into Primitive-Heavy Code** | `085-introducing-value-objects-into-primitive-heavy-code.md` |
| 086 | **Extracting Domain Logic from Framework Code** | `086-extracting-domain-logic-from-framework-code.md` |
| 087 | **Strangling a Legacy Domain Model** | `087-strangling-a-legacy-domain-model.md` |
| 088 | **Migrating Persistent Representations** | `088-migrating-persistent-representations.md` |
| 089 | **Maintaining Compatibility During Model Change** | `089-maintaining-compatibility-during-model-change.md` |
| 090 | **Using Production Evidence to Revise a Domain Model** | `090-using-production-evidence-to-revise-a-domain-model.md` |

### Block 10 — Design Judgment and Review

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Designing for Testability Without Test-Induced Distortion** | `091-designing-for-testability-without-test-induced-distortion.md` |
| 092 | **Balancing Abstraction and Directness** | `092-balancing-abstraction-and-directness.md` |
| 093 | **Recognizing Anemic and Overengineered Models** | `093-recognizing-anemic-and-overengineered-models.md` |
| 094 | **Assessing Model-to-Code Fidelity** | `094-assessing-model-to-code-fidelity.md` |
| 095 | **Reviewing Dependency and Ownership Graphs** | `095-reviewing-dependency-and-ownership-graphs.md` |
| 096 | **Evaluating Consistency and Transaction Choices** | `096-evaluating-consistency-and-transaction-choices.md` |
| 097 | **Explaining Design Trade-Offs to Non-Specialists** | `097-explaining-design-trade-offs-to-non-specialists.md` |
| 098 | **Recording Design Rationale** | `098-recording-design-rationale.md` |
| 099 | **Comparing Competing Models for the Same Domain** | `099-comparing-competing-models-for-the-same-domain.md` |
| 100 | **Conducting an Adversarial Software Design Review** | `100-conducting-an-adversarial-software-design-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
