---
module_id: SDRE-030
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 30
title: Designing a Safe Release Pipeline
status: complete
last_verified: 2026-09-06
---

# Designing a Safe Release Pipeline

## One-Page Review

### Governing question

How can a release pipeline transform an approved source change into a verified production outcome while preserving subject identity, evidence scope, least privilege, recovery, and an auditable answer to every failure or uncertain state?

### Essential definitions

- a **release pipeline** is a governed state machine that builds, verifies, promotes, deploys, observes, and recovers exact release subjects;
- a **release subject** binds artifact digests, effective configuration, infrastructure declarations, dependency resolutions, migrations, and feature state;
- a **stage** is a bounded transformation or evaluation with declared inputs, outputs, identity, and failure behavior;
- a **gate** is a policy decision over an exact subject, target, evidence set, and time;
- **evidence** is a claim with subject, producer, method, environment, result, time, and limitations;
- an **attestation** is authenticated metadata that binds a predicate to identified software subjects;
- **promotion** advances the same immutable subject to a target after target-specific policy passes;
- **trust separation** prevents one compromised actor or stage from authoring, approving, building, and deploying an unreviewed result;
- **hermetic build** means declared inputs determine the build without undeclared host or network dependencies;
- **reconciliation** compares desired release state with observed system state and converges safely;
- **break glass** is narrowly authorized emergency action with explicit scope, audit, reconciliation, and expiry;
- **release completion** is verified user and system behavior, not merely a successful deployment command.

### Central model, mechanism, or theorem

Represent the pipeline as a directed acyclic graph $G=(V,E)$ for finite build and verification work, followed by a stateful deployment controller. For subject $s$, target $e$, policy version $p$, and time $t$, promotion is permitted only when

$$
Permit(s,e,p,t)=Identity(s)\land Provenance(s)\land Evidence(s,e,t)\land Policy(s,e,p,t)\land Recoverable(s,e,t).
$$

Every conjunct is fail-closed for promotion: missing evidence is not passing evidence. Successful promotion starts exposure; it does not establish production correctness.

For stage durations $d(v)$, the fastest dependency-respecting completion is bounded below by the critical path

$$
T_{critical}=\max_{\pi}\sum_{v\in\pi}d(v),
$$

not the sum of every parallel stage. Optimize feedback by shortening the critical path and ordering high-information checks early without weakening required evidence.

### Critical invariants

- build once, identify by digest, and promote exact bytes rather than rebuilding per environment;
- every evidence item binds to the subject and assumptions it actually evaluated;
- untrusted change code cannot silently alter the policy that approves or deploys itself;
- stages receive minimum, short-lived credentials and isolated writable scope;
- secrets never enter artifacts, untrusted logs, caches, or pull-request execution contexts;
- policy evaluates freshness, target, configuration, migrations, dependencies, and recovery—not a generic green badge;
- production exposure expands in bounded stages and stops on adverse or missing signals;
- database and external effects remain compatible with rollback or have a governed roll-forward plan;
- retries and controller restarts are idempotent and generation-checked;
- actual running state, traffic, and outcomes reconcile with declared state before completion.

### Common failures

Failures include rebuilding after tests, deploying mutable tags, accepting evidence for a different commit, letting pull-request code access production secrets, trusting unsigned metadata, granting one pipeline identity broad permanent access, running every check sequentially, skipping slow high-risk checks, treating staging as production proof, hiding configuration and migrations outside subject identity, sharing untagged metrics, rolling every change globally, ignoring partial deployment, using an untested rollback script, and allowing emergency changes to remain outside declared state.

### Compact example

A signed source revision enters an isolated hermetic build. The builder emits an artifact digest, SBOM, provenance, and test evidence. Independent policy verifies identities and freshness, then promotes the same digest with target configuration and migration identities. Production begins with one bounded canary cohort. Version-tagged correctness, SLO, saturation, security, and telemetry-completeness guardrails govern expansion. A schema compatibility record proves rollback eligibility. Every controller action uses generation 61 and reconciles actual state. Completion is recorded only after full traffic and a justified observation window; otherwise the pipeline contains, rolls back, or rolls forward.

