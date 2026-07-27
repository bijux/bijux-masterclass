# Exercise Answers

Use this page after you have written your own answers. The point is comparison, not
copying.

## How to use the answer page well

Do not read a model answer first and then reshape your exercise to match it.

A better rhythm is:

1. finish the exercise with your own files and commands
2. write one plain-language explanation of the design
3. compare that explanation with the model answer
4. revise where the model answer exposes a missing boundary or proof route

The goal is not identical wording. The goal is reviewable reasoning about dynamic
workflow behavior.

The strongest Module 02 answers usually do four things:

- they name the discovery or integrity boundary directly
- they explain why the current shape is weak or strong
- they point to one evidence route
- they describe the repair in terms of reviewable artifacts, not workflow folklore

The strongest self-study packets also leave behind six concrete artifacts:

- one source-of-truth note
- one normalized registry or target list
- one fanout check
- one checkpoint-justification note
- one rejection or validation record
- one publication note for discovery artifacts

If your answers rely only on what Snakemake happened to do, the reasoning is still too
thin.

## Exercise 1: Compare two discovery surfaces

A strong answer compares the source of truth directly.

Example:

> In the sample-sheet version, `config/samples.tsv` is the declared source of truth, so
> version control records every membership change explicitly. In the directory-scan version,
> `data/raw/*.fastq.gz` is the source of truth, so the workflow must sort and normalize the
> scan result to make it trustworthy. A dry-run shows that both designs produce the same
> target list, but they differ in how that list is governed.

Why this is strong:

- it makes both discovery surfaces explicit
- it compares governance, not just convenience
- it keeps the target list as the shared proof route

## Exercise 2: Turn ambient discovery into a declared contract

A strong answer sounds like this:

> The weak version scanned `data/raw/` at parse time and expanded targets immediately, so
> the workflow had no durable record of what it discovered. The repair gives discovery one
> owned output such as `results/discovery/accepted_samples.json`, and when rejection is
> possible it keeps `results/discovery/rejected_samples.json` beside it. Downstream rules
> fan out from the accepted registry instead of trusting a transient directory scan.

Why this is strong:

- it names the old weakness clearly
- it adds owned discovery artifacts instead of vague "better organization"
- it explains why review got easier

The missing but important sentence is usually this one:

> Another reviewer can now inspect the recorded accepted and rejected sets directly instead
> of reverse-engineering a transient directory scan.

## Exercise 3: Prevent one accidental fanout explosion

A strong answer makes the multiplication visible.

Example answer shape:

- buggy design:
  - `expand("results/{sample}/{panel}/report.json", sample=SAMPLES, panel=PANELS)`
- unintended effect:
  - every sample is paired with every panel, even when the data model is one panel per
    sample
- repair:
  - build targets from validated records such as `{"sample": "sampleA", "panel": "dna"}`
- evidence:
  - `snakemake -n` shows four planned jobs before the repair and two after it

Why this is strong:

- it explains the wrong relationship, not just the wrong count
- it keeps one data source of truth for paired values

## Exercise 4: Design the integrity trail for a dynamic run

A strong answer gives three explicit paths and one explicit role for each:

- accepted registry:
  - `results/discovery/accepted_samples.json`
  - proves which validated candidates drove downstream work
- rejection record:
  - `results/discovery/rejected_samples.json`
  - proves which candidates were excluded and why
- provenance artifact:
  - `publish/v1/provenance.json`
  - proves the resolved run identity and materialized config
- manifest artifact:
  - `publish/v1/manifest.json`
  - proves which files belong to the public boundary

The strongest answers also mention published copies of the accepted and rejected discovery
artifacts, such as `publish/v1/accepted_samples.json` and
`publish/v1/rejected_samples.json`, because downstream review often needs the full
decision trail instead of only the final surviving set.

## Exercise 5: Improve performance without weakening truth

A strong answer sounds like this:

