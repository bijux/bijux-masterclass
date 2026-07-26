# Exercises


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Generated Files Multi Output Pipeline Boundaries"]
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

Use these after reading the five core lessons and the worked example. The goal is not to
show off Make syntax. The goal is to make your generation and pipeline reasoning visible.

Each exercise asks for three things:

- the generator fact you are trying to prove
- the evidence or command that would prove it
- the repair or design choice that follows from that evidence

## Exercise 1: Tell the graph story of one generated file

Choose a generated file such as a header, manifest, or report output. Explain what makes
it stale and which downstream target actually consumes it.

What to hand in:

- the generated file path
- the semantic inputs that define its meaning
- one consumer target and why it should depend on that published output

## Exercise 2: Repair a coupled output rule

A single generator invocation produces both `api.h` and `api.json`, but the current rule is
naive and occasionally runs twice under `-j`.

Design a repair that gives the build one honest publication event.

What to hand in:

- the bug explanation in plain language
- either a grouped-target repair or a stamp-based repair
- one command you would run to prove single invocation under pressure

## Exercise 3: Decide whether a manifest is justified

A teammate wants to add `build/codegen.manifest`. You are not yet convinced it represents a
real boundary rather than a missing edge.

Explain how you would decide whether the manifest is justified.

What to hand in:

- the specific boundary fact the manifest would represent
- one example of a target that should depend on it
- one example of a target that should still depend on a direct generated output instead

## Exercise 4: Protect a pipeline from partial publication

A multi-stage generator writes final output files directly into the trusted output
directory before validation completes. Describe how you would redesign it so downstream
targets never trust partial results.

What to hand in:

- the temporary-space rule you would introduce
- the validation step
- the exact publication point after which outputs become trustworthy

## Exercise 5: Diagnose one generator failure mode

Pick one of these symptoms:

- stale generated output
- duplicate execution under `-j`
- unstable manifest
- partial outputs after failure
- confused consumer edge

Write the repair loop you would use to diagnose and fix it.

What to hand in:

- the failure class
- the command that would give you the first useful evidence
- the graph or publication repair you would try next

## Exercise 6: Build your first generated target

Generate `build/version.h` from a plain-text `VERSION` file. The generated header must
rebuild when `VERSION` changes and remain untouched on a no-op build.

What to hand in:

- the complete rule
- traces from the initial, no-op, and changed-input runs
- the generated header after the change

## Exercise 7: Recover from one deleted coupled output

Create a grouped rule that produces `build/api.h` and `build/api.json`. Build both, delete
only the JSON file, and ask Make to build both again.

What to hand in:

- the grouped-target rule
- generator invocation counts before and after deletion
- an explanation of why the whole grouped recipe runs

## Exercise 8: Inject a generator failure

Modify a toy generator so it can exit after writing temporary output but before
validation. Run the failed build and inspect both temporary and trusted paths.

What to hand in:

- the failure switch or input
- the failing command and exit status
- proof that the previously trusted outputs were not replaced

## Exercise 9: Choose a publication protocol

Compare these requirements:

- two generated files may briefly differ during an interrupted local build
- a serving process must always observe both files from the same generation

Choose a publication design for each requirement and explain why two final-path `mv`
commands are insufficient for the second.

What to hand in:

- the local-build design
- the strict publication design
- a diagram showing the point where downstream trust begins

## Exercise 10: Repair a complete generator pipeline

Build a small pipeline with source input, generator, two coupled outputs, validator,
manifest, and consumer. Demonstrate a clean build, no-op build, source edit, parallel
build, deleted-output recovery, and injected failure.

What to hand in:

- the Makefile and generator
- the six command transcripts
- a graph drawing that distinguishes generation, validation, publication, and consumption
- one paragraph identifying the remaining publication guarantee and its limits

## Mastery standard for this exercise set

Across all ten answers, the module wants the same habits:

- you name the publication or boundary truth being tested
- you choose evidence before you choose a repair
- you explain the repair in terms of graph truth, convergence, or publication discipline

If an answer says only "generators are tricky," keep going.
