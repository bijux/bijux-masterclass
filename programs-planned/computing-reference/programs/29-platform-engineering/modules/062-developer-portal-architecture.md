---
module_id: PLAT-062
program: Platform Engineering
level: 2
module_number: 62
title: Developer Portal Architecture
status: complete
last_verified: 2026-09-02
---

# Developer Portal Architecture

## One-Page Review

### Governing question

How should a developer portal unify discovery, documentation, status, and self-service journeys without becoming an all-powerful control-plane monolith, a stale source of truth, an inaccessible dashboard, or a supply-chain path into every engineering system?

### Essential definitions

- A **developer portal** is a product experience that composes discoverability, guidance, read models, and authorized actions over platform and engineering capabilities.
- A **portal shell** owns navigation, layout, identity session, design system, routing, and extension assembly; domain semantics remain in capability contracts.
- A **plugin** is a versioned, permission-aware extension with declared routes, APIs, data, dependencies, ownership, and lifecycle.
- A **backend for frontend (BFF)** adapts backend data and authentication for a user experience without becoming the authoritative domain API.
- A **read model** is a derived, query-optimized view with source, revision, freshness, and rebuild semantics.
- A **software template** is a guided, versioned input and action definition for a repeatable journey; it is neither continuous reconciliation nor proof of outcome.
- A **task** is a durable execution instance with identity, requester, inputs, permissions, steps, outputs, logs, status, cancellation, and retention.
- **progressive disclosure** presents the common decision path first while keeping advanced detail discoverable and contextual.
- A **capability card** is a bounded UI projection of one owned capability; it must fail independently of unrelated cards.
- A **plugin trust tier** states which APIs, secrets, browser privileges, backend credentials, and actions an extension may use.

### Central model, mechanism, or theorem

For journey $j$, let step success probability be $p_{jk}$ and active user effort be $e_{jk}$. A simplified journey model is

$$
P_j=\prod_k p_{jk}, \qquad E_j=\sum_k e_{jk}.
$$

This independence/product approximation is diagnostic, not a measured guarantee: abandonment, correlated dependencies, and conditional branches require real funnel evidence. Portal architecture should remove avoidable steps while preserving consequential review. The shell authenticates and composes UI; permission-aware plugins call BFFs or canonical domain APIs; read models declare freshness; self-service persists a uniquely identified task or declarative resource before effects; workers reauthorize consequential steps and use scoped credentials; logs/audit are protected; and optional plugins fail behind local boundaries. A portal outage must not stop already accepted reconciliation or eliminate direct API/CLI/Git access.

### Critical invariants

- Portal, CLI, SDK, Git, and direct API paths share domain schema, defaults, authorization, status, and lifecycle semantics.
- The browser never receives platform-wide provider credentials or trusts hidden UI elements as authorization enforcement.
- Sign-in identity mapping is unambiguous, tested for account linking/hijack, and separated from delegated third-party tokens.
- Each action is authorized at backend/task/effect boundaries against current identity, object, tenant, and policy—not only when a button renders.
- Catalog, search, cost, health, and ownership cards identify authority, observation time, revision, staleness, and remedy.
- Tasks persist requester, authorized input, template/action versions, operation identity, checkpoints, outputs, audit, and cancellation semantics.
- Secrets are referenced or brokered just in time, redacted from URLs/forms/logs/events, least-privilege, short-lived where possible, and revoked after use.
- Plugins declare ownership, trust tier, dependency/performance budget, data handling, accessibility, compatibility, failure boundary, and retirement plan.
- Essential journeys remain keyboard-operable, screen-reader meaningful, responsive, and understandable under error, slow network, zoom, and localization.
- Optional plugin failure cannot blank the shell, block unrelated actions, exhaust shared resources, or corrupt canonical state.

### Common failures

Treating the portal as the platform; placing defaults only in forms; hiding buttons instead of enforcing permissions; sending user/provider tokens to arbitrary plugins; using a guest or ambiguous sign-in resolver in production; browser-direct calls to privileged third parties; one backend with every credential; search results as ownership truth; no freshness labels; secret input in task logs; templates from untrusted catalog locations; custom actions with unrestricted filesystem/network; retrying a task by replaying all effects; cancel meaning rollback; infinite dashboards; synchronous page fan-out; inaccessible custom controls; incompatible plugin upgrades; measuring page views rather than completed journeys; and removing a plugin while tasks and consumers remain.

### Compact example

A team opens a service page. The shell renders ownership and documentation from catalog read models with source revision and last-sync time; deployment health and cost cards load independently with timeouts. “Create production environment” uses a schema generated from the canonical `Environment` API, explains cost/security consequences, previews the current policy resolution, and posts a client operation ID to a task/domain backend. The backend reauthenticates, stores requester/input/template/action versions, and returns a task ID. A worker acquires scoped short-lived credentials per step, checkpoints external operation IDs, redacts logs, and publishes domain status. Refreshing the browser or losing the portal does not duplicate work. A failed cost plugin shows local degraded state; direct API/CLI remains available. Keyboard, focus, live progress announcements, error summaries, and reduced-motion behavior are tested.

### Connections

This module specializes the experience and access boundaries from [PLAT-061](061-platform-api-layers.md) and projects the domain contract from [PLAT-060](060-designing-a-domain-specific-platform-api.md). PLAT-063 deepens catalog authority and ingestion; PLAT-064 ownership metadata; PLAT-065 workflow; PLAT-066 policy; and PLAT-070 portal-component integration without monolithic coupling.

## Governing Question

How can a portal give developers one coherent place to understand and act on their software estate while remaining a replaceable, least-privilege experience over independently owned systems?

A successful portal feels integrated: identity is consistent, terminology is familiar, related information is colocated, and self-service has clear progress. Architectural success is almost the opposite of centralization. Domain state, workflow checkpoints, policies, source code, provider effects, and operational telemetry retain their owners. The portal assembles them without silently taking ownership.

