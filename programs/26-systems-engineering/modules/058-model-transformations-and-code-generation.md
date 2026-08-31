---
module_id: SYSENG-058
program: Systems Engineering
level: 2
module_number: 58
title: Model Transformations and Code Generation
status: complete
last_verified: 2026-08-31
---

# Model Transformations and Code Generation

## One-Page Review

### Governing question

How can engineers transform models into other models, documents, configurations or executable code so the output is reproducible, traceable and verified for its intended use—without assuming that automation preserves semantics, completeness or safety?

### Essential definitions

- A **model transformation** maps a source model conforming to source metamodel $MM_s$ into a target model conforming to target metamodel $MM_t$ under declared rules and execution configuration.
- A **model-to-model transformation** produces another structured model. A **model-to-text transformation** produces linearized artifacts such as source code, configuration, reports or deployment files.
- An **endogenous** transformation stays within one metamodel; an **exogenous** transformation crosses metamodels. A **horizontal** transformation stays near one abstraction level; a **vertical** transformation changes abstraction level.
- A **declarative transformation** states relations or desired correspondences; an **imperative transformation** states an execution procedure. Real toolchains commonly mix them.
- A **transformation rule** identifies source patterns, guards, target construction/update, trace production and error behavior.
- A **trace model** records which source identities and rules produced which target identities/regions and diagnostics. A trace is evidence of derivation, not proof of semantic equivalence.
- **Semantic preservation** means specified source properties remain true, correspond appropriately or are intentionally refined in the target under an explicit relation. It must name the properties and abstraction relation.
- **Information loss** is source meaning that cannot be represented in the target or is deliberately omitted. Loss must be detected, bounded and accepted—not hidden by successful serialization.
- **Code generation** is compilation from a model or intermediate representation into source/binary/configuration artifacts. The generator, templates, libraries, adapters and build environment are part of the implementation chain.
- **Determinism** means the same controlled inputs and environment produce semantically equivalent, preferably byte-identical, outputs. Nondeterministic ordering, timestamps and locale undermine review and reproducibility.
- **Round-trip engineering** attempts coordinated forward and reverse updates. It requires defined authority, correspondences and conflict resolution; parsing generated text back does not recover omitted intent automatically.
- **Incremental transformation** updates affected targets after source changes rather than rebuilding everything. Correctness depends on dependency/trace completeness and deletion handling.
- A **protected region** is a generated-file area intended for controlled manual content. It creates merge, ownership and regeneration obligations.
- **Tool qualification/accreditation** supplies evidence that a tool is suitable for a bounded use. It never removes the need to verify outputs and integrated behavior required by the project's assurance regime.

### Central model, mechanism, or theorem

Treat transformation as a versioned compilation judgment:

\[
(M_s,MM_s,R,L,E)\Downarrow(M_t,\tau,D),
\]

where $M_s$ is the controlled source, $MM_s$ the source metamodel/libraries, $R$ transformation rules/templates, $L$ target runtime libraries/adapters, $E$ execution environment, $M_t$ target artifacts, $\tau$ trace and $D$ diagnostics. Acceptance requires:

\[
Pre(M_s)\land Conforms(M_t,MM_t)\land Post(M_s,M_t,\tau)\land Tests(M_t)\land D_{critical}=\varnothing.
\]

For semantic property set $P$, preservation is never simply “output generated.” It is a family of obligations:

\[
\forall p\in P:\quad M_s\models p\Rightarrow M_t\models \alpha(p),
\]

where $\alpha$ states how a source property maps or refines into target semantics. Unsupported $p$ must yield explicit loss/unknown evidence.

### Critical invariants

- Pin source/target metamodels, libraries, profiles, transformation/template/generator versions, target platform, runtime dependencies and environment.
- Validate source preconditions before generation; reject or quarantine invalid, incomplete and out-of-scope constructs rather than guessing.
- Every consequential source element is transformed, intentionally omitted with rationale, retained externally, or reported unresolved.
- Target identity, names, order and formatting are deterministic under declared inputs; unavoidable nondeterminism is isolated and explained.
- Trace records source identity/version, rule/template, target identity/region, diagnostics and transformation run.
- Rule guards, priorities, dispatch, defaults, recursion, ordering, deletion and conflict semantics are explicit and tested.
- Target output satisfies syntax/schema/metamodel, target-language type/static analysis, project coding/configuration standards and integration contracts.
- Semantic equivalence/refinement claims name properties, abstraction relation, assumptions and proof/test evidence; visual similarity and compilation are insufficient.
- Generated and handwritten authorities are separated. Manual edits cannot disappear silently or become an untraceable fork.
- Secrets, untrusted model text, identifiers and comments are escaped/validated for the target; generation is a supply-chain and injection boundary.
- The source, generator, rules/templates, libraries, configuration, toolchain and evidence are configuration-controlled so outputs can be reproduced.
- Invalid-source, unsupported-construct, generator-crash, partial-output, stale-trace, target-build and test failures are observable and fail according to policy.
- Generated code receives verification, validation, safety, security, performance and integration evidence appropriate to the same intended product use as handwritten code.
- Changes to source semantics, transformation, generator, libraries, compiler/runtime or target platform trigger impact analysis and proportionate regeneration/reverification.

