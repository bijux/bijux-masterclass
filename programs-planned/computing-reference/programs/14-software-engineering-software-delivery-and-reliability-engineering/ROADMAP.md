# 14. Software Engineering: Software Delivery & Reliability Engineering

**Program code:** `SDRE`

**Purpose:** Develop the engineering discipline required to turn source changes into safe production releases and keep services reliable under change, load, dependency failure, and operator error.

**Level-II professional outcome:** Ready to design CI/CD systems, release strategies, observability, SLOs, incident response, resilience mechanisms, and reliability programs for production services.

**Prerequisites:** software engineering experience; basic networking, systems, and cloud knowledge; testing fundamentals.

**Primary ownership:** build and artifact engineering; continuous integration and delivery; release and deployment safety; observability; SRE; incident management; resilience engineering; capacity and overload; disaster recovery; software supply-chain delivery.

**Explicit exclusions:** cloud resource design (Program 30); platform product construction (Program 29); testing technique ownership (Program 13); security engineering ownership (Program 25).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Builds, Artifacts, and Release Inputs

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **From Source Change to Deployable Artifact** | `001-from-source-change-to-deployable-artifact.md` |
| 002 | **Dependency Resolution and Locking** | `002-dependency-resolution-and-locking.md` |
| 003 | **Reproducible and Hermetic Builds** | `003-reproducible-and-hermetic-builds.md` |
| 004 | **Incremental Builds and Caching** | `004-incremental-builds-and-caching.md` |
| 005 | **Artifact Repositories** | `005-artifact-repositories.md` |
| 006 | **Semantic Versioning and Release Identity** | `006-semantic-versioning-and-release-identity.md` |
| 007 | **Build Metadata and Provenance** | `007-build-metadata-and-provenance.md` |
| 008 | **Generating and Verifying Software Bills of Materials** | `008-generating-and-verifying-software-bills-of-materials.md` |
| 009 | **Artifact Signing and Verification** | `009-artifact-signing-and-verification.md` |
| 010 | **Designing an Auditable Build Pipeline** | `010-designing-an-auditable-build-pipeline.md` |

### Block 02 — Continuous Integration

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Continuous Integration as a Working Practice** | `011-continuous-integration-as-a-working-practice.md` |
| 012 | **Trunk-Based Development** | `012-trunk-based-development.md` |
| 013 | **Branching Strategies and Integration Delay** | `013-branching-strategies-and-integration-delay.md` |
| 014 | **Change Detection and Selective Execution** | `014-change-detection-and-selective-execution.md` |
| 015 | **Parallelizing CI Workloads** | `015-parallelizing-ci-workloads.md` |
| 016 | **Merge Queues** | `016-merge-queues.md` |
| 017 | **Quality Gates** | `017-quality-gates.md` |
| 018 | **Handling Flaky CI** | `018-handling-flaky-ci.md` |
| 019 | **CI Secrets and Untrusted Contributions** | `019-ci-secrets-and-untrusted-contributions.md` |
| 020 | **Optimizing Feedback Time Without Hiding Risk** | `020-optimizing-feedback-time-without-hiding-risk.md` |

### Block 03 — Continuous Delivery and Deployment

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Continuous Delivery Versus Continuous Deployment** | `021-continuous-delivery-versus-continuous-deployment.md` |
| 022 | **Environment Promotion** | `022-environment-promotion.md` |
| 023 | **Configuration and Secret Separation** | `023-configuration-and-secret-separation.md` |
| 024 | **Database Change Delivery** | `024-database-change-delivery.md` |
| 025 | **Blue-Green Deployment** | `025-blue-green-deployment.md` |
| 026 | **Canary Deployment** | `026-canary-deployment.md` |
| 027 | **Rolling Deployment** | `027-rolling-deployment.md` |
| 028 | **Feature Flags** | `028-feature-flags.md` |
| 029 | **Automated Rollback and Roll Forward** | `029-automated-rollback-and-roll-forward.md` |
| 030 | **Designing a Safe Release Pipeline** | `030-designing-a-safe-release-pipeline.md` |

### Block 04 — Observability Foundations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Observability Versus Monitoring** | `031-observability-versus-monitoring.md` |
| 032 | **Structured Logging** | `032-structured-logging.md` |
| 033 | **Metrics and Dimensionality** | `033-metrics-and-dimensionality.md` |
| 034 | **Distributed Tracing** | `034-distributed-tracing.md` |
| 035 | **Events and Change Annotations** | `035-events-and-change-annotations.md` |
| 036 | **Correlation and Context Propagation** | `036-correlation-and-context-propagation.md` |
| 037 | **Dashboards for Questions, Not Decoration** | `037-dashboards-for-questions-not-decoration.md` |
| 038 | **Alerting and Actionability** | `038-alerting-and-actionability.md` |
| 039 | **Telemetry Sampling and Cost** | `039-telemetry-sampling-and-cost.md` |
| 040 | **Instrumenting a Service for Diagnosis** | `040-instrumenting-a-service-for-diagnosis.md` |

