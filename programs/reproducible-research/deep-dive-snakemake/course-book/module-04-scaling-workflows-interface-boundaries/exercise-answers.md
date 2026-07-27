# Exercise Answers

Use this page after you have written your own answers. The point is comparison, not
copying.

## How to use the answer page well

Do not read a model answer first and then rebuild your exercise to match it.

A better rhythm is:

1. complete the exercise with your own repository tree and evidence
2. write one plain-language explanation of the boundary you are protecting
3. compare that explanation with the model answer
4. revise where the model answer exposes hidden ownership or a missing review surface

The goal is not identical wording. The goal is explicit repository reasoning about growth.

The strongest Module 04 answers usually do four things:

- they name the owning boundary directly
- they explain why the proposed split or contract is strong or weak
- they choose one proportionate review surface
- they describe the repair in terms of repository clarity, not architecture fashion

The strongest self-study packets also leave behind six concrete artifacts:

- one ownership map
- one before-and-after entrypoint view
- one include-versus-module decision note
- one public file contract excerpt
- one gate table tied to claims
- one rejected abstraction note

If your answer page comparisons rely only on folder names and intuition, the structural
reasoning is still too implicit.

## Exercise 1: Name the current ownership problem

A strong answer starts by mapping the existing concerns before changing any files.

Example:

> The current `Snakefile` mixes preprocessing, summarization, publication, and report
> assembly in one flat surface. That hides ownership because a reviewer cannot tell which
> rules belong together or which concern should absorb the next change. The workflow is
> still one graph because all of those concerns contribute to one top-level target story,
> but the file arrangement no longer teaches that story clearly.

Why this is strong:

- it explains the existing ownership problem before refactoring
- it distinguishes one graph from one file

## Exercise 2: Choose one healthy include split

A strong answer sounds like this:

> The workflow should split its publish logic into `workflow/rules/publish.smk` because
> that file can own one clear concern: promotion of reviewed internal results into the
> public boundary. This improves named ownership while keeping the top-level orchestration
> visible. It is not yet a module because the repository still owns one visible graph and
> the split is about internal organization rather than reusable external interface.

Why this is strong:

- it names one real concern
- it distinguishes an include-level split from a module-level split

The missing but important sentence is usually this one:

> After the split, the top-level `Snakefile` still explains configuration, major rule
> families, and the final contract without sending the reader on a scavenger hunt.

## Exercise 3: Prove the graph stayed visible

A strong answer compares graph visibility before and after the split rather than treating
the refactor as successful by default.

Example:

> The before and after rule graphs preserve the same high-level dependency story, but the
> after version makes it easier to see where publication begins and where preprocessing
> ends. A warning sign would be needing to open several files before understanding the
> top-level target route that the original graph showed immediately.

Why this is strong:

- it uses the graph as a review surface, not decoration
- it names one criterion for "too much hiding"

## Exercise 4: Decide whether a boundary is a module

The first caller remains:

```python
use rule normalize from normalize as normalize_sample with:
    input:
        source="data/sample.txt"
    output:
        artifact="build/sample.txt"
    params:
        prefix=config["normalize"]["prefix"]
```

Add the control policy to `config.yaml`:

```yaml
normalize:
  prefix: reviewed
  control_prefix: control-reviewed
```

Then add the second caller:

```python
use rule normalize from normalize as normalize_control with:
    input:
        source="data/control.txt"
    output:
        artifact="build/control.txt"
    params:
        prefix=config["normalize"]["control_prefix"]
```

Add both outputs to `all`:

```python
rule all:
    input:
        rules.normalize_sample.output.artifact,
        rules.normalize_control.output.artifact,
    default_target: True
```

The important result is not merely that the syntax parses. The module implementation did
not change. The new caller bound every consumer-visible surface.

A useful override matrix is:

| Surface | Module template | Sample caller | Control caller | Owner |
| --- | --- | --- | --- | --- |
| input | `unbound.txt` | `data/sample.txt` | `data/control.txt` | caller |
| output | `unbound.txt` | `build/sample.txt` | `build/control.txt` | caller |
| prefix | `UNBOUND` | `reviewed` | `control-reviewed` | caller |
| shell | normalize and publish | unchanged | unchanged | module |
| candidate rename | required | unchanged | unchanged | module |

Expected rule-list evidence includes:

```text
all
normalize_control
normalize_sample
```

The dry-run should plan two normalization jobs. The artifacts should begin:

```text
build/sample.txt: reviewed
build/control.txt: control-reviewed
```

Now remove the `params` block from `normalize_control`. A useful gate fails because the
caller contract is incomplete, even if someone changes the module default to preserve the
same bytes. Matching bytes do not prove matching ownership.

The correct decision is to keep the module if both callers remain expressible without
private module edits. A limit remains: this evidence does not prove compatibility across
independently versioned remote module releases.

## Exercise 5: Write a public file contract

A strong answer sounds like this:

> `publish/v1/summary.json` is a stable public output describing the run-level summary,
> while `results/sampleA/qc_raw.tsv` remains internal workflow state. A change to the
> published summary keys or semantics would require explicit interface review because it
> affects downstream trust, not just internal orchestration.

Why this is strong:

- it distinguishes public from internal paths clearly
- it explains what kind of change becomes an interface event

## Exercise 6: Review one abstraction you should reject

Begin with the actual summary row:

```text
hidden-coupling  PASS  HIDDEN_MODULE_COUPLING_REPRODUCED
```

The row is green because the promised defect was observed. It is not an approval.

The decisive observations in `report.json` are:

```text
broad_module_config: true
caller_binds_policy: false
module_reads_private_policy: true
artifact_lines: ["inherited", "sample payload"]
```

The rule listing and dry-run are still useful:

```text
all
normalize_sample
```

They prove that the imported rule is visible and planned. They cannot identify policy
ownership because both explicit and hidden models have the same graph shape.

A repair has three coordinated edits:

1. Move the policy into an owned config subtree.
2. Pass only that subtree to the module.
3. Bind the policy at the caller's `use rule` site.

```python
module normalize:
    snakefile: "module/Snakefile"
    config: config["normalize"]

use rule normalize from normalize as normalize_sample with:
    input:
        source="data/sample.txt"
    output:
        artifact="build/sample.txt"
    params:
        prefix=config["normalize"]["prefix"]
```

The module then uses a placeholder instead of reading caller-private policy:

```python
params:
    prefix="UNBOUND"
```

After repair, the old hidden-coupling finding should fail. That failure is correct because
the specimen no longer reproduces its named defect. Reclassify it as an explicit control
only after its expected finding and tests change deliberately.

The abstraction is rejected because it hides consumer-visible policy, not because modules
are inherently risky.

## Exercise 7: Break and defend a schema boundary

The valid fixture passes a schema that describes required fields, types, and allowed
values. Renaming a required field fails the targeted contract check even when the file is
valid JSON or TSV. That failure is correct: parseability is weaker than compatibility,
and a consumer-visible field change requires deliberate versioning or migration.

The strongest answers also name the broken consumer clearly: for example, a downstream
report generator, dashboard loader, or bundle validator that trusts the documented field
names and would silently misread or reject the changed surface.

## Exercise 8: Keep resources portable while scaling

Rules declare abstract needs such as threads, memory, and runtime. A local profile maps
them to bounded workstation execution; a cluster profile maps the same needs to scheduler
resources. Neither rule contains a queue name or submission command. The invariant is that
resource policy can change without changing target paths, algorithms, or output semantics.

Good answers also point to one place where scheduler folklore was kept out on purpose,
such as refusing to hardcode queue names, partition names, or submission flags inside the
rule body.

## Exercise 9: Review a full structural pull request

A strong review starts with findings ordered by trust impact.

Example:

1. **High:** the proposed module receives the full workflow config and privately reads the
   publish version. That value changes output meaning but is absent from the caller
   binding. Narrow config and bind the value through `use rule` before approval.
2. **High:** the public summary schema removed a required field without versioning.
   Contract validation correctly rejects the changed fixture.
3. **Medium:** the include split preserves all rules but makes the top-level target route
   harder to locate. Restore one visible orchestration surface.
4. **Low:** the new local imported rule name is ambiguous beside an existing rule. Rename
   it at the caller boundary.

The review packet should contain:

- before-and-after rule lists or rulegraphs
- dry-run paths for the final target
- module-interface `summary.tsv`
- the relevant source observations from `report.json`
- one module mutation that the selftest rejects
- valid and invalid public contract fixtures
- the exact validator failure

Use a claim table to prevent gate inflation:

| Gate | Claim defended | Required failure example |
| --- | --- | --- |
| rule list or rulegraph | intended rule families remain visible | imported local rule disappears |
| dry-run | final target still selects intended paths | caller output binding drifts |
| module interface audit | config, path, and policy ownership match the model | broad config in explicit control |
| module interface selftest | the gate discriminates | dishonest mutation exits nonzero |
| schema validation | public consumers receive the promised shape | required field disappears |

The acceptance conclusion should separate decisions:

> Accept the ownership-based include split. Request repair of the broad module config and
> incompatible schema change. Retain the narrow interface and schema gates. Do not add a
> second end-to-end job because the unresolved claims already have focused rejection
> routes.

This answer is stronger than "CI passed" because every judgment cites evidence and every
gate names the lie it should reject.

## Exercise 10: Rehearse the next month of growth

A strong answer predicts future landing places from the current structure rather than
inventing a new structure on the spot. If a new assay, report, or publish artifact already
has an obvious owning boundary, the current design is working. If every imagined change
requires reopening the whole directory strategy, the repository is not scaled yet even if
the current diff looks neat.

The healthiest answers sound calm here. They can say where the next concern lands, what
gate reruns, and what sign would trigger another redesign without pretending the current
tree is timeless.

## What all ten answers should have in common

The best Module 04 answers usually:

1. split by named ownership rather than by file length
2. promote boundaries into modules only when the interface is explicit
3. distinguish internal workflow state from public file contracts
4. choose proof routes that defend the actual scaling boundary under review

Weak answer pattern:

- "the repository is more modular now, so the structure must be better"

That sentence skips ownership, interface, public contract, and proof surfaces all at
once. If your answers still sound like that, keep revising.

If your answers do those four things, the module is landing in the right direction.