### Common failures

Common failures include treating transformation as file conversion; mapping by display name instead of identity; failing open on unsupported constructs; silently dropping stereotypes, constraints, units or behavior; relying on undocumented rule order; generating unstable output; embedding timestamps; letting locale change numbers; producing traces that cannot survive rename/delete; updating targets incrementally with stale dependencies; editing generated files; merging protected regions incorrectly; trusting compilation as equivalence; validating generated code only at model level; reusing one golden model that lacks negative cases; ignoring target runtime/library semantics; generating injection-vulnerable text; accepting vendor qualification without project scope; checking in irreproducible output; and changing generator versions without replaying regression and system evidence.

### Compact example

A synthetic three-state controller model declares four transitions. A small generator sorts transitions, emits an eleven-line Python state function, records a four-entry source-to-line trace, regenerates byte-identically, checks required emitted structures, confirms all target states exist, reaches all three states and checks four transformed-table behavior cases. This establishes only the declared fixture and generator mapping. It does not parse, compile or execute the emitted function or establish SysML semantics, full state-machine semantics, real-time behavior, safety, target-platform correctness or tool qualification.

### Connections

SYSENG-056 supplies SysML semantics and SYSENG-057 supplies consistency/validation gates. SYSENG-058 turns governed models into downstream artifacts. SYSENG-059 must preserve their digital-thread identity/provenance; SYSENG-060 must integrate generation without creating process bureaucracy or shadow authority.

## Governing Question

Can an independent reviewer reproduce the exact target from controlled source and toolchain inputs, traverse source-to-target traces, account for every unsupported or intentionally lost construct, and demonstrate the target's required behavior and quality at the target execution layer?

A diff that says “generated successfully” is not an answer. Transformation moves engineering claims across semantic boundaries. Each boundary can add defaults, discard meaning, introduce platform assumptions or amplify one generator defect into every output.

## Why This Matters

Automation can remove transcription, standardize patterns and make downstream artifacts refreshable. It can also replicate errors at machine speed. A wrong handwritten condition affects one location; a wrong template can affect hundreds of services, controllers or interface files. The economics therefore shift verification toward source semantics, generator/rule evidence, representative fixtures and target integration—not away from verification.

OMG QVT 1.3 addresses model query/view/transformation, while OMG MOF Model to Text 1.0 specifies template-oriented production of text such as code, deployment specifications and reports. SysML 2.0 includes a separate normative v1-to-v2 transformation specification, demonstrating that even related language versions need explicit mappings. The Systems Modeling API and machine-readable artifacts enable automation, but API access is not semantic preservation.

NASA's current SWE-146 guidance requires an approach covering generator V&V, configuration management, allowable scope, generated-code V&V using the same standards/processes as handwritten code, actual-use monitoring, manual-edit policy and control of inputs/outputs/modifications. SWE-206 requires direct electronic access to auto-generation inputs and related artifacts. These are governance necessities because a generator is part compiler, dependency and production process.

## Prerequisites and Retrieval

Before designing or accepting a transformation, retrieve:

1. intended target use, users, decisions, criticality, regulatory/assurance constraints and acceptance authority;
2. exact source project/commit/configuration, source metamodel/libraries/profiles/extensions and source validity evidence;
3. target metamodel/language/schema/platform/compiler/runtime/library versions and downstream contracts;
4. mapping specification, rule/template source, priorities/guards/defaults, transformation engine, plugins and build container/environment;
5. stable identity policy, trace schema, naming/order/formatting rules, deletion and incremental-dependency semantics;
6. supported, partially supported and unsupported source constructs with information-loss and fallback policies;
7. generated/handwritten boundary, extension points, protected-region policy, ownership and regeneration/merge workflow;
8. reference fixtures, negative/adversarial cases, semantic properties, golden outputs, target tests, static analysis and qualification evidence;
9. source/toolchain licensing, provenance, integrity, vulnerabilities, secret handling and long-term reproducibility/maintenance plan;
10. prior runs, diagnostics, exceptions, known generator defects, affected outputs and revalidation triggers.

