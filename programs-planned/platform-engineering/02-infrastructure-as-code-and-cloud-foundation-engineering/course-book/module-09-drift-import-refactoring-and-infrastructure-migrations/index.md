# Module 9 — Drift, Import, Refactoring, and Infrastructure Migrations

Infrastructure lives longer than its first module layout. Names change, modules split, providers evolve, manually created resources must be adopted, and incidents cause emergency changes outside the normal workflow. The question is not whether change will happen. It is whether identity and authority survive change without destructive surprise.

This module treats infrastructure migration as a first-class engineering discipline. It replaces the dangerous instinct to “edit state until the plan looks clean” with a sequence of observation, classification, explicit address migration, controlled import, and data-plane verification.

## Learning outcomes

You will be able to:

- distinguish configuration drift, remote drift, state corruption, provider normalization, and intentional emergency change;
- decide when to reconcile configuration to reality and when to restore reality to configuration;
- import existing resources declaratively and validate their full managed surface;
- preserve resource identity with `moved` blocks during refactoring;
- retire ownership with explicit removed/decommissioning steps;
- use refresh-only planning carefully without treating it as automatic repair;
- upgrade providers and modules with bounded version-skew evidence;
- design expand–transition–contract migrations for cloud foundations;
- reserve direct state surgery for narrow, reviewed recovery cases;
- prove that a no-replacement plan still preserves real service behavior.

## Five conditions that people call drift

“Drift” is often used too broadly. Diagnosis improves when the condition is named precisely.

### 1. Remote configuration changed outside OpenTofu

An operator modifies a security-group rule in the console. Configuration and prior state still describe the old rule; refresh observes the new remote value. The next plan may propose restoring the declared rule.

### 2. Configuration changed but was not applied

The repository expects a new CIDR, but the remote VPC remains old. This is an unapplied change, not remote drift.

### 3. Provider representation changed

A provider upgrade may normalize an empty set, reorder a computed collection, or model a default differently. The remote object may be unchanged while the plan changes.

### 4. State is stale or damaged

Remote resources and configuration may agree, but local/remote state lineage, serial, or object bindings are wrong. Repeated applies can worsen the incident if the state problem is not isolated.

### 5. Emergency change was intentional

An incident responder blocks an abusive source manually. The change is outside the standard pipeline but may be correct. The follow-up decision is whether to encode, replace, or expire it—not blindly revert it.

The drift report classifies each difference before proposing action.

## Configuration remains the policy, but reality has evidence

“Configuration is the source of truth” is useful but incomplete. If production reality contains an emergency safety control, automatically forcing it back to the repository version can reopen the incident.

The reconciliation decision considers:

- why the difference exists;
- who made it;
- whether it protects or violates policy;
- whether it affects data or availability;
- whether the repository or remote system is more current;
- whether another controller owns the field;
- what rollback and audit evidence exists.

The result is one of:

```text
restore remote to declared configuration
adopt remote change into configuration
replace resource deliberately
transfer ownership to another controller
expire temporary change
repair state binding
```

## Refresh-only plans

A refresh-only plan updates state to match observed remote values without proposing changes to remote objects. It is useful for inspecting and recording out-of-band changes, but it is not a universal fix.

Before applying a refresh-only plan, ask:

- Is the state backend healthy and correctly selected?
- Is the observed remote object authoritative?
- Will accepting the value hide an unauthorized change?
- Does configuration need to change too?
- Does the provider read every security-relevant property?

State becoming current does not mean infrastructure becoming correct.

## Import is the beginning of management

Import associates an existing remote object with a resource address. It does not automatically prove that the configuration describes every important property.

A safe import sequence is:

1. inventory and identify the remote object;
2. determine the owner and blast radius;
3. write configuration with the intended address;
4. declare an import block;
5. initialize with the pinned provider;
6. plan and inspect all proposed changes;
7. add or correct configuration until the plan expresses the intended adoption;
8. apply in a controlled environment;
9. verify data-plane behavior;
10. retain the import record.

Example:

```hcl
import {
  to = module.network.aws_vpc.atlas
  id = "vpc-0123456789abcdef0"
}
```

Importing a VPC while omitting DNS support, tenancy, tags, or related routes can produce an immediate change. That may be correct, but it must be intentional.

## Identity-preserving refactors

Resource addresses are bindings. Moving a resource from:

```text
aws_vpc.atlas
```

to:

```text
module.network.aws_vpc.this
```

without recording the move makes the plan interpret one deletion and one creation.

A `moved` block communicates continuity:

```hcl
moved {
  from = aws_vpc.atlas
  to   = module.network.aws_vpc.this
}
```

The migration remains in configuration long enough for every relevant state to observe it. Removing it immediately can break environments that have not yet upgraded.

For `for_each` changes, identity design is especially important. Changing a key from an availability-zone name to an index may require multiple explicit moves and can reveal that the old identity was unstable.

## State splitting

As a foundation grows, one state may contain bootstrap, organization, network, workload, and data resources. Splitting can reduce blast radius and authority, but it is a migration with cross-state dependencies.

A controlled split:

1. defines the target ownership boundary;
2. creates the target backend and access roles;
3. freezes conflicting changes;
4. copies or imports the selected bindings;
5. replaces broad `terraform_remote_state` consumption with narrow published contracts where possible;
6. verifies both states and remote resources;
7. removes old ownership without destroying resources;
8. resumes changes with explicit sequencing.

