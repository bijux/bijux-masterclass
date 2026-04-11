# Exercise Answers

These answers are model explanations, not the only acceptable wording.

What matters is whether the reasoning treats environment as a real input surface without
mythologizing DVC into owning everything.

## Answer 1: Name the environment as input

Why the claim is too strong:

- code, data, and parameters can remain aligned while runtime facts still influence the result

Which runtime facts may matter:

- interpreter or library versions
- system tools
- hardware differences
- thread behavior
- locale or filesystem behavior

Why this does not make the workflow hopeless:

- it means the team needs a clearer environment strategy and evidence route, not surrender

The main lesson is that environment influence is ordinary, not mystical.

## Answer 2: Explain conditional determinism

Why the workflow may still be honest:

- small divergence can come from runtime-sensitive numerical behavior rather than hidden misconduct

What conditional determinism means:

- the workflow is only reliably identical under certain declared runtime conditions

What evidence to inspect next:

- environment and platform reports
- dependency versions
- the workflow's own tolerance or review standards for acceptable drift

## Answer 3: Draw DVC's environment boundary

Strong note:

> DVC helps keep data identity, parameters, and recorded workflow state explicit. That
> makes environment drift easier to diagnose, but DVC does not itself resolve dependency
> pinning, container images, OS/runtime selection, or hardware variation. The distinction
> matters because otherwise teams either overpromise what DVC can do or underuse the
> clarity it actually provides.

The main lesson is to keep DVC's contribution precise.

## Answer 4: Choose an environment strategy

Strong reasoning:

- use lockfiles when reviewable dependency change and fast local iteration matter
- use containers when you need broader runtime consistency, especially in automation
- use CI as a canonical executor when the team needs one shared proof environment

A combined answer is often strongest:

- lockfiles for explicit dependency history
- containers for stable CI/runtime packaging
- CI for shared authority about what counts as a trusted run

## Answer 5: Diagnose local-versus-CI drift

Environment evidence to inspect next:

- tool and interpreter versions
- dependency versions
- platform-report output

How to decide whether the difference is acceptable:

- compare the observed drift against the workflow's expected tolerance and release needs

Possible repair if the strategy is too weak:

- tighten dependency control
- move more of the runtime into containers
- treat CI more explicitly as the canonical proof environment
- document acceptable drift more clearly

## Self-check

If your answers consistently explain:

- why environment belongs in the input surface
- why conditional determinism is a serious engineering concept
- what DVC clarifies without directly managing
- how environment strategies trade explicitness, stability, and authority

then you are using Module 03 correctly.
