<a id="top"></a>

# Module 09 — Performance, Observability, and Workflow Incident Response

Once a workflow is correct and operationally portable, the next challenge is keeping it
understandable when runs become slow, noisy, or flaky. Performance work in Snakemake is
not about chasing smaller timings for their own sake. It is about preserving useful
feedback loops and making the workflow debuggable when something behaves differently under
real load.

This module teaches a cost model for workflow performance, the observability surfaces that
make incidents explainable, and the review habits that keep tuning from quietly damaging
workflow truth.

### Before You Begin

This module works best after Modules 01-08, especially the parts on dynamic DAGs,
operating contexts, publish boundaries, and reusable architecture.

Use this module if you need to learn how to:

* tell scheduler cost from actual computation cost
* add observability without flooding the workflow with meaningless noise
* diagnose slow or flaky runs with a repeatable incident ladder

Proof loop for this module:

```bash
snakemake -n -p
snakemake --summary
snakemake --list-changes input code params
```

Capstone corroboration:

* inspect `capstone/benchmarks/`
* inspect `capstone/logs/`
* inspect `capstone/Makefile` targets such as `wf-dryrun`, `verify`, and `tour`
* inspect `capstone/tests/test_workflow_integration.py`

---

<a id="toc"></a>
## 1) Table of Contents

1. [Table of Contents](#toc)
2. [Learning Outcomes](#outcomes)
3. [How to Use This Module](#usage)
4. [Core 1 — A Cost Model for Snakemake Runs](#core1)
5. [Core 2 — Logs, Benchmarks, Summaries, and Drift Reports](#core2)
6. [Core 3 — Incident Triage for Slow or Flaky Workflows](#core3)
7. [Core 4 — Tuning Without Hiding Truth](#core4)
8. [Core 5 — Operational Runbooks and Review Surfaces](#core5)
9. [Capstone Sidebar](#capstone)
10. [Exercises](#exercises)
11. [Closing Criteria](#closing)

---

<a id="outcomes"></a>
## 2) Learning Outcomes

By the end of this module, you can:

* distinguish workflow planning cost, scheduling cost, and real compute cost
* add observability surfaces that help incident response instead of creating more confusion
* diagnose slow or flaky runs using a fixed evidence-first ladder
* tune workflow structure while preserving file-contract truth and reproducibility
* produce a short operational runbook that another maintainer can actually use

[Back to top](#top)

---

<a id="usage"></a>
## 3) How to Use This Module

Take one working workflow and collect four surfaces:

```text
lab/
  workflow/
  logs/
  benchmarks/
  docs/
    incident-notes.md
```

For one representative run, capture:

1. dry-run output
2. a summary or drift report
3. per-rule logs or benchmarks
4. one written incident note describing what was slow, noisy, or surprising

This module goes well only when you compare symptoms with evidence instead of guessing
from memory.

[Back to top](#top)

---

<a id="core1"></a>
## 4) Core 1 — A Cost Model for Snakemake Runs

Performance problems in Snakemake usually come from one of several places:

* workflow planning or discovery
* scheduler overhead across many small jobs
* filesystem or staging latency
* the real computation inside tools or scripts

Those are not interchangeable.

Useful first questions:

* is the DAG surprisingly large?
* are there many tiny jobs whose runtime is smaller than scheduling overhead?
* is the filesystem slow to reveal outputs?
* is one actual tool doing most of the work?

Without a cost model, “optimize the workflow” usually turns into unprincipled tinkering.

[Back to top](#top)

---

<a id="core2"></a>
## 5) Core 2 — Logs, Benchmarks, Summaries, and Drift Reports

Snakemake already gives you strong observability surfaces when you use them deliberately:

* per-rule logs
* `benchmark:` outputs
* `--summary`
* `--list-changes`
* dry-runs with printed commands

The point is not to collect everything. The point is to keep enough evidence to answer:

* what ran
* why it ran
* what changed
* where time or failure accumulated

Good observability is narrow, purposeful, and reviewable.

[Back to top](#top)

---

<a id="core3"></a>
## 6) Core 3 — Incident Triage for Slow or Flaky Workflows

Use a fixed incident ladder:

1. confirm the symptom
2. dry-run the same target set
3. inspect changed inputs, code, or params
4. inspect logs and benchmarks for the affected rules
5. decide whether the problem is workflow shape, operating context, or tool behavior

Common incident classes:

* dynamic discovery produced more work than expected
* too many tiny jobs overwhelmed the scheduler or filesystem
* retries masked a real deterministic failure
* a changed environment or helper script caused drift that looked like randomness
* publish verification passed locally but failed in a stricter context

[Back to top](#top)

---

<a id="core4"></a>
## 7) Core 4 — Tuning Without Hiding Truth

Allowed tuning moves:

* combine tiny tasks when the grouping remains truthful
* reduce redundant work in helper scripts or summary steps
* make scheduling or profile defaults more realistic
* improve staging discipline or file placement

Disallowed tuning moves:

* suppressing reruns by hiding a real dependency
* removing logs or benchmarks because they are inconvenient during review
* publishing fewer proofs so a run only appears faster
* changing profiles in ways that alter semantics but look like optimization

Fast wrong workflows are still wrong workflows.

[Back to top](#top)

---

<a id="core5"></a>
## 8) Core 5 — Operational Runbooks and Review Surfaces

A mature workflow should have a minimal runbook that answers:

* how to dry-run safely
* how to inspect what changed
* where logs and benchmarks live
* how to confirm the publish surface is still sane
* when to treat the issue as workflow design rather than executor friction

The runbook does not need to be long. It does need to exist somewhere a teammate can find
before an incident becomes folklore.

[Back to top](#top)

---

<a id="capstone"></a>
## 9) Capstone Sidebar

Use the capstone to inspect:

* `benchmarks/` and `logs/` as routine observability surfaces
* `Makefile` proof targets as operational shortcuts
* `tests/test_workflow_integration.py` as a signal that incidents can become executable checks
* the workflow tour bundle as a human-readable incident and review artifact

[Back to top](#top)

---

<a id="exercises"></a>
## 10) Exercises

1. Write a short incident note for one slow or surprising workflow run and back every claim with an artifact.
2. Add one benchmark or log surface that makes a recurring review question easier to answer.
3. Tune one workflow bottleneck without changing the publish contract or hiding a dependency.
4. Convert one recurrent operational issue into a repeatable check or proof target.

[Back to top](#top)

---

<a id="closing"></a>
## 11) Closing Criteria

You pass this module only if you can demonstrate:

* a cost model that distinguishes workflow overhead from tool runtime
* observability surfaces that answer real review or incident questions
* one documented incident ladder for slow or flaky runs
* one tuning change that improves feedback without weakening workflow truth

[Back to top](#top)