Directly running `state mv` between backends can be valid, but it needs backups, exact commands, lineage checks, locking, and recovery. Configuration-driven import/removal can be easier to review in some organizations.

## Expand–transition–contract for infrastructure

Cloud migrations often need old and new paths to coexist.

### Expand

Add the new route table, role, key, subnet, or target without removing the old path. Establish compatibility and capacity.

### Transition

Move consumers gradually. Observe, compare, and retain rollback.

### Contract

Remove the old path only after no consumer depends on it and recovery no longer requires it.

Examples:

- migrate from broad VPC CIDR ingress to security-group references;
- move from one NAT gateway to per-zone egress;
- rotate a KMS key while old snapshots remain decryptable;
- migrate backend locking mechanisms;
- change a module output consumed by several stacks;
- move public traffic to a new load balancer.

A direct replacement may be simpler when coexistence adds more risk than a planned interruption. The course asks for a decision, not ritual use of a pattern.

## Provider upgrades

A provider upgrade changes executable code that reads remote systems, calculates plans, and performs mutations. Treat it as a dependency release.

The upgrade process includes:

- review release notes and compatibility constraints;
- update the lock file in a dedicated change;
- run syntax, validation, and module tests;
- plan every managed state;
- classify normalization-only changes;
- apply first to a disposable/sandbox environment;
- verify data-plane behavior;
- promote with rollback constraints documented.

Do not combine a major provider upgrade, module refactor, and network redesign in one opaque plan.

## Module upgrades and semantic compatibility

A module version can be syntactically compatible while changing behavior. For example, an optional `enable_flow_logs` variable might change default from false to true, creating new costs and permissions.

A module release record states:

- input changes;
- output changes;
- resource-address changes;
- default changes;
- replacement risks;
- migration blocks;
- security and cost effects;
- tested consumer versions.

Course 2’s module fixtures include accepted additive, review-required default change, and rejected identity-breaking candidates.

## Removed ownership and decommissioning

Sometimes OpenTofu should stop managing an object without deleting it, for example when ownership transfers to a dedicated platform or another state. Sometimes the object should be destroyed after consumers leave.

The plan must distinguish:

```text
forget ownership but preserve remote object
transfer ownership with import into a new state
retire object and delete it
quarantine object pending evidence
```

An explicit removed/decommissioning record is safer than deleting a resource block and discovering the implied destroy during apply.

## Direct state manipulation

Commands such as state move, remove, or push operate on infrastructure identity. They are not ordinary refactoring tools.

A direct state operation requires:

- incident/change identifier;
- backend backup/version identifier;
- exclusive lock or controlled freeze;
- source and destination addresses;
- expected remote IDs;
- peer review;
- command transcript;
- post-operation plan;
- data-plane verification;
- recovery procedure.

Never edit raw JSON casually. Sensitive values, lineage, serials, provider metadata, and dependency information can be corrupted even when the file parses.

## Drift automation without auto-destruction

Scheduled plans can detect changes, but an automated “apply every drift” system can erase emergency mitigations or replace critical resources unexpectedly.

Atlas drift automation:

- runs read-only refresh/plan with a dedicated role;
- records structured differences;
- classifies high-risk fields;
- opens a review item;
- never auto-applies destructive or authority-changing changes;
- allows narrow, pre-approved remediation classes only after evidence.

## Worked migration: public host to private host behind ALB

Initial state:

```text
public EC2 instance
public IP
host security group permits 443 from internet
```

Target:

```text
public ALB
private EC2 instance
host permits only ALB security group
```

A safe migration:

1. create ALB, target group, and certificate;
2. permit ALB-to-host traffic while existing path remains;
3. register and health-check the host;
4. publish a temporary test hostname;
5. verify TLS, requests, and logs;
6. lower DNS TTL before the change window if justified;
7. switch the canonical record;
8. observe traffic and errors;
9. remove public ingress and public IP dependency;
10. retire the old path after rollback window.

The migration is not complete when the plan applies. It is complete when the old authority and route are removed and evidence shows no remaining consumer.

## When the clean plan is the suspicious one

An operator manually adds a route during an outage. A subsequent refresh-only
operation records it in state, and a module default happens to tolerate extra
routes. The next plan is empty.

The empty plan does not mean the emergency route has an owner, expiry, or policy
approval. Drift evidence must include the remote audit event and incident
record, not only the plan. Atlas therefore maintains a reconciliation inventory
for temporary changes until they are encoded or removed.

Conversely, a noisy provider plan can be harmless normalization. The skill is
not maximizing empty plans; it is making every meaningful difference owned and
explainable.

## Atlas capstone increment

Module 9 adds:

- drift classification and reporting;
- declarative import fixtures;
- moved-block refactors;
- module and provider upgrade candidates;
- state-split architecture record;
- backend-lock migration playbook;
- public-to-private edge migration;
- decommissioning records;
- a guarded state-repair runbook;
- data-plane verification after every identity migration.

## Completion standard

You may continue when a plan that appears to replace a critical resource no longer causes panic or blind approval. You can identify whether the cause is address change, provider normalization, remote drift, state damage, or an intended redesign—and select a migration path that preserves evidence and rollback.
