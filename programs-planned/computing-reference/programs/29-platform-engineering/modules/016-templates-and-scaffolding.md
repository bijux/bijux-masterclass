---
module_id: PLAT-016
program: Platform Engineering
level: 1
module_number: 16
title: Templates and Scaffolding
status: complete
last_verified: 2026-09-02
---

# Templates and Scaffolding

## One-Page Review

### Governing question

How should a platform design, execute, evolve, and retire templates so they shorten the path to a verified first outcome without hiding consequential decisions, spreading stale code, or claiming permanent ownership of generated projects?

### Essential definitions

- A **template** is a versioned source model containing files, questions, rules, and optional transformations from which project material can be rendered.
- **scaffolding** is the governed operation that selects a template version, collects and validates intent, previews a plan, renders output, performs authorized effects, verifies the result, and transfers ownership.
- A **starter repository** copies a known file tree into an unrelated new history; it usually provides little built-in support for later synchronization.
- A **generator** computes output from explicit inputs and a template version, possibly varying files and configuration by profile.
- A **golden path** is a supported journey and set of interoperable defaults; it is broader than one template and must retain escape paths.
- **generated ownership** identifies which files remain generator-managed, which are consumer-owned, and which are governed continuously by another platform contract.
- A **template provenance record** binds a run to template identity and revision, input schema, redacted answers, executor, policy, produced files, and verification evidence.
- **template drift** is the difference between a generated project and a newer supported baseline; it is not automatically a defect because consumer evolution can be intentional.

### Central model, mechanism, or theorem

Model a scaffold run as $Q=(T_v,X,A,P,R,F,E,H)$: immutable template revision $T_v$, validated inputs $X$, actor and authorization $A$, previewed plan $P$, rendered tree $R$, external effects $F$, verification evidence $E$, and ownership handoff $H$. Pure rendering is $R=g(T_v,X)$ and should be reproducible for equivalent normalized inputs. Publication is a separate, idempotent workflow. Generation is successful only when the output's declared acceptance predicates pass and ownership is explicit—not when files merely exist.

### Critical invariants

- Template identity and immutable revision are recorded for every run; mutable branch names alone are insufficient provenance.
- Inputs express durable consumer decisions, not every implementation toggle available to the template author.
- Preview distinguishes pure file changes from repositories, credentials, registrations, deployments, and other external effects.
- Untrusted template code, hooks, extensions, and dependencies never receive ambient credentials or unrestricted execution.
- Generated output passes the same build, test, policy, security, metadata, and first-outcome contracts expected after handoff.
- Secrets are referenced or provisioned through bounded operations; they are never rendered into source, logs, answers, or provenance.
- Ownership is transferred deliberately: the consuming team owns its project while the platform owns the template product and stated update channel.
- A template change is tested against representative generations and upgrades, not only against the template repository itself.

### Common failures

Copying a fashionable reference service; asking dozens of questions before the consumer understands them; rendering secrets; fetching mutable dependencies; running arbitrary hooks with a user's credentials; mixing render and publish so retry duplicates repositories; claiming success before build or deploy; silently overwriting consumer changes; forcing every project to remain byte-identical; leaving generated TODO placeholders; shipping defaults with no owner or expiry; counting generations as adoption; and deprecating a template without an inventory, migration route, or successor.

### Compact example

A team chooses the supported `http-service` template at immutable revision `8f4…`, supplies service identity, owner, runtime profile, data class, and deployment target, then reviews a plan. Rendering occurs in an isolated workspace with no production credentials. Checks prove deterministic output, repository metadata, locked dependencies, secret references, build, tests, policy, and catalog validity. A separately authorized publisher creates one repository with an idempotency key, protects its default branch, registers the canonical component, and returns durable operation and evidence links. The team accepts ownership; future baseline changes arrive as reviewable update pull requests rather than silent rewrites.

### Connections

