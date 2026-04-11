# Glossary

Use this glossary to keep the language of Module 03 stable while you move between the
core lessons, worked example, exercises, and capstone evidence.

The goal is not extra jargon. The goal is to make sure production operation is described
with clear boundaries instead of folklore.

## Terms in this module

| Term | Meaning in this module |
| --- | --- |
| clean-room confirmation | The strongest built-in proof route, used to show the repository still proves itself from a fresh operational stance. |
| fail-fast error | A failure that should stop the run because retrying would only repeat the wrong job or wrong configuration. |
| failure policy | The repository’s explicit rule for when to retry, rerun, preserve evidence, or stop. |
| incomplete output | A partially produced artifact that must not be trusted as final and may need rerun handling. |
| operational boundary | A repository surface that changes execution context without changing workflow meaning. |
| policy drift | A change in profiles, recovery settings, staging assumptions, or proof routes that may weaken reviewability over time. |
| profile | A versioned operating-context surface that records execution policy such as logging, latency, retries, or scheduler-facing defaults. |
| profile audit | A proof route that compares context-specific profile surfaces and their visible planning consequences. |
| proof route | A named command or bundle used to answer one bounded review question. |
| rerunnable state | A failed or incomplete state that the workflow recognizes and rebuilds deliberately instead of trusting silently. |
| scratch space | A temporary working area used for operation or staging, distinct from the final output contract. |
| semantic drift | A change that alters workflow meaning while pretending to be only operational. |
| staging | The operational act of moving or placing work in a context-specific area before final publication. |
| transient failure | A failure likely caused by temporary infrastructure or execution-context instability rather than by wrong workflow meaning. |
| workflow meaning | The intended outputs, contracts, and semantic behavior of the workflow, as distinct from how or where it runs. |

## The vocabulary standard for this module

When you explain a Module 03 situation, aim to say things like:

- "that change belongs to an operational boundary, not to workflow meaning"
- "the failure policy should retry this class but fail fast on that one"
- "scratch placement changed, but the final contract surface did not"
- "profile audit is the right route for this question, not clean-room confirmation"
- "this diff risks semantic drift even though it looks operational"

Those sentences are much more useful than saying only "production is complicated."
