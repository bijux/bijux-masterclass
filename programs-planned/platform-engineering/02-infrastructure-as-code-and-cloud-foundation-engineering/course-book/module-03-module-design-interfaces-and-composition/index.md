# Module 3 — Module Design, Interfaces, and Composition

Modules should make infrastructure easier to reason about. Many modules do the opposite: they hide provider semantics behind hundreds of options, create networks and identities as side effects, or wrap one resource without adding a meaningful abstraction.

This module treats a module as a versioned architectural interface. The goal is not maximum reuse. The goal is a clear owner, a bounded responsibility, and predictable change.

## Learning outcomes

You will be able to:

- distinguish root-module composition from reusable child modules;
- design modules around architectural capabilities rather than provider resource names;
- keep provider credentials and configurations in the root;
- write typed inputs, validations, preconditions, outputs, and invariants;
- use stable collection keys and avoid identity changes hidden inside a module;
- keep module trees flat and dependencies explicit;
- version module interfaces and migrate callers without accidental replacement;
- test modules at syntax, semantic, plan, and live-provider levels;
- decide when not to create a module.

## Root modules and child modules have different jobs

A root module selects:

- backend;
- provider configurations and aliases;
- accounts and regions;
- input sources;
- child-module versions;
- composition among capabilities;
- release policy.

A reusable child module declares provider requirements and creates one architectural capability. It should not embed credentials, select a caller’s account implicitly, or create unrelated shared infrastructure.

For Atlas, the root assembles:

```hcl
module "network" { ... }
module "identity" { ... }
module "audit" { ... }
module "workload" { ... }
module "edge" { ... }
module "data_protection" { ... }
```

The workload module receives subnet IDs, role/profile names, KMS keys, and policy choices. It does not create a surprise VPC or an administrator role.

## A module should raise the level of meaning

`aws_security_group` is a provider resource. `atlas_edge_path` is an architectural capability that may include:

- load balancer security group;
- workload ingress security group rule;
- target group;
- listener;
- access logs;
- health check and drain policy;
- outputs that identify the approved edge path.

A module named `security-group` that forwards every provider argument is usually a thin wrapper. It adds another versioned interface without reducing architectural decisions.

## Start from responsibility and invariants

Before writing HCL, state:

```text
module name:
responsibility:
objects owned:
dependencies received:
security invariants:
lifecycle and replacement behavior:
outputs promised:
changes considered breaking:
```

For the Atlas network module:

- responsibility: account-local routed VPC foundation;
- owns: VPC, subnets, route tables, gateways/endpoints, flow-log plumbing;
- receives: address plan, zone selection, egress profile, log destination;
- invariants: no overlapping CIDRs; public routes only in public tables; private routes follow declared egress profile; flow logging enabled;
- outputs: VPC ID, subnet IDs keyed by zone slot, route-table IDs, address metadata;
- breaking changes: key changes, CIDR changes, subnet role changes, or output removal.

## Types prevent entire classes of configuration errors

Use structured types rather than parallel lists:

```hcl
variable "subnets" {
  type = map(object({
    role            = string
    ipv4_cidr       = string
    availability_id = string
  }))

  validation {
    condition = alltrue([
      for subnet in values(var.subnets) :
      contains(["public", "private", "data"], subnet.role)
    ])
    error_message = "subnet role must be public, private, or data"
  }
}
```

A map preserves semantic keys. The object keeps related fields together. Validation rejects unsupported roles before provider calls.

Avoid a variable for every provider attribute. A platform module should choose safe defaults and expose only decisions callers genuinely own.

## Inputs are authority boundaries

An input says the caller may decide something. Exposing `allow_public_ssh = true` grants a caller authority to widen the management path. Atlas does not expose that input because public SSH is outside the foundation policy.

Likewise, an input named `extra_iam_policy_json` is effectively an escape hatch around module security. If extension is required, constrain the action/resource vocabulary or accept an explicit policy object that the release policy can inspect.

## Outputs are contracts, not debug dumps