Retrieve cognitive-load limits from [PLAT-003](003-developer-cognitive-load.md), product and lifecycle duties from [PLAT-004](004-platform-as-product.md), guardrails and escape paths from [PLAT-005](005-self-service-and-guardrails.md) and [PLAT-006](006-paved-roads-and-escape-hatches.md), capability boundaries from [PLAT-007](007-platform-capabilities-versus-tool-catalogs.md), journeys and verified outcomes from [PLAT-011](011-developer-journeys.md) and [PLAT-012](012-time-to-first-successful-deployment.md), and channel and resource contracts from [PLAT-013](013-command-line-interfaces.md) through [PLAT-015](015-apis-and-declarative-resources.md).

## Governing Question

Which repeated decisions should a platform encode in a template, which must remain visible consumer choices, and what continuing obligation follows after generated code enters an independently evolving project?

Templates compress knowledge. They can make a safe, observable starting state easier than assembling a project by hand. They can also clone yesterday's vulnerabilities, policies, dependencies, organizational assumptions, and accidental architecture into hundreds of repositories. The relevant product is therefore not a directory full of placeholders. It is a maintained journey from intent to verified ownership.

Scaffolding is usually a beginning, not a convergence controller. Once a team changes generated code, the output develops its own history. A platform must decide explicitly whether later change is delivered through generator-aware updates, automated pull requests, dependency tooling, shared runtime capabilities, continuously enforced policy, documentation, or no synchronization at all.

## Why This Matters

A new project often needs repository metadata, build definitions, ownership, test structure, dependency policy, telemetry, deployment configuration, documentation, security contacts, and catalog registration before it can produce a useful outcome. Repeating these decisions manually wastes attention and creates inconsistent omissions. A focused scaffold can embody tested defaults and make the remaining decisions legible.

Current Backstage Software Templates documentation illustrates a multi-step scaffolding service: collect parameters, review them, execute actions, publish results, retain task identity, show logs, and expose success or failure. Its writing, authorization, dry-run, and audit documentation makes the broader lesson clear: template execution is an operational and permissioned workflow, not only string substitution. This chapter uses those capabilities as examples rather than requiring Backstage.

GitHub template repositories demonstrate a simpler model: generate a repository with the same structure and files but unrelated history. That is useful for one-time starting state, yet unrelated histories do not provide an inherent merge path from template to generated repository. Update ownership must be designed separately.

Copier documents a generator model that records answers and template version to support later updates and conflicts. It also warns that tasks, migrations, and extensions can execute arbitrary code and therefore require trust. The general principle applies across tools: a template is software supplied into a privileged creation path and must be reviewed, pinned, isolated, and observable accordingly.

NIST SSDF 1.1 provides a high-level secure-development vocabulary that can be integrated into development lifecycles. SLSA 1.2 describes provenance and increasing build-integrity guarantees. A scaffold can install hooks and metadata that help a project adopt such controls, but generated configuration alone does not prove compliance or provenance. Verification must inspect the actual project and its build system.

## Prerequisites and Retrieval

Retrieve platform boundaries, consumer research, cognitive-load theory, product management, self-service state machines, paved roads, capability contracts, provider choices, team authority, value hypotheses, journey blueprints, verified first deployment, CLI and portal behavior, and declarative-resource semantics from PLAT-001 through PLAT-015.

You should understand source control, filesystems, schemas, template engines, build systems, dependency locks, continuous integration, repository permissions, secrets, authentication and authorization, idempotency, supply-chain threats, provenance, semantic versioning, migrations, testing, observability, product analytics, and software ownership.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish starter repositories, parameterized generators, composable blueprints, and continuously managed platform capabilities;
2. define a template contract with immutable identity, inputs, outputs, effects, evidence, ownership, and lifecycle;
3. design deterministic rendering and isolate it from idempotent external publication;
4. secure template sources, engines, hooks, dependencies, credentials, paths, logs, and generated output;
5. test templates across input partitions, snapshots, builds, policies, upgrades, failures, and first verified outcomes;
6. choose an explicit strategy for consumer customization and later baseline changes;
7. release, deprecate, migrate, and retire templates using inventory and compatibility evidence; and
8. measure template value through task outcomes, safety, freshness, retention, and maintenance cost rather than generation counts.

## Core Exposition

### Choose the smallest useful mechanism

