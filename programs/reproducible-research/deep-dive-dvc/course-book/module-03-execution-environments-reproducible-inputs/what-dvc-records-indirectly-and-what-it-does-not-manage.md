# What DVC Records Indirectly and What It Does Not Manage

Learners often ask DVC to solve the whole environment problem.

That is too much and too vague.

Module 03 works better when DVC's boundary is named precisely.

## What DVC helps make visible

DVC helps by making other parts of the workflow explicit enough that environment questions
become easier to diagnose:

- data identity is tracked
- stage relationships are declared
- recorded execution state exists
- parameters can be compared explicitly
- recovered artifacts can be tied back to recorded runs

This matters because environment drift is much harder to discuss when every other input is
still hidden too.

## What DVC does not manage directly

DVC does not itself manage:

- Python package resolution
- Conda or system dependency pinning
- OS image selection
- container runtime behavior
- CPU or GPU driver stacks
- exact low-level numerical behavior

Those concerns still need other tools, policies, and review surfaces.

## Why indirect evidence still matters

Even when DVC does not own the environment, it can still support environment reasoning by
keeping the rest of the workflow story clearer.

If the same data, parameters, and stage graph are visible, then a mismatch becomes easier
to interpret as a runtime question instead of a total mystery.

That is an important contribution even though it is not full environment control.

## A practical contrast

| Question | DVC helps with | DVC does not settle by itself |
| --- | --- | --- |
| which inputs and outputs were recorded | yes | not enough for full environment control |
| which data and params were used | yes | still does not pin the whole runtime stack |
| which Python, OS, and library stack should be installed | only indirectly at best | this needs other tooling and policy |
| why local and CI runs differ | makes diagnosis clearer | does not automatically eliminate the difference |

This is the right scale of claim for Module 03.

## A small example

Suppose two runs differ and the team can already confirm:

- same DVC-tracked data
- same `params.yaml`
- same pipeline declaration

That does not mean DVC failed.

It means DVC has already narrowed the field. The remaining question is more plausibly
about the environment boundary than about hidden data or parameter drift.

That narrowing is valuable.

## Why clear boundaries protect learners

Without a clear DVC boundary, learners tend to fall into one of two bad stories:

- DVC should have prevented every runtime difference
- DVC is irrelevant because it did not prevent every runtime difference

Both stories are wrong.

The better story is:

> DVC makes important workflow state explicit, and that explicitness helps us review
> environment drift honestly, even though environment control still needs more than DVC.

## What capstone surfaces teach here

The DVC capstone helps because it exposes a few environment-adjacent facts clearly:

- `make platform-report` shows key tool versions
- the Makefile shows the install/runtime route
- the declared pipeline and control surface stay visible while you inspect runtime questions

This is a good learning pattern. It keeps environment evidence close to the workflow
without pretending one tool owns everything.

## Keep this standard

When a learner asks what DVC contributes to environment reproducibility, do not answer only
with "not much" or "everything."

Answer more precisely:

- DVC records and connects important workflow state
- that clarity makes environment drift diagnosable
- full environment management still belongs to complementary tools and governance

That is the level of truth Module 03 needs.
