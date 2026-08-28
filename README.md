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
- `tools/validate_blueprint.py` — corpus and roadmap structural validator
- `tools/validate_module.py` — focused chapter-contract validator
- `tools/verify_snippets.py` — safe extraction and executable-snippet evidence
- `tools/create_review_record.py` — incomplete source, mathematics, and review record
- `tools/validate_review.py` — focused review-evidence validator
- `tools/complete_module.py` — guarded chapter and manifest completion transition
- `Makefile` — repository validation entry points

## Validate

```bash
make validate
python3 tools/verify_snippets.py PLS-001
python3 tools/create_review_record.py PLS-001
python3 tools/validate_review.py PLS-001
python3 tools/validate_module.py PLS-001 --allow-draft
python3 tools/complete_module.py PLS-001
python3 tools/validate_module.py PLS-001
```

The draft command checks a real chapter, its annotated snippets, and its completed
review record while its manifest row remains `planned`. The completion command
requires the chapter and both module manifests to agree on `complete`. Structural
and executable validation reject contract, synchronization, safety, and
observed-behavior defects; the review record covers the broader technical,
mathematical, citation, and pedagogical judgments that automation cannot prove.

The completion command first validates the planned draft, snippets, and review
record, then changes only its front-matter status and its matching CSV and JSONL
status fields. It reruns blueprint, chapter, snippet, and review validation and
restores the three files if a post-transition check fails. The chapter and both
manifests belong in the same module commit.

Review records live under `artifacts/reviews/<MODULE_ID>/`. The generated template
is intentionally incomplete. It becomes valid only after source checking, every
mathematics category, conceptual review, practitioner review, and pedagogical
review have an explicit outcome and substantive notes bound to the chapter
digest. These are internal checks and never constitute external peer review.

Generated: 2026-08-28