Output only what callers need. Exposing every resource ID encourages callers to reach inside the module and depend on implementation details.

Good network outputs:

```hcl
output "private_subnet_ids" {
  value = {
    for key, subnet in aws_subnet.private : key => subnet.id
  }
}
```

Fragile output:

```hcl
output "everything" {
  value = aws_subnet.private
}
```

The latter leaks the provider resource schema and makes provider upgrades part of the module’s public interface.

## Provider configuration belongs in the root

Reusable modules declare:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.58.0, < 7.0.0"
    }
  }
}
```

They do not contain `provider "aws"` blocks. The root passes default or aliased providers. This keeps account and region selection visible and allows `for_each`, `count`, and `depends_on` on module calls.

A reusable module’s provider constraint should usually state compatibility, while the root/lock file selects the exact version for a release.

## Flat composition limits hidden coupling

Deep module trees hide resource ownership and make provider aliases, outputs, and migrations difficult. Prefer one root that composes modules and passes dependencies explicitly.

Bad:

```text
platform
└── workload
    └── network
        └── audit
            └── kms
```

Better:

```text
root
├── network
├── audit
├── identity
├── workload  ← receives network and identity outputs
├── edge      ← receives network and workload outputs
└── backup    ← receives key and data outputs
```

The root is allowed to know the architecture. Child modules remain reusable and independently testable.

## Conditional creation can blur ownership

A module with `create_vpc`, `existing_vpc_id`, `create_kms`, `existing_kms_arn`, and dozens of similar switches often contains two incompatible ownership models.

Prefer separate composition paths:

- network module owns a VPC and returns its interface;
- workload module receives a VPC/subnet interface regardless of who created it.

Dependency inversion lets the root choose created or discovered infrastructure without embedding both paths inside every module.

## Version the behavior, not only the files

A module version changes when its caller-visible contract changes. Examples:

- adding an optional output can be additive;
- changing a default egress profile can be behaviorally breaking;
- changing `for_each` keys can destroy/recreate resources;
- narrowing an input validation can break callers;
- changing a resource address can require `moved` blocks;
- increasing retention can increase cost even if technically compatible.

Release notes must describe plan and operational effects.

## Refactoring inside modules

Use `moved` blocks in the module to preserve addresses across versions:

```hcl
moved {
  from = aws_security_group.atlas
  to   = aws_security_group.workload
}
```

Keep move declarations for as long as supported upgrade paths require them. Removing them can break callers upgrading from older versions.

When splitting one module into two, root-level moves may be needed because addresses cross module paths. Test upgrades from real prior state fixtures, not only clean creation.

## Testing strategy

### Static

- formatting;
- validation;
- documentation and variable/output inventory;
- policy and forbidden-pattern checks.

### Semantic

- CIDR non-overlap;
- supported profile combinations;
- stable keys;
- output contract;
- replacement policy.

### OpenTofu test

Use `tofu test` with mock providers where appropriate and plan assertions. Mocking proves configuration logic, not AWS behavior.

### Live sandbox

Create a minimal fixture, inspect routes/IAM/health/storage, test a negative case, then destroy. Live tests need cost and account boundaries.

### Upgrade

Initialize from a prior module version and state fixture, upgrade the module, and verify the plan contains only documented actions.

## Worked design: network module versus landing-zone module

A learner proposes one `landing_zone` module that creates Organizations accounts, identity, central logs, VPCs, NAT, load balancers, and workloads.

The module is not a useful abstraction. It combines multiple owners, credentials, lifecycles, and blast radii. A failure in one provider alias can block unrelated change. Callers cannot adopt an existing account or network without toggles that weaken ownership.

Atlas separates organization architecture (documented and optionally provisioned by a dedicated root) from account-local foundation modules. The course baseline assumes a sandbox/workload account already exists and focuses on reproducible resources within it.

## Atlas module catalogue

### `naming`

Pure locals and validations for names/tags. No cloud objects.

### `network`

VPC, subnet roles, route tables, gateways/endpoints, flow logs.

### `identity`

Workload role, instance profile, backup policy, permission boundaries/profile constraints.

### `audit`

CloudTrail, log bucket policy, flow-log delivery role/destination.

### `workload`

Launch template or instance, metadata options, root/data volumes, bootstrap contract.

### `edge`

Load balancer, listener, target group, health/draining, approved security-group path.

### `data-protection`

Backup bucket, lifecycle/retention, snapshot policy, restore metadata.

Each module has a concise interface and exposes no generic arbitrary-policy escape hatch.

## Design review: should `atlas-host` be one module?

A proposed module creates:

- VPC and subnets;
- instance role and KMS key;
- backup bucket;
- EC2 launch template and instance;
- load balancer and DNS record;
- CloudTrail trail;
- budgets.

The module has many variables, so it appears reusable. In practice, it combines
resources with different owners and lifecycles. A network change now shares a
module version with an application image change. A workload team can indirectly
control audit and KMS behavior through one call. Testing one optional feature
combination becomes combinatorial.

The Atlas catalogue instead separates capabilities:

```text
naming
    pure governed names/tags

