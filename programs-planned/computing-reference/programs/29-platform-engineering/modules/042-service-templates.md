---
module_id: PLAT-042
program: Platform Engineering
level: 1
module_number: 42
title: Service Templates
status: complete
last_verified: 2026-09-02
---

# Service Templates

## One-Page Review

### Governing question

How should a platform design, execute, test, secure, version, upgrade, and retire service templates so they create owned, operable services quickly without copying secrets, freezing stale practices, concealing partial failure, or turning generated repositories into unmaintainable forks?

### Essential definitions

- A **service template** is a versioned product contract that validates intent, executes authorized actions, creates a minimal service seed and platform bindings, records provenance, and defines how consumers evolve.
- A **template specification** declares metadata, owner, supported archetype, input schema, policy, action graph, outputs, guarantees, non-guarantees, compatibility, and lifecycle.
- A **service seed** is the smallest generated repository content that establishes domain entry points and references centrally maintained capabilities; it is not a permanent copy of every organizational standard.
- A **template action** is one bounded operation in a scaffolding workflow, such as rendering files, creating a repository, registering a catalog component, or requesting an environment.
- An **execution** is a uniquely identified attempt bound to user/workload identity, template revision, normalized inputs, action revisions, status, outputs, and audit evidence.
- **customization surface** is the documented region consumers own and may change without losing supported upgrade behavior.
- **conformance** is current evidence that a service satisfies a versioned capability or policy contract; ancestry from a template is not conformance.
- **upgrade mechanism** is the maintained route that changes existing consumers through reusable dependencies, workflow revisions, migration tooling, or reviewable change proposals.
- **generation manifest** records template/action revisions, normalized non-secret inputs, generated paths, provider outputs, and applicable compatibility metadata.
- A **compensation** is a deliberate recovery action for a completed side effect after later workflow failure; it is not a general distributed rollback guarantee.

### Central model, mechanism, or theorem

For request $q=(u,a,p,v,x)$, authenticated user/workload $u$ selects archetype $a$, policy context $p$, template revision $v$, and inputs $x$. Validation and authorization produce normalized secret-free intent $x'$. An action dependency graph executes idempotent or explicitly compensated operations and emits service seed $F$, platform resources $R$, catalog relations $C$, and generation manifest $M$. Acceptance is safe only if resulting service passes structural, security, build, deployment, ownership, observability, and lifecycle gates. Later conformance depends on current service state and contract revision—not merely $M$ or template ancestry.

### Critical invariants

- Templates implement validated workload archetypes and user journeys; they are not organized primarily by team, framework fashion, or vendor.
- Template inputs express intent and references, never raw credentials, private keys, access tokens, or other reusable secret values.
- Identity, authorization, and policy apply independently to template visibility, input fields, actions, providers, outputs, task logs, retry, and cancellation.
- Every side-effecting action declares idempotency key, timeout, retry class, partial-result behavior, compensation or reconciliation, and audit semantics.
- Template revision, action revisions, source digests, normalized inputs, output identities, and status remain correlatable without exposing sensitive data.
- Generated code is minimal; rapidly changing standards live in governed dependencies, reusable workflows, policy, or platform capabilities with upgrade routes.
- Generated content has explicit ownership boundaries; upgrades never blindly overwrite consumer-owned code.
- A successful scaffold means the complete declared terminal outcome passed, not merely that files or a repository were created.
- Dry runs, render tests, and mocks do not prove external permissions, provider behavior, cleanup, or production readiness; integration and failure tests cover real boundaries.
- Catalog registration, accountable owner, support, documentation, build, artifact, deployment, configuration, secret references, connectivity, telemetry, cost, and retirement are coherent outputs where the archetype requires them.
- Existing services receive assessment and migration paths; greenfield templates do not become an excuse to abandon the installed fleet.
- Template and action deprecation includes consumer inventory, compatibility windows, migration evidence, revocation, and removal of obsolete providers and credentials.

### Common failures

Copying a large “perfect service” repository; creating one template per team; accepting passwords in forms; letting a privileged action run for every user; interpolating untrusted values into paths or shell commands; fetching an unpinned template branch; declaring success after repository creation; retrying non-idempotent provider calls; deleting useful evidence during compensation; logging rendered secrets; registering a catalog entity with a nonexistent owner; generating CI that uses broad tokens; embedding standards that cannot be upgraded; re-running the generator over modified code; measuring template launches rather than terminal service outcomes; and supporting new projects while inherited services drift indefinitely.

### Compact example

A team selects the `stateless-request-service` archetype and a supported runtime profile. The API validates a DNS-safe service identity, catalog group owner, data class, repository location, and environment intent; it accepts secret references but no values. An authenticated execution pins template and action digests, creates the repository idempotently, renders a small domain skeleton, binds versioned build/test/telemetry libraries and reusable workflows, registers component/API/resource relations, requests staging, and returns one operation status. A generated manifest records non-secret inputs and outputs. Integration gates build a signed artifact, deploy it, exercise health and telemetry, verify ownership and least privilege, then mark the service ready. Future dependency and workflow changes arrive as tested pull requests; customization files are never overwritten. Failed later actions reconcile or leave an explicit partial state and recovery route.

### Connections

Service templates operationalize [PLAT-041](041-workload-archetypes.md) through the coherent product boundary in [PLAT-040](040-designing-a-coherent-minimum-viable-platform.md). They compose repository, build, artifact, environment, deployment, configuration, secret, connectivity, observability, and data-access capabilities from [PLAT-031](031-application-build-capability.md) through [PLAT-039](039-database-and-data-service-access.md), while later modules specialize batch, event-driven, stateful, and golden-path evolution.

## Governing Question

