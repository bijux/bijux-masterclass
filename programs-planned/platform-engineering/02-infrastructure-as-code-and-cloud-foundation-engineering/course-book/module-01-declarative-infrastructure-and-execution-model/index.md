# Module 1 — Declarative Infrastructure and the OpenTofu Execution Model

A resource block is not infrastructure. It is one statement in a program that asks a provider to reconcile remote objects and then records the relationship between those objects and stable resource addresses.

This module establishes the execution model used by the rest of the course. Without it, later topics—state recovery, module evolution, imports, drift, policy, and release automation—turn into command memorization.

## Learning outcomes

By the end of the module you can:

- distinguish configuration, state, provider observation, and data-plane behavior;
- explain how resource addresses and dependency edges shape a plan;
- predict when values are known during planning and when they remain unknown until apply;
- choose stable `for_each` keys instead of identity-fragile list positions;
- read a plan as a proposed transition, not an inventory report;
- identify provider and input changes that invalidate a saved plan;
- use conditions and checks to reject invalid infrastructure assumptions;
- prove that a successful apply produced the intended service behavior.

## The control problem behind infrastructure as code

Imagine that Atlas needs a VPC, four subnets, an instance profile, a load balancer, one EC2 instance, one data volume, and two S3 buckets. A script can call the relevant APIs. The hard part begins on the second run:

- Which remote object corresponds to each declaration?
- Which attributes are defaults returned by the provider rather than choices in the repository?
- Which values can change in place?
- Which changes require replacement?
- What happens when the fifth API call succeeds and the sixth fails?
- How does another operator continue without repeating successful calls?

OpenTofu answers these questions through configuration, provider schemas, a resource graph, and state. The model is powerful but not magical.

```text
configuration + variables + provider versions + state + refresh
                              |
                              v
                            plan
                              |
                         approved apply
                              |
                  provider API operations
                              |
                     updated state snapshot
```

Each input matters. The same source commit can produce a different plan when the caller identity, region, provider version, remote state, or data source result changes.

## Configuration is intent, not history

Configuration describes desired relationships. It does not contain every fact needed to manage existing objects. Consider:

```hcl
resource "aws_s3_bucket" "backup" {
  bucket = "atlas-prod-backup-eu-central-1"
}
```

The block expresses a desired bucket and gives it the address `aws_s3_bucket.backup`. It does not say whether OpenTofu created the bucket yesterday, imported it today, or should create it tomorrow. State stores the association between that address and the provider’s remote identity.

Deleting the block does not merely delete text. It tells OpenTofu that the object previously associated with the address is no longer desired. Unless another lifecycle mechanism intervenes, the plan proposes destruction.

## Resource addresses are durable identities

A resource address is part of the operational API of the configuration.

```text
module.network.aws_subnet.private["zone-a"]
```

The address carries:

- module path;
- resource type;
- local resource name;
- instance key.

Renaming `private` to `workload` is not cosmetic. Without a `moved` declaration, OpenTofu sees one address disappear and another appear. If the provider reports that the resource must be replaced, a refactor can become an outage.

Stable keys matter for collections. This pattern is fragile:

```hcl
resource "aws_subnet" "private" {
  count      = length(var.private_cidrs)
  cidr_block = var.private_cidrs[count.index]
}
```

Inserting a CIDR at index zero shifts every later identity. Prefer semantic keys:

```hcl
variable "private_subnets" {
  type = map(object({
    cidr = string
    zone = string
  }))
}

resource "aws_subnet" "private" {
  for_each          = var.private_subnets
  cidr_block        = each.value.cidr
  availability_zone = each.value.zone
}
```

Now `aws_subnet.private["zone-a"]` remains the same address even when another subnet is added.

## Dependencies are values before they are ordering instructions

OpenTofu infers most graph edges from references:

```hcl
resource "aws_subnet" "private" {
  vpc_id = aws_vpc.atlas.id
}
```

The subnet needs the VPC ID, so it depends on the VPC. Avoid `depends_on` when an actual value relationship can express the dependency. A broad explicit dependency can make more values unknown during planning and can serialize unrelated work.

`depends_on` is justified for hidden behavioral dependencies—for example, when a resource must wait for an IAM policy attachment even though no argument refers to it. When you use it, document the remote behavior that creates the hidden edge.

## Unknown values are a feature

A plan can know that an instance will be created without knowing its future ID or private address. OpenTofu represents such values as unknown rather than guessing.

