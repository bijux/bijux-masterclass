# 13. Software Engineering: Testing & Quality Engineering

**Program code:** `STQE`

**Purpose:** Develop rigorous, economical approaches for evaluating software behavior, preventing defects, diagnosing failures, and making quality visible across the lifecycle.

**Level-II professional outcome:** Ready to design and lead testing strategies, build reliable automation, test distributed and data-intensive systems, and improve organizational quality engineering.

**Prerequisites:** software construction; basic design and architecture; version control and CI familiarity.

**Primary ownership:** test theory; unit and component testing; integration and system testing; test design; property and model-based testing; fuzzing and mutation; performance and security testing; test automation architecture; quality models and metrics; defect prevention.

**Explicit exclusions:** delivery pipelines (Program 14); formal proof theory (Program 07); security architecture (Program 25); domain design ownership (Program 09).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Testing Foundations and Oracles

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Why Software Testing Cannot Prove Absence of Defects** | `001-why-software-testing-cannot-prove-absence-of-defects.md` |
| 002 | **Specifications, Expectations, and Test Oracles** | `002-specifications-expectations-and-test-oracles.md` |
| 003 | **Verification, Validation, and Fitness for Purpose** | `003-verification-validation-and-fitness-for-purpose.md` |
| 004 | **Test Levels and Test Types** | `004-test-levels-and-test-types.md` |
| 005 | **Black-Box, White-Box, and Gray-Box Testing** | `005-black-box-white-box-and-gray-box-testing.md` |
| 006 | **Positive, Negative, and Boundary Testing** | `006-positive-negative-and-boundary-testing.md` |
| 007 | **Determinism, Repeatability, and Isolation** | `007-determinism-repeatability-and-isolation.md` |
| 008 | **Defects, Failures, Root Causes, and Symptoms** | `008-defects-failures-root-causes-and-symptoms.md` |
| 009 | **Risk-Based Test Selection** | `009-risk-based-test-selection.md` |
| 010 | **Writing a Test Strategy from Quality Risks** | `010-writing-a-test-strategy-from-quality-risks.md` |

### Block 02 — Unit and Component Testing

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Unit Boundaries and Observable Behavior** | `011-unit-boundaries-and-observable-behavior.md` |
| 012 | **Arrange-Act-Assert and Alternative Test Structures** | `012-arrange-act-assert-and-alternative-test-structures.md` |
| 013 | **State-Based and Interaction-Based Testing** | `013-state-based-and-interaction-based-testing.md` |
| 014 | **Test Doubles: Stubs, Fakes, Spies, and Mocks** | `014-test-doubles-stubs-fakes-spies-and-mocks.md` |
| 015 | **Dependency Control and Test Seams** | `015-dependency-control-and-test-seams.md` |
| 016 | **Testing Exceptions and Error Paths** | `016-testing-exceptions-and-error-paths.md` |
| 017 | **Testing Time, Randomness, and Environment** | `017-testing-time-randomness-and-environment.md` |
| 018 | **Table-Driven and Parameterized Tests** | `018-table-driven-and-parameterized-tests.md` |
| 019 | **Readable Test Names and Failure Messages** | `019-readable-test-names-and-failure-messages.md` |
| 020 | **Refactoring a Brittle Unit-Test Suite** | `020-refactoring-a-brittle-unit-test-suite.md` |

### Block 03 — Test Design Techniques

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Equivalence Partitioning** | `021-equivalence-partitioning.md` |
| 022 | **Boundary-Value Analysis** | `022-boundary-value-analysis.md` |
| 023 | **Decision-Table Testing** | `023-decision-table-testing.md` |
| 024 | **State-Transition Testing** | `024-state-transition-testing.md` |
| 025 | **Pairwise and Combinatorial Testing** | `025-pairwise-and-combinatorial-testing.md` |
| 026 | **Cause-Effect Graphing** | `026-cause-effect-graphing.md` |
| 027 | **Use-Case and Scenario Testing** | `027-use-case-and-scenario-testing.md` |
| 028 | **Coverage Criteria** | `028-coverage-criteria.md` |
| 029 | **Data-Flow Testing** | `029-data-flow-testing.md` |
| 030 | **Deriving a Compact Test Set from a Complex Specification** | `030-deriving-a-compact-test-set-from-a-complex-specification.md` |

