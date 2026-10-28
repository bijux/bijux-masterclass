---
module_id: API-028
program: API & Service Engineering
level: 1
module_number: 28
title: Contract-First and Code-First Workflows
status: complete
last_verified: 2026-09-01
---

# Contract-First and Code-First Workflows

## One-Page Review

### Governing question

How should a team choose and control a contract-first or code-first workflow so that one authoritative source produces reviewable interface artifacts, implementations conform to their published promises, and neither generation nor deployment creates hidden drift?

### Essential definitions

- A **contract-first workflow** makes a reviewed interface description the authoritative design input before provider implementation.
- A **code-first workflow** makes reviewed implementation declarations—types, annotations, routing metadata, and explicit policy—the authoritative input from which an interface description is generated.
- The **authoritative source** is the artifact maintainers edit to change the public interface; generated projections are not edited independently.
- A **projection** is a deterministic derived artifact such as OpenAPI, generated server interfaces, clients, documentation, or mock configuration.
- **Drift** is a meaningful disagreement among intended contract, description, implementation, deployed behavior, and consumer expectations.
- **Conformance evidence** is a bounded observation that an implementation satisfies selected contract claims in a named environment.
- A **semantic diff** classifies changes by consumer-visible meaning rather than textual difference alone.

### Central model, mechanism, or theorem

Let $A$ be the authoritative source and $P_i=g_i(A,t_i,c_i)$ a projection produced by generator version $t_i$ and configuration $c_i$. A controlled workflow requires deterministic regeneration, reviewed transformations, and no independent edits to $P_i$. Let $K$ be the set of machine-checkable contract claims, $I$ the implementation, and $D$ the deployed service. Generation establishes provenance, not correctness: teams still need evidence that $I\models K$ and that observed $D\models K$. Transformations may lose information, so generally $h(g(A))\ne A$; round-trip generation is not synchronization.

### Critical invariants

One artifact is authoritative for each public fact. Generated files identify source, generator, configuration, and digest. Regeneration from a clean checkout is deterministic or its permitted variation is named. Generated outputs are never hand-edited. Consumer requirements precede representation choice. Semantic review occurs before compatibility-sensitive merge. Implementation-independent behavior—authorization, errors, timing, idempotency, and operational limits—is modeled explicitly. Provider and consumer checks use the published artifact. Release gates compare the artifact tested with the artifact deployed. Exceptions have an owner, expiry, and removal path.

### Common failures

Calling a workflow contract-first because YAML exists; generating a description from code that omits failure semantics; generating server stubs and assuming the provider conforms; editing generated clients; maintaining code and OpenAPI as coequal sources; using textual diffs as compatibility judgments; bidirectional generation that drops vendor extensions or schema constraints; exposing framework internals as public design; regenerating with floating tool versions; publishing an artifact from a different commit than the binary; and treating a mock as deployed evidence.

### Compact example

A team edits reviewed OpenAPI, generates a typed server interface, and writes domain logic behind it. The generator proves only that the interface was derived from the document. CI also validates the document, checks the semantic diff, compiles the generated boundary, runs provider scenarios, records the OpenAPI digest in the binary, and compares that digest at deployment. **Conclusion:** “contract-first” names the direction of authorship; the surrounding controls make it trustworthy.

### Connections

[Outside-In API Requirements](011-outside-in-api-requirements.md) identifies consumer tasks before either workflow. [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md) defines the promise being represented. [OpenAPI Structure](023-openapi-structure.md) and [Examples and Executable Documentation](027-examples-and-executable-documentation.md) supply description and evidence artifacts. [Mocking and Consumer Exploration](../ROADMAP.md) later uses a candidate contract before provider completion, while Contract Testing tests selected obligations.

## Governing Question

Which facts should humans author, which projections should tools generate, where can information be lost, and what review and conformance gates make contract-first or code-first delivery safe for independent consumers?

## Why This Matters

An API exists at several surfaces at once. Consumers see documentation, descriptions, examples, generated clients, observed HTTP exchanges, and runtime behavior. Producers see requirements, route declarations, types, validation code, domain policies, generated interfaces, tests, build artifacts, and deployed processes. If these surfaces disagree, the label attached to the workflow does not protect anyone.

Contract-first is attractive when independent consumers need to explore and review an interface before provider code exists. It can expose resource modeling, compatibility, naming, error, and authorization questions early. Code-first is attractive when implementation language types and framework declarations can express the public surface accurately and keep documentation close to working routes. It can reduce duplicated declarations and give developers rapid feedback.

