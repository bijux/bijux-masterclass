---
module_id: PLAT-006
program: Platform Engineering
level: 1
module_number: 6
title: Paved Roads and Escape Hatches
status: complete
last_verified: 2026-09-02
---

# Paved Roads and Escape Hatches

## One-Page Review

### Governing question

How can a platform make a reviewed delivery approach easier, safer, and cheaper for the workloads it fits while preserving governed routes for legitimate variation, innovation, emergency action, and independent ownership?

### Essential definitions

- A **paved road** is a coherent, supported, versioned journey that composes platform capabilities, defaults, controls, documentation, diagnostics, and lifecycle promises for a declared workload class.
- A **golden path** is often used synonymously with paved road. The “golden” label is a product hypothesis about fitness, not evidence of universal superiority.
- A **road contract** states eligible consumers and workloads, declarations, derived defaults, guarantees, responsibilities, observability, support, compatibility, and exit conditions.
- An **extension point** permits bounded variation inside the road contract without changing its core invariants.
- An **alternate road** is a separately supported pattern for a materially different recurring workload class.
- An **escape hatch** is a governed transition outside one or more road assumptions with explicit reason, authority, ownership, retained controls, evidence, support boundary, and possible re-entry.
- A **bypass** evades a control or ownership boundary without authorization or evidence. A bypass is not an escape hatch.
- **Road drift** occurs when generated instances, dependencies, controls, or documentation diverge from the maintained road after creation.

### Central model, mechanism, or theorem

Define a road $R=(U,J,F,D,C,O,E,L)$: eligible segments $U$, jobs $J$, fitness predicate $F$, meaningful declarations $D$, composed capabilities $C$, operating promise $O$, evidence $E$, and lifecycle $L$. Route each workload by evidence: standard road, bounded extension, alternate road, governed escape, or independently owned path. Prefer the road because its total experience is compelling and its defaults are demonstrably fit—not because alternatives are hidden or punished.

### Critical invariants

- Eligibility and exclusion are based on workload evidence, not team status or political influence.
- Defaults preserve domain authority and expose consequential assumptions.
- The road remains observable, supportable, upgradeable, reversible where promised, and secure through its lifecycle.
- Escape never silently removes non-delegable legal, security, privacy, safety, or audit obligations.
- The escaping team and platform know who owns build, operation, incidents, cost, migration, and retirement.
- Recurrent escapes are product evidence and trigger road, extension, alternate-road, or scope review.
- Adoption and conformance are not treated as proof of outcome or fit.

### Common failures

Calling a repository template a road; coercing adoption while claiming product pull; supporting only first creation; exposing provider options as “flexibility”; granting permanent waivers; routing influential teams around review; forcing unlike workloads through one abstraction; abandoning escaped teams; and measuring template count instead of safe delivery and recovery outcomes.

### Compact example

A paved road supports stateless HTTP services with declared owner, data class, availability objective, and exposure. It derives repository controls, build, identity, deployment, telemetry, and support metadata. A team needing a GPU batch workload does not toggle dozens of hidden fields: it uses a separately supported batch road. A team evaluating a novel confidential-computing runtime uses a six-month escape with a named sponsor, security review, team-owned operation, cost boundary, evidence plan, and decision date. Every path retains identity, audit, incident, and data obligations.

### Connections

