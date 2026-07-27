# Worked Example: Repairing a Deceptive Pipeline


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Truthful Pipelines Declared Dependencies"]
  page["Worked Example: Repairing a Deceptive Pipeline"]
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

This example shows how Module 04 fits together when a pipeline looks reasonable but the
graph is not telling the full truth.

The goal is not to make the YAML longer. The goal is to make the result explainable.

## The situation

A team has a small incident escalation pipeline:

```yaml
stages:
  prepare:
    cmd: python -m incident_escalation_capstone.prepare
    deps:
      - data/raw/service_incidents.csv
    outs:
      - data/prepared/incidents.parquet
  fit:
    cmd: python -m incident_escalation_capstone.fit
    deps:
      - data/prepared/incidents.parquet
    outs:
      - models/escalation-model.json
  evaluate:
    cmd: python -m incident_escalation_capstone.evaluate
    deps:
      - models/escalation-model.json
    outs:
      - reports/evaluation.json
```

The graph looks tidy: prepare, fit, evaluate.

But you notice something uncomfortable. The evaluation report changes between two manual
runs even though DVC does not see a reason to rerun evaluation.

That is the Module 04 alarm bell:

> A tidy graph can still be deceptive.

## Step 1: Read the command, not the stage name

The weak review says:

> The stage is named `evaluate`, so it probably evaluates the model.

The stronger review asks:

> What does the command actually read?

You inspect `evaluate.py` and find these reads:

- `models/escalation-model.json`
- `data/prepared/incidents.parquet`
- `data/reference/escalation_policy.csv`
- `params.yaml` key `evaluate.threshold`

Only one of those is declared. The stage can skip after a data or policy change because
DVC only knows about the model dependency.

## Step 2: Separate dependency from parameter

You do not dump everything into `deps`.

The prepared data and policy CSV are file reads, so they belong in `deps`.

The threshold is a reviewed control value, so it belongs in `params`.

The repaired evaluation stage becomes:

```yaml
stages:
  evaluate:
    cmd: python -m incident_escalation_capstone.evaluate
    deps:
      - models/escalation-model.json
      - data/prepared/incidents.parquet
      - data/reference/escalation_policy.csv
      - src/incident_escalation_capstone/evaluate.py
    params:
      - evaluate.threshold
    outs:
      - reports/evaluation.json
```

Now a reviewer can explain what should make evaluation stale.

## Step 3: Check the producer-consumer edge

You now ask whether `data/prepared/incidents.parquet` is owned correctly.

The `prepare` stage already lists it in `outs`, and `evaluate` now lists it in `deps`.
That creates a real edge:

```mermaid
flowchart LR
  raw["raw incidents"] --> prepare["prepare"]
  prepare --> prepared["prepared incidents"]
  prepared --> fit["fit"]
  prepared --> evaluate["evaluate"]
  policy["escalation policy"] --> evaluate
  fit --> model["model"]
  model --> evaluate
```

The graph now says: evaluation depends on the model, prepared incidents, and policy.

That is a better causal story than "evaluation depends on the model."

## Step 4: Predict rerun behavior

Before running anything, you write predictions:

- if `evaluate.threshold` changes, only evaluation should rerun
- if `data/reference/escalation_policy.csv` changes, evaluation should rerun
- if `data/raw/service_incidents.csv` changes and preparation changes its output, fitting and evaluation should rerun downstream
- if `fit.model_family` changes, fitting should rerun and evaluation should rerun because the model output changed

This prediction is the learning moment. It turns `dvc repro` from a button into a check
against your mental graph.

## Step 5: Compare against lock evidence

After running `dvc repro`, you inspect `dvc.lock`.

The useful question is not "did a lock file change?"

The useful questions are:

- does `evaluate` now record the policy CSV dependency?
- does it record the threshold value?
- does it record the prepared dataset dependency?
- does the output hash update when the report really changes?

If yes, the repair is now visible in recorded evidence.

## Step 6: Narrow broad declarations only after safety

During review, someone proposes:

```yaml
deps:
  - data/
```

That would make policy changes visible, but it would also make the stage rerun for
unrelated files. The team rejects that as too broad because they now know the real read
surface.

The final declaration is narrower and safer:

```yaml
deps:
  - models/escalation-model.json
  - data/prepared/incidents.parquet
  - data/reference/escalation_policy.csv
  - src/incident_escalation_capstone/evaluate.py
params:
  - evaluate.threshold
```

This is the best Module 04 outcome: not maximum YAML, but honest YAML.

## The review note you would want

> Evaluation was previously deceptive because the command read prepared incidents, a
> policy CSV, and a threshold value that were not declared on the stage. That created stale
> output risk: DVC could skip evaluation after a meaningful input or control change. The
> repair adds the missing file reads to `deps`, adds the threshold to `params`, and keeps
> the output ownership unchanged. The graph now explains reruns from declared state, and
> `dvc.lock` can record the evidence needed for review.