Neither direction is inherently rigorous. A contract-first document can be fictional, unimplementable, or detached from production. A code-first description can faithfully expose accidental framework choices while omitting behavior that annotations cannot express. The durable decision is not “YAML or code.” It is the ownership and evidence architecture: where each fact originates, how it is transformed, who reviews it, how loss is detected, and how the released artifact is tied to deployed behavior.

The OpenAPI Specification 3.2.0 defines a language-agnostic interface description for HTTP APIs. It does not prescribe an authoring workflow and does not claim that an implementation conforms merely because it can emit an OpenAPI document. HTTP semantics remain governed by HTTP standards, while schemas describe selected instance constraints. Workflow design must preserve these distinctions.

## Prerequisites and Retrieval

Retrieve consumer tasks and service boundaries; HTTP method, status, header, representation, cache, and precondition semantics; OpenAPI paths, operations, components, schemas, examples, callbacks, and security declarations; JSON Schema dialect and validation behavior; request and response ownership; compatibility; generated-code boundaries; deterministic builds; source control; continuous integration; contract tests; deployment identity; and observability.

Before choosing a workflow, retrieve the consumer population, change cadence, implementation languages, supported generators, public-behavior owners, regulatory or review constraints, existing description quality, release topology, and whether clients and providers can update independently. The correct workflow depends on these conditions, not team fashion.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish contract-first and code-first authorship from generation and testing;
2. assign a single authoritative source to every public interface fact;
3. model generation as a potentially lossy transformation with explicit provenance;
4. design review, compatibility, conformance, and deployment gates;
5. diagnose drift among descriptions, source code, binaries, and observed services;
6. select a workflow from consumer, organizational, and technical constraints; and
7. migrate incrementally without creating two editable sources of truth.

## Core Exposition

### Begin outside the workflow

The first input is not an OpenAPI file or a controller class. It is a set of consumer tasks, domain meanings, failure expectations, security boundaries, and operational constraints. Both workflows can otherwise optimize an interface that should not exist or mirror an internal data model that does not serve consumers.

Write decision records for the facts that no generator can infer reliably: why the operation exists; which actor may attempt it; what authorization disclosure policy applies; whether retries are safe; what consistency is observable; which errors are stable; and which latency, quota, or retention statements are contractual. Then decide where each fact can be represented and checked.

A workflow should answer four questions for every public fact:

1. Where is it authored?
2. How is it reviewed?
3. Into which artifacts is it projected?
4. Which evidence checks the deployed behavior?

If a team cannot answer the first question, it has ambiguous ownership. If it cannot answer the fourth, it has documentation rather than a controlled contract workflow.

### Understand contract-first accurately

In contract-first delivery, the interface description is reviewed before provider implementation is the authority for that public surface. A typical flow is:

1. capture consumer situations and behavioral decisions;
2. author OpenAPI, referenced schemas, examples, and complementary policy;
3. validate structure and resolve references;
4. review semantics, security, compatibility, and implementability;
5. expose mocks or generated clients for exploration;
6. generate provider boundary code where useful;
7. implement behavior behind that boundary;
8. run conformance and consumer checks; and
9. publish exactly the reviewed artifact with the release.

“Before implementation” does not mean a large document is frozen before learning begins. Teams can work in thin vertical slices: one consumer task, a small contract change, examples, mock exploration, implementation, and evidence. The key property is that public design changes enter through the contract authority rather than being discovered accidentally after code merge.

Contract-first supports language-neutral review. Consumer representatives, security engineers, technical writers, and teams in other languages can inspect one artifact without reading provider framework code. It also makes mocking and client generation possible before the provider is complete. These benefits depend on the document being sufficiently semantic. A generated server interface cannot implement authorization, transaction boundaries, idempotency, or state transitions by itself.

### Understand code-first accurately

In code-first delivery, implementation declarations are the authoritative input. These may include route registration, public request and response types, annotations, explicit response variants, security metadata, and documentation strings. A generator analyzes those declarations and emits OpenAPI or another interface description.

A controlled code-first flow is:

1. capture consumer and behavioral decisions outside framework syntax where necessary;
2. modify reviewed public boundary declarations;
3. compile and test them;
4. generate the description with pinned tooling;
5. validate and semantically review the generated artifact;
6. compare it with the released contract;
7. run consumer and provider evidence; and
8. publish the generated artifact tied to the binary.

Code-first does not mean “whatever the running server happens to expose.” Accidental routes, implementation-only fields, framework defaults, undocumented exception mappings, and internal types must not become public merely because reflection can see them. Define a deliberate public boundary inside the implementation and keep domain and persistence models behind it.

The approach is strongest when the framework can represent the required contract without opaque extensions, generation is deterministic, and the same team owns contract and provider. It weakens when several languages need neutral review, consumers must begin before provider code, annotations cannot express required semantics, or generation changes significantly between tool versions.