The difficult boundary is action. Read-only integration can already leak sensitive topology or stale ownership; scaffolding and operational actions can create repositories, credentials, deployments, accounts, and bills. Portal architecture must treat plugins, templates, actions, identity mapping, and proxies as privileged software supply chain.

## Why This Matters

Developer portals sit at a high-value intersection. They know people, teams, repositories, services, dependencies, incidents, infrastructure, and credentials. Compromise or authorization confusion can traverse many systems.

Portals can also multiply usability. One well-designed journey can replace tickets and fragmented documentation for thousands of users. One misleading readiness card or hidden default can equally multiply mistakes.

An integrated page has many dependencies. Without timeouts, local error boundaries, read models, and performance budgets, the slowest plugin controls the experience. Optional data becomes a platform-wide outage.

The portal is often mistaken for the platform’s source of truth. Catalog entities and search indexes are useful derived models, while Git, domain APIs, identity systems, provider state, and workflow stores may each remain authoritative for different facts. Architecture must make this visible.

Accessibility and internationalization are correctness, not polish. A self-service action inaccessible by keyboard or a progress state invisible to assistive technology excludes users and creates operational workarounds.

## Prerequisites and Retrieval

Retrieve internal developer platforms, platform as product, user research and journey mapping, information architecture, frontend shells and micro-frontends/plugins, backend-for-frontend, API gateways, identity federation and account linking, authentication versus authorization, OAuth/OIDC and delegated tokens, sessions/CSRF/CORS, permission decision/enforcement, software catalogs and search indexes, schemas/forms, templates and scaffolding, durable tasks/workflows, idempotency and cancellation, secret brokerage, least privilege, browser security, supply-chain security, sandboxing, observability/audit, SLOs and performance budgets, cache freshness, error boundaries, responsive design, localization, WCAG accessibility, versioning, feature flags, backup/recovery, and decommissioning.

You should distinguish portal from platform; shell from plugin; frontend authorization hint from backend enforcement; sign-in identity from delegated access token; BFF from system of record; catalog from source; search ranking from policy; template definition from task instance; retry from restart; cancel from compensation; task log from audit record; trace ID from operation ID; card health from capability health; page availability from accepted-work continuity; UI feature flag from security boundary; and installation from governed plugin lifecycle.

## Learning Objectives

After completing this module, you should be able to:

1. define portal product boundaries, personas, journeys, information architecture, and non-goals;
2. design shell, frontend plugin, BFF/backend plugin, domain API, and read-model boundaries;
3. secure sign-in resolution, sessions, delegated credentials, permissions, proxies, templates, and actions;
4. build durable, idempotent, auditable self-service task experiences with explicit cancellation and recovery;
5. control catalog/search freshness, page fan-out, performance, backpressure, and degraded behavior;
6. govern plugin and template supply chains through trust tiers, manifests, review, isolation, and retirement;
7. verify accessibility, localization, responsive behavior, privacy, and user comprehension;
8. measure journey outcomes and operate, upgrade, recover, and decommission the portal; and
9. preserve canonical domain semantics and alternate access paths during portal failure.

## Core Exposition

### Define the portal’s product boundary

Start with personas and journeys, not a plugin catalog. Common personas include application developer, service owner, incident responder, security reviewer, platform operator, engineering manager, and new joiner. Their information and action needs overlap but are not identical.

Observe discover, understand, create, change, diagnose, recover, transfer, and retire journeys. Record starting context, questions, decisions, authoritative evidence, handoffs, wait time, active effort, errors, and completion criteria. A homepage full of links is not a product journey.

State non-goals. The portal should not become the sole domain API, provider credential vault, workflow database, log warehouse, incident system, or source-code authority merely because it can link them. Integration is not ownership.

Prioritize recurrent, high-friction paths. Progressive disclosure keeps the common path comprehensible while deep links preserve expert detail. Avoid a generic “single pane of glass” objective; no screen can make every system current, complete, and actionable simultaneously.

Define alternate paths. Automation needs API/SDK/Git; incident recovery may need CLI or break-glass access independent of the portal. Accepted work continues if the browser session closes or the portal is down.

### Design the shell as a narrow composition root

The shell owns bootstrapping, global navigation, page layout, route binding, theme/design tokens, identity/session integration, feature discovery, error boundaries, localization framework, accessibility primitives, and shared client facilities. It should be boring and stable.

Plugins contribute bounded pages, cards, search results, actions, or navigation. They use published extension points and client interfaces instead of importing another plugin’s internals. This permits independent testing and replacement.

Keep global state small. One mutable frontend store containing catalog, tasks, permissions, cost, incidents, and provider objects couples releases and leaks data across plugin boundaries. Use domain clients and scoped caches with explicit invalidation.

Route and extension indirection allows integrators to replace or omit plugins. Missing optional routes should degrade to a clear unavailable state, not crash the app. Detect conflicting route/extension registrations at build or startup.

The shell is not a super-controller. It may coordinate presentation, but backend systems own effects and state transitions.

### Choose frontend, BFF, and domain boundaries

Browser-only plugins suit public or already user-authorized data and local presentation. A BFF is appropriate for token exchange, server-side secrets, response aggregation, protocol adaptation, caching, and protection from browser constraints. Canonical writes still go to domain/task APIs.

Do not expose broad third-party tokens to frontend JavaScript. A backend proxy that forwards arbitrary paths with a powerful token merely moves the vulnerability. Constrain destination, method, resource, identity, scope, headers, size, and response.

Each backend plugin owns its schema/database and can be deployed separately when scale or security requires. Shared runtime services for logging, auth, discovery, and databases do not justify direct table access between plugins.

Avoid a universal BFF that accumulates every credential and transaction. Prefer capability-aligned backends and a thin shell. Aggregation for one page can occur through parallel bounded calls or a read model without making the aggregator authoritative.

Document browser→backend→domain/provider flows with identity, credentials, data classification, CORS/CSRF, cache, timeout, and audit at each hop.

### Establish identity without account ambiguity

Sign-in authenticates a human and maps the external identity to one internal subject. Delegation authorizes access to another service on that user’s behalf. These are different tokens and risks.

