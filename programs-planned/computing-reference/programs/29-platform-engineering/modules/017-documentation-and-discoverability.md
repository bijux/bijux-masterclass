---
module_id: PLAT-017
program: Platform Engineering
level: 1
module_number: 17
title: Documentation and Discoverability
status: complete
last_verified: 2026-09-02
---

# Documentation and Discoverability

## One-Page Review

### Governing question

How should a platform make capabilities, interfaces, decisions, evidence, and support discoverable at the moment of need while preserving ownership, version, freshness, accessibility, authorization, and a clear route from reading to verified action?

### Essential definitions

- **documentation** is maintained information that helps a defined audience learn, perform work, look up facts, understand decisions, or recover from failure.
- **discoverability** is a consumer's ability to locate, recognize, evaluate, and enter the appropriate supported capability or information path.
- **information scent** is the evidence in names, labels, summaries, relationships, and links that lets a person predict whether a destination will help.
- A **documentation contract** states audience, job, scope, authority, owner, version, freshness, prerequisites, expected outcome, and feedback route.
- A **tutorial** creates a guided learning experience; a **how-to guide** directs a competent reader through a task; **reference** describes the system; **explanation** builds understanding.
- **docs as code** applies source control, review, build, testing, and release practices to documentation; it does not mean only programmers can contribute.
- **authoritative source** is the system whose owner governs a fact. A portal, search index, or generated page may project that fact without acquiring authority.
- A **stale document** no longer meets its declared freshness or version contract; staleness is evidence-based, not merely old age.

### Central model, mechanism, or theorem

Model a documentation surface as $D=(U,J,C,S,A,F,O,E)$: audience $U$, job $J$, content type and contract $C$, source and version $S$, authorization $A$, freshness $F$, owner $O$, and task evidence $E$. Discovery is a chain—query or browse, recognize, evaluate, enter, act, verify—and failure at any link prevents self-service. Search relevance alone is insufficient: ranking and presentation must preserve authority, access, lifecycle, and freshness.

### Critical invariants

- Every supported capability has canonical identity, purpose, owner, lifecycle, access route, documentation, and support path.
- Task guidance, conceptual explanation, and machine-generated reference are related but not collapsed into one undifferentiated page.
- Generated reference comes from an authoritative contract and never invents semantics absent from that contract.
- Search and catalog results enforce authorization before retrieval and do not leak restricted names, snippets, relationships, or embeddings.
- Version, applicability, source, owner, last verification, deprecation, and known limitations remain visible at decision points.
- Examples are safe, complete, copyable when appropriate, version-bound, and tested against supported interfaces.
- Documentation navigation and content remain operable and understandable with supported assistive technologies and input methods.
- Success is measured by correct task outcomes and recovery, not page views, document count, or search clicks alone.

### Common failures

Writing one giant guide; organizing by platform-team structure; indexing secrets or restricted metadata; ranking an obsolete page above the current contract; publishing generated API fields without workflow meaning; showing commands that mutate production by default; using screenshots as the only instruction; hiding ownership; breaking inbound links on rename; duplicating the same fact across many pages; treating search clicks as success; letting an assistant answer without sources or access checks; and archiving a capability without a successor or migration route.

### Compact example

A developer searches “deploy payments canary.” Access-aware search returns a current task guide owned by the payments platform team, scoped to platform release 7, with prerequisites and a tested CLI example. The capability page links the underlying deployment resource reference, conceptual rollout explanation, operational status, known limitations, and support route. A deprecated release-5 guide remains accessible through a version selector but is labeled, excluded from default ranking, and points to migration. The developer completes the deployment and sees workload verification evidence; the journey records task success rather than assuming the clicked page solved the problem.

### Connections

Retrieve consumer vocabulary from [PLAT-002](002-platform-consumers-and-jobs-to-be-done.md), cognitive-load constraints from [PLAT-003](003-developer-cognitive-load.md), product lifecycle from [PLAT-004](004-platform-as-product.md), capability and provider boundaries from [PLAT-007](007-platform-capabilities-versus-tool-catalogs.md) and [PLAT-008](008-internal-platforms-and-external-cloud-services.md), ownership from [PLAT-009](009-platform-team-boundaries.md), journey evidence from [PLAT-011](011-developer-journeys.md) and [PLAT-012](012-time-to-first-successful-deployment.md), and channel, resource, and scaffold contracts from [PLAT-013](013-command-line-interfaces.md) through [PLAT-016](016-templates-and-scaffolding.md).

