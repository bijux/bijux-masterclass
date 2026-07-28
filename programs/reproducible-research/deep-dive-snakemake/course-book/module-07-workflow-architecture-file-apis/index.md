# Module 07: Workflow Architecture and File APIs

A Snakemake repository can produce correct files and still be difficult to change
safely. The warning sign is not its line count. It is that a maintainer cannot answer
ordinary questions without reconstructing hidden relationships:

- Where is the workflow assembled?
- Which policy belongs to the caller and which belongs to a reusable module?
- Which paths may downstream code rely on?
- Which script is an adapter and which package is independently reusable software?
- What proof must survive when a boundary moves?

This module teaches how to answer those questions from repository evidence.

## The architecture claim

Architecture is the placement of decisions and contracts, not the arrangement of
folders. A reviewable workflow makes this chain visible:

```mermaid
flowchart LR
  caller["Caller intent\nconfig + requested targets"]
  assembly["Workflow assembly\nentrypoint + includes"]
  graph["Rule ownership\ninputs + outputs + resources"]
  execution["Execution adapters\nscripts + environments"]
  api["File API\nstable consumer paths"]
  proof["Review evidence\nplans + audits + consumer checks"]

  caller --> assembly --> graph --> execution --> api --> proof
```

Every arrow is a boundary to inspect. If a package reads global workflow config, the
execution boundary reaches backward into caller policy. If downstream users scrape an
HTML report, the file API is weaker than the consumer behavior. If a module receives
the entire parent config, its apparent reuse boundary hides coupling.

## The repository you will review

Use the Snakemake capstone throughout the session. It is deliberately substantial
enough to create real architectural questions:

```text
capstone/
├── Snakefile
├── config/
├── workflow/
│   ├── CONTRACT.md
│   ├── REVIEW.md
│   ├── contracts/FILE_API.md
│   ├── envs/
│   ├── modules/
│   ├── rules/
│   └── scripts/
├── src/
├── profiles/
├── tests/
└── publish/
```

Do not assume the tree proves good separation. The top-level `Snakefile`, for example,
contains configuration defaults, a checkpoint, publication rules, includes, and the
default target. Your job is to decide which of those decisions are legitimate assembly
and which create review pressure.

## Learning outcomes

By the end of the session, you should be able to:

1. explain Snakemake's parse-time assembly without treating includes as runtime calls
2. distinguish a local rule-family split from a reusable `module` interface
3. trace config, path, artifact, and rule-name ownership across a module boundary
4. specify a file API from the consumer side, including compatibility and identity
5. distinguish workflow adapters from reusable domain packages
6. diagnose coupling through imports, global config reads, implicit path conventions,
   and side effects
7. justify a refactor with a failed review question and a preservation proof
8. hand another maintainer an architecture packet they can audit without an oral tour

## Build one architecture packet

All ten exercises contribute to one packet:

```text
architecture-packet/
├── entrypoint-inventory.md
├── assembly-map.md
├── responsibility-table.md
├── module-interface-card.md
├── artifact-trace.md
├── file-api-ledger.md
├── coupling-finding.md
├── refactor-comparison.md
├── proof-bridge.md
└── review-decision.md
```

These names describe durable evidence roles. You may keep the packet in your course
notebook rather than creating these files, but preserve all ten records.

## Session sequence

| Work block | Question | Output |
| --- | --- | --- |
| orient | what is the exact architectural reliance under review? | one bounded claim |
| read assembly | what happens at parse time, and where is it declared? | entrypoint inventory and assembly map |
| classify ownership | which decisions belong to local rule families, modules, or callers? | responsibility table and module interface card |
| trace a consumer surface | which path is public, who produces it, and how may it change? | artifact trace and file-API ledger |
| inspect code boundaries | where does config, path, or runtime coupling cross layers? | coupling finding |
| compare repairs | which movement improves the failed review question without losing proof? | refactor comparison and proof bridge |
| review | what may the next maintainer rely on now? | bounded architecture decision |

## Evidence before opinions

Use four evidence lanes:

| Lane | Useful evidence | What it can establish |
| --- | --- | --- |
| assembly | `Snakefile`, include statements, module declarations, rule listing | what the workflow exposes after parsing |
| dependency direction | config slices, imports, module bindings, path parameters | which layer knows about which other layer |
| consumer contract | file-API documentation, manifest, schema, consumer test | which outputs are intentionally stable |
| preservation | dry-run plans, module-interface audit, tests, publish verification | whether a proposed boundary change retained required behavior |

One lane cannot substitute for another. A DAG image does not define path compatibility.
A file-API document does not prove the producer emits conforming data. A successful run
does not prove the module avoids parent-private config.

## Study route

Read in this order:

1. [Entrypoints, Repository Layers, and Visible Assembly](entrypoints-repository-layers-and-visible-assembly.md)
2. [Rule Families, Modules, and Ownership Boundaries](rule-families-modules-and-ownership-boundaries.md)
3. [File APIs, Public Paths, and Contract Docs](file-apis-public-paths-and-contract-docs.md)
4. [Helpers, Scripts, Packages, and Coupling Control](helpers-scripts-packages-and-coupling-control.md)
5. [Architecture Review, Drift, and Refactor Triggers](architecture-review-drift-and-refactor-triggers.md)
6. [Worked Example: Reading a Snakemake Repository Like an Architect](worked-example-reading-a-snakemake-repository-like-an-architect.md)
7. [Exercises](exercises.md)
8. [Exercise Answers](exercise-answers.md)
9. [Glossary](glossary.md)

The order moves from parse-time visibility to ownership, then to external contracts,
internal coupling, and change judgment.

## Commands and their limits

Run raw workflow commands from `programs/reproducible-research/deep-dive-snakemake/capstone/`.

| Command | Question | Limit |
| --- | --- | --- |
| `snakemake --list-rules` | which rules exist after assembly? | does not show ownership quality |
| `snakemake -n --printshellcmds` | which jobs and commands are planned? | does not execute runtime boundaries |
| `snakemake --dag` | which jobs and file edges are visible for requested work? | does not reveal hidden Python coupling |
| `gmake module-interface-audit` | do paired module models expose or hide config, path, and policy contracts? | tests the supplied models, not every repository module |
| `gmake module-interface-selftest` | can the audit reject dishonest interface evidence? | proves the gate, not the capstone's entire architecture |
| `gmake verify-report` | does the publish-facing evidence satisfy its checks? | does not decide whether internal layering is maintainable |

Record the working directory, requested target, config, and profile with every command.
Architecture evidence without invocation context is difficult to review.

## A first diagnostic

Before reading the lessons, open the capstone `Snakefile` and classify each top-level
statement:

```text
contract gate | configuration policy | assembly | rule definition | target selection
```

Then answer:

- Which classifications appear more than once?
- Which statements must a new maintainer understand before reading included rule files?
- Which statements could move without changing the public workflow contract?
- What proof would distinguish a safe move from a merely successful one?

Do not refactor yet. The classification is the baseline.

## Exit standard

You are ready to leave Module 07 when you can review one proposed architectural change
with this structure:

```text
reliance:
current owner:
coupling or review failure:
proposed owner:
contract that crosses the boundary:
preservation evidence:
consumer compatibility result:
remaining limit:
```

You must also complete all ten exercises and produce the architecture packet. “The new
tree is cleaner” is not an exit argument. The decision must identify a safer dependency
direction, a clearer contract, or a stronger review path.