What template product can turn an authorized service intent into a minimal, owned, buildable, deployable, observable, supportable service and continue helping it evolve after generation?

A template is executable organizational policy with supply-chain and infrastructure authority. It may create source repositories, grant teams access, configure workflows, request cloud resources, register ownership, and initiate deployments. Its defects reproduce at fleet scale.

Repository creation is only the first state transition. The intended outcome might be “an internal request service is healthy in staging with trusted build evidence, an owner, telemetry, documentation, rollback, and cost attribution.” Every intermediate success and partial failure must remain visible.

The design must balance standardization with product ownership. Consumers need safe defaults and upgradeable common capabilities, but generated domain code becomes theirs. A generator that repeatedly overwrites application logic replaces autonomy with a fragile central merge engine.

## Why This Matters

Templates compress expert decisions at the moment a project has the least local context. Good defaults can establish identity, ownership, secure supply chains, tested delivery, telemetry, and support before drift begins. Bad defaults institutionalize vulnerabilities, unused boilerplate, and hidden coupling.

Copying creates divergence. A defect fixed in the source template does not automatically change repositories already generated from it. GitHub repository templates create new repositories with unrelated history rather than a maintained merge relationship. Upgradeability therefore needs a deliberate mechanism.

Scaffolding spans multiple authorities. Repository creation may succeed while catalog registration, environment provisioning, or deployment fails. No general transaction can atomically roll back Git hosting, cloud providers, identity systems, and catalogs. Workflows require idempotency, reconciliation, compensation judgment, and durable status.

Templates are also user interfaces. Confusing inputs, unexplained policy denials, excessive choices, inaccessible forms, and secret exposure can negate automation. The platform must test the journey as carefully as the rendered code.

## Prerequisites and Retrieval

Retrieve workload archetypes, platform capability contracts, JSON Schema and validation, API idempotency, dependency graphs, workflow engines, distributed transactions and sagas, compensation, source control and repository permissions, code generation, templating and injection risks, file paths, escaping, supply-chain provenance, trusted builds, dependency management, semantic versioning, compatibility, automated pull requests, policy as code, catalog ownership, deployment, telemetry, user research, accessibility, secrets, audit, rate limiting, SLOs, incident response, cost allocation, and deprecation.

You should distinguish template from golden path; service seed from reference implementation; template source from rendered output; repository ancestry from current conformance; input intent from provider configuration; secret reference from secret value; dry run from real execution; task acceptance from terminal service readiness; retry from safe replay; compensation from atomic rollback; generated ownership from platform ownership; template revision from action/provider revision; and new-service success from fleet modernization.

## Learning Objectives

After completing this module, you should be able to:

1. define a service-template contract from a supported workload archetype and terminal user outcome;
2. design safe schemas, defaults, identity, authorization, and policy for template inputs;
3. decompose generation into bounded actions with idempotency, compensation, reconciliation, and durable status;
4. minimize generated code and separate consumer-owned customization from maintained common capabilities;
5. bind repositories, catalogs, builds, artifacts, environments, deployments, telemetry, support, cost, and retirement coherently;
6. establish source, action, dependency, and output supply-chain integrity;
7. test rendering, actions, security, usability, integration, failure, recovery, and upgrades;
8. upgrade and assess both generated and existing services without destructive re-scaffolding; and
9. govern template inventory, adoption, exceptions, deprecation, and retirement.

## Core Exposition

### Define the terminal outcome first

Begin with one archetype and journey. Name the user cohort, triggering intent, starting prerequisites, supported runtime profiles, and terminal state. “Files rendered” is an internal milestone; “owned service passes staging acceptance and is ready for its first domain change” is a user outcome.

List every output and authority: repository, team permission, catalog component, API/resource relations, build workflow, artifact namespace, environment, deployment, configuration schema, secret references, service identity, connectivity, telemetry, documentation, support route, cost owner, and deletion handle.

Not every template must create every capability. The selected archetype and declared scope determine required outputs. A library template may publish a package without a runtime; a request-service template needs a serving path.

State non-guarantees. Creation does not prove future code security, runtime reliability, user adoption, correct domain logic, current dependency health, or perpetual conformance.

### Write a versioned template specification

Specify stable identifier and revision, owner/support, archetype and profiles, intended cohort, prerequisites, input/output schemas, action graph, permissions, providers, policies, terminal conditions, failure/cleanup behavior, evidence, compatibility, upgrade mechanism, deprecation, and retirement.

Version the contract separately from its implementation release when helpful. A patch to documentation may not change output semantics; changing repository layout, workflow identity, required policy, or resource ownership may.

Pin source and action revisions by immutable digest or governed release. Fetching a mutable default branch makes identical requests produce different untraceable results and expands compromise risk.

Publish examples and a changelog describing generated and consumer impact. “Updated dependencies” is inadequate; identify affected capability, security/reliability consequence, and migration.

### Model inputs as intent

Ask only for decisions users understand and must own: service identity, accountable group, archetype profile, data classification, API visibility, recovery tier, repository namespace, and optional capabilities. Derive provider-specific fields from policy and adapters.

Use typed schemas with required fields, enums, formats, ranges, conditional dependencies, descriptions, examples, and defaults. Validate again server-side even when the portal or CLI validates locally.

Normalize before authorization and execution. Canonicalize names, references, paths, and enum values so policy and idempotency see one representation. Reject ambiguous Unicode, traversal components, reserved names, invalid owners, and output collisions.

Avoid free-form switches that bypass contracts. A text field called `extra_yaml` or `custom_command` transfers arbitrary provider authority into a supposedly safe template.

### Never accept raw secrets as ordinary parameters

Template forms, API bodies, task databases, audit events, logs, rendered files, source history, and error traces can retain inputs. Accept stable secret references or request a secret-binding capability; do not accept passwords, tokens, private keys, certificates with private material, or connection strings.

