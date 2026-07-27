# Exercise Answers

These answers are model explanations, not the only acceptable wording.

What matters is whether the reasoning stays evidence-first and truth-preserving.

## How to use these answers

Do not read this file before attempting the exercises yourself.

Use it for three kinds of comparison:

1. check whether you named the right boundary or cost class
2. check whether you chose evidence in a disciplined order
3. check whether your proposed response preserved workflow meaning

If your wording differs but your reasoning is equally precise and equally honest, your
answer can still be strong.

The strongest self-study packets also leave behind six concrete artifacts:

- one cost-class note
- one evidence-order note
- one raw baseline record
- one bounded incident packet
- one single-boundary tuning note
- one revised runbook

If your answers rely only on feelings of slowness or one lucky faster run, the reasoning
is still too thin.

## Exercise 1: Name the dominant cost class

Strong diagnosis:

- the dominant lead is planning and discovery cost

Why:

- dry-run is already slower, which means the problem begins before tool execution
- benchmark files for the heavy rules are unchanged, which weakens the case for a tool
  runtime regression
- the discovered sample list is larger, which suggests the workflow is planning more work

What is not the strongest lead right now:

- pure tool runtime
- a benchmark-detectable slowdown in the heavy rules

What to inspect next:

- the discovery artifact or sample list
- the dry-run target set
- the recent edit that changed discovery behavior

The main lesson is to name the planning problem before touching execution settings.

## Exercise 2: Choose the right evidence surface

First artifact to inspect:

- `snakemake --summary`

Why:

- the claim begins with a surprising rebuild of `summary.tsv`, so workflow-state evidence
  should come before rule-runtime evidence

Second artifact if the first one does not support the claim:

- the benchmark file for the aligner rule family

Why:

- once the rebuild scope is understood, benchmark evidence can test whether the aligner
  itself became slower

The important distinction is that `--summary` tells you what changed in workflow state,
while the benchmark tells you what a specific rule cost.

Weak answers usually start at the loudest log file and only later ask what question they
were trying to answer.

## Exercise 3: Triage a flaky cluster-only incident

Why the proposed fix is not yet sufficient:

- raising retries and latency waits changes operating policy without first classifying the
  failure
- it may hide a deterministic storage, staging, or profile problem

Incident class to test first:

- operating context or storage behavior

Why:

- the incident appears only on one scheduler-backed profile

Evidence to consult first:

- the relevant rule logs for failing targets
- benchmark or timing evidence for the same rule family
- provenance or profile evidence such as `make -C capstone profile-audit`

The main lesson is that cluster-only incidents should not be flattened into "needs more
retries."

Weak answers usually skip classification and jump straight to policy inflation.

## Exercise 4: Review a suspicious optimization

Potentially valid tuning move:

- grouping several tiny QC jobs into one aggregation step

Why it may be valid:

- grouping can honestly reduce scheduler overhead if the declared outputs, failure
  visibility, and evidence surfaces stay reviewable

Semantic or evidence regressions:

- removing one declared input from a slow rule
- deleting benchmark files because they create clutter

Why:

- removing a declared input changes workflow meaning and rerun truth
- deleting benchmark files weakens the evidence surface needed for performance review

Proof required before approving the valid part:

- dry-run showing the same semantic target set
- benchmark evidence at the new grouped boundary
- confirmation that output and failure visibility remain usable

Weak answers praise the speed idea without checking whether the review surface survived.

## Exercise 5: Draft a runbook entry

A strong minimal runbook entry could say:

1. Run `snakemake -n -p` or `make -C capstone wf-dryrun` first.
2. Check `snakemake --summary` to see whether the workflow state matches the report.
3. Inspect one matching rule log and one benchmark file for the suspicious rule family.
4. If the issue appears context-specific, run `make -C capstone profile-audit`.
5. Escalate when the issue points to profile drift, publish trust, or a semantic change
   rather than local runtime behavior.
6. Prove the repair with `make -C capstone tour` or `make -C capstone verify-report`,
   depending on whether execution evidence or published trust is the main question.

Why this is strong:

- it starts with the narrowest honest command
- it separates workflow-state evidence from rule-local evidence
- it includes a real escalation trigger
- it ends with a proof route rather than with vague advice

Weak runbooks say "inspect logs" or "rerun with more resources" without telling the next
maintainer how to know whether the issue is semantic, operational, or already resolved.

The missing but important sentence is usually this one:

> After the first command, the maintainer should expect one specific observation before
> continuing, otherwise the runbook has already lost the thread of the incident.

## Exercise 6: Establish a measured baseline

Use identical inputs and context for repeated runs, retaining raw observations rather than
only an average.

Why:

- median resists one extreme value
- range reveals variability
- planning, end-to-end, and rule-local measurements answer different questions

What a strong answer says explicitly:

- what was held constant
- what remained uncontrolled
- why the baseline is informative but still conditional on context

Example answer shape:

- planning measurements:
  - five `snakemake -n` timings written under `artifacts/baselines/planning.tsv`
- execution measurements:
  - five end-to-end runs on unchanged inputs
- heavy-rule measurements:
  - benchmark rows for the dominant align or summarize step
- summary:
  - "planning median was 7.2 seconds with a 1.1 second range; total runtime median was
    88 seconds with a 6 second range; the heavy rule median was 53 seconds with a 2 second
    range"

Why this is strong:

- it preserves raw evidence
- it separates planning, total runtime, and rule-local cost
- it keeps the baseline conditional rather than pretending it is universal

The key explanatory sentence is:

> A single fast run is not a baseline because it cannot tell you whether the improvement
> was real, noisy, or accidental.

## Exercise 7: Build an incident evidence packet

The packet states an observable symptom and bounded scope before offering a theory.

It includes:

- planned jobs
- file-status evidence
- one relevant log
- timing evidence
- provenance needed to reproduce the state

A strong packet separates known facts from hypotheses and avoids dumping unrelated logs.
Another maintainer should be able to classify the incident without asking what command was
run.

Example packet shape:

- symptom:
  - "`publish/v1/report.html` took 4x longer on CI than on local runs"
- bounded scope:
  - "only the reporting family, only the CI profile, first seen after commit X"
- evidence:
  - one dry-run, one summary, one relevant rule log, one benchmark row, one provenance or
    profile record
- unknowns:
  - whether the delay is scheduler overhead or slower shared storage

Why this is strong:

- it makes the scope explicit
- it avoids burying the real question inside unrelated artifacts
- it records what is still unknown instead of pretending certainty

## Exercise 8: Tune one boundary at a time

Change only the hypothesized overhead source, repeat measurements, and compare semantic
outputs or their governed checksums.

Keep the change only when:

- the distribution improves meaningfully
- failure visibility remains intact
- target membership remains intact
- output meaning remains intact

If results overlap the baseline or evidence weakens, revert rather than rationalize.

Example answer shape:

- hypothesis:
  - "grouping per-fragment QC into one per-sample step will reduce scheduler overhead"
- single change:
  - change only the QC boundary, keep inputs, outputs, and publish rules the same
- repeated measurements:
  - compare five before/after runs
- semantic comparison:
  - compare checksummed public outputs and representative QC tables
- decision:
  - keep the change only if speed improves materially and the same trusted outputs remain

Weak answers declare victory after one lucky faster run.

The strongest answers also say explicitly that a small speed gain is not worth keeping if
the workflow’s semantic truth, failure visibility, or review surface got weaker.

## Exercise 9: Diagnose a context-specific regression

Queue timestamps distinguish waiting from execution. Job launch records reveal scheduler
overhead, logs and latency events reveal storage behavior, resource telemetry reveals
pressure, and benchmarks isolate tool runtime.

A strong answer rejects higher retries until evidence shows a transient class. The
smallest useful experiment changes one context factor while preserving the target and
input set.

Example answer shape:

- queue delay evidence:
  - timestamps show jobs waited 90 seconds before starting
- launch overhead evidence:
  - many tiny jobs spend more time entering the scheduler than computing
- storage evidence:
  - no strong latency errors in logs
- tool runtime evidence:
  - benchmark medians unchanged
- strongest supported class:
  - scheduler overhead under the current context

A strong answer rejects "increase retries" here because retries do not fix queued jobs
that are merely too small and too numerous.

## Exercise 10: Rehearse and revise a runbook

Observed reader stalls are evidence that the runbook assumes hidden knowledge.

Revise it with:

- prerequisites
- exact bounded commands
- expected evidence
- stop conditions
- escalation ownership

A successful rehearsal reaches the appropriate verification route without destructive
cleanup, indiscriminate retries, or an unrelated full-suite run.

Example revision moves:

- add the exact prerequisite state
- replace "check the logs" with the specific log path family
- add one expected observation after each command
- add a stop condition that prevents cargo-cult retries

Why this matters:

- a runbook is itself an evidence surface
- if another maintainer cannot follow it safely, the repository still depends on oral
  tradition

Weak answer pattern:

- "the workflow is slow, so we tuned some settings and it seemed better"

That sentence skips cost class, evidence order, and semantic guardrails all at once. If
your answers still sound like that, keep revising.

## Self-check

If your answers consistently explain:

- which cost class is dominant
- which evidence surface fits the question
- what incident class is under review
- what semantic truth must remain unchanged

then you are using Module 09 correctly.
