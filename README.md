# Bijux Courses — 3,000-Module Production Blueprint v1

This repository blueprint defines **30 non-negotiable computing and software-engineering programs**, each with:

- **Level I:** Modules 001–050 — rigorous undergraduate core;
- **Level II:** Modules 051–100 — graduate and professional depth;
- **100 canonical modules total**;
- **one future Markdown chapter per module**;
- **no lab files, capstone files, slide decks, or placeholder module files**.

The blueprint contains **3,000 unique module titles and future paths**. It does not claim that the teaching chapters already exist.

## Purpose

The curriculum is designed to:

1. consolidate years of practical and academic knowledge into a coherent mental model;
2. fill genuine gaps rather than add random tutorial material;
3. update every domain to current engineering practice;
4. connect theory, implementation, production behavior, failure, and trade-offs;
5. support repeated review and first-principles teaching;
6. provide professional depth sufficient to prepare for real work in each named domain.

“MIT/Stanford level” is used as a **rigor calibration**, not as a claim of equivalence, accreditation, or affiliation.

## Canonical completion rule

A program's Level I is complete only when its 50 real module files pass the module contract.

A program's Level II is complete only when Modules 051–100 also pass.

A roadmap row, empty file, generated outline, or title-only file never counts as a completed module.

## Package map

- `MASTER_SPEC.md` — governing specification
- `CANONICAL_30_PROGRAMS.md` — final roster and purpose
- `LEVEL_AND_MODULE_MODEL.md` — level, workload, and progression rules
- `PROGRAM_BOUNDARIES.md` — ownership and anti-duplication rules
- `DEPENDENCY_AND_SEQUENCE.md` — coherent study and production order
- `MODULE_CONTENT_CONTRACT.md` — exact future chapter contract
- `ROADMAP_QUALITY_GATES.md` — rejection and acceptance criteria
- `LEVEL_III_POLICY.md` — how future Levels III+ may be justified
- `SOURCE_CALIBRATION.md` — authoritative curriculum references
- `ALL_3000_MODULES.md` — combined table of contents
- `programs/*/ROADMAP.md` — one complete roadmap per program
- `manifests/modules.csv` and `.jsonl` — machine-readable plan
- `tools/validate_blueprint.py` — structural validator
- `Makefile` — repository validation entry points

## Validate

```bash
python3 tools/validate_blueprint.py
```

Generated: 2026-08-28