## Governing Question

What must a consumer be able to find, trust, understand, and do, and how can a platform keep that path correct as interfaces, teams, permissions, and underlying systems change?

Documentation is not an inventory of everything the platform team knows. It is a product surface that connects a consumer's situation to a supported action or understanding. Discoverability begins before prose: names, catalog entities, ownership, API descriptions, search terms, portal navigation, CLI help, errors, templates, and peer vocabulary all influence what can be found.

A technically correct page can still fail if the reader cannot locate it, identify its applicability, access its prerequisites, understand its language, execute its example, or verify the result. The unit of design is the information journey, not the document.

## Why This Matters

Self-service without trustworthy information transfers queue time into search and guesswork. Consumers compare old pages, chat messages, code, portal views, and provider documentation, then choose whichever seems plausible. If ownership and versions are invisible, the cost appears as rework, unsafe copying, support interruptions, and platform distrust.

Diátaxis distinguishes tutorials, how-to guides, reference, and explanation according to different reader needs. The separation is useful because a learner needs a safe guided experience, a practitioner needs a direct task route, an implementer needs precise reference, and a reader making a decision needs context. The model is a design aid rather than a required site hierarchy; one journey can link several content types.

Current Backstage TechDocs documentation illustrates docs-like-code, preview, build, publish, catalog integration, search, and issue reporting. Its catalog documentation models software, APIs, resources, systems, domains, ownership, and lifecycle to help people discover the ecosystem. These are examples of an information architecture; a catalog should remain a governed projection rather than absorb every dynamic fact as truth.

OpenAPI 3.2.0 describes HTTP interfaces so humans and computers can discover capabilities. A description can generate useful reference and tooling, but structure does not explain consumer goals, authorization decisions, asynchronous outcomes, recovery, or operational promises. Authored task and conceptual information remain necessary.

WCAG 2.2 navigation guidance emphasizes ways to find content, determine location, use meaningful headings and labels, and bypass repeated blocks. Accessibility applies to the complete information task: search, results, navigation, examples, code-copy controls, feedback, and linked operations. Google’s maintained developer-documentation guidance reinforces direct language, hierarchy, meaningful links, alternative text, and global readability.

## Prerequisites and Retrieval

Retrieve platform definition, consumer segments and jobs, cognitive load, product management, self-service, paved roads, capability contracts, provider boundaries, team interfaces, value hypotheses, developer journeys, deployment evidence, CLI help, portal navigation, API resources, and template provenance from PLAT-001 through PLAT-016.

You should understand technical writing, information architecture, source control, APIs and schemas, static-site generation, search indexing and ranking, authorization, caching, versioning, redirects, localization, accessibility, telemetry, privacy, user research, incident response, and content lifecycle management.

## Learning Objectives

After completing this module, you should be able to:

1. derive documentation and discovery paths from consumer jobs, vocabulary, and decision points;
2. choose tutorial, how-to, reference, explanation, or embedded guidance according to reader need;
3. define canonical capability metadata and a versioned documentation contract;
4. design access-aware catalogs, browse structures, search indexes, ranking, and result presentation;
5. generate reference from authoritative contracts while adding honest workflow semantics and examples;
6. verify links, examples, versions, accessibility, freshness, ownership, and complete task outcomes;
7. operate feedback, change, deprecation, redirects, archiving, and incident documentation; and
8. measure findability and successful action without surveillance or misleading engagement metrics.

## Core Exposition

### Begin with the information journey

Describe the consumer's situation, vocabulary, urgency, authority, environment, prior knowledge, and desired outcome. Map how the person currently asks: portal search, general web search, CLI help, repository search, catalog browse, error message, colleague, support channel, or automated client. Each entry point needs enough scent to reach the same canonical capability.

