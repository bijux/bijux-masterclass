# Dependency, Parameter, and Output Boundaries


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Truthful Pipelines Declared Dependencies"]
  page["Dependency, Parameter, and Output Boundaries"]
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

The hardest part of a truthful DVC stage is often not the command. It is the boundary
judgment around the command.

Learners need to decide:

- which files are real dependencies
- which values are parameters rather than code details
- which artifacts are outputs owned by the stage
- which files are temporary scratch and should not become part of the public graph

These decisions make `dvc repro` predictable. They also make review conversations less
vague, because the team can point to the exact field that carries the claim.

## Dependencies are real reads

A dependency is something the command reads to produce its result.

Good dependency questions are concrete:

- Would changing this file possibly change the output?
- Would removing this file make the command fail or produce a different result?
- Does the command read this path directly or through a library call?
- Is this source file part of the implementation that should trigger rerun when changed?

Example:

```yaml
stages:
  evaluate:
    cmd: python -m incident_escalation_capstone.evaluate
    deps:
      - data/prepared/incidents.parquet
      - models/escalation-model.json
      - src/incident_escalation_capstone/evaluate.py
    params:
      - evaluate.threshold
    outs:
      - reports/evaluation.json
```

This tells the reviewer that evaluation depends on the prepared data, the model, the
evaluation implementation, and a threshold value. If the command also reads
`data/reference/team_roster.csv`, the declaration is incomplete.

That missing file is not a small clerical issue. It means `dvc repro` may skip evaluation
after a roster change even though the report is stale.

## Parameters are reviewable controls

Parameters are not just variables. They are values the team wants to change, compare, and
review as controls.

Good parameter candidates include:

- thresholds
- train/test split values
- random seeds
- model family choices
- feature toggles
- filtering limits

Bad parameter candidates include values that are only implementation plumbing or values
that would be clearer as ordinary code constants.

The key question is:

> If this value changed, would a reviewer want the pipeline to notice and the history to
> explain it?

If yes, it probably belongs in `params.yaml` and under the stage's `params`.

Example:

```yaml
# params.yaml
fit:
  model_family: logistic_regression
  regularization: 0.2
  random_seed: 20260411
```

```yaml
# dvc.yaml
stages:
  fit:
    cmd: python -m incident_escalation_capstone.fit
    deps:
      - data/prepared/incidents.parquet
      - src/incident_escalation_capstone/fit.py
    params:
      - fit.model_family
      - fit.regularization
      - fit.random_seed
    outs:
      - models/escalation-model.json
```

Now a change to `fit.regularization` is not hidden inside Python. It becomes a declared
control change.

## Outputs are owned artifacts

An output is an artifact the stage is responsible for producing.

Good output questions:

- Does this stage create or replace the artifact?
- Would downstream stages treat this artifact as an input?
- Should DVC record the content identity of this artifact?
- Would losing this artifact require rerunning this stage or restoring from cache?

Outputs should be specific enough to make ownership clear. A broad output directory can
be right when the stage truly owns the whole directory. It is risky when multiple stages
write into the same directory.

Weak:

```yaml
outs:
  - reports/
```

Clearer:

```yaml
outs:
  - reports/evaluation.json
  - reports/error-slices.csv
```

The clearer version says exactly what the evaluation stage owns.

## Scratch space is not an output contract

Many commands create temporary files while they run.

Not every temporary file belongs in `outs`. If a file is purely scratch, the better design
is often to keep it under an internal work directory and remove it or keep it outside the
review contract.

The danger is accidental reliance:

```mermaid
flowchart LR
  prepare["prepare stage"] --> scratch["tmp/features.cache"]
  scratch -. "not declared" .-> fit["fit stage reads it"]
  prepare --> declared["data/prepared/incidents.parquet"]
  declared --> fit
```

In this diagram, `fit` has a hidden dependency on scratch. The pipeline may appear to
work on one machine and break or go stale on another.

If the file matters to a later stage, promote it into a declared output of the producer
and a declared dependency of the consumer. If it does not matter, keep later stages from
reading it.

## A placement table for review

| Influence | Best placement | Why |
| --- | --- | --- |
| raw CSV read by a command | `deps` | content change should influence rerun |
| Python module containing the command behavior | `deps` | implementation change should be visible |
| threshold chosen by the team | `params` | control change should be reviewable |
| model file produced by training | `outs` | DVC should record and restore it |
| log file used only for debugging | usually outside `outs` | it is not part of the result contract |
| shared feature file used downstream | producer `outs`, consumer `deps` | ownership and use must both be declared |

