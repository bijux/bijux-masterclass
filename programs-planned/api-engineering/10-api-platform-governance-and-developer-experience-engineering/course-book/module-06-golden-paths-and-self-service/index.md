# Module 06 — Golden Paths, Templates, and Self-Service Provisioning

> **Program stage:** Course 10 of 10 — Operate APIs as an organizational platform.

> **Central question:** How can a platform reduce repeated setup work without hiding essential engineering decisions or creating clone-and-forget debt?

## Where this module fits

Module 05 produced **Publish the lifecycle policy, consumer inventory, deprecation impact report, and retirement decision**. This module extends that result by asking: **How can a platform reduce repeated setup work without hiding essential engineering decisions or creating clone-and-forget debt?**

The new capstone increment is **Publish and verify the `api-capability-v1` golden path and generated reference fixture**. It becomes the prerequisite for **Documentation, Discovery, Sandboxes, and Consumer Onboarding**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Design a golden path as a maintained product.
- Choose safe defaults and essential parameters.
- Render deterministically and atomically.
- Include ownership, tests, docs, and governance hooks.
- Govern upgrades and supported escape hatches.

## Capstone increment

Publish and verify the `api-capability-v1` golden path and generated reference fixture.

## Golden paths reduce repeated risk

A golden path is the easiest supported route from an idea to a trustworthy release. It provides a maintained project shape, contract location, owner metadata, documentation skeleton, tests, policy hooks, and publication workflow. It does not decide the business domain or erase protocol choice.

The capstone template accepts API name, title, owner, protocol, and system. These parameters represent essential context. It does not ask the learner to choose among fifteen linters, five CI layouts, or arbitrary folder names; those choices are the repeated accidental work the platform is meant to remove.

## Template as a product

A template needs its own owner, version, changelog, support policy, compatibility promise, and usage inventory. Teams generated from version 1.0 still exist when the template reaches 1.4. The platform must explain whether an update is required, optional, or irrelevant. A template without an upgrade story transfers maintenance debt to every consumer.

## Safe generation pipeline

Validate every parameter before writing. Render into a temporary directory. Reject unresolved placeholders, unsafe names, path traversal, embedded credentials, and output sets that do not match the template contract. Run generated tests and policy checks. Only then publish the result. Partial generation leaves ambiguous ownership and can expose secrets or malformed metadata.

## Defaults and escape hatches

Defaults should encode evidence: supported contract versions, safe authentication boundaries, standard documentation shape, known observability hooks, and maintained build paths. An escape hatch is appropriate when a team has a real requirement the golden path cannot meet. The exception must name who supports the alternative and what equivalent evidence replaces the paved road.

A platform that forbids all variation becomes a central architecture team. A platform that supports every variation becomes an unmaintainable catalog of choices. The product decision is to support a small set of high-value paths and make unsupported choices visible.

## Generated ownership and policy hooks

The scaffold emits `catalog-info.yaml`, a contract stub, quickstart, API metadata, and a contract-presence test. It begins in `proposed`, not `active`. Generation creates a credible starting point; it does not grant release status. The owner must replace the stub, define semantics, and collect evidence through the lifecycle.

## Determinism and provenance

Record template version, parameters, source digest, and rendered manifest. Deterministic generation makes review and regeneration possible. It also allows the platform to identify which projects are affected by a template defect. This is the beginning of template supply-chain management, not merely convenience.

## Worked rejection

A proposed template includes a sample bearer token so the quickstart works immediately. The platform rejects it. A sandbox credential must be issued per session and expire; a copied token has no lifecycle or audience control. Convenience cannot override the security guarantees established in Course 3.

## Implementation review

The Python renderer validates patterns and enumerations, creates only declared outputs, rejects unresolved placeholders, and scans rendered text for secret-like assignments. The TypeScript core demonstrates the same parameter and text rules. The final generated fixture is compared by manifest rather than by visual inspection.

## Standards anchor