> The original workflow created one environment file per nearly identical Python rule and
> one trivial job per tiny fragment, so setup overhead dominated useful work. The repair
> reuses one shared Python environment for the related rules and batches work at the sample
> boundary. This lowers environment solve and launch cost without hiding required artifacts
> or changing the meaning of the publish boundary.

Why this is strong:

- it names the overhead source
- it repairs the boundary instead of deleting evidence
- it explicitly says why workflow truth stayed intact

## Exercise 6: Build a validated candidate registry

A strong loader reads `config/samples.tsv`, validates required columns, rejects blank or
duplicate identifiers, checks source existence, and sorts records by identifier. It then
derives both the source lookup and concrete output list from those records. A duplicate
sample should fail while the workflow is parsed, before any expensive job starts.

Static planning is sufficient because the manifest already contains every fact needed to
name the targets. A checkpoint would not discover new information; it would only defer
known information and make the graph harder to inspect.

The key explanatory sentence is:

> A checkpoint is wrong here because it hides a fact we already knew and could have
> validated before execution began.

## Exercise 7: Justify one checkpoint and reject one fake one

A strong answer contrasts the two designs directly.

Example:

- justified checkpoint:
  - the workflow cannot know which declared candidates are usable until a validator reads
    their contents
  - the checkpoint writes `results/discovery/accepted_samples.json` and
    `results/discovery/rejected_samples.json`
  - downstream targets read the accepted registry
- unjustified checkpoint:
  - the sample list already lives in config or a validated manifest
  - using a checkpoint would only hide a target list that was already known
  - the cleaner alternative is to expand directly from validated static data

Why this is strong:

- it shows that checkpoints are for genuine runtime facts
- it rejects the temptation to use checkpoints as a dramatic wrapper for weak modeling

## Exercise 8: Implement a justified checkpoint

The checkpoint should own one directory containing a deterministic accepted registry and
rejection record. Its downstream input function calls
`checkpoints.validate_candidates.get()`, reads the accepted identifiers, sorts them, and
expands concrete paths. Before completion the graph ends at validation; afterward
Snakemake reevaluates the input function and extends the graph.

The justification is not that files exist in a directory. It is that executing a
validator determines which candidates satisfy a semantic condition that planning could
not evaluate safely.

The strongest answer also says what the rejection record proves:

> It keeps excluded candidates visible, so the workflow explains both membership and
> non-membership instead of silently dropping bad inputs from the story.

## Exercise 9: Test discovery integrity under change

A strong result compares registry versions rather than relying on memory:

- adding a valid candidate adds one accepted record and one downstream target
- removing a candidate removes it from the next registry and target set
- corrupting a candidate moves it from accepted records to explicit rejection evidence

The workflow must define whether stale outputs from removed candidates are retained,
quarantined, or cleaned. Silently presenting them as current would make the publish
boundary dishonest.

## Exercise 10: Publish a reviewable dynamic result

The public bundle should contain accepted and rejected discovery records, result files,
resolved semantic configuration, provenance, and a checksummed manifest. A consumer can
verify checksums, read the manifest, and connect every result to an accepted identifier
without opening `results/` or `.snakemake/`.

Checkpoint directories and scheduler logs remain internal unless they are deliberately
part of the support contract. The accepted registry becomes public because it explains
why the result set has exactly its observed membership.

The strongest answers also say explicitly which discovery surfaces stay internal, such as
checkpoint working directories or engine metadata, so the publish contract stays small
and reviewable.

## What all ten answers should have in common

The best Module 02 answers usually:

1. explain dynamic behavior without mystical language
2. identify one artifact or boundary that carries the truth
3. point to a concrete proof route such as `snakemake -n`, accepted and rejected discovery records, or a publish manifest
4. describe repairs as stronger contracts, not just shorter code

If your answers do those four things, you are learning the module in the right direction.

Weak answer pattern:

- "Snakemake will figure out the dynamic part for us"

That sentence skips the discovery artifact, the validation boundary, and the public
review surface all at once. If your answers still sound like that, keep revising.