Trace discovery as query or browse, recognition, evaluation, entry, action, and verification. A zero-result search fails early. A vague title fails recognition. Missing owner or version prevents evaluation. An inaccessible page prevents entry. An incomplete example prevents action. A success message without evidence prevents verification.

Design common and consequential tasks first. Rare reference facts still matter, but a beautiful alphabetical index does not replace a route for “restore the production database safely” or “find who owns this failed deployment.”

### Separate content by reader need

A tutorial is learning-oriented: it controls complexity, provides a safe environment, produces visible progress, and teaches one coherent path. Do not interrupt it with every alternative or exhaustive field list.

A how-to guide is task-oriented: it states a goal, applicability, prerequisites, steps, expected observations, failure recovery, and completion evidence. It assumes relevant competence and avoids becoming a conceptual essay.

Reference is information-oriented and mirrors the system it describes: resources, fields, operations, commands, configuration, errors, limits, permissions, and compatibility. Generate what can be generated from schemas and source. Annotate gaps rather than invent semantics.

Explanation is understanding-oriented: it covers reasons, models, architecture, trade-offs, history that remains decision-relevant, and connections. Keep decision records near the owned system, but synthesize them for consumers who should not reconstruct architecture from dozens of records.

Embedded guidance—CLI help, form descriptions, validation errors, empty states, and operation status—serves the moment of action. It should link to deeper canonical material and share vocabulary rather than duplicate a parallel contract.

### Define the documentation contract

Model one surface as

$$
D=(U,J,C,S,A,F,O,E),
$$

where $U$ is audience, $J$ job, $C$ content type and contract, $S$ authoritative source and applicable version, $A$ authorization, $F$ freshness state, $O$ accountable owner, and $E$ evidence that the information helps complete the task.

Every page should make title, purpose, audience when non-obvious, prerequisites, applicable product or API version, owner, last verified state, and feedback route discoverable. Consequential guides also state environment, permissions, reversibility, expected output, verification, failure recovery, and limitations.

Avoid a ritual “last reviewed” date with no contract. Define what invalidates the page: interface change, owner change, dependency release, policy change, incident learning, elapsed review interval, broken example, or consumer report. Freshness is tied to sources and risk.

### Build a canonical capability catalog

The catalog answers what exists, what it does, who owns it, who may use it, its lifecycle, interfaces, dependencies, documentation, status, support, and entry actions. Use durable domain and capability names. Include synonyms and previous names for search without making them canonical labels.

Keep stable ownership and relationship metadata near its authoritative source when practical, and project it into the catalog. Dynamic runtime state belongs to operational systems and should be linked or freshly queried with provenance. A catalog cache must show source and freshness rather than masquerade as live truth.

Model at a useful level. Cataloging every transient object creates noise; omitting systems, APIs, and owners hides the mental model. Backstage's current catalog guidance explicitly centers human models and warns against treating the catalog as exhaustive dynamic truth. The durable principle is to choose entities that support discovery, ownership, and action.

### Design access-aware search and browse

Index canonical identity, title, summary, body, headings, owner, domain, capability, API terms, error codes, synonyms, lifecycle, versions, and relationships. Preserve source revision, index time, authorization policy, and freshness metadata. Deduplicate mirrors and select a canonical URL.

Apply authorization before a result, snippet, count, facet, relationship, or semantic representation reaches the consumer. Filtering after retrieval can leak restricted names and text. Re-index access changes promptly, and test cache and search-engine behavior with revoked identities.

Ranking combines textual or semantic relevance with task fit, authority, lifecycle, version applicability, ownership, quality, and freshness. Popularity can help but can also entrench an obsolete page. Deprecated and archived content should remain retrievable when needed while being labeled and demoted for default current queries.

The following synthetic ranker checks that a current owned how-to outranks a deprecated exact-title match.