### Connections

[SDRE-029](029-automated-rollback-and-roll-forward.md) supplies recovery decisions. [SDRE-031](../ROADMAP.md) next distinguishes observability from monitoring. Security Engineering owns threat models and admission policy; Platform Engineering owns pipeline and deployment mechanisms.

## Governing Question

A list of commands is not a safe release pipeline. A green sequence can still deploy the wrong bytes, trust evidence from another revision, leak a credential, skip a target-specific assumption, race a newer release, or report success while users receive errors. Safety comes from explicit identities, state transitions, evidence scope, trust boundaries, and recovery behavior.

The pipeline must answer: what exact subject is changing, who and what produced it, which claims have been established, where they apply, which policy authorized exposure, what actually runs, and how harm is contained. It should make the safe path routine and unsafe ambiguity visible.

## Why This Matters

Google SRE release-engineering guidance emphasizes reproducible builds, unique release identity, automation, policy enforcement, canaries, and recorded release contents [1]. Continuous Delivery develops the pipeline as the executable path by which every candidate is built, tested, configured, and deployed [2]. These foundations reduce special-case manual work and make recovery repeatable.

Supply-chain evidence strengthens but does not replace delivery evidence. SLSA version 1.2 defines current build and source tracks, provenance, and artifact verification guidance [3]. The in-toto Attestation Framework version 1.2 defines authenticated metadata bound to software subjects for policy consumers [4]. Provenance can establish where and how an artifact was produced under its guarantees; it does not establish business correctness, capacity, or production safety.

NIST SSDF 1.1 gives high-level secure-development practices for protecting software and responding to vulnerabilities [5]. NIST SP 800-204D gives supply-chain security strategies for CI/CD pipelines [6]. These publications provide risk and control vocabulary; this chapter does not claim compliance.

The pipeline itself is a high-value production system. OWASP's CI/CD guidance highlights flow control, identity, dependency, poisoned execution, credential, artifact-integrity, configuration, and logging risks [7]. A pipeline with broad deployment authority must be threat-modeled, isolated, monitored, recoverable, and changed through its own governed path.

## Prerequisites and Retrieval

Retrieve revision, commit, digest, artifact, build, hermeticity, dependency lock, SBOM, provenance, attestation, signature, policy, identity, least privilege, secret, evidence, test, environment, promotion, configuration, migration, canary, feature flag, SLO, error budget, rollback, reconciliation, and audit.

Retrieve SDRE-001 through SDRE-010 for artifact and supply-chain foundations; SDRE-011 through SDRE-020 for integration and feedback; and SDRE-021 through SDRE-029 for promotion, configuration, state, deployment, exposure, flags, and recovery. This chapter composes those mechanisms; it does not replace their detailed assumptions.

## Learning Objectives

After completing this module, you should be able to:

1. model a release pipeline as transformations, evidence gates, and a stateful deployment controller;
2. define a complete immutable release subject;
3. bind attestations and test results to exact subjects and environments;
4. separate change code, build authority, policy, deployment, and audit trust;
5. protect credentials and isolate untrusted execution;
6. optimize the dependency graph without dropping high-risk evidence;
7. compose target promotion, migrations, progressive exposure, and feature activation;
8. design idempotent, generation-checked cancellation and recovery;
9. verify declared, running, traffic, and user-outcome state;
10. threat-model, test, operate, and evolve the pipeline itself.

## Core Exposition

**Start with the release subject.** Source revision alone is not the deployed system. Define subject $s=(a,c,i,d,m,f)$ containing artifact digests $a$, effective configuration $c$, infrastructure declaration $i$, resolved dependencies $d$, migration set and state $m$, and governed feature configuration $f$. Some components vary by target; bind their rendered identities before target policy runs.

Use cryptographic digests for content identity. Human labels such as `candidate`, `stable`, and `production` can point to digests but are mutable references. Resolve them at decision time and record the immutable value. If any subject component changes after evidence, determine which claims are invalidated.

Build once and promote exact artifacts. Rebuilding in production changes inputs, tools, timestamps, or dependencies and severs the link to prior evidence. For platform matrices, build every declared target artifact in the controlled build and promote the applicable member by digest.