network
    VPC, subnets, routes, endpoints

identity
    runtime role and workload key

audit
    account-local evidence path

data-protection
    workload data volume contract

workload
    launch template and optional host

edge
    public routing resources
```

The root module composes them because the root owns the environment decision.
This is not “more modules is better.” Each boundary earns its existence through
one of these properties:

- independent owner;
- independent lifecycle;
- reusable capability;
- narrower authority;
- meaningful invariant;
- testable interface.

If a module is only a renamed `aws_s3_bucket` with every provider argument
exposed, it has not raised the abstraction. It may still be useful as a policy
wrapper, but then the policy and supported variation must be explicit.

## Interface design by forbidden states

A strong interface makes unsafe configurations unrepresentable or at least
rejectable early.

Instead of:

```hcl
variable "public"  { type = bool }
variable "private" { type = bool }
```

use:

```hcl
variable "tier" {
  type = string
  validation {
    condition     = contains(["public", "private", "data"], var.tier)
    error_message = "tier must be public, private, or data"
  }
}
```

The first interface permits both booleans true or both false. The second
expresses one semantic choice.

Likewise, subnet inputs are keyed by a stable identity rather than supplied as
a list. IAM inputs accept a purpose-specific prefix or resource ARN rather than
an arbitrary policy blob. Outputs publish the values consumers need, not every
resource attribute available from the provider.

## Output minimization and security

A broad output such as:

```hcl
output "everything" {
  value = {
    role = aws_iam_role.runtime
    key  = aws_kms_key.workload
  }
}
```

leaks implementation details, creates accidental consumers, and may expose
sensitive/computed data through state-sharing paths. Narrow outputs such as
`runtime_role_arn` and `workload_kms_key_arn` establish a deliberate contract.

This is especially important when a downstream root obtains outputs through a
registry, parameter publication, or generated handoff. The consumer should not
need read access to the producer's entire state.

## A module migration is a consumer release

Changing an input default can be behavior-breaking even when no variable is
removed. Enabling NAT or flow logs by default can add cost and permissions.
Changing a map key can change resource addresses. Renaming an output can break
composition roots.

The course classifies module evolution as:

```text
additive
    optional input or new output with no default behavior change

review-required
    default, cost, security, or operational behavior changes

breaking
    required input, removed output, changed type, or identity loss
```

A module release includes migration blocks and tested consumer roots. The
version number is a communication tool only when the behavior and evidence are
recorded.

## Atlas capstone increment

Module 3 implements the catalogue and a module-interface linter. Fixtures include:

- a valid flat composition;
- a thin wrapper rejected for no architectural value;
- a deep dependency tree;
- a provider block inside a child module;
- an unstable list-key interface;
- an unversioned breaking default change.

## Completion standard

You are ready for Module 4 when you can defend each Atlas module’s responsibility, inputs, outputs, provider requirements, state owner, replacement behavior, and upgrade path—and can also explain why several resources remain directly in a root rather than being forced into modules.