<!-- bijux-verify: {"id":"documentation-discovery-ranking","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidates=4\ntop=payments-deploy-howto\ntop_owner=team-payments\nstale_results=1\norphan_results=1\nunsafe_top=false\n","stderr":""}} -->
```python
records = [
    {"id": "payments-deploy-v5", "relevance": 10, "task": 2, "current": False, "owner": "team-payments"},
    {"id": "payments-deploy-howto", "relevance": 8, "task": 5, "current": True, "owner": "team-payments"},
    {"id": "payments-api-reference", "relevance": 7, "task": 2, "current": True, "owner": "team-payments"},
    {"id": "payments-notes", "relevance": 6, "task": 1, "current": True, "owner": None},
]

def score(record):
    lifecycle_penalty = 8 if not record["current"] else 0
    ownership_penalty = 4 if record["owner"] is None else 0
    return record["relevance"] + record["task"] - lifecycle_penalty - ownership_penalty

ranked = sorted(records, key=lambda record: (-score(record), record["id"]))
top = ranked[0]
print(f"candidates={len(ranked)}")
print(f"top={top['id']}")
print(f"top_owner={top['owner']}")
print(f"stale_results={sum(not record['current'] for record in ranked)}")
print(f"orphan_results={sum(record['owner'] is None for record in ranked)}")
print(f"unsafe_top={str((not top['current']) or top['owner'] is None).lower()}")
```

Real ranking weights require evaluation with representative queries and judgments. The example contains no authorization, semantic retrieval, click data, or production evidence; it only demonstrates that relevance must not erase lifecycle and ownership signals.

Browse complements search. Organize by consumer jobs, domains, capabilities, owned resources, lifecycle, and supported paths—not only by the platform organization chart. Provide breadcrumbs, meaningful headings, multiple ways to find important content, stable URLs, version selectors, and related next actions.

### Join generated reference with authored semantics

Generate API, CLI, schema, event, configuration, and policy reference from authoritative machine-readable contracts. Bind output to contract revision, preserve deprecation and compatibility, validate examples, and fail the build when unresolved references or invalid shapes appear.

OpenAPI can describe paths, operations, parameters, representations, servers, security schemes, and schemas. It cannot by itself specify which business task to choose, when asynchronous status is trustworthy, what authorization will be granted, how to recover from partial failure, or which operational objective applies. Add authored guides and explanations linked to canonical operations.

Do not copy generated fields into handwritten tables that immediately drift. Add descriptions at the authoritative schema where possible. When consumer explanation belongs elsewhere, link by stable operation or resource identity and test that the link resolves for each supported version.

### Make examples executable and safe

An example states prerequisites, environment, permissions, placeholders, complete command or request, expected output, verification, cleanup, and version. Use obviously non-secret values and safe test targets. Never make production, deletion, public exposure, or expensive provisioning the copy-paste default.

Test syntax and execution in clean supported environments. Validate output against the real interface contract. Redact nondeterministic IDs while keeping semantic assertions. For asynchronous operations, show durable operation identity and how to distinguish accepted, running, succeeded, failed, and unknown.

Examples are compatibility consumers. Running them detects documentation defects and breaking interface changes. A skipped test must remain visible with reason and owner; a green prose build does not prove code samples work.

### Use docs-as-code without excluding contributors

Co-locating documentation with code can align review and release, enable previews, and connect owners. It can also hide information in repositories that consumers do not know, impose Git fluency, and privilege implementation structure over user journeys. Provide portal editing, issue reports, or assisted contribution routes where appropriate, then preserve review and provenance.

Build documentation in isolated, pinned environments. Treat Markdown, plugins, diagrams, remote includes, API descriptions, and generated HTML as untrusted input. Prevent path and link escape, sanitize active content, restrict networks, scan secrets, validate licenses, and publish with least privilege.

Use automated checks for structure, links, anchors, spelling rules, schemas, code blocks, images, alternative text, headings, duplicated titles, prohibited secrets, source versions, owner references, and freshness. Human review remains necessary for correctness, task fit, clarity, accessibility, and harm.

### Design for accessibility and global use

Use descriptive titles and a logical heading hierarchy. Link text should make sense out of context. Preserve keyboard navigation, visible focus, skip mechanisms, meaningful landmarks, zoom and reflow, contrast, text alternatives, captions, and non-color status. Code-copy controls need accessible names and feedback.