**Model finite work as a graph.** Checkout, dependency resolution, compile, unit tests, static analysis, package, SBOM, provenance, integration tests, and policy checks form a dependency graph. Edges represent real input or evidence dependencies, not a decorative sequence.

Parallelize independent checks. Compile-dependent tests wait for the artifact; source linters may run alongside the build. Put fast, high-detection checks early to avoid consuming expensive environments on obvious failures. Keep a slower check when it covers a distinct severe risk; latency is not justification to erase evidence.

The graph's lower-bound duration is its longest dependency path. Optimizing a short off-path task does not improve delivery time. Queue delay, worker startup, flaky retries, artifact transfer, and human approval also contribute to observed lead time; measure them separately.

Stages are deterministic where practical and always explicit about inputs. Pin tools and dependencies, isolate writable directories, constrain network, and clean environments between subjects. A cache is an optimization: validate its key includes every semantic input and verify restored content before use.

**Treat evidence as scoped data.** A result includes subject digest, claim type, method, producer identity, tool and version, environment, inputs, output, time, policy relevance, and limitations. “Tests passed” without identity or scope cannot authorize deployment.

Evidence has different transfer rules. Unit tests may apply to the artifact across targets. A staging load test applies under its workload and dependency assumptions. A production canary provides bounded evidence for its cohort and time. Record assumptions so policy can decide reuse rather than copying green status.

Freshness matters. A new critical vulnerability can invalidate an old scan; target drift can invalidate an environment check; a changed policy can require new evidence. Cache evidence by complete claim key, not just commit hash. Never allow a success from one matrix member to satisfy another accidentally.

Attestations bind claims to subjects and authenticate the producer. Verify schema, subject digest, predicate type, signer or workload identity, trust root, time, and policy. A valid signature proves origin and integrity under key assumptions, not truth of the predicate. The verifier still interprets the claim.

**Separate trust domains.** Pull-request code is adversarial input to the pipeline even when written by colleagues. It must not read production credentials, modify protected policy, publish trusted releases, or forge approvals. Run it in isolated workers with bounded CPU, memory, network, filesystem, and time.

Separate source approval, build service, evidence producer, policy decision, deployment controller, and audit storage where the threat model needs independent compromise. One administrator may operate several systems, but credentials and logged actions should not make one stolen token sufficient to replace production silently.

Protect pipeline definitions and reusable actions. Pin external actions or plugins to reviewed immutable versions. Review changes that alter build commands, output paths, test selection, signing, policy, or deployment. A code change that disables its own checks is a policy change, not an ordinary feature.

Use short-lived workload identity bound to repository, revision, workflow, environment, and action. A build stage can read dependencies and write its isolated outputs; it cannot deploy. A deployment stage can fetch an already accepted subject and update one target; it cannot rewrite the artifact. Avoid long-lived shared secrets.

Keep secrets out of command arguments, environment dumps, artifacts, caches, test fixtures, and logs. Forked or untrusted pull requests receive no privileged secrets. Masking output is defense in depth, not permission to expose values to arbitrary code.

**Make gates complete decisions.** A gate evaluates exact subject, target, policy version, evidence, time, actor, and recovery state. It returns pass, deny, hold, or unavailable with reasons. `Hold` means evidence may arrive; `unavailable` means the decision mechanism cannot establish permission. Neither is pass.

Required evidence depends on change classification and target risk. A documentation-only path may skip executable deployment checks only when classification is trustworthy and no deployable subject changes. A schema change adds compatibility and migration gates. An authorization change adds abuse and policy tests. Risk adaptation changes evidence intentionally; it does not let the candidate self-label as low risk.

Human approval is one evidence item, not magic. Show the reviewer subject diff, configuration, migrations, dependency changes, test limitations, target, exposure, recovery eligibility, and policy. Approval expires when those inputs change. Require separation of duties for high-impact targets where justified.

**Promote through environments.** Promotion reuses exact artifact bytes while binding target configuration, secrets references, infrastructure, migrations, and policy. Validate rendered configuration and hash it. Resolve secrets through target identity; do not copy values from staging.

