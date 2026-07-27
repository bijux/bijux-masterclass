# Exercise Answers

These answers are model explanations, not the only acceptable wording.

What matters is whether the reasoning protects downstream trust.

## How to use the answer page well

Do not read a model answer before you have tried the exercise yourself.

A stronger rhythm is:

1. complete the exercise with your own tree, manifest, consumer, or review note
2. write one plain-language explanation of the contract you are defending
3. compare that explanation with the model answer
4. revise where the model answer reveals missing artifact roles, weak evidence, or a
   downstream assumption you did not notice

The target is not identical wording. The target is durable downstream reasoning.

The strongest self-study packets also leave behind six concrete artifacts:

- one artifact-role table
- one public-tree sketch
- one manifest verification transcript
- one consumer test transcript
- one compatibility note
- one downstream-review note

If your answers rely only on the fact that files now sit under `publish/`, the reasoning
is still too thin.

## Exercise 1: Classify the current outputs

What should remain internal:

- `results/sample-a/qc.json`
- `results/sample-a/trim.json`
- `results/sample-b/qc.json`
- `logs/summarize.log`

Why:

These files support workflow execution, detailed inspection, or debugging. They are not
yet a stable downstream-facing surface.

What could belong in the published contract:

- `publish/v1/summary.tsv`
- `publish/v1/report/index.html`

What is still missing:

- a versioned publish boundary such as `publish/v1/`
- a manifest and checksums
- provenance
- a clear explanation of artifact roles and stability

The main lesson is that copying a few files into `publish/` is not enough by itself.

Weak answers say only "this file is useful" without naming whether it is internal,
diagnostic, machine-facing, or human-facing.

## Exercise 2: Draw the first publish boundary

A strong answer promotes only the smallest honest set of downstream-facing files into
`publish/v1/` and keeps per-sample workflow-operational detail, logs, and other debugging
surfaces internal. Each included file should have a one-sentence role explanation such as
"machine-facing summary," "human-facing report," or "integrity inventory." The quality
signal is not how many files move; it is whether a downstream user can rely on the public
bundle without learning the internal workflow tree.

The missing but important sentence is usually this one:

> This bundle is for a downstream reader or program that needs the published summary,
> report, and integrity surfaces, not the producer’s intermediate workflow state.

Weak answers celebrate a larger publish tree without proving why every added file belongs
to the contract.

## Exercise 3: Separate machine and human surfaces

A strong answer names one structured artifact such as `summary.json` or `summary.tsv` as
authoritative for programmatic use and one report artifact such as `report/index.html` as
authoritative for human inspection. The relationship should be explicit: the report is
derived from or aligned with the structured summary, not a separate truth. Scraping the
report weakens the contract because presentation markup is less stable than a documented
machine-facing schema.

Weak answers call both artifacts "the output" and therefore hide which one a consumer
should trust first.

## Exercise 4: Write a manifest for the bundle

A good manifest uses stable relative paths from the bundle root, deterministic ordering,
and digests such as SHA-256. The ordering rule should be simple and reproducible, for
example sorted normalized relative paths. Absolute paths do not belong because the bundle
contract must travel across machines and directories without changing meaning. A useful
verification transcript shows both a successful pass and the exact command used.

Example answer shape:

- manifest rows:
  - `sha256<TAB>relative/path`
- ordering:
  - lexicographic order on normalized relative bundle paths
- verification:
  - one command that rehashes the bundle and compares against the manifest
- explanation:
  - "relative paths keep the contract portable; absolute paths would change when the
    bundle moves even if the bundle meaning does not"

The key explanatory sentence is:

> The manifest proves that the inventoried bytes are the same bundle; it does not prove
> that the bundle is scientifically correct or semantically compatible with every consumer.

## Exercise 5: Add provenance without confusing its role

