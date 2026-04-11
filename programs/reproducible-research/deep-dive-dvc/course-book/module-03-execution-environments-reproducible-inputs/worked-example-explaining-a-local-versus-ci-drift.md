# Worked Example: Explaining a Local Versus CI Drift

This example shows how Module 03 fits together when a workflow does something that makes
teams uneasy:

the local run and the CI run are both honest, but the result is not exactly the same.

## The situation

Suppose you run the DVC capstone locally and see one set of metrics.

CI runs the same repository and reports a slightly different metric.

Nobody changed:

- the Git commit
- the DVC-tracked data
- `params.yaml`

That is exactly the kind of moment where weak environment thinking breaks down.

## Step 1: Resist the wrong first conclusion

The weak conclusions are:

- someone must have changed the data
- CI is random nonsense
- DVC failed to make the workflow reproducible

Module 03 asks for a slower, better question:

> if the explicit data and parameter story still matches, what runtime facts might still be
> part of the input surface?

## Step 2: Confirm the explicit workflow state first

You check:

- DVC-tracked data identity
- `params.yaml`
- the declared workflow path

Those still align.

This matters because it narrows the drift question. The repository is not completely
mysterious anymore.

## Step 3: Inspect runtime evidence

Next you compare environment clues:

- local toolchain versions
- CI toolchain versions
- `make platform-report`

Now the story becomes clearer:

- Python version differs slightly
- one numerical dependency version differs as well

This does not automatically explain the metric gap perfectly, but it turns the problem
from folklore into a reviewable runtime difference.

## Step 4: Classify the drift honestly

You now have to decide:

- is this an expected amount of conditional determinism
- or is it meaningful enough to tighten the environment strategy

That is the real judgment in Module 03.

If the delta is tiny and within declared comparison tolerance, the honest answer may be:

> these runs are conditionally deterministic, and the current strategy allows small runtime variation.

If the delta is too large for the workflow's review standards, the answer may instead be:

> we need a stronger environment strategy or a stricter canonical executor.

## Step 5: Choose the right repair

The repair is not automatically "pin everything harder."

Possible honest moves include:

- tightening dependency control with better lockfiles
- standardizing more of the runtime through containers
- treating CI as the canonical proof executor
- documenting the acceptable comparison tolerance more clearly

The correct move depends on the workflow's review and release needs.

## What DVC contributed here

DVC did not solve the environment drift directly.

What it did do was make the rest of the story more explicit:

- the data identity was not in doubt
- the parameter surface was not in doubt
- the stage story was not in doubt

That clarity made the environment explanation possible instead of speculative.

## The review note you would want

> Local and CI runs differed slightly even though the recorded data, parameters, and
> workflow declaration aligned. Platform evidence showed a runtime version difference,
> which makes environment drift the strongest current explanation. This does not mean DVC
> failed; it means the repository has made other state explicit enough for the remaining
> difference to be diagnosed as runtime-sensitive behavior. The next decision is whether
> the observed drift fits the workflow's accepted tolerance or whether environment control
> should be tightened.

That note is much stronger than "CI was weird."

## Why this is a mastery example

This one story exercises the whole module:

- Core 1: environment was treated as input
- Core 2: divergence was read through the determinism spectrum
- Core 3: DVC's boundary stayed honest
- Core 4: environment strategy became the repair question
- Core 5: runtime evidence was used instead of superstition
