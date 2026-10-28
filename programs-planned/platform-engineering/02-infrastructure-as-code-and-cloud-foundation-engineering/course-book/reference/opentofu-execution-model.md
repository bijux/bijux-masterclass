# Reference — OpenTofu Execution Model

OpenTofu is a change engine over several imperfect representations. Understanding those representations is more important than memorizing commands.

## The five participants

```text
configuration
    desired relationships and constraints

state
    durable association between resource addresses and provider objects

provider
    executable schema, planning rules, state upgrade logic, and API adapter

remote control plane
    cloud objects currently reported by APIs

data plane
    traffic, storage, identity, and application behavior users actually depend on
```

A successful transition in one participant does not prove the others are correct.

## Initialization

`tofu init` resolves modules, installs providers, verifies dependency-lock information, and initializes the backend. Backend initialization occurs before ordinary input-variable evaluation, which is why backend values are normally supplied through partial configuration rather than ordinary variables.

Initialization proves that the selected dependencies and backend can be initialized in the current environment. It does not prove that the intended account is selected or that a future apply is safe.

## Loading and evaluation

OpenTofu loads the root module and its child modules, evaluates expressions, applies type constraints and validations, and builds resource instances from `count` and `for_each`.

Resource addresses are created here. For example:

```text
module.network.aws_subnet.this["private-a"]
```

is an identity used in state and planning. Changing an index or key can change identity even when the provider arguments are unchanged.

## Refresh and observation

During normal planning, providers read remote objects associated with state addresses. This observation may reveal:

- external changes;
- provider normalization;
- deleted objects;
- newly computed attributes;
- API behavior changed since the last state write.

Refresh is not a universal discovery process. A remote object absent from state is not automatically adopted merely because its name resembles the configuration.

## Graph construction

References create dependency edges. Passing `module.network.vpc_id` into another object establishes both a value relationship and the ordering needed to produce that value. `depends_on` should be reserved for a real behavioral dependency that cannot be expressed through data flow.

Broad explicit dependencies can:

- reduce parallelism;
- make more values unknown until apply;
- enlarge the apparent blast radius;
- obscure the actual ownership relationship.

## Unknown values

When an object has not yet been created, its generated ID, ARN, IP address, or DNS name can be unknown. OpenTofu preserves the expression and type so downstream planning can continue.

Unknown values are useful because they prevent invented placeholders. They are risky when a reviewer needs to know a security- or destruction-critical value before approval. In such cases, redesign the interface, move the decision into a known input, or create an explicit apply-time/post-apply gate.

## Planning

A plan is calculated from:

```text
configuration
+ input values
+ state snapshot
+ refreshed provider observations
+ provider schemas and versions
+ target account/region/credentials
+ lifecycle and condition rules
```

The plan classifies actions such as create, update, replace, delete, import, move, and read. It is not a text diff. Provider schemas determine which changes can occur in place and which require replacement.

A plan can be wrong for operational purposes while being internally consistent. It may expose a public path, replace durable state, exceed quota, or create an object that never becomes ready.

## Saved plan and apply

A saved plan reduces the race in which approval describes one calculation and apply recalculates another. It should be bound to source, inputs, backend, state lineage/serial, provider lock, account, region, and identity class.

A saved plan does not freeze:

- remote quotas;
- organization policy;
- cloud-service availability;
- credentials and session expiry;
- concurrent external changes;
- data-plane conditions.

Apply executes graph nodes subject to dependencies and provider concurrency. One remote operation can succeed before a later operation fails. A provider can also complete an API call before OpenTofu persists the new state. This is why partial apply and orphan reconciliation are first-class topics.

## State commit

After provider operations, OpenTofu writes the new state through the backend. Backends may provide locking, but a lock only establishes writer exclusion. It does not make the proposed change correct.

If the state write fails, remote reality may have advanced beyond the last authoritative snapshot. Recovery must compare state, remote inventory, and operation evidence; simply restoring an old snapshot or repeating apply can duplicate or destroy objects.

## Conditions and lifecycle

Preconditions, postconditions, check blocks, and variable validations make assumptions executable. They should express invariants that can actually be evaluated at the relevant stage.

Lifecycle arguments are sharp tools:

- `create_before_destroy` needs coexistence capacity and dependency compatibility;
- `prevent_destroy` disappears if the resource block is removed and does not prevent out-of-band deletion;
- `ignore_changes` is safe only when another explicit owner reconciles the ignored attribute;
- replacement triggers can widen the change set unexpectedly.

## Final rule

Treat an OpenTofu release as a chain:

```text
reviewable plan
→ controlled apply
→ state commit
→ control-plane observation
→ data-plane proof
→ recovery and cleanup evidence
```

Stopping at “apply complete” leaves the most important platform claims unproved.
