# Reference — Module Interface and Review Guide

A reusable module is an API for infrastructure decisions. It should reduce the number of invalid compositions, preserve resource identity through evolution, and make ownership visible. Moving blocks into a directory is not sufficient.

## 1. Responsibility

State the module’s responsibility in one sentence:

> `atlas_network` owns the VPC address boundary, subnet roles, route-table associations, NAT profile, and S3 gateway endpoint for one environment network.

Then list what it deliberately does **not** own: account creation, workload security groups, DNS zones, transit attachment, or public edge policy.

Reject a module whose responsibility is “create some AWS resources.”

## 2. Owned objects and lifecycle

List every resource the module owns and which lifecycle decisions are internal. The caller should not unknowingly co-own a resource or change an internal address by reaching into implementation details.

For each durable object, state:

```text
stable resource address
replacement triggers
retention/deletion behavior
migration path
recovery owner
```

## 3. Inputs as authority boundaries

Classify inputs:

- required architectural choice;
- optional policy choice with a safe default;
- dependency identity passed from another owner;
- sensitive reference;
- immutable identity;
- derived value that should not be caller-controlled.

Prefer typed objects and semantic maps over parallel lists and positional indices.

Reject escape hatches such as:

```hcl
extra_policy_json = string
arbitrary_ingress = any
create_everything = bool
```

unless the module can validate and own the resulting behavior. An input that lets every caller disable encryption or widen network access transfers the platform’s policy responsibility to unreviewed call sites.

## 4. Validation and forbidden states

Use type constraints, variable validation, preconditions, postconditions, and check blocks to reject combinations such as:

- per-zone NAT without one public NAT subnet per private zone;
- public edge enabled without a certificate and sufficient subnets;
- unsupported architecture values;
- account IDs in the wrong format;
- data tier with a default internet route;
- target attachment enabled without a target.

Validation should produce a useful architectural error, not merely allow a later provider index or API failure.

## 5. Provider ownership

Reusable child modules declare required providers and aliases but do not configure provider credentials, regions, or accounts. The root owns provider configuration because the root owns the deployment target and authority.

Provider aliases must be explicit in the interface when a module legitimately works across accounts or regions. Hidden default-provider use in a multi-account root can create resources in the wrong account.

## 6. Outputs as stable contracts

Expose what callers need to compose another owned capability:

```text
VPC ID
subnet IDs by semantic key
subnet zone mapping
runtime role ARN
KMS key ARN
backup bucket ARN
```

Avoid dumping whole resource objects or every provider attribute. Large output surfaces couple callers to implementation details, expose sensitive values, and make refactoring difficult.

Ask for each output:

- Which caller needs it?
- Is the value stable across internal refactors?
- Does exposing it invite another owner to mutate or depend on internals?
- Could a narrower capability be published instead?

## 7. Composition shape

Prefer a flat root that makes dependencies visible:

```text
root
├── naming
├── network
├── identity
├── audit
└── workload (in another root, consuming a narrow foundation contract)
```

Deep module trees hide provider aliases, state addresses, and ownership. Some nesting is justified when the child is an implementation detail of one coherent abstraction, but it should not become an unreviewable private platform.

## 8. Compatibility and release

Classify changes:

| Change | Typical class |
|---|---|
| add optional output | additive |
| add optional input with safe default | additive/review |
| narrow validation | potentially breaking |
| change default NAT profile | breaking behavioral change |
| rename resource address | requires move mapping |
| change output type | breaking |
| change provider constraint | compatibility review |
| replace internal resource | operationally breaking even if interface stable |

A module release includes state-address migration, operational impact, and caller upgrade evidence—not only a version tag.

Retain `moved` declarations long enough for every supported caller path to cross the migration. Removing them immediately after one environment upgrades breaks later consumers.

## 9. Testing ladder

A strong module has evidence at several levels:

1. **Static** — formatting, parsing, types, lint, policy.
2. **Semantic** — dependency-light fixtures and interface rules.
3. **Native OpenTofu** — `tofu test`, plan behavior, moves/imports.
4. **Provider integration** — create and inspect real sandbox resources.
5. **Data plane** — prove routing, identity, health, encryption, and recovery.
6. **Upgrade** — old caller/state to new module version without unintended replacement.
7. **Failure** — quota, partial apply, denied permission, or unavailable dependency.

Not every module needs every level on every commit, but the release claim must match the executed evidence.

## 10. Reasons not to create a module

Keep resource blocks in the root when:

- they are used once and express a clear root-owned decision;
- no stable abstraction has emerged;
- wrapping would only rename provider arguments;
- the caller needs most of the provider surface anyway;
- ownership crosses several modules and would become more ambiguous;
- the proposed module would require many escape hatches.

A mature codebase is not the one with the highest module count. It is the one in which each abstraction has a defensible responsibility and migration path.
