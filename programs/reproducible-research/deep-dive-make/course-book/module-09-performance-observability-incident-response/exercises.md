# Exercises
Use these after reading the five core lessons and the worked example. The goal is not to
produce more diagnostics for their own sake. The goal is to make your measurement,
observability, and incident-response reasoning visible.

## How to work this exercise set

Treat these as operational investigations, not as benchmarking games:

- Exercises 1-3: define the symptom and choose proportional evidence
- Exercises 4-6: build real baselines and truth-preserving tuning habits
- Exercises 7-9: explain rebuilds, shell cost, and parallelism with measured context
- Exercise 10: preserve a complete incident record another maintainer could reuse

Each exercise asks for three things:

- the operational fact or boundary you are trying to establish
- the evidence or command that would establish it
- the tuning or response decision that follows from that evidence

Every timing answer must retain the semantic guardrail:

| Baseline command and samples | Proposed change | After samples | Convergence check | Artifact-equivalence check |
| --- | --- | --- | --- | --- |

If the last two columns are absent, you have measured speed but not a safe optimization.

## Minimum evidence for every answer

Try to include:

- one repeated measurement or trace excerpt
- one explicit statement of the layer being investigated
- one reason the proposed response preserves truth instead of merely suppressing cost

## Exercise 1: Split one "slow build" complaint into layers

Take one build route and describe how you would tell whether the cost is mainly parse-time,
recipe-time, or evidence-surface overhead.

What to hand in:

- the commands you would run
- the three measurements or observations you would compare
- one sentence explaining how different results would change the diagnosis

## Exercise 2: Add one bounded observability surface

Your repository has many ad hoc debug prints inside recipes, but no named diagnostic route.

Design one observability surface that would help incidents without mutating semantic
outputs.

What to hand in:

- the question the surface should answer
- the target name or command route you would add
- one current debug habit that should be removed instead

## Exercise 3: Write a triage ladder for one flaky symptom

Choose one flaky symptom such as:

- "rebuild happens for no obvious reason"
- "`-j` occasionally fails"
- "CI and local behave differently"

Write the first five steps of the evidence ladder you would follow.

What to hand in:

- the measurable symptom
- the ordered triage steps
- one sentence explaining why editing the Makefile should not be the first move

## Exercise 4: Propose one truth-preserving optimization

You identify repeated parse-time shell work as a likely cost. Explain one optimization that
reduces that waste without hiding real inputs or dropping rebuilds.

What to hand in:

- the expensive habit
- the truthful replacement boundary
- one command you would use afterward to prove the build is still honest

## Exercise 5: Write a small operational runbook entry

Take one build route and write a short runbook entry another engineer could use under
pressure.

What to hand in:

- one convergence or sanity check
- one serial/parallel comparison or resolved-state inspection
- one escalation trigger
- one thing the responder should avoid doing too early

## Exercise 6: Build a repeatable timing baseline

Measure dry-run, clean-build, and no-op-build cost at least three times each. Keep target,
parallelism, environment, and machine conditions recorded.

What to hand in:

- the exact commands and conditions
- all measurements plus a representative value
- one source of noise and how you limited it

## Exercise 7: Explain an unexpected rebuild

Choose a target that rebuilds when you expect a no-op. Use trace output and timestamps to
identify the prerequisite edge that caused the decision.

What to hand in:

- the target and expected behavior
- the smallest useful trace excerpt
- prerequisite timestamps or content evidence
- the graph repair, or an explanation that the rebuild is correct

## Exercise 8: Audit parse-time shell work

Find every `$(shell ...)` in a Make build. Measure dry-run cost, classify each shell call,
and replace one avoidable call without caching away real discovery.

What to hand in:

- the search result and baseline
- the selected shell call and its semantic purpose
- the replacement
- post-change timing, discovery, and convergence evidence

## Exercise 9: Measure useful parallelism

Compare `-j1`, `-j2`, and a higher job count for one clean route. Inspect the graph before
interpreting the timings.

What to hand in:

- repeated measurements
- the independent work visible in the graph
- the job count after which speedup becomes small or negative
- one reason the result must not be generalized to every machine

## Exercise 10: Respond to a complete build incident

Investigate a slow, noisy, flaky, or unexpectedly rebuilding route without cleaning or
editing first. Preserve commands, environment, timing, trace, resolved state, and the
final classification.

What to hand in:

- the incident statement and reproduction route
- a compact evidence directory
- the diagnosis and smallest truth-preserving repair
- before-and-after verification
- a runbook entry for the next responder

## Before you read the answers

Do not open `exercise-answers.md` until you can already point to:

- one symptom rewritten as a measurable claim
- one baseline with repeated samples
- one incident you investigated without editing first
- one optimization you rejected because it would have hidden truth

## Mastery standard for this exercise set

Across all ten answers, the module wants the same habits:

- you name the cost or incident boundary being tested
- you choose evidence before choosing edits
- you explain the response in terms of measurement, observability quality, or truth-preserving tuning

If an answer says only "the build should be easier to debug," keep going.
