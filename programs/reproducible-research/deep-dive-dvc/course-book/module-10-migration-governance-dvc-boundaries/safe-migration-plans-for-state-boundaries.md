# Safe Migration Plans for State Boundaries


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Migration Governance Dvc Boundaries"]
  page["Safe Migration Plans for State Boundaries"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Migration is risky because it often looks like simple movement.

Examples:

- move to a new DVC remote
- rename a publish boundary
- split one pipeline into two
- move metrics into a new schema
- change how experiments become releases

Each change can break trust if the state boundary moves without proof.

## Move one boundary at a time

A safe migration names the boundary being moved:

> Move promoted release artifacts from `publish/v1/` to `registry/incident-escalation/v1/`
> while preserving manifest, params, metrics, and recovery checks.

That is stronger than:

> Reorganize publishing.

The first plan has a testable promise. The second can hide many unrelated changes.

## A migration plan needs proof before and after

Before the change:

- record the current trusted state
- run the current verification route
- identify consumers of the old boundary
- decide rollback conditions

After the change:

- run the same or replacement verification route
- confirm consumers have a stable new boundary
- compare manifests and release evidence
- document what changed and what did not

```mermaid
flowchart LR
  old["old boundary"] --> inventory["inventory evidence"]
  inventory --> migrate["move boundary"]
  migrate --> verify["verify new boundary"]
  verify --> note["record migration note"]
```

## Migration should preserve meaning

Renaming a metric key can be a migration. Moving the file is not the hard part. Preserving
or explicitly changing the metric meaning is the hard part.

Ask:

- did the metric definition change?
- did the consumer path change?
- did the retention promise change?
- did recovery documentation change?
- did any old release become harder to audit?

If yes, the migration note should say so.

## Review checkpoint

You understand this core when you can:

- name the state boundary being moved
- avoid bundling unrelated migrations
- define before-and-after proof routes
- protect consumers and rollback paths
- document meaning changes instead of hiding them inside movement

Safe migration is controlled boundary change, not file shuffling.