Unknown values protect the graph from pretending that apply-time results are already known. They also constrain policy and review. If a security-critical field is unknown—such as whether a route points to an approved target—the plan may need to be rejected or redesigned so the value is known earlier.

Do not convert unknowns into empty strings or placeholder defaults. That erases the distinction between “not yet known” and “known to be empty.”

## Providers are executable translators and observers

The AWS provider:

- defines resource and data-source schemas;
- validates arguments;
- translates planned actions into AWS API calls;
- reads remote objects and normalizes responses;
- decides which changes require replacement;
- upgrades stored resource state across provider versions.

A provider upgrade can therefore change plans without a source-code change. Pin provider versions in `required_providers`, commit the dependency lock file, and review upgrades deliberately.

Reusable child modules declare compatible provider requirements but do not configure provider credentials or regions. Provider configurations belong in root modules, where account and region authority is visible.

## Planning is not a pure diff of text

A normal plan may:

1. load configuration and input values;
2. initialize modules and provider schemas;
3. read backend state;
4. ask providers to refresh remote objects;
5. compare refreshed state with desired configuration;
6. calculate create, update, replace, destroy, import, and move actions;
7. propagate unknown values through the graph;
8. evaluate validations, preconditions, postconditions, and checks that are decidable;
9. produce human and machine-readable output.

A data source can make planning depend on current remote facts. For example, selecting “the latest AMI” means the same commit can choose a different image tomorrow. Course 2 uses explicit image parameters for released stacks and treats dynamic image lookup as a discovery step whose result is promoted into versioned input.

## Saved plans reduce one race, not every race

A saved plan binds a proposed change to the configuration, state, provider selections, and inputs used during planning. Applying that plan avoids silently recalculating a different transition at approval time.

It does not freeze the cloud. Another actor can change or delete a remote object between plan and apply. Provider APIs can reject the request because a quota or policy changed. A saved plan also contains sensitive values and must be protected.

The release process therefore records:

- source digest;
- input digest;
- state lineage and serial;
- provider lock digest;
- caller/account/region class;
- plan digest;
- approval;
- apply result;
- post-apply data-plane evidence.

## Lifecycle settings are sharp tools

### `create_before_destroy`

Useful when two generations can coexist and remote naming/quotas allow it. It is not a universal zero-downtime switch. A globally unique name, fixed IP, attached volume, or quota can prevent coexistence.

### `prevent_destroy`

A guard against plans that include destruction while the block remains present. It does not protect an object after its entire resource block disappears, and it does not replace backend/object retention policy.

### `ignore_changes`

Useful when another authority legitimately owns selected attributes. Dangerous when used to silence unexplained drift. Every ignored attribute needs a named owner and reconciliation path.

### `replace_triggered_by`

Expresses that a change elsewhere should replace the resource. Use it only when replacement reflects a real lifecycle dependency.

Prefer `tofu apply -replace=ADDRESS` to legacy taint workflows when deliberate replacement is needed; the replacement intent remains visible in the plan.

## Conditions make assumptions executable

Variable validation rejects invalid inputs before remote operations:

```hcl
variable "environment" {
  type = string

  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "environment must be dev or prod"
  }
}
```

Preconditions attach requirements to a resource or data source. Postconditions verify provider-returned properties. `check` blocks can validate broader assertions without always blocking the apply, depending on the check behavior and timing.

Use these mechanisms for facts OpenTofu can observe. Do not claim that a plan-time condition proves application-level restore success or network reachability from an external client.

## A successful apply can still be a failed release

Suppose the load balancer, target group, security groups, and instance all create successfully. The instance boot script fails before Atlas starts. The provider sees valid resources; the target remains unhealthy.

The infrastructure apply succeeded. The platform release failed.

Post-apply validation must follow the data path:

```text
DNS resolution
→ TLS hostname validation
→ load balancer listener
→ healthy target selection
→ Atlas readiness
→ durable job completion
```

Control-plane evidence and data-plane evidence are complementary.

## Worked case: a harmless list edit replaces the network

An early Atlas configuration uses `count` for two subnets. A learner inserts a new subnet at index zero. The plan now associates old remote subnet A with new configuration item B, old subnet B with item C, and creates item A. Depending on immutable attributes, the provider proposes replacement.

The correction is not “approve carefully.” The identity model is wrong. Convert the collection to a map with semantic keys and use `moved` blocks to preserve existing addresses:

```hcl
moved {
  from = aws_subnet.private[0]
  to   = aws_subnet.private["zone-a"]
}
```

The migration must map every old index to the correct semantic key before changing the collection.

## Plan review as an engineering conversation

Consider a proposed plan for the development foundation:

```text
  # module.network.aws_subnet.private["euc1-az1"] must be replaced
-/+ resource "aws_subnet" "private" {
      availability_zone = "eu-central-1a" -> "eu-central-1b" # forces replacement
      cidr_block        = "10.64.16.0/20"
    }

  # module.network.aws_vpc_endpoint.s3 will be created
  + resource "aws_vpc_endpoint" "s3" { ... }
```

The author intended only to add an S3 endpoint. A weak review says, “one create,
one replace; looks small.” A real review reconstructs causality.

First, ask why the subnet zone changed. The repository may have used an
account-relative availability-zone **name** and regenerated a mapping on a
different account. The semantic identity should have been the stable zone ID,
with the account-local name supplied only at composition. The plan has exposed
an identity bug, not an ordinary replacement.

Second, follow dependents. Replacing the subnet can replace or interrupt:

- route-table associations;
- network interfaces;
- a singleton Atlas host;
- a zonal data-volume attachment path;
- load-balancer target registration;
- source IPs and DNS evidence.

The plan file may not include every data-plane consequence. The review needs the
architecture and workload facts from Course 1.

Third, decide whether the replacement is intended. If not, repair the identity
input and regenerate the plan. If it is intended, create a migration record,
quota check, replacement procedure, and packet/application proof. A lifecycle
flag cannot turn an unintended replacement into a safe one.

A useful review note therefore looks like this:

```text
Intent:
  add the S3 gateway endpoint to private/data route tables

Unexpected action:
  replace private subnet in euc1-az1

Cause:
  composition used account-relative AZ name as identity

Decision:
  reject plan; change key to stable AZ ID; regenerate

Required evidence after repair:
  subnet remote IDs unchanged; endpoint created; S3 path selects endpoint;
  no new default route; Atlas readiness unchanged
```

This style makes infrastructure review teachable. It also prevents a common
failure: approving plans by line count instead of by semantic effect.

## Unknown values and policy timing

Suppose an S3 bucket ARN is not known until apply, and a runtime policy refers
to it. A static policy evaluator may see an unknown resource and either reject
the plan or treat it as safe. Both choices can be wrong if they are
unqualified.

Course 2 classifies policy rules by when they can be decided:

| Rule | Earliest trustworthy point |
|---|---|
| no public SSH CIDR | configuration/plan |
| IMDSv2 required | configuration/plan |
| generated bucket name matches prefix | plan or apply depending on value |
| role can write only the created bucket | plan graph plus post-apply IAM vector |
| DNS resolves to the new load balancer | post-apply data plane |
| backup can be restored | recovery experiment |

Unknowns are therefore routed to later evidence instead of being silently
converted into a pass. This is the first appearance of an evidence pattern that
will continue throughout Platform Engineering: **the proof must occur at the
layer that owns the fact**.

## The provider is part of the release

An HCL repository without a dependency lock does not identify the program that
will interpret it. Provider code decides defaults, reads remote values,
classifies replacement, and calls APIs. Its version and checksum belong in the
same review as module code.

A careful upgrade starts with a plan on every state while the source
configuration remains otherwise unchanged. Differences are classified as:

- provider normalization only;
- newly observed remote property;
- corrected provider behavior;
- schema migration;
- actual infrastructure change.

Only after the upgrade is understood should an unrelated network or IAM design
change be added. This gives reviewers one causal variable at a time.

## Atlas capstone increment

Module 1 adds a dependency-light plan engine under `capstone/cloud_model/` and a real HCL root that declares only built-in `terraform_data` objects for Level B experimentation. The model supports:

- resource addresses;
- dependencies;
- known and unknown values;
- create/update/replace/destroy actions;
- state serials;
- saved-plan identity;
- stale-plan rejection.

It is deliberately small enough to read. Its purpose is to make the conceptual model executable, not to imitate every OpenTofu feature.

## What mastery looks like

You are ready to continue when you can take a plan and explain:

- why each action exists;
- which address and remote object it concerns;
- which input or observation caused the action;
- which values are unknown and why;
- which failure can occur after approval;
- which data-plane check closes the evidence gap.

Module 2 then focuses on the operational record that makes repeated execution possible: state.