### Block 05 — Reliability Foundations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Reliability, Availability, and Durability** | `041-reliability-availability-and-durability.md` |
| 042 | **Service-Level Indicators** | `042-service-level-indicators.md` |
| 043 | **Service-Level Objectives** | `043-service-level-objectives.md` |
| 044 | **Service-Level Agreements** | `044-service-level-agreements.md` |
| 045 | **Error Budgets** | `045-error-budgets.md` |
| 046 | **Toil and Automation** | `046-toil-and-automation.md` |
| 047 | **Failure Domains** | `047-failure-domains.md` |
| 048 | **Redundancy and Diversity** | `048-redundancy-and-diversity.md` |
| 049 | **Graceful Degradation** | `049-graceful-degradation.md` |
| 050 | **Writing a Production-Readiness Review** | `050-writing-a-production-readiness-review.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Incident Detection and Response

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Incident Severity and Classification** | `051-incident-severity-and-classification.md` |
| 052 | **On-Call Design** | `052-on-call-design.md` |
| 053 | **Operational Alert Triage** | `053-operational-alert-triage.md` |
| 054 | **Incident Command** | `054-incident-command.md` |
| 055 | **Technical Investigation Under Pressure** | `055-technical-investigation-under-pressure.md` |
| 056 | **Mitigation Before Root Cause** | `056-mitigation-before-root-cause.md` |
| 057 | **Status Communication** | `057-status-communication.md` |
| 058 | **Evidence Preservation and Timelines** | `058-evidence-preservation-and-timelines.md` |
| 059 | **Blameless Post-Incident Analysis** | `059-blameless-post-incident-analysis.md` |
| 060 | **Turning Incident Findings into Verified Improvements** | `060-turning-incident-findings-into-verified-improvements.md` |

### Block 07 — Resilience and Overload Engineering

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Timeout Budgets and Deadline Propagation** | `061-timeout-budgets-and-deadline-propagation.md` |
| 062 | **Retries, Backoff, and Jitter** | `062-retries-backoff-and-jitter.md` |
| 063 | **Idempotency Under Retry** | `063-idempotency-under-retry.md` |
| 064 | **Circuit Breakers** | `064-circuit-breakers.md` |
| 065 | **Bulkheads and Failure Containment** | `065-bulkheads-and-failure-containment.md` |
| 066 | **Rate Limiting and Quotas** | `066-rate-limiting-and-quotas.md` |
| 067 | **Engineering Load Shedding** | `067-engineering-load-shedding.md` |
| 068 | **Backpressure for Overload Control** | `068-backpressure-for-overload-control.md` |
| 069 | **Queue Stability and Admission Control** | `069-queue-stability-and-admission-control.md` |
| 070 | **Preventing Retry Storms and Cascading Failure** | `070-preventing-retry-storms-and-cascading-failure.md` |

### Block 08 — Capacity, Performance, and Efficiency

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Workload Characterization** | `071-workload-characterization.md` |
| 072 | **Capacity Models** | `072-capacity-models.md` |
| 073 | **Latency Distributions and Tail Behavior** | `073-latency-distributions-and-tail-behavior.md` |
| 074 | **Concurrency Limits** | `074-concurrency-limits.md` |
| 075 | **Saturation Signals** | `075-saturation-signals.md` |
| 076 | **Autoscaling Inputs and Delays** | `076-autoscaling-inputs-and-delays.md` |
| 077 | **Headroom and Safety Margins** | `077-headroom-and-safety-margins.md` |
| 078 | **Cost per Request and Unit Economics** | `078-cost-per-request-and-unit-economics.md` |
| 079 | **Performance Regression Detection** | `079-performance-regression-detection.md` |
| 080 | **Planning Capacity for Growth and Failure** | `080-planning-capacity-for-growth-and-failure.md` |

### Block 09 — Recovery and Continuity

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Recovery Point and Recovery Time Objectives** | `081-recovery-point-and-recovery-time-objectives.md` |
| 082 | **Backup Design** | `082-backup-design.md` |
| 083 | **Restore Verification** | `083-restore-verification.md` |
| 084 | **Point-in-Time Recovery** | `084-point-in-time-recovery.md` |
| 085 | **Dependency Failure Plans** | `085-dependency-failure-plans.md` |
| 086 | **Regional Evacuation** | `086-regional-evacuation.md` |
| 087 | **Operational Multi-Region Failover** | `087-operational-multi-region-failover.md` |
| 088 | **Disaster-Recovery Exercises** | `088-disaster-recovery-exercises.md` |
| 089 | **Business Continuity and Manual Operation** | `089-business-continuity-and-manual-operation.md` |
| 090 | **Auditing Recoverability Rather Than Backup Presence** | `090-auditing-recoverability-rather-than-backup-presence.md` |

### Block 10 — Advanced Delivery and Reliability Systems

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Progressive Delivery with Automated Analysis** | `091-progressive-delivery-with-automated-analysis.md` |
| 092 | **Release Orchestration Across Services** | `092-release-orchestration-across-services.md` |
| 093 | **Compatibility Windows and Coordinated Upgrades** | `093-compatibility-windows-and-coordinated-upgrades.md` |
| 094 | **Supply-Chain Policy Enforcement** | `094-supply-chain-policy-enforcement.md` |
| 095 | **Reliability Testing in Production** | `095-reliability-testing-in-production.md` |
| 096 | **Chaos Engineering with Explicit Hypotheses** | `096-chaos-engineering-with-explicit-hypotheses.md` |
| 097 | **Reliability Governance and Error-Budget Policy** | `097-reliability-governance-and-error-budget-policy.md` |
| 098 | **Reliability for Multi-Tenant Platforms** | `098-reliability-for-multi-tenant-platforms.md` |
| 099 | **Balancing Reliability, Velocity, and Cost** | `099-balancing-reliability-velocity-and-cost.md` |
| 100 | **Reviewing an End-to-End Delivery and Reliability System** | `100-reviewing-an-end-to-end-delivery-and-reliability-system.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
