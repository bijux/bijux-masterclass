# Bijux Masterclass

<section class="bijux-hero">
  <div class="bijux-hero__eyebrow">Catalog Handbook</div>
  <h1 class="bijux-hero__title">Choose the right program family before you choose the course.</h1>
  <p class="bijux-hero__lede">Bijux Masterclass is the root catalog for the full program collection. Start here when you need to choose a family first, then narrow down to the course that matches the real design or reproducibility pressure in front of you.</p>
  <div class="bijux-topic-row">
    <span class="bijux-topic-pill">Python design</span>
    <span class="bijux-topic-pill">Workflow truth</span>
    <span class="bijux-topic-pill">Reproducible systems</span>
    <span class="bijux-topic-pill">Long-form courses</span>
  </div>
</section>

<div class="bijux-callout"><strong>The catalog should route by pressure, not by tool branding.</strong> Use the family pages to decide which system model you need first. Drop into one course only after the boundary is clear enough that the course home is the honest next page.</div>

<div class="bijux-panel-grid">
  <div class="bijux-panel"><h3>Python Programming</h3><p>Open this family when the pressure is about object boundaries, functional composition, runtime hooks, or long-lived API behavior.</p></div>
  <div class="bijux-panel"><h3>Reproducible Research</h3><p>Open this family when the pressure is about build graphs, workflow orchestration, state identity, publication, and recoverable change.</p></div>
  <div class="bijux-panel"><h3>Stable Routing</h3><p>Use the root catalog to compare families first, then use family pages to choose one course home with the right learner entry and capstone route.</p></div>
</div>

<div class="bijux-quicklinks">
  <a class="md-button md-button--primary" href="python-programming/README.md">Open Python Programming</a>
  <a class="md-button" href="reproducible-research/README.md">Open Reproducible Research</a>
</div>

This README is the maintained source for the root catalog page, and the family
README files under `programs/` are the maintained source for the family landing pages.

## Catalog Maps

```mermaid
graph TD
  home["Bijux Masterclass"]
  home --> python["Python Programming"]
  home --> research["Reproducible Research"]
  python --> oop["python-object-oriented-programming/"]
  python --> fp["python-functional-programming/"]
  python --> meta["python-meta-programming/"]
  research --> make["deep-dive-make/"]
  research --> snakemake["deep-dive-snakemake/"]
  research --> dvc["deep-dive-dvc/"]
```

```mermaid
flowchart LR
  home["Choose a family"] --> family["Read the family index"]
  family --> program["Open one course home"]
  program --> course["Enter the ordered course tree"]
  course --> capstone["Cross-check the capstone guide when needed"]
  capstone --> review["Return to the catalog when switching programs"]
```

## How to Use This Catalog

| If you need to choose... | Open |
| --- | --- |
| the right program family | [Python Programming](python-programming/README.md) or [Reproducible Research](reproducible-research/README.md) |
| a specific course inside Python work | [Python Programming](python-programming/README.md) |
| a specific course inside reproducibility and workflow work | [Reproducible Research](reproducible-research/README.md) |

Use the family indexes when you know the problem space but not the exact course yet.
Use a course home when you already know which program you want. Return here when you
need to compare families before switching.

## Program Families

<div class="bijux-panel-grid">
  <div class="bijux-panel">
    <h3><a href="python-programming/README.md">Python Programming</a></h3>
    <p>Use this family when the pressure is about Python design itself: object boundaries, functional flow, runtime hooks, long-lived semantics, and reviewable code structure.</p>
    <ul>
      <li><a href="python-programming/python-object-oriented-programming/course-book/index.md">Python Object-Oriented Programming</a></li>
      <li><a href="python-programming/python-functional-programming/course-book/index.md">Python Functional Programming</a></li>
      <li><a href="python-programming/python-meta-programming/course-book/index.md">Python Metaprogramming</a></li>
    </ul>
  </div>
  <div class="bijux-panel">
    <h3><a href="reproducible-research/README.md">Reproducible Research</a></h3>
    <p>Use this family when the pressure is about build graphs, workflow orchestration, data state, reproducibility, publication, and recovery under change.</p>
    <ul>
      <li><a href="reproducible-research/deep-dive-make/course-book/index.md">Deep Dive Make</a></li>
      <li><a href="reproducible-research/deep-dive-snakemake/course-book/index.md">Deep Dive Snakemake</a></li>
      <li><a href="reproducible-research/deep-dive-dvc/course-book/index.md">Deep Dive DVC</a></li>
    </ul>
  </div>
</div>

## Local Commands

```bash
make docs-serve
make docs-audit
make PROGRAM=python-programming/python-functional-programming docs-serve
make PROGRAM=reproducible-research/deep-dive-make test
```

If port `8000` is already busy, the docs server automatically moves to the next open
local port. Set `DOCS_PORT=<port>` when you want a different starting port.

## Honesty Boundary

The root catalog is a synchronized mirror of the checked-in course and capstone
Markdown. It is not a separate editorial fork. When a course or family route changes in
`programs/`, the root docs build should publish that same source rather than a second
hand-maintained version.

## Maintenance Contract

- Update this file when a family is added, removed, renamed, or rerouted.
- Update the owning family `README.md` when a program is added, removed, renamed, or rerouted.
- Keep links pointed at the real learner entry pages for each program.
- Treat these README files as catalog documents, not scratch notes: they should stay
  stable, direct, and clear enough for someone returning much later.
