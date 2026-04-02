# Inspection Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  inspect["inspect"] --> summary["summary.txt"]
  inspect --> rules["rules.txt"]
  inspect --> history["history.txt"]
  summary --> snapshot["Policy snapshot"]
  rules --> lifecycle["Rule lifecycle state"]
  history --> incidents["Incident history"]
  snapshot --> review["Review ownership and projections"]
  lifecycle --> review
  incidents --> review
```

```mermaid
flowchart LR
  question["Choose the state question"] --> command["Run the inspect bundle route"]
  command --> output["Read the saved learner-facing files"]
  output --> owner["Name the owning object or projection"]
  owner --> next["Decide whether you need tests, demo, or proof next"]
```
<!-- page-maps:end -->

Use this guide when you want to inspect the capstone state without opening implementation
files first. The goal is to make each inspection command answer one kind of question well.

## Which command to use

| Command | Best question |
| --- | --- |
| `make inspect` | I want the whole learner-facing inspection bundle |
| `make inspect-summary` | what policy state and open incidents exist right now |
| `make inspect-rules` | which rules are draft, active, or retired |
| `make inspect-history` | how incidents accumulated for each metric |
| `make inspect-timeline` | what ordered scenario moments produced the current state |

## Recommended reading order

1. `make inspect`
2. `summary.txt`
3. `rules.txt`
4. `history.txt`
5. `timeline.txt`

That order moves from the current high-level snapshot into lifecycle detail, incident
history, and finally the ordered scenario flow.

## What each route should teach

- `inspect-summary` should show the learner that the capstone still has one readable aggregate-centered story.
- `inspect-rules` should show that lifecycle state is explicit and reviewable.
- `inspect-history` should show that downstream incident views are derived from the scenario instead of controlling it.

## How to read the outputs honestly

| Output | Best question | What it cannot prove on its own |
| --- | --- | --- |
| `summary.txt` | what state and incidents a learner should understand first | whether the domain rules were enforced correctly under all behaviors |
| `rules.txt` | which rules are draft, active, or retired | whether evaluation variability is placed in the right seam |
| `history.txt` | which incidents were published and accumulated downstream | whether the history source remained non-authoritative in code |
| `timeline.txt` | which ordered steps produced the saved scenario state | whether the runtime and aggregate boundaries are placed correctly under arbitrary change |

## Best follow-up choices

- Go to `PACKAGE_GUIDE.md` when the question becomes "which package owns this state?"
- Go to `TEST_GUIDE.md` when the question becomes "which test proves this state change?"
- Go to `PROOF_GUIDE.md` when the question becomes "which route is strongest for this claim?"

## Escalate when

- the output shows surprising state but you cannot yet name the owner of the change
- two outputs look consistent, but you still do not know which one is authoritative
- the inspection bundle tells a coherent story, but you need executable evidence for the same claim

## What this guide prevents

- using one summary output to justify every design claim
- confusing rule lifecycle state with incident history
- treating learner-facing inspection output as a substitute for tests
- forgetting that projections are derived artifacts rather than authoritative domain state
