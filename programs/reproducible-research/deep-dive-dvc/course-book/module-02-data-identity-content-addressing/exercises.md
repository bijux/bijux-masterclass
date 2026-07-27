# Exercises


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Data Identity Content Addressing"]
  page["Exercises"]
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

Use these exercises to practice identity and state-layer judgment, not only DVC command
vocabulary. The goal is to make different trust questions stop collapsing into "the repo"
or "the data."

## How to work through this set

Treat the ten exercises as one full lab day on state authority and recovery boundaries.

Before each answer:

1. name the trust question you are trying to answer
2. decide which layer should answer it first
3. explain what that layer can and cannot prove by itself

If you skip the layer question, DVC pointers, cache objects, workspace files, remotes,
and published bundles all blur together.

Do the exercises in order. The day is one progression:

- Exercises 1-3 separate paths, identity, and state-authority questions
- Exercises 4-6 explain DVC commands as state moves and inspect pointers by hand
- Exercises 7-8 test checkout and remote recovery honestly
- Exercises 9-10 diagnose missing objects and draw a full authority diagram

Keep one state-authority packet as you go. By the end of the day it should contain:

- one explanation of why a path is weaker than identity
- one plain-language separation of pointer, cache, and workspace
- one authoritative-layer table
- one hand inspection of a pointer and its cache object
- one empty-cache remote recovery drill
- one state-authority diagram with commands and recovery claims

If those six artifacts are missing, you are probably memorizing DVC terms instead of
learning how the layers answer different questions.

## Recommended working layout

If you want one lab tree that can support the whole day, use something like:

```text
module02-lab/
├── data/
├── dvc.yaml
├── notes/
├── publish/
└── artifacts/
```

Keep one authority table while you work:

| Question | First authoritative layer | Evidence route | What it still cannot prove |
| --- | --- | --- | --- |

Also keep one state-move table:

| Command | Layer changed | New trust added | Trust not added |
| --- | --- | --- | --- |

Those two tables matter because Module 02 is where many students first stop treating all
copies of "the data" as equivalent.

```mermaid
flowchart LR
  path["distinguish path from identity"]
  layer["separate pointer, cache, workspace, remote"]
  move["explain commands as state moves"]
  inspect["inspect pointer and cache by hand"]
  recover["test bounded recovery honestly"]
  publish["state who is authoritative for what"]

  path --> layer --> move --> inspect --> recover --> publish
```

Use that route on purpose. It keeps the day centered on trust and authority instead of on
surface-level command memory.

## Exercise 1: Explain why the path is too weak

A teammate says:

> The dataset is `data/train.csv`, so as long as that file exists, the identity problem is solved.

Write a short response that explains:

- what the path does tell you
- what it does not tell you
- why that difference matters for reproducibility
- one sentence explaining when the path is still useful

Study note:
The point is not to dismiss paths. The point is to stop mistaking location for identity.

## Exercise 2: Separate pointer, cache, and workspace

Suppose you have run `dvc add data/raw.csv`.

Explain in plain language:

- what the `.dvc` file is doing
- what the cache is doing
- why the workspace file is still a different layer from both
- one sentence explaining why calling the pointer "the data" is misleading

Your answer should avoid jargon where possible.

Study note:
This exercise is about conceptual clarity. If the language stays fuzzy here, later remote
and recovery reasoning will also stay fuzzy.

## Exercise 3: Name the authoritative layer

For each question below, say which layer you would inspect first:

1. what did the pipeline actually record as executed?
2. what may a downstream reviewer safely trust?
3. what survives local cache loss?
4. what files are visible in the working tree right now?

Use the vocabulary from the module rather than generic phrases like "the repo."

What to hand in:

- the four layer assignments
- one sentence per assignment explaining why that layer comes first
- one sentence explaining why the same answer would be wrong for a different question

Study note:
This is where many students realize that "where should I look?" is itself a trust
question.

## Exercise 4: Explain the commands as state moves

Write a short explanation of what changes when you run:

- `dvc push`
- `dvc pull`
- `dvc checkout`

Your answer should focus on which layer each command affects and what new trust it adds or
does not add.

What to hand in:

- the three command explanations
- one sentence explaining which command helps recovery most directly
- one sentence explaining which command does not prove durability by itself

Study note:
The commands matter less than the state movement they perform.

## Exercise 5: Diagnose a recovery claim

A team says:

> We rebuilt the workspace after deleting local files, so the published release and the full repository are both fully proven.

Explain:

- what this recovery success does prove
- what it does not prove yet
- which additional boundary the team may be confusing with recovery
- one sentence explaining why bounded proof is still valuable

Study note:
Recovery is strong evidence. It is just not infinite evidence.

## Midday self-check

Before you move into pointer inspection, revision switching, and missing-object diagnosis,
make sure your packet can already answer these questions cleanly:

- why a path is weaker than identity
- what each of pointer, cache, and workspace contributes to the workflow story
- which layer you would inspect first for at least two different trust questions
- what kind of claim a recovery success still cannot justify

If you cannot answer those four questions in plain language, return to Exercises 1-5 and
make the packet more explicit before continuing.

## Exercise 6: Predict the identity audit

Before running any command, inspect `capstone/repro/data-identity/README.md` and predict
the result of all seven findings:

- pointer names cached content
- same bytes share identity
- changed bytes change identity
- cache restores workspace
- remote restores after cache loss
- remote recovery preserves identity
- pointer only is not recoverable

For each prediction, name the minimum evidence that would make it defensible.

Then run:

```bash
make -C programs/reproducible-research/deep-dive-dvc/capstone data-identity-audit
```

What to hand in:

- a prediction table written before execution
- the generated `summary.tsv`
- corrections for every wrong prediction
- one sentence explaining why `PASS / REJECT` is expected for the pointer-only row

Study note:
Prediction exposes whether you understand the layer model before command output supplies
the answer.

## Exercise 7: Disprove path-based identity

Use only the `same-content` and `changed-content` workspaces.

Build a causal contrast with these columns:

| Case | Path changed? | Bytes changed? | Pointer ID changed? | Conclusion |
| --- | --- | --- | --- | --- |

Quote the actual paths and pointer IDs. Do not replace them with “same” or “different.”

What to hand in:

- both pointer files from the same-content case
- before and after content IDs from the changed-content case
- the completed contrast table
- a two-sentence argument showing why neither path change nor path stability defines
  identity

Study note:
The two cases belong together. Each controls the variable changed by the other.

## Exercise 8: Trace cache and remote recovery

Compare `cache-recovery` with `remote-recovery`. For each case, identify:

1. which local layer was deleted
2. which storage layer supplied the bytes
3. which command receipt records the move
4. which digest check validates the result
5. whether the local cache exists afterward

What to hand in:

- a layer-by-layer timeline for both cases
- the relevant checkout, push, and pull receipts
- the restored content ID and SHA-256
- one sentence stating what cache-only recovery cannot prove about the remote
- one sentence stating why remote recovery after cache deletion is stronger than push
  success

Study note:
Do not infer the source of recovered bytes from the final workspace alone.

## Exercise 9: Diagnose pointer-only failure

Open:

```text
workspace/pointer-only/data/observations.csv.dvc
evidence/pointer-only-checkout.stderr.txt
report.json
```

Classify the incident as projection failure, availability failure, identity disagreement,
or a combination. Defend the classification from the saved surfaces.

What to hand in:

- the content ID that remains recorded
- the checkout return code and essential stderr meaning
- cache and workspace existence checks
- the failure classification
- one repair that would preserve identity
- one tempting action that would conceal the missing-object problem

Study note:
A valid pointer can outlive every accessible copy of the bytes it names.

## Exercise 10: Defend a bounded recovery claim

Prepare a six-item reviewer packet from the generated bundle. It must include:

- summary
- original pointer
- state-move receipts
- restored cache evidence
- restored workspace digest
- pointer-only negative control

Draw a diagram that distinguishes identity authority from content availability. Then write
a review conclusion using this structure:

> After loss of ___, storage layer ___ supplied content ID ___. Evidence ___ confirms the
> restored bytes. Counterexample ___ rules out ___. This proves ___. It does not prove
> ___.

What to hand in:

- the six-item packet inventory
- the authority-and-availability diagram
- the completed bounded conclusion
- one follow-up proof required before downstream publication

Study note:
The final exercise is not a command recital. It is a review argument another maintainer
can verify without oral context.

## Mastery check

You have a strong grasp of this module if your answers consistently keep four ideas
visible:

- paths are locators, not identity
- content identity needs recorded references and storage layers
- different repository layers answer different trust questions
- recovery is a bounded proof, not a magic guarantee about everything
