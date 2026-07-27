# Anti-Pattern Atlas

Use this page when a workflow feels wrong but the problem still sounds vague. The goal is
to move from "something about this pipeline is messy" to a smaller, testable statement
about hidden logic, unsafe discovery, policy drift, weak publish contracts, or blurred
ownership.

This page is not a catalogue to memorize. It is a field guide for naming the failure
class before you start repairing code.

## How to use this atlas

Work in this order:

1. start from the symptom that best matches what you are seeing
2. inspect the smallest surface that could settle the question honestly
3. write the failure class in one sentence
4. repair the contract before you polish the implementation

If you skip the naming step, you will usually patch the visible symptom and leave the
workflow hard to trust.

## Quick symptom routing

| If you notice... | Suspect this first | Inspect this surface first | Study next |
| --- | --- | --- | --- |
| the workflow only makes sense when someone narrates it | hidden workflow logic | `Snakefile`, rule inputs and outputs, helper script assumptions | Module 01, Module 05 |
| a checkpoint feels magical or unpredictable | unsafe staged discovery | discovery artifact, checkpoint outputs, dry-run story | Module 02 |
| a profile change alters meaning instead of only execution context | policy leaking into semantics | profile values, config boundaries, plan differences | Module 03, Module 08 |
| downstream users can see files but still cannot trust the result | weak publish contract | published bundle, manifest, integrity report, consumer view | Module 06 |
| a repository is split into many files but change ownership is still blurry | boundary collapse | entrypoint, rule modules, helper packages, file API | Module 04, Module 07 |
| an incident review depends on memory and terminal scrollback | evidence route failure | saved summary, rerun explanation, benchmark artifact, runbook | Module 09, Module 10 |

## Anti-pattern families

### Hidden logic escaped the DAG

**What it looks like**

- A rule output is technically correct, but you cannot explain why it exists by reading
  the workflow contract.
- Important behavior lives in shell fragments, helper scripts, or undocumented config.
- Reviewers trust the workflow only after a live walkthrough.

**What is actually wrong**

The DAG is no longer carrying the main story. The workflow still runs, but the contract
has moved into places that are harder to inspect than the rules themselves.

**Inspect first**

- declared rule inputs and outputs
- wildcard constraints
- helper code that invents paths, sample identity, or file meaning

**What good repair looks like**

- rule boundaries become explainable from the workflow
- helper code consumes declared inputs instead of inventing hidden ones
- a dry-run tells roughly the same story a maintainer would tell out loud

**Common false repair**

Making the helper code cleaner without restoring the missing workflow contract.

### Checkpoint discovery became folklore

**What it looks like**

- discovery "works," but another maintainer cannot say where the discovered sample set is
  recorded
- reruns are surprising because discovery state is only implicit
- checkpoint logic feels clever instead of auditable

**What is actually wrong**

Dynamic behavior is being treated as runtime magic rather than staged evidence. The
workflow has a changing graph, but the change is not being made reviewable.

**Inspect first**

- checkpoint output directories
- discovery registries or manifests
- before-and-after dry-runs

**What good repair looks like**

- discovery leaves a durable artifact another reviewer can inspect later
- the changing graph has a legible cause
- integrity checks catch malformed or partial discovery results

**Common false repair**

Adding more log lines while the actual discovery artifact remains absent or ambiguous.

### Policy leaked into workflow semantics

**What it looks like**

- the same target means different things under different profiles
- local and CI runs disagree about expected outputs, wildcards, or core parameters
- executor or storage settings quietly change analytical meaning

**What is actually wrong**

Execution policy has crossed the boundary into workflow truth. Profiles are supposed to
change how work is scheduled or provisioned, not what the workflow claims to build.

**Inspect first**

- profile files
- config ownership
- `snakemake -n` comparisons across operating contexts

**What good repair looks like**

- semantic choices move back into workflow or governed config
- profile differences stay operational and reviewable
- a policy audit can explain why a change is safe

**Common false repair**

Treating the drift as a performance issue because that feels smaller than admitting a
semantic boundary failure.

### Publish directories became output piles

**What it looks like**

- downstream users receive many files but no clear contract
- public artifacts and scratch state are mixed together
- trust depends on insider knowledge about which files "really matter"

**What is actually wrong**

The workflow can produce files without publishing a stable interface. Existence is being
mistaken for trustworthiness.

**Inspect first**

- publish bundle layout
- manifest or checksum surfaces
- the smallest downstream consumer path

**What good repair looks like**

- public outputs are explicit and smaller than the whole repository
- integrity evidence travels with the published result
- a downstream user can tell what is stable without reading workflow internals

**Common false repair**

Improving directory names while leaving the contract itself implicit.

### Repository structure hides ownership

**What it looks like**

- modules exist, but nobody agrees where the next change belongs
- helper code, rules, packages, and configs all appear to own the same behavior
- architecture reviews produce style opinions instead of boundary decisions

**What is actually wrong**

The repository has decomposition without durable ownership. Splitting files created more
surfaces, but not clearer responsibility.

**Inspect first**

- entrypoint files
- rule module boundaries
- `FILE_API.md` or equivalent contract pages
- helper package responsibilities

**What good repair looks like**

- each layer owns a smaller, stable responsibility
- file APIs explain what a module promises to produce or consume
- review questions can be routed to one obvious layer first

**Common false repair**

Creating another module or helper package before the ownership question is settled.

### Incident evidence is noisy but not reviewable

**What it looks like**

- a run was slow or surprising, but no saved evidence tells the story afterward
- incident review depends on terminal history or memory
- teams jump straight to tuning without classifying the failure

**What is actually wrong**

The workflow has runtime evidence, but not a durable review route. The problem is not
only observability; it is the absence of a stable bundle that supports later judgment.

**Inspect first**

- saved summaries
- change reports
- benchmark artifacts
- runbook or triage notes

**What good repair looks like**

- incident class is named before tuning starts
- review artifacts survive after the run completes
- maintainers can compare evidence across contexts instead of retelling the incident

**Common false repair**

Collecting more raw logs without choosing a smaller proof route.

## Repair order

Once you have identified a likely anti-pattern:

1. name the failure class in plain language
2. point to the contract, artifact, or boundary that is lying
3. choose the smallest module or capstone route that teaches the repair
4. rewrite the contract first
5. only then simplify code, directories, or implementation details

## Escalation signs

Pause and widen the review if any of these are true:

- the symptom appears in both workflow code and published outputs
- local and CI contexts disagree on what the target means
- a change requires guessing whether rules, scripts, or profiles own the fix
- the repair seems to require more narration, not less

Those usually indicate that the visible issue is a boundary problem, not an isolated bug.

## Study routes by failure class

| Failure class | Best first module | Best capstone route |
| --- | --- | --- |
| hidden workflow logic | Module 01 or Module 05 | `make walkthrough` |
| unsafe staged discovery | Module 02 | `make walkthrough` |
| policy drift | Module 03 or Module 08 | `make profile-audit` |
| weak publish contract | Module 06 | `make publish-review` |
| ownership collapse | Module 04 or Module 07 | `make architecture` |
| incident evidence failure | Module 09 or Module 10 | `make proof` |

## Companion pages

- [Boundary Review Prompts](boundary-review-prompts.md)
- [Self-Review Prompts](self-review-prompts.md)
- [Review Checklist](review-checklist.md)
- [Topic Boundaries](topic-boundaries.md)
