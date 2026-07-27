# Staging, Shared Filesystems, and Data Locality

Many production failures are blamed on "the cluster" or "Snakemake being weird" when the
real issue is simpler:

> the repository never stated what it assumes about where files live and when they become visible.

This page is about making those assumptions explicit.

## How to read this page

Read this page with one boundary question in mind:

> which paths are temporary operating context, and which paths are the stable contract the
> workflow is promising to produce?

If you keep that question visible, staging and filesystem behavior stop sounding mystical
and start sounding reviewable.

## Why this lesson belongs in Module 03

By Module 03, the workflow already has meaningful outputs and publish surfaces. That is
exactly why locality matters now.

If the repository does not separate temporary placement from final trust surfaces:

- incidents get explained as cluster folklore
- scratch paths start acting like accidental contracts
- local and CI differences feel haunted rather than owned

## Data locality is an operational boundary

The workflow meaning may be unchanged while the operating context changes:

- local filesystem
- CI workspace
- shared cluster filesystem
- scratch or staged working directory

Those contexts can differ safely, but only if the repository treats them as policy
surfaces instead of invisible background facts.

## A strong beginner habit

When a run behaves differently across environments, ask about path roles before you ask
about Snakemake.

For example:

- where is the job reading from
- where is it writing temporary work
- when is it publishing to the declared final output

## The two questions to ask first

When an output "goes missing" or appears late, ask:

1. where was the job really writing
2. when should another process be allowed to trust that write

Those questions are often more useful than staring at one failed command.

## The common beginner mistake

People often collapse these questions into one vague thought:

> the file should be there somewhere.

That is exactly the mindset this page is trying to replace.

## Shared filesystems add timing pressure

On a shared filesystem, a job may finish before another process sees the output
immediately. That does not mean the workflow semantics changed. It means the operating
context needs an explicit patience policy.

This is where settings such as latency handling belong:

- they acknowledge the storage model
- they remain operational rather than semantic
- they help the workflow remain honest under normal infrastructure lag

That is a legitimate profile concern.

## A quick self-check before you keep reading

Imagine a shared filesystem where a finished output appears a little later to another
process.

Did the workflow meaning change?

No. The storage visibility policy changed. That is why latency handling belongs on the
operational side of the boundary.

## Scratch and staging are not semantic detours

Teams often stage work to local scratch or temporary directories for good reasons:

- faster local IO
- reduced pressure on shared storage
- simpler cleanup during execution

That can be healthy. It becomes dangerous when the repository stops answering:

- which paths are temporary
- which path is the final trusted publication surface
- how staged outputs become durable outputs

Staging is safe only when the final contract remains clear.

## One healthy mental model

```mermaid
flowchart LR
  input["declared input surface"] --> work["temporary work area or scratch"]
  work --> final["declared final outputs"]
  final --> publish["published contract surface"]
```

This model matters because it keeps three roles separate:

- where work happens
- where final workflow outputs live
- what downstream users are allowed to trust

When those collapse into one vague directory story, incidents get harder to explain.

## A weak staging habit

Weak operational habit:

- write directly to whatever path is convenient on the current machine
- move files around ad hoc when the scheduler changes
- let each maintainer decide whether scratch is used

This creates repository behavior that feels situational rather than intentional.

The repository may still run. Another maintainer will not know which path story to trust.

## A stronger staging pattern

Healthy staging design usually has these properties:

- the final output path is still the declared contract
- temporary or scratch paths are clearly operational
- publication into the final path is deliberate
- profiles or operating docs explain the context difference

This keeps the workflow semantics stable even while the operating context changes.

## Extend the scheduler receipt with a storage question

The scheduler-policy specimen records CPU, memory, and runtime. That is enough to
review resource translation, but not enough to execute a real job. A reviewer
must ask one more question:

> From the allocated worker, how does each declared path become reachable?

Complete this table for a deployment:

| Path role | Example | Worker access | Publication rule |
| --- | --- | --- | --- |
| immutable input | `data/records.tsv` | shared read-only mount | never modified |
| scratch work | node-local allocation | worker-local | removed after success |
| declared result | `results/summary.tsv` | shared project storage | atomic rename |
| audit evidence | artifact bundle | CI or reviewer storage | immutable per run |