Do not put essential instructions only in screenshots, diagrams, hover content, video, or color. Explain image intent in surrounding text when alternative text cannot carry the detail. Tables need headers and should not be used for visual layout.

Use direct, literal language; define terms and abbreviations; place conditions before actions; identify the actor; use unambiguous dates and units; and avoid culture-specific metaphors. Design strings, layout, search tokens, and examples for localization even if translation comes later. Localized content needs version and freshness parity or an honest warning.

Test representative end-to-end tasks with screen readers, keyboard-only input, zoom, reflow, high contrast, speech input, reduced motion where relevant, and users with different cognitive and language needs. Automated scans are useful but incomplete.

### Preserve version and lifecycle truth

Version documentation with the interface it describes. Default to the current supported release while retaining old versions required by live consumers. Every version selector and search result must show applicability. Do not silently update an old guide so it no longer matches its named version.

When moving content, create durable redirects and update canonical links. When renaming a capability, preserve old terms as synonyms and migration cues. Record deprecation date, reason, replacement, compatibility boundary, migration route, support window, and owner.

Archive rather than delete when operational history remains necessary, but mark archives prominently and exclude them from default guidance. Remove secrets and unlawful data even when preservation would otherwise be useful. Test inbound links from portals, CLI errors, SDKs, templates, incidents, and external bookmarks.

### Make feedback and incidents part of the system

Offer page-specific feedback with document identity, version, section, and optional task context. Route it to an accountable owner, acknowledge it, classify consequence, and close the loop. Avoid collecting source code, secrets, personal data, or individual performance telemetry in free-text and analytics.

Support queries, failed searches, incident findings, and repeated errors are inputs to documentation work. During an incident, prioritize current operational truth, timestamped updates, safe commands, owners, and decision evidence. Afterward, repair durable guides and runbooks rather than leaving the incident channel as canonical documentation.

AI or conversational retrieval can help translate questions and synthesize sources. It must enforce the same authorization as source systems, cite exact sources and versions, expose uncertainty, resist prompt or content injection, avoid training leakage, and provide a direct path to canonical material. An answer without provenance is not a new source of truth.

### Measure discoverability and task outcomes

Track representative-query success, zero-result and low-confidence queries, result relevance judgments, time to correct capability, search reformulation, task-guide completion, example pass rate, broken links, stale and orphan inventory, feedback resolution, support deflection with quality checks, first verified outcome, and recovery from failure.

Page views, time on page, and click-through are ambiguous. High time can mean engagement or confusion; a search click can lead to failure. Join analytics only at privacy-preserving journey boundaries and validate interpretation through interviews, usability studies, search-log review, and task observation.

Set objectives by consequence. A stale tutorial is different from a stale credential-revocation runbook. Prioritize ownership gaps, unsafe examples, broken critical journeys, and deprecated results outranking current guidance. Measure the maintenance burden on content owners so the information system remains operable.

## Definitions and Notation

$D=(U,J,C,S,A,F,O,E)$ models a documentation surface through audience, job, content contract, source/version, authorization, freshness, owner, and task evidence.

Let a discovery journey be $q\rightarrow r\rightarrow e\rightarrow a\rightarrow v$: query or browse $q$, recognition of candidate $r$, evaluation $e$, action $a$, and verification $v$. Reaching $r$ does not imply successful $v$.

For document $d$, freshness predicate $F(d,t)$ is true only when its governed sources, applicable versions, owner, and risk-based review contract remain valid at time $t$. Age alone neither proves nor disproves freshness.

Let result score $s(d,q)$ combine relevance, task fit, authority, lifecycle, applicability, quality, ownership, and freshness under an authorization filter. No scalar score removes the need to show these attributes to the consumer.

## Mechanisms, Invariants, or Proof Structure

Use an information-product loop: research questions and vocabulary; inventory capabilities and sources; assign identity and owner; model content needs; author or generate; test contracts and examples; build and publish securely; index with authorization; evaluate search and browse; observe complete tasks; accept feedback; respond to change and incidents; version, redirect, deprecate, archive, and retire.