If a provider requires ephemeral authorization, obtain it through the execution's workload identity or a brokered, narrowly scoped credential. Keep it out of normalized inputs and generation manifests.

Classify even non-secret inputs. Repository visibility, tenant names, internal system topology, personal identifiers, and incident contacts may need restricted display and retention.

Test redaction before execution and at every action/log boundary. Masking a portal field does not prevent backend persistence.

### Authenticate and authorize every layer

Template discovery can reveal capabilities or organizational structure. Authorize listing, schema visibility, parameter visibility, execution, each privileged action, task status/logs, cancellation, retry, and outputs.

Derive actor and owner from authenticated catalog/organization authorities; do not trust a free-form `owner` string to grant repository or cloud permissions. Verify the actor may create for that owner and environment.

Backstage's scaffolder permission integration can control access to tasks, parameters, steps, and actions. That mechanism still depends on correct policies, identity resolution, template ingestion trust, and action implementation.

Separate platform author, action developer, template approver, provider administrator, and user roles. A template change can broaden infrastructure authority even when rendered source looks harmless.

Break-glass execution is time-bounded, strongly authenticated, audited, and reviewed. It must not become the path for fixing template usability gaps.

### Build a bounded action graph

Represent dependencies explicitly: reserve service identity before repository creation; create catalog owner relation before or with registration; obtain artifact namespace before writing workflows that target it. Parallelize only independent actions.

Each action declares input/output schema, required identity, side effects, idempotency key, preconditions, timeout, retryable and terminal errors, rate/capacity behavior, cancellation, sensitive fields, audit, compensation, and reconciliation.

Use globally unique execution and operation IDs. Provider requests should include deterministic client tokens where supported so a lost response can be queried rather than blindly replayed.

Treat action plugins as privileged supply-chain components. Pin, review, sign/build, scan, test, inventory, and restrict their network/filesystem/credential access. A small template cannot sandbox an unsafe action by convention.

### Handle partial failure honestly

Cross-provider creation is not one ACID transaction. Persist state before and after each effect, including provider operation/output identity. On restart, resume from observed state rather than assuming previous calls failed.

Compensation depends on value and reversibility. If repository creation succeeds but environment provisioning fails, deleting the repository may destroy user commits or diagnostic evidence. Mark it partial and offer retry or explicit cleanup unless automatic deletion is provably safe.

Reconciliation is often better than reverse-order rollback: converge missing catalog registration or environment state while preserving completed durable outputs. Bound retries and surface blocked ownership.

Define cancellation as a requested state, not instant erasure. An in-flight provider action may complete after cancellation; observe and reconcile its result.

Terminal statuses distinguish ready, failed with no side effects, failed partial/recoverable, cancelled clean, cancelled partial, and unknown. Never collapse unknown provider outcome into failure safe to retry.

### Make execution reproducible enough to investigate

Record template source digest, specification revision, action identifiers/digests, platform/provider adapter revisions, normalized non-secret inputs, actor/owner, timestamps, policy revision, output identities, rendered-content digest, and terminal evidence.

Perfect bit-for-bit reproducibility may be impossible when providers allocate identifiers or registries change. Separate deterministic rendering from external allocation and record both.

Use controlled clocks, locale, ordering, line endings, and generators for rendered fixtures. Avoid embedding generation time or random identifiers in source unless required and recorded.

SLSA defines provenance as verifiable information describing where, when, and how an artifact was produced. Apply the same traceability instinct to template outputs without claiming a SLSA level merely because a manifest exists.

### Generate a minimal service seed

The seed contains domain entry points, package/build metadata, a few representative tests, configuration schema/reference wiring, ownership/catalog descriptor, documentation entry, and references to maintained workflows or libraries.

Do not copy hundreds of lines of generic logging, HTTP, authentication, telemetry, retry, policy, and deployment code into every repository. Central packages, reusable workflows, and platform capabilities can receive fixes through explicit versions.

Minimize placeholder code. Users often retain sample endpoints, permissive settings, and TODO security markers into production. Every generated line needs purpose, ownership, tests, and a removal or maintenance story.

Keep examples safe and realistic. A health endpoint should demonstrate correct lifecycle semantics; sample configuration should use non-secret values and references; tests should assert behavior rather than only compilation.

### Define ownership and customization boundaries

Mark generated paths as consumer-owned, platform-maintained by dependency/reference, or replaceable generated configuration. Do not depend on comments alone when a schema, separate directory, or generated artifact boundary can enforce clarity.

Application domain code and tests become the product team's responsibility. Reusable workflow definitions, build images, policy bundles, and platform APIs remain owned by their providers under versioned contracts.

For regenerable files, store their source inputs and deterministic generator revision. Detect local modification and require review rather than overwriting.

Avoid “do not edit” files inside ordinary source trees when the platform cannot safely reconcile them. Prefer generated output in governed build paths or configuration projections.

### Bind a coherent catalog identity

Create or validate one stable component identity and accountable group. Link the repository, APIs, resources, environments, deployments, dashboards, runbooks, cost attribution, and support through that identity.

Backstage models components, APIs, resources, systems, domains, users, and groups. A template can register relationships, but the catalog may project other authorities and must not invent ownership absent from the organizational source.

Validate name collision and ownership before side effects. A failed late registration after creating resources can produce an orphaned service.

Record template/archetype revision as provenance or status, not as proof of present conformance. Runtime and repository state change independently.

### Establish trusted source and repository defaults

Create repository visibility, owner/team permissions, branch rules, code review, signed or verified changes where policy requires, security policy, vulnerability reporting, dependency update configuration, CI permissions, and archival/deletion rules.

