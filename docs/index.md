# Deep Dive Series

The Deep Dive Series is the umbrella catalog for a growing set of
correctness-first courses. The repository keeps all course histories in one
place and organizes them by long-lived subject area so new courses can be
added without inventing a new repository shape each time.

## Course Families

### Reproducible Research

Build systems, workflow engines, and other tooling used to create reliable,
traceable, repeatable research and data-processing systems.

- `deep-dive-make`
- `deep-dive-snakemake`

### Python Programming

Language-centric courses focused on how to write Python systems with explicit
semantics, strong engineering contracts, and maintainable abstractions.

- `python-functional-programming`
- `python-meta-programming`

## Repository Layout

```text
courses/
  reproducible-research/
  python-programming/
```

## Working Locally

Build the series site:

```bash
make series-docs-build
```

Serve the series site locally:

```bash
make series-docs-serve
```

Work with a specific course:

```bash
make COURSE=reproducible-research/deep-dive-make course-help
make COURSE=python-programming/python-functional-programming test
```
