---
module_id: PLAT-014
program: Platform Engineering
level: 1
module_number: 14
title: Web Portals
status: complete
last_verified: 2026-09-02
---

# Web Portals

## One-Page Review

### Governing question

How can a platform team design and operate a web portal that helps diverse consumers complete consequential journeys through consistent platform contracts without becoming a second source of truth, an inaccessible façade, or an insecure collection of plugins?

### Essential definitions

- A **developer portal** is a web channel that composes discovery, documentation, catalog, self-service operations, status, evidence, and support around platform journeys.
- A **portal shell** supplies cross-cutting navigation, identity, authorization context, design system, routing, search, telemetry, and extension boundaries.
- A **portal plugin** is a bounded feature contribution with declared routes, data contracts, permissions, dependencies, ownership, lifecycle, and failure isolation.
- A **resource page** presents a stable platform entity and its related actions, evidence, dependencies, ownership, and lifecycle.
- An **operation view** presents the durable state, evidence, progress, errors, recovery, and correlation for an asynchronous platform operation.
- **Progressive enhancement** begins with meaningful semantic content and supported actions, then adds richer client behavior without making essential work depend on fragile enhancement.
- **Accessible completion** means the entire supported task can be perceived, operated, understood, and completed with required assistive technologies and input methods.
- **ambient authority** is authority inferred from a session or mutable context rather than made explicit at the moment and scope of an action.

### Central model, mechanism, or theorem

Model portal experience $P=(J,C,S,O,E,A,G)$ as journey contract $J$, capability and resource model $C$, presentation state $S$, durable operation state $O$, evidence $E$, authorization context $A$, and guardrails $G$. The portal may cache, aggregate, and render authoritative state, but it must preserve provenance, freshness, uncertainty, operation identity, and ownership. Interface polish cannot repair a broken underlying capability contract.

### Critical invariants

- Portal, CLI, API, events, and support expose the same resource, operation, permission, and outcome semantics.
- The browser is never the sole source of durable operation truth.
- Every state-changing action binds authenticated principal, exact target, environment, request identity, authorization decision, and anti-forgery control.
- Accessibility is validated across discovery, input, error, confirmation, waiting, recovery, and completion—not inferred from a component library.
- Loading, empty, stale, partial, denied, failed, unknown, and degraded states are explicit and actionable.
- URLs identify meaningful authorized views; refresh, back, deep link, and concurrent-tab behavior do not corrupt work.
- Plugins cannot silently broaden permissions, capture secrets, or collapse the portal when a dependency fails.
- Analytics measure product journeys with data minimization and never become individual developer surveillance.

### Common failures

Building a dashboard instead of a journey; duplicating provider truth in portal storage; showing a spinner without operation identity; displaying green from stale data; authorizing only in the browser; using generic cards as information architecture; requiring pointer gestures; losing form work on reauthentication; hiding denials as missing resources; letting one plugin break global navigation; confirming deletion without scope; and measuring clicks while ignoring task completion, abandonment, recovery, accessibility, and operator burden.

### Compact example

A service page shows canonical owner, environment, artifact, dependencies, current application and platform evidence, freshness timestamps, and authorized actions. “Deploy” opens a task-specific flow, validates progressively, previews the exact revision and environment, and submits with an idempotency key. The page transitions from accepted to running using a durable operation ID, survives refresh, exposes logs and policy evidence, announces status accessibly, and ends only after the workload verification contract passes. A provider outage produces stale and degraded states with safe continuation rather than a frozen spinner or false success.

### Connections

Retrieve jobs and segments from [PLAT-002](002-platform-consumers-and-jobs-to-be-done.md), self-service operations from [PLAT-005](005-self-service-and-guardrails.md), capability/provider separation from [PLAT-007](007-platform-capabilities-versus-tool-catalogs.md) and [PLAT-008](008-internal-platforms-and-external-cloud-services.md), team authority from [PLAT-009](009-platform-team-boundaries.md), journeys from [PLAT-011](011-developer-journeys.md), deployment evidence from [PLAT-012](012-time-to-first-successful-deployment.md), and cross-channel contracts from [PLAT-013](013-command-line-interfaces.md).