Configure one unambiguous resolver per intended sign-in method, using stable verified identifiers. Email local-part or mutable display-name matching can collide across domains or account changes. Test duplicate accounts, renamed users, contractor conversion, disabled users, multiple identity providers, and rehire.

Short-lived portal sessions should have secure cookies, appropriate same-site/CSRF controls, rotation, logout/revocation behavior, and no tokens in URLs or browser storage beyond the threat model. Privileged actions may require fresh authentication or step-up.

The catalog can enrich identity and group membership, but a missing or stale entity should not silently map an attacker to a privileged subject. Define authority and freshness for employment and group claims.

Service/automation clients need distinct non-human identities and APIs; simulating a person through a browser session destroys audit and lifecycle.

### Enforce permissions at consequence boundaries

Frontend permission checks improve navigation and prevent confusing choices. They are not enforcement because clients can call backend endpoints directly. Every backend plugin declares and enforces permissions for its resources/actions.

Complex tasks need more than create-task permission. Authorize template visibility, sensitive parameters, steps/actions, target resources, output/log access, cancellation, retry, and the downstream effect. A step added in a later template version must not inherit authority accidentally.

Policy input includes current subject/group/tenant, object ownership, environment, action, resource, and sometimes data classification. Record decision and policy revision. Reauthorize irreversible or delayed effects when policy demands; do not assume the launch-time session grants indefinite power.

Avoid existence leaks. Search, autocomplete, task lists, logs, and error messages must filter before returning sensitive entity names or metadata. Hiding a card after fetching unauthorized data is too late.

Separate portal operator, plugin developer, template author, capability owner, security approver, and ordinary user roles. Installation/configuration rights can be more powerful than clicking any one action.

### Treat the plugin ecosystem as supply chain

A plugin can execute browser code in the portal origin, access shared clients, render deceptive UI, call backends, and introduce dependencies. Backend plugins/actions may hold credentials or execute code. Govern them like privileged software.

Maintain a registry with package/source, version and integrity/provenance, license, maintainer, trust tier, requested frontend/backend capabilities, routes, APIs, secrets, data, permissions, network destinations, dependencies, update cadence, vulnerabilities, accessibility, SLO, and retirement.

Use trust tiers. A read-only public-data card differs from a plugin that reads catalog-wide metadata, streams task logs, or creates cloud accounts. Isolate higher-risk backends by process/network/credential boundary; browser code sharing one origin has limited security isolation even if visually sandboxed.

Review dependency and build provenance; pin versions/lockfiles; scan/sign artifacts according to policy; test configuration migration; stage upgrades; and have a disable/rollback plan. A marketplace listing is not security review.

Extension APIs are public contracts. Keep them minimal, versioned, and capability-oriented. Direct imports across plugin internals create a portal monolith disguised as packages.

### Govern templates and actions separately

Template visibility is not execution authorization. A template defines input schema, steps, action identifiers, output links, and presentation. Every referenced action is independently installed and privileged.

Restrict who may publish and which sources may be ingested as templates. Validate signed/approved revisions, pin or record the exact template revision at task creation, and prevent a template change from mutating an already accepted task.

Actions declare input/output schema, permissions, secret needs, network/filesystem access, idempotency, timeout, retry, cancellation, cleanup, audit, and support owner. Avoid generic `run shell`, arbitrary URL fetch, or unrestricted repository write under broad credentials.

Dry run helps inspect rendered output but does not prove external permissions, concurrency, provider behavior, or cleanup. Separate simulated outputs and audit so users cannot mistake them for effects.

Review generated repositories/configuration for injection, secret exposure, ownership, branch protection, dependency pinning, and update path. Scaffolding creates a starting point; continuous maintenance needs other mechanisms.

### Persist task identity before effects

At submission, server-side schema and policy validate current input, then store task ID, client operation ID, requester/tenant, template and action versions, normalized inputs or protected references, policy decision, creation time, and intended outputs. Return only after durable acceptance.

Workers acquire scoped credentials just in time, checkpoint each effect with idempotency/provider identity, and record bounded events. Refreshing or retrying the page queries the existing task instead of resubmitting.

Define retry. It may resume from a safe checkpoint, rerun a failed idempotent step, or create a new task linked to the old one. Replaying all steps can create duplicate repositories, accounts, or resources.

Define cancellation. It stops future cancellable work; it does not imply rollback of completed external effects. State `CancelRequested`, current non-interruptible action, residual effects, compensation options, and final disposition.

Protect task visibility, inputs, logs, artifacts, and outputs independently. Retain audit longer than verbose logs when needed, with deletion/privacy policy.

### Broker secrets instead of moving them through the UI

Prefer workload identity or delegated short-lived tokens acquired by the backend worker for a narrowly scoped step. If a user must supply a secret, use a dedicated sensitive channel, never query parameters, analytics, ordinary form persistence, task input JSON, template output, or logs.

Templates reference secret names/scopes, not values. Workers read at execution time under task identity, prevent cross-tenant name guessing, and avoid returning secrets in status. Redaction is defense in depth, not permission to log first.

Rotate/revoke after completion or cancellation where appropriate. Record secret version/reference and access event without material. Failure messages must not echo tokens or credential-bearing URLs.

Separate credentials by plugin/action/provider and environment. One portal backend token able to administer source control, cloud, CI, and identity makes every plugin a cross-system escalation path.

Test malicious templates, log injection, exception serialization, analytics capture, browser developer tools, task replay, support exports, and backup access.

### Design catalog and search as explicit read models

Catalogs ingest metadata from source control, organizational directories, cloud inventory, domain APIs, and other providers. For each field, declare authority and merge/ownership rules. “Last writer wins” can let a low-trust processor overwrite ownership.

Processing and stitching can introduce lag or errors. Surface source, last successful observation, source revision, processing status, and incomplete/unprocessed state. Absence from the catalog does not prove nonexistence.

Search is even more derived. Indexing, authorization filtering, ranking, stemming, and retention alter results. Filter authorized documents before disclosure and treat search results as navigation, not policy or deletion evidence.