The table is not a law book. It is a way to slow down and ask the right question.

## Decide from the consequence of change or loss

Names such as `config`, `metadata`, `log`, and `cache` are weak placement evidence. Ask
what should happen when the item changes or disappears.

| If this happens... | And the stage should... | Declare it as... |
| --- | --- | --- |
| file contents change | become stale | `deps` |
| reviewed control value changes | become stale and expose the changed key | `params` |
| produced artifact disappears | become stale or restore the artifact | `outs` |
| diagnostic file disappears | remain valid because nobody relies on it | scratch or operational residue |
| code implementation changes | become stale | a code path in `deps` |
| environment fact changes | follow an external environment contract | not silently ignored |

The decision is about the pipeline response, not the file extension.

### A policy file is a dependency even when it looks like configuration

In the stage-contract specimen, both input stages read
`policy/threshold.txt`. Only one lists it:

```yaml
deps:
  - data/source.txt
  - policy/threshold.txt
  - scripts/render.py
```

Changing the policy to `20` makes that stage stale. The stage that omits the path keeps a
result containing `threshold=10`.

The policy file is not a parameter in this specimen because the command consumes the file
as a file dependency. The important point is not that policy must always use `deps`. The
important point is that the chosen contract must let DVC detect the influence.

### A parameter file is not automatically a parameter contract

This declaration is incomplete:

```yaml
cmd: python scripts/render.py param --params params.yaml
deps:
  - data/source.txt
  - scripts/render.py
outs:
  - results/hidden-param.txt
```

The command visibly receives `params.yaml`, but DVC does not infer which key matters from
the command line or from Python behavior. The truthful declaration adds:

```yaml
params:
  - settings.multiplier
```

After the value changes from `2` to `3`, the audit demonstrates the consequence:

| Stage | Listed key? | DVC marks stale? | Value after declared rebuild |
| --- | --- | --- | --- |
| `declared_param` | yes | yes | `multiplier=3`, `score=24` |
| `hidden_param` | no | no | `multiplier=2`, `score=16` |

This is why “we put controls in one YAML file” is not a sufficient reproducibility claim.
The stage still has to declare the part of that control surface it uses.

### A sidecar is an output when its absence matters

Suppose a command writes:

```text
results/declared-main.txt
results/undeclared-receipt.txt
```

The receipt might be:

- disposable debug residue;
- a quality-control receipt reviewed before promotion;
- a row-count contract consumed by another stage;
- an audit record required after an incident.

Only the first case is clearly scratch. In the other cases, deleting the receipt should
invalidate something or trigger restoration. The audit proves that DVC does neither when
the path is outside `outs`.

Use this ownership test:

1. Delete the artifact in a disposable workspace.
2. Run `dvc status --json`.
3. Run `dvc repro <producer>`.
4. Ask whether the artifact is restored.
5. If not, decide whether that is the intended contract.

The test does not force every side effect into `outs`. It forces the team to make the
meaning of absence explicit.

## Build an influence ledger before editing YAML

For a real stage, create this table from command behavior:

| Path or value | Read, write, or control? | Meaningful change or loss | Required DVC response | Placement |
| --- | --- | --- | --- | --- |
| `data/source.csv` | read | rows change | rerun | `deps` |
| `policy/threshold.txt` | read | decision policy changes | rerun | `deps` |
| `settings.multiplier` | control | scoring changes | rerun and record key | `params` |
| `results/report.json` | write | report missing | rerun or restore | `outs` |
| `logs/debug.txt` | write | debug history missing | no pipeline response | outside contract |

Do not fill the placement column first. If you start from existing YAML, you are likely to
restate the declaration instead of auditing the command.

```mermaid
flowchart LR
  command["inspect real reads and writes"] --> consequence["name change or loss consequence"]
  consequence --> response["state required DVC response"]
  response --> placement["choose deps, params, outs, or external contract"]
  placement --> pressure["test one mutation"]
```

The pressure test closes the loop. A placement that looks reasonable but produces the
wrong response is not yet a truthful boundary.

## Review checkpoint

You understand this core when you can inspect one command and separate:

- real reads from convenient nearby files
- reviewable controls from ordinary implementation detail
- owned outputs from temporary run artifacts
- shared intermediates from accidental leftovers
- values stored in `params.yaml` from keys actually declared by the stage
- disposable side effects from artifacts whose absence should invalidate the result

The goal is simple: after reading `dvc.yaml`, a reviewer should understand what can
legitimately change the result and where that change is recorded.