Use least-privilege automation identities. Generated workflows should declare token permissions, pin third-party actions/dependencies as required by policy, avoid dangerous untrusted-code contexts, and separate pull-request validation from release authority.

OpenSSF Scorecard automates checks across source, build, dependency, testing, and maintenance practices. Its scores and checks are evidence, not a guarantee that generated or future code is secure.

GitHub repository templates copy directory structure and files into a new unrelated history. Treat this as seed creation; do not assume fixes to the template propagate.

### Connect build, artifact, and deployment paths

The generated project should build in the supported hermetic or controlled path, run tests, produce an immutable artifact with SBOM/provenance/signature policy, and deploy by digest through the archetype adapter.

Do not give repository workflows permanent cloud administrator credentials. Use workload federation or brokered short-lived authority scoped to build, publication, and deployment roles.

Parameterize environment intent through platform APIs, not copied provider YAML for every team. Preserve desired and observed revision, operation status, rollback, and evidence.

Run a terminal acceptance deployment in an isolated environment where safe. A template that only compiles can still create services incompatible with runtime policy, health, networking, or telemetry.

### Wire configuration, secrets, connectivity, and data access

Generate configuration schemas and non-secret defaults, plus references to platform delivery. Never render environment credentials or mutable production values into source.

Declare logical service/dependency identities and access requests, not fixed endpoints. Let environment and connectivity adapters resolve them with authentication, authorization, TLS, and network policy.

Database access uses separate runtime and migration roles, bounded pools, transaction expectations, and schema authority. A generic `DATABASE_URL` placeholder hides these decisions.

Template optional dependencies should compose tested capability modules. Arbitrary combinations can create unvalidated identity, order, cost, and failure interactions.

### Provide observability and operational readiness

Seed resource/service identity, structured events, bounded metrics, traces where applicable, deployment/configuration/archetype revision correlation, health semantics, starter dashboards, and alert/runbook references.

Avoid generating domain metrics or SLOs the template cannot know. Require teams to define user outcome, valid population, objectives, and response while supplying tested scaffolding.

Observe template execution itself: attempts, stages, queues, provider latency, retries, partial states, compensation, terminal outcomes, abandonment, and support contacts by bounded template/archetype/revision dimensions.

Exclude raw inputs, repository secrets, rendered configuration values, source payloads, and provider credentials from telemetry. Audit privileged actions separately under retention and access policy.

### Design the user experience

Use progressive questions grouped by decisions, with clear defaults, consequences, examples, validation, and links. Do not expose every provider option or hide consequential defaults.

Provide a review screen that shows normalized intent, resources and permissions requested, cost/recovery tier, irreversible effects, and applicable policy—without secrets. Backstage templates provide a review step, but the template author owns content quality.

Errors identify the invalid field or failed action, durable operation, completed effects, safe retry/cleanup, owner, and support route. Avoid dumping provider stack traces.

Ensure keyboard operation, labels, focus, error association, contrast, and screen-reader semantics in portal forms. Offer an API/CLI with equivalent contract for automation and users who prefer it.

### Test templates as products

Schema tests cover required/optional/conditional inputs, normalization, collisions, boundaries, invalid owners, forbidden names, and malicious strings. Authorization tests prove allowed and denied visibility, parameters, actions, status, logs, retry, and output access.

Render/golden tests compare deterministic output for canonical profiles without treating snapshots as semantic proof. Unit tests exercise actions, including timeouts, unknown provider outcomes, cancellation, redaction, and idempotent replay.

Dry run can reveal rendered files and predicted actions while intentionally avoiding real effects. Backstage documents dry-run support per custom action; action tests must prove the dry-run branch does not mutate external state.

Integration tests use actual test authorities and providers to create the repository/catalog/build/environment/deployment path, then update and delete it. Failure injection interrupts each boundary and validates resume, compensation, reconciliation, and evidence.

Security tests cover template injection, path traversal, unsafe filenames, symbolic links/archives where relevant, untrusted repository content, command arguments, network egress, secret leakage, action privilege, dependency substitution, and malicious pull-request workflows.

Usability tests observe representative users completing real creation and first-change tasks. Measure terminal success, active effort, confusion, abandonment, support, and remediation—not clicks alone.

### Treat dry run as a distinct guarantee

Label predicted versus validated fields. A dry run may validate schemas and render source, yet cannot prove a repository name remains available, an external permission is granted, a quota has capacity, or provider state will not change.

Do not invoke an unsafe action and hope a flag suppresses effects. Each action explicitly supports dry run, and tests assert absence of external mutations and sensitive logging.

Show the exact template/action revisions used by the preview. If execution occurs later under different revisions, require a new review or disclose/revalidate the change.

Retain dry-run audit separately from actual execution; it is not creation evidence and should not inflate adoption metrics.

### Build upgradeability into the first release

Choose the update channel for every generated concern:

- libraries and build plugins use dependency versions plus automated, tested change proposals;
- CI/CD uses versioned reusable workflows or centrally governed actions with compatibility and pinning policy;
- policies and platform capabilities evolve at declared control points with previews and compatibility windows;
- generated schemas/configuration use merge-aware migrations and local-modification detection;
- domain code remains consumer-owned and receives documented refactoring aids, never blind replacement.

Store consumer inventory and current observed versions. A generation manifest says what existed initially; repository/runtime scanning and authoritative platform state establish what exists now.

Test upgrade paths from every supported template revision, not only fresh generation. Include changed layouts, local customizations, removed dependencies, renamed services, and partial prior migrations.

Do not re-run the original generator over a living repository as the default upgrade. It cannot reliably distinguish user intent from stale generated content and may re-trigger external side effects.

### Measure drift and conformance responsibly

