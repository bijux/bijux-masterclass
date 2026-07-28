# Exercises

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Reproducibility Failures in Real Teams"]
  page["Exercises"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  claim["bound the claim"] --> evidence["inventory evidence"]
  evidence --> hidden["find hidden influences"]
  hidden --> boundary["assign Git, DVC, and other owners"]
  boundary --> repair["design repair"]
  repair --> handoff["test independent explanation"]
```
<!-- page-maps:end -->

These ten exercises form one workflow-evidence lab. You will begin with two
matching local results and finish with an adoption contract another maintainer
can review without the original author's memory.

Do not answer from general DVC knowledge. Run the specimen and cite its
artifacts.

## Prepare the audit and learning packet

From the repository root:

```console
make PROGRAM=reproducible-research/deep-dive-dvc \
  capstone-workflow-evidence-audit

mkdir -p artifacts/learning/deep-dive-dvc/workflow-foundations
```

The audit is under:

```text
artifacts/audit/reproducible-research/deep-dive-dvc/workflow-evidence/
```

Create:

```text
artifacts/learning/deep-dive-dvc/workflow-foundations/
├── claim-boundary.md
├── evidence-inventory.md
├── hidden-control-finding.md
├── content-identity-finding.md
├── transformation-contract.md
├── git-dvc-boundary.md
├── runtime-recovery-review.md
├── reproducibility-decision.md
├── adoption-contract.md
└── maintainer-handoff.md
```

Link to generated audit evidence rather than copying the entire bundle.

## Exercise: Bound the repeatability claim

Inspect:

```text
workspace/same-workspace-rerun/evidence/local-run-a.json
workspace/same-workspace-rerun/evidence/local-run-b.json
workspace/same-workspace-rerun/assessment.json
```

In `claim-boundary.md`, write:

- exact observation;
- narrow claim it supports;
- stronger claim it does not support;
- missing evidence;
- evidence result: verified, contradicted, unverified, unavailable, or out of
  scope;
- one sentence that corrects “the workflow is reproducible” without discarding
  the matching reruns.

Include a digest comparison or structured JSON comparison.

**Falsification question:** What observation would contradict local
repeatability rather than merely leave team reproducibility unverified?

**Completion check:** Your conclusion distinguishes equal output in one
workspace from a clean reconstruction.

## Exercise: Inventory one trusted result

Use `risk-summary.json` as the trusted result. In `evidence-inventory.md`,
create these sections:

- result, consumer, and supported decision;
- source inputs;
- controls;
- transformations;
- runtime and external state;
- output identity and verification;
- reconstruction;
- recovery;
- unresolved proof limits.

For every influential surface, record:

| Surface | Role | Identity | Declared? | Recoverable? | Evidence result |
|---|---|---|---:|---:|---|

Use `complete-evidence/evidence/workflow-record.json` as evidence, but state
which fields are specimen assertions rather than production observations.

**Falsification question:** Which row could change the result while every
visible path remained unchanged?

**Completion check:** No source input is identified only by filename.

## Exercise: Diagnose the hidden threshold

Compare:

```text
workspace/complete-evidence/evidence/workflow-record.json
workspace/hidden-threshold/evidence/workflow-record.json
workspace/hidden-threshold/assessment.json
```

Write `hidden-control-finding.md` with:

- observed command shape;
- effective threshold;
- declared control source;
- actual control source;
- why equal local output does not repair the gap;
- smallest complete repair;
- closure proof.

Then evaluate two possible repairs:

1. require `--threshold` from `params.json`;
2. keep the environment control but record its name, value identity, owner, and
   stage influence.

State when each is appropriate.

**Falsification question:** If the environment and file both contain `0.20`,
what evidence still distinguishes the routes?

**Completion check:** Your finding names a hidden control contract, not a
general ban on environment variables.

## Exercise: Prove content identity beyond the path

Inspect:

```text
workspace/changed-input-same-path/evidence/workflow-record.json
workspace/changed-input-same-path/source/observations.csv
workspace/changed-input-same-path/assessment.json
```

Write `content-identity-finding.md` containing:

- current path;
- recorded digest;
- current digest;
- result production time relative to mutation;
- invalid inference a path-only reviewer might make;
- repair using Git or DVC;
- recovery evidence still needed after identity is recorded.

Explain why renaming the changed file does not solve historical provenance.

**Falsification question:** Can a known digest support team reproduction if no
authorized maintainer can retrieve the bytes?

**Completion check:** Identity and recovery appear as separate rows.

## Exercise: Turn manual preprocessing into a contract

Inspect:

```text
workspace/manual-preprocessing/source/observations.csv
workspace/manual-preprocessing/source/prepared-observations.csv
workspace/manual-preprocessing/evidence/workflow-record.json
workspace/manual-preprocessing/assessment.json
```

In `transformation-contract.md`, define:

- raw input identity;
- transformation behavior;
- implementation owner;
- control inputs;
- prepared output;
- failure behavior;
- evidence that the prepared file came from the raw file;
- clean reconstruction test.

Sketch a DVC stage declaration in pseudocode or YAML. It must make the
raw-to-prepared edge visible. Do not invent domain justification for removing
an observation.

**Falsification question:** Which proof is mechanical, and which approval still
belongs to a domain reviewer?

**Completion check:** The prepared file is classified as derived state rather
than a new unexplained source.

## Exercise: Draw the Git and DVC responsibility boundary

In `git-dvc-boundary.md`, map:

- scoring source;
- parameter file;
- workflow contract;
- input metadata;
- input bytes;
- pipeline declaration;
- recorded execution state;
- runtime declaration;
- shared artifact storage;
- scientific threshold approval.

Use:

| Fact | Authority | Supporting system | Evidence | Not proved |
|---|---|---|---|---|

Your map should use Git and DVC together. It must also leave runtime, storage
policy, access, and scientific validity with fitting owners.

**Falsification question:** What failure occurs if DVC metadata reaches Git but
the referenced object never reaches the shared remote?

**Completion check:** No row says “DVC owns everything reproducible.”

## Exercise: Separate runtime reconstruction from input recovery

Compare:

```text
workspace/missing-runtime/assessment.json
workspace/unrecoverable-input/assessment.json
```

Write `runtime-recovery-review.md` with two independent contracts.

Runtime contract:

- required interpreter or image identity;
- dependency evidence;
- relevant system assumptions;
- clean execution route;
- tolerated output variation.

Recovery contract:

- protected input identity;
- governed storage boundary;
- authorized credential class;
- clean-cache retrieval;
- content verification;
- retention owner.

**Falsification question:** Why can a perfect environment fail to reconstruct
an unavailable input, and a perfect input copy fail in an unknown runtime?

**Completion check:** Each contract has its own failure observation and repair.

## Exercise: Write a reproducibility decision

Assume:

- two local outputs match;
- input and implementation identities match;
- threshold is declared;
- all transformations are represented;
- runtime identity is recorded;
- no clean reconstruction was attempted;
- input is recoverable.

Write `reproducibility-decision.md` with:

- `ACCEPT_REPRODUCIBILITY_CLAIM` or
  `REJECT_REPRODUCIBILITY_CLAIM`;
- premise table;
- decisive evidence gap;
- claims still verified;
- immediate next action;
- closure proof;
- scientific and operational claims outside scope.

Then state the single new observation that would change the decision.

**Falsification question:** Can six passing premises compensate for one
required premise that was never observed?

**Completion check:** The decision does not describe the workflow as wholly
broken.

## Exercise: Design a narrow DVC adoption contract

In `adoption-contract.md`, choose one first boundary:

- incident-input content identity and shared recovery; or
- declared scoring stage with input, threshold, implementation, and output.

Write:

```text
current gap:
bounded claim:
DVC-owned evidence:
Git-owned evidence:
other owners:
acceptance route:
adversarial test:
proof limits:
later concerns deliberately excluded:
```

Include at least one change that should invalidate the stage and one that should
not.

**Falsification question:** What would show that the DVC adoption formalized an
incomplete workflow story?

**Completion check:** The contract can be implemented and reviewed
independently from experiment tracking, promotion, and deployment.

## Exercise: Prepare an independent maintainer handoff

Write `maintainer-handoff.md` for a learner who missed the session.

Give them a route to:

- run the audit;
- verify the two local results;
- find the clean-rebuild gap;
- inspect a hidden control;
- distinguish input path from identity;
- find the manual transformation;
- assign Git and DVC responsibilities;
- decide the first adoption boundary;
- state what remains unproved.

For each route, include:

| Entry | Expected evidence | Failure meaning | Owner | Proof limit |
|---|---|---|---|---|

End with three questions they must answer without your help:

1. What exactly do the matching local files prove?
2. Which evidence makes the result transferable to another maintainer?
3. Which important trust decision remains outside DVC?

**Falsification question:** Which sentence in the handoff still relies on
“everyone knows” or “ask the author”?

**Completion check:** Rewrite every such sentence into evidence, an owner, or
an explicit unknown.

## Mastery review

Your packet demonstrates Module 1 mastery when:

- claim strength grows only with evidence;
- trusted results are traced to inputs, controls, transformations, and runtime;
- paths never substitute for content identity;
- hidden state findings name causal influence;
- Git and DVC have complementary responsibilities;
- runtime reconstruction and artifact recovery stay separate;
- decisions preserve verified local evidence while rejecting overstatement;
- DVC adoption begins with one bounded state contract;
- the handoff works without private memory.

Complete all ten artifacts before reading the answer models.