### Assign authority at fact level

“The OpenAPI file is the source of truth” is too broad if rate policy lives in a gateway configuration, authorization in policy code, and examples in a fixture repository. Conversely, “the code is truth” is vague when public documentation and compatibility policy cannot be derived from code.

Create an authority map. For example:

| Public fact | Authoritative source | Projection | Evidence |
|---|---|---|---|
| path, method, parameter shape | reviewed OpenAPI | server interface, client | request conformance |
| domain state transition | domain policy and contract prose | scenario fixtures | postcondition test |
| public error classification | OpenAPI responses plus error registry | exception mapping | negative scenarios |
| actor capability | authorization policy | OpenAPI security hints, portal text | policy and non-disclosure tests |
| quota | service policy configuration | documentation and response headers | gateway/service observation |
| deployed contract identity | build manifest | endpoint metadata, catalog entry | deployment attestation |

The table may differ under code-first: route and shape authority moves to public boundary declarations, but semantic policy might remain elsewhere. What matters is that two editable artifacts do not both claim the same fact. A derived description can be reviewed and committed, but changes to it must be made through its authority.

### Treat generation as a compiler pipeline

Generation is a transformation, not clerical convenience. Model a projection as:

$$
P_i=g_i(A,t_i,c_i,e_i),
$$

where $A$ is authoritative input, $t_i$ generator identity and version, $c_i$ configuration and templates, and $e_i$ relevant environment. Reproducibility requires these inputs to be pinned or recorded. If locale, filesystem ordering, current time, network state, or floating dependencies alter output, the projection is not safely reviewable.

Store provenance beside or inside generated output: source commit and digest, generator version and digest, configuration digest, command, and relevant platform assumptions. Rebuild in a clean environment and compare. Some generated timestamps can be normalized, but hiding widespread nondeterminism with a broad ignore rule makes review weaker.

Never manually repair generated output. A repair disappears on regeneration and creates two histories. Change the authority, generator, template, or explicit post-processing transformation. Test custom templates like source code because a template can weaken validation, rename fields, mishandle nullable values, or omit authentication.

Generation success proves only that the tool accepted its input and produced output. It does not prove that the design is sensible, the output compiles, the implementation behaves correctly, or consumers are compatible.

### Assume transformations can lose information

Suppose $g:C\rightarrow O$ derives OpenAPI $O$ from code declarations $C$, and $h:O\rightarrow C'$ derives server code. A tempting expectation is:

$$
h(g(C))=C.
$$

Usually this is false. The code may contain control flow, validation, generics, framework behavior, or annotations the description cannot express. The description may contain examples, links, constraints, and extensions the code generator ignores. Even when observed wire shapes match, comments, naming, defaults, or type precision can change. Therefore:

$$
h(g(C))\ne C
$$

is the safe default unless a narrowly defined equivalence relation has been proven for the supported subset.

Round-trip editors amplify the problem. Alternating code-to-description and description-to-code transformations can erase a little information each time. Do not use bidirectional generation as automatic merge. Pick a direction, define the supported language subset, and reject constructs that cannot survive the intended transformation.

Loss can be semantic without being syntactic. A language integer type might map to an OpenAPI integer format that overstates or understates range. A nullable host-language type might conflate missing with explicit null. An exception hierarchy might collapse into one `500`. A framework default may emit `200` where the reviewed contract expects `201`. Audit the mapping table, not merely parser success.

### Separate interface, generated boundary, and domain implementation

Generated server code is best treated as an adapter boundary. It can parse messages, validate declared shapes, dispatch typed calls, and serialize responses. Domain behavior belongs behind a stable application interface. Regeneration should not overwrite handwritten policies.

Use ownership boundaries such as:

- generated files: replaceable, never edited;
- boundary adapters: thin handwritten mapping if generation does not own it;
- application services: use-case orchestration and transaction policy;
- domain model: business invariants and state transitions; and
- infrastructure: persistence and external integrations.

Code-first systems need the same separation in reverse. Public request and response models should not be persistence entities. Otherwise a database migration can silently change required fields, names, null behavior, or sensitive projections in the generated contract.

Generation should fail on unsupported or ambiguous mappings. Quietly degrading `oneOf`, precision, discriminators, read/write ownership, or constraints creates plausible but false types. If a generator cannot preserve a crucial construct, keep that piece handwritten behind a generated interface or choose another mechanism.

### Design semantic review before implementation lock-in

Textual diffs report changed lines, not consumer consequences. Reordering YAML, resolving references, or changing descriptions can make a large textual diff with no wire change. A one-line change from optional to required can be breaking.

A semantic diff should classify at least:

- operation addition, removal, or relocation;
- method, path, parameter location, style, or encoding change;
- request accepted-set widening or narrowing;
- response produced-set widening or narrowing;
- status, header, media type, schema, and error changes;
- security requirement and disclosure changes;
- default and example changes that influence generated clients;
- lifecycle and deprecation changes; and
- generator surface changes for supported languages.

Classification is directional. Adding an optional response property may be compatible for tolerant readers but break closed generated models. Widening accepted requests usually helps consumers, while widening produced responses may challenge them. Policy must reflect actual consumer behavior rather than a universal “non-breaking” label.

Run semantic comparison on the normalized, resolved artifact that consumers receive, but preserve source locations for review. A tool can flag possible compatibility effects; a human still evaluates meaning, consumer evidence, and mitigation.

### Build layered gates

A mature workflow uses gates with distinct claims:

1. **Source gate:** parse, lint, resolve references, validate schemas, and enforce style and ownership rules.
2. **Generation gate:** regenerate in a clean environment, check provenance, reject diffs, and compile generated surfaces.
3. **Compatibility gate:** compare against the last released contract and require review for classified changes.
4. **Implementation gate:** exercise request parsing, response serialization, errors, policy, and postconditions against the provider.
5. **Consumer gate:** compile or test representative supported consumers and mocks.
6. **Artifact gate:** bind the contract digest to the binary or immutable image.
7. **Deployment gate:** verify the deployed workload advertises or attests the same digest and run bounded smoke conformance.

The ordering matters. Fast source and generation checks reject basic defects before expensive integration checks. Compatibility review should occur before dependent work builds on a breaking shape. Deployment identity closes a common gap: CI tested commit $x$, but the portal or service deployed artifact from commit $y$.

The following executable example audits a small delivery ledger. It requires one authority, deterministic generation, matching tested and deployed digests, and no operation drift. It demonstrates workflow invariants, not OpenAPI parsing.