Define conformance as evidence against current contracts: owner exists, build path supported, artifacts trusted, runtime profile compatible, required telemetry present, policy satisfied, dependencies within support, and lifecycle owned.

Classify drift as intentional supported customization, temporary exception, stale version, policy violation, missing evidence, or provider mismatch. A file diff from the seed is not inherently bad.

Scorecards should link each finding to evidence, impact, remediation, owner, and exception route. Do not make one opaque percentage a release gate.

Use automated pull requests for safe changes and preserve product-team review. Avoid floods by batching compatible upgrades, respecting change budgets, and measuring merge/failure outcomes.

### Onboard existing services

Inventory existing services against the archetype and capability contracts. Separate missing identity/ownership, unsupported architecture, stale workflow/dependency, security gaps, runtime incompatibility, and purely cosmetic differences.

Offer import/adoption tooling that creates catalog/resource bindings and proposes minimal changes without regenerating domain code. An existing repository may use a different layout while satisfying all important contracts.

Prioritize high-risk and high-friction gaps. Do not demand wholesale rewrite merely to resemble the new seed.

Track greenfield and brownfield outcomes together. A platform that improves only new repositories while most production services remain unsupported has not standardized the fleet.

### Operate the template service

Set objectives for schema/list availability, execution admission, queue delay, stage completion, status freshness, and recovery from partial operations. Preserve existing service operation when the scaffolder is unavailable.

Apply quotas and fairness by user/team/template/provider. A burst of repository or environment requests can exhaust provider APIs, address space, build capacity, or cost budgets.

Maintain on-call/runbooks for stuck tasks, credential/action compromise, provider outage, template regression, mass-bad generation, catalog inconsistency, and cleanup backlog.

Canary new revisions with platform-owned fixtures and willing teams. Pause or roll back admission while preserving status and recovery for existing executions.

### Govern the template portfolio

Maintain template, revision, owner, archetype, runtime profiles, actions, providers, consumers, execution outcomes, support state, security review, costs, exceptions, and deprecation in a catalog.

Create a new template only for a durable archetype or materially distinct supported runtime journey. A different team name, color scheme, repository owner, or minor framework preference belongs in parameters or supported customization—not another fork.

Review overlap and usage. Merge near-duplicates through compatible paths; remove unused options and experimental actions before they harden.

Adoption does not prove value. Balance terminal journey success and time with first-change success, deployment reliability, security, support/toil, upgrade uptake, cost, and abandonment reasons.

### Deprecate and retire safely

Announce replacement, rationale, affected behavior/security, migration path, compatibility deadline, support, and exception process. Stop new executions before removing upgrade support for existing consumers.

Inventory consumers by generated and current state. Provide tested change proposals and verify terminal service behavior, not only manifest version.

After migration, revoke action/provider credentials and permissions, remove template discovery/admission, drain executions, reconcile partial outputs, archive required audit/provenance, delete unused test/provider resources, and remove obsolete actions last.

Retirement does not delete consumer services. It ends one template contract while keeping service ownership and supported replacement paths explicit.

The following executable inventory is synthetic template-governance evidence. It counts declared controls and does not prove rendered-code correctness, authorization, provider atomicity, supply-chain integrity, service readiness, upgrade safety, or user value.