The authority invariant preserves source ownership across generated pages and projections. The applicability invariant binds guidance to versions and environments. The authorization invariant prevents discovery leakage. The accessibility invariant covers the full path, not prose alone. The example invariant binds instructions to tested outcomes. The lifecycle invariant prevents obsolete information from appearing current.

Adversarial review includes restricted title leaked in autocomplete; revoked access retained in cache; malicious Markdown or remote include; OpenAPI reference cycle or script content; command injection through a placeholder; copied production deletion; secret in logs or search index; deprecated exact match outranking current guidance; owner team dissolved; redirect loop; localization behind current safety change; assistant fabricates an answer; attacker plants high-ranking content; and analytics expose individual behavior.

## Alternatives and Trade-Offs

**Central documentation site** creates one discovery surface and consistent navigation. It can detach content from code owners and become a publishing bottleneck.

**Repository-local documentation** aligns changes and ownership. It fragments search, navigation, style, and access for cross-cutting journeys.

**Generated reference** is consistent with structured contracts. It inherits missing descriptions and cannot supply all task or operational semantics.

**Handwritten reference** can explain nuance. It duplicates structured truth and drifts without contract tests.

**Keyword search** is explainable and strong for identifiers. It struggles with vocabulary mismatch and intent.

**Semantic or conversational retrieval** can bridge vocabulary and synthesize. It adds authorization, provenance, injection, evaluation, latency, and uncertainty risks.

**One current version** simplifies discovery. It abandons consumers on supported older interfaces.

**All versions indexed equally** preserves history. It lets obsolete exact matches mislead current work unless lifecycle and applicability shape ranking.

## Failure Modes and Misconceptions

- **“If it exists, people will find it.”** Discovery requires vocabulary, metadata, indexing, navigation, access, and information scent.
- **“One comprehensive guide is simplest.”** Mixed learning, task, reference, and explanation needs make it hard to scan and maintain.
- **“Generated reference is complete documentation.”** Schemas omit goals, decisions, recovery, and operational truth.
- **“The catalog is the source of truth.”** It often projects governed metadata and dynamic systems with delay.
- **“Search relevance is enough.”** Access, owner, version, lifecycle, authority, and freshness affect safety.
- **“Last reviewed means current.”** Only a defined source and invalidation contract establishes freshness.
- **“Copyable commands are usable.”** They also need prerequisites, safe scope, expected output, verification, and cleanup.
- **“Automated accessibility passed.”** Complete-task testing with assistive technologies and people is still required.
- **“Clicks prove success.”** They prove navigation, not correct action or outcome.
- **“An AI answer replaces docs.”** Without authorized sources, citations, versions, and uncertainty, it weakens truth.

## Worked Examples

### Example 1

A catalog organizes tools by the platform team's squads. Research shows consumers ask for “publish an event” and “restore a database.” Navigation changes to job and capability terms while team ownership remains visible metadata.

### Example 2

An onboarding tutorial lists every network option before the first deployment. It moves alternatives into reference and explanation, chooses a safe sandbox path, and preserves visible learning checkpoints.

### Example 3

OpenAPI generates accurate request fields for an asynchronous deployment. An authored how-to adds permission prerequisites, idempotency, accepted-versus-verified status, failure recovery, and workload evidence.

### Example 4

A restricted service name appears in autocomplete for an unauthorized developer. The index pipeline moves authorization ahead of result, facet, snippet, and embedding retrieval and purges stale caches on revocation.

### Example 5

A release-5 page exactly matches “rotate credential” and outranks release 7. Ranking demotes deprecated versions, the result displays applicability, and the old page links a tested migration.

### Example 6

A copied command deletes the default project because the placeholder is optional. The example uses an explicit sandbox identifier, validates context, previews targets, requires confirmation, and supplies expected evidence and cleanup.

### Example 7

A diagram contains the only dependency explanation. The page adds a textual relationship list and narrative, meaningful alternative text, keyboard-accessible links, and a downloadable machine-readable graph.

### Example 8

A team rename breaks ownership and old bookmarks. The catalog resolves the canonical new team, retains the old name as a search synonym, redirects stable URLs, and flags orphaned documents until ownership is accepted.

### Example 9