Staging provides useful integration evidence but cannot reproduce production data, traffic, identities, topology, quotas, and dependency behavior perfectly. Explicitly identify which claims remain target-specific. Production begins as a bounded evidence stage rather than a ceremonial final copy.

Reconcile desired and actual state. Verify running digests, configuration generation, replica and topology state, migrations, routes, and feature values. A deployment API acknowledgment is not proof every instance converged or every request uses the target.

**Coordinate stateful changes.** Database and message changes are pipeline subjects with their own checkpoints and compatibility. Use expand–migrate–contract: add compatible representations, deploy tolerant readers, introduce writers gradually, backfill idempotently, observe, then contract only after the rollback window closes.

Prevent application startup from racing an incomplete migration. Serialize where necessary, use locks or fencing for one-time authority, and make retries idempotent. Record partial migration state. A failed application deployment must not automatically reverse a data operation whose recovery semantics differ.

External effects require test isolation and production idempotency. Synthetic probes use dedicated accounts and reversible actions. Mirrored traffic suppresses writes. Delivery evidence never authorizes unsafe duplicate payment, email, or device commands.

**Control production exposure.** Choose blue-green, canary, rolling, or another strategy from capacity, compatibility, routing, and failure constraints. The pipeline records exact old and new subjects, cohort, traffic, topology, stage duration, and maximum harm.

Canary gates require absolute service guardrails, candidate-control comparison, representative traffic, sufficient volume and duration, telemetry completeness, and current rollback eligibility. A replica count or “no alert” is not a decision. Pause between stages when signals need time.

Feature activation is a separate production change. Bind flag generation, targeting, owner, expiry, and recovery policy. A dark deployment can complete before release, but the pipeline must not claim users received the feature. Flag changes need identity and audit comparable to code changes.

**Design failure as a first-class path.** Every stage declares timeout, retry, cancellation, partial-output handling, and cleanup. Retry only idempotent work or use attempt identity and fencing. A timeout creates unknown state; inspect actual outputs before repeating.

Fail closed for promotion, not necessarily for service. If a policy service is unavailable, hold the release while production continues serving its current subject. If telemetry disappears during canary, stop expansion and apply the declared containment policy. Do not take production down merely because delivery is unavailable.

Cancellation stops future stage starts and reconciles running work. It does not erase published artifacts, migration effects, or deployed instances. Record the terminal state and retain forensic evidence.

Recovery reuses the normal controller. Precompute and continuously validate rollback eligibility, but recheck current data, dependencies, secrets, and security at action time. If rollback is unsafe, contain and roll forward. Verify user and business outcomes after either action.

**Use generations and concurrency control.** Assign release attempt and rollout generation. Every write uses compare-and-swap against expected target generation. A stale pipeline cannot promote an older subject over a newer incident fix.

Serialize incompatible deployments to one target. Independent services may proceed concurrently when ownership and evidence do not interfere. Shared database, gateway, flag, or dependency changes require an explicit coordination graph. Avoid a global lock that unnecessarily blocks the organization.

On controller restart, load durable attempt state and observe the target. Reconcile rather than replay from the beginning. At-least-once task delivery is safe only when step effects are idempotent or fenced.

**Observe and verify completion.** Emit structured events for stage start and end, subject, evidence, gate reason, actor, target generation, deployment observation, route change, guardrail, recovery, and override. Protect audit records from alteration by the subject being deployed.

Define completion at several layers: artifact accepted, target desired state updated, instances converged, traffic converged, service objectives healthy, business invariants healthy, and observation window satisfied. Report the actual layer. Do not collapse them into “deployed.”

Version-tag telemetry while limiting sensitive and high-cardinality labels. Missing data, evaluator error, and lag are signals. Correlate with dependency and platform events so a halt preserves attribution without claiming causality.

**Operate the pipeline as a product.** Assign owners, SLOs, threat model, recovery plan, capacity, dependency inventory, change process, and support. Test worker isolation, secret denial, policy bypass, artifact substitution, forged attestation, cache poisoning, audit loss, queue duplication, control-plane outage, and region failure.

