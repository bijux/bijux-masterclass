# Exercises

Use these after reading the five core lessons and the worked example. The goal is not to
show off Make cleverness. The goal is to make your architecture reasoning visible through
interfaces, ownership, and growth-safe structure.

Generate the shared evidence before beginning:

```sh
cd programs/reproducible-research/deep-dive-make/capstone
gmake architecture-contract-audit
```

Keep `summary.tsv`, `report.json`, the traces, and the workspaces open. Several exercises
ask you to move from those controlled models to a repository of your own.

## How to work through this set

Treat the ten exercises as one full lab day on build architecture review.

Before each answer:

1. name the interface or responsibility boundary you are testing
2. choose the inspection path that would make that boundary visible
3. state what structural decision would follow if the evidence confirms your concern

If you skip the boundary question, architecture work collapses into vague cleanup talk.
This module is about making the Makefile itself reviewable as an interface.

Do the exercises in order. The day is one progression:

- Exercises 1-3 define the public target surface, include layers, and abstraction limits
- Exercises 4-6 prepare the build for growth and document the interface for contributors
- Exercises 7-9 audit automation, variable ownership, and macro inspection honestly
- Exercise 10 turns those ideas into one real refactor of a mixed-responsibility build

Keep one architecture packet as you go. By the end of the day it should contain:

- one public target contract list
- one include-layer ownership map
- one abstraction decision you can defend either way
- one namespace redesign for future growth
- one automation audit against the public API
- one short architecture review naming a remaining risk

If those six artifacts are missing, you are probably editing layout without improving the
build’s long-term interpretability.

## Recommended working layout

If you want one lab tree that can support the whole day, use something like:

```text
module07-lab/
├── Makefile
├── mk/
├── src/
│   ├── app/
│   └── lib/
├── scripts/
├── .github/
├── notes/
└── artifacts/
```

Use this ownership map in every architecture answer:

| Responsibility | Owning file | Public consumer | Evidence that the boundary holds |
| --- | --- | --- | --- |

A file list without responsibilities is not an architecture explanation.

Also keep one caller map:

| Caller | Target invoked | Public or internal | Why that status is justified |
| --- | --- | --- | --- |

That second table matters because automation often becomes the real consumer of your build
interface long before humans read `help`.

```mermaid
flowchart LR
  surface["define the public interface"]
  layers["separate responsibilities into layers"]
  inspect["inspect callers, variables, and generated rules"]
  grow["prepare names and paths for growth"]
  simplify["remove unjustified cleverness"]
  review["leave a maintainable architecture note"]

  surface --> layers --> inspect --> grow --> simplify --> review
```

Use that route on purpose. It keeps the day centered on ownership and interface clarity
instead of on cosmetic reshuffling.

## Exercise 1: Define a public target surface

Start with the `public-api/private-caller` specimen. Compare its `help` output with
`automation-private.sh`, then run that caller. Decide which target is a promise, which
target is merely reachable, and which promised evidence the caller bypasses.

What to hand in:

- the exact help output and caller command
- a table classifying `help`, `verify`, and `internal-build`
- the caller's exit status and the two expected artifact-presence observations
- the audit finding that justifies your classification
- one repair that does not enlarge the public API

Study note:
Reachability is a property of Make's graph. Public status is a compatibility promise.
Successful use of a private target does not turn it into a sound interface.

## Exercise 2: Split one Makefile into layers

Compare the two `include-ownership` specimens. They already have identical `mk/*.mk`
layouts, yet only one keeps release policy inside the release branch. Explain why the
file split fails to enforce the intended boundary, then apply the same analysis to one
Makefile that mixes policy, discovery, artifact rules, and release logic.

What to hand in:

- the four artifact flag values from the paired specimens
- the assignment and scope responsible for each pair of values
- a proposed include order and responsibility table for your Makefile
- one executable check showing ordinary policy is unchanged by a release-only decision
- one sentence distinguishing include order from variable scope

Study note:
Identical filenames and include order can still enforce different contracts. Ownership is
established by where a value propagates and by evidence from the affected targets.

## Exercise 3: Decide whether a macro is justified

Compare the `explicit-rules` and `bounded-macro` specimens from the abstraction audit.
Treat the explicit rules as a contract baseline, not as the automatically preferred
implementation. Prove whether the macro preserves that contract.

What to hand in:

- a target, prerequisite, policy, publication, and owner table for the explicit model
- the bounded macro’s owner list and call-domain output
- the evaluated target/prerequisite map from both models
- a byte-level comparison of both artifact pairs
- a keep/remove decision with one stated limit of the evidence

Study note:
Line count is not a contract. The macro earns consideration only after its evaluated graph
and artifacts match the explicit baseline.

## Exercise 4: Prepare the repository for growth

Run both `output-ownership` specimens. Trace how two sources named `util.txt` become either
one flat output or two namespaced outputs. Then extend the control with a third source root
that uses the same basename.

What to hand in:

- the evaluated source and output lists for both original models
- source count and unique-output count for each model
- the contents and owner of every produced artifact
- the third root's discovery and path-mapping rule
- one assertion that fails whenever distinct sources map to the same output