Use documentation when the work is rare, high judgment, or too volatile to encode. Use a starter repository when a small, stable file tree is useful and no update relationship is promised. Use a parameterized generator when a bounded set of inputs reliably determines a project shape. Use composable capabilities when applications need common behavior without copying its implementation. Use policy or dependency automation when a property must remain current after generation.

Avoid making a template the universal platform abstraction. Copying authentication middleware, deployment logic, telemetry pipelines, or organizational policy into every repository multiplies migration work. A shared library, build platform, controller, service, or declarative resource may retain a better ownership boundary. Templates should connect consumers to those capabilities rather than reproduce them.

Define the golden path as a journey with support and evidence, not the generated skeleton. The path includes discovery, input guidance, preview, repository creation, build, first deployment, ownership, diagnosis, update, and exit. A template is one implementation component.

### Define the scaffold contract

Model one run as

$$
Q=(T_v,X,A,P,R,F,E,H),
$$

where $T_v$ is an immutable template revision; $X$ validated normalized inputs; $A$ actor, authorization, and policy context; $P$ previewed plan; $R$ rendered file tree; $F$ external effects; $E$ verification evidence; and $H$ ownership handoff.

The template contract states supported consumer and job, prerequisites, input schema, defaults, sensitive fields, produced files, effectful actions, required permissions, acceptance checks, known limitations, support owner, release policy, update relationship, deprecation window, and escape path. Publish this information where a consumer chooses a template, not only inside its repository.

Bind every run to canonical template identity and immutable revision or content digest. Record engine and action versions where they affect output. A friendly release name can accompany the identity; it cannot replace it.

### Ask only durable, answerable questions

Inputs should represent decisions the consumer owns: component name, accountable owner, workload profile, data classification, jurisdiction, exposure, availability need, and destination. Derive package names, labels, repository paths, and tool configuration when rules are stable and visible.

Do not ask consumers to choose implementation details the platform claims to manage. Conversely, do not hide consequential choices behind defaults. Public exposure, high-cost profiles, destructive retention, privileged credentials, and regulated residency deserve explicit selection and confirmation.

Validate syntax and semantics early. Normalize case and identifiers before preview. Resolve owner and destination references against authoritative systems. Preserve the distinction between omitted, defaulted, and explicitly chosen input. Never store secret values as ordinary answers.

### Separate pure rendering from external effects

Define pure rendering as

$$
R=g(T_v,X).
$$

For the same immutable template, normalized inputs, engine, and declared environment, output should be reproducible. Eliminate implicit current time, random identifiers, workstation paths, locale, mutable network fetches, and undeclared environment variables. When unique identity or time is required, provision it as an explicit input or effect and record it.

The following synthetic check renders a minimal service twice and evaluates baseline acceptance without creating external resources.

