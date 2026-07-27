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

## Exercise 2: Draw the first publish boundary

A strong answer promotes only the smallest honest set of downstream-facing files into
`publish/v1/` and keeps per-sample workflow-operational detail, logs, and other debugging
surfaces internal. Each included file should have a one-sentence role explanation such as
"machine-facing summary," "human-facing report," or "integrity inventory." The quality
signal is not how many files move; it is whether a downstream user can rely on the public
bundle without learning the internal workflow tree.

## Exercise 3: Separate machine and human surfaces

A strong answer names one structured artifact such as `summary.json` or `summary.tsv` as
authoritative for programmatic use and one report artifact such as `report/index.html` as
authoritative for human inspection. The relationship should be explicit: the report is
derived from or aligned with the structured summary, not a separate truth. Scraping the
report weakens the contract because presentation markup is less stable than a documented
machine-facing schema.

## Exercise 4: Write a manifest for the bundle

A good manifest uses stable relative paths from the bundle root, deterministic ordering,
and digests such as SHA-256. The ordering rule should be simple and reproducible, for
example sorted normalized relative paths. Absolute paths do not belong because the bundle
contract must travel across machines and directories without changing meaning. A useful
verification transcript shows both a successful pass and the exact command used.

## Exercise 5: Add provenance without confusing its role

A strong provenance file records the producing repository revision, workflow identity,
runtime or environment context, and relevant configuration details that affect meaning.
It answers questions such as "what software context produced this bundle?" It does not by
itself answer "which published files are part of the public promise?" or "what should a
consumer read first?" Those remain contract questions.

## Exercise 6: Write a consumer test

A strong consumer accepts only the bundle path, validates the documented machine-facing
artifact, and intentionally knows nothing about `results/`, internal rule names, or
producer-only configuration. The success condition is that the consumer can do useful
work with no hidden repository knowledge. That is the proof that the public contract is
real and not just a copied folder.

## Exercise 7: Corrupt the bundle and detect it

The failed verification should identify the changed path and report a checksum mismatch or
equivalent integrity failure. What this proves is file identity: the bytes are no longer
the same as the inventoried bundle. What it does not prove is semantic correctness,
scientific validity, or whether the bundle was the right contract to publish in the first
place.

## Exercise 8: Simulate a downstream compatibility check

Likely compatible within `v1`:

- adding a new optional field to `summary.json`

Likely versioning discussion:

- renaming the file to `published-summary.json`
- removing an existing field that consumers may rely on

Why:

An additive field can preserve the old contract if existing consumers still work. Path
changes and field removals often alter the public promise directly.

## Exercise 9: Design a deliberate version migration

`v1` should remain intact for supported consumers while `v2` introduces the breaking
change under a new public boundary. A good migration note maps old paths or fields to the
new ones, states who should move and when, and keeps separate consumer tests for both
supported versions. The internal workflow tree still does not belong in either API,
because versioning is about the public promise, not about exposing producer internals.

## Exercise 10: Review a full publish change like a downstream maintainer

A strong review starts with findings ordered by downstream trust impact: hidden dependency
on `results/`, renamed public path, mismatched manifest coverage, changed artifact role,
or unclear consumer surface. Each correction should name the narrowest verification route
that proves the repair, such as rerunning the bundle verifier, rerunning the consumer
test, or diffing the published role table. One appropriate outcome is to say a change
should be versioned, postponed, or removed rather than merged under the current contract.

## Self-check

If your answers consistently explain:

- what is internal versus public
- what changed in the contract
- which artifact carries which responsibility
- what evidence supports downstream trust

then you are using the module correctly.
