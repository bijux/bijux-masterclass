<a id="top"></a>

# Module 09 — Promotion, Registry Boundaries, Release Contracts, and Auditability

Recoverable state is not automatically trusted state. A DVC repository becomes far more
useful when a team can answer which artifacts are experimental, which are baseline, which
are promoted for downstream use, and which pieces of evidence must travel with a release
so another person can review or restore it later.

This module is about the point where state management becomes product management:
promotion rules, release contracts, registry-style boundaries, audit evidence, and the
difference between "we have the files" and "we can defend this exact state."

### Before You Begin

This module works best after Modules 01-08, especially the parts on truthful pipelines,
metrics, experiments, collaboration, and recovery.

Use this module if you need to learn how to:

* distinguish exploratory state from promoted state
* define a stable release or publish contract around DVC-managed artifacts
* decide which metadata, metrics, and manifests are necessary for auditability

Proof loop for this module:

```bash
dvc status
dvc metrics diff
make -C capstone verify
```

Capstone corroboration:

* inspect `capstone/publish/v1/`
* inspect `capstone/params.yaml`
* inspect `capstone/dvc.lock`
* inspect `capstone/TOUR.md`

---

<a id="toc"></a>
## 1) Table of Contents

1. [Table of Contents](#toc)
2. [Learning Outcomes](#outcomes)
3. [How to Use This Module](#usage)
4. [Core 1 — Promotion Is a Contract, Not a Copy Step](#core1)
5. [Core 2 — Stable Release Surfaces and Registry Boundaries](#core2)
6. [Core 3 — Audit Evidence: Params, Metrics, Locks, and Manifests](#core3)
7. [Core 4 — Reviewable Promotion Workflows](#core4)
8. [Core 5 — Failure Modes in State Promotion](#core5)
9. [Capstone Sidebar](#capstone)
10. [Exercises](#exercises)
11. [Closing Criteria](#closing)

---

<a id="outcomes"></a>
## 2) Learning Outcomes

By the end of this module, you can:

* distinguish experimental state, baseline state, and promoted state clearly
* define a stable release boundary around DVC-managed outputs
* decide which params, metrics, manifests, and lock evidence must accompany a promoted result
* design a reviewable promotion workflow that survives handoff and audit pressure
* spot promotion shortcuts that make downstream trust impossible

[Back to top](#top)

---

<a id="usage"></a>
## 3) How to Use This Module

Set up a repository with these surfaces:

```text
lab/
  dvc.yaml
  dvc.lock
  params.yaml
  metrics/
  publish/
    v1/
```

Then force yourself to name three categories of state:

1. experimental outputs that are useful for exploration but not yet trustworthy downstream
2. baseline outputs that remain comparable over time
3. promoted outputs that downstream users are allowed to depend on

The teaching goal is not just to "publish files." It is to make the learner say exactly
why one state is trusted more than another.

[Back to top](#top)

---

<a id="core1"></a>
## 4) Core 1 — Promotion Is a Contract, Not a Copy Step

Promotion should answer a question such as:

* which model or report is now approved for downstream use?
* which params and metrics define that promoted result?
* which state is still exploratory and must not leak into a release boundary?

If promotion is treated as "copy the latest files somewhere stable," then the repository
is quietly delegating trust to human memory.

Good promotion discipline:

* a stable publish directory or release boundary
* explicit params and metrics that explain what was promoted
* a lockfile or equivalent state record tied to that promotion
* a clear rule for when a new version is warranted

[Back to top](#top)

---

<a id="core2"></a>
## 5) Core 2 — Stable Release Surfaces and Registry Boundaries

A release surface should stay small and durable enough that downstream users do not have
to know the internal repository layout.

Examples of a useful release surface:

* a versioned `publish/v1/` directory
* a manifest naming the promoted files
* a report that explains the run in human terms
* parameters and metrics captured in their promoted form

The key distinction:

* internal pipeline state helps the system operate
* promoted state helps another person trust, consume, or review the result

Those are related, but they are not interchangeable.

[Back to top](#top)

---

<a id="core3"></a>
## 6) Core 3 — Audit Evidence: Params, Metrics, Locks, and Manifests

Auditability depends on enough evidence to answer:

* what exactly was run?
* which inputs and params mattered?
* what metrics were observed?
* which files form the promoted result?

Four surfaces matter especially in DVC:

| Surface | Why it matters |
| --- | --- |
| `params.yaml` | shows the declared control surface |
| metrics | makes comparisons reviewable |
| `dvc.lock` | records the executed state graph |
| publish manifest | tells a consumer what the release contains |

If one of those is missing, a promotion can still happen. It just becomes much harder to
defend later.

[Back to top](#top)

---

<a id="core4"></a>
## 7) Core 4 — Reviewable Promotion Workflows

A strong promotion workflow should be reviewable by another engineer who was not present
for the experiment cycle.

That review should be able to answer:

* what changed from baseline?
* why is this promoted state better or more appropriate?
* which artifact bundle is now the contract?
* how would a future recovery drill restore this exact result?

Useful practice:

* promote from an explicit baseline or experiment comparison
* require verification before promotion
* keep published artifacts stable enough for consumers and audits
* document the downstream contract where a reviewer will actually see it

[Back to top](#top)

---

<a id="core5"></a>
## 8) Core 5 — Failure Modes in State Promotion

Practice identifying these failures:

* the promoted report no longer matches the promoted params
* metrics are diffed, but the compared runs are not semantically comparable
* a release bundle exists, but the lock state needed to explain it is unclear
* baseline and experiment outputs are mixed into one publish directory
* a consumer depends on internal pipeline paths because the release surface is vague

Promotion failures are dangerous because they often look neat from the outside. The
directory exists, the report renders, and the metrics are present. The problem is that
the repository can no longer explain why that state deserves trust.

[Back to top](#top)

---

<a id="capstone"></a>
## 9) Capstone Sidebar

Use the capstone to inspect:

* `publish/v1/` as the stable promoted surface
* `params.yaml` and `metrics/metrics.json` as the semantic comparison surfaces
* `dvc.lock` as evidence of the executed state graph
* `TOUR.md` and the tour bundle as review artifacts for promoted state

[Back to top](#top)

---

<a id="exercises"></a>
## 10) Exercises

1. Define a stable publish boundary for one DVC repository and explain which internal paths are excluded.
2. Promote one experimental result and write down exactly which params, metrics, and lock evidence justify it.
3. Create a manifest for a promoted bundle and explain how a downstream user should validate it.
4. Review a repository promotion story and list the top three reasons it would fail under audit.

[Back to top](#top)

---

<a id="closing"></a>
## 11) Closing Criteria

You pass this module only if you can demonstrate:

* a clear distinction between exploratory state and promoted state
* a stable release surface another consumer can trust
* enough params, metrics, and lock evidence to defend a promoted result
* a promotion flow that another reviewer can understand without private context

[Back to top](#top)
