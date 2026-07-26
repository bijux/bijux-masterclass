# Exercises
Use these after reading the five core lessons and the worked example. The goal is not to
show off Make cleverness. The goal is to make your architecture reasoning visible.

## How to work this exercise set

Treat these as architecture review and design exercises:

- Exercises 1-3: define API boundaries and justify reuse choices
- Exercises 4-6: make growth and public surfaces readable
- Exercises 7-9: inspect real callers, variable ownership, and macro behavior
- Exercise 10: refactor a mixed-responsibility build into a clearer structure

Each exercise asks for three things:

- the architecture fact or boundary you are trying to establish
- the evidence or inspection path that would establish it
- the refactor or policy decision that follows from that evidence

Use this ownership map in every architecture answer:

| Responsibility | Owning file | Public consumer | Evidence that the boundary holds |
| --- | --- | --- | --- |

A file list without responsibilities is not an architecture explanation.

## Minimum evidence for every answer

Try to include:

- one ownership map
- one public or internal caller
- one inspection command that shows the structure is really behaving as claimed

## Exercise 1: Define a public target surface

Take a Make-based repository with several top-level targets and decide which ones should be
public and which ones should stay internal.

What to hand in:

- the public target list
- one sentence of contract meaning for each public target
- one target that should be demoted to internal and why

## Exercise 2: Split one Makefile into layers

You inherit a single large Makefile that mixes shell policy, source discovery, artifact
rules, and release logic.

Sketch a layered `mk/*.mk` design that separates those responsibilities.

What to hand in:

- the top-level include order
- one sentence describing the job of each layer
- one example of a mutation or override that the new structure should make easier to review

## Exercise 3: Decide whether a macro is justified

A teammate wants to replace three similar explicit rules with one macro plus `call` and
`eval`.

Explain how you would decide whether that abstraction improves the build or turns it into a
private language.

What to hand in:

- the invariant the macro would protect
- one reason to keep the explicit rules instead
- one inspection command or technique you would use after the refactor

## Exercise 4: Prepare the repository for growth

A second subsystem is about to be added under `src/lib/`, but the current build assumes a
flat `src/*.c` layout and flat output names.

Describe how you would redesign discovery and naming so the graph stays stable and
ownership stays legible.

What to hand in:

- the new discovery roots
- the new output naming or namespacing pattern
- one concrete collision or ambiguity the redesign prevents

## Exercise 5: Review a build architecture before it rots

Take an existing Make architecture and write a short review note focused on future risk
rather than current success.

What to hand in:

- one public API risk
- one layer-boundary risk
- one reuse or naming risk
- one recommendation that should be made before the next growth step lands

## Exercise 6: Publish a useful help target

Create a `help` target for five public targets. The output must explain the contract of
each target in language a new contributor can act on.

What to hand in:

- the explicit public-target list
- the `help` recipe and output
- one helper target intentionally excluded from the interface

## Exercise 7: Audit automation against the public API

Search a repository's CI, release, and developer scripts for Make invocations. Compare
every invoked target with the public target list.

What to hand in:

- the search command
- a table of caller, target, and public/internal status
- one repair for automation that calls an internal target

## Exercise 8: Make variable ownership inspectable

Choose a variable that several include files currently mutate. Assign one layer as its
owner and define where command-line overrides are allowed.

What to hand in:

- the old mutation sites
- the new ownership rule
- output from `$(origin ...)`, `$(flavor ...)`, or `make -p` that proves the behavior

## Exercise 9: Inspect a macro instead of trusting it

Write or choose a bounded rule-generating macro. Inspect its expanded rules and compare
them with equivalent explicit rules.

What to hand in:

- the invariant the macro protects
- the macro and two call sites
- the inspection output
- a decision to keep or remove the macro, with reasoning

## Exercise 10: Refactor a growing build

Take a Makefile that mixes at least three responsibilities. Define its public API, split
ownership into include layers, namespace discovery for two source roots, and keep CI on
public targets.

What to hand in:

- before-and-after tree and include order
- public target contracts
- a source-to-object mapping for both roots
- dry-run, no-op, and selftest evidence
- a short architecture review naming one remaining risk

## Before you read the answers

Do not open `exercise-answers.md` until you can already point to:

- one clear public target contract
- one include layer with a single responsibility
- one macro you kept or rejected for a reason you can defend
- one future-growth risk you can already see

## Mastery standard for this exercise set

Across all ten answers, the module wants the same habits:

- you name the architectural boundary being tested
- you choose inspection and evidence before proposing the cleanup
- you explain the cleanup in terms of API clarity, responsibility, reuse discipline, or growth safety

If an answer says only "the Makefiles need cleanup," keep going.