Backstage Software Templates demonstrate a practical scaffolding model: a versioned template declares parameters and executes actions to create components. The course adopts the self-service idea while keeping the golden-path contract explicit. See [Software Templates](https://backstage.io/docs/features/software-templates/) and [writing templates](https://backstage.io/docs/features/software-templates/writing-templates/).

## The golden-path contract

Treat a template release as an API. Its inputs, outputs, defaults, failure modes,
and support promise form a contract. Validate backward compatibility for
parameters and generated structure. Removing a parameter or changing a default
can break automation even if the template still renders.

The `api-capability-v1` output contract contains exactly six files. A production
path would include more, but exactness is educationally useful: unexpected files
or missing hooks fail the build. Consumers can rely on the baseline while adding
domain code outside platform-owned sections.

## Self-service is not self-approval

Self-service means a user can initiate and complete routine platform work without
waiting for manual platform intervention. It does not mean bypassing ownership,
security, compatibility, or lifecycle requirements. A generated proposed API can
enter automated checks immediately; active publication still requires evidence.

Design workflow states so the user always knows what is automated, what evidence
is missing, and who must review. A hidden manual queue behind a “Create” button is
not self-service.

## Template boundaries

Split generated content into:

- **platform-owned baseline:** CI hooks, metadata schema, evidence wiring;
- **owner-owned domain content:** contract semantics, examples, documentation;
- **shared extension points:** supported configuration with validation.

This makes upgrades possible. If teams freely edit every generated file, the
platform cannot apply fixes. If platform automation overwrites domain content,
it violates ownership. Mark managed regions or provide codemods and migrations
rather than blind regeneration.

## Upgrading generated projects

Maintain a generation receipt with template ID, version, parameters, and file
digests. An upgrade tool can classify files as unchanged, owner-modified, or
platform-obsolete. Apply safe changes automatically, propose merges for
conflicts, and record declined upgrades. Security-critical changes can become
policy blockers after a notice period.

Do not require all projects to regenerate from scratch. That destroys history and
custom work. Upgrade is a migration across template contracts.

## Template testing pyramid

Test at several levels:

1. Parameter schema and validation.
2. Deterministic rendering and secret scan.
3. Generated project unit and contract tests.
4. Policy and catalog ingestion.
5. Build and package generation.
6. Optional deployment and sandbox smoke test.

A template can render perfectly and still create a project that fails on first
build. The generated fixture in the course is evidence for the complete local
path.

## Paved-road portfolio

Avoid one template per team or framework permutation. Organize paths by meaningful
product boundary: public HTTP API, event consumer, internal RPC service, graph
extension, or API documentation package. If two templates differ only in naming,
consolidate. If they have different security or operational ownership, keep the
difference explicit.

## Adoption and support

Track generated projects, template versions, upgrade state, first release time,
and support categories. A large number of old unupgraded projects signals that
the path is not maintainable. Survey owners about removed work, not only
satisfaction. The best path may be one teams rarely notice because it eliminates
routine failure.

## Generated-project ownership contract

The generated README should tell the new owner which files are theirs, which are
platform-managed, and which interfaces are stable extension points. Without this,
teams either fear editing anything or change critical wiring unknowingly.

A generation receipt can look like:

```json
{
  "template": "api-capability-v1",
  "version": "1.0.0",
  "parametersDigest": "...",
  "generatedFiles": {"catalog-info.yaml": "..."},
  "createdAt": "..."
}
```

Store it with the project. Upgrade tooling compares current files with these
baselines and a new template release.

## Self-service permissions

Do not give the scaffolder universal repository or cloud authority. Scope actions
to the requesting owner and target system. Validate repository names, groups,
environments, and requested resources. Require review for public exposure,
sensitive data, high-cost infrastructure, or unusual protocols.

A template action is code execution in a privileged control plane. Pin actions,
validate inputs, audit execution, and prevent templates from exfiltrating
secrets. A visually declarative YAML workflow can still be a supply-chain risk.

## Failure recovery

Generation can fail after repository creation but before catalog registration or
policy setup. Use idempotent actions and a workflow state record. Cleanup should
remove incomplete resources or clearly mark them for repair. Retrying must not
create duplicate repositories or credentials.

## Maintaining defaults

Review defaults using operational and support evidence. If most new APIs fail on
missing owner, make owner mandatory. If generated retry policy causes incidents,
fix the path and plan upgrades. If a framework version is unsupported, remove it
from new generation and publish a migration route for existing projects.

## Educational use of the template

In this course, the template stops at a proposed contract stub. This is deliberate.
A platform cannot generate domain semantics. The learner must write the contract
and explain its audience. The path automates everything around that essential
work, making the ownership boundary visible.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## Template contract

A golden path has an input contract, output contract, upgrade policy, support
owner, and tests. Course 10’s `api-capability-v1` requires a canonical API name,
title, owner, protocol, and system. It emits exactly six files: ownership
metadata, a contract location, quickstart, policy metadata, test, and README.
Exact outputs make review and regression possible. An open-ended generator that
quietly changes dozens of files is difficult to trust.

Validate inputs before writing. Write into an empty staging directory. Reject
unresolved placeholders and embedded credentials. Compare actual outputs with
the declared set. Run syntax and policy checks on the result. Only then publish
or copy it to the destination. A partially generated repository is a failure,
not a starting point the learner must repair manually.

## Defaults and decisions

Defaults should encode repeated, evidence-backed choices: canonical identifiers,
ownership metadata, docs structure, test hooks, and publication workflow. They
must not decide business semantics, data classification, authorization, or
service objectives. The generated contract stub explicitly tells the owner to
replace it. That incompleteness is honest; generating plausible domain schemas
would create false confidence.

Every default needs a reason and an escape route. If all APIs use a system field,
make it required. If most public APIs use OAuth but an internal mTLS interface is
valid, expose a deliberate protocol or security choice rather than forcing users
to delete generated middleware. Escape routes still preserve invariants such as
ownership and contract publication.

## Template evolution

Templates are products with consumers. Version their parameter and output
contracts. A new template version affects future repositories; existing
repositories do not magically upgrade. Provide a change report or migration tool
for important improvements, especially security and CI controls. Record which
repositories were generated from which version and which generated sections are
safe to update.

Avoid owning application code through continuous template overwrite. A better
pattern separates maintained reusable components, generated files with clear
ownership, and team-owned code. When the template changes a policy hook, the
platform can propose a patch and evidence; the domain team reviews changes that
affect its behavior.

## Self-service with accountability

Self-service means a user can complete a safe journey without waiting for a
central operator. It does not mean anonymous creation or absence of review. The
platform knows who requested the capability, who owns it, which policy applies,
and which evidence is still missing. Proposed and experimental states let teams
learn before an active release.

Measure successful generated products, time to first valid contract, and support
requests—not template invocation count. A template used hundreds of times to
create abandoned repositories is a cost. A template used less often but reducing
weeks of repeated setup may be valuable. Product evidence must follow the user
outcome.

## Implementation drill: exact template outputs

A safe renderer writes only declared files and fails on unresolved placeholders.

```python
from pathlib import Path


def render(source: Path, destination: Path, values: dict[str, str]) -> None:
    text = source.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    if "{{" in text or "}}" in text:
        raise ValueError("unresolved-placeholder")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
```

```typescript
function renderText(source: string, values: Record<string, string>): string {
  let result = source;
  for (const [key, value] of Object.entries(values)) {
    result = result.replaceAll(`{{${key}}}`, value);
  }
  if (result.includes("{{") || result.includes("}}")) {
    throw new Error("unresolved-placeholder");
  }
  return result;
}
```

The complete implementation adds parameter schemas, empty-destination checks,
secret detection, and an exact output-set comparison. Those controls turn a
string replacement helper into a governed golden path.

## Module synthesis

You are ready to leave this module when you can **design a golden path as a maintained product, choose safe defaults and essential parameters, and render deterministically and atomically** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **the lab introduces its declared planted defect** and requiring the following oracle: **Valid generation is deterministic and complete. Invalid inputs fail before publication. Secret and output-contract defects fail. Version impact is explained from generated-consumer compatibility, not intuition.**

The cumulative platform now includes **Publish and verify the `api-capability-v1` golden path and generated reference fixture**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Documentation, Discovery, Sandboxes, and Consumer Onboarding](../module-07-documentation-discovery-and-sandbox/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
