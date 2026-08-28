# Validation Report

Generated: 2026-08-28

## Structural result

```text
PASS
Programs: 30
Blocks: 300
Modules: 3,000
Modules per program: 100
Level-I modules per program: 50
Level-II modules per program: 50
Unique module IDs: 3,000
Unique module titles: 3,000
Unique future paths: 3,000
Placeholder module files: 0
Capstone or lab roadmap rows: 0
Banned filler-title findings: 0
```

## Additional checks

- Every program contains ten blocks of ten modules.
- Numbering is continuous from 001 through 100.
- Every program has an explicit purpose, prerequisite set, ownership boundary, exclusion boundary, and professional outcome.
- Every future path is deterministic and unique.
- No module directory or empty module file has been generated.
- Roadmap titles agree with the machine-readable manifest.
- Exact duplicate module titles were removed by making each program's perspective explicit.
- Level III is reserved rather than padded speculatively.
- All thirty program roadmaps are present.

## What this report does not prove

Structural validation does not prove that a future chapter is:

- technically correct;
- pedagogically excellent;
- current;
- sufficient for self-study;
- comparable in rigor to a particular university subject;
- professionally effective.

Those claims require authoring, teaching, review, exercises, code execution, and external evaluation.

## Semantic correction applied during repository acceptance

The accepted package assigned both `SEME-082` and `SARCH-071` to architectural
drift and erosion even though the Methods & Evolution boundary explicitly excludes
architecture ownership. `SEME-082` is therefore scoped to **Socio-Technical Causes
of Architectural Erosion**, which owns the lifecycle, organizational, and process
forces behind structural decay. `SARCH-071` retains ownership of architectural
drift and erosion as an architecture evaluation and governance concern.

The correction affects the Methods & Evolution roadmap, combined index, and both
module manifests. No module number, level, block, or program boundary changed.

## Reproduce

```bash
python3 tools/validate_blueprint.py
```
