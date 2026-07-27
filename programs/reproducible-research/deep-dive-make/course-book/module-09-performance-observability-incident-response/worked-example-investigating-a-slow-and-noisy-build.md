# Worked Example: Investigating a Slow and Noisy Build

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Performance Observability Incident Response"]
  page["Worked Example: Investigating a Slow and Noisy Build"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  claim["rewrite the complaint"] --> baseline["establish a controlled baseline"]
  baseline --> guardrail["interpret the evidence guardrail"]
  guardrail --> incident["open one executed incident"]
  incident --> classify["classify ownership"]
  classify --> runbook["write a reusable response"]
```
<!-- page-maps:end -->

This worked example uses the course capstone. It does not ask you to imagine a repository
or accept invented timings. You will:

1. turn "slow and noisy" into separate claims
2. establish clean and no-op evidence on the reference build
3. inspect its bounded trace guardrail
4. generate an executed parallel incident bundle
5. distinguish successful exit status from truthful output ownership
6. write the first runbook branch

Run the commands from the repository root. They use `gmake` because macOS commonly reserves
`make` for an older GNU Make. On Linux, use `make` only after `make --version` confirms GNU
Make 4.3 or newer.

Set a shell variable only to keep the commands readable:

```sh
CAPSTONE=programs/reproducible-research/deep-dive-make/capstone
```

The variable is local convenience, not part of the build contract.

## The report

Assume a teammate files this message:

> The capstone build is slow, the trace is noisy, and parallel execution looks suspicious.
> Can we reduce the diagnostics and force serial mode?

There are at least three claims hidden inside it:

| Complaint | Measurable claim | First evidence |
| --- | --- | --- |
| slow | one named route and state exceeds a stated baseline | repeated clean, no-op, or dry-run samples |
| noisy | one evidence surface is too large or hard to interpret | trace count plus usability inspection |
| suspicious under parallelism | a pressure route changes output or correctness | governed serial/parallel comparison or incident repro |

The proposed changes do not follow yet. Removing diagnostics could hide causality. Forcing
serial mode could hide an ownership defect. First, classify each claim.

## Preserve the starting context

Create the incident packet:

```sh
mkdir -p artifacts/module09-incident
git rev-parse HEAD > artifacts/module09-incident/revision.txt
git status --short > artifacts/module09-incident/worktree.txt
gmake --version > artifacts/module09-incident/make-version.txt
```

Write `artifacts/module09-incident/incident.md` in this shape:

```text
Route under review: capstone `all`
Build states: clean and no-op
Parallel concern: controlled shared-output repro
Observed claim: not yet established
Expected contract: `all` converges; selftest proves serial/parallel equivalence
Proposed shortcuts to evaluate: remove diagnostics; force serial execution
```

Notice the phrase "not yet established." A ticket is not a baseline.

## Read the public route before measuring it

Discover the capstone surface:

```sh
gmake -C "$CAPSTONE" help \
  > artifacts/module09-incident/help.txt
gmake -C "$CAPSTONE" perf \
  > artifacts/module09-incident/perf-command.txt 2>&1
```

The relevant target meanings are:

- `all` builds the application, dynamic binaries, and a convergence sentinel
- `trace-report` records a clean planning trace with attribution and usability checks
- `selftest` checks convergence and serial/parallel equivalence
- `incident-audit` executes one controlled failure specimen and saves a review bundle
- `perf` executes governed clean, no-op, and dry-run scenarios and writes review evidence
- `performance-selftest` proves the evidence gates accept truth and reject controlled drift

This reading step matters. Timing an undocumented helper would not establish the cost of
the public build contract.

## Read the experiment contract before the numbers

The command writes:

```text
artifacts/performance/reproducible-research/deep-dive-make/current/
├── PERFORMANCE_EVIDENCE_GUIDE.md
├── evidence.json
├── logs/
├── manifest.json
├── route.txt
├── scenarios.tsv
└── summary.tsv
```

Read `scenarios.tsv` first:

```text
# scenario	state	jobs	route
clean-build	clean	4	all
converged-noop	converged	1	all
converged-dry-run	converged	1	dry-run-all
```

Now the words *clean*, *no-op*, and *dry-run* have executable meanings. The collector, not
the learner's memory, establishes each precondition.

Cleaning is appropriate for `clean-build` because the experiment contract explicitly asks
for a clean route. It would still be the wrong first action on an unpreserved production
incident.

## Inspect distributions and semantic proof

Open `summary.tsv`. Your values will differ, but its shape is stable:

```text
scenario  state  jobs  samples  minimum  median  maximum  spread  convergence
```

For each scenario, check:

- the sample count matches the policy you intended to run
- median is reported with minimum, maximum, and spread
- convergence is `PASS`
- no sample has a nonzero exit status in `evidence.json`
- the trusted-output inventory names all five declared outputs

The clean route describes full production cost. The no-op route describes an already
converged invocation. Dry-run localizes work before ordinary recipe execution but does not
isolate parsing.

If no compatible earlier bundle exists, write:

> A governed local baseline now exists. No performance regression has been established.

That is a completed finding, not a failure to diagnose.

## Check necessary incremental work

Open `incremental-policy.tsv`, then `incremental-work.json`. Confirm:

```text
input=src/util.c
missing_rebuild=[]
unexpected_rebuild=[]
result=PASS
```

The report should show `build/util.o`, `app`, and `all` as rebuilt, while unrelated objects
and dynamic outputs remain untouched. This evidence answers a question the timing
distribution cannot: did the build stay selective without becoming stale?

If `build/util.o` is missing, stop the performance claim because the graph lost a required
edge. If `build/bin/dyn1` appears unexpectedly, investigate why unrelated work was selected
before claiming an incremental improvement.

## Prove that the gate can reject dishonesty

Run:

```sh
gmake -C "$CAPSTONE" performance-selftest \
  > artifacts/module09-incident/performance-selftest.txt 2>&1
```

The tests include controlled policy drift, sample-count drift, failed evidence, and changed
trusted outputs. A useful comparison gate must reject all four.

You can also observe the public missing-baseline boundary:

```sh
if gmake -C "$CAPSTONE" performance-compare \
  > artifacts/module09-incident/missing-baseline.txt 2>&1; then
  printf '%s\n' 'unexpected comparison success' >&2
  exit 1
fi
```

Read the captured output. The failure is correct because a candidate timing cannot compare
itself with an unstated past.

## Inspect the trace evidence

Run:

```sh
gmake -C "$CAPSTONE" trace-report
```

Read `trace-evidence.json` before `trace.log`. Confirm the report says `state=clean-plan`,
`focus_target=all`, and `result=PASS`. Then inspect:

- whether `all` appears among planned targets
- whether rule locations identify the owning Makefiles
- whether the line count is below the declared boundary
- whether the raw trace explains why representative targets would run

The target establishes clean state, so do not compare its count with a trace captured after
convergence. If focus or attribution fails, the evidence is unusable even when it is short.
If volume alone fails, inspect repeated low-value lines before changing the boundary. Do not
merge this conclusion with timing: trace usability and route cost remain separate claims.

## Generate a controlled incident

The capstone includes a repro where two targets append to one shared file. Generate its
incident bundle:

```sh
gmake -C "$CAPSTONE" incident-audit \
  REPRO_CASE=repro/shared-log-interleaving.mk
```

The bundle appears under:

```text
artifacts/audit/reproducible-research/deep-dive-make/incident/
```

Read these files in order:

1. `command.txt`
2. `run.txt`
3. `exit-status.txt`
4. `shared-log-interleaving.mk`
5. `INCIDENT_REVIEW_GUIDE.md`

An observed bundle contains:

```text
printf 'A\n' >> shared.log
printf 'B\n' >> shared.log
```

and:

```text
exit_status=0
```

That is the important surprise. The route can exit successfully while the graph still
models shared mutable output dishonestly.

## Classify from ownership, not from exit status

The copied repro contains:

```make
all: log1 log2

log1:
	printf 'A\n' >> shared.log

log2:
	printf 'B\n' >> shared.log
```

Ask the ownership question:

> Which target owns `shared.log`?

The honest answer is "neither owns it uniquely." Two independent targets mutate the same
path, and `shared.log` is not even a declared target. Parallel scheduling exposes the
problem, but parallelism did not create it.

Classify the incident:

| Field | Decision |
| --- | --- |
| boundary | graph truth and publication ownership |
| immediate risk | nondeterministic shared output |
| misleading signal | exit status `0` |
| mitigation | serial mode may reduce exposure but does not repair ownership |
| repair direction | one target owns the file, or each worker owns separate output followed by a declared merge |
| proof after repair | repeated pressure runs, stable content, one writer, and convergence |

Now the suggestion to force serial mode can be rejected as a completed fix. It changes the
scheduler while leaving two undeclared writers.

## Connect the repro back to the real build

Do not "repair" the controlled repro and stop. It is a teaching specimen. Use the real
capstone proof route:

```sh
gmake -C "$CAPSTONE" selftest-report
```

Read:

```text
artifacts/proof/reproducible-research/deep-dive-make/selftest/
├── summary.txt
├── settings.env
├── commands.txt
├── schedule-comparison.json
├── serial-inventory.json
├── parallel-inventory.json
├── hidden-input.txt
├── logs/
└── workspace/
```

The comparison classifies missing, unexpected, and changed artifacts before the two
inventories provide path-level detail. The command logs and preserved workspace keep a
failed stopping boundary reviewable. The repro demonstrates the failure class; the
selftest bundle demonstrates the production proof shape.

## Write the runbook branch

Add this to `artifacts/module09-incident/runbook.md`:

```text
Entry: a route differs under parallel execution or mutates one shared output.

Preserve:
- command, revision, Make version, job count, output, and artifact state
- do not clean before capture

Classify:
- search for every writer of the suspect path
- use target-attributed output and non-executing trace

If multiple targets write one path:
- stop publication of that output
- treat serial mode only as labeled mitigation
- repair to one owner or isolated worker outputs plus one merge target

Close when:
- repeated pressure runs pass
- serial and parallel artifact comparisons satisfy the contract
- the route converges
```

This branch can be used by someone who did not attend the class.

## The final decision

The original complaint does not produce one verdict:

- "slow" requires comparison with a controlled historical baseline; this exercise
  establishes the missing baseline
- "noisy" must be evaluated by trace usability and responder value, not dislike of output
- the parallel concern is real in the controlled repro, but serial mode is only mitigation
- removing diagnostics would weaken the evidence needed to classify the ownership defect

A strong incident summary is:

> We separated the broad complaint into cost, evidence, and pressure claims. The capstone
> now has a governed clean, no-op, and dry-run baseline whose scenarios, samples,
> convergence, and trusted outputs are reviewable. Its trace is evaluated by searchability
> as well as line count. The executed repro exits successfully but reveals
> two undeclared writers to one shared file, so the defect is output ownership rather than
> "too much parallelism." Serial execution is temporary mitigation; repair requires one
> publication owner and schedule-equivalence proof.

## Exit check

You have completed the example when you can point to:

- governed clean, no-op, and dry-run samples with their scenario contract
- convergence and trusted-output evidence beside every timing distribution
- the declared and observed incremental rebuild scope
- one performance-gate rejection you can explain
- the trace state, focus target, semantic checks, and one raw causal line
- the incident bundle's command, output, status, and copied makefile
- a classification that does not rely on exit status alone
- the selftest report that represents the repaired proof shape
- a runbook branch another learner could follow without you