Study note:
Sorting can make a collision deterministic without preserving ownership. Count unique
outputs and inspect artifact identity; do not infer safety from stable ordering.

## Exercise 5: Review a build architecture before it rots

Choose one architecture claim from the course audit bundles and review the corresponding
surface in another Make repository. Keep the investigation bounded enough that another
learner can rerun it without your explanation.

What to hand in:

- one claim naming its owner and consumer
- one observation that would falsify the claim
- the smallest source, evaluated-graph, and runtime evidence needed
- a defect/control comparison or controlled mutation
- an accept, repair, or defer record with a remaining limit and future trigger

Study note:
Separate observations from conclusions. Preserve complete raw evidence in the packet, but
quote only the entries that support the decision.

## Midday self-check

Before you move into interface publishing, automation audits, and macro inspection, make
sure your packet can already answer these questions cleanly:

- which targets are truly public and why
- which include layer owns policy, discovery, and artifact edges respectively
- which abstraction you would reject even if it reduced duplication
- which path collision or naming ambiguity your future growth redesign prevents

If you cannot answer those four questions in plain language, return to Exercises 1-5 and
make the packet more explicit before continuing.

## Exercise 6: Publish a useful `help` target

Extend a disposable copy of the public-API control with public targets for building,
testing, verifying build invariants, cleaning, and showing help. Keep `internal-build`
reachable but private. Write one script that uses only the help output to select the
verification route.

What to hand in:

- the explicit public-target list
- the `help` recipe and output
- the script's selected target and exit status
- the artifacts that prove the selected target fulfilled its contract
- a negative check showing `internal-build` is absent from help
- one compatibility consequence of renaming a listed target

Study note:
If help only repeats names, the caller still needs source knowledge. A useful description
states the outcome or evidence the target promises.

## Exercise 7: Audit automation against the public API

Audit two environments. First compare `automation-private.sh` and
`automation-declared.sh` with their Makefile's help output and artifacts. Then search a
repository's CI, release, and developer scripts for Make invocations and apply the same
test.

What to hand in:

- the search command
- a table of caller, target, and public or internal status
- a promised-evidence column for every public invocation
- the two specimen findings and the observation that distinguishes them
- one repaired repository caller with before-and-after command lines
- evidence that the repaired caller receives the full public contract

Study note:
Do not repair a private call by listing every helper in `help`. Either move the caller to
an existing promise or deliberately design a new stable contract.

## Exercise 8: Make variable ownership inspectable

Start from `include-ownership/global-mutation`. Explain why the ordinary artifact receives
`-DRELEASE`, repair the release decision without changing the include filenames, and test
the repair from clean state. Then choose one variable that several includes mutate in
another repository and assign its ownership using the same method.

What to hand in:

- the old global mutation and repaired target-scoped assignment
- ordinary and release artifact contents before and after repair
- `$(origin ...)`, `$(flavor ...)`, or `gmake -p` evidence for your repository variable
- the target branches allowed to specialize that variable
- one case where command-line override is supported and one invariant that must reject it

Study note:
Variable database output proves the evaluated value; target artifacts prove where that
value propagated. Use both when scope is the contract under review.

## Exercise 9: Inspect a macro instead of trusting it

Start from `bounded-macro`. Add a third owner and confirm the expected rule appears. Then
inject one unrelated target or policy assignment into the macro body and show which
evidence surface exposes the side effect.

What to hand in:

- the third owner’s source, generated target, and artifact contents
- the relevant `gmake -npRr all` entries before and after mutation
- help output compared with every generated callable target
- artifact modes before and after mutation
- the rejection-test result and a repair that restores one-responsibility generation

Study note:
Inspect both dispatched artifacts and undispatched target surface. A successful `all` run
cannot prove that the macro generated nothing else.

## Exercise 10: Refactor a growing build

Take a Makefile that exhibits or could exhibit all three audited risks: private automation
calls, cross-layer policy mutation, and flat output mapping. Preserve baseline evidence,
repair each boundary independently, and add rejection checks that make a dishonest repair
fail.

What to hand in:

- a before-and-after contract table with caller, policy, and output observations
- help output and the actual automation command
- ordinary and release artifact policy values
- source-to-output mappings with equal source and unique-output counts
- clean-run, no-op, and rejection-test evidence
- a review note naming one remaining architecture risk and its future proof route

Study note:
Do not accept a new tree as the result. Accept changed observations, preserved public
meaning, and tests that fail when the claimed ownership boundaries are violated.

## Before you read the answers

Do not open `exercise-answers.md` until you can already point to:

- one clear public target contract
- one include layer with a single responsibility
- one macro you kept or rejected for a reason you can defend
- one future-growth risk you can already see
- one automation caller that forced you to clarify the interface

If you do not yet have those five things, the answer page will sound stronger than it can
teach.

## Mastery standard for this exercise set

Across all ten answers, the module wants the same habits:

- you name the architectural boundary being tested
- you choose inspection and evidence before proposing the cleanup
- you explain the cleanup in terms of API clarity, responsibility, reuse discipline, or
  growth safety

If an answer says only "the Makefiles need cleanup," keep going.
