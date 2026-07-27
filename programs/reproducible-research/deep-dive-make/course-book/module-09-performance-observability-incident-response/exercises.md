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

Run:

```sh
gmake -C "$CAPSTONE" perf PERFORMANCE_RUNNER=module09-local
```

Audit the `context` object in the generated `evidence.json`. Cross-check it against:

- repository revision
- worktree status
- GNU Make version
- compiler and Python versions used by the capstone
- platform and the stable runner label you chose
- relevant target help
- job count chosen for pressure runs

Use `gmake -C "$CAPSTONE" portability-audit` where it provides governed evidence. Review
any environment output before retaining or sharing it. Do not copy these values into a
separate packet and discard their binding to the timings.

What to hand in:

- the context object and the revision it names
- a table separating repository-controlled conditions from machine-controlled conditions
- one explanation of why comparison permits different revisions but rejects a changed
  compiler or runner
- the action you would take if repository status were `dirty`
- one condition you could not control and how it limits the claim

Checkpoint:
Another learner should know whether your result can reasonably be compared with theirs.

## Exercise 3: Establish controlled cost baselines

Use the governed route from Exercise 2. Read `route.txt`, `scenarios.tsv`,
`incremental-policy.tsv`, `incremental-summary.tsv`, and the context in `evidence.json`
before the timing `summary.tsv`.

Before opening `incremental-policy.tsv`, complete this prediction table:

| Input | Must rebuild | Two representative outputs that must remain |
| --- | --- | --- |
| `src/util.c` |  |  |
| `include/util.h` |  |  |
| `include/sub.h` |  |  |
| `scripts/gen_dynamic_h.py` |  |  |
| `src/dynamic/dyn1.c` |  |  |

Derive each answer by following dependency paths. Then compare your table with the policy
and observed summary. Confirm that every policy row classifies the same governed output
set.

For each scenario, trace one row in the summary back to:

- all raw elapsed samples in `evidence.json`
- its command transcript in `logs/`
- its convergence result
- its trusted-output inventory

Copy or preserve the complete bundle under `measurements/`; do not copy only the summary.
Explain why the collector establishes clean or converged state separately for each sample.

What to hand in:

- the governed scenario table
- one raw-sample-to-summary audit
- the convergence and trusted-output result for each scenario
- your completed five-input prediction table
- the governed-output-set comparison for two different input rows
- the observed missing and unexpected rebuild sets for every case
- one header-case trace and one generated-producer trace tied to their owning rules
- proof that the incremental result is bound inside `evidence.json`
- one leading and one competing explanation for the observed differences
- one sentence stating whether a performance regression was proven
- one machine condition that the bundle cannot fully control

Checkpoint:
Without a controlled historical baseline, the correct conclusion is usually "current
baseline established," not "regression confirmed." A summary without its semantic evidence
does not complete the exercise.

Explain why restoring each input after its mutation is necessary, why the runner reconverges
before each case, and why restoring an input does not mean generated outputs should be
rolled back before evidence is reviewed.

## Exercise 4: Choose observability by question

Run and retain:

```sh
gmake -C "$CAPSTONE" trace-report
gmake -C "$CAPSTONE" -np all
```

Do not submit the entire database dump as your explanation. Extract one rule or variable
that answers a question you state first.

Evaluate the trace on:

- declared build state and requested route
- searchability
- target and rule attribution
- causal usefulness
- semantic side effects
- bounded volume

What to hand in:

- one question answered by trace
- one different question answered by focused database inspection
- the smallest excerpts that support both answers
- one conclusion neither surface can establish alone
- the `trace-evidence.json` checks and one supporting raw trace line
- the failure you would expect if the focus target changed from `all` to an absent target

Checkpoint:
The exercise is incomplete if your judgment ignores state or collapses all checks into line
count. Explain why a one-line converged trace cannot replace a larger clean-plan trace.

## Exercise 5: Verify three parallel incident signatures

Before running anything, predict each case:

| Case | Expected exit | Required artifact observation | Wrong failure to reject |
| --- | --- | --- | --- |
| shared log interleaving | | | |
| directory creation race | | | |
| shared staging collision | | | |

Generate the complete capstone incident bundle:

```sh
gmake -C "$CAPSTONE" incident-audit
```

Read:

1. `summary.tsv`
2. `report.json`
3. every named file under `runs/`
4. every named file under `evidence/`
5. the matching workspace and specimen

What to hand in:

- the completed prediction table with observed results added
- the three findings reported by the audit
- the exact semantic evidence that supports each finding
- an explanation of why aggregate `PASS` means the broken specimens behaved as promised
- one mismatch that should make each case fail its own audit
- one sentence explaining why neither zero nor nonzero exit status proves the mechanism