## Governing Question

What must a portal reveal, preserve, and constrain so that a person can discover, understand, initiate, observe, recover, and complete platform work safely through a browser?

A portal is attractive because it can integrate fragmented experiences. It can also concentrate inconsistency, privilege, stale state, plugin risk, and inaccessible interaction. The design unit is not the page or card. It is the complete journey across browser, platform services, providers, teams, and later lifecycle work.

The portal succeeds when it makes platform contracts more understandable and usable while retaining authoritative boundaries. It fails when it becomes an ornamental homepage, a second database of questionable truth, or a privileged bypass around the same APIs other consumers must use.

## Why This Matters

Web portals can reduce discovery cost, join documentation with owned resources, and provide strong feedback for occasional or complex tasks. They are especially useful when a journey requires comparison, preview, rich evidence, progressive disclosure, or collaboration. They also provide a shared place to expose service ownership, lifecycle state, support, and platform status.

Current DORA platform guidance emphasizes critical user journeys, an internal-product mindset, independent work, and clear task-outcome feedback. These are product requirements, not instructions to build a universal portal. A good browser channel should make a chosen journey demonstrably better and coexist with automation rather than become mandatory for every lifecycle action.

Current Backstage architecture illustrates a composable portal shell, frontend and backend plugins, catalog, templates, documentation, search, and entity-oriented extensions. Its catalog documentation also distinguishes visualized metadata from source files stored with code. The general lesson is durable: composition and aggregation do not transfer source-of-truth ownership to the screen.

The browser creates its own threat model. Sessions, cookies, cross-site requests, untrusted plugin content, navigation, cached documents, third-party dependencies, and client-side state all cross trust boundaries. OWASP ASVS and current session/CSRF guidance provide verification requirements and defenses, but controls must be selected for the actual authentication and deployment architecture.

Accessibility is not a polish pass. WCAG 2.2 is a W3C Recommendation and defines perceivable, operable, understandable, and robust requirements, including keyboard access, focus, status messages, input assistance, accessible authentication, and complete-process conformance. Conformance still does not address every user need, so research with disabled consumers remains necessary.

## Prerequisites and Retrieval

Retrieve platform boundaries, consumers, cognitive load, product lifecycle, self-service operations, build-or-buy routes, capability contracts, provider boundaries, team interfaces, value hypotheses, journey blueprints, deployment measurement, and CLI channel semantics from PLAT-001 through PLAT-013.

You should understand HTTP, browser navigation, cookies and sessions, cross-site request forgery, content security, authentication and authorization, APIs, asynchronous operations, caching, design systems, semantic HTML, accessibility, responsive design, user research, progressive delivery, observability, privacy, plugins, and incident response.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a portal product from a dashboard, link directory, catalog, and source-of-truth system;
2. derive information architecture and navigation from developer journeys, resources, and tasks;
3. model loading, stale, partial, operation, error, recovery, and completion states with authoritative evidence;
4. design accessible forms, navigation, feedback, authentication, and consequential actions across complete processes;
5. define secure session, authorization, anti-forgery, secret, and plugin boundaries;
6. compose plugins without fragmenting semantics, ownership, performance, or reliability;
7. preserve deep links, refresh, concurrency, idempotency, and cross-channel continuity; and
8. evaluate portal value using task outcomes, qualitative research, accessibility evidence, reliability, security, and operator burden.

## Core Exposition

### Choose the portal's product boundary

Begin with prioritized journeys and consumers. Decide which work benefits from a browser: discovering a capability, comparing profiles, viewing dependencies, declaring structured intent, previewing a consequential change, observing a long operation, diagnosing failure, or coordinating ownership. Do not add a page merely because a backend exists.

State what the portal owns. It may own navigation, presentation, browser session, user preferences, saved drafts, operation correlation, and aggregation. Capability services own resource and operation truth. Source repositories may own declarative metadata. Providers own their bounded state. Domain teams own application acceptance. Display provenance instead of absorbing all ownership into “the portal.”