Track build reproducibility, evidence latency, queue time, flaky failure, false gate decisions, escaped defects, rollout harm, recovery time, credential age, policy exceptions, and drift. Optimize for reliable learning and bounded impact, not maximum green runs.

Break-glass workflows use narrow temporary authority, require reason and incident identity, preserve immutable audit, and reconcile the result into declared state. They must be rehearsed. An undocumented bypass becomes the normal unsafe path under pressure.

## Definitions and Notation

Let finite pipeline graph be $G=(V,E)$, with edge $(u,v)$ meaning $v$ requires output or evidence from $u$. Let $d(v)\ge0$ be stage duration. For any dependency path $\pi$, its duration is $\sum_{v\in\pi}d(v)$ and the critical-path lower bound is the maximum over paths.

Let release subject be $s=(a,c,i,d,m,f)$. Let evidence item $z=(s,q,r,x,t,\ell)$ bind subject, claim $q$, result $r$, execution context $x$, time $t$, and limitations $\ell$. A gate must reject an item whose bound subject differs from $s$ even if its result is green.

For target $e$, policy version $p$, and time $t$,

$$
Permit(s,e,p,t)=I(s)\land A(s)\land Z(s,e,t)\land P(s,e,p,t)\land R(s,e,t),
$$

where $I$ is identity, $A$ authenticated provenance/attestation, $Z$ sufficient scoped evidence, $P$ authorization and policy, and $R$ recovery readiness.

Let declared target generation be $D(e,t)$ and observed generation be $O(e,t)$. Convergence requires $D=O$ for relevant subject components plus service-level verification; equality of generation labels alone is insufficient.

## Mechanisms, Invariants, or Proof Structure

**Subject-binding argument.** Evidence for digest $a_1$ does not establish a claim about different digest $a_2$. Rebuilding after verification can yield $a_2$, so build-once promotion preserves the evidence subject while rebuild-per-environment does not.

**Critical-path argument.** Dependency edges impose precedence. Every path must complete in order, so total completion cannot be shorter than its longest path. Independent vertices can overlap; summing all stage durations overstates the achievable lower bound.

**Signature limitation.** Successful attestation authentication shows that protected bytes came from the asserted identity under trust assumptions. A signer can still make a false or weak claim. Policy must validate predicate meaning, evidence method, and scope.

**Privilege-separation argument.** If untrusted change code cannot access signing or deployment authority, compromising only that code-execution stage is insufficient to publish or deploy directly. This narrows attack paths but does not prove the remaining identities or policy uncompromised.

**Executable gate model.** The model checks subject identity, provenance, evidence freshness, policy, recovery, target generation, and telemetry. It is not a build service, policy engine, or deployment controller.

<!-- bijux-verify: {"id":"safe-release-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=permit\nwrong_subject=deny:identity\nmissing_provenance=deny:provenance\nstale_evidence=hold:evidence\npolicy_denied=deny:policy\nrecovery_missing=hold:recovery\nstale_generation=deny:generation\nmissing_telemetry=hold:telemetry\ncritical_path=13\nparallel_not_sum=True\n","stderr":""}} -->
```python
def gate(subject, *, provenance=True, evidence_age=0, policy=True,
         recoverable=True, generation=8, observed_generation=8,
         telemetry=True):
    if subject != "sha256:release-A7-C4":
        return "deny:identity"
    if not provenance:
        return "deny:provenance"
    if evidence_age > 24:
        return "hold:evidence"
    if not policy:
        return "deny:policy"
    if not recoverable:
        return "hold:recovery"
    if generation != observed_generation:
        return "deny:generation"
    if not telemetry:
        return "hold:telemetry"
    return "permit"

subject = "sha256:release-A7-C4"
print(f"accepted={gate(subject)}")
print(f"wrong_subject={gate('sha256:other')}")
print(f"missing_provenance={gate(subject, provenance=False)}")
print(f"stale_evidence={gate(subject, evidence_age=25)}")
print(f"policy_denied={gate(subject, policy=False)}")
print(f"recovery_missing={gate(subject, recoverable=False)}")
print(f"stale_generation={gate(subject, generation=7)}")
print(f"missing_telemetry={gate(subject, telemetry=False)}")
# Paths: source->build->package->deploy is 2+6+3+2; lint runs in parallel.
critical_path = 2 + 6 + 3 + 2
all_stage_sum = critical_path + 4
print(f"critical_path={critical_path}")
print(f"parallel_not_sum={critical_path < all_stage_sum}")
```