Page cards should state observed time and link to authoritative systems. Before a consequential action such as ownership transfer or delete, the backend rereads authority with identity/revision checks.

Design rebuild. Catalog/search databases and caches must be reconstructible from declared sources or backed up where they contain non-derivable ownership/annotation state.

### Compose pages with local failure boundaries

A service page may contain identity, ownership, docs, dependencies, builds, deployments, SLOs, incidents, cost, security, and actions. Load independent cards concurrently with deadlines and cancellation; avoid serial waterfalls.

Each card has loading, empty, unauthorized, stale, unavailable, and error states. One thrown exception, invalid payload, or slow backend must not blank the page. Bound response size, pagination, and rendering work.

Classify critical content. Identity/name/owner and primary action status may be essential; cost recommendations or recent news may be optional. The shell can render useful core state while optional cards degrade.

Do not silently show stale data as current. A stale last-known deployment state may be useful with timestamp and refresh; security revocation or destructive preconditions may require fail closed.

Prevent thundering herds on popular pages through cached read models, request coalescing, pagination, and per-plugin/tenant limits. Do not let one integration consume every backend connection.

### Use explicit performance and dependency budgets

Set budgets for shell JavaScript/CSS, startup, authentication, core content, plugin bundles, API calls, p50/p95/p99, error rate, and interaction responsiveness. Measure representative devices/networks and cold/warm cache.

For a page with required components $R$ and optional components $O$, useful-core time is governed by the slowest required completion, not by waiting for all optional cards. A single global spinner turns optional latency into total outage.

Lazy-load routes and heavy visualizations; prefetch only with privacy/cost bounds. Avoid downloading every plugin to render navigation. Server-side aggregation can reduce round trips but may create a shared bottleneck; use owned read models and bounded concurrency.

Track dependency fan-out. Adding “one card” can add several API, token, DNS, and provider dependencies. Architecture review should include its synchronous cut and degraded behavior.

Performance is accessibility and reliability. Long main-thread work, layout shifts, timeouts, and moving content impair keyboard and assistive-technology use as well as user trust.

### Build accessibility into primitives and journeys

Adopt an explicit WCAG target and test supported browsers/assistive technologies. Use semantic HTML, correct headings/landmarks, labels and instructions, keyboard navigation, visible focus, sufficient contrast, text resizing/reflow, error identification, status announcements, and reduced motion.

Shared design-system primitives reduce repeated defects, but custom plugins must still test actual composition. A visually polished custom dropdown can fail keyboard, name/role/value, zoom, or screen-reader semantics.

For multi-step forms, preserve values, identify errors in text, focus the summary or first error predictably, state required/optional fields, explain consequences before submission, and allow review/correction. Do not rely on color alone.

For asynchronous tasks, expose stable textual states and use restrained live regions for meaningful updates; streaming every log line overwhelms assistive technology. Provide pause, filter, copy, and downloadable accessible records.

Test keyboard-only, screen readers, 200–400% zoom/reflow, high contrast, reduced motion, slow network, localization expansion, and cognitive comprehension with users. Automated scanners find only part of the problem.

### Design responsive and localized information architecture

Prioritize content rather than shrinking desktop dashboards. On narrow screens, essential identity/status/actions precede secondary cards; tables need responsive alternatives; focus/order must follow meaningful reading order.

Externalize strings, dates, numbers, currency, time zones, pluralization, and relative time. Avoid concatenated fragments that cannot translate. Domain identifiers may remain invariant, while labels and explanations localize.

Show absolute timestamp/time zone for consequential events; relative “five minutes ago” alone becomes ambiguous in audit and screenshots. Handle right-to-left layout if in scope.

URLs and deep links should preserve durable entity/task identities and avoid sensitive inputs. Browser history/back navigation through multi-step forms must not resubmit effects.

Information architecture follows user vocabulary and ownership, not backend product names. Search synonyms and aliases can bridge language without making taxonomy arbitrary.

### Protect browser and content boundaries

Use content security policy, secure dependency delivery, output encoding, trusted Markdown/HTML sanitization, CSRF defenses, careful CORS, clickjacking protection, and secure session cookies according to deployment threat model. Browser extensions and same-origin plugins remain risks.

Catalog annotations, documentation, task logs, provider errors, repository content, and plugin metadata are untrusted display input. Escape by context and restrict active content. A trusted employee is not automatically trusted to preserve confidentiality/integrity for every tenant.

Proxy allowlists include scheme, host, path, method, headers, redirects, and response limits. Block server-side request forgery into metadata/internal endpoints. Never forward user-controlled authorization headers blindly.

Uploads need type/size/content validation, malware policy, isolated storage, and safe rendering. Exported CSV/office content can carry formula or active-content risks.

Threat-model denial of service. Portals often need upstream edge protection, request limits, queue bounds, and plugin isolation beyond application authorization.

### Observe journeys without surveilling users

Measure discovery success, search refinement/no-result rate, form validation failures, abandonment, active effort, accepted task rate, time to domain-ready outcome, retries/cancellations, support escalation, stale data, permission denials, accessibility errors, and satisfaction.

Segment carefully by journey, plugin, interface, cohort, and environment without exposing personal or sensitive behavior. Define purpose, minimization, retention, access, and consent/notice according to policy.

Technical telemetry includes shell/plugin errors, bundle size, web vitals, backend latency, dependency errors, cache age, task queue/step status, auth failures, and audit. Correlate through safe IDs, not secret-bearing URLs or full form values.

Page views and template launches do not prove value. Completion of a usable domain capability, lower support burden, safer decisions, and user success do.

Preserve audit separately from analytics. Users may opt out of product analytics while security-relevant privileged actions still require governed audit.

### Operate degraded modes and incidents

Define named modes: shell unavailable; identity unavailable; catalog/search stale; read-only portal; self-service submission blocked; accepted tasks progressing; one capability/plugin unavailable; third-party outage; and security shutdown.

