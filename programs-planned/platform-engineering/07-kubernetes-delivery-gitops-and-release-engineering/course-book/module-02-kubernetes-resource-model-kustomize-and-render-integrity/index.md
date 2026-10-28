# Module 2 — Kubernetes Resource Model, Kustomize, and render integrity

## Central question

**How can one reusable configuration produce environment-specific desired state without making the rendered result surprising, unreviewable, or unstable?**

Git stores source. Kubernetes consumes objects. Between them sits a renderer. That renderer is part of the release system and must be treated with the same rigor as a compiler.

## Configuration is a program even when it is YAML

A directory of Kubernetes manifests can contain imports, generators, substitutions, patches, name transforms, label transforms, remote bases, plugins, and post-renderers. The output may depend on tool version, file order, environment variables, network content, and default schemas. Calling the inputs “just YAML” hides the computation.

A release record therefore needs:

- renderer name and version;
- root source revision;
- all remote source identities;
- environment inputs;
- plugin identities;
- canonical rendered objects;
- render digest;
- warnings and deprecated API findings.

The object submitted to the API server is the release subject for reconciliation, not the human-friendly template alone.

## Kubernetes resource identity

Kustomize and other KRM tools operate on Kubernetes-style identities. A resource is not identified by filename. Atlas uses:

```text
API group
kind
namespace
name
```

For core resources, the group is empty. Resource version is not part of logical identity; it changes as APIs evolve. Two files producing the same identity are a conflict unless the renderer has an explicit merge rule.

Identity stability matters because patches, inventories, ownership, and prune decisions refer to it. A patch that accidentally changes a selector or name can create a second workload rather than update the intended one.

## Base and overlay are responsibility boundaries

A base should express behavior shared by all environments: ports, probes, security context, stable labels, workload shape, and required services. An overlay should express a legitimate environmental difference: replica scale, resource class, hostnames, external references, or feature enablement.

An overlay should not silently repair a defective base. If production requires a different security context because the base runs as root, the base is wrong. If every overlay repeats the same patch, the concern belongs in the base or a reusable component.

Atlas uses:

```text
apps/atlas/base
apps/atlas/overlays/dev
apps/atlas/overlays/staging
apps/atlas/overlays/prod
```

The production overlay is intentionally boring. It chooses environment identities and capacity without replacing selectors, container names, probe semantics, security constraints, or storage authority.

## Patch semantics

A patch is meaningful only relative to a schema and target. Strategic merge behavior historically used Kubernetes merge metadata; JSON Patch uses ordered path operations; JSON merge patch replaces arrays rather than merging them intelligently. Kustomize supports several patch forms, but the engineer must understand the resulting object rather than memorize syntax.

Consider a Deployment with two containers. A naive merge patch that replaces the container array can delete the sidecar. A JSON Patch that targets `/spec/template/spec/containers/0/image` assumes stable ordering. A named merge can target the correct container when schema information is available. The safe choice depends on the object schema and the invariants being changed.

The capstone renderer validates that an overlay may change only approved field paths. Production cannot modify workload selectors or security context without a separate policy review.

## Transformers have wide blast radius

Name prefixes, suffixes, common labels, namespaces, image transforms, and replacements can touch many resources. Their convenience is proportional to the need for render evidence.

A common label transform may modify a Deployment selector as well as Pod labels. If applied inconsistently, the Deployment becomes invalid or stops selecting existing Pods. Namespace transforms can move namespaced resources while leaving cluster-scoped references unchanged. Name prefixes can break strings embedded in CRD fields that the renderer does not understand.

Atlas treats every transformer as a typed operation with a declared target set. The render proof lists all identities before and after transformation.

## Generated ConfigMaps and Secrets

Kustomize generators can derive names from content hashes, which is useful for rollout identity. The generated object and every reference to it must change together. Disabling the hash suffix may simplify names but removes an automatic change signal.

Generated Secret content still exists in the rendered output. Base64 is not encryption. Course 7 uses generators for non-sensitive configuration and external secret references for sensitive values. Module 7 examines the trust boundary in depth.

## Remote bases and reproducibility

A remote base referenced by a branch or mutable tag makes the consuming render non-reproducible. Even a commit reference is insufficient if the fetch is unauthenticated or if submodules and dependencies are not pinned.

The strongest release lane vendors or resolves remote content into an immutable source artifact with a digest. At minimum, record the exact remote commit and verify it during render. Network access during a production render should be considered a dependency with availability and supply-chain implications.

## Deterministic canonicalization

YAML permits comments, anchors, multiple scalar spellings, and map ordering. A render digest should not change because a comment moved or keys were reordered. Atlas parses each resource, rejects duplicate keys, normalizes scalar types, removes fields outside the desired-state subject such as `status`, sorts resources by logical identity, emits canonical JSON, and hashes the resulting sequence.

Canonicalization must not erase meaningful distinctions. The string `"1"` is not the number `1`. An absent field is not always equivalent to an explicit default because API-version changes can alter defaulting. Atlas preserves explicit input semantics and records the Kubernetes schema profile used for normalization.

## Server-Side Apply and field ownership

