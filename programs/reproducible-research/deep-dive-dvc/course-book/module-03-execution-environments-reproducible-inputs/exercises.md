# Exercises


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Execution Environments Reproducible Inputs"]
  page["Exercises"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["name the environment boundary"] --> inspect["inspect runtime evidence"]
  inspect --> compare["compare execution strategies"]
  compare --> break["break the environment on purpose"]
  break --> govern["design a durable operating rule"]
```
<!-- page-maps:end -->

Use these exercises to practice environment judgment, not only runtime vocabulary.

The goal of the day is to stop saying "the code and data were the same" as if that
settles the result. In real reproducible work, the environment is part of the input
surface. The hard part is not memorizing that slogan. The hard part is learning how to
name the boundary, collect the right evidence, and decide which differences matter.

## How to work through this set

Treat the ten exercises as one full lab day on environment authority.

Before each answer:

1. name the result claim under review
2. name the environment facts that could change that claim
3. say what evidence would separate acceptable drift from a real reproducibility failure

Do the exercises in order. The day is one progression:

- Exercises 1-3 define the boundary and separate DVC's job from environment management
- Exercises 4-5 compare lockfiles, containers, and CI as control strategies
- Exercises 6-8 collect evidence and break the environment on purpose
- Exercises 9-10 turn the lesson into a reviewable gate and a cross-context proof

Keep one environment packet as you go. By the end of the day it should contain:

- one plain-language statement of why environment is part of the input surface
- one boundary table separating DVC-managed state from environment-managed state
- one environment fingerprint from a real run
- one deliberate drift experiment with a written judgment
- one strategy comparison table for lockfiles, containers, and CI
- one environment drift gate design with failure wording and exception process

If those six artifacts are missing, you are probably still reading about environment drift
instead of learning how to govern it.

## Recommended working layout

If you want one lab tree that can support the whole day, use something like:

```text
module03-lab/
├── artifacts/
├── containers/
├── notes/
├── params.yaml
├── requirements.lock
└── src/
```

Keep one boundary table while you work:

| Surface | Example evidence | What it can prove | What it cannot prove by itself |
| --- | --- | --- | --- |
| DVC-tracked inputs | `dvc.lock`, hashes, `params.yaml` | declared data and parameter identity | runtime library or platform state |
| Dependency contract | lockfile, package manifest | resolved dependency intent | host image, kernel, or hardware |
| Execution image | container digest, image recipe | packaged runtime filesystem | external services or runtime flags |
| Run authority | CI logs, artifacts, provenance bundle | what the governed executor actually used | whether local machines matched it |

Also keep one environment fingerprint table:

| Run context | Interpreter | Dependency identity | Platform | Special flags | Result note |
| --- | --- | --- | --- | --- | --- |

```mermaid
flowchart LR
  boundary["name the boundary"]
  evidence["collect runtime evidence"]
  compare["compare control strategies"]
  drift["introduce drift deliberately"]
  decide["decide tolerated versus broken"]
  govern["write the gate"]

  boundary --> evidence --> compare --> drift --> decide --> govern
```

Use that route on purpose. It keeps the day focused on evidence and judgment instead of
falling into vague talk about "machine differences."

## Exercise 1: Name the environment as input

A teammate says:

> The code, data, and parameters are unchanged, so the environment cannot be the reason
> the result moved.

Write a short response that explains:

- why this claim is too strong
- which runtime facts may still matter
- why that does not make the workflow hopeless
- one sentence stating what evidence you would ask for next

Study note:
The point is not to make environment sound mysterious. The point is to make the input
surface complete enough to review honestly.

## Exercise 2: Explain conditional determinism

You see a tiny metric difference between two honest runs on different machines.

Explain:

- why the workflow may still be behaving honestly
- what it means to call the workflow conditionally deterministic
- what kind of follow-up evidence you would want next
- how you would describe the difference to a reviewer without either hiding it or
  exaggerating it

Study note:
Many students think the only honest choices are "identical" or "broken." Real practice is
more demanding than that.

## Exercise 3: Draw DVC's environment boundary

A teammate says:

> Once we use DVC, environment drift stops being our problem.

Write a short note that explains:

- what DVC really helps with in this situation
- what it still does not manage directly
- why the distinction matters
- one example of a failure that DVC makes diagnosable without directly preventing it

What to hand in:

- one paragraph in plain language
- one two-column table with `DVC clarifies` and `separate environment controls`

Study note:
Module 03 gets much easier once DVC stops being treated as a magical reproducibility box.

## Exercise 4: Choose an environment strategy

A small team wants:

- reviewable dependency changes
- more stable CI behavior
- faster local iteration

Explain how you would think about:

- lockfiles
- containers
- CI as a canonical executor

You do not need to choose only one, but you should explain what each contributes, what
each fails to cover, and how you would combine them for a serious project.

What to hand in:

- one comparison table
- one recommended operating model for this team

Study note:
The strongest answer does not pick a winner too early. It explains which problem each
control solves.

## Exercise 5: Diagnose local-versus-CI drift

A workflow differs slightly between local and CI runs.

You already confirmed:

- the DVC-tracked data matches
- `params.yaml` matches
- the declared workflow matches

Describe:

- what environment evidence you would inspect next
- how you would decide whether the difference is acceptable or needs escalation
- what repair might follow if the current environment strategy is too weak
- what single sentence you would put in a PR review while the investigation is open

Study note:
This exercise is about disciplined triage. Good teams do not jump from "it moved" to "the
whole pipeline is untrustworthy."

## Midday self-check

Before you move into fingerprinting, deliberate drift, and gate design, make sure your
packet can already answer these questions clearly:

- why environment belongs in the input surface
- what DVC does and does not govern
- what kind of evidence separates acceptable numeric sensitivity from a broken run
- why lockfiles, containers, and CI are not interchangeable

If you cannot answer those four questions in plain language, return to Exercises 1-5 and
make the packet more explicit before continuing.

## Exercise 6: Capture an environment fingerprint

Run one pipeline stage and record:

- interpreter version
- operating system
- dependency lock digest
- relevant tool versions
- container image digest if used
- any environment variables or runtime flags that plausibly affect result meaning

Identify which values can change result meaning and which are only useful context.

What to hand in:

- the completed environment fingerprint table
- one sentence naming the smallest fingerprint that would still be reviewable

Study note:
The job is not to record every possible fact. The job is to record the facts that explain
or constrain the result claim.

## Exercise 7: Break an environment deliberately

Change one dependency version while keeping code, data, and parameters fixed. Compare the
output and logs, then decide whether the difference is deterministic, tolerated, or a
release blocker.

What to hand in:

- the exact environment change
- the observed result difference
- the judgment you made
- the evidence that supports that judgment

Study note:
Deliberate breakage is one of the fastest ways to stop treating environment governance as
theoretical.

## Exercise 8: Compare lockfile and container guarantees

Write a table showing what a language lockfile and a container digest each constrain.
Include:

- operating-system libraries
- hardware
- environment variables
- network access
- entry commands
- package resolution

Then write one paragraph explaining why teams that say "we have containers, so we no
longer need a dependency contract" are still missing something.

Study note:
This is where many students first see that package identity and runtime packaging are
related but not identical controls.

## Exercise 9: Design an environment drift gate

Specify a CI check that detects accidental environment drift before accepting a result.
Name its:

- inputs
- evidence artifact
- failure message
- approval path for intentional upgrades
- reviewer expectation after a failed gate

Study note:
The most useful gates fail with enough detail that the team can respond without guessing.

## Exercise 10: Reproduce across two contexts

Run a small stage locally and in a second context such as CI, a container, or another
machine. Compare content digests and runtime evidence, and explain any difference without
assuming byte identity is always required.

What to hand in:

- the two context fingerprints
- the output comparison
- the result contract you used
- one conclusion about whether your current environment strategy is strong enough

Study note:
This final exercise matters because the whole module is about governed comparison across
contexts, not only neat local runs on one machine.

## Mastery check

You have a strong grasp of this module if your answers consistently keep five ideas
visible:

- environment is part of the input surface
- determinism is often conditional rather than absolute
- DVC helps make drift diagnosable without owning all environment management
- lockfiles, containers, and CI solve different parts of the runtime problem
- result trust improves when environment evidence is explicit and reviewable