## Alternatives and Trade-Offs

**Monolithic versus composed pipelines.** One workflow is easy to view but accumulates privilege and coupling. Composed typed stages improve reuse and separation while requiring stable interfaces and versioning.

**Hosted versus self-managed execution.** Hosted workers reduce operational burden; self-managed workers offer isolation and network control. Either model needs threat analysis, ephemeral state, patching, and identity boundaries.

**Push versus pull deployment.** Push grants the pipeline target access and offers direct control. Pull lets a target-side reconciler fetch authorized desired state, reducing inbound authority while adding reconciliation latency and controller complexity.

**Central policy versus repository policy.** Central rules improve consistency and resistance to local bypass. Repository rules capture domain context. Layer them so local policy can strengthen but cannot silently weaken organizational minimums.

**Fail-fast versus maximum diagnostics.** Stopping at the first failure saves resources. Continuing independent checks provides more feedback. Never continue a stage that consumes an invalid prerequisite.

**Static gates versus risk-adaptive gates.** Static gates are predictable. Risk adaptation reduces unnecessary latency but depends on trustworthy classification and explicit minimum controls.

**Manual approval versus automated evidence.** Humans interpret ambiguous risk; automation is repeatable and fast. Approval should receive evidence and remain bound to unchanged inputs rather than replace technical checks.

**One global pipeline versus domain platforms.** A single path centralizes governance but can become a bottleneck and blast radius. Domain-specific pipelines can fit workloads while consuming shared identities, evidence schemas, and policy foundations.

## Failure Modes and Misconceptions

- **“Green means safe.”** a green result has value only for its bound subject, claim, assumptions, and time.
- **“Same commit means same artifact.”** undeclared tools and dependencies can change bytes.
- **“A signature proves correctness.”** it authenticates a claim or artifact under trust assumptions.
- **“Staging passed, so production will.”** target data, load, identity, topology, and dependencies differ.
- **“The pipeline file is ordinary code.”** it can alter tests, credentials, publishing, and deployment authority.
- **“Secret masking makes exposure safe.”** arbitrary code can exfiltrate values without printing them directly.
- **“One deploy token is simpler.”** broad permanent credentials enlarge compromise scope.
- **“All checks must be sequential.”** independent evidence can run in parallel.
- **“Slow checks should be removed.”** optimize placement and implementation; preserve distinct severe-risk evidence.
- **“Cached output already passed.”** validate cache identity and evidence freshness.
- **“Deploy success means release success.”** user exposure and outcomes may not have converged.
- **“No telemetry means no regression.”** missing evidence blocks expansion.
- **“Rollback is a script at the end.”** recovery is a tested, eligibility-checked deployment path.
- **“Cancellation undoes stages.”** published and external effects remain.
- **“A global lock is safest.”** it creates unnecessary coupling and availability risk.
- **“Break glass may bypass records.”** emergency authority requires stronger reconciliation and audit.

## Worked Examples

### Example 1

**Catch subject drift.** Tests pass for digest A7. A production stage rebuilds from the same commit and produces A8 due to a newer compiler. The gate rejects A8 because evidence binds A7. Conclusion: promote exact bytes or reacquire evidence for the new subject.

### Example 2

**Calculate the critical path.** Checkout takes 2 minutes, build 6, package 3, and deploy 2 in sequence; a 4-minute source lint runs beside the build path. The critical path is $2+6+3+2=13$ minutes, not 17. Conclusion: speeding the four-minute lint cannot reduce end-to-end time unless it becomes critical.

### Example 3

**Reject evidence confusion.** Linux tests pass, while the Windows package has a different digest and no test evidence. A matrix-summary badge is green. The target-specific gate rejects Windows. Conclusion: evidence identity includes the matrix subject, not only the workflow run.

