# Deep Dive Series

This repository is the permanent home for the Deep Dive course collection.
Each course keeps its own full git history while living inside one repository,
so new courses can be added without duplicating repo-level setup.

## Repository Layout

```text
.
├── courses/
│   ├── deep-dive-make/
│   ├── deep-dive-snakemake/
│   ├── python-functional-programming/
│   └── python-meta-programming/
├── Makefile
└── README.md
```

## Included Courses

- `deep-dive-make`
- `deep-dive-snakemake`
- `python-functional-programming`
- `python-meta-programming`

## Working With Courses

List the available courses:

```bash
make courses
```

Run a common target against a selected course:

```bash
make COURSE=deep-dive-make docs-build
make COURSE=python-functional-programming test
```

Show a course's own Make targets:

```bash
make COURSE=deep-dive-snakemake course-help
```