### Block 04 — Integration, Contract, and System Testing

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Integration Boundaries and Failure Surfaces** | `031-integration-boundaries-and-failure-surfaces.md` |
| 032 | **Bottom-Up, Top-Down, and Incremental Integration** | `032-bottom-up-top-down-and-incremental-integration.md` |
| 033 | **Consumer-Driven Contract Testing** | `033-consumer-driven-contract-testing.md` |
| 034 | **Database Integration Testing** | `034-database-integration-testing.md` |
| 035 | **File and Message Integration Testing** | `035-file-and-message-integration-testing.md` |
| 036 | **API and Protocol Testing** | `036-api-and-protocol-testing.md` |
| 037 | **End-to-End Testing and Its Cost** | `037-end-to-end-testing-and-its-cost.md` |
| 038 | **Acceptance Testing** | `038-acceptance-testing.md` |
| 039 | **Environment Parity and Test Containers** | `039-environment-parity-and-test-containers.md` |
| 040 | **Designing a Layered Test Portfolio** | `040-designing-a-layered-test-portfolio.md` |

### Block 05 — Automation Reliability and Test Operations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Test Discovery and Execution Models** | `041-test-discovery-and-execution-models.md` |
| 042 | **Fixtures, Setup, and Teardown** | `042-fixtures-setup-and-teardown.md` |
| 043 | **Test Data Builders and Factories** | `043-test-data-builders-and-factories.md` |
| 044 | **Parallel Test Execution** | `044-parallel-test-execution.md` |
| 045 | **Flaky Tests and Nondeterminism** | `045-flaky-tests-and-nondeterminism.md` |
| 046 | **Quarantine, Ownership, and Repair** | `046-quarantine-ownership-and-repair.md` |
| 047 | **Test Runtime and Feedback Speed** | `047-test-runtime-and-feedback-speed.md` |
| 048 | **Failure Triage and Artifact Collection** | `048-failure-triage-and-artifact-collection.md` |
| 049 | **Test-Suite Maintenance** | `049-test-suite-maintenance.md` |
| 050 | **Building Trust in an Automated Test Pipeline** | `050-building-trust-in-an-automated-test-pipeline.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Property, Model, and Metamorphic Testing

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Properties Versus Examples** | `051-properties-versus-examples.md` |
| 052 | **Generators and Shrinking** | `052-generators-and-shrinking.md` |
| 053 | **Stateful Property-Based Testing** | `053-stateful-property-based-testing.md` |
| 054 | **Algebraic Laws as Test Properties** | `054-algebraic-laws-as-test-properties.md` |
| 055 | **Model-Based Testing** | `055-model-based-testing.md` |
| 056 | **Finite-State Models** | `056-finite-state-models.md` |
| 057 | **Metamorphic Relations** | `057-metamorphic-relations.md` |
| 058 | **Differential Testing** | `058-differential-testing.md` |
| 059 | **Round-Trip and Inverse Properties** | `059-round-trip-and-inverse-properties.md` |
| 060 | **Designing Properties for a Stateful API** | `060-designing-properties-for-a-stateful-api.md` |

### Block 07 — Mutation, Fuzzing, and Robustness Testing

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Mutation Testing and Test-Suite Sensitivity** | `061-mutation-testing-and-test-suite-sensitivity.md` |
| 062 | **Equivalent and Surviving Mutants** | `062-equivalent-and-surviving-mutants.md` |
| 063 | **Coverage-Guided Fuzzing** | `063-coverage-guided-fuzzing.md` |
| 064 | **Grammar-Based Fuzzing** | `064-grammar-based-fuzzing.md` |
| 065 | **Structure-Aware Fuzzing** | `065-structure-aware-fuzzing.md` |
| 066 | **Corpus Management and Minimization** | `066-corpus-management-and-minimization.md` |
| 067 | **Fault Injection** | `067-fault-injection.md` |
| 068 | **Chaos Experiments Versus Tests** | `068-chaos-experiments-versus-tests.md` |
| 069 | **Robustness Against Malformed and Hostile Inputs** | `069-robustness-against-malformed-and-hostile-inputs.md` |
| 070 | **Combining Mutation and Fuzzing to Expose Weak Oracles** | `070-combining-mutation-and-fuzzing-to-expose-weak-oracles.md` |

### Block 08 — Specialized System Testing

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Concurrency Testing and Schedule Exploration** | `071-concurrency-testing-and-schedule-exploration.md` |
| 072 | **Distributed-System Testing** | `072-distributed-system-testing.md` |
| 073 | **Time, Retry, and Failure Simulation** | `073-time-retry-and-failure-simulation.md` |
| 074 | **Performance Load, Stress, Spike, and Soak Testing** | `074-performance-load-stress-spike-and-soak-testing.md` |
| 075 | **Capacity and Scalability Testing** | `075-capacity-and-scalability-testing.md` |
| 076 | **Security Testing and Abuse Cases** | `076-security-testing-and-abuse-cases.md` |
| 077 | **Data Pipeline Reconciliation Testing** | `077-data-pipeline-reconciliation-testing.md` |
| 078 | **Database Migration Testing** | `078-database-migration-testing.md` |
| 079 | **Compatibility and Upgrade Testing** | `079-compatibility-and-upgrade-testing.md` |
| 080 | **Testing Recovery, Backup, and Disaster Procedures** | `080-testing-recovery-backup-and-disaster-procedures.md` |

### Block 09 — Quality Models, Measurement, and Analysis

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Product Quality Models** | `081-product-quality-models.md` |
| 082 | **Process Quality and Prevention** | `082-process-quality-and-prevention.md` |
| 083 | **Defect Taxonomies** | `083-defect-taxonomies.md` |
| 084 | **Escaped Defects and Detection Effectiveness** | `084-escaped-defects-and-detection-effectiveness.md` |
| 085 | **Coverage as Evidence and Its Limits** | `085-coverage-as-evidence-and-its-limits.md` |
| 086 | **Static Analysis Findings and Signal Quality** | `086-static-analysis-findings-and-signal-quality.md` |
| 087 | **Reliability Growth Models** | `087-reliability-growth-models.md` |
| 088 | **Quality Cost: Prevention, Appraisal, and Failure** | `088-quality-cost-prevention-appraisal-and-failure.md` |
| 089 | **Using Production Incidents to Improve Tests** | `089-using-production-incidents-to-improve-tests.md` |
| 090 | **Creating a Quality Scorecard Without Metric Gaming** | `090-creating-a-quality-scorecard-without-metric-gaming.md` |

### Block 10 — Advanced Quality Engineering Leadership

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Testability as an Architectural Quality** | `091-testability-as-an-architectural-quality.md` |
| 092 | **Testing Strategies for Legacy Systems** | `092-testing-strategies-for-legacy-systems.md` |
| 093 | **Testing Microservices Without End-to-End Dependence** | `093-testing-microservices-without-end-to-end-dependence.md` |
| 094 | **Test Platforms and Shared Quality Capabilities** | `094-test-platforms-and-shared-quality-capabilities.md` |
| 095 | **Governance for Critical and Regulated Software** | `095-governance-for-critical-and-regulated-software.md` |
| 096 | **Independent Verification and Validation** | `096-independent-verification-and-validation.md` |
| 097 | **Quality Gates and Risk Acceptance** | `097-quality-gates-and-risk-acceptance.md` |
| 098 | **Reviewing Tests as Production Code** | `098-reviewing-tests-as-production-code.md` |
| 099 | **Balancing Speed, Confidence, and Cost** | `099-balancing-speed-confidence-and-cost.md` |
| 100 | **Conducting an Adversarial Quality-Engineering Review** | `100-conducting-an-adversarial-quality-engineering-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