Do not couple worker execution to portal sessions or frontend availability. Workers use durable tasks and service identity. If event streaming fails, users can poll task status later without restarting it.

Provide a status route outside the failing shell where practical and document direct API/CLI/Git alternatives. Avoid emergency banners that depend on the same broken catalog or plugin.

Disable compromised plugins/actions centrally, revoke their credentials, preserve task/effect evidence, and identify affected users/resources. Feature flags are operational controls only if protected, audited, and enforced backend-side where consequence matters.

After recovery, reconcile tasks, provider effects, catalog/read models, and audit. Do not declare success because the homepage loads.

### Upgrade, recover, and retire safely

Version shell extension interfaces, plugin APIs/config/data migrations, permission names/rules, identity mappings, templates/actions, task checkpoint schemas, catalog entity schemas/processors, search indexes, and design-system behavior.

Roll compatible readers before writers, run plugin database migrations under ownership, canary privileged actions, and test mixed frontend/backend versions. Cached browser bundles can outlive deployment; APIs must tolerate them or force safe refresh.

Back up non-derivable portal/task/catalog data, configuration, identity/permission mappings, template/action revisions, audit references, and encryption keys. Rebuild derived search/cache, then compare in-flight tasks with external effects before workers resume.

Retire a plugin by stopping new uses, inventorying routes/callers/tasks/data/credentials/permissions/dependencies, migrating or exporting state, draining work, revoking access, measuring zero use, and removing frontend/backend/config/database/recovery artifacts.

Portal replacement should not require domain-resource migration if boundaries were sound. Preserve deep-link redirects and user guidance while canonical APIs continue.

## Definitions and Notation

Let $J$ be portal journeys and $K_j$ the steps in journey $j$. For step $k$, $p_{jk}\in[0,1]$ is observed conditional success and $e_{jk}\geq0$ active user effort. The diagnostic independent-step model is

$$P_j=\prod_{k\in K_j}p_{jk}, \qquad E_j=\sum_{k\in K_j}e_{jk}.$$

Actual journey completion must be measured because branches, retries, selection bias, abandonment, and correlated failures violate the product approximation.

For page $v$, let $R_v$ be required components, $O_v$ optional components, and $T_i$ usable render time. Core usable time under parallel loading is approximately

$$T_{core}(v)=\max_{i\in R_v}T_i,$$

provided the shell does not wait on $O_v$. Backend/network concurrency and main-thread contention can violate this idealization.

Let task identity be $\tau$, client operation ID $o$, requester/tenant $a$, template revision $r_t$, action set/revisions $r_A$, policy revision $r_p$, step checkpoint $c_s$, and external effect identity $e_s$. Correlating these distinguishes browser request, logical task, authorized definition, progress, and provider effect.

For a read-model fact $f$, record authoritative source $S_f$, source revision $r_f$, observed time $t_f$, and allowed staleness $\Delta_f$. Display may use last known state with labeling; consequential actions apply the stricter domain rule.

## Mechanisms, Invariants, or Proof Structure

### Portal architecture protocol

1. Research full lifecycle journeys, personas, vocabulary, accessibility needs, and alternative interfaces.
2. Assign every fact/action an authority, permission, owner, freshness, and consequence.
3. Keep shell narrow; define plugin/extension and BFF/domain boundaries.
4. Threat-model sign-in resolution, sessions, delegated tokens, proxies, plugins, templates, actions, secrets, and display content.
5. Persist resource/task identity and authorization evidence before effects; make refresh/retry idempotent.
6. Build catalog/search/cards as bounded, freshness-labeled, rebuildable read models.
7. Enforce local error boundaries, timeouts, bulkheads, performance budgets, and degraded modes.
8. Verify WCAG target, responsive/localized journeys, user comprehension, privacy, and support.
9. Version/canary components and privileged actions; test mixed versions, failure, restore, and alternate paths.
10. Measure outcome and retire plugins/templates/capabilities through complete lifecycle evidence.

### Projection invariant

The portal may guide, preview, and render, but canonical APIs/backends enforce the same schema, defaults, policy, authorization, idempotency, and status used by non-portal clients. No hidden UI behavior is necessary for safety.

### Least-authority invariant

Frontend and backend plugins receive only the identities, data, routes, credentials, and actions required for their trust tier. A compromised optional plugin cannot automatically administer every integrated system.

### Durable-task invariant

Once accepted, $\tau,o,a,r_t,r_A,r_p$ and enough checkpoint/effect identity survive portal/worker failure. Duplicate submission or event cannot create a second logical effect without explicit new intent.

### Freshness invariant

Every derived fact used in presentation identifies source and time/revision. A destructive, ownership, security, or adoption decision revalidates against its authoritative source and current permission.

### Failure-containment invariant

Optional plugin/backend/search/analytics failure is handled within its card/route/resource budget. It cannot prevent shell/core content, unrelated capability action, accepted task progress, or direct API access unless the documented dependency truly is essential.

### Journey-product argument

If a journey has required independent steps with success below one, adding an avoidable required step cannot increase $P_j$ because multiplication by $p\leq1$ does not increase the product; it also adds nonnegative effort. Therefore remove avoidable steps, but retain steps that convey or authorize consequential decisions. This is a scoped proof sketch, not evidence of actual independence or user behavior.

### Executable portal inventory

The following synthetic classifier assigns ten portal components to core, optional, or privileged paths from their declared criticality and effect authority. It checks the example data only; it does not test a real portal, permission policy, accessibility, security, or performance.

