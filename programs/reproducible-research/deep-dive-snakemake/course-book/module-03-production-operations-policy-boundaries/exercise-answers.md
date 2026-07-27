# Exercise Answers

Use this page after you have written your own answers. The point is comparison, not
copying.

## How to use the answer page well

Do not read a model answer first and then retrofit your exercise around it.

A better rhythm is:

1. complete the exercise with your own repository state and commands
2. write one plain-language explanation of the boundary you are reviewing
3. compare that explanation with the model answer
4. revise where the model answer exposes a missing proof route or a blurred policy line

The goal is not identical wording. The goal is disciplined operational reasoning.

The strongest Module 03 answers usually do four things:

- they name the owning operational boundary
- they explain why the current shape is safe or unsafe
- they choose one proportionate proof route
- they describe the repair in terms of repository discipline, not heroics

The strongest self-study packets also leave behind six concrete artifacts:

- a profile comparison table
- one paired dry-run comparison
- one failure-class matrix
- one storage lifecycle sketch
- one proof ladder
- one short maintainer review note

If your packet contains only commands and verdicts, go back and make the reasoning more
visible.

## Exercise 1: Separate policy from workflow meaning

A strong answer sounds like this:

> `latency-wait` and `show-failed-logs` belong in a profile because they change runtime
> behavior without changing the intended outputs. A sample list and publish version do not
> belong in a profile because they change target meaning and downstream contract surfaces.
> If those semantic values moved into a profile, local and CI contexts could appear to be
> harmless policy differences while actually changing what the workflow means.

Why this is strong:

- it gives two good policy examples and two bad ones
- it explains the review risk, not only the placement rule

## Exercise 2: Compare the same target across two profiles

A strong comparison keeps targets, semantic config, and publish paths identical. Local may
use more cores and shorter latency patience; CI may serialize work, show failed logs, and
wait longer for filesystem visibility. The paired dry-runs should resolve the same jobs
and dependencies for the same requested target. A line-by-line table prevents a harmless
operational difference from concealing semantic drift.

A compact model table might look like this:

| Surface | Local | CI | Safe difference? |
| --- | --- | --- | --- |
| target | `publish/v1/manifest.json` | `publish/v1/manifest.json` | must stay the same |
| cores | 4 | 1 | yes |
| latency wait | 5 | 20 | yes |
| publish root | `publish/v1/` | `publish/v1/` | must stay the same |

Why this is strong:

- it checks the boundary with the same target surface
- it treats profile differences as reviewable lines, not intuition

## Exercise 3: Choose the smallest honest proof route

A strong answer matches the route to the question:

- planning difference between local and CI:
  - compare dry-runs
- visible profile differences for review:
  - `make profile-audit`
- strongest repository confidence:
  - `make confirm`

The strongest answers also explain why the routes are not interchangeable:

- `confirm` is too heavy for a simple planning question
- dry-run is too weak for the strongest clean-room claim
- profile-audit is better than intuition for context-comparison review

## Exercise 4: Write a small failure policy

A strong answer distinguishes failure classes cleanly.

Example answer shape:

- retryable:
  - transient infrastructure or storage hiccup
- fail-fast:
  - wrong config value or invalid sample contract
- rerun-incomplete:
  - partial output left behind after a crashed job
- logs:
  - per-job logs help determine whether the failure was transient, semantic, or
    partial-publication related

A compact model matrix might look like this:

| Failure class | Evidence surface | Response |
| --- | --- | --- |
| transient infrastructure issue | failed log plus external service or storage symptom | bounded retry |
| semantic defect | config value, rule contract, or deterministic traceback | fail fast |
| interrupted output | incomplete file plus interrupted execution evidence | rerun incomplete state deliberately |

Why this is strong:

- it makes retry, fail-fast, and rerun-incomplete different on purpose
- it treats logs as evidence for the decision, not as decoration

## Exercise 5: Review one staging or locality assumption

A strong answer sounds like this:

> The workflow may use a different scratch or staging location on shared infrastructure,
> but the declared final output paths and publish boundary must stay semantically stable.
> If the team confuses scratch placement with final output meaning, reviewers can no longer
> tell which paths are temporary and which are part of the contract.

Why this is strong:

- it allows context variation honestly
- it protects the stable trust surface

## Exercise 6: Review one operational diff like a maintainer

A strong answer begins with the owning boundary:

- first inspect the changed profile file
- then inspect the changed proof route or target
- ask:
  - does this change execution context only, or workflow meaning too
  - what claim is stronger or weaker after the proof-route edit

Why this is strong:

- it reviews in boundary order
- it does not let a policy diff drift into vague trust language

## Exercise 7: Inject and classify failures

The transient simulation may be retried only if repetition can plausibly change the
outcome, such as a temporary service or storage interruption. Invalid configuration fails
before work and must not be retried. An interrupted write requires removal or replacement
of incomplete state before rerun. Logs should capture the command, failure class, and
relevant context; a retry count alone cannot explain correctness.

## Exercise 8: Design a staging route

The route should copy or link a declared source into job-specific scratch, execute there,
validate the result, and atomically publish to the declared final path. Failure cleanup
must not delete unrelated jobs or present scratch files as final outputs. Scratch root,
transfer mechanism, and latency assumptions belong to operating context. Input identity,
result content, and final contract remain stable.

The diagram is not complete unless it marks where trust starts. A reviewer should be able
to point to one step and say, "before this, execution state is provisional; after this,
the declared output may be trusted."

## Exercise 9: Prove a clean-room run

A strong clean-room route begins from documented inputs and a declared software
environment, executes into an empty work area, and verifies an expected output inventory.
Checksums or semantic assertions establish more than file existence. The exercise rules
out ambient files, previously solved environments, undeclared variables, and stale outputs
as hidden dependencies.

## Exercise 10: Review a production policy change

Higher resources are acceptable when they only alter scheduling capacity. Retries require
a named transient failure class, a bounded count, and evidence that repeated execution is
safe. A new staging root is acceptable only when scratch remains private and publication
returns to the unchanged final boundary. Compare profile dry-runs and run the smallest
executed selftest that traverses staging and recovery; do not invoke the strongest suite
without a claim that needs it.

A strong review also shows a stable order:

1. inspect the changed profile keys
2. classify whether each line is capacity, observability, recovery, or storage policy
3. reject any semantic leak before debating convenience
4. choose the narrowest route that proves the accepted changes remain honest

## What all ten answers should have in common

The best Module 03 answers usually:

1. distinguish policy from semantics clearly
2. explain recovery as a contract rather than a habit
3. treat proof routes as proportionate tools instead of ritual commands
4. describe operational governance as something the repository should teach

Weak answer pattern:

- "production is complicated, so more retries and more confirmation should be fine"

That sentence hides every boundary the module is trying to teach. If your answers still
sound like that, keep revising.

If your answers do those four things, the module is landing in the right way.