Do not write “shared filesystem” in the worker-access column. Name the mount,
object-store transfer, or staging command that makes the path reachable. Vague
storage nouns hide the exact boundary that fails during deployment.

## Trace a staged scheduler job

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant S as Scheduler
    participant W as Worker scratch
    participant P as Project storage
    O->>S: submit resources and path policy
    S->>W: allocate worker
    P->>W: stage declared inputs
    W->>W: compute and validate temporary result
    W->>P: atomically publish declared output
    P-->>O: output visible at contract path
```

Each arrow needs evidence:

- submission receipt for orchestrator to scheduler;
- scheduler job ID for allocation;
- transfer log or mount record for input availability;
- command log and validation result for computation;
- checksum or manifest for publication;
- Snakemake completion state for the final contract path.

If a deployment cannot produce one of those records, say which claim remains
untested. Do not replace the missing evidence with “works on our cluster.”

## Decide where a failure belongs

Consider four incidents:

1. The scheduler rejects `--mem=8000M`.
2. The worker cannot see `data/records.tsv`.
3. The command succeeds but the final rename is delayed.
4. The published result contains the wrong records.

They belong to different owners:

| Incident | Primary boundary | First evidence |
| --- | --- | --- |
| request rejected | scheduler policy | submission stderr |
| input invisible | staging or mount policy | worker path probe |
| rename delayed | shared-storage consistency | publication log and latency |
| wrong records | workflow semantics | result content and threshold |

Only the third case may justify increasing `latency-wait`, and only after showing
that the writer completed and visibility lagged. Increasing latency for the
other cases merely delays a useful failure.

## Preserve one final-path invariant

Across local, CI, and scheduler contexts:

```text
results/summary.tsv
```

must remain the declared output. Scratch locations may differ. Transfer tools
may differ. The path that downstream rules trust must not silently change.

That invariant lets the DAG preserve meaning while profiles vary execution:

```mermaid
flowchart TD
    L["local temporary directory"] --> F["results/summary.tsv"]
    C["CI workspace"] --> F
    S["scheduler scratch"] --> F
    F --> V["content verification"]
    V --> D["downstream dependency"]
```

The arrows are context-specific policy. The final node is the workflow
contract.

## What a good explanation sounds like

Strong:

> The workflow may use scratch differently by context, but it still publishes into the same
> declared final paths, so the trust surface does not drift.

Weak:

> On the cluster, the file story is just different.

## What should stay out of workflow meaning

The following often belong in policy rather than workflow meaning:

- latency expectations
- scratch or staging location
- executor-facing storage behavior
- log-location conventions for one operating context

The following usually do not belong purely in policy:

- which files count as final outputs
- whether a file is part of the publish boundary
- which sample identities the workflow is meant to process

That is the same module boundary in a new setting.

## Common failure modes

| Failure mode | What it looks like | Better repair |
| --- | --- | --- |
| shared-filesystem lag is treated as random workflow failure | reruns feel arbitrary | make latency handling explicit in policy |
| scratch usage changes the apparent final path story | maintainers cannot tell what is durable | keep final outputs and scratch paths separate |
| local and CI use different path assumptions without review | one context works and the other feels haunted | document and encode the context difference in profiles or operation docs |
| staging hides partial publication | files appear in final locations too early | keep publication explicit and deliberate |
| temporary paths become accidental contracts | downstream tools start depending on scratch layout | reserve stable trust only for declared final outputs |

## The explanation a reviewer trusts

Strong explanation:

> the workflow may stage work in a context-specific scratch area, but the final outputs are
> still published into the same declared contract paths; profile settings handle latency and
> execution context, while publish and results paths remain semantically stable.

Weak explanation:

> on the cluster we write files somewhere else first because that is just how it works.

The first explanation gives a boundary. The second gives a habit without a contract.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain why data locality is an operational boundary
- describe one legitimate policy use for latency handling
- distinguish scratch space from final output contracts
- explain one staging design that keeps workflow meaning stable across contexts