Use a retrieval test: “This code came from the model.” Ask which model commit and configuration, generator/templates/libraries, target/compiler/runtime, exact run and digest, trace from requirement/behavior to target, unsupported/lost content, manual modifications, tests and acceptance authority. Without that chain, “generated” is provenance theater.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish model-to-model, model-to-text, endogenous/exogenous, horizontal/vertical and declarative/imperative transformations;
2. define source/target conformance, preconditions, mapping rules, postconditions, trace and diagnostic contracts;
3. specify semantic preservation/refinement and information loss without overclaiming equivalence;
4. design deterministic, reproducible full and incremental transformations;
5. govern identity, deletion, rule dispatch, conflict, ordering and round-trip authority;
6. separate generated and handwritten content with safe extension mechanisms;
7. test transformations with positive, negative, boundary, metamorphic, differential and mutation fixtures;
8. verify generated code at model, generator, target-code, integration and real-system layers;
9. manage injection, dependency, toolchain, qualification and long-term maintenance risk;
10. assess changes and communicate bounded transformation evidence.

## Core Exposition

**Frame the transformation contract.** Name source and target languages/metamodels, abstraction levels, intended use and authoritative direction. State whether the target is derived/disposable, independently owned or synchronized. A report generator, migration, analysis export and flight-code generator need different round-trip and assurance policies.

**Classify the transformation.** Model-to-model preserves structured target semantics for further transformation/query. Model-to-text linearizes content. Endogenous refactoring can still change behavior; exogenous mapping can lose constructs. Vertical refinement adds platform decisions; horizontal translation may still change semantics. Classification exposes risks but does not prove correctness.

**Validate source preconditions.** Require declared conformance, approved subset, resolved references, configuration completeness and project invariants. Decide how unknowns and partial models behave. Never make the generator silently invent safety behavior, units, defaults or missing multiplicities to produce compilable output.

**Define mapping at semantic level.** For each source concept state target concept/pattern, guard, property mapping, identity, cardinality, defaults, trace, loss and postcondition. Map meaning rather than shapes or names. When target semantics differ, define refinement/abstraction and additional target assumptions.

**Make rule selection deterministic.** Overlapping rules need explicit specificity/priority/conflict behavior. Sort unordered source collections with stable keys. Fix locale, timezone, encoding, newline, floating formatting and dependency resolution. Avoid timestamps/random IDs in governed output or isolate them from semantic/diff comparison.

**Treat identity as a first-class mapping.** Stable target IDs may derive from source IDs plus namespace/rule, not mutable display names or traversal order. Preserve source-target trace across rename/move. On deletion, remove or deprecate target artifacts according to policy; orphan detection is essential.

**Produce durable traces.** Record source commit and element IDs, transformation/rule version, target artifact/region IDs, run ID, diagnostics and digests. Support one-to-many, many-to-one and split/merge mappings. A line-number-only trace is fragile; use stable anchors plus line mappings where useful.

**Detect and report loss.** Maintain a coverage matrix for constructs and properties. Unsupported content should fail, emit explicit unknown/loss, or be preserved in a controlled extension—not disappear. Sample successful mappings and all high-consequence loss paths. “No target equivalent” is an engineering decision requiring owner acceptance.

**Separate derivation from migration.** Derived targets can be regenerated and should usually not accept independent semantic edits. A migration creates a new target authority after reconciliation and acceptance. Keeping a live reverse transform after migration can reintroduce obsolete semantics.

**Design incremental transformation carefully.** Dependency graph and trace must include direct, transitive, negative-query and ordering dependencies. Handle additions, updates, moves, deletes and rule/library changes. Compare periodic clean rebuilds with incremental outputs to detect stale targets. Full regeneration is often simpler and safer when affordable.

**Constrain round trips.** Declare authoritative fields/directions and conflict-resolution policy. Bidirectional relations can synchronize selected semantics but cannot resolve stakeholder intent automatically. Avoid two independently editable full authorities. Protected regions should be narrow, typed extension points with structural merge tests.

**Generate code as a compiler pipeline.** Use stages: validated source model, normalized intermediate representation, target generation, formatting, compilation/static analysis, unit/property tests, integration and system validation. Version every stage. Intermediate representations make defaults and platform decisions reviewable.