<!-- bijux-verify: {"id":"service-template-control-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"templates 10\narchetype_owned 10\ninputs_secret_free 9\nactions_bounded 8\nprovenance_recorded 9\nterminal_tested 8\ncustomization_owned 8\nupgrade_supported 7\nexisting_service_path 7\nretirement_owned 8\n","stderr":""}} -->
```python
templates = [
    ("request-service", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("internal-api", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("public-api", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("service-with-store", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("service-with-events", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("grpc-service", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("library", 1, 1, 1, 1, 1, 1, 1, 0, 1),
    ("static-site", 1, 1, 1, 1, 1, 1, 0, 0, 1),
    ("legacy-import", 1, 1, 0, 1, 0, 0, 0, 1, 0),
    ("experimental-runtime", 1, 0, 0, 0, 0, 0, 0, 0, 0),
]
fields = [
    "archetype_owned", "inputs_secret_free", "actions_bounded",
    "provenance_recorded", "terminal_tested", "customization_owned",
    "upgrade_supported", "existing_service_path", "retirement_owned",
]
print("templates", len(templates))
for index, field in enumerate(fields, start=1):
    print(field, sum(row[index] for row in templates))
```

## Definitions and Notation

Let request $q=(u,a,p,v,x)$ contain authenticated actor $u$, workload archetype/profile $a$, policy context $p$, template revision $v$, and raw intent inputs $x$. Normalization $N(x)=x'$ must be deterministic for policy/idempotency and exclude secret material.

Represent action workflow as directed acyclic graph $G=(A,E)$ for actions $A$ and dependencies $E$ where possible. Some reconciliations form state machines rather than one DAG; persist execution state and provider identities across retries.

For action $i$, idempotency function $k_i(q)$ identifies one intended effect under defined scope. Equal keys prevent duplicate intent only if the action/provider enforces them correctly; they do not prove output correctness or cross-action atomicity.

Let result $Y=(F,R,C,M)$ contain rendered service seed $F$, external/platform resource identities $R$, catalog relations $C$, and generation manifest $M$. Terminal readiness predicate $T(Y,e)$ depends on required evidence $e$ for the archetype, not merely nonempty outputs.

Let template revision $v$, action vector $\mathbf{r}$, maintained dependency/workflow vector $\mathbf{d}$, and observed consumer state $s_t$ distinguish origin from current conformance. A consumer generated at $v$ is conformant at time $t$ only through current evidence over $s_t$, not ancestry alone.

## Mechanisms, Invariants, or Proof Structure

The service-template assurance chain is:

1. derive one terminal user outcome from a supported workload archetype and complete lifecycle;
2. specify versioned intent inputs, outputs, owners, policies, actions, terminal evidence, upgrades, and retirement;
3. authenticate the actor, normalize and authorize secret-free intent, and disclose consequences before execution;
4. pin reviewed template/action sources and execute bounded operations with durable identity, status, idempotency, and recovery;
5. render a minimal service seed with explicit consumer/platform ownership and maintained dependency/workflow references;
6. bind catalog identity, source controls, build/artifact, environment/deployment, configuration/secrets, connectivity, telemetry, support, cost, and deletion as required;
7. validate structure, security, rendering, actions, dry-run non-effects, real integration, failure/recovery, usability, and terminal service behavior;
8. record non-secret provenance and observe executions, partial states, outcomes, support, and provider effects;
9. maintain existing consumers through dependencies, reusable capabilities, reviewable migrations, and present-state conformance; and
10. stop admission, migrate consumers, drain/reconcile tasks, revoke authority, remove actions/providers, and preserve required evidence during retirement.

This chain does not prove generated domain logic is correct, providers are atomic, secrets cannot leak through an unknown plugin, users will adopt the output, current service state remains conformant, or a successful synthetic deployment predicts production reliability.

The invariants are archetype-driven scope, secret-free intent, layered authorization, bounded action semantics, correlatable revisions/outputs, minimal generated code, explicit ownership, terminal-outcome success, layered testing, coherent capability bindings, brownfield inclusion, and governed deprecation.

## Alternatives and Trade-Offs

**Repository template versus workflow scaffolder:** a repository template is simple and transparent but mainly copies files. A workflow can validate identity and create external bindings while adding privileged actions, state, failure, and operations.

**Large seed versus thin seed:** a large seed makes initial behavior visible and self-contained but copies defects and increases drift. A thin seed upgrades through maintained dependencies but introduces version and availability dependencies.

**Central reusable workflows versus copied CI:** central workflows propagate fixes and policy consistently. Copied workflows allow autonomy and local debugging but require fleet update automation.

**Strict uniformity versus customization:** strict output reduces combinations but can force workarounds. Explicit customization surfaces preserve domain ownership while limiting what the platform promises to upgrade.

**Automatic compensation versus retained partial state:** cleanup reduces leaks but can destroy user work and evidence. Retention aids recovery but creates cost and orphan risk; decide per action and execution stage.

**Dry run versus sandbox execution:** dry run is fast and non-mutating but cannot test real authorities/providers. Sandboxes expose integration behavior while consuming time, quota, and cleanup capacity.

**Greenfield generation versus brownfield adoption:** greenfield paths demonstrate standards quickly. Brownfield migration yields broader risk reduction but needs assessment and merge-aware changes.

**One multi-runtime template versus separate supported profiles:** one template reduces discovery but grows conditions and test combinations. Separate templates clarify contracts but can duplicate actions and create portfolio sprawl.

**Automatic upgrades versus pull-request proposals:** automatic central changes close urgent gaps quickly but can break services. Reviewable proposals preserve ownership and evidence while depending on timely adoption.

## Failure Modes and Misconceptions

- **“A template is a golden path.”** it may seed one part; a golden path covers the maintained end-to-end journey.
- **“Repository created means success.”** ownership, build, deployment, telemetry, support, and terminal evidence may still fail.
- **“Copying best practices standardizes the fleet.”** copies diverge unless maintained through upgrade mechanisms.
- **“Template ancestry proves compliance.”** current repository/runtime evidence determines conformance.
- **“Masked form fields make secrets safe.”** backend input, task state, logs, outputs, and source may retain values.
- **“Portal authorization protects actions.”** every task/action/provider/output boundary needs independent enforcement.
- **“Retry is harmless.”** repository, grant, resource, and deployment creation can duplicate or conflict without idempotency.
- **“Compensation is rollback.”** external effects can be irreversible, concurrent, or already used.
- **“Dry run validates execution.”** quotas, permissions, races, provider behavior, and cleanup remain untested.
- **“Snapshots prove templates work.”** they detect render change but not semantic or integration correctness.
- **“Generated files remain platform-owned.”** domain code belongs to the consumer unless a clear generated boundary exists.
- **“Re-scaffolding upgrades services.”** it can overwrite user intent and repeat external effects.
- **“One template per team provides flexibility.”** it creates forks with no durable semantic distinction.
- **“One universal template reduces maintenance.”** conditional combinations can become untestable and confusing.
- **“Security tooling scores guarantee safety.”** automated checks are bounded evidence with false positives/negatives and scope limits.
- **“New services are enough.”** existing production services retain most risk and toil.
- **“Deleting the template retires it.”** actions, credentials, consumers, executions, outputs, and support obligations remain.

## Worked Examples

### Example 1

A template copies 2,000 lines of logging, HTTP, CI, deployment, and policy code. A security fix requires 300 repository edits. Moving common behavior to versioned libraries, reusable workflows, and platform APIs leaves a small seed. Conclusion: generation without upgrades manufactures drift.

### Example 2

A form accepts a database password and masks it visually. The value persists in task JSON and error logs. The template accepts an authorized secret reference and binds delivery at runtime. Conclusion: UI masking is not secret handling.

### Example 3

Repository creation succeeds, but catalog registration times out after committing. A blind retry reports collision and deletes the repository. Durable provider identity and reconciliation discover the existing repo and complete registration. Conclusion: unknown outcomes need observation, not destructive replay.

### Example 4

A custom action interpolates service name into a shell command and output path. A malicious name injects flags and traversal. Typed normalization, direct API calls, safe path joining, fixed arguments, and adversarial tests remove the channel. Conclusion: template inputs cross privileged interpreters.

### Example 5

The task turns green after source rendering, although generated code cannot build under the supported workflow. Terminal acceptance builds, produces a trusted artifact, deploys staging, and checks health/telemetry. Conclusion: success follows the user outcome.

### Example 6

An urgent workflow fix is applied only to the template repository. Existing services remain vulnerable. A pinned reusable workflow revision and automated tested pull requests update consumers with evidence. Conclusion: template fixes do not propagate by ancestry.

### Example 7

An upgrade generator overwrites a team's domain handler because it matches old seed text. Ownership boundaries make domain files immutable to automation; a migration proposes only maintained configuration changes. Conclusion: upgrades must preserve consumer intent.

### Example 8

A dry run reports that a production environment will be created, but the actor lacks provider quota and the name is taken at execution time. The preview labels these as predictions and the execution revalidates before effects. Conclusion: dry runs have bounded guarantees.

### Example 9

Each language team forks the service template to change five build fields. Shared actions and archetype contract plus supported runtime-profile adapters reduce eight forks to one product with tested variants. Conclusion: provider variation need not become template ownership sprawl.

### Example 10

The greenfield path is excellent, but 200 existing services lack owners and trusted builds. Import assessment links identities and proposes targeted changes without replacing domain layouts. Conclusion: standardization requires a brownfield path.

## Cross-Program Connections

- **Software Engineering:** code generation, modularity, dependency management, semantic versioning, testing, refactoring, and ownership govern maintainability.
- **Computer Security:** input validation, injection, least privilege, secrets, supply-chain provenance, workflow tokens, audit, and threat modeling constrain authority.
- **Distributed Systems:** idempotency, partial failure, unknown outcomes, reconciliation, compensation, queues, and durable state shape executions.
- **Human-Computer Interaction:** progressive disclosure, review, accessibility, error recovery, and usability determine whether self-service works.
- **Product Management:** cohort needs, terminal outcomes, adoption, support, portfolio scope, migration, and retirement make templates products.
- **Configuration Management:** schemas, normalization, generated boundaries, drift, present-state conformance, and change proposals preserve intent.
- **Reliability Engineering:** SLOs, failure injection, status, runbooks, canaries, rollback, and cleanup make scaffolding operable.
- **Economics:** template/action sprawl, support toil, provider quota, upgrade cost, brownfield debt, and opportunity cost guide investment.
- **Governance:** accountable owners, policy, exceptions, evidence, retention, and deprecation keep fleet standards legitimate.

## References

1. CNCF TAG App Delivery, “CNCF Platforms White Paper,” current edition, retrieved 2026-09-02. https://tag-app-delivery.cncf.io/whitepapers/platforms/
2. Backstage Project, “Software Templates,” current documentation, retrieved 2026-09-02. https://backstage.io/docs/features/software-templates/
3. Backstage Project, “Writing Templates,” current documentation, retrieved 2026-09-02. https://backstage.io/docs/features/software-templates/writing-templates/
4. Backstage Project, “Authorizing Scaffolder Tasks, Parameters, Steps, and Actions,” current documentation, retrieved 2026-09-02. https://backstage.io/docs/features/software-templates/authorizing-scaffolder-template-details/
5. Backstage Project, “Dry Run Testing,” current documentation, retrieved 2026-09-02. https://backstage.io/docs/features/software-templates/dry-run-testing/
6. Backstage Project, “Audit Events,” current documentation, retrieved 2026-09-02. https://backstage.io/docs/features/software-templates/audit-events/
7. Backstage Project, “System Model,” current documentation, retrieved 2026-09-02. https://backstage.io/docs/features/software-catalog/system-model/
8. GitHub, “Creating a Repository from a Template,” current documentation, retrieved 2026-09-02. https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template
9. SLSA, “Provenance,” specification version 1.2, retrieved 2026-09-02. https://slsa.dev/spec/v1.2/provenance
10. NIST, “Secure Software Development Framework (SSDF) Version 1.1,” SP 800-218, February 2022. https://csrc.nist.gov/pubs/sp/800/218/final
11. OpenSSF, “OpenSSF Scorecard,” current project documentation, retrieved 2026-09-02. https://scorecard.dev/
12. JSON Schema, “JSON Schema Core,” Draft 2020-12, retrieved 2026-09-02. https://json-schema.org/draft/2020-12/json-schema-core
13. OpenGitOps, “GitOps Principles,” version 1.0.0, retrieved 2026-09-02. https://opengitops.dev/

## Exercises

### Exercise 1

Define service template, template specification, service seed, action, execution, customization surface, conformance, upgrade mechanism, generation manifest, compensation, dry run, and terminal outcome. State one non-guarantee for each.

### Exercise 2

Design a request-service template from authenticated intent through normalization, authorization, repository/catalog creation, build/artifact, environment/deployment, configuration/secrets, connectivity, telemetry, acceptance, upgrade, and retirement. Mark every owner, authority, status, and partial-failure decision.

### Exercise 3

A template accepts passwords, fetches a mutable branch, interpolates names into shell, runs all actions as administrator, retries repository creation blindly, deletes outputs on any failure, declares success after rendering, copies 3,000 lines of standards, has no upgrade path, and ignores existing services. Diagnose at least fifteen defects and correct them.

### Exercise 4

Design a service-template portfolio for 60 teams using four languages, three repository providers, regulated and non-regulated environments, two request-service profiles, and 400 existing services. Minimize template sprawl while preserving identity, policy, supply-chain, provider, customization, testing, and migration requirements.

### Exercise 5

A critical template action and reusable workflow are compromised after 120 services were generated. Design containment, inventory, provenance analysis, credential revocation, consumer remediation, verification, communication, rollback, evidence retention, and safe restoration or retirement.

## Answers to the Exercises

### Answer 1

A service template is a maintained creation/evolution contract but cannot guarantee future code quality. A specification versions intent, actions, outputs, evidence, and lifecycle but may be implemented incorrectly. A seed is minimal initial content but does not remain current automatically. An action is a bounded workflow operation but its provider may return unknown outcomes. An execution binds actor/revisions/state but cannot make cross-provider effects atomic. A customization surface identifies consumer-owned variation but cannot prevent unsupported edits. Conformance evaluates current evidence but is limited by check coverage and freshness. An upgrade mechanism changes consumers but cannot guarantee compatibility with every customization. A generation manifest records origin and outputs but not current state. Compensation responds to prior effects but cannot universally reverse them. A dry run predicts/render-checks without proving permissions, capacity, or provider effects. A terminal outcome defines accepted completion but cannot prove long-term reliability or business correctness.

### Answer 2

The platform product owner defines terminal staging readiness for the stateless request archetype. The actor authenticates and selects owner, stable name, runtime profile, data class, API visibility, and environment intent; schemas normalize values, organization/catalog authorities validate owner, policy authorizes every effect, and no secret values enter inputs. A pinned template/action set reserves component identity and executes durable idempotent steps: create repository and least-privilege team binding, render thin seed and generation manifest, register catalog component/API/resource relations, configure trusted build and artifact namespace, request isolated environment, deploy digest with configuration schemas and secret references, establish logical connectivity, and attach telemetry/runbook/cost. Each step records provider identity and handles timeout, retry, cancellation, compensation, or reconciliation; failure retains valuable user work and exposes partial state. Acceptance builds/tests, verifies provenance and repository controls, deploys staging, exercises health/telemetry/rollback, and marks the common operation ready. Product team owns domain code; platform/provider teams own reusable capabilities. Inventory, dependency/workflow proposals, compatibility tests, and merge-aware migrations upgrade it. Retirement stops new use, migrates consumers, drains tasks, revokes authority, removes actions/providers, and preserves required audit while consumer services continue under the replacement contract.

### Answer 3

Passwords can persist across forms, task storage, logs, and source; accept authorized references and runtime delivery. Mutable branches make output untraceable and vulnerable to source changes; pin reviewed digests/releases. Shell interpolation permits injection and traversal; normalize typed inputs, use fixed-argument APIs and safe paths, and adversarially test. Administrator execution violates least privilege and selective authorization; use actor-derived, per-action brokered identities with independent permissions and audit. Blind repository retry can duplicate or collide after an unknown success; use deterministic client tokens, persist state, query provider result, and reconcile. Blanket deletion can destroy commits/evidence and itself partially fail; define per-effect compensation and retain valuable partial state with cleanup ownership. Render success is not user success; require ownership, build, trusted artifact, deployment, health, telemetry, and terminal evidence. Copying 3,000 standard lines creates fleet forks; keep a thin seed and move common behavior to versioned libraries, reusable workflows, policy, and platform capabilities. No upgrade path freezes vulnerabilities; inventory consumers and issue tested proposals/migrations. Ignoring existing services leaves most risk untouched; provide assessment/import and targeted adoption. Further fixes include explicit archetype scope, source/action provenance, secret-safe audit, schema boundaries, cancellation, rate limits, dry-run semantics, customization ownership, usability/accessibility, SLO/support, cost, deprecation, and retirement.

### Answer 4

Define one request-service archetype contract with two tested profiles rather than multiplying language/provider combinations. Use a common intent schema, identity/catalog model, action/status API, security policy, generation manifest, and acceptance suite. Implement four runtime adapters that render minimal language seeds and bind versioned build/test/telemetry libraries; use shared actions for catalog, environment, artifact, and deployment. Implement three repository-provider adapters behind one repository capability, exposing only material provider limits. Regulated profiles add reviewed data/environment policy, stronger source/artifact evidence, restricted actions, audit/retention, and deployment approval without forking every runtime. Template combinations are admitted only if included in a compatibility matrix; uncommon combinations use owned exceptions. Consumer-owned domain paths remain separate from regenerable configuration. Test schema, rendering, action security/idempotency, each supported provider/runtime/profile integration, failure recovery, acceptance deployment, and upgrades. Inventory all 400 services by archetype, owner, provider, language, controls, and current capability versions; import catalog/resource bindings and propose risk-prioritized dependency/workflow/policy changes without replacing layouts. Portfolio governance tracks use, support, cost, exceptions, and deprecates redundant variants.

### Answer 5

Pause affected template/action admissions and workflow releases while preserving read-only task/status evidence. Revoke action, repository, build, artifact, cloud, and signing credentials within the compromised trust boundary; rotate downstream authority and isolate suspicious infrastructure. Use generation manifests, action/template/workflow digests, execution audit, repository histories, artifact provenance, deployment inventory, and current scanning to identify all potentially affected executions and services—ancestry alone is insufficient, and absence of evidence is not clearance. Notify service owners, security, incident command, providers, and leadership with affected revisions, actions, uncertainty, containment, and safe operating guidance. Quarantine untrusted artifacts and workflow runs; inspect unauthorized repositories, grants, resources, source changes, secret access, and releases. Issue signed, reviewed remediation changes that replace workflows/actions, rotate credentials, rebuild from trusted source/builders, verify artifacts, redeploy canaries, exercise service behavior, and then progress by risk. Roll back to a known trusted revision only if its dependencies and credentials remain trusted. Preserve evidence under incident/legal retention without secrets in broad tickets. Root-cause source, review, build, distribution, permission, and audit gaps; restore through new trust roots, narrowed actions, independent verification, canaries, and monitoring, or retire the action/template and migrate consumers if trust cannot be re-established.