Search click-through rises while support requests also rise. Task observation shows users opening a popular but incomplete guide. The team adds failure recovery and verification, tests the example, and measures successful completion instead.

### Example 10

A conversational assistant recommends a private runbook to an unauthorized user. The design retrieves only after source authorization, cites versioned passages, labels uncertainty, refuses unavailable content without confirming its existence, and links the canonical page.

## Cross-Program Connections

Information retrieval contributes indexing, lexical and semantic ranking, evaluation judgments, and query analysis. API engineering contributes machine-readable descriptions, versioning, authorization, examples, and error contracts. Software engineering contributes docs-as-code, tests, builds, ownership, redirects, and compatibility.

Security contributes access-aware retrieval, sanitization, injection resistance, secrets, audit, and privacy. Accessibility and human-computer interaction contribute navigation, language, content structure, assistive technology, and task research. Reliability contributes runbooks, freshness objectives, incidents, status, and recovery.

Knowledge management contributes taxonomy, provenance, lifecycle, and organizational memory. Product management contributes segmentation, jobs, feedback, outcome measures, and retirement. Organizational design makes ownership and support discoverable across team changes.

## References

- Diátaxis, [*Diátaxis in Five Minutes*](https://diataxis.fr/start-here/), current handbook retrieved September 2, 2026. Tutorials, how-to guides, reference, and explanation organized by distinct reader needs.
- Backstage Project, [*TechDocs Documentation*](https://backstage.io/docs/features/techdocs/), current documentation retrieved September 2, 2026. Docs-like-code, catalog integration, search, publishing, extensions, issue reporting, and supported architecture.
- Backstage Project, [*Creating and Publishing Your Docs*](https://backstage.io/docs/features/techdocs/creating-and-publishing/), current documentation retrieved September 2, 2026. Source layout, preview, generation, publication, source annotations, and symbolic-link containment.
- Backstage Project, [*Software Catalog*](https://backstage.io/docs/features/software-catalog/), current documentation retrieved September 2, 2026. Ownership, metadata, source-controlled descriptors, discovery, search, filtering, and team maintenance.
- Backstage Project, [*System Model*](https://backstage.io/docs/features/software-catalog/system-model/), current documentation retrieved September 2, 2026. Components, APIs, resources, systems, domains, groups, visibility, relationships, and machine-readable interfaces.
- Backstage Project, [*Creating the Catalog Graph*](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph/), current documentation retrieved September 2, 2026. Human mental models, catalog boundaries, ownership, inventory, lifecycle, search, projections, and dynamic-source cautions.
- OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), September 19, 2025. Language-agnostic interface description, human and machine discovery, references, cycles, and rich-text sanitization responsibilities.
- W3C, [*Web Content Accessibility Guidelines 2.2*](https://www.w3.org/TR/WCAG22/), W3C Recommendation dated December 12, 2024. Perceivable, operable, understandable, robust content and complete-process conformance.
- W3C Web Accessibility Initiative, [*Understanding Guideline 2.4: Navigable*](https://www.w3.org/WAI/WCAG22/Understanding/navigable), current guidance retrieved September 2, 2026. Finding content, location, headings, labels, multiple ways, focus, links, and bypass mechanisms.
- Google, [*Write Accessible Documentation*](https://developers.google.com/style/accessibility), current developer-documentation style guidance retrieved September 2, 2026. Direct language, scanning, headings, meaningful links, text alternatives, tables, and accessible media.
- Google, [*Developer Documentation Style Guide Highlights*](https://developers.google.com/style/highlights), updated April 2, 2025. Clear, consistent, accessible, inclusive, global, structured, and action-oriented technical writing guidance.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Internal-product framing, critical journeys, task-outcome feedback, independent work, adoption, retention, task success, and balanced measurement.

## Exercises

### Exercise 1

Design the documentation and discovery system for a deployment capability. Specify audiences, jobs, content types, catalog entity, source authority, versions, ownership, search metadata, access, examples, feedback, and outcome evidence.

### Exercise 2

Evaluate search results for “restore production database” containing a current how-to, obsolete exact match, provider reference, incident chat transcript, restricted runbook, and ownerless wiki page. Define filtering, ranking, labeling, and safe result behavior.

### Exercise 3

Turn a generated OpenAPI page into a complete consumer information journey for an asynchronous credential-rotation operation without duplicating the structured contract.

### Exercise 4

Design a verification and freshness program for 600 documentation sites with different risk, versions, owners, examples, localization, and inbound dependencies.

### Exercise 5

Transfer the model to hospital medication-administration guidance. Separate education, task procedure, drug/device reference, clinical explanation, authoritative policy, patient-specific orders, access, version, emergency change, accessibility, and evidence without allowing documentation to substitute for clinical authority.

## Answers to the Exercises

### Answer 1

Model novice application developers, experienced operators, automation authors, and incident responders separately. Provide a sandbox tutorial, deploy and rollback how-tos, generated resource/API/CLI reference, rollout and evidence explanation, and embedded CLI/portal/error guidance. The canonical `Deployment` capability entity exposes purpose, owner, lifecycle, access, status, support, resources, operations, docs, and synonyms; schemas and live operations retain their own authority. Bind pages and tested examples to platform versions and environments. Index identity, job terms, owners, errors, relationships, lifecycle, and freshness after authorization. Results show applicability and source. Feedback carries page/version/section to the owner. Measure correct capability selection, example pass, first verified deployment, safe rollback, failed-query recovery, and support quality—not clicks alone.

### Answer 2

Authorize before retrieval: the restricted runbook produces no title, snippet, count, facet, or existence signal for unauthorized users. Rank the current owned production how-to first when it applies to the user's platform version; show owner, verification date, risk scope, and expected outcome. Keep the obsolete exact match only behind a conspicuous deprecated label, version scope, demotion, and migration link. Provider reference supports underlying facts but does not replace platform procedure. The incident transcript is evidence and should point to the repaired durable guide, not rank as canonical. The ownerless wiki page is demoted or excluded from supported results and queued for ownership resolution. Evaluate with task judgments and restoration simulations, not clicks.

### Answer 3

Keep paths, schemas, security declarations, status representations, and examples generated from the versioned OpenAPI description. Add a how-to keyed to the canonical rotate operation: when to rotate, prerequisites, affected identity, environment, authorization, idempotency key, preview, request, accepted operation ID, polling or watch, terminal and unknown outcomes, application adoption, revocation boundary, verification, rollback limits, audit, and support. Link an explanation of overlap and recovery and a reference for errors and conditions. Test commands against a sandbox and supported versions; redact values. Do not copy field tables. Acceptance of the HTTP request is not rotation success; finish only after new use and old revocation evidence meet the contract.

### Answer 4

Inventory every site by canonical identity, owner, source, supported versions, content type, risk, languages, examples, inbound links, and invalidation events. Run continuous structural, link, anchor, schema, secret, owner, accessibility, and example checks. Weight review intervals and deployment simulations by consequence: credential revocation and database recovery receive tighter objectives than introductory explanations. Trigger review on source, API, owner, policy, dependency, incident, translation, and deprecation changes. Test representative assistive-technology and localized journeys. Provide owner dashboards and escalation for stale or orphaned pages. Preserve versioned archives and redirects. Sample human task accuracy and search judgments. A timestamp refresh without source and outcome checks does not satisfy freshness.

### Answer 5

Use tutorials for supervised learning, task procedures for authorized medication-administration workflows, reference for governed drug/device facts and interface fields, and explanation for clinical rationale and system behavior. Hospital policy and pharmacy formularies remain organizational authorities; prescriber orders and verified patient identity remain patient-specific clinical truth. Search must enforce role, ward, patient, and emergency access before revealing restricted content. Every procedure shows jurisdiction, facility, population, device/software version, owner, effective date, contraindication boundaries, escalation, and downtime route. Emergency updates are approved, timestamped, prominently distributed, and later reconciled into durable sources. Provide accessible text alternatives, clear units, unambiguous names, multilingual parity where supported, and non-color alerts. Verification can prove retrieval, identity checks, scanning, recording, and acknowledgement; documentation never diagnoses, prescribes, overrides an order, or proves safe administration by itself.
