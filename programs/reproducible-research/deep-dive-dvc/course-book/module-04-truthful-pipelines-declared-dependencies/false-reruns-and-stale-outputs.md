# False Reruns and Stale Outputs


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Truthful Pipelines Declared Dependencies"]
  page["False Reruns and Stale Outputs"]
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

Not every pipeline surprise has the same severity.

Module 04 separates two failure classes:

- false reruns: DVC reruns more than the team expected
- stale outputs: DVC skips work even though the result should change

Both deserve attention. They do not deserve equal fear.

A false rerun wastes time and can make the workflow noisy. A stale output can make the
team trust a wrong result.

## False reruns

A false rerun happens when a stage reruns even though the meaningful result would not have
changed.

Common causes:

- a dependency declaration is too broad
- a whole directory is declared when only one file matters
- a generated log or timestamp file is declared as an output or dependency
- a parameter key is attached to a stage that does not actually use it
- code is organized so unrelated implementation changes touch a declared dependency

Example:

```yaml
stages:
  evaluate:
    cmd: python -m incident_escalation_capstone.evaluate
    deps:
      - data/
      - src/
    params:
      - fit.model_family
      - evaluate.threshold
    outs:
      - reports/evaluation.json
```

This stage might rerun whenever any file under `data/` or `src/` changes, even if
evaluation only reads `data/prepared/incidents.parquet` and
`src/incident_escalation_capstone/evaluate.py`.

The fix is not to remove safety. The fix is to declare the real boundary:

```yaml
deps:
  - data/prepared/incidents.parquet
  - models/escalation-model.json
  - src/incident_escalation_capstone/evaluate.py
params:
  - evaluate.threshold
```

That declaration gives DVC less noise and gives reviewers a clearer contract.

## Stale outputs

A stale output happens when a result should change but DVC has no declared reason to
rerun the stage.

Common causes:

- the command reads an undeclared file
- the command uses a hard-coded control value that belongs in `params.yaml`
- the command reads an environment variable that is not managed or recorded elsewhere
- the stage writes an output that DVC does not own
- a downstream stage reads a file produced by another stage but the file is not declared

Example:

```yaml
stages:
  inspect:
    cmd: python -m incident_escalation_capstone.inspect
    deps:
      - data/prepared/incidents.parquet
    outs:
      - reports/inspection.json
```

If `inspect` also reads `data/reference/escalation_policy.csv`, then a policy change may
not rerun inspection. The report can stay old while looking current.

The repair is direct:

```yaml
deps:
  - data/prepared/incidents.parquet
  - data/reference/escalation_policy.csv
```

Now the graph has a reason to react.

## A severity lens

Use this table when reviewing a pipeline surprise:

| Symptom | Likely class | Risk | First question |
| --- | --- | --- | --- |
| stage reruns after unrelated file change | false rerun | wasted time and review noise | is the dependency too broad? |
| stage skips after a real input change | stale output | wrong result | is a real read missing from `deps` or `params`? |
| downstream stage reruns after upstream output changed | usually correct propagation | expected recomputation | does the downstream stage depend on that output? |
| output exists but is not in `outs` | stale or orphan risk | untracked result boundary | who owns this artifact? |
| rerun happens after command text changes | usually correct | expected recomputation | did the command contract change? |

This lens keeps you from treating every rerun as bad. Sometimes the rerun is exactly the
proof that the graph is honest.

## Prefer safe noise over silent staleness

When uncertain, DVC workflows should usually prefer a visible rerun over a hidden stale
result.

That does not mean broad declarations are best. It means the review standard should be:

1. eliminate stale-output risk first
2. narrow false reruns where the boundary is understood
3. keep the declaration explainable

A pipeline that reruns too often is frustrating, but the team can observe the problem. A
pipeline that silently skips required work can corrupt downstream decisions without an
obvious warning.

## A practical diagnosis pattern

When a rerun surprises you, ask:

- Which declared dependency, parameter, output, or command text changed?
- Is that declared item truly part of this stage's result?
- If not, can the declaration be narrowed without hiding a real influence?

When a skipped rerun surprises you, ask:

- What real influence changed?
- Where should that influence be declared?
- Did the command read a path, parameter, or environment fact that the graph cannot see?
- Would the downstream result become stale if nobody noticed?

The first case is mostly contract cleanup. The second case is correctness repair.

## An empty status is conditional evidence

When `dvc status --json` returns `{}`, DVC is making a bounded claim:

> Current declared dependencies, parameters, commands, and outputs agree with recorded
> declared state.

It is not claiming:

- the command has no hidden file reads;
- every value used by the command is listed under `params`;
- every meaningful write is listed under `outs`;
- the runtime environment is equivalent to the recorded run;
- the artifact is semantically current against facts outside the graph.

The stage-contract audit makes this limitation visible. After changing the policy file,
the status receipt is:

```json
{
  "declared_input": [
    {
      "changed deps": {
        "policy/threshold.txt": "modified"
      }
    }
  ]
}
```

`hidden_input` is absent. That absence is expected from the declaration and wrong for the
real command behavior.

After deleting the undeclared receipt, status is simply:

```json
{}
```

The empty object is correct about the declared graph. It is insufficient evidence for the
larger artifact contract.

## Diagnose with a causal contrast

A single surprising stage is difficult to reason about because several explanations fit:

- DVC did not detect the change;
- the command ran but ignored the new value;
- the output was restored from cache;
- the reviewer inspected the wrong artifact;
- the declaration is complete and the change truly does not matter.

Use a paired case to remove ambiguity:

| Evidence question | Declared case | Hidden case |
| --- | --- | --- |
| Did status name the stage? | yes | no |
| Did the stage rebuild? | yes | no |
| Did the artifact adopt the current value? | yes | no |
| Is the observed difference explained by one declaration edge? | yes | yes |

The commands and input values are otherwise equivalent. The missing declaration is the
causal difference.

```mermaid
flowchart TD
  mutation["change one real influence"] --> status["capture dvc status --json"]
  status --> planned{"stage marked stale?"}
  planned -- yes --> rebuild["reproduce only that stage"]
  planned -- no --> inspect["inspect semantic value anyway"]
  rebuild --> inspect
  inspect --> current{"artifact records current value?"}
  current -- yes --> accept["accept bounded contract"]
  current -- no --> trace["trace hidden read, control, or output"]
```

The semantic-value check belongs on both paths. A stage can run and still ignore the
changed value, and a skipped stage can accidentally remain semantically valid.

## Build a stale-output receipt

For a real incident, record these fields before repairing anything:

| Field | Example from the audit |
| --- | --- |
| mutation | `policy/threshold.txt`: `10` to `20` |
| status result | only `declared_input` marked stale |
| declared output before | `threshold=10` |
| declared output after | `threshold=20` |
| hidden output after | `threshold=10` |
| decision | hidden stage is semantically stale |
| contract repair | add policy path to hidden stage `deps` |
| proof after repair | mutation marks stage stale and rebuilt value becomes `20` |

This receipt is more useful than “DVC skipped unexpectedly.” It preserves the mutation,
planner decision, artifact meaning, and intended repair.

## Avoid three false repairs

### Force the stage

`dvc repro --force hidden_input` may produce the current value once. It does not add the
missing edge. The next policy change can be missed again.

### Delete the output

Deleting a declared output creates a reason to reproduce, but the graph remains blind to
the real file or parameter influence.

### Declare an entire directory

Adding the repository root or a broad parent directory may catch the hidden file, but it
also creates unrelated reruns and obscures the intended contract. Declare the specific
influence once you know it.

The repair is complete only when the original mutation becomes visible for the right
reason.

## Review checkpoint

You understand this core when you can classify pipeline surprises without drama:

- false reruns are visible inefficiency
- stale outputs are hidden correctness risk
- downstream reruns can be correct propagation
- broad declarations should be narrowed only after the real read surface is understood
- missing declarations should be fixed before performance convenience
- an empty status is evidence about declared state, not proof that declarations are complete
- a repair must make the original mutation visible without relying on force or deletion

That distinction is one of the most important habits in Module 04.