### Example 4

**Separate privilege.** A pull request changes a test script to upload artifacts. Its worker has no signing identity, production credential, or protected policy write access. A later trusted builder checks out the reviewed revision in a clean environment. Conclusion: untrusted execution cannot directly convert its output into a production subject.

### Example 5

**Scope a staging claim.** Staging proves API contract behavior at 50 requests/s with synthetic identities. Production requires 5,000 requests/s, real authorization policy, and regional dependencies. Conclusion: reuse contract evidence but reacquire capacity, identity, and target-dependency evidence.

### Example 6

**Handle a migration failure.** Expand schema succeeds; application canary fails; no new-only values were written. The pipeline stops writers, verifies old readers remain compatible, rolls application back, and leaves additive schema in place. Conclusion: code and database recovery can have different safe targets.

### Example 7

**Treat missing telemetry correctly.** Candidate errors appear zero because the telemetry exporter lost credentials. Completeness drops below 99%. The gate holds and removes new candidate exposure under policy. Conclusion: absence of measurements is unavailable evidence, not health.

### Example 8

**Reconcile a timeout.** The deployment call times out after generation 20 is submitted. A retry first reads desired and observed state and discovers half the target already updated. It adopts the attempt and continues within surge limits. Conclusion: unknown outcomes require observation, not blind replay.

### Example 9

**Bound a break-glass action.** An incident operator disables one target route using a 30-minute credential tied to incident I44. The action writes immutable audit and desired state. After stabilization, normal reconciliation either preserves the reviewed change or reverts it. Conclusion: emergency speed need not create invisible drift.

### Example 10

**Verify complete release.** Every instance reports digest A7, but only 70% of traffic reaches it because long-lived connections remain on A6; billing correctness also lacks one full cycle. The pipeline reports deployment convergence but not release completion. Conclusion: name the achieved layer and continue observation.

## Cross-Program Connections

- **Security Engineering:** threat modeling, workload identity, least privilege, signing, and policy defend the pipeline.
- **Platform Engineering:** workers, artifact stores, policy services, reconcilers, and deployment controllers implement it.
- **Systems Engineering:** capacity, failure boundaries, recovery objectives, and hazard analysis shape gates.
- **Distributed Systems:** idempotency, generations, partial failure, and convergence govern stateful execution.
- **Testing and Quality Engineering:** claim design, coverage, experiment validity, and oracle quality create evidence.
- **Database Engineering:** migration compatibility and repair constrain promotion and recovery.
- **API and Service Engineering:** contract tests, versioning, deadlines, and telemetry connect services across releases.
- **Software Architecture:** ownership and dependency boundaries determine independent release units.
- **Data Engineering:** evidence lineage, audit events, and backfills require governed data movement.
- **Cloud Engineering:** regions, quotas, managed identities, and control planes influence target-specific risk.

## References