<!-- bijux-verify: {"id":"developer-portal-component-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"core=3\noptional=4\nprivileged=3\n"}} -->
```python
components = [
    ("shell-navigation", True, False),
    ("identity-session", True, False),
    ("domain-status", True, False),
    ("cost-card", False, False),
    ("build-history", False, False),
    ("docs-recommendations", False, False),
    ("team-news", False, False),
    ("environment-create", True, True),
    ("credential-rotate", True, True),
    ("data-delete", True, True),
]

counts = {"core": 0, "optional": 0, "privileged": 0}
for _, required, effect in components:
    category = "privileged" if effect else "core" if required else "optional"
    counts[category] += 1

for category in ("core", "optional", "privileged"):
    print(f"{category}={counts[category]}")
```

Privileged actions remain required for their own journey but are separated because they need stronger authorization, audit, confirmation, and recovery. “Optional” means the page can remain useful without the card, not that its data quality is irrelevant.

### Verification matrix

Test unauthenticated, disabled, renamed, duplicated, contractor, service, and multi-provider identities; permissions on UI/backend/task/step/output/log/effect; malicious catalog/template/plugin content; CSRF/XSS/SSRF/redirect/token leakage; secret redaction; duplicate submission/retry/cancel; worker/browser crash; provider ambiguity; catalog/search lag; plugin timeout/crash/large payload; tenant overload; accessibility and localization; cached old frontend with new backend; feature disable; backup restore; external-ahead tasks/effects; and plugin/capability retirement.

## Alternatives and Trade-Offs

### Buy/adopt a portal framework versus build a focused portal

A framework supplies catalog, plugin, template, and design machinery but brings upgrade and trust-surface cost. A focused portal can match a few journeys tightly but must build identity, extensibility, governance, and accessibility. Choose from owned outcomes, not fashion.

### Monolithic frontend versus plugin architecture

A monolith simplifies consistent releases and shared state but grows coupling. Plugins enable ownership and replacement but add contracts, dependency/version governance, and limited browser isolation. Keep the shell stable and extension surfaces narrow.

### Browser-direct integration versus BFF

Direct calls reduce backend code and preserve user delegation but expose tokens, CORS, provider variance, and client complexity. BFFs protect credentials and normalize data but can centralize privilege. Scope them per capability.

### Live fan-out versus materialized read model

Live data can be fresher but makes page latency/availability depend on many systems. Read models are fast and resilient but stale. Label freshness and reread authority for consequence.

### Schema-generated form versus custom journey

Generated forms stay aligned and cover fields cheaply but may be cognitively poor. Custom forms guide decisions but can drift. Use shared schema/admission and custom presentation only where research justifies it.

### Template action versus declarative resource

Templates suit scaffolding and finite tasks; declarative resources maintain ongoing state and drift. A template may create a resource, but should not impersonate its controller.

### User-delegated token versus service identity

Delegation preserves user authority and provider audit but can be broad/long-lived or unavailable for workers. Scoped service identity supports automation but risks confused deputy. Bind task/user/policy context and minimize scope.

### Central permission policy versus domain policy services

Central policy gives consistency and one control point but can become bottleneck and lowest common denominator. Domain policy preserves semantics but needs shared identity/audit. Centralize framework and common rules while keeping enforcement with resource owners.

### One backend deployment versus isolated privileged plugins

One process is operationally simple but shares credentials and blast radius. Isolation costs more but protects high-risk actions/providers. Deploy according to trust tier and failure evidence.

### Streaming logs versus curated status

Raw logs aid experts but leak secrets, overwhelm users/assistive tech, and expose implementation. Domain status is stable but less detailed. Provide curated state first and permissioned redacted diagnostics.

### Automatic task cleanup versus long retention

Short retention reduces privacy/cost risk but weakens diagnosis/audit. Long retention supports evidence but accumulates sensitive data. Split audit, task metadata, verbose logs, and artifacts by purpose.

### Portal-only self-service versus multiple interfaces

Portal-only delivery is guided but blocks automation and creates a single outage/control path. Multiple interfaces cost documentation/testing but preserve canonical contract and resilience.

## Failure Modes and Misconceptions

1. **“The portal is the platform.”** It is an experience over capabilities and authorities.
2. **“One screen should show everything.”** Unbounded fan-out and cognitive load make it slow and misleading.
3. **“Hidden buttons enforce authorization.”** Direct backend calls bypass presentation.
4. **“Authenticated employees are trusted.”** They may not be authorized for other teams’ confidential/integrity boundaries.
5. **“Email matching is identity.”** Mutable or nonunique attributes can link the wrong account.
6. **“A proxy makes browser calls safe.”** Broad tokens, arbitrary destinations, redirects, and SSRF remain.
7. **“Plugins are just UI.”** They execute code, access shared origin/clients, and may install privileged backends.
8. **“Marketplace availability means approved.”** Provenance, permissions, dependencies, data, and operations need review.
9. **“Template visibility grants action permission.”** Steps, targets, outputs, and effects require enforcement.
10. **“Dry run proves safety.”** It does not reproduce real credentials, races, provider failures, or cleanup.
11. **“Retry means run again.”** Completed effects may duplicate without checkpoints and identity.
12. **“Cancel means rollback.”** External effects may be irreversible or already committed.
13. **“Redaction makes secrets safe in logs.”** Prevention and scoped brokerage are primary.
14. **“Catalog absence means resource absence.”** Ingestion, processing, authorization, and staleness can hide it.
15. **“Search can drive policy.”** Ranking/index lag is not authoritative evidence.
16. **“A page is healthy if the shell loads.”** core data/actions or accepted work may be broken.
17. **“Accessibility can be audited at the end.”** Interaction architecture and primitives determine it early.
18. **“Feature flags are security controls.”** Frontend-only flags are bypassable and may be unaudited.
19. **“Page views measure platform value.”** usable lifecycle outcomes and reduced effort/risk matter.
20. **“Uninstalling a plugin retires it.”** tasks, data, credentials, permissions, callers, and backups remain.

## Worked Examples

### Example 1

**Situation.** A production form defaults a recovery tier only in React code.

**Reasoning.** Direct API/Git users receive another outcome. Move the default to canonical schema/policy, render the resolved value, and test all interfaces.

**Conclusion.** A form cannot own domain semantics.

### Example 2

**Situation.** The portal hides “Delete data” from nonowners, but its backend endpoint checks only sign-in.

**Reasoning.** Enforce current ownership, tenant, policy, object revision, and step-up approval at backend/effect; audit denial and action.

**Conclusion.** UI permission is guidance, not enforcement.

### Example 3

**Situation.** Two identity resolvers map a contractor email to different internal users.

**Reasoning.** Disable ambiguous resolution, use stable verified issuer/subject mapping, reconcile accounts explicitly, invalidate sessions, and audit prior actions.

**Conclusion.** Account linking is a privileged identity design.

### Example 4

**Situation.** A service page waits serially for cost, CI, incidents, Kubernetes, and recommendations.

**Reasoning.** Render shell/core identity immediately, load bounded cards concurrently, use read models and local errors, and exclude optional cards from core readiness.

**Conclusion.** Page composition must preserve failure isolation.

### Example 5

**Situation.** A repository-creation action times out after the provider created the repository.

**Reasoning.** The worker checkpoints task/client operation identity, queries provider by stable intended identity, adopts the match, and does not blindly replay.

**Conclusion.** Portal tasks need control-plane idempotency.

### Example 6

**Situation.** A user cancels after an account and billing link exist but before policy bootstrap.

**Reasoning.** Mark cancel requested, stop safe future steps, run authorized compensation or quarantine, report residual owner/cost, and record terminal disposition.

**Conclusion.** Cancellation is a state machine, not process termination.

### Example 7

**Situation.** A malicious catalog description contains active HTML and credential-looking links.

**Reasoning.** Treat descriptors as untrusted, sanitize/render safely, constrain links, block active content, and review ingestion authority. Catalog ownership does not grant script execution.

**Conclusion.** Internal metadata crosses a content trust boundary.

### Example 8

**Situation.** Streaming task logs announces hundreds of updates to a screen reader.

**Reasoning.** Publish stable stage/progress through restrained live regions, provide paused/filterable logs, focus errors intentionally, and test real assistive technology.

**Conclusion.** Operational visibility needs accessible information pacing.

### Example 9

**Situation.** After restore, task storage says “creating” while the provider account and repository already exist.

**Reasoning.** Fence old workers, inventory by task/effect identity, adopt verified effects, repair checkpoints, rotate temporary credentials, then rebuild search/read models.

**Conclusion.** Portal recovery reconciles durable tasks with external-ahead reality.

### Example 10

**Situation.** A security advisory requires disabling a privileged cloud plugin.

**Reasoning.** Remove route/action server-side, revoke credentials, preserve and classify tasks/effects, provide direct safe alternatives, patch/canary, and audit exposure.

**Conclusion.** Plugin governance includes emergency isolation and effect recovery.

## Cross-Program Connections

1. **Human-Computer Interaction:** journey research, cognitive load, progressive disclosure, error recovery, and accessibility shape the product.
2. **Web Engineering:** shells, routing, browser security, performance, responsive design, localization, and frontend isolation shape delivery.
3. **Security Engineering:** identity mapping, sessions, authorization, delegation, SSRF/XSS/CSRF, secrets, supply chain, and audit define trust.
4. **API & Service Engineering:** canonical contracts, BFFs, idempotency, asynchronous tasks, errors, versions, and quotas preserve semantics.
5. **Distributed Systems:** partial failure, retries, checkpoints, stale read models, events, and external-ahead recovery govern behavior.
6. **Database Systems:** task persistence, read models, source revisions, migrations, retention, backup, and reconciliation govern state.
7. **Reliability Engineering:** performance budgets, error boundaries, SLOs, bulkheads, degraded modes, and incident recovery bound failure.
8. **Software Supply Chain:** plugin/template/action provenance, dependencies, signing, scanning, pinning, and rollback govern extensions.
9. **Product Management:** personas, journeys, adoption, funnel evidence, support burden, and satisfaction measure value.
10. **Organizational Design:** owners, capability teams, template authors, operators, security reviewers, and support escalation determine stewardship.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://github.com/cncf/tag-app-delivery/blob/main/platforms-whitepaper/latest/index.md). Retrieved 2026-09-02.
2. Backstage. [Architecture Overview](https://backstage.io/docs/overview/architecture-overview/). Retrieved 2026-09-02.
3. Backstage. [Frontend Plugins](https://backstage.io/docs/frontend-system/architecture/plugins/). Retrieved 2026-09-02.
4. Backstage. [Backend Plugins](https://backstage.io/docs/backend-system/architecture/plugins/). Retrieved 2026-09-02.
5. Backstage. [Permission Framework Overview](https://backstage.io/docs/permissions/overview/). Retrieved 2026-09-02.
6. Backstage. [Permission Concepts](https://backstage.io/docs/permissions/concepts/). Retrieved 2026-09-02.
7. Backstage. [Sign-in Identities and Resolvers](https://backstage.io/docs/auth/identity-resolver/). Retrieved 2026-09-02.
8. Backstage. [Threat Model](https://backstage.io/docs/next/overview/threat-model/). Retrieved 2026-09-02.
9. Backstage. [Software Templates](https://backstage.io/docs/features/software-templates/). Retrieved 2026-09-02.
10. Backstage. [Authorizing Scaffolder Tasks, Parameters, Steps, and Actions](https://backstage.io/docs/features/software-templates/authorizing-scaffolder-template-details/). Retrieved 2026-09-02.
11. Backstage. [Software Catalog](https://backstage.io/docs/features/software-catalog/). Retrieved 2026-09-02.
12. Backstage. [The Life of an Entity](https://backstage.io/docs/features/software-catalog/life-of-an-entity/). Retrieved 2026-09-02.
13. Backstage. [System Model](https://backstage.io/docs/features/software-catalog/system-model/). Retrieved 2026-09-02.
14. W3C. [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/). W3C Recommendation, 2023.

## Exercises

### Exercise 1

Architect a portal for service discovery, documentation, deployment status, and production-environment creation. Define shell/plugin/BFF/domain boundaries, sources of truth, performance and degraded behavior.

### Exercise 2

Threat-model identity mapping, delegated tokens, plugin installation, template ingestion, action execution, proxying, task logs, and secret handling for a multi-tenant portal.

### Exercise 3

Design the durable task state machine for creating a repository, cloud account, policy baseline, and catalog entity under timeout, retry, cancellation, and partial compensation.

### Exercise 4

Define an accessibility, responsive, localization, and performance verification plan for catalog search, a multi-step form, and live task progress.

### Exercise 5

Plan recovery from a portal database snapshot while tasks/effects may be newer, then plan emergency disablement and final retirement of a privileged plugin without stopping canonical APIs.

## Answers to the Exercises

### Answer 1

Use a narrow shell for sign-in/session integration, navigation, routes, layout, design/accessibility primitives, localization, and local error boundaries. Catalog, docs, CI/deployment, and environment plugins use published extension APIs. Capability-aligned BFFs exchange scoped credentials and adapt responses; they do not own `Environment` semantics. The canonical environment API/task backend validates, authorizes, persists intent/progress, and remains callable by CLI/Git.

Declare sources: repository metadata for code-owned descriptors, organization directory for current teams, domain APIs for environment status, CI/deployment systems for their observations, and task store for execution. Catalog/search are derived with source revision/time; consequential actions reread authority.

Render name/owner/core status first. Load docs/deployment/cost cards concurrently with deadlines and independent unauthorized/stale/error states. Environment creation remains available if recommendations fail; existing task progress continues if the portal fails. Set budgets for shell/bundles/core p95, response size, calls, and backend concurrency. Provide direct API/CLI plus an external status route for incident use.

### Answer 2

Assets are subject identity, group/tenant mapping, sessions, delegated/provider credentials, catalog/private metadata, templates/actions, task input/logs/output, source/cloud effects, and audit. Threats include ambiguous resolver/account linking, disabled-user session, token theft, CSRF/XSS, SSRF/open proxy, plugin dependency compromise, malicious template/action, cross-tenant enumeration, secret logging, arbitrary filesystem/network, replay, and operator abuse.

Use stable issuer/subject sign-in mappings, one intentional resolver per provider, short secure sessions, revocation and step-up. Keep delegated tokens scoped/short-lived in backends. Enforce permissions at backend, task, step, target, log/output, cancel/retry, and effect; frontend checks only guide. Restrict template sources/authors and pin revisions. Register actions with schemas, network/filesystem/credential scopes, idempotency, timeout, audit, and owner. Allowlist proxy scheme/host/path/method/header/redirect and block metadata networks.

Broker secrets just in time, reference rather than persist values, redact defense-in-depth, split credentials by action/provider/tenant, and test exceptions/analytics/backups. Review plugin provenance, permissions, data, dependencies, CSP, isolation, upgrades, disablement, and retirement. Audit principal, policy, task, template/action revision, operation/effect, and outcome.

### Answer 3

States include `Accepted`, `Planning`, `Repository`, `Account`, `Policy`, `Catalog`, `Validating`, and terminal `Succeeded`, `Failed`, `Cancelled`, or `NeedsIntervention`, with `CancelRequested` orthogonal where useful. Persist task/client operation ID, requester/tenant, input digest/protected references, policy/template/action revisions, step checkpoint, attempt, external operation/effect identity, outputs, residual effects, and audit.

Each step observes before acting, uses an idempotency key, checkpoints accepted provider identity, and translates ambiguity. Repository timeout queries intended owner/name/request marker. Account creation uses provider operation ID/tags. Policy and catalog upsert by stable identities. Duplicate events reread checkpoints. Retry resumes one safe step or creates a linked new task; it never blindly starts over.

Cancellation prevents later steps and requests cancellation where supported. If repository/account exist, compensation follows explicit policy: delete if newly created and safe, transfer/quarantine when deletion is unsafe, revoke temporary credentials, report ongoing cost/owner, and require approval for destructive cleanup. Success validates all domain outcomes, not only action return codes.

### Answer 4

Set a WCAG 2.2 conformance target and supported browser/assistive-technology matrix. Search needs labeled input, meaningful result counts, keyboard navigation without focus traps, authorized/no-result/error distinction, and accessible pagination. The form needs semantic groups, labels/instructions, required markers, text error summary with focus, retained values, review/correction, consequence explanation, and no color-only cues. Task progress uses stable headings/stages, restrained live announcements, pause/filter for logs, and terminal focus/summary.

Test keyboard-only, multiple screen readers, 200–400% zoom/reflow, contrast/high-contrast, reduced motion, touch target, slow network, errors, and cognitive comprehension with users. Localize strings, pluralization, dates/numbers/currency/time zones; test expansion and right-to-left if supported. On narrow screens keep core identity/status/action order meaningful and replace wide tables.

Budget shell and route bundle, core render p95/p99, main-thread work, layout shift, card deadlines, response size, and API fan-out. Use real device/network tests and production monitoring. An automated accessibility scan, Lighthouse score, or fast shell alone is insufficient; complete representative journeys with assistive technologies and degraded dependencies.

### Answer 5

First fence old workers and privileged credentials. Restore trusted identity/configuration, plugin schemas/migrations, task data, permission/template/action revisions, keys, and audit references. Inventory source/cloud effects by task/client operation/object/provider identity. For each restored in-flight task classify matched-complete, matched-partial, desired-ahead, external-ahead, collision, or unknown. Adopt verified effects and repair checkpoints; quarantine ambiguity. Only then resume bounded workers. Reingest/rebuild catalog/search and verify task outputs, permissions, secret revocation, cost ownership, and stale-worker denial.

For emergency disablement, remove routes and action registration backend-side, deny new tasks, revoke plugin credentials, preserve logs/audit and package/version inventory, classify running tasks/effects, and publish canonical API/CLI alternatives. Patch and canary only after threat and compatibility review.

For final retirement, announce successor, stop new use, inventory routes/callers/templates/tasks/data/databases/permissions/credentials/dependencies/backups, migrate or export state, drain/compensate work, revoke access, remove catalog links, and measure zero calls/tasks over the agreed window. Remove frontend, backend, config, data, recovery decoders, and redirects in dependency order while domain APIs/controllers continue. Test restore without the retired component before deleting last recovery material.