That note is stronger than "fixed dvc.yaml" because it names the risk and the repair.

## Execute the same reasoning on the specimen

The conceptual repair above names the right fields. The stage-contract audit lets you
test the same reasoning without inventing evidence.

Run:

```bash
make PROGRAM=reproducible-research/deep-dive-dvc capstone-stage-contract-audit
```

Open the generated bundle and use this order:

1. `STAGE_CONTRACT_AUDIT_GUIDE.md`
2. `workspace/baseline/dvc.yaml`
3. `summary.tsv`
4. `evidence/input-change-status.stdout.txt`
5. `workspace/input-change/results/`
6. `evidence/param-change-status.stdout.txt`
7. `workspace/param-change/results/`
8. `workspace/output-loss/results/`
9. `report.json`

Do not start with `report.json`. The compact report is useful after you understand the
raw DVC and artifact evidence.

### Predict the decisions

Before reading `summary.tsv`, complete this table:

| Finding family | Your prediction | Evidence that would change your mind |
| --- | --- | --- |
| baseline convergence | accept or reject | second run unexpectedly executes a stage |
| declared file influence | accept or reject | status omits `declared_input` |
| hidden file influence | accept or reject | hidden output adopts `20` without a declared edge |
| declared parameter | accept or reject | status omits `declared_param` |
| hidden parameter | accept or reject | hidden output adopts `3` without a declared key |
| undeclared receipt | accept or reject | deletion makes the stage stale or repro restores it |

The expected answer is not “all pass.” Some findings intentionally reproduce behavior
that should be rejected.

### Follow the file mutation

Read `evidence/input-change-status.stdout.txt`. Its JSON names the modified policy path
under `declared_input`.

Then compare:

```text
workspace/input-change/results/declared-input.txt
workspace/input-change/results/hidden-input.txt
```

The first contains `threshold=20`; the second contains `threshold=10`.

Write the reasoning without using the words “DVC bug”:

> DVC reacted consistently with each declaration. The declared stage exposed the policy
> path, became stale, and rebuilt with the current value. The hidden stage read the same
> path but omitted it from `deps`, so its old value remained compatible with the declared
> graph. The defect is the stage contract.

That distinction matters. Blaming the tool would hide the repair location.

### Follow the parameter mutation

Read `evidence/param-change-status.stdout.txt`. DVC represents the modified parameter
under the declared stage.

Then inspect:

```text
declared-param.txt  multiplier=3  score=24
hidden-param.txt    multiplier=2  score=16
```

The arithmetic makes semantic staleness reviewable. The hidden output is not just missing
a metadata update; it contains a score derived from an obsolete control value.

### Follow the missing output

In `workspace/output-loss/results/`, the main result exists and the receipt does not.
`evidence/output-loss-status.stdout.txt` contains an empty JSON object, and
`evidence/output-loss-repro.stdout.txt` says the stage did not change.

Now make the ownership decision:

- If the receipt is required for review, add it to `outs` and prove deletion is detected.
- If it is scratch, rename or relocate it so consumers do not mistake it for durable
  evidence.
- If another stage consumes it, declare producer ownership and consumer dependency.

“The script happens to write it” is not an ownership decision.

## Write a bounded acceptance argument

A strong conclusion separates observation, inference, and limit:

> On the local five-stage specimen, DVC 3.67.1 detected the modified file and parameter
> only for stages that declared those influences. Reproducing the declared stages moved
> their stored values from `10` to `20` and from `2` to `3`; paired hidden stages retained
> the old values. Deleting an undeclared receipt produced no status change and did not
> restore the file. These observations support the claim that the declarations govern
> DVC’s response. They do not prove that every stage in another repository has a complete
> contract; that requires comparing each real command’s reads and writes against its own
> declaration.

The scope sentence prevents a useful specimen from becoming an universal claim.

## Preserve a review packet

Your worked-example packet should contain:

- the original stage declaration;
- a ledger of real reads, controls, and writes;
- predicted status and rerun behavior;
- raw status receipt;
- before and after semantic values;
- repaired declaration;
- repeated mutation showing the repair works;
- one explicit limit on what the evidence establishes.

Without the repeated mutation, the repair remains plausible rather than demonstrated.

## Why this is a mastery example

This one story exercises the whole module:

- Core 1: the stage contract was read as a promise, not a label
- Core 2: dependencies and parameters were placed differently
- Core 3: rerun predictions were checked against lock evidence
- Core 4: stale-output risk was prioritized before false rerun cleanup
- Core 5: the producer-consumer edge for the prepared data was made explicit
- executable proof: planner decisions were joined to current and stale artifact values
- review discipline: the conclusion states both demonstrated behavior and evidence limits

The pipeline became more trustworthy because the declared graph became closer to the real
work.
