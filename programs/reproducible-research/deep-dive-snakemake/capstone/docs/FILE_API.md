# File API (publish/v1)


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
  guide["Capstone docs"]
  section["FILE_API"]
  page["File API (publish/v1)"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  orient["Read the guide boundary"] --> inspect["Inspect the named files, targets, or artifacts"]
  inspect --> run["Run the confirm, demo, selftest, or proof command"]
  run --> compare["Compare output with the stated contract"]
  compare --> review["Return to the course claim with evidence"]
```
<!-- page-maps:end -->

This capstone exports a small, versioned set of artifacts under `publish/v1/`.
All JSON files:

* are UTF-8
* end with a newline
* are deterministic (sorted keys where applicable)
* include `schema_version` for forward-compatible evolution

The per-sample intermediate files live under `results/{sample}/` and are
documented here as well because they form the workflow contracts.

Use `PUBLISH_REVIEW_GUIDE.md` when the question is not just what the files are, but why
they deserve downstream trust.

## Results per sample (`results/{sample}/`)

### `qc_raw.json` / `qc_trimmed.json`

Produced by: `python -m capstone.qc_fastq`

Minimal fields:

* `schema_version` (int)
* `path` (str)
* `reads` (int)
* `bases` (int)
* `mean_read_length` (float)
* `gc_fraction` (float)
* `n_fraction` (float)
* `qual_mean_per_pos` (list[float])
* `length_hist` (dict[int,int])

### `trim.json`

Produced by: `python -m capstone.trim_fastq`

* `schema_version`
* `input`: `{path, reads, bases}`
* `output`: `{path, reads, bases}`
* `params`: trimming parameters used for the run
* `clipping`: nested counts for adapter, quality, and poly-run clipping

### `dedup.json`

Produced by: `python -m capstone.dedup_fastq`

* `schema_version`
* `mode` (`dedup` or `copy`)
* `input`: `{path, reads, bases}`
* `output`: `{path, reads, bases}`
* `dedup_key`
* `duplicates_dropped`

### `kmer.json`

Produced by: `python -m capstone.kmer_profile`

* `schema_version`
* `input`
* `k`
* `signature_size`
* `unique_kmers`
* `total_kmers`
* `signature` (list[int])
* `top_kmers` (list[{kmer,count}])

### `screen.json`

Produced by: `python -m capstone.screen_panel`

* `schema_version`
* `sample_kmer_json`
* `panel_fasta`
* `k`
* `signature_size`
* `score_type`
* `scores` (sorted list of panel hits)

## Published API (`publish/v1/`)

### `discovered_samples.json`

Produced by the checkpoint `discover_samples`.

* `schema_version`
* `allow_paired_end`
* `raw_dir`, `glob`, `n_files`
* `samples` mapping: `{sample: {mode: SE|PE, reads: {SE|R1|R2: path}}}`

### `summary.json` and `summary.tsv`

Produced by: `python -m capstone.summarize`

* `schema_version`
* `units`: `{sample: {...}}` (merged metrics from all upstream steps)
* each unit includes `raw_qc`, `trim`, `trimmed_qc`, `dedup`, `kmer`, `screen`, and `highlights`

### `report/index.html`

Produced by: `python -m capstone.report`

Static HTML report (no external JS/CSS).

### `provenance.json`

Produced by rule `provenance`.

Records:

* `timestamp_utc`
* `python_version`, `python_executable`, `platform`
* `snakemake_version`
* `git_commit` (if available)
* the fully materialized config

### `manifest.json`

Produced by: `python -m capstone.manifest`

* `schema_version`
* `base`: absolute directory used to relativize published paths
* `files`: ordered list of `{path, sha256}` records

Use `RESULTS_BOUNDARY_GUIDE.md` when the question is whether a surface belongs under
`results/` as an internal contract or under `publish/v1/` as a downstream-facing one.