**Keep generated and manual code separate.** Prefer generated modules plus stable handwritten adapters/callbacks/interfaces. Mark generated headers with provenance and do-not-edit policy. If generated output is stored, verify clean regeneration and digest; if not stored, ensure the build environment remains reproducible and archival obligations are met.

**Escape target content.** Model names, descriptions and values may be untrusted. Apply grammar-aware escaping for identifiers, strings, paths, shell/config/SQL/HTML contexts. Prevent path traversal and secret emission. Validate generated permissions, network endpoints and credentials references. Templates are code and require review/security tests.

**Control runtime libraries and adapters.** Generated code often delegates semantics to runtime frameworks. Pin versions and verify scheduling, numeric types, overflow, concurrency, memory, error handling and platform bindings. Generator correctness does not cover a defective runtime or handwritten integration adapter.

**Test the transformation engine.** Positive fixtures cover each mapping. Negative fixtures must be rejected or diagnosed. Boundary fixtures cover empty/single/maximal/recursive structures, Unicode, reserved words, collisions and large models. Metamorphic tests check rename/order invariance. Mutation tests seed mapping defects. Differential tests compare independent implementations or interpreters where possible.

**Test semantic correspondence.** Run the same stimulus/property against executable source semantics/reference interpreter and generated target when meaningful. Compare state/output/timing under declared abstraction. Use property checking or proof for high-consequence transformations where feasible. Matching examples does not prove all behaviors.

**Verify target artifacts independently.** Parse/type-check/compile, lint/static-analyze, test target units and contracts, scan dependencies/secrets/vulnerabilities, measure timing/resource use and test integration/faults. Generated code follows the same product standards as handwritten code unless a qualified process explicitly supplies equivalent evidence.

**Qualify tools by use.** Define tool function, failure modes, whether failures can introduce/omit errors, detection by downstream activities and required confidence. Qualification evidence is version/configuration/platform/scope-specific. Reassess on tool/template/library changes. A vendor certificate outside the use case is background, not project acceptance.

**Make builds reproducible.** Pin source commit, transformation repository, dependency lockfiles, container/compiler/runtime, configuration and environment. Capture commands, logs, diagnostics, traces, outputs and digests. Rebuild independently and compare semantic/byte outputs. Preserve tool availability or emulation/migration strategy for long-lived systems.

**Review generated diffs causally.** Link target changes to source/rule/library changes. Flag unexplained churn and unexpectedly unchanged outputs. Large formatting churn hides semantic changes; separate formatter upgrades. Review high-consequence generated regions through model views and target artifacts as appropriate.

**Govern failures atomically.** Generate into isolated staging, validate completely, then promote as one configuration. Never leave partial targets mixed with the previous baseline. Keep last accepted outputs and recovery procedure. Diagnostics must distinguish source defect, unsupported mapping, tool crash, target build failure and test failure.

**Monitor deployed behavior.** Compare runtime/configuration telemetry and discrepancies with model assumptions. Generated code can drift through platform, configuration, dependency and environmental change even if source remains fixed. Feed discrepancies to model, transformation and validation owners; do not patch deployed generated files without controlled emergency/change recovery.

The following synthetic generator validates a declared transition table, generates deterministic Python text, checks required emitted structures, records source-to-line traces and compares four behaviors through the transformed target table. It does not parse, compile or execute the emitted code, parse SysML or implement complete state-machine semantics.