<!-- bijux-verify: {"id":"workflow-ledger-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"authority=contract\ngeneration=deterministic\nmissing_in_implementation=[]\nundocumented_implementation=[]\ndeployment_digest=matched\npromotion=allowed\n","stderr":""}} -->
```python
ledger = {
    "authority": "contract",
    "source_digest": "sha256:8ad1",
    "generated_from": "sha256:8ad1",
    "regenerated_digest": "sha256:b741",
    "committed_projection_digest": "sha256:b741",
    "tested_contract_digest": "sha256:8ad1",
    "deployed_contract_digest": "sha256:8ad1",
}
contract_operations = {"GET /orders/{id}", "POST /orders"}
implemented_operations = {"POST /orders", "GET /orders/{id}"}

missing = sorted(contract_operations - implemented_operations)
undocumented = sorted(implemented_operations - contract_operations)
deterministic = (
    ledger["regenerated_digest"] == ledger["committed_projection_digest"]
    and ledger["generated_from"] == ledger["source_digest"]
)
deployed_match = (
    ledger["tested_contract_digest"] == ledger["deployed_contract_digest"]
)
allowed = deterministic and deployed_match and not missing and not undocumented

print(f"authority={ledger['authority']}")
print(f"generation={'deterministic' if deterministic else 'drifted'}")
print(f"missing_in_implementation={missing}")
print(f"undocumented_implementation={undocumented}")
print(f"deployment_digest={'matched' if deployed_match else 'mismatched'}")
print(f"promotion={'allowed' if allowed else 'blocked'}")
```

Real conformance goes beyond operation-set equality. The example makes an important discipline visible: promotion is a conjunction of evidence, so one successful generator or test cannot erase another failed invariant.

### Model drift explicitly

Useful drift classes include:

- **described but not implemented:** the contract promises an operation, status, field, or constraint absent at runtime;
- **implemented but not described:** a reachable route, accepted field, error, or response escapes review;
- **generated approximation:** a projection exists but weakened, widened, or changed the authority's meaning;
- **version skew:** provider, client, mock, or portal uses a different contract version;
- **deployment mismatch:** tested source and deployed executable do not correspond; and
- **behavioral drift:** shapes match while authorization, effects, ordering, idempotency, or timing differs.

Detect each class with an appropriate comparison. Static route-to-description checks find some operation drift. Schema-based provider checks find selected shape drift. Scenario postconditions find behavior drift. Artifact digests find version mismatch. Production observations can reveal undocumented outcomes, but traffic sampling is incomplete and must protect sensitive data.

Do not “fix” drift by automatically importing whatever production currently does into the authority. Runtime may be defective or compromised. Reconcile intent, compatibility, and observations through review.

### Keep generated clients subordinate to the contract

Generated clients are projections optimized for one language and generator. Their public surface can change when templates, naming rules, reserved-word handling, nullable mappings, or dependency versions change even if the wire contract does not. Pin supported generators and treat generator upgrades as compatibility events.

Do not make consumers edit generated models to work around a contract problem. Put handwritten conveniences in a separate wrapper or partial-extension boundary where the language supports it. Regeneration should be safe and routine.

Compile generated clients, run serialization fixtures, and exercise unknown response values, optional fields, numeric boundaries, and error variants. A client compile check is useful evidence, but it cannot show that the provider performs the promised state transition.

### Represent what types cannot infer

Host-language types rarely express the whole public contract. They may not capture conditional constraints, cross-field invariants, access-dependent fields, stable problem types, header obligations, caching, idempotency, retry safety, or eventual observations. Code-first workflows need explicit declarations or complementary governed artifacts for these facts.

Annotations can also lie. `@Success(200)` does not force a handler to return only `200`; `@Authorized` does not establish object-level authorization; and a non-null type does not guarantee data is present after a partial database failure. Check runtime paths, including exceptions and middleware.

Contract-first descriptions also have expressive limits. OpenAPI describes an HTTP interface but does not by itself prove temporal properties, exactly-once effects, fairness, or a complete authorization policy. Use prose with testable language, state models, policy code, and scenario evidence without pretending all meaning fits one document.

### Coordinate branches and reviews

Long-lived contract and implementation branches create skew. Prefer small changes and an order that makes compatibility visible:

1. propose the authority change and examples;
2. run semantic review with affected consumer owners;
3. merge compatible provider support where necessary;
4. publish an immutable candidate or version;
5. update consumers independently; and
6. activate behavior only when compatibility evidence permits.

For additive changes, providers often deploy tolerant support before consumers use it. For breaking changes, introduce a parallel compatible surface or migration window instead of merging description and behavior changes blindly. Feature flags may control activation, but the contract must state which behavior consumers can rely on at each lifecycle stage.

Generated output can create noisy merge conflicts. Regenerate from the merged authoritative source using the pinned tool rather than manually combining generated hunks. CI should reject a projection whose source digest does not match the current authority.

### Choose from constraints, not ideology

Prefer contract-first when multiple independent teams need early language-neutral agreement; client work must precede provider code; public governance is strong; several implementations share one interface; or compatibility risk dominates local development convenience.

Prefer code-first when one team owns a rapidly evolving internal service; public boundary declarations are precise; tooling covers required semantics; the implementation language is stable; and generated descriptions receive real semantic review. Code-first can still support independent consumers if publication and compatibility controls are strong.

A hybrid is safe only when authority is unambiguous. For example, contract-first may own external operations while code-first generates internal diagnostic endpoints into a separate non-public description. Another safe hybrid keeps OpenAPI authoritative for shapes and a policy repository authoritative for authorization. An unsafe hybrid lets developers edit both annotations and OpenAPI and “merge whichever changed last.”

Evaluate total cost: authoring, tool maintenance, semantic gaps, consumer lead time, review access, generator churn, testing, and migration. The shortest path to the first endpoint may create the most expensive long-term compatibility system.

### Migrate without dual authority

To move from undocumented code to contract-first, first capture observed and intended behavior separately. Generate or inventory a candidate description, but mark it as discovered evidence rather than truth. Reconcile routes, shapes, errors, and policies; add provider checks; obtain consumer review; then designate an accepted contract version as authoritative. Subsequent changes enter through that contract.

To move from manually maintained OpenAPI to code-first, define the supported semantic subset and map every existing construct to code declarations. Generate a candidate, normalize both artifacts, and compare meaning. Block migration if constraints, examples, security, or errors disappear. Only after equivalence evidence and consumer review should authority move to code.

Use a cutover record with date, responsible owners, old and new authority digests, known exceptions, and removal conditions. During a bounded transition, CI can require equivalence between old and new representations, but humans must not independently edit both. Route changes through one side and regenerate the other.

### Tie publication to deployment

Version descriptions and artifacts immutably. A mutable `/openapi.json` generated at server startup is useful for discovery but insufficient as the release record if framework or configuration changes can alter it. Archive the reviewed artifact, embed its digest or version in the build manifest, and expose safe deployment metadata.

At promotion, verify that provider tests used the archived contract, the binary was built from the corresponding source, and the portal or registry publishes the same artifact. After deployment, run bounded non-destructive checks and observe unexpected statuses or fields without logging sensitive payloads.

Rollback must restore a compatible contract-behavior pair. Rolling back only the binary while leaving a newer portal contract, gateway policy, or generated client release can preserve the incident. Treat release identity as a set of related immutable artifacts.

## Definitions and Notation

Let $R$ be reviewed consumer requirements and behavioral decisions. Let $A$ be the chosen authoritative source for a public fact, and let $P_1,\ldots,P_n$ be generated projections. Each projection is produced by $P_i=g_i(A,t_i,c_i,e_i)$.

Let $N(X)$ normalize artifact $X$ only over explicitly irrelevant syntax. Deterministic generation requires:

$$
N(g_i(A,t_i,c_i,e_i))=N(g_i(A,t_i,c_i,e_i'))
$$

for every permitted build environment $e_i'$; otherwise environment differences must be included in provenance or eliminated.

Let $K(A)$ be machine-checkable claims extracted from authority $A$, $I$ the implementation under test, and $D$ the deployed system. $I\models K(A)$ means collected evidence satisfies the selected claims, not that all possible behavior is correct. Release identity requires contract digest $d_A$, tested digest $d_T$, embedded digest $d_B$, published digest $d_P$, and deployed digest $d_D$ to agree:

$$
d_A=d_T=d_B=d_P=d_D.
$$

Let $\Delta_s(A_0,A_1)$ be a semantic, directional change classification. It differs from textual diff $\Delta_t$ because small text can change a large accepted set and large text can preserve meaning. A **supported subset** is the precisely documented constructs a transformation preserves. A **generated boundary** is replaceable derived code that adapts wire messages to handwritten behavior. A **cutover record** establishes when authority moved and under what evidence.

## Mechanisms, Invariants, or Proof Structure

1. Elicit consumer tasks and behavioral guarantees before choosing artifact form.
2. Assign one authoritative source to every public fact.
3. Map projections, owners, transformation versions, and evidence.
4. Pin generators, templates, dependencies, configuration, and normalization.
5. Reject unsupported or lossy mappings instead of silently approximating them.
6. Review semantic changes before implementation and consumer lock-in.
7. Compile generated boundaries and keep handwritten domain behavior separate.
8. Run provider, consumer, compatibility, and negative scenario checks.
9. Bind reviewed contract, tested implementation, published artifact, and deployment by digest.
10. Observe drift, reconcile it through authority, and record exceptions with expiry.

The core proof obligation is not “a file was generated.” It is a chain: requirements justify authority; deterministic transformations justify provenance; semantic review justifies intended compatibility; execution supplies bounded conformance evidence; and artifact identity justifies that the evidence applies to the deployed release.

## Alternatives and Trade-Offs

Contract-first improves early, language-neutral collaboration and makes consumer exploration possible before provider completion. Its costs include maintaining description expertise, generator limitations, and the risk that implementation work diverges. Strong provider checks and thin slices control that risk.

Code-first keeps public declarations close to compiled code and can reduce repeated shape definitions. Its costs include framework coupling, incomplete semantic expressiveness, accidental exposure, and delayed consumer review. A deliberate public boundary, generated-artifact review, and complementary policy sources control those risks.

Handwritten clients preserve idiomatic design and precise behavior but cost more and can drift. Generated clients scale across languages but expose generator decisions as another compatibility surface. Generated transport cores with handwritten ergonomic wrappers often balance the two.

Committing generated artifacts makes diffs, offline builds, and consumer access easier, but adds repository noise and merge conflicts. Generating only in release pipelines reduces noise but requires immutable toolchains and artifact storage. Either policy must allow reproducibility and review.

Strictly rejecting any semantic change protects consumers but can block safe additions. Automatically accepting tool-labeled additions is fast but ignores actual consumer strictness. Use directional classification, real consumer evidence, ownership, and explicit exceptions.

Runtime description generation reflects the deployed framework state but may vary with flags, middleware, or environment. Build-time archival gives stable identity but can miss runtime routing changes. Compare both under controlled configuration and investigate differences.

## Failure Modes and Misconceptions

- **“Contract-first means writing YAML before code.”** It means a reviewed contract is authoritative; file timing alone says nothing about rigor.
- **“Code is always the real truth.”** Code contains bugs and internal details; public truth is the promise consumers may rely on.
- **“Generated means synchronized.”** Generation links artifacts only for one run and direction; provenance and regeneration checks maintain that link.
- **“Round-trip generation preserves everything.”** Transformations commonly lose semantics, names, constraints, examples, or framework behavior.
- **“A server stub conforms by construction.”** It may conform at a type boundary while returning wrong statuses, effects, authorization, or timing.
- **“A generated OpenAPI document needs no review.”** Generators can expose accidental routes, wrong nullability, incomplete errors, or unstable names.
- **“Both files can be sources of truth.”** Coequal editing creates conflicts with no principled resolution.
- **“A clean textual diff is a compatibility proof.”** Compatibility concerns admitted and produced behavior, not line count.
- **“An additive response field is always safe.”** Closed models and brittle consumers may reject it; consumer evidence matters.
- **“Annotations express every behavior.”** Cross-field rules, temporal guarantees, access policy, and operational limits often need other authorities.
- **“Mocks prove provider conformance.”** Mocks demonstrate configured expectations and consumer behavior, not provider execution.
- **“Passing provider tests proves production matches.”** Artifact or deployment skew can invalidate otherwise good evidence.
- **“Generated files can be patched once.”** The patch will be lost or create permanent divergence; fix the source or transformation.
- **“Tool upgrades are maintenance-only.”** They can change client APIs, serialization, defaults, or generated contract meaning.
- **“Migrating means generate and replace.”** Authority changes require semantic reconciliation, evidence, consumer review, and a recorded cutover.

## Worked Examples

### Example 1

**Situation:** Three consumer teams must begin clients before a new order provider exists. **Reasoning:** Their languages differ, and they need shared error, pagination, and authorization decisions. Make reviewed OpenAPI and scenario fixtures authoritative, expose a mock for exploration, generate optional client cores, and implement provider behavior against the same artifact. **Conclusion:** contract-first fits early language-neutral coordination, but provider conformance remains a separate gate.

### Example 2

**Situation:** One team owns a small internal service and its only consumer, using a framework whose public types express all current shapes. **Reasoning:** Delaying every route for separate document editing adds duplication. Use deliberate public boundary types as authority, generate OpenAPI in CI, review the semantic diff, and keep errors and authorization in complementary governed declarations. **Conclusion:** code-first can be rigorous when its expressiveness and ownership assumptions are explicit.

### Example 3

**Situation:** A developer changes generated client code to treat an unknown enum as `UNKNOWN`. **Reasoning:** Regeneration will erase the repair, and other languages remain unsafe. Change the authoritative response design or generator template, add an unknown-value fixture, pin the updated tool, and regenerate every supported client. **Conclusion:** repair the authority or transformation, never a replaceable projection.

### Example 4

**Situation:** Code-to-OpenAPI generation maps a missing-or-null host type to `type: [string, "null"]`. **Reasoning:** The mapping preserves explicit null but may lose whether the property is required. Compare four instances—missing, null, string, and wrong type—against intended behavior and declare `required` independently. **Conclusion:** type mapping must be checked as accepted-set semantics, not name similarity.

### Example 5

**Situation:** A semantic diff tool labels a new optional response field non-breaking. **Reasoning:** Inventory shows an old generated client rejects unknown properties. Deploying the field would break that consumer despite an additive schema diff. Upgrade or configure the client first, use tolerant-reader tests, or introduce a controlled migration. **Conclusion:** tooling classifies likely effects; real consumer behavior decides release safety.

### Example 6

**Situation:** OpenAPI promises `404` for concealed inaccessible orders, while controller annotations declare `403`. **Reasoning:** This is a security disclosure conflict, not documentation polish. Identify the authorization policy as authority, align description and mapping, then test authorized, absent, and concealed targets. **Conclusion:** fact-level authority resolves drift that file-level slogans cannot.

### Example 7

**Situation:** Clean regeneration changes hundreds of client lines after a generator upgrade but no OpenAPI line. **Reasoning:** The generator is part of the projected public surface. Compare serialization and public client APIs, compile supported consumers, review template release changes, and version the generator upgrade separately. **Conclusion:** a toolchain change can be compatibility-sensitive even with a stable wire contract.

### Example 8

**Situation:** CI tests contract digest `a1`, but the deployed container advertises `b7`. **Reasoning:** Provider tests cannot be attributed to this deployment. Block promotion, trace image and portal provenance, rebuild from the reviewed commit, and require equality across archived, tested, embedded, published, and deployed digests. **Conclusion:** release identity is a conformance prerequisite.

### Example 9

**Situation:** A legacy service emits runtime OpenAPI containing 64 routes, while the intended inventory has 60. **Reasoning:** Do not automatically bless the extra four. Classify them as internal health routes, accidental debug routes, or undocumented public behavior; remove or isolate them, then establish an accepted contract and route check. **Conclusion:** discovered behavior is evidence to reconcile, not automatic authority.

### Example 10

**Situation:** A team wants to migrate from contract-first to code-first because annotations are easier. **Reasoning:** Map every schema constraint, example, response, security declaration, and extension to the proposed declarations. Generate a candidate, compare normalized semantics, test boundary instances, and retain contract authority until equivalence and consumer review pass. Record one cutover digest and forbid dual editing. **Conclusion:** workflow migration is an authority migration, not a file conversion.

## Cross-Program Connections

[Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) supplies requirements, design records, and iterative delivery. [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies boundary and ownership reasoning. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies oracles, generated-artifact tests, and conformance evidence. [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies reproducible builds, artifact provenance, promotion, and rollback. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) can provide paved-road generators and registries, but API owners retain responsibility for interface meaning.

## References

1. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), language-agnostic interface description and normative object model, 19 September 2025. Checked 2026-09-01.
2. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), Internet Standard, June 2022. Checked 2026-09-01.
3. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema: A Media Type for Describing JSON Documents, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-core), 16 June 2022. Checked 2026-09-01.
4. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema Validation: A Vocabulary for Structural Validation of JSON, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-validation), 16 June 2022. Checked 2026-09-01.
5. OpenAPI Generator contributors, [*Using Templates*](https://openapi-generator.tech/docs/templating/), transformation model and template customization. Checked 2026-09-01.
6. M. Nottingham and E. Wilde, [*RFC 9205: Building Protocols with HTTP*](https://www.rfc-editor.org/rfc/rfc9205.html), Best Current Practice 56, June 2022. Checked 2026-09-01.

## Exercises

### Exercise 1

For a contract-first service, identify what generation proves and what it does not prove. Classify server-interface generation, compilation, schema conformance, provider scenario execution, and deployment digest comparison.

### Exercise 2

Trace a code-first change that makes `nickname` nullable in a host language. Determine the intended behavior for missing, explicit null, valid string, empty string, and wrong type; then state the OpenAPI/JSON Schema information the generator must preserve.

### Exercise 3

Diagnose a pipeline where developers edit OpenAPI and controller annotations, regenerate clients manually, publish docs from `main`, test an older binary, and deploy an image built from a release branch. Propose the smallest coherent authority and artifact controls.

### Exercise 4

Choose contract-first or code-first for a public payments interface implemented by three provider teams and consumed in six languages. Compare consumer lead time, semantics, security review, generator limits, ownership, and conformance; include the complementary artifacts your choice still needs.

### Exercise 5

Design an incremental migration for a legacy service whose runtime description disagrees with observed traffic and intended policy. Specify discovery, reconciliation, cutover, compatibility, generation, testing, artifact identity, and rollback.

## Answers to the Exercises

### Answer 1

Server-interface generation proves that a named tool accepted a contract and produced a projection under recorded inputs. Deterministic clean regeneration adds provenance. Compilation proves that generated and handwritten code type-check in the recorded toolchain. Schema conformance proves selected messages satisfy selected structural claims. Provider scenarios add bounded evidence for statuses, headers, effects, failures, and policies. Deployment digest comparison establishes that tested contract identity matches the running release. None alone proves universal correctness; together they form a traceable evidence chain.

### Answer 2

Test five distinct instances: absent property, property set to JSON `null`, a representative string, empty string, and a non-string. Decide independently whether the property is required and whether null is in its type. If optional and nullable, the schema omits `nickname` from `required` and admits both `string` and `null`; an empty string requires a length decision. Wrong type should fail. The generator must not conflate host-language defaulting, optional presence, nullability, or minimum length. Boundary fixtures should fail the build if those mappings change.

### Answer 3

The system has dual authority and broken provenance. Choose either reviewed OpenAPI or deliberate public boundary declarations as authority; given existing cross-artifact use, OpenAPI is the smaller likely cutover. Generate clients and any controller boundary only through pinned CI, prohibit manual generated edits, and compare committed projections after clean regeneration. Archive the reviewed contract, bind its digest to the tested binary and image, publish that immutable artifact, and require the deployed digest to match. Controller annotations become derived checks or are removed where they duplicate public facts.

### Answer 4

Contract-first is the stronger default because independent provider teams and six consumer languages need early neutral agreement and centralized compatibility and security review. Make OpenAPI, schemas, examples, and an error registry authoritative for representable facts; use explicit authorization and payments policy for facts OpenAPI cannot prove. Generate replaceable language clients and server boundaries with pinned tools, but permit idiomatic wrappers. Require semantic diffs, security review, consumer compilation and serialization fixtures, provider postcondition tests, and deployment identity. Code-first could work only with a single neutral generation authority and equivalent review, but three provider codebases would otherwise compete to define the interface.

### Answer 5

Inventory intended operations and policies, generate a candidate from routes, and sample observed traffic safely; label both as evidence rather than truth. Reconcile every extra, missing, or conflicting operation with owners and consumer usage. Create an accepted candidate contract, classify compatibility from the last observed supported behavior, and add provider and consumer fixtures. Select one authority, pin transformations, and prohibit dual editing. Record the cutover digests and known exceptions, bind the contract to a tested immutable image, and deploy behind bounded observation or staged traffic. Rollback restores the previous compatible image, gateway policy, and published contract as one release set; unexplained drift blocks cutover.
