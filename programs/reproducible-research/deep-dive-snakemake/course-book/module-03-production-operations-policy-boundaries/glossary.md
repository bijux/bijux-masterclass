# Glossary

Module 03 is where many learners start saying "production" as if it were one big vague
thing. It is not. Production work gets safer when you can separate workflow meaning,
operating policy, recovery rules, and evidence routes.

Use this glossary whenever an explanation starts slipping back into folklore.

## When to stop and check the glossary

Pause and check a term when:

- your explanation depends on "production stuff" without naming the actual boundary
- you are treating profile policy and workflow meaning as if they were the same thing
- you can tell a recovery decision feels risky but cannot yet name the failure class
- you are mixing scratch placement and final contract paths in one explanation

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

## Confusion pairs worth fixing early

These pairs matter because they decide whether you are repairing operations or quietly
changing the science:

- `profile` versus `workflow meaning`: the profile changes operating context; workflow
  meaning defines the intended outputs and semantics.
- `transient failure` versus `fail-fast error`: transient failures may justify retry;
  fail-fast errors should stop the run because repeating them only repeats the mistake.
- `scratch space` versus final contract paths: scratch helps execution; final contract
  paths are what readers and downstream tools are allowed to trust.
- `proof route` versus `profile audit`: a profile audit is one kind of proof route focused
  on policy differences across contexts.

## Quick self-check

Before you leave Module 03, make sure you can answer these in a full sentence:

- If local and cluster profiles behave differently but should produce the same trusted
  meaning, what boundary are you trying to protect?
- If an NFS delay makes a file appear late but rerunning the same correct command usually
  succeeds, what failure class are you naming?
- If a repository quietly moves trusted outputs into scratch-only paths, which operational
  mistake has crossed the line into contract risk?
- If you want evidence that one profile changes retries and logging but not planned
  outputs, what review route inside this module should you reach for first?

## Terms you should be able to use by the end of the day

If Module 03 is landing properly, these terms should feel ordinary by the end:

- profile
- failure policy
- fail-fast error
- transient failure
- proof route
- clean-room confirmation
- semantic drift

If those still feel decorative rather than useful, revisit the worked example and the
first seven exercises before moving on.