Rendering answers what Atlas wants. Server-Side Apply helps define which fields Atlas owns. The field manager must remain stable across reconciliations. Changing the manager name can create apparent conflicts or transfer ownership unexpectedly.

A delivery system should not force conflicts globally. Forced ownership transfer is a migration with a reviewable field set. For example, moving replica ownership from a human-managed Deployment to a GitOps application may be intentional. Forcing ownership of an operator-managed status or injected sidecar is not.

The semantic capstone records owned field paths with each resource. Drift comparison ignores status and preserves declared external managers.

## Render review as an engineering practice

Reviewing only source diffs is insufficient when a small source change produces a large render change. A high-quality pull request includes:

- source diff;
- rendered object diff;
- identity additions and removals;
- API-version changes;
- protected-resource changes;
- image and chart digest changes;
- field-ownership changes;
- policy results;
- render digest.

Reviewers should be able to answer “What will the controller try to create, modify, and delete?” without running the tool locally.

## Failure patterns

### Environment fork

Copying full manifests into each environment makes immediate edits easy and long-term convergence difficult. Security fixes and probe changes land unevenly. The copies become separate products without explicit versioning.

### Overlay as patch pile

An overlay with dozens of patches becomes a hidden fork. It should be refactored into a clearer base, component, or distinct application if the behavioral differences are real.

### Mutable remote source

A remote base at a branch produces a new render without a local commit. Review and rollback identities become incomplete.

### Renderer-version drift

Two environments use different Kustomize versions and produce different output from the same source. Tool version must be part of render identity.

### Hidden substitution

Environment-variable substitution in CI changes output but is absent from Git review. Every variable input must be declared and included in the digest.

## Atlas render contract

Atlas Delivery Plane adopts these rules:

1. production desired state is rendered without unrecorded network input;
2. all remote sources and renderer versions are immutable identities;
3. duplicate resource identities and duplicate YAML keys fail the render;
4. overlays may change only declared environment-owned fields;
5. protected-resource deletion is visible before reconciliation;
6. canonical rendered sets produce deterministic digests;
7. source and rendered diffs are both review artifacts;
8. field ownership is explicit and force-conflict is never the default.

Module 3 introduces Helm, where the configuration surface is an explicit chart API and the rendering language is more powerful—and therefore easier to misuse.

## Deep-dive practicum

### Rendering is compilation, not text concatenation

A Kubernetes release renderer has source files, dependency resolution, transformation rules, versioned implementation behavior, and output semantics. That is a compiler-shaped system. Treating it as text substitution misses failures such as type coercion, list replacement, name-reference rewriting, remote-base movement, and API defaulting.

Consider a base Deployment with two containers and an overlay patch that supplies one container named `api`. A strategic merge may merge by the container merge key; a JSON merge patch replaces the complete list; a JSON Patch edits a position; Server-Side Apply later reasons about structured field ownership. The same visible YAML fragment can therefore have different meaning depending on patch mechanism. A review that shows only the patch is incomplete. The reviewer needs the rendered object and the transformation semantics.

### Canonical identity and duplicate objects

The Atlas renderer identifies a resource by API group, kind, namespace, and name. Two inputs producing the same identity are not harmless duplicates. Their precedence can depend on file order or renderer behavior, making the release non-local and difficult to audit. Course 7 rejects duplicate identities before digesting the set.

The canonical digest removes server-owned status and metadata, sorts by resource identity, preserves scalar types, and serializes deterministically. It does not remove arbitrary defaults. If one renderer writes `replicas: 1` and another omits the field, the desired sets differ even if the API server later defaults both to one. This is deliberate: the repository’s declared ownership differs.

### Remote bases and supply-chain reach

A remote Kustomize base extends the release supply chain. Pinning a Git commit prevents branch movement but does not by itself guarantee availability, repository integrity, or retention. A mature release record binds the remote commit, repository identity, renderer version, and—where possible—the fetched content digest. Production builds should not require an unbounded live fetch from a mutable third party.

A useful review question is: could two isolated reviewers with only the recorded inputs render the same set? If not, the release does not have a reproducible desired state.

### What native validation contributes

The course’s semantic renderer deliberately supports the transformations used by Atlas. Native Kustomize remains necessary because the complete field specification, generators, OpenAPI merge metadata, plugins, and name-reference behavior exceed a teaching model. Independent proof should include:

- native `kustomize build` with the pinned binary;
- duplicate-identity and policy checks over the output;
- schema validation against the target Kubernetes version and installed CRDs;
- a second isolated render to compare canonical digests;
- admission dry-run or bounded cluster evidence for server-side defaults and policy.

Passing only the semantic lane demonstrates the invariant. It does not certify every Kustomize feature.

### Review exercise: a one-line patch with four possible failures

Suppose production changes `replicas: 3` to `replicas: 5`. Ask four questions before calling it low risk:

1. Does an autoscaler or another manager own `/spec/replicas`?
2. Does the patch target the intended suffixed name and namespace after transformation?
3. Does the environment have capacity and disruption headroom?
4. Will the controller’s diff policy expose or hide a conflict?

The visible change is one line; the authority and runtime implications are not.