<!-- bijux-verify: {"id":"scaffold-render-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"files=5\nowner_present=true\npolicy_violations=0\ndeterministic=true\nsecret_materialized=false\n","stderr":""}} -->
```python
def render(template_revision, inputs):
    assert template_revision == "service@8f4c"
    files = {
        "README.md": f"# {inputs['name']}\nOwner: {inputs['owner']}\n",
        "catalog.yaml": f"name: {inputs['name']}\nowner: {inputs['owner']}\n",
        "runtime.lock": "python==3.14.1\n",
        "src/main.py": "def health(): return {'status': 'ok'}\n",
        "tests/test_health.py": "from src.main import health\nassert health()['status'] == 'ok'\n",
    }
    return files

answers = {"name": "ledger-api", "owner": "team-ledger"}
first = render("service@8f4c", answers)
second = render("service@8f4c", answers)
violations = [path for path, body in first.items() if "TODO_OWNER" in body]
secret_markers = ("BEGIN PRIVATE KEY", "api_key=", "password=")
secret_materialized = any(marker in body for body in first.values() for marker in secret_markers)
print(f"files={len(first)}")
print(f"owner_present={str('team-ledger' in first['catalog.yaml']).lower()}")
print(f"policy_violations={len(violations)}")
print(f"deterministic={str(first == second).lower()}")
print(f"secret_materialized={str(secret_materialized).lower()}")
```

Real reproducibility includes file modes, line endings, ordering, archive metadata, executable tool versions, and dependency resolution. A content digest can compare trees, but matching digests prove only matching bytes under the test—not architectural quality or safety.

External effects belong to a durable operation after preview: create repository, set protection, create cloud project, register component, provision secrets, or open a pull request. Give the operation a stable idempotency key, persist step state, use least privilege, verify each effect, classify unknown outcomes, and compensate only when reversal is safe. Retrying rendering is cheap; blindly retrying publication can create duplicate or partially governed resources.

### Treat templates as a software supply chain

Allow only approved sources and immutable revisions. Review changes through protected source control. Authenticate the template, engine, plugins, actions, container images, and fetched dependencies according to risk. Provenance identifies origins and processes; verification compares that evidence with policy.

Assume hooks, tasks, migrations, custom extensions, and template expressions can be hostile. Execute them in an isolated workspace with bounded CPU, memory, time, filesystem, process, and network access. Do not mount broad user credentials, SSH agents, cloud configuration, or home directories. Grant short-lived capabilities per effectful action rather than ambient authority to the rendering engine.

Prevent path traversal and unsafe links. A rendered filename must remain inside the destination; symbolic links, device files, absolute paths, Unicode ambiguity, file modes, archives, and overwrite rules need validation. Escape values for the target syntax rather than concatenate untrusted input into shell, YAML, workflow, source, or command text.

Never render secrets. Generate or import them in a dedicated secret system, write only references, redact operation views, and test output and logs for known secret forms. Treat generated workflows as code: their permissions, third-party actions, triggers, interpolation, and untrusted pull-request behavior require review.

### Design the generated project as a supported baseline

Start with the smallest coherent repository. Include accountable ownership, purpose, build and test entry points, dependency declarations and locks where supported, formatting and linting, security contacts, vulnerability reporting route, license or internal-use terms, documentation, metadata, CI with least privilege, deployment connection, telemetry hooks, and local cleanup. Include only controls the organization will maintain.

Generated code must be production-shaped but not production-sized. Avoid placeholder credentials, disabled TLS, permissive network rules, fake domains that can escape into deployment, broad IAM, unbounded retries, and tests that assert nothing meaningful. TODOs need an owner and should block completion when consequential.

Profiles are preferable to combinatorial toggles. A small set such as internal HTTP service, event consumer, batch job, and library can carry tested compositions. Orthogonal features can be layered only when their interactions are verified. If $n$ independent booleans create $2^n$ shapes, sampling one default path is not adequate test coverage.

### Test the template, its output, and the journey

Template-unit checks validate schemas, expressions, filenames, transformations, and forbidden content. Golden-tree or snapshot tests detect intentional byte changes, but snapshots must be reviewed rather than blindly refreshed. Generate representative input partitions: minimum and maximum values, each profile, Unicode and reserved names, optional features, denied destinations, invalid owners, and consequential policy combinations.

Run generated-project checks in clean environments: parse configuration; build; unit and integration test; lint; scan dependencies and secrets; validate policies and metadata; produce artifacts; deploy to an ephemeral target when feasible; verify health, telemetry, ownership, and cleanup. Test the output with current supported toolchains, not the template repository's helper code alone.

Test failure and retry: render error, existing destination, repository created but protection failed, catalog unavailable, response lost, cancellation, authorization expiry, provider throttling, and cleanup failure. Preview must not perform hidden effects. Dry run should state which checks were simulated or skipped and cannot promise external acceptance it did not observe.

Measure the complete journey from selection to first verified outcome. A generated repository that does not build, deploy, or reach its owner is failure even if the scaffolder task is green.

### Transfer ownership without abandoning consumers

At handoff, state what the consumer owns, what remains managed, where provenance lives, how to reproduce the generation, which exceptions were selected, how to get support, and how future baseline changes arrive. The platform team owns template quality and its supported update mechanism; it does not become accountable for every generated application's behavior.

Mark files only when a tool truly manages them. Whole-file generated ownership is easier to reason about than interleaving generated and handwritten fragments. If generated regions are necessary, use stable markers, syntax-aware transforms, conflict detection, and explicit refusal when ownership is ambiguous.

Consumer edits are not automatically drift to erase. They may encode valid product requirements. Update tools must preserve local evolution, surface conflicts, and produce reviewable changes. Never silently regenerate over a dirty working tree or merge conflict.

### Choose an update strategy deliberately

**One-shot copy** transfers all file ownership and promises no automatic updates. It is simple, but security and policy changes need separate channels.

**Generator-aware update** records template revision and non-secret answers, computes changes from old template, new template, and local project, and exposes conflicts. It can carry structural migrations but creates tooling and compatibility obligations.

**Automated pull requests** apply targeted transformations or baseline updates across an inventory. They preserve review and project tests but can create noise, merge queues, and unowned failures.

**Shared capabilities and dependency updates** keep common behavior centralized or versioned without rewriting project structure. **Continuous policy** enforces properties that cannot depend on voluntary regeneration. Most mature platforms combine these mechanisms.

Version templates by consumer-visible contract, not by arbitrary repository activity. Release immutable tags, publish change notes and migration risk, test upgrades from supported prior releases, and state support windows. An answer file is provenance-sensitive state: altering it to pretend different generation inputs corrupts update reasoning.

### Operate freshness, deprecation, and retirement

Maintain an inventory linking generated projects to template identity/revision, owning team, generation time, selected profile, update channel, and current support state without recording secrets. Detect ownership gaps and repository deletion. Do not infer that a project is unchanged merely because its original revision is known.

Set service objectives for template validation and critical baseline propagation. Continuously test supported templates against supported runtimes, dependency resolvers, CI platforms, policies, and platform APIs. A green template release from last year can be unusable today even when its bytes did not change.

Deprecation needs a reason, successor or documented alternative, affected-project inventory, risk classification, migration tool or guide, support window, communication, and completion evidence. Disable new generations before removing source or support. Retain provenance needed to understand existing projects.

### Measure value and harm

Track selection-to-preview time, abandonment by field, validation errors, generation success, duplicate or partial effects, first build, first verified deployment, time to owner acceptance, support contacts, update conflicts, baseline freshness, exception use, retention, and template maintenance toil. Segment by consumer and profile.

Counts of generated repositories measure activity, not value. High adoption can amplify a defect. Pair quantitative journeys with interviews, usability sessions, generated-project audits, security evidence, and comparisons with manual or alternative paths. DORA's current platform guidance emphasizes clear task-outcome feedback and a balanced scorecard; template evaluation should follow that product discipline.

## Definitions and Notation

$Q=(T_v,X,A,P,R,F,E,H)$ models a scaffold run through immutable template revision, normalized inputs, authorization context, previewed plan, rendered output, external effects, verification evidence, and ownership handoff.

$R=g(T_v,X)$ denotes pure rendering. Equivalent declared inputs and environment should yield equivalent file-tree bytes, paths, and modes. Reproducibility does not imply correctness.

Let $C(R)$ be the set of declared acceptance checks on rendered project $R$. Generation is acceptable only if every required check passes: $\forall c\in C(R),\ c(R)=\mathrm{pass}$. External-effect and deployed-outcome checks remain separate evidence.

Let $D(p,T_v)$ describe detected baseline difference for project $p$. $D\ne\varnothing$ is not itself a violation: policy, support window, consumer ownership, and risk determine required action.

## Mechanisms, Invariants, or Proof Structure

Use a lifecycle loop: research the repeated job; choose the smallest mechanism; define contract and owner; model inputs and profiles; pin sources and executor; isolate render; preview files and effects; authorize effects; verify output and first outcome; transfer ownership; inventory provenance; test new releases and upgrades; distribute baseline changes; measure; deprecate; migrate; retire.

The provenance invariant binds output to immutable template and declared inputs. The determinism invariant makes rendering reviewable and repeatable. The effect-isolation invariant prevents harmless retries from duplicating resources. The security invariant denies ambient trust to executable templates. The acceptance invariant distinguishes files from working outcomes. The ownership invariant prevents scaffolding convenience from creating permanent ambiguity.

Adversarial review includes malicious template revision; mutable tag; compromised plugin; path traversal; symbolic-link escape; shell injection through a project name; secret in an answer or log; network fetch changes between runs; duplicate repository after response loss; cancellation after partial publication; existing nonempty destination; dirty update; conflict markers committed; old template with revoked CI action; new default that changes exposure; missing owner; and template retirement with live dependents.

## Alternatives and Trade-Offs

**Starter repository** is transparent and low-complexity. It has limited parameterization and no inherent upgrade lineage.

**Text generator** supports repeatable variation. It can produce invalid syntax or unsafe combinations without target-aware validation.

**Syntax-aware transformation** preserves structure and supports migration. It requires parsers, language knowledge, compatibility handling, and careful comment preservation.

**Monolithic template** gives one obvious entry point. Its conditional matrix and release blast radius grow rapidly.

**Composable templates** reuse bounded features. Composition order, version compatibility, field ownership, and interactions become new contracts.

**Automatic synchronization** propagates standards quickly. It can overwrite consumer intent and create widespread breakage unless changes are reviewed and verified.

**Reviewable update pull requests** respect repository ownership. They can accumulate, conflict, and produce alert fatigue without prioritization and support.

**Central managed capability** reduces copied maintenance. It creates runtime dependency, availability, tenancy, versioning, and provider-boundary obligations.

## Failure Modes and Misconceptions

- **“The template is just boilerplate.”** It is executable supply-chain input and an architectural distribution mechanism.
- **“Generated means standardized.”** Consumers can change output, and the baseline itself can be incomplete or unsafe.
- **“More questions mean flexibility.”** They often transfer platform implementation choices and cognitive load to newcomers.
- **“The latest branch is current.”** A mutable ref is weak provenance and can change between preview, execution, and audit.
- **“Dry run proves success.”** It proves only the simulated checks and effects the dry-run contract actually executed.
- **“Regenerate to update.”** Blind regeneration can erase legitimate local evolution and corrupt ownership.
- **“One golden service fits all.”** Different jobs and risk classes need bounded profiles or different mechanisms.
- **“Security is inherited forever.”** Generated controls and dependencies age immediately after handoff.
- **“A green scaffolder task is completion.”** Build, policy, deployment, ownership, and application verification can still fail.
- **“Adoption proves value.”** Generation volume can amplify defects and does not measure retained task success.

## Worked Examples

### Example 1

A template asks for `cloudInstanceType` although the platform promises a workload profile. The input is replaced by `capacityClass`; provider choice moves behind a declarative resource so future migrations do not require regenerating application repositories.

### Example 2

A repository template copies files with unrelated Git history. Its documentation explicitly promises a one-shot baseline, records source revision in provenance, and routes later dependency and security changes through automated pull requests rather than pretending upstream merges exist.

### Example 3

A service name contains shell metacharacters. Schema validation rejects it before rendering; the publisher passes structured API fields rather than interpolating the name into a shell command. No privileged token enters the template workspace.

### Example 4

A template renders the current date into a banner and fetches `main` from a shared workflow repository. Repeated output differs. The revision pins the workflow digest and removes the banner time, making equivalent runs byte-reproducible.

### Example 5

Repository creation succeeds but the response is lost. The publisher queries by organization, requested name, run identity, and ownership marker; it adopts the exact repository and continues protections instead of issuing a second create under a modified name.

### Example 6

A database option doubles the template's file combinations and secretly creates a public endpoint. The design replaces it with a separate database resource reference and an explicit exposure decision that admission policy can validate.

### Example 7

A baseline update changes CI permissions. Tests generate every supported profile, parse workflows, verify least-privilege permissions, run builds, and open reviewable pull requests only for affected repositories. Failed projects retain an owner and migration evidence.

### Example 8

A team customized its README and deployment manifests. Generator-aware update owns only catalog metadata and a workflow file, preserves consumer files, and stops on an overlapping workflow conflict rather than choosing the template silently.

### Example 9

Metrics show 98% generation success but only 61% first deployment success. Journey research finds invalid owner references and unavailable environments after repository creation. The platform moves reference validation earlier and makes deployment evidence part of completion.

### Example 10

A deprecated runtime template has 140 known descendants. New generation is disabled, a supported successor and migration pull request are offered, high-risk projects receive prioritized help, and retirement occurs only after inventory and exception evidence are reconciled.

## Cross-Program Connections

Software engineering contributes modularity, build systems, testing, dependency management, refactoring, and code ownership. API engineering contributes schemas, idempotency, operation identity, preview, authorization, and status. Distributed systems contributes partial failure, retry, reconciliation, and unknown outcomes.

Security engineering contributes least privilege, sandboxing, injection prevention, secrets, secure development, artifact provenance, and supply-chain verification. Reliability engineering contributes objectives, failure modes, rollback, degraded behavior, and operational ownership. Data governance contributes retention, classification, lineage, and privacy for answers and provenance.

Product management and developer experience contribute consumer research, progressive disclosure, task measurement, and lifecycle decisions. Organizational design contributes the handoff between template maintainers, platform operators, security owners, and independently accountable application teams.

## References

- Backstage Project, [*Software Templates*](https://backstage.io/docs/features/software-templates/), current documentation retrieved September 2, 2026. Template selection, parameters, review, task identity, execution, logs, cancellation, restart, success, and failure.
- Backstage Project, [*Writing Templates*](https://backstage.io/docs/features/software-templates/writing-templates/), current documentation retrieved September 2, 2026. Versioned template entities, schemas, steps, typed expressions, cleanup status checks, outputs, editor, and dry-run workflow.
- Backstage Project, [*Authorizing Scaffolder Tasks, Parameters, Steps, and Actions*](https://backstage.io/docs/features/software-templates/authorizing-scaffolder-template-details/), current documentation retrieved September 2, 2026. Permission tags and authorization boundaries for template inputs, actions, and tasks.
- Backstage Project, [*Dry Run Testing*](https://backstage.io/docs/features/software-templates/dry-run-testing/), current documentation retrieved September 2, 2026. Explicit action support and simulation contracts for template dry runs.
- Backstage Project, [*Audit Events*](https://backstage.io/docs/features/software-templates/audit-events/), current documentation retrieved September 2, 2026. Audit event taxonomy for parameter schemas, actions, tasks, retries, cancellation, execution, and dry runs.
- GitHub, [*Creating a Template Repository*](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository), current documentation retrieved September 2, 2026. Repository generation, copied structure and files, optional branches, unrelated history, permissions, and limitations.
- Copier Project, [*Copier*](https://copier.readthedocs.io/en/stable/), stable documentation retrieved September 2, 2026. Templates, questionnaires, recorded answers, generated projects, and update intent.
- Copier Project, [*Configuring a Template*](https://copier.readthedocs.io/en/stable/configuring/), stable documentation retrieved September 2, 2026. Answer files, migrations, tasks, path patterns, cleanup, version behavior, trust, and arbitrary-code-execution warnings.
- Copier Project, [*Updating a Project*](https://copier.readthedocs.io/en/stable/updating/), stable documentation retrieved September 2, 2026. Versioned updates, retained answers, local project evolution, conflicts, diffs, and answer-file integrity.
- NIST, [*SP 800-218: Secure Software Development Framework Version 1.1*](https://csrc.nist.gov/pubs/sp/800/218/final), February 2022. High-level secure-development practices for integration into software lifecycles and supplier communication.
- SLSA, [*SLSA Specification 1.2*](https://slsa.dev/spec/v1.2/), current approved specification retrieved September 2, 2026. Source and build tracks, provenance, verification, threats, levels, and attestation formats.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Internal product, critical journey, clear task-outcome feedback, independence, adoption, retention, task success, and balanced measurement guidance.

## Exercises

### Exercise 1

Design a scaffold contract for an internal HTTP service. Specify template identity, inputs, profiles, preview, render, external effects, permissions, acceptance, evidence, ownership, updates, and retirement.

### Exercise 2

Threat-model a template that accepts repository name and owner, runs hooks, fetches dependencies, creates a repository, configures CI, provisions a secret, and registers a catalog component.

### Exercise 3

Design a test matrix for four profiles and three optional features without pretending all combinations are equally valuable. Include output, journey, upgrade, failure, and adversarial checks.

### Exercise 4

Choose update mechanisms for a critical CI permission correction, a style-guide change, a new telemetry library, a runtime end-of-support migration, and a consumer-owned domain model.

### Exercise 5

Transfer the scaffold model to standardized hospital clinical-study workspaces. Address study classification, protocol ownership, data access, audit, reproducibility, local amendments, validation, retention, and retirement without treating a generated workspace as regulatory approval.

## Answers to the Exercises

### Answer 1

Use canonical `http-service` identity plus immutable release digest and supported engine/action versions. Inputs are service name, accountable owner reference, exposure, data class, jurisdiction, availability profile, runtime family, and destination; derive package and metadata names visibly. Preview lists normalized answers, files, managed ownership, repository/protection/catalog effects, permissions, estimates, and unknown provider checks. Render without network or broad credentials in an isolated workspace. Publish through a durable idempotent operation using narrow tokens. Acceptance parses configuration, builds, tests health behavior, validates locked dependencies, workflows, metadata, policy, secret absence, first deployment evidence, telemetry, ownership, and cleanup. Provenance records redacted inputs and digests. The team accepts project ownership; the platform owns the template, support, inventory, update-PR channel, support window, successor, and retirement evidence.

### Answer 2

Threats include malicious or mutable template source, hook code execution, dependency substitution, path traversal, link escape, shell/workflow injection through names, secrets in arguments/files/logs, token theft, overbroad repository permissions, duplicate creation after response loss, partial protections, CI workflows that expose tokens to untrusted changes, catalog spoofing, and false completion. Pin and authenticate sources; review changes; validate and normalize names; render in a sandbox without ambient credentials or network; reject paths outside destination; scan output; use structured APIs; separate effect actions with short-lived least-privilege tokens; store secret references only; persist idempotency and step evidence; verify repository identity, protections, CI permissions, catalog UID, and secret access policy; redact audit; and retain a recovery owner for unknown or partial outcomes.

### Answer 3

Partition by the four profiles, then select optional-feature combinations using risk and interaction: each feature alone, the default composition, all high-risk pairs, and the full combination only if supported. Add boundary names, absent options, denied owners, and consequential policy cases. For each selected case compare reviewed trees and modes, parse formats, build, test, scan, validate policy and metadata, and deploy representative ephemeral outputs. Upgrade from every supported prior template release for consumer-clean, common-customization, and conflict fixtures. Inject render failure, existing destination, response loss, authorization expiry, cancellation, provider throttling, and cleanup failure. Add traversal, injection, malicious hook, secret leakage, mutable fetch, and revoked dependency cases. Record explicitly untested combinations and block any combination the product claims to support but cannot validate proportionately.

### Answer 4

The critical CI permission correction should use targeted, prioritized pull requests plus continuous repository policy where enforceable; verify merges and exceptions. A style-guide change belongs in documentation, formatting tooling, or an optional low-noise pull request, not forced regeneration. A telemetry library moves through ordinary dependency updates and compatibility tests, while a centrally managed telemetry capability may reduce future copying. Runtime end-of-support needs inventory, successor profile, tested structural migration, reviewable project changes, staged support, and explicit exceptions. The consumer-owned domain model must remain untouched; offer guidance or a domain-owned migration if its owner requests one. Mechanism follows ownership and consequence, not template convenience.

### Answer 5

A `clinical-study-workspace` template may collect study identifier, accountable sponsor and investigator, protocol reference, classification, approved jurisdictions, authorized roles, analysis environment, retention class, and publication constraints. It renders pinned analysis structure, environment locks, data dictionaries, validation scripts, audit configuration, provenance metadata, and references to controlled data and secrets—not patient data or credentials. Separate authorized operations create access groups, storage, keys, and registries with durable identity and evidence. Validation proves structural conformance, access boundaries, reproducible reference analyses, audit capture, retention configuration, and owner acceptance; it does not claim protocol, ethics, statistical, clinical, privacy, or regulatory approval. Protocol authorities own study intent and amendments, data custodians own source data and access, analysts own derived code, and the platform owns scaffold quality. Local amendments are reviewed and preserved. Updates are risk-classified and traceable; closure verifies export, retention, revocation, evidence, and workspace retirement under applicable policy.