A strong provenance file records the producing repository revision, workflow identity,
runtime or environment context, and relevant configuration details that affect meaning.
It answers questions such as "what software context produced this bundle?" It does not by
itself answer "which published files are part of the public promise?" or "what should a
consumer read first?" Those remain contract questions.

Weak answers ask provenance to replace the manifest, consumer contract, and file API all
at once.

## Exercise 6: Write a consumer test

A strong consumer accepts only the bundle path, validates the documented machine-facing
artifact, and intentionally knows nothing about `results/`, internal rule names, or
producer-only configuration. The success condition is that the consumer can do useful
work with no hidden repository knowledge. That is the proof that the public contract is
real and not just a copied folder.

Example answer shape:

- input:
  - only `publish/v1/`
- first file read:
  - one documented machine-facing summary
- validation:
  - schema or required-column check
- deliberate ignorance:
  - no `results/` reads, no repository-root assumptions, no producer-only helper imports

Why this is strong:

- it proves the bundle is self-contained enough for downstream use
- it forces the machine-facing surface to behave like a real API

The deliberate boundary sentence is:

> Reading `results/` would weaken the contract because it asks the consumer to depend on
> producer-only workflow layout that the public bundle was meant to hide.

## Exercise 7: Corrupt the bundle and detect it

The failed verification should identify the changed path and report a checksum mismatch or
equivalent integrity failure. What this proves is file identity: the bytes are no longer
the same as the inventoried bundle. What it does not prove is semantic correctness,
scientific validity, or whether the bundle was the right contract to publish in the first
place.

Weak answers claim checksum failure proves the scientific result is wrong. It only proves
the published bytes no longer match the inventoried bundle.

## Exercise 8: Simulate a downstream compatibility check

Likely compatible within `v1`:

- adding a new optional field to `summary.json`

Likely versioning discussion:

- renaming the file to `published-summary.json`
- removing an existing field that consumers may rely on

Why:

An additive field can preserve the old contract if existing consumers still work. Path
changes and field removals often alter the public promise directly.

The strongest answers also write one sentence from the consumer’s point of view, such as:

> My existing parser still succeeds without modification, so this additive field is
> compatible within `v1`; a renamed path would not be.

Weak answers classify compatibility from the producer's convenience instead of from the
surviving consumer's experience.

## Exercise 9: Design a deliberate version migration

`v1` should remain intact for supported consumers while `v2` introduces the breaking
change under a new public boundary. A good migration note maps old paths or fields to the
new ones, states who should move and when, and keeps separate consumer tests for both
supported versions. The internal workflow tree still does not belong in either API,
because versioning is about the public promise, not about exposing producer internals.

Example migration note elements:

- what changed in `v2`
- which `v1` consumers are still supported and for how long
- how one old path or field maps to the new surface
- which verification route should be run for each supported version

## Exercise 10: Review a full publish change like a downstream maintainer

A strong review starts with findings ordered by downstream trust impact: hidden dependency
on `results/`, renamed public path, mismatched manifest coverage, changed artifact role,
or unclear consumer surface. Each correction should name the narrowest verification route
that proves the repair, such as rerunning the bundle verifier, rerunning the consumer
test, or diffing the published role table. One appropriate outcome is to say a change
should be versioned, postponed, or removed rather than merged under the current contract.

A useful review order often looks like this:

1. check whether the public artifact roles still tell the truth
2. verify that the consumer still reads only documented bundle surfaces
3. inspect whether manifest and provenance still match their intended jobs
4. classify whether any changed path or field remains compatible inside the current version

Weak reviews start with low-value style notes before naming contract breakage or
verification gaps.

## Self-check

If your answers consistently explain:

- what is internal versus public
- what changed in the contract
- which artifact carries which responsibility
- what evidence supports downstream trust

then you are using the module correctly.

Weak answer pattern:

- "the bundle is better now because it has more files and more metadata"

That sentence skips the consumer surface, the artifact roles, and the compatibility
question all at once. If your answers still sound like that, keep revising.