Retrieve end-to-end self-service and guardrails from [PLAT-005](005-self-service-and-guardrails.md), product lifecycle from [PLAT-004](004-platform-as-product.md), and cognitive-load boundaries from [PLAT-003](003-developer-cognitive-load.md). The next module distinguishes [platform capabilities from tool catalogs](../roadmap.md#block-01--platform-engineering-foundations). Later modules own templates, golden-path versioning, workload archetypes, service templates, and optional-but-attractive path design in depth.

## Governing Question

How should a platform encode and operate a preferred way of delivering software without turning a useful default into a mandatory lowest-common-denominator architecture or letting “escape” become ungoverned risk transfer?

The question contains two opposing errors. Unlimited variation makes every team integrate and operate the same undifferentiated machinery. Universal standardization hides workload differences and concentrates architectural power in the platform. A robust design chooses an explicit fitness boundary, offers a compelling supported road within it, and allocates responsibility clearly outside it.

## Why This Matters

Teams rarely need raw tools in isolation. To deliver one service they must connect source control, build, artifacts, identity, policy, deployment, observability, ownership, support, and recovery. Each separate choice can be reasonable while the combined journey remains inconsistent and expensive. A paved road composes the organization’s reviewed knowledge into a repeatable route so teams can begin from a working, operable system rather than an integration project.

Composition creates leverage. Updating a shared road can improve many services; a defect can also spread widely. A road can accelerate onboarding while freezing old assumptions. A template can create compliant code once while every generated repository drifts afterward. A mandatory path can show high adoption while teams build shadow workarounds, lose domain fit, and wait for platform changes.

Escape hatches are necessary because no classification is complete. New workload classes emerge, provider capabilities change, emergencies invalidate ordinary timing, and high-consequence domains may require specialist controls. But “just opt out” is not enough. The organization still needs identity, ownership, incident response, data handling, cost, and lifecycle accountability. The escape design determines whether variation is governable evidence or invisible fragmentation.

Current CNCF guidance describes platforms as optional and composable, driven by user requirements, with secure defaults and a thinnest reasonable layer. DORA's platform research emphasizes automated self-service golden paths, user-centeredness, and developer independence while reporting mixed effects that make local validation necessary. Current Backstage documentation demonstrates templates, input review, task identity, failure logs, cancellation, dry runs, authorization, and cleanup hooks; those mechanisms are useful but do not by themselves create a durable organizational road.

## Prerequisites and Retrieval

Retrieve from PLAT-001 the total-system complexity and central blast-radius model. Retrieve consumer segmentation and jobs from PLAT-002. Retrieve bounded cognitive-load claims from PLAT-003, product hypotheses and lifecycle from PLAT-004, and self-service, guardrails, exceptions, and break glass from PLAT-005.

You should understand service ownership, workload classes, APIs, templates, versioning, policy, software supply chains, observability, incident response, compatibility, migration, and basic cost and risk analysis. This chapter focuses on choosing and governing routes rather than on a particular portal or orchestration product.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a paved road from a template, checklist, tool chain, reference architecture, and mandatory standard;
2. specify road eligibility, declarations, derived defaults, capabilities, promises, evidence, and lifecycle;
3. classify variation as configuration, extension, alternate road, governed escape, or independent ownership;
4. design escape records with authority, retained controls, expiry, evidence, and re-entry or retirement decisions;
5. prevent scaffolding drift and compatibility traps through continuous road ownership;
6. use deviation and escape evidence to evolve product scope rather than punish consumers; and
7. measure attractiveness, fit, safety, recovery, migration, and total operating burden without equating adoption with value.

## Core Exposition

### Define the road as a supported product journey

A paved road is not a list of recommended tools. It is an end-to-end, product-managed route for a class of work. It begins with consumer intent and ends with a usable, observable, supported, and eventually retired outcome. It may expose a portal, CLI, API, templates, documentation, and automation, but none is individually the road.

Model a road as

$$
R=(U,J,F,D,C,O,E,L),
$$

where $U$ is eligible consumer segments, $J$ supported jobs, $F$ the fitness predicate for workload context, $D$ meaningful declarations, $C$ composed capabilities, $O$ the operating promise, $E$ outcome and conformance evidence, and $L$ lifecycle policy. Omitting $F$ invites universal claims. Omitting $O$ creates a demo. Omitting $L$ turns generated assets into unmanaged forks.

The road should define a workload archetype rather than a language or team label alone. A stateless request/response service, scheduled batch job, event consumer, stateful database-backed service, and safety-critical control system have materially different runtime, recovery, scaling, and evidence needs. Several languages may use one road; one language may require several roads.

### Separate standards, defaults, and road choices

Some obligations apply across every route: legal restrictions, identity, ownership, incident reporting, audit retention, or data-handling controls. Others are platform defaults appropriate only inside a road. Others remain consumer choices. Mixing them makes dialogue dishonest.

Label each decision as:

- **non-delegable obligation:** defined by an accountable external or organizational authority;
- **road invariant:** necessary for the road's service promise and support model;
- **reviewed default:** appropriate for the declared class but inspectable and sometimes overridable;
- **bounded configuration:** consumer choice within supported limits;
- **extension point:** additional behavior preserving core invariants; or
- **outside-road ownership:** the platform makes no road-level guarantee, while broader obligations remain.

A team should know whether changing an item loses support, violates policy, creates an alternate ownership model, or simply chooses another supported value. “Best practice” is too vague for these consequences.

### Design meaningful declarations and derivations

Ask consumers for facts and decisions they own: workload archetype, data class, exposure, availability and recovery objectives, owner, region constraints, scaling intent, and cost boundary. Derive provider settings, pipeline configuration, identity bindings, baseline telemetry, policy checks, and documentation from those declarations.

Every derivation should have provenance: declaration, rule or road version, derived value, reason, and effective time. Preview consequential output. Consumers need not understand every low-level option, but they must be able to inspect what affects their responsibility and diagnose failures.

Do not convert the road into a universal meta-platform with every provider option. Each option expands testing, compatibility, support, documentation, and migration state. When combinations become qualitatively different, define an alternate road or leave ownership outside the platform.

### Route variation deliberately

Use five outcomes rather than a binary “on road/off road” label:

1. **Standard road:** context satisfies $F$ using reviewed defaults and bounded configuration.
2. **Road extension:** a supported extension preserves core contracts and invariants.
3. **Alternate road:** a recurrent materially different archetype has its own product promise.
4. **Governed escape:** a bounded case leaves some road assumptions with explicit ownership and evidence.
5. **Independent path:** the organization decides the platform should not own the workload class; the team or another provider owns it under cross-cutting obligations.

This taxonomy avoids forcing every difference into configuration. It also prevents “escape hatch” from becoming a permanent euphemism for an unsupported population the platform still claims to serve.

The following deterministic classifier applies synthetic gates. It verifies a declared routing rule, not real workload fitness.

<!-- bijux-verify: {"id":"road-routing-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"web-api=standard\ntracing-plugin=extension\ngpu-batch=alternate\nconfidential-runtime=escape\nclinical-controller=independent\ncounts=1,1,1,1,1\n","stderr":""}} -->
```python
workloads = [
    ("web-api", True, False, False, False),
    ("tracing-plugin", True, True, False, False),
    ("gpu-batch", False, False, True, False),
    ("confidential-runtime", False, False, False, True),
    ("clinical-controller", False, False, False, False),
]

def route(fits, extension, alternate, approved_escape):
    if fits and not extension:
        return "standard"
    if fits and extension:
        return "extension"
    if alternate:
        return "alternate"
    if approved_escape:
        return "escape"
    return "independent"

results = [(name, route(fits, extension, alternate, escape)) for name, fits, extension, alternate, escape in workloads]
for name, outcome in results:
    print(f"{name}={outcome}")
order = ("standard", "extension", "alternate", "escape", "independent")
print("counts=" + ",".join(str(sum(outcome == label for _, outcome in results)) for label in order))
```

The one-of-each result follows solely from declared inputs. Real classification requires workload evidence, authority, technical feasibility, operating capacity, risk analysis, and consumer review. An “approved escape” flag cannot model approval quality.

### Specify a governed escape

An escape record should contain:

- workload, owner, consumer job, and road assumption that does not fit;
- alternatives considered and evidence that bounded configuration or extension is insufficient;
- approving authority and separate control owners;
- capabilities and promises retained from the platform;
- responsibilities transferred to the escaping team or another provider;
- security, privacy, legal, reliability, cost, audit, and incident obligations;
- dependency, compatibility, and support boundaries;
- start, review, expiry, and decision dates;
- success, harm, and operating evidence; and
- re-entry, alternate-road, continued-independent, or retirement criteria.

An escape can be temporary experimentation, long-lived independent ownership, or emergency action. Do not force every one to expire into the standard road; evidence may show the road is wrong or the workload should remain elsewhere. Time bounds ensure a decision, not a predetermined conclusion.

Escaped teams must not become invisible. Publish how they receive security notices, provider changes, incident coordination, and identity or audit services. Conversely, do not imply platform support for components the platform does not operate.

### Distinguish extension from escape

An extension point has a stable contract, compatibility policy, security model, tests, ownership, and support boundary. Examples include an approved build step, telemetry exporter, or runtime adapter. It preserves the road's core promises. An escape changes who owns one or more promises.

Unbounded plugins can reproduce the complexity the road was meant to manage. Extension execution needs identity, permission, isolation, resource limits, provenance, failure behavior, and versioning. Platform teams should offer extensions only where recurring variation justifies the ongoing product surface.

### Avoid scaffolding drift

Templates are useful at creation. Current Backstage software templates, for example, can collect variables, execute steps, publish repositories, register catalog entries, present a review, expose task identity and logs, support cancellation, run dry runs, authorize actions, and define cleanup after failure. Once files are copied, however, later template changes do not automatically update generated repositories.

Choose lifecycle mechanisms deliberately:

- generate only stable bootstrap files and consume versioned shared capabilities;
- use dependency management and automated update proposals;
- reconcile declarative resources continuously;
- attach conformance tests and policy checks to repositories and runtime state;
- publish road-version and provenance metadata;
- support migrations and compatibility windows; and
- detect divergence without silently overwriting consumer-owned code.

Conformance is not identical to textual sameness. A team can satisfy road invariants through an allowed implementation variation. Conversely, an unchanged generated file can be unsafe because its dependencies or assumptions are obsolete.

### Make the road attractive through total experience

The road earns adoption when it reduces elapsed and coordination time, supplies trustworthy defaults, improves feedback and recovery, makes obligations easier, and remains responsive to consumer evidence. Penalizing alternative paths, withholding documentation, or making security approval available only on road can force use but does not validate fit.

Attractiveness includes expert experience. Novices may value guided creation; experienced teams need APIs, composability, observability, predictable versioning, and low-friction extension. High-consequence teams need evidence, assurance, and explicit authority. One interface need not serve all segments, but one road contract should remain coherent.

Publish service objectives, supported classes, roadmaps, limitations, changes, incidents, and deprecations. Trust increases when the platform admits gaps and helps teams choose another ownership model.

### Operate and evolve the road

Treat road components as a dependency graph. A runtime, base image, build service, identity provider, policy, telemetry contract, or documentation site can change the promise. Maintain owners, compatibility, security response, upgrade paths, capacity, and rollback for each critical dependency.

Version the road semantically by consumer-observable contract, not a marketing release number. Record which instances use which road version and what can be upgraded automatically. Migration must preserve domain-owned changes and expose irreversible effects. Support coexistence for a bounded period; indefinite version proliferation destroys supportability.

Analyze deviations and escapes as evidence. Cluster them by job and reason: missing capability, invalid default, unsupported archetype, provider constraint, performance, policy, expertise, cost, organizational power, or experimentation. Repeated legitimate cases may justify a configuration, extension, alternate road, or changed scope. Repeated bypasses may reveal poor diagnostics or enforcement, but they can also reveal misconduct; investigate rather than automatically productize.

### Measure fit and system effects

Measure eligible voluntary selection, task success, time and waits, recovery, quality and safety, upgrade success, drift, support, exception and escape frequency, escape age, re-entry, independent-path outcomes, platform operator burden, and total cost. Use an eligible denominator: teams whose workload fails $F$ should not lower road adoption.

Interpret deviation carefully. Low escape volume can mean excellent fit, fear, hidden work, or impossible approval. High escape volume can mean innovation, a narrow road, bad defaults, unclear classification, or privileged bypass. Study rejected and abandoned escape requests, not only approved ones.

Compare the road with current alternatives and with its own previous version. Segment outcomes by workload, experience, risk, region, and access needs. A faster first deployment with worse incident recovery or upgrade burden is not a complete improvement.

## Definitions and Notation

Let $U$ be consumer segments, $J$ jobs, $W$ workload contexts, $D$ declarations, and $C$ capabilities. A paved road is $R=(U,J,F,D,C,O,E,L)$, where $F:W\to\{true,false\}$ is a reviewed fitness predicate, $O$ an operating promise, $E$ evidence, and $L$ lifecycle policy.

Let $Q=\{standard,extension,alternate,escape,independent\}$ be route outcomes. A routing decision $q(w)\in Q$ is attributable when its workload facts, classifier version, authority, and decision time are recorded. Classification is not moral ranking; `independent` can be the correct destination.

An escape record is $H=(w,r,a,b,o,t,e,z)$: workload $w$, reason $r$, authority $a$, changed boundary $b$, transferred ownership $o$, time bounds $t$, evidence $e$, and end-state criteria $z$. A **waiver** permits deviation from a specific obligation under an authorized process. An escape may require waivers, but leaving a road does not itself waive any obligation.

**Conformance** means satisfying declared contract and invariants. **Drift** is an unintended or ungoverned divergence from desired or supported state. **Forking** creates an independently evolving copy. **Migration** moves consumers between supported contracts. **Re-entry** returns an escaped workload to a road after the fitness or road boundary changes.

## Mechanisms, Invariants, or Proof Structure

Use this road-governance mechanism:

1. Segment consumers and define workload archetypes and jobs.
2. State $F$, exclusions, declarations, obligations, defaults, configurations, and invariants.
3. Compose capabilities and define the operating, support, evidence, compatibility, and lifecycle promise.
4. Test standard, boundary, expert, novice, accessible, degraded, recovery, and adversarial journeys.
5. Define extension contracts and alternate roads only for evidenced recurring variation.
6. Provide an accountable escape request, decision, operation, review, and end-state process.
7. Preserve cross-cutting obligations and make transferred ownership explicit.
8. Track road versions, instances, drift, dependency changes, upgrades, and deprecations.
9. Measure fit, outcomes, harms, escape evidence, and platform-side burden.
10. Change the road, add an alternate, narrow scope, support independence, or retire based on evidence.

The invariants are **evidence-based eligibility**, **domain-authority preservation**, **operational completeness**, **obligation continuity**, **ownership completeness**, **escape observability**, and **learning from variance**.

The claim “the standard path has 95% adoption, therefore it fits 95% of workloads” fails by counterexample. If leadership mandates the road and approval for escape takes months, eligible and ineligible teams both appear as adopters while the latter carry shadow work. Adoption is therefore not sufficient evidence of fitness; classification, choice context, task outcomes, deviations, support, and harms are required.

## Alternatives and Trade-Offs

**One road versus several archetype roads.** One road maximizes consistency and shared learning but can become over-configurable or exclusionary. Several roads improve fit but multiply product, integration, and lifecycle cost. Split when recurring differences change core promises rather than superficial settings.

**Template versus managed capability.** Templates provide transparent, forkable bootstrap and work across environments. Managed capabilities retain upgrade and operational control. Compose them: scaffold consumer-owned code and declarations while consuming versioned managed services where centralized ownership is justified.

**Extension versus provider exposure.** A stable extension can support innovation inside invariants. Raw provider access preserves maximum capability but transfers integration and lifecycle ownership. Do not disguise provider leakage as a supported extension.

**Voluntary versus mandatory road.** Voluntary use yields stronger product evidence and incentivizes quality. Mandates may be legitimate for non-delegable obligations, but should name the policy and retain fit review rather than claiming attraction.

**Temporary escape versus permanent independent path.** Time-bounded experiments protect learning and review. Some specialist workloads should remain independently owned. A permanent exception without a clear owner is worse than an explicit independent contract.

**Automatic upgrade versus consumer-controlled migration.** Automatic upgrades reduce fragmentation but can break domain behavior. Consumer-controlled migration preserves agency but accumulates versions. Classify changes, test compatibility, provide previews and rollback, and bound support windows.

## Failure Modes and Misconceptions

- **A template is a paved road.** It may bootstrap one moment; the road includes operation, support, evolution, and retirement.
- **Golden means universally best.** Fitness depends on workload, context, authority, and evidence.
- **Optional means unsupported alternatives.** Honest optionality states alternative ownership and preserves cross-cutting access to obligations.
- **Escape means policy exemption.** Leaving platform defaults does not erase law, security, privacy, safety, cost, or audit duties.
- **More configuration means broader fit.** Combinatorial options can destroy coherent testing and support.
- **Conformance means identical files.** Contract and outcome invariants matter more than textual sameness.
- **Low escape volume proves fit.** Fear, delays, hidden bypasses, and missing observability can suppress recorded escape.
- **High escape volume proves consumer irresponsibility.** The road may exclude legitimate jobs or impose invalid defaults.
- **The platform owns escaped incidents.** Support must follow the recorded ownership boundary, while shared incident coordination remains possible.
- **Road launch is completion.** Dependencies, versions, generated instances, migrations, and retirement require continuous ownership.

## Worked Examples

### Example 1

**Situation:** A Java repository template configures CI and Kubernetes manifests. **Reasoning:** It creates a useful baseline but defines no runtime service promise, upgrade mechanism, incident ownership, or drift detection. Compose it with supported build, identity, deployment, telemetry, documentation, and lifecycle contracts. **Conclusion:** Scaffolding becomes part of a road only inside an operated end-to-end journey.

### Example 2

**Situation:** A team asks to choose a different log exporter. **Reasoning:** If the road defines an authenticated telemetry protocol, resource bounds, schema, delivery evidence, and support seam, an approved exporter can be a bounded extension. If it bypasses retention and access controls, it changes obligations and needs a different route. **Conclusion:** Extension is defined by preserved invariants, not small code size.

### Example 3

**Situation:** GPU batch jobs fail the stateless service fitness predicate. **Reasoning:** Their scheduling, cost, retry, artifact, and completion semantics recur across teams. Adding flags to the service road would distort its promise; a batch road can reuse identity, build, and telemetry capabilities under a distinct runtime contract. **Conclusion:** Recurrent archetype differences justify an alternate road.

### Example 4

**Situation:** A research team needs a confidential runtime unavailable on the road. **Reasoning:** Approve a time-bounded escape with security authority, team-owned runtime operation, retained identity and audit, cost limits, incident roles, evidence, and a six-month decision. **Conclusion:** Governed experimentation preserves learning without pretending production support.

### Example 5

**Situation:** An executive's team receives a permanent undocumented exemption. **Reasoning:** No fitness evidence, transferred ownership, retained controls, or review exists. Influence has produced a bypass and unequal risk treatment. Require the same attributable route decision and control authority as other teams. **Conclusion:** Organizational rank is not an escape mechanism.

### Example 6

**Situation:** A road update changes the base image, but 400 generated repositories remain old. **Reasoning:** Copy-time templating lacks update propagation. Track provenance, publish automated update proposals, test compatibility, measure migration, and set supported deadlines; avoid overwriting consumer changes. **Conclusion:** A maintained road needs an instance evolution mechanism.

### Example 7

**Situation:** Road adoption is high while platform tickets and lead time increase. **Reasoning:** A mandate caused migration, but diagnostic gaps and manual exceptions moved coordination behind the interface. Observe complete journeys, classify tickets, inspect ineligible workloads, and compare recovery. **Conclusion:** Conformance and outcome can diverge.

### Example 8

**Situation:** A team wants direct cloud access for one unsupported database. **Reasoning:** Determine whether the provider service can satisfy cross-cutting identity, network, data, audit, backup, and incident obligations. Assign provider lifecycle and cost ownership, retain shared controls, and state that platform database support does not apply. **Conclusion:** Independent ownership can be safer than a leaky platform abstraction.

### Example 9

**Situation:** During an outage, the road's deployment controller is unavailable. **Reasoning:** A rehearsed emergency route permits a scoped rollback through an independent control path with strong identity, immutable evidence, expiry, and review. It does not allow arbitrary feature deployment. **Conclusion:** Emergency escape is bounded recovery authority, not removal of governance.

### Example 10

**Situation:** A medical-device controller cannot use the ordinary application road. **Reasoning:** Its real-time behavior, verification, safety case, regulatory change control, and field recovery require specialist ownership. It may consume shared identity, artifact provenance, and audit capabilities, but clinical engineering and regulatory authorities own release acceptance. **Conclusion:** An explicit independent path preserves platform value without claiming unsafe universality.

## Cross-Program Connections

- **Software architecture:** paved roads operationalize reference architectures while preserving boundaries, extension contracts, and domain-specific alternatives.
- **Software delivery:** templates, pipelines, artifacts, promotion, and rollback are road components, but delivery practice remains broader than platform ownership.
- **Security engineering:** non-delegable controls, waivers, extensions, exceptions, break glass, and independent paths require distinct authorities and evidence.
- **Reliability engineering:** service promises, dependency graphs, degraded paths, upgrade safety, and incident ownership determine road trust.
- **Product management:** attractiveness, segmentation, adoption confounders, deviation evidence, lifecycle, and retirement guide road evolution.
- **Configuration management:** provenance, versioning, conformance, drift, reconciliation, and migration prevent copy-time standards from decaying.
- **Organizational design:** routes allocate cognitive load, platform responsibility, team autonomy, collaboration, and operational burden.

## References

- CNCF TAG App Delivery, [*CNCF Platforms White Paper*](https://tag-app-delivery.cncf.io/whitepapers/platforms/), 2023. Current guidance on user-centered platforms, secure defaults, optionality, composability, capabilities, and the thinnest reasonable layer.
- DORA, [*2024 Accelerate State of DevOps Report*](https://dora.dev/research/2024/dora-report/), corrected edition v2024.3. Empirical treatment of automated self-service golden paths, user-centeredness, developer independence, platform effects, and methodological limits.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current critical-journey, product-mindset, self-service, and balanced-measurement guidance.
- Matthew Skelton and Manuel Pais, *Team Topologies: Organizing Business and Technology Teams for Fast Flow*, IT Revolution, 2019. Practitioner foundation for platform teams, cognitive load, interaction modes, and the thinnest viable platform.
- Backstage, [*Software Templates*](https://backstage.io/docs/features/software-templates/), current documentation retrieved 2026. Template inputs, review, task execution, identity, logs, cancellation, retry, and results.
- Backstage, [*Writing Templates*](https://backstage.io/docs/features/software-templates/writing-templates/), current documentation retrieved 2026. Versioned template schemas, actions, dry runs, conditional cleanup, authoring, and testing mechanisms.
- Google, [*Operational Efficiency: Eliminating Toil*](https://sre.google/workbook/eliminating-toil/), *Site Reliability Workbook*, 2018. Self-service automation, human-backed interfaces, safety checks, maintenance, and toil trade-offs.
- NIST, [SP 800-53 Rev. 5, Release 5.2.0 — *Security and Privacy Controls for Information Systems and Organizations*](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), 2025. Current cross-cutting control catalog for access, audit, configuration, contingency, identity, privacy, risk, and integrity obligations.

## Exercises

### Exercise 1

Given a repository template that creates source code, CI, deployment manifests, and ownership metadata, identify what is still missing before it qualifies as a paved road.

### Exercise 2

Classify five requests—different log exporter, GPU runtime, higher replica count, direct cloud database, and emergency rollback—as bounded configuration, extension, alternate road, governed escape or independent path. State assumptions that could change each classification.

### Exercise 3

Design an escape record for a team evaluating a new serverless provider. Include authority, retained controls, transferred ownership, evidence, time bounds, incidents, cost, and end states.

### Exercise 4

Compare copy-time scaffolding, automated dependency updates, and continuous reconciliation as road-evolution mechanisms. Analyze transparency, drift, consumer ownership, rollback, and blast radius.

### Exercise 5

Transfer the road model to a government analytics platform serving routine reporting, confidential investigations, public-health emergencies, and experimental research. Propose routes and authority boundaries.

## Answers to the Exercises

### Answer 1

The template covers initial output only. A road still needs an eligible workload definition, meaningful declarations, derived-default provenance, supported build and runtime capabilities, identity and policy behavior, artifact and dependency lifecycle, observability and diagnostics, service objectives, support and incident ownership, conformance evidence, update propagation, compatibility, migration, deprecation, cleanup, and retirement. It must also state consumer obligations and exclusions. Without these, the generated repository is a useful bootstrap that can drift immediately rather than an operated end-to-end product journey.

### Answer 2

Higher replicas are bounded configuration if resource and reliability limits remain inside the supported contract. A different log exporter is an extension if it satisfies the road's telemetry, security, resource, and support interface. GPU runtime is an alternate road when it represents a recurring batch or accelerated archetype with distinct scheduling and cost semantics. A direct cloud database is an independent path when the platform does not support its class and the team can own provider lifecycle under cross-cutting obligations; it might instead be a governed temporary escape during evaluation. Emergency rollback is a governed emergency escape from the normal deployment mechanism. Classifications change if recurrence, risk, platform authority, support capacity, extension contracts, or road fitness changes.

### Answer 3

Record the workload and why existing road and provider options fail, the product and platform owners, architecture and security approvers, and the specific road promises being left. Retain enterprise identity, artifact provenance, data classification, audit, vulnerability response, incident notification, and cost reporting. Transfer serverless runtime configuration, provider availability, quotas, deployment behavior, observability integration, incident diagnosis, and migration to the team. Set a limited account and budget, no restricted data unless separately approved, a three-month experiment, monthly evidence reviews, and automatic access expiry. Measure task fit, reliability, cost, security findings, operator burden, and portability. End by re-entering a road, proposing an evidenced alternate road, continuing under an explicit independent contract, or deleting resources and evidence according to retention rules.

### Answer 4

Copy-time scaffolding is transparent and leaves code with consumers, but later fixes do not propagate and forks multiply. Automated dependency or file update proposals preserve review and can scale migrations, but create queue burden, merge conflicts, and partial adoption. Reconciliation continually restores declared state and reduces drift, but can overwrite legitimate changes, amplify controller defects, and require a clear authority/conflict model. Use scaffolding for stable consumer-owned bootstrap, updates for versioned dependencies and reviewable migrations, and reconciliation for platform-owned desired state. Every approach needs provenance, conformance tests, preview, observability, rollback or compensation, and blast-radius controls.

### Answer 5

Routine reporting can use a standard road with approved data products, reproducible transformations, scheduled execution, lineage, quality checks, access, publication, and retention. Experimental low-sensitivity research can use a bounded extension or sandbox road with quotas and non-production outputs. Confidential investigations need a distinct supported road or independently governed environment because identity, purpose limitation, disclosure, evidence, and legal authority differ materially. A public-health emergency uses a time-bounded emergency escape or alternate road with incident-command authority, strong access, data minimization, expiry, public-health and privacy review, and post-event accountability. The platform owns shared mechanics and evidence; data stewards own meaning and access, legal/privacy authorities own permissible use, incident command owns emergency purpose and timing, analysts own interpretation, and affected communities require appropriate transparency and redress.