Define non-goals and escape routes. Expert automation may use APIs or CLI. Specialist provider access may remain necessary. An outage-safe read-only path or direct status page may exist. Avoid mandatory browser clicks in an otherwise automated production flow unless a genuine human decision requires them.

### Organize around journeys and resources

Information architecture should answer: What do I own? What needs attention? What can I do? What is happening? What failed? Who owns this? Where is the evidence? Group by stable domain concepts and user jobs, not platform-team org charts or plugin names.

Entity pages can form a useful spine when services, environments, pipelines, data products, identities, and operations have stable references. Each page should expose canonical identity, ownership, lifecycle, relationships, current evidence, freshness, actions, support, and history appropriate to authorization.

Global search, browse, recent work, favorites, notifications, and task entry points are complementary. Personalization may reduce repeated navigation but must not hide globally important status or produce a different authorization reality. Provide more than one way to locate essential content, consistent with current accessibility guidance.

### Treat the portal as a projection

Model the experience as

$$
P=(J,C,S,O,E,A,G),
$$

where $J$ is journey contract, $C$ capability/resource model, $S$ presentation state, $O$ durable operation state, $E$ evidence and provenance, $A$ authenticated and authorized context, and $G$ accessibility, safety, privacy, and reliability guardrails.

The portal projects these inputs into views and actions. It can cache for performance, but cached state needs observed time, source time, age, refresh behavior, and safe consequences. “Healthy” without freshness or scope is not an operational fact.

Use backend aggregation when it protects credentials, enforces policy, reduces fragile browser fan-out, or composes provider responses. Do not create an unowned “backend for frontend” that silently changes domain semantics. Its contracts, objectives, authorization, and failure behavior need owners.

### Model every meaningful interface state

For each view and task, design initial, loading, loaded, empty, stale, partially loaded, denied, not found, invalid, submitting, accepted, running, needs action, succeeded, failed, cancelled, timed out, and unknown states. Distinguish “you lack access” from “does not exist” according to the security policy without misleading authorized users.

Skeletons and spinners communicate activity, not progress or success. Long work needs durable operation identity, stage, evidence, latest observation, expected next transition, safe navigation away, notification option, cancellation semantics, and recovery. Refreshing the page should reconstruct state from the server.

The following synthetic operation projection checks state and action invariants. It validates a teaching model, not a production frontend.