1. Dinah McNutt, [“Release Engineering”](https://sre.google/sre-book/release-engineering/), in *Site Reliability Engineering*, O'Reilly, 2016; retrieved 2026-09-06.
2. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010.
3. SLSA, [SLSA Specification v1.2](https://slsa.dev/spec/v1.2/), approved specification retrieved 2026-09-06. Used for current provenance, verification, and supply-chain assurance vocabulary.
4. in-toto, [Attestation Framework Specification v1.2](https://github.com/in-toto/attestation/blob/main/spec/README.md), current specification retrieved 2026-09-06. Used for authenticated subject-bound metadata structure.
5. NIST, [SP 800-218: *Secure Software Development Framework Version 1.1*](https://csrc.nist.gov/pubs/sp/800/218/final), February 2022.
6. NIST, [SP 800-204D: *Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines*](https://csrc.nist.gov/pubs/sp/800/204/d/final), February 2024.
7. OWASP, [“CI/CD Security Cheat Sheet”](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html), current guidance retrieved 2026-09-06.
8. Alec Warner et al., [“Canarying Releases”](https://sre.google/workbook/canarying-releases/), *The Site Reliability Workbook*, O'Reilly, 2018; retrieved 2026-09-06.
9. Clare Liguori, [“Automating safe, hands-off deployments”](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/), Amazon Builders' Library, 2020; retrieved 2026-09-06. Used as documented AWS practice, not a universal guarantee.

## Exercises

### Exercise 1

Define release pipeline, release subject, stage, gate, evidence, attestation, promotion, trust separation, reconciliation, and release completion. Explain why a green workflow run is insufficient evidence by itself.

### Exercise 2

A graph has checkout 2 minutes, build 8, unit tests 5 after build, package 2 after build, integration tests 7 after package, and policy 1 after both test branches. Compute the critical path. Identify which one-minute optimization can and cannot improve it.

### Exercise 3

Threat-model a pull-request pipeline that currently receives one permanent token capable of reading secrets, publishing packages, and deploying production. Redesign identities, isolation, artifact flow, and approval.

### Exercise 4

Design a production path for a release containing application code, an additive database change, target configuration, and a feature flag. Include subject identity, evidence, canary, missing telemetry, rollback eligibility, and completion.

### Exercise 5

A regional deployment call times out, an emergency operator changes routing, and a newer approved release enters the queue. Design reconciliation and concurrency rules that preserve user service and prevent stale overwrite.

## Answers to the Exercises

### Answer 1

A release pipeline is the governed state machine; a release subject binds every behavior-relevant artifact and configuration identity; a stage transforms or evaluates declared inputs; a gate makes a policy decision; evidence is a scoped claim and result; an attestation authenticates subject-bound metadata; promotion advances the same immutable subject; trust separation limits one actor or compromise; reconciliation compares desired and observed state; and release completion is verified system and user behavior. A green run lacks meaning unless its subject, producer, method, target assumptions, freshness, limitations, policy, and actual deployment outcome are known.

### Answer 2

After checkout and build, unit tests take 5 while package then integration takes $2+7=9$. Policy waits for both. The critical path is $2+8+9+1=20$ minutes. Reducing integration by one minute reduces total to 19; reducing unit tests from 5 to 4 does not change the 9-minute competing branch and therefore does not change total. Reducing build by one minute also reduces both branches and total to 19. Queue and setup time would need separate inclusion in observed latency.

### Answer 3

Treat pull-request code as untrusted. Run it in an ephemeral isolated worker with no production secrets, no trusted signing key, bounded network and filesystem, and read-only scoped source access. A separate trusted builder checks out the reviewed immutable revision, resolves pinned dependencies, builds hermetically, and emits digest-bound provenance and test evidence. A publisher identity can write only the artifact store and only after policy. A target-specific short-lived deploy identity can fetch accepted immutable artifacts and update one environment. Protected policy and workflow definitions require independent review. Audit storage is append-protected. Production approval binds the digest, evidence, target, and recovery state; no reusable token spans all capabilities.

### Answer 4

Build the application once and bind its digest with rendered target configuration digest, additive migration identity, infrastructure, dependencies, and initial flag generation. Verify provenance, SBOM, tests, configuration schema, migration idempotency, old/new reader compatibility, target identity, capacity, and recovery subject. Apply the additive change first and verify it, deploy code dark, then expose a stable canary through the flag. Gate on correctness, SLOs, candidate-control evidence, actual exposure, state compatibility, and telemetry completeness. Missing telemetry halts expansion. Roll back code only while old readers accept all state; otherwise contain and roll forward. Completion requires full intended flag exposure, traffic and instance convergence, migration state, business invariants, and a justified observation window.

### Answer 5

Assign immutable attempt and target generations. After timeout, the controller reads desired and observed regional subjects, routes, instances, and audit before retrying. The emergency route change uses a higher compare-and-swap generation, incident identity, bounded credential, and declared-state record. The timed-out attempt cannot overwrite that generation. Hold the newer release until service stabilizes and the emergency state is reviewed; then either reconcile the existing subject under the new route or authorize the newer subject from the observed base. Idempotent steps adopt already completed work, stale steps terminate, and all transitions preserve current serving capacity. Release completion waits for route, subject, telemetry, and user-outcome convergence.
