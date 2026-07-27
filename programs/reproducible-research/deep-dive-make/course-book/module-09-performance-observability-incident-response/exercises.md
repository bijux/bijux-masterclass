# Exercises

These ten exercises form one incident-response lab. Use the course capstone so the
commands, failure specimens, and proof surfaces are available to a learner working alone.
If you substitute another repository, map every named capstone target to an equivalent
public contract before starting.

The lab does not ask you to make the capstone faster. It asks you to determine what the
evidence justifies, reject unsafe shortcuts, and leave a packet another maintainer can
review.

## Lab boundary

Run from the repository root. These instructions use `gmake` for GNU Make 4.3+ on macOS.
On Linux, use `make` only after confirming the required version.

```sh
CAPSTONE=programs/reproducible-research/deep-dive-make/capstone
PACKET=artifacts/module09-lab
mkdir -p "$PACKET"
```

Your packet should end with:

```text
artifacts/module09-lab/
├── incident.md
├── context/
├── measurements/
├── observability/
├── parallel-incident/
├── tuning-decision.md
├── verification.md
├── runbook.md
└── handoff.md
```

Do not use generated evidence from another learner. The point is to preserve and explain
your own run.

## Evidence rules for the whole lab

Apply these rules to every exercise:

1. record the exact command before interpreting its output
2. distinguish observed fact, inference, and decision
3. keep all timing samples, not only the fastest
4. do not clean an incident state unless the question explicitly requires clean state
5. state what each evidence surface cannot prove
6. do not call serial mode a repair for a parallel-only defect
7. keep credentials and other sensitive environment values out of submissions

Use this notation in your notes:

```text
Observed:
Inferred:
Still unknown:
Decision:
```

That structure makes unsupported jumps visible.

## Exercise 1: Open the incident without accepting its diagnosis

Use this report:

> The capstone is slow and noisy. Parallel Make may be the cause. Remove some diagnostics
> and force serial execution.

Create `incident.md`. Rewrite the report into separate measurable claims for:

- clean-build cost
- no-op cost
- dry-run cost
- trace usability
- parallel correctness

For each claim, name:

- the requested target and build state
- the expected behavior and its source
- the first evidence surface
- one shortcut that must not be taken before evidence is preserved

What to hand in:

- `incident.md`
- one paragraph explaining why the proposed diagnosis and remedies are premature
- one risk that would require immediate containment rather than ordinary measurement

Checkpoint:
Your incident statement must make it possible for two learners to run comparable routes.

## Exercise 2: Capture a reproducibility context

Populate `context/` with:

- repository revision
- worktree status
- GNU Make version
- compiler and Python versions used by the capstone
- relevant target help
- job count chosen for pressure runs

Use `gmake -C "$CAPSTONE" portability-audit` where it provides governed evidence. Review
any environment output before retaining or sharing it.

What to hand in:

- the context files
- a table separating repository-controlled conditions from machine-controlled conditions
- one condition you could not control and how it limits the claim

Checkpoint:
Another learner should know whether your result can reasonably be compared with theirs.

## Exercise 3: Establish controlled cost baselines

Collect five samples for each route:

1. clean `gmake -j4 all`
2. confirmed no-op `gmake all`
3. converged dry-run `gmake -n all`

Save the exact command, every sample, median, minimum, and maximum under `measurements/`.
Before no-op timing, prove `gmake -q all` succeeds. Keep clean and no-op results in separate
tables.

What to hand in:

- raw timing files
- a summary table with state and parallelism
- one leading and one competing explanation for the observed differences
- one sentence stating whether a performance regression was proven

Checkpoint:
Without a controlled historical baseline, the correct conclusion is usually "current
baseline established," not "regression confirmed."

## Exercise 4: Choose observability by question

Run and retain:

```sh
gmake -C "$CAPSTONE" trace-count
gmake -C "$CAPSTONE" --trace -n all
gmake -C "$CAPSTONE" -np all
```

Do not submit the entire database dump as your explanation. Extract one rule or variable
that answers a question you state first.

Evaluate the trace on:

- searchability
- target and rule attribution
- causal usefulness
- semantic side effects

What to hand in:

- one question answered by trace
- one different question answered by focused database inspection
- the smallest excerpts that support both answers
- one conclusion neither surface can establish alone
- a keep, narrow, or retire decision for `trace-count`

Checkpoint:
The exercise is incomplete if your only observability judgment is a line count.

## Exercise 5: Generate and preserve a parallel incident

Create a capstone incident bundle:

```sh
gmake -C "$CAPSTONE" incident-audit \
  REPRO_CASE=repro/shared-log-interleaving.mk
```

Copy or reference the generated bundle from `parallel-incident/` and read:

1. the recorded command
2. executed output
3. exit status
4. copied repro Makefile
5. incident review guide

What to hand in:

- the observed command and exit status
- the two targets and the path they both mutate
- one sentence explaining why exit status `0` does not prove graph truth
- one piece of evidence to preserve before any rerun or cleanup

Checkpoint:
You must describe the incident from the executed bundle before reading the repair guidance.

## Exercise 6: Classify ownership and reject false repairs

Build a competing-explanations table for the shared-log incident:

| Explanation | Evidence expected if true | Evidence that weakens it |
| --- | --- | --- |
| missing ownership or publication model | | |
| parallel scheduler defect | | |
| external filesystem failure | | |

Then classify the boundary and evaluate these proposals:

- force `-j1`
- add more `echo` lines
- declare one target that owns the shared file
- give each worker a private output and merge them through one target

What to hand in:

- the completed explanation table
- the boundary owner
- mitigation, repair, and rejected-action labels for the proposals
- one graph sketch of the preferred repair direction
- the proof required before closing the incident

Checkpoint:
The preferred repair must make output ownership visible in the graph.

## Mid-lab review

Stop before tuning. Your packet should now answer:

- which cost claims have actually been established
- which trace or database evidence changed a decision
- why the controlled incident is a graph/publication defect
- why serial execution is at most temporary mitigation

If any answer relies on "Make is slow" or "parallelism is unreliable," return to the
evidence.

## Exercise 7: Write a falsifiable tuning proposal

Choose one real cost candidate from the capstone or explicitly reject tuning because the
measurements do not justify it.

If you propose a change, create `tuning-decision.md` with:

- measured cost and localized boundary
- critical-path relevance
- proposed change
- truth invariant most at risk
- controlled before-and-after comparison
- requested-work test
- convergence test
- artifact comparison
- serial/parallel pressure test
- rejection condition

If no change is justified, write the evidence threshold that would cause you to reopen the
decision.

What to hand in:

- the complete experiment contract or justified rejection
- one unsafe optimization you rejected
- one sentence explaining what new freshness contract a cache would introduce

Checkpoint:
"Expected to be faster" is not a measured cost, and "tests pass" is not a complete semantic
proof.

## Exercise 8: Audit the capstone proof route

Run:

```sh
gmake -C "$CAPSTONE" selftest-report
```

Inspect the generated selftest bundle. Map its files to these claims:

- build convergence
- serial/parallel artifact equivalence
- hidden-input detection
- runtime and guardrail settings

Write `verification.md` explaining which proof dimension each file covers and which
performance claim the bundle does not cover.

What to hand in:

- a claim-to-file table
- the serial/parallel comparison result
- the convergence result
- one limitation of the selftest as performance evidence
- one additional proof your tuning proposal would require

Checkpoint:
The selftest proves build invariants. It does not prove a speedup.

## Exercise 9: Write an executable runbook

Create `runbook.md` for:

> a public build route differs or fails only under parallel execution

Include:

- entry and non-entry conditions
- trusted outputs at risk
- first preservation and containment actions
- two evidence branches with different next actions
- a serial route labeled correctly as mitigation if used
- recovery and convergence checks
- escalation triggers and owner
- closure criteria
- the date or event that should trigger the next runbook exercise

Every command must have an expected observation and a branch.

What to hand in:

- the runbook
- one command you deliberately excluded because it mutates state too early
- one peer-review question that tests whether the runbook needs private context

Checkpoint:
A learner unfamiliar with the capstone should know when to stop, escalate, and close.

## Exercise 10: Hand off the incident

Write `handoff.md` as if the investigation is moving to the build owner.

Include:

- symptom and impact
- state and context preserved
- measurements collected
- explanations strengthened and weakened
- current boundary classification
- active containment or mitigation
- tuning decision
- verification completed
- one exact unresolved question for the next owner
- packet reading order

Then audit the complete packet for:

- commands without results
- results without interpretation
- decisions without competing explanations
- timing claims without build state
- raw environment values that should not be shared
- temporary mitigation presented as repair

What to hand in:

- `handoff.md`
- the final packet tree
- a short removal or redaction list
- one paragraph explaining how the packet would shorten the next response

Checkpoint:
The next owner should not need a meeting to understand what has been observed, decided,
and left unresolved.

## Before you read the answers

Do not open `exercise-answers.md` until your packet contains:

- one controlled baseline rather than one timing
- one observability conclusion based on usability as well as volume
- one executed incident classification
- one rejected false repair
- one experiment contract or justified no-change decision
- one claim-to-proof map
- one branched runbook
- one bounded handoff question

## Mastery standard

A strong submission does not necessarily change code. It shows disciplined operational
judgment:

- state is preserved before mutation
- claims are narrower than complaints
- evidence is chosen to distinguish explanations
- performance and correctness remain separate proof obligations
- mitigations are not renamed as repairs
- another maintainer can reuse the packet without private context