<!-- bijux-verify: {"id":"portal-operation-projection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"operations=7\nterminal=3\nactionable=4\nstale=2\nunsafe_success=0\n","stderr":""}} -->
```python
operations = [
    {"id": "o1", "state": "accepted", "action": "observe", "age": 5, "verified": False},
    {"id": "o2", "state": "running", "action": "observe", "age": 75, "verified": False},
    {"id": "o3", "state": "needs_action", "action": "repair", "age": 20, "verified": False},
    {"id": "o4", "state": "succeeded", "action": "inspect", "age": 10, "verified": True},
    {"id": "o5", "state": "failed", "action": "retry", "age": 8, "verified": False},
    {"id": "o6", "state": "failed", "action": "support", "age": 30, "verified": False},
    {"id": "o7", "state": "unknown", "action": "reconcile", "age": 120, "verified": False},
]

terminal_states = {"succeeded", "failed", "cancelled"}
actionable_states = {"needs_action", "failed", "unknown"}
unsafe_success = sum(op["state"] == "succeeded" and not op["verified"] for op in operations)
print(f"operations={len(operations)}")
print(f"terminal={sum(op['state'] in terminal_states for op in operations)}")
print(f"actionable={sum(op['state'] in actionable_states for op in operations)}")
print(f"stale={sum(op['age'] > 60 for op in operations)}")
print(f"unsafe_success={unsafe_success}")
```

“Actionable” is a UI classification, not a claim that every failed operation is safely retryable. The displayed action must come from typed failure and capability semantics. In this cohort, both failures are actionable, but one offers retry and the other offers support. Production code should derive those distinct continuations from authoritative error classes, retained state, idempotency, and recovery policy rather than from the broad `failed` label alone.

### Design forms as conversations with a contract

Ask only for decisions the consumer owns. Derive known identity, ownership, policy, and provider values visibly. Use sensible profile defaults, but show consequential derived values and allow authorized correction. Progressive disclosure can reduce initial load without hiding cost, security, data, or irreversibility.

Use semantic controls, persistent labels, helpful descriptions, correct input purpose, grouped choices, and keyboard-operable widgets. Validate as early as useful without announcing every keystroke. On submission, focus and summarize errors, associate each error with its field, preserve valid input, and explain safe correction. Server validation remains authoritative.

Support save/resume for long work with explicit retention and privacy. Reauthentication should preserve entered data where safe, consistent with WCAG's concern for reauthenticating complete processes. A draft is not a submitted platform operation and should never be represented as one.

### Make consequential actions reviewable

Separate intent, preview, authorization, confirmation, submission, observation, and verification. A review page should name principal, exact resource, environment/account/region, changed fields, policy results, dependencies, cost, reversibility, and expected evidence. Bind submission to the reviewed version or detect drift.

Avoid confirmation modals that say only “Are you sure?” Explain what happens and what remains. Use strong confirmation for high-consequence deletion, revocation, or traffic shift, but do not rely on confirmation as authorization. Where possible, support undo, retention, rollback, cancellation, or staged rollout.

Prevent duplicate submission with a stable request identity and disabled/relabelled controls, while retaining recovery if the response is lost. Browser back, refresh, or a second tab must not create duplicate mutations. Preserve and expose authoritative operation state.

### Engineer accessibility across complete journeys

Set an explicit conformance target appropriate to policy and users, commonly WCAG 2.2 AA, and treat it as a floor. Use native HTML semantics before ARIA. The WAI-ARIA Authoring Practices Guide supplies patterns and keyboard guidance, but copying an ARIA role does not guarantee an accessible implementation.

Test landmarks, headings, page title, language, link purpose, focus order, focus visibility and obstruction, keyboard operation, target size, reflow, zoom, contrast, non-color cues, motion, timeouts, status messages, errors, authentication, and redundant entry. Status changes must be programmatically available without stealing focus.

Test the complete process with screen readers, keyboard-only use, magnification, high contrast, reduced motion, voice input, touch, and representative browsers. Combine automation, code review, manual evaluation, and research with disabled consumers. Plugin boundaries do not excuse a portal-wide conformance failure.

### Secure the browser boundary

Define session creation, binding, renewal, rotation, idle/absolute expiry, logout, revocation, and reauthentication. Use secure transport and appropriately scoped, `Secure`, `HttpOnly`, and `SameSite` cookies when cookies carry sessions. Avoid tokens in URLs, browser storage chosen by convenience, logs, analytics, or client-visible configuration.

Enforce authorization on every server-side operation and data access. Client-side hiding is presentation only. Protect state-changing requests against cross-site request forgery using framework-supported defenses appropriate to the architecture, such as synchronizer tokens or signed double-submit patterns plus origin and Fetch Metadata checks. SameSite is defense in depth, not a universal replacement.

Apply content security policy, safe output encoding, dependency governance, clickjacking defense, upload validation, and restrictive cross-origin configuration. Treat catalog descriptions, documentation, logs, provider messages, plugin content, and URLs as untrusted. Rich rendering needs sanitization at the correct context.

### Govern plugins as product and security boundaries

Each plugin declares owner, purpose, routes, extension points, APIs, data sensitivity, permissions, session needs, dependencies, performance budget, accessibility evidence, support, release compatibility, and retirement plan. Installing code is a supply-chain and runtime decision, not a visual customization.

The portal shell should provide consistent identity, authorization clients, design tokens, error boundaries, telemetry, navigation, and operation components. Plugins should use shared capability contracts rather than call providers with browser credentials. Feature discovery still requires an allowlist, provenance, version policy, and review.

Isolate failures. A broken cost widget should not remove the deployment action or global navigation. Set timeouts, lazy-load bounded features, degrade independently, and make ownership visible. Test plugin combinations; individually accessible components can create an inaccessible page through focus, landmarks, or duplicated labels.

### Preserve navigation and cross-channel continuity

Meaningful state belongs in stable URLs where safe: resource identity, operation ID, tab, filter, and pagination. Do not place secrets or sensitive content in URLs, which leak through history, logs, referrers, and screenshots. Apply authorization on every deep link.

Back and forward navigation should restore a comprehensible view. Refresh should reconstruct from durable state. Unsaved edits should be distinguished from submitted work. Concurrent edits require versions or preconditions and a reconciliation UI rather than last-write-wins surprise.

Return copyable CLI/API equivalents for tasks where useful, using the same canonical identifiers and context. An operation started by CLI should be observable in the portal, and a portal-created resource should be manageable through authorized APIs. Channel presentation can differ; semantics cannot.

### Design for performance and degraded operation

Define budgets for shell load, key journey interaction, API fan-out, and plugin contribution. Prioritize meaningful content and current operation state over decorative dashboards. Use caching, pagination, streaming, and lazy loading deliberately; measure real user experience without collecting sensitive developer behavior unnecessarily.

Distinguish portal availability from capability availability. During a provider outage, the portal may still show last-known state with freshness, accept only safely queueable intent, block unsafe mutation, link incident status, and support reconciliation. During portal outage, documented CLI/API paths and status communication may remain available.

Avoid a single page that fetches every provider synchronously. Backend composition can produce partial results with per-source state. A global error boundary that says “Something went wrong” discards valuable surviving evidence and ownership.

### Measure journeys, not page traffic

Measure eligible task attempts, completion, independent completion, elapsed and active time, abandonment, error, recovery, support, accessibility, satisfaction, trust, freshness, operation uncertainty, security events, and operator toil. Segment by journey and relevant context without creating individual rankings.

Page views, clicks, searches, and feature adoption help diagnose navigation but are not developer productivity or value. Minimize data, state purpose, restrict access, set retention, and consider non-users and blocked attempts. Backstage's optional visit tracking is a reminder that seemingly benign personalization still creates stored behavioral data requiring a decision.

Combine telemetry with observation, interviews, accessibility research, support themes, incidents, and plugin-owner evidence. Publish portal hypotheses and guardrails. Remove or redesign features that attract traffic but do not improve an owned outcome.

## Definitions and Notation

$P=(J,C,S,O,E,A,G)$ models portal experience through journey contract, capability/resource model, presentation state, durable operation state, evidence/provenance, authorization context, and guardrails.

For evidence item $e$, record source time $t_s(e)$, observation time $t_o(e)$, and presentation time $t_p$. Display age at presentation is $a(e)=t_p-t_s(e)$ when clocks and provenance support that calculation. Missing source time is unknown freshness, not age zero.

Let plugin set $Q$ contribute routes and views over shared contract $C$. Portal correctness is not componentwise: $\forall q\in Q$, local accessibility or availability of $q$ does not prove the composed journey is accessible or available. Composition requires end-to-end evaluation.

## Mechanisms, Invariants, or Proof Structure

Use a product loop: select critical journey; observe current work; define portal/non-portal boundary; establish canonical resources and operations; design information architecture; enumerate interface states; prototype complete paths including failure; evaluate accessibility and security; define plugin contracts; instrument minimally; release progressively; compare task and guardrail evidence; operate and retire.

The projection invariant prevents duplicate truth. The operation invariant survives navigation and client interruption. The authorization invariant validates every server action. The accessibility invariant covers complete processes. The freshness invariant prevents stale green status. The composition invariant prevents plugins from fragmenting semantics or global resilience.

Adversarial review includes expired session mid-form; cross-site state-changing request; reflected provider content; compromised plugin; stale cache; partial backend fan-out; slow screen reader announcement; keyboard trap; focus hidden by sticky navigation; repeated submission; back after deletion; two-tab update conflict; deep link without access; provider outage; portal outage; and analytics exposing sensitive resource names.

## Alternatives and Trade-Offs

**Central portal** offers consistent navigation and composition. It can become a bottleneck, concentrated failure domain, and ownership blur. Federated plugins with strong contracts reduce central implementation load.

**Separate domain portals** preserve specialist ownership and pace. They multiply navigation, identity, terminology, and accessibility work. Shared deep links and capability semantics can reduce fragmentation.

**Resource-centric navigation** supports ownership and lifecycle. It can obscure cross-resource tasks. Add journey entry points and task views.

**Task-centric navigation** supports immediate work. It can hide durable resource state and later responsibilities. Link outcomes to canonical resource pages.

**Single-page application** enables rich transitions. It increases client state, bundle, routing, and accessibility complexity. Server rendering and progressive enhancement can simplify critical paths.

**Embedded provider UI** speeds integration. It creates inconsistent identity, accessibility, styling, support, and trust boundaries. Prefer stable links or capability integration when embedding cannot meet contracts.

**Personalized homepage** reduces repeat navigation. It can create filter bubbles and behavioral data. Keep critical status and universal discovery independent of personalization.

**Real-time updates** reduce refresh effort. They add connection, ordering, battery, announcement, and stale-recovery complexity. Polling with freshness may be sufficient for slower operations.

## Failure Modes and Misconceptions

- **“A portal is a dashboard.”** A useful portal supports complete journeys, actions, recovery, ownership, and lifecycle.
- **“The screen is the source of truth.”** It is a projection whose provenance and freshness must remain visible.
- **“Our component library is accessible.”** Complete composed tasks still require manual and user evaluation.
- **“Hidden means unauthorized.”** Server-side enforcement is required for every data access and mutation.
- **“A spinner means work continues.”** Only durable operation state and correlation establish progress.
- **“More plugins mean more value.”** Plugins add supply-chain, performance, semantic, accessibility, and support costs.
- **“One homepage serves everyone.”** Segments and contexts require different entry points over shared contracts.
- **“The portal replaces CLI and API.”** Browser interaction is one channel and often unsuitable for automation.
- **“Green is current.”** Health without source, scope, and freshness can be dangerously stale.
- **“Clicks measure productivity.”** They are activity signals and can rise because a journey became harder.

## Worked Examples

### Example 1

A catalog page shows a service owner from repository metadata, runtime state from the platform API, cost from a provider, and application SLO from telemetry. Each card labels source and freshness; no aggregated portal table becomes the new owner of all four facts.

### Example 2

A deployment operation continues after the user closes the tab. Returning through a stable operation URL reconstructs accepted, running, failed health check, rollback, and repair evidence. The browser session never owns the operation lifecycle.

### Example 3

A keyboard user opens a combobox, selects a region, reviews validation, submits, and reaches confirmation without focus loss or pointer gestures. Automated checks had passed before manual testing found a focus trap in the plugin overlay.

### Example 4

A session expires during a long environment form. Reauthentication returns to the preserved, encrypted draft with a new authorization check. It does not silently submit, erase work, or expose values through a URL.

### Example 5

A malicious catalog description contains markup and a provider error includes a crafted link. Context-aware encoding and sanitization render both as safe content. The portal does not trust data because it originated inside the organization.

### Example 6

A cost plugin times out. Its error boundary shows last update and owner while the service page, documentation, and deployment action remain available. Portal telemetry attributes the degraded feature without turning the whole page into a generic failure.

### Example 7

A database deletion preview lists dependents, backups, retention, cost stop, and the exact production resource. Submission binds to the reviewed resource version; drift forces a new review. The confirmation does not override a policy denial.

### Example 8

A provider outage makes resource observation stale. The portal labels the last source time, blocks destructive work requiring current state, allows safe read access, links the incident, and later reconciles queued observations. It never shows cached green as live.

### Example 9

A CLI-created rotation operation appears in the portal using the same operation ID. The portal adds visual evidence and accessible recovery controls but does not rename states or invent a second retry token.

### Example 10

A homepage “most visited” widget is popular but stores sensitive resource patterns and improves no task. The team removes it, shortens retention for remaining journey analytics, and invests in search failure and independent-completion research.

## Cross-Program Connections

Human-computer interaction contributes information architecture, interaction design, accessibility, usability research, progressive disclosure, and error prevention. Web engineering contributes HTTP, navigation, rendering, caching, sessions, responsive layout, and performance. Security engineering contributes authentication, authorization, anti-forgery, output encoding, content policy, dependency trust, and audit.

Distributed systems contributes durable operations, uncertainty, partial failure, event ordering, idempotency, and freshness. API engineering supplies resource and operation schemas. Reliability engineering supplies degraded modes, status, objectives, and recovery. Data governance constrains analytics, personalization, and browser storage.

Product management connects portal investment to segments, journeys, hypotheses, and lifecycle. Organizational design assigns shell, plugin, capability, provider, support, and application ownership. Documentation and content design make interfaces understandable instead of relying on graphical arrangement alone.

## References

- W3C, [*Web Content Accessibility Guidelines (WCAG) 2.2*](https://www.w3.org/TR/WCAG22/), Recommendation of December 12, 2024. Current normative perceivable, operable, understandable, robust, complete-process, and conformance requirements.
- W3C Web Accessibility Initiative, [*ARIA Authoring Practices Guide*](https://www.w3.org/WAI/ARIA/apg/), current guide retrieved September 2, 2026. Accessible widget patterns, semantics, properties, states, and keyboard interaction guidance.
- OWASP Foundation, [*Application Security Verification Standard*](https://owasp.org/www-project-application-security-verification-standard/), current project and standard retrieved September 2, 2026. Verifiable web-application security requirements across architecture, authentication, sessions, authorization, input, and communications.
- OWASP Cheat Sheet Series, [*Session Management Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), current guidance retrieved September 2, 2026. Session identifiers, cookies, transport, renewal, expiry, logout, and client-side storage guidance.
- OWASP Cheat Sheet Series, [*Cross-Site Request Forgery Prevention Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html), current guidance retrieved September 2, 2026. Token, SameSite, origin, Fetch Metadata, and defense-in-depth patterns with architectural limitations.
- Backstage Project, [*Architecture Overview*](https://backstage.io/docs/overview/architecture-overview/), current documentation retrieved September 2, 2026. Portal app, frontend/backend, extension tree, plugins, catalog, templates, and documentation composition.
- Backstage Project, [*Software Catalog*](https://backstage.io/docs/features/software-catalog/), current documentation retrieved September 2, 2026. Source-controlled metadata, ownership, discovery, entity views, integrated tooling, and diagnostic boundaries.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Current internal-product, critical-journey, clear-feedback, independent-work, task-success, and balanced-measurement guidance.
- ISO, [ISO 9241-210:2019 — *Human-Centred Design for Interactive Systems*](https://www.iso.org/standard/77520.html), reviewed and confirmed 2025. Current human-centered lifecycle, context-of-use, multidisciplinary, and iterative evaluation principles.
- UK Government Digital Service, [*Designing Good Government Services: An Introduction*](https://www.gov.uk/service-manual/design/introduction-designing-government-services), current Service Manual retrieved September 2, 2026. End-to-end design across digital, offline, support, exception, supplier, and unpredictable technical paths.

## Exercises

### Exercise 1

Design a portal product boundary and information architecture for teams that own services, data pipelines, and machine-learning endpoints. Identify sources of truth, journey entry points, resource pages, global functions, non-goals, and escape routes.

### Exercise 2

Design the complete portal state model for creating an environment through an asynchronous provider. Include form, validation, preview, submission, operation, stale, partial, failure, interruption, recovery, and verification states.

### Exercise 3

Audit a plugin that reads provider credentials from browser storage, renders provider HTML, hides unauthorized buttons client-side, and has no error boundary. Specify the security, ownership, and architecture changes required before installation.

### Exercise 4

Create an accessibility evaluation plan for a production database deletion journey. Cover standards, automation, manual testing, assistive technologies, research, plugin composition, destructive review, errors, reauthentication, status, and recovery.

### Exercise 5

Transfer the portal model to a regional hospital laboratory-result platform. Define authoritative boundaries, clinical and privacy authority, accessible workflows, operation evidence, degraded behavior, plugin constraints, and analytics limits.

## Answers to the Exercises

### Answer 1

The portal owns shell, navigation, identity presentation, authorized aggregation, operation views, preferences, and drafts. Repository metadata owns declared component ownership; platform APIs own resources and operations; providers own bounded infrastructure state; telemetry owns observations; domain teams own application acceptance. Journey entries include create/deploy/recover service, run/repair pipeline, and provision/retire governed endpoint. Canonical pages exist for team, workload, environment, operation, policy evidence, and incident, with source and freshness. Global search, “what I own,” attention queue, documentation, notifications, and support cross domains. Non-goals include replacing automation, provider specialist tools, or domain decisions. CLI/API equivalents, provider escape routes, and outage-safe status are documented. Shared vocabulary and IDs connect every path.

### Answer 2

Start with discover/eligible, new draft, restored draft, validating, invalid with field summary, valid, preview loading, preview ready with derived scope, stale preview, authorization denied, and submission ready. Submission uses a request identity and becomes submitting, response unknown, accepted, queued, running by stage, needs action, cancelling, cancelled, provider-degraded, succeeded technically, verification pending, verified, failed retryable, failed non-retryable, and expired. Each state names authoritative source, freshness, mutation truth, available action, and ownership. Refresh reconstructs by operation ID; duplicate submit reuses identity. Client interruption stops observation only. Partial resources list retained state and cleanup. Success requires the environment verification contract, not provider creation alone.

### Answer 3

Reject installation pending redesign. Replace browser-stored provider credentials with a server-side capability service or backend plugin using short-lived scoped identity; authorize every request server-side. Treat provider HTML as untrusted and render typed encoded data or rigorously sanitized content under a restrictive content policy. Client-side button visibility may improve comprehension but never enforces access. Add plugin owner, threat model, data classification, permission manifest, dependency provenance, accessibility evidence, performance budget, objectives, support, compatibility, and retirement policy. Add timeouts and an error boundary so failure does not remove shell or unrelated actions. Use shared resource/operation contracts and audit correlation; do not let the plugin invent provider-facing authority.

### Answer 4

Set the applicable policy and WCAG 2.2 AA target, then map the complete path: locate database, verify identity, inspect dependents/backups/retention, request preview, handle denial and drift, confirm exact target, submit, observe, interrupt, recover, and verify deletion. Automate semantic, name/role/value, contrast, and selected regression checks, but manually test keyboard, screen reader combinations, magnification, reflow, high contrast, reduced motion, touch, voice, focus order/obstruction, status announcements, errors, timeout, and reauthentication. Include disabled consumers in scenario research. Test composed plugins and provider messages, not isolated controls. Ensure confirmation is understandable without color or pointer, retained form data is safe, operation state survives navigation, and recovery is accessible. Record evidence and unresolved user needs rather than claiming universal accessibility.

### Answer 5

Laboratories own result truth, provenance, correction, and release; clinicians own interpretation and care; privacy authorities own lawful access and disclosure; the platform owns technical routing, correlation, and evidence; receiving systems own acknowledgement. The portal projects these sources with timestamps and never turns transport green into clinical receipt. Accessible paths cover identity, search, urgent routing, result review, correction, downtime queue, acknowledgement, error, support, and patient recourse where authorized. Strong confirmation names patient-safe pseudonymous context, destination, result version, and correction consequence. During outage it shows last-known state, queues only safe intent, and supports reconciliation. Plugins declare clinical data access, permission, owner, accessibility, supply chain, and isolation. Analytics exclude result content and individual performance, minimize identifiers, restrict access/retention, and measure safe task completion and inequitable failure.
