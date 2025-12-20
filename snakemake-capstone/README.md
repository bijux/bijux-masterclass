# Snakemake Capstone — Reference Workflow

A compact, end-to-end Snakemake workflow that demonstrates rigorous engineering practices on toy FASTQ inputs. The biological analysis is intentionally minimal; the emphasis is on workflow correctness, reproducibility, and maintainability: explicit contracts, safe dynamic DAGs, governed configuration, versioned publishing, artifact verification, and execution across contexts (local, CI, cluster, Docker).

This project is designed to be **executed**, **studied**, and **extended** as a reference implementation.

[![CI](https://github.com/bijux/deep-dive-snakemake/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/bijux/deep-dive-snakemake/actions/workflows/ci.yml?query=branch%3Amain)
[![Snakemake](https://img.shields.io/badge/Snakemake-8.0%2B-blue?style=flat-square)](https://snakemake.readthedocs.io/en/stable/)
[![License](https://img.shields.io/github/license/bijux/deep-dive-snakemake?style=flat-square)](https://github.com/bijux/deep-dive-snakemake/blob/main/LICENSE)
[![Course Book](https://img.shields.io/badge/docs-course_book-blue?style=flat-square)](https://bijux.github.io/deep-dive-snakemake/)

> The CI workflow executes full confirmation runs, including workflow execution and artifact validation.

[Back to top](#top)

---

## Purpose

This capstone provides a practical reference for constructing Snakemake workflows that remain reliable at scale. It addresses common failure modes—implicit dependencies, unsafe dynamic behavior, partial outputs, configuration drift, and reproducibility gaps—through disciplined patterns:

- Early and explicit failure detection
- Clear input/output contracts and deterministic paths
- Safe handling of dynamic DAGs via checkpoints
- Strict configuration validation and modular composition
- Versioned, integrity-checked publishing
- Comprehensive testing and verification gates

The workflow is deliberately small yet complete, allowing full execution and inspection on any machine.

[Back to top](#top)

---

## Key Concepts Demonstrated

### Workflow Design
- Explicit rule contracts with stable filenames and directories
- Protected and temporary outputs to prevent partial artifacts
- Safe dynamic DAGs using checkpoints and proper re-evaluation
- Scatter/gather patterns for per-sample and run-level processing
- Modular rule organization with namespacing
- Clear separation of internal intermediates (`results/`) and published deliverables (`publish/vN/`)

### Operational Practices
- Execution profiles for environment-specific settings
- Structured, per-rule logging and benchmarking
- Resource declarations with resolved-value traceability
- Docker execution surface for consistent runtime

### Quality Assurance
- Schema-validated configuration as a required step
- Unit tests for pure Python components
- Artifact verification (parsing and sanity checks)
- Clean-room confirmation via Make targets

[Back to top](#top)

---

## Pipeline Overview

### High-Level Stages

1. **Sample Discovery** (checkpoint)  
   Scans `data/raw/` for FASTQ files and produces a sample registry.

2. **Per-Sample Processing**  
   - Raw FASTQ quality control  
   - Adapter trimming  
   - Trimmed quality control  
   - Deduplication  
   - k-mer profiling  
   - Reference panel screening  

3. **Run-Level Aggregation**  
   - Consolidation of per-sample results into summary tables  
   - HTML report generation  

4. **Publishing**  
   - Emission of versioned outputs to `publish/v1/`  
   - Generation of a checksummed manifest for integrity verification  

[Back to top](#top)

---

## Published Artifacts (Stable Interface)

Published outputs reside in `publish/v1/` and form a stable, externally consumable contract:

- `discovered_samples.json`
- `provenance.json`
- `summary.json` and `summary.tsv`
- `report/index.html`
- `manifest.json` (inventory with SHA-256 checksums)

Detailed specifications are provided in `FILE_API.md`.

Internal directories (`results/`, `logs/`, `benchmarks/`, `.snakemake/`) are not part of the stable interface.

[Back to top](#top)

---

## Repository Layout

```text
.
├── Snakefile                  # Top-level orchestration and targets
├── workflow/                  # Rule modules and publishing logic
├── src/                       # Python package for workflow steps
├── tests/                     # Unit tests for Python components
├── config/                    # config.yaml + schema.yaml
├── profiles/                  # Execution profiles (local, CI, cluster patterns)
├── data/                      # Toy inputs (FASTQs, reference panel)
├── FILE_API.md                # Published artifact contract
└── Makefile                   # Quality gates and entrypoints
```

Runtime-generated:
- `results/`, `logs/`, `benchmarks/`, `publish/`, `.snakemake/`

[Back to top](#top)

---

## Requirements

**Host execution**
- Python 3.11+
- Snakemake (system or virtual environment)

**Docker execution**
- Docker daemon available  
  (Designed to eliminate host Conda dependencies)

[Back to top](#top)

---

## Quick Start

### Full Clean-Room Execution with Verification
```bash
make clean verify
```

Executes the workflow from scratch and validates published artifacts (parsing, sanity, manifest integrity).

### Dry-Run Preview
```bash
make wf-dryrun
```

Displays planned jobs and commands without execution.

[Back to top](#top)

---

## Execution via Profiles

Profiles separate workflow logic from execution context.

```bash
snakemake --profile profiles/local --cores all --configfile config/config.yaml
```

Add `-p` to print commands as they would be executed.

**Note on Checkpoints**: The sample discovery checkpoint triggers DAG re-evaluation—an expected and intentional behavior visible in dry-runs.

[Back to top](#top)

---

## Makefile Targets (Primary Interface)

| Category       | Target                  | Purpose                                                                 |
|----------------|-------------------------|-------------------------------------------------------------------------|
| Cleanup        | `make clean`            | Remove all generated state and outputs                                  |
| Formatting     | `make fmt`, `make fmt-check` | Format and validate code formatting                                |
| Linting        | `make lint`, `make check` | Static analysis and composite checks                                  |
| Testing        | `make test`, `make ci`  | Unit tests and CI-style gate                                            |
| Workflow       | `make wf-lint`          | Snakemake lint                                                          |
|                | `make wf-dryrun`        | Preview execution plan                                                  |
|                | `make run`              | Execute workflow                                                        |
|                | `make dag` / `make rulegraph` | Generate visualizations                                      |
| Validation     | `make validate-config`  | Schema validation                                                       |
|                | `make verify-artifacts` | Parse and sanity-check published outputs                                |
|                | `make verify`           | Full run + artifact verification                                        |
|                | `make confirm`          | Strongest gate: clean + checks + tests + lint + dry-run + run + verify  |
| Docker         | `make docker-build`     | Build container image                                                   |
|                | `make docker-run`       | Execute workflow in container                                           |

**Recommendation**: Use `make confirm` for confidence before commits or releases.

[Back to top](#top)

---

## Extending the Workflow

Preserve these invariants when adding functionality:

- Deterministic outputs for identical inputs and configuration
- Explicit input/output declarations
- Temporary writes moved atomically
- Stable publish boundary (`publish/vN/`)
- Validation coverage for new artifacts

To modify the published contract, increment the version directory (e.g., `v2`) and update `FILE_API.md`.

[Back to top](#top)

---

## License

MIT — see the top-level [LICENSE](https://github.com/bijux/deep-dive-snakemake/blob/main/LICENSE). © 2025 Bijan Mousavi.

[Back to top](#top)