<!-- bijux-verify: {"id":"state-transform-codegen-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"source_states=3\nsource_transitions=4\ngenerated_lines=11\ntrace_entries=4\ndeterministic=1\ngenerated_structure_valid=1\nreachable_states=3\ninvalid_targets=0\nacceptance_cases=4\nacceptance_passed=4\nstatus=declared_transform_fixture_passed\nevidence=synthetic_subset_only\n","stderr":""}} -->
```python
states = {"IDLE", "RUNNING", "FAULT"}
transitions = [
    ("IDLE", "start", "RUNNING"),
    ("RUNNING", "stop", "IDLE"),
    ("RUNNING", "fail", "FAULT"),
    ("FAULT", "reset", "IDLE"),
]

def generate(rows):
    lines = ["def next_state(state, event):", "    transitions = {"]
    trace = {}
    for source, event, target in sorted(rows):
        lines.append(f"        ({source!r}, {event!r}): {target!r},")
        trace[(source, event, target)] = len(lines)
    lines.extend([
        "    }",
        "    key = (state, event)",
        "    if key not in transitions:",
        "        raise ValueError(f'unsupported transition: {key}')",
        "    return transitions[key]",
    ])
    return "\n".join(lines) + "\n", trace

invalid_targets = sum(source not in states or target not in states for source, _, target in transitions)
generated, trace = generate(transitions)
regenerated, _ = generate(list(reversed(transitions)))
generated_structure_valid = int(
    generated.startswith("def next_state(state, event):\n    transitions = {\n")
    and generated.endswith("    return transitions[key]\n")
    and all(repr((s, e)) in generated and repr(t) in generated for s, e, t in transitions)
)

cases = {(s, e): t for s, e, t in transitions}
target_table = {(s, e): t for s, e, t in sorted(transitions)}
passed = sum(target_table[(s, e)] == t for (s, e), t in cases.items())
reachable = {"IDLE"}
changed = True
while changed:
    before = len(reachable)
    reachable |= {t for s, _, t in transitions if s in reachable}
    changed = len(reachable) != before

print(f"source_states={len(states)}")
print(f"source_transitions={len(transitions)}")
print(f"generated_lines={len(generated.splitlines())}")
print(f"trace_entries={len(trace)}")
print(f"deterministic={int(generated == regenerated)}")
print(f"generated_structure_valid={generated_structure_valid}")
print(f"reachable_states={len(reachable)}")
print(f"invalid_targets={invalid_targets}")
print(f"acceptance_cases={len(cases)}")
print(f"acceptance_passed={passed}")
print("status=" + ("declared_transform_fixture_passed" if invalid_targets == 0 and generated_structure_valid and len(reachable) == len(states) and passed == len(cases) else "declared_transform_fixture_failed"))
print("evidence=synthetic_subset_only")
```

The structural string check does not establish target-language syntax and does not compile or execute the emitted function. The target table has no concurrency, time, entry/exit actions, guards, hierarchy or platform effects. Four examples cannot establish semantic preservation beyond this finite declared mapping.

## Definitions and Notation

Let transformation run record be

\[
g=(sourceDigest,sourceMM,rules,generator,libraries,environment,targetDigest,trace,diagnostics,time).
\]

Let trace relation $\tau\subseteq E_s\times Rule\times E_t$ support many-to-many mappings. Trace completeness for in-scope source element $s$ means:

\[
mapped(s)\lor omittedWithApproval(s)\lor externalized(s)\lor unresolved(s).
\]

Unresolved is visible failure/unknown according to criticality, never implicit success.

For full generator $G$ and incremental generator $G_\Delta$, an important regression property is semantic equivalence after change $\Delta$:

\[
G(M_s\oplus\Delta)\equiv G_\Delta(G(M_s),\Delta,\tau).
\]

Test it periodically with clean regeneration. Equality may be byte equality or a declared normalized semantic comparison; state which.

## Mechanisms, Invariants, or Proof Structure

**Commuting evidence.** Where an executable source interpretation $I_s$, generated target $G$, target execution $I_t$ and abstraction $\alpha$ exist, desired correspondence is

\[
\alpha(I_s(M_s,x))=I_t(G(M_s),x)
\]

for inputs/domain $x$ under assumptions. Finite differential tests sample this relation; formal proof requires complete semantics and proof obligations.

**Trace invariant.** Every promoted target region has one reproducible derivation or declared handwritten authority. Every high-consequence source element has target/loss disposition. Trace refers to stable identities and versions.

**Determinism invariant.** Reordered semantically identical inputs, fixed environment and repeated execution do not change governed output. Metamorphic tests challenge traversal-order, locale and rename assumptions.

**Regeneration invariant.** Accepted output is reproducible without manual reconstruction. If manual modifications exist, their protected extension source is controlled and round-trip merge is tested.

**Failure invariant.** A failed run cannot promote partial output. Diagnostics and old accepted baseline remain available. Unsupported semantics cannot be downgraded to warnings without authority.

No generic proof establishes all transformation correctness. Evidence is composed from source validation, rule review, fixtures, trace/loss coverage, semantic correspondence, target verification and system validation.

## Alternatives and Trade-Offs

**Full versus incremental regeneration.** Full builds are simpler and expose deletions; incremental builds reduce latency but depend on complete traces/dependencies. Use periodic clean equivalence checks when incremental.

**Declarative versus imperative rules.** Declarative relations can expose intent and support bidirectionality; imperative control can handle complex target construction predictably. Either can hide order/conflict if implementation semantics are unclear.

**Generated output stored versus build-derived.** Not storing avoids stale diffs; storing supports audit, consumers without generators and long-term builds. Decide by reproducibility, review, licensing and archival constraints, then enforce clean-generation checks.

**Protected regions versus adapters.** Protected regions seem convenient but complicate merges and authority. Separate handwritten adapters/interfaces are usually clearer; protected regions need structural parsing and tests when unavoidable.

**Generic versus domain-specific generators.** Generic tools broaden reuse; domain-specific generators can enforce stronger semantics. Domain specialization raises maintenance, qualification and vendor-lock risks.

**Tool qualification versus output verification.** Qualification can reduce repeated low-level review within scope. Output/integration verification catches misuse, model defects and external dependencies. Risk usually requires both in proportion.

## Failure Modes and Misconceptions

**“It compiles, so the transformation is correct.”** Compilation checks target syntax/types, not source intent, omitted constraints or behavior equivalence.

**“Generated code needs less testing.”** Automation changes defect origin. Verify generator use/output and apply product standards.

**“A trace proves equivalence.”** It proves a recorded correspondence. Check semantic properties and target behavior.

**“Round trip keeps everything synchronized.”** Authority and conflicts remain. Define directional ownership and loss.

**“Protected regions solve manual integration.”** They can lose edits or create forks. Prefer typed extension points and test regeneration.

**“Deterministic source guarantees deterministic output.”** Traversal order, environment, plugins, time, locale and dependencies can vary.

**“Incremental generation is just faster full generation.”** It adds dependency and deletion correctness obligations.

**“The generator handles unsupported features.”** Demand an explicit coverage/loss report; silent omission is failure.

**“Vendor qualification covers our use.”** Confirm version, configuration, platform, feature subset and assurance regime.

**“The model is the only source needed long term.”** Preserve generator, rules, libraries, build environment, trace, target contracts and evidence.

## Worked Examples

### Example 1

**Requirement export.** A transformation produces a supplier table. Stable IDs and source commit accompany text; unsupported formal constraints fail the export. Supplier edits return through an owned change workflow rather than overwriting the model from a spreadsheet.

### Example 2

**Unit loss.** A target schema stores numbers but no quantity kind. Generation of 12 kW becomes `12`. Coverage analysis flags semantic loss; the adapter adds canonical units and schema metadata before promotion.

### Example 3

**Rule-order nondeterminism.** Two templates match specialized ports. Different plugin load order changes generated protocol code. Explicit most-specific dispatch and overlapping-rule negative tests restore determinism.

### Example 4

**Rename stability.** Target IDs were based on names, so renaming `mainPump` deleted/recreated deployment resources. Source-ID-derived target identity and trace-aware name update prevent destructive churn.

### Example 5

**Stale incremental output.** Removing a source state leaves generated handlers because deletion dependencies were absent. Clean-build comparison detects the orphan; deletion/tombstone rules and periodic full regeneration are added.

### Example 6

**Protected-region loss.** A manual retry patch inside generated code disappears. The team restores from history, moves policy to a handwritten adapter/configured model extension and blocks direct edits with a regeneration check.

### Example 7

**Injection boundary.** A model description containing quotes/newlines enters generated YAML and changes structure. Grammar-aware serialization, schema validation and adversarial strings replace concatenation.

### Example 8

**Golden-output trap.** A formatting change breaks thousands of byte comparisons though semantics remain. Tests separate normalized semantic assertions from a small intentional formatting contract; unexplained semantic diffs still block.

### Example 9

**Runtime mismatch.** Generated controller code matches transition cases, but target integer overflow changes timer behavior. Target-platform numeric and timing tests reveal what source simulation missed.

### Example 10

**Generator upgrade.** A new version optimizes condition ordering. Fixture, mutation, differential, static, timing and system regressions reveal a short-circuit side-effect change. Upgrade pauses while the accepted old toolchain remains reproducible.

## Cross-Program Connections

**Platform engineering.** Scaffolders, policy/config generators and deployment templates need deterministic builds, extension boundaries, provenance and regeneration checks.

**API and service engineering.** OpenAPI/client/server generation must preserve contract semantics, escaping, version compatibility and handwritten business boundaries.

**Data engineering.** Schema/ETL generation requires lineage, nullability/unit/precision preservation, idempotency and backfill validation.

**Object-oriented programming.** Generated classes need stable identity, encapsulation boundaries and composition/inheritance semantics that match the domain rather than template convenience.

**Functional programming.** Pure transformations, immutable inputs and property/metamorphic tests strengthen reproducibility; target effects and runtime semantics remain explicit.

## References

1. Object Management Group, *SysML v1 to SysML v2 Transformation*, formal/2026-03-03. <https://www.omg.org/spec/SysML/2.0/Transformation/PDF>
2. Object Management Group, *OMG Systems Modeling Language, Version 2.0, Part 1: Language Specification*. <https://www.omg.org/spec/SysML/2.0/Language/PDF>
3. Object Management Group, *Kernel Modeling Language, Version 1.0*. <https://www.omg.org/spec/KerML/1.0/PDF>
4. Object Management Group, *Systems Modeling API and Services, Version 1.0*. <https://www.omg.org/spec/SystemsModelingAPI/1.0/PDF>
5. Object Management Group, *About the MOF Query/View/Transformation Specification Version 1.3*. <https://www.omg.org/spec/QVT/1.3>
6. Object Management Group, *MOF Query/View/Transformation, Version 1.3*. <https://www.omg.org/spec/QVT/1.3/PDF>
7. Object Management Group, *About the MOF Model to Text Transformation Language Specification Version 1.0*. <https://www.omg.org/spec/MOFM2T/1.0>
8. Object Management Group, *MOF Model to Text Transformation Language, Version 1.0*. <https://www.omg.org/spec/MOFM2T/1.0/PDF>
9. NASA, *Software Engineering and Assurance Handbook, SWE-146: Auto-generated Source Code*, current Version D. <https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695503/SWE-146%2B-%2BAuto-generated%2BSource%2BCode>
10. NASA, *Software Engineering and Assurance Handbook, SWE-206: Auto-Generation Software Inputs*, current Version D. <https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695540/SWE-206%2B-%2BAuto-Generation%2BSoftware%2BInputs>

## Exercises

### Exercise 1

Design a model-to-code pipeline for a safety-relevant controller, including contracts, traces, fixtures, target tests and tool evidence.

### Exercise 2

Audit a generator that compiles successfully but has nondeterministic diffs, warnings for unsupported constructs, protected manual edits and no controlled runtime.

### Exercise 3

Specify an incremental requirements-to-test transformation with correct update/delete behavior and clean-build equivalence evidence.

### Exercise 4

Plan a SysML v1-to-v2 transformation acceptance campaign for a repository with profiles, scripts, diagrams and external integrations.

### Exercise 5

A code-generator upgrade changes 30 percent of target files but all unit tests pass. Define investigation and release decision evidence.

## Answers to the Exercises

### Answer 1

Define allowed controller subset and target/platform use, safety integrity/consequence, timing/resource constraints and authority. Pin source model/metamodel/libraries, generator/rules/templates, runtime/adapters, compiler/build environment. Source preconditions cover unique identity, typed/configured states/events/transitions, deterministic guards/priorities, initial/safe/failure states, units/timing and requirement/hazard trace. Unsupported constructs block.

Normalize into a reviewed intermediate representation exposing event ordering, numeric types, scheduling, defaults and platform decisions. Define each mapping, stable target identity, source-target trace, postconditions and loss policy. Generate to isolated staging deterministically with fixed ordering/locale/encoding. Separate generated modules from handwritten hardware/runtime adapters; forbid direct edits.

Test generator with positive mapping coverage; negative malformed/unsupported models; boundary empty/deep/large/state collisions; metamorphic reorder/rename; mutations in guards/targets/timers; and differential execution against a qualified reference interpreter. Track source IDs/rules to target functions and test cases. Periodically independently reproduce digests.

Compile and static-analyze under target toolchain; test MC/DC or other mandated coverage where applicable, numeric overflow, timing/deadlines, concurrency, memory, initialization, fault/recovery, invalid events and adapter failures. Run hardware/software-in-loop and integrated system V&V against requirements/hazards. Qualify/accredit generator only for exact use/version or retain full output verification. Preserve diagnostics, traces, reports, limitations, discrepancies and technical-authority approval; reopen on any chain change.

### Answer 2

Freeze source, outputs and full environment. Nondeterminism means review/reproducibility fails even if compilation passes. Re-run in clean environments and vary source enumeration, locale, timezone, machine and plugin order. Find timestamps/random IDs, hash iteration, parallel race, unpinned dependencies or formatter drift. Define stable ordering/IDs and isolate approved volatile metadata.

Inventory every warning by source identity, semantic consequence and configuration. Unsupported constructs must block, map to approved external/extension representation or have explicit loss acceptance; a warning count alone is not disposition. Seed fixtures to ensure future instances are detected.

Diff manual edits against clean regenerated output. Recover them, determine authority and move them into model, transformation or stable handwritten adapter. If protected regions remain, use structural merge, ownership and regeneration tests; do not rely on comment delimiters alone.

Identify runtime/library/compiler/platform versions and semantics: numeric types, scheduling, errors, concurrency, resources and security. Pin and verify them. Rebuild traces and target tests, run static/security/integration/system evidence, and compare source/reference behavior. Until deterministic generation, loss disposition, manual authority and runtime control are restored, compilation is only a narrow pass and the output is not release-ready.

### Answer 3

Define source requirement identities/status/configuration and target test-spec identities, generated versus manual fields and authoritative direction. Map requirement subject/constraints, acceptance criteria, method, configuration and evidence placeholders into target schema. Trace each source property/rule to target fields; manual procedure/results live in separate owned records or typed extension points.

Build dependencies for direct fields, referenced definitions, inherited constraints, configuration filters, ordering and negative queries such as “requirements without tests.” Handle add, property update, rename/move, supersession and delete explicitly. Deletion may remove an unexecuted derived spec but must archive/detach executed evidence under retention policy rather than erase history.

Test sequential change scripts against a clean full transform after every operation. Normalize only declared volatile fields and require semantic equality, no orphan targets, trace completeness and deterministic order. Add property/metamorphic tests for source reorder/rename and mutation tests for missing dependency/deletion propagation. Periodically force full rebuild in CI.

Promote atomically after target schema validation, coverage queries, generated/manual boundary checks and review. Return unknown/block on partial source retrieval, unsupported requirement semantics or stale trace. Version source commit, rules/engine, output and trace. A generated test spec establishes planning continuity, not that a test was correctly executed or a requirement passed.

### Answer 4

Freeze v1 repository/tool/profile versions and target formal SysML 2.0, KerML, libraries, transformation implementation and target tool/API. Inventory standard elements plus profiles/stereotypes/tag values, opaque expressions, instance usage, units, diagrams/tables, IDs, scripts, validation rules, reports and integrations. Rank by consequence and frequency.

Create mapping/coverage register tied to normative transformation rules: source construct/property, target semantics, identity/trace, expected loss/default, validation method and owner. Build representative and adversarial fixtures before bulk transformation. Require invalid input rejection and explicit unmapped diagnostics. Preserve immutable v1 source and run logs.

Execute into controlled target branches. Compare identities/inventories and semantic graph projections, not pictures or element counts. Review definition/usage, feature relations, behavior, requirement/case, view and metadata semantics. Recompute golden analyses; regenerate reports; exercise API queries and downstream integrations; round-trip only where intended. Domain owners resolve custom profiles/scripts and accept intentional change/loss.

Test transformation determinism, source-target trace completeness and tool interoperability. Sample high-consequence chains requirement-to-design-to-analysis-to-verification. Record unresolved/retained legacy links. Target becomes authority only after configuration, domain, tool and decision approval; keep v1 accessible for audit/rollback until obligations permit retirement.

### Answer 5

Freeze old/new generators, templates, dependencies, source commit, build/runtime and both target trees. Classify churn by formatting, ordering, naming/identity, API/signature, control/data flow, numeric/runtime or diagnostic behavior. Remove intentional formatter-only noise through normalized comparison but retain byte-reproducibility expectations.

Read change records, then independently map every changed region to generator/rule/library source. Unexplained changed or unexpectedly unchanged high-consequence outputs block. Compare trace coverage and loss diagnostics. Run clean repeat builds and metamorphic reorder/locale/platform cases.

Replay positive/negative/boundary/mutation/reference fixtures and differential source-versus-target behaviors. Expand beyond unit tests to compilation warnings, static/security analysis, coding/coverage rules, ABI/API, runtime adapters, numeric overflow/precision, timing/resources, concurrency, faults and integrated system/hardware-in-loop scenarios. Unit tests may miss generator common-mode errors because expected results share generated assumptions.

Perform impact analysis to requirements, hazards, interfaces, verification evidence and certifications. Requalify tool use where version change invalidates evidence. Release only after causal explanation, required regressions, discrepancy closure/waiver and technical authority acceptance. Otherwise keep the reproducible old version or block. Preserve comparison/evidence and monitor deployment; “tests green” is necessary evidence, not a decision by itself.