Then isolate one case:

```sh
gmake -C "$CAPSTONE" incident-audit \
  INCIDENT_CASE=shared-staging-collision
```

Confirm that the report contains one case while the bundle retains the review guidance
and specimen catalog.

Checkpoint:
You must classify from preserved semantic state before reading the repair guidance. A
table containing only exit statuses is incomplete.

## Exercise 6: Route each incident to an ownership repair

Build a competing-explanations table for all three incidents:

| Explanation | Evidence expected if true | Evidence that weakens it |
| --- | --- | --- |
| shared publication ownership | | |
| repeated setup ownership | | |
| parallel scheduler defect | | |
| external filesystem failure | | |

Complete this repair table:

| Case | Boundary | Temporary mitigation | Durable repair | Adjacent proof |
| --- | --- | --- | --- | --- |
| shared log | | | | |
| directory race | | | | |
| shared staging | | | | |

Evaluate these proposals:

- force `-j1`
- add more `echo` lines
- replace every `mkdir` with `mkdir -p`
- declare one directory setup target and use order-only edges
- declare one target that owns a combined output
- give each producer a private staging or worker path

What to hand in:

- the completed explanation table
- the completed repair table
- mitigation, repair, and rejected-action labels for the proposals
- one graph sketch for directory ownership
- one graph sketch for private worker output plus deterministic merge
- the serial, parallel, convergence, and failure-cleanup proof required before closure

Checkpoint:
Every preferred repair must make setup, intermediate, and final output ownership visible
in the graph. Do not use one repair shape for all three cases.

## Mid-lab review

Stop before tuning. Your packet should now answer:

- which cost claims have actually been established
- which trace or database evidence changed a decision
- why the controlled incident is a graph/publication defect
- why serial execution is at most temporary mitigation

If any answer relies on "Make is slow" or "parallelism is unreliable," return to the
evidence.

## Exercise 7: Write a falsifiable tuning proposal

First prove the evidence route discriminates:

```sh
gmake -C "$CAPSTONE" performance-selftest
```

Name two rejected cases and explain why accepting either would make a speedup claim
dishonest.

Before choosing a tuning candidate, classify these bundle pairs:

| Pair | Baseline | Candidate |
| --- | --- | --- |
| A | clean revision `a`, runner `lab`, compiler `cc 1`, expected work observed | clean revision `b`, runner `lab`, compiler `cc 1`, expected work observed |
| B | clean revision `a`, runner `lab`, compiler `cc 1`, expected work observed | dirty revision `b`, runner `lab`, compiler `cc 1`, expected work observed |
| C | clean revision `a`, runner `lab`, compiler `cc 1`, expected work observed | clean revision `b`, runner `lab`, compiler `cc 2`, expected work observed |
| D | clean revision `a`, runner `lab`, compiler `cc 1`, five input cases present | clean revision `b`, runner `lab`, compiler `cc 1`, the `include/sub.h` case is absent |
| E | clean revision `a`, runner `lab`, compiler `cc 1`, expected work observed | clean revision `b`, runner `lab`, compiler `cc 1`, the `src/dynamic/dyn1.c` case rebuilds `app` |

For each pair, predict `compare` or `reject`, name the field that decides it, and state what
work would make a rejected pair reviewable. Pair E may represent an intentional graph
change; explain why that still blocks the original timing comparison.

Choose one real cost candidate from the capstone or explicitly reject tuning because the
measurements do not justify it.

If you propose a change, create `tuning-decision.md` with:

- measured cost and localized boundary
- critical-path relevance
- proposed change
- truth invariant most at risk
- controlled before-and-after comparison
- compatible scenario policy and sample count
- matching execution context except for the named clean revisions
- requested-work test
- explicit expected-work and expected-non-work sets
- convergence test
- artifact comparison
- serial/parallel pressure test
- rejection condition

If no change is justified, write the evidence threshold that would cause you to reopen the
decision.

What to hand in:

- the performance-selftest result and two rejection explanations
- the five-pair compatibility table
- the complete experiment contract or justified rejection
- one unsafe optimization you rejected
- one sentence explaining what new freshness contract a cache would introduce

Checkpoint:
"Expected to be faster" is not a measured cost, and "tests pass" is not a complete semantic
proof. A passing comparison reports compatible deltas; it does not decide materiality for
you.

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
- command-level evidence and preserved failure state

Write `verification.md` explaining which proof dimension each file covers and which
performance claim the bundle does not cover.

What to hand in:

- a claim-to-file table
- the serial/parallel comparison result
- the convergence result
- how `FAIL` differs from `NOT_RUN` in the summary
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
