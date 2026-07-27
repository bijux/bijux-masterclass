# Worked Example: Promoting Results Into a Versioned Publish Bundle

This file ties the whole module together around one realistic problem:

> a workflow already produces useful results, but downstream users still have no clear, reviewable contract they can trust.

The question is not "how do we copy more files into `publish/`?" The question is how to
turn internal results into a smaller, versioned bundle that another program can use
honestly.

## How to use this worked example

Work through this page with the five core lessons nearby.

Do not treat it as a decorative summary. Treat it as a guided dry run of the exact review
questions the module is building:

- what stays internal
- what becomes public
- what each public artifact is responsible for
- how the bundle proves itself to a downstream user

## The one-day teaching goal

By the end of this example, you should be able to explain one publish bundle without
falling back on vague phrases like "final outputs" or "metadata."

You should be able to point to each promoted file and say:

- why it is public
- what audience it serves
- what evidence supports trusting it

## The lab route

Work through the example in this order:

1. separate internal workflow detail from files a downstream consumer should see
2. promote the smallest honest public bundle into `publish/v1/`
3. assign one clear job to each artifact in that bundle
4. verify the bundle through manifest and consumer checks
5. finish by classifying one compatible change and one breaking change

## The starting situation

Assume the workflow already produces rich internal outputs under `results/`, such as:

- per-sample QC JSON files
- trimming summaries
- deduplication summaries
- screening summaries

Those files are useful, but they are not yet a downstream contract. If another notebook
or pipeline must browse `results/{sample}/` to discover what is safe to read, the publish
story is still weak.

## What the learner should notice first

The workflow is not failing here.

The weakness is subtler: the repository is producing useful material, but it is still
making downstream consumers infer the public surface for themselves.

That distinction matters because many real repositories reach this stage and stop too
early.

## Promote only the right surfaces

Start by choosing the smallest bundle that another program can understand:

- `publish/v1/summary.json`
- `publish/v1/summary.tsv`
- `publish/v1/report/index.html`
- `publish/v1/provenance.json`
- `publish/v1/manifest.json`
- `publish/v1/discovered_samples.json`

That bundle is smaller than the full workflow state, but stronger as a contract because
each file has a named role.

The summarize and report rules should make the promotion visible:

```python
rule summarize:
    output:
        json="publish/v1/summary.json",
        tsv="publish/v1/summary.tsv"

rule report:
    input:
        json=rules.summarize.output.json
    output:
        html="publish/v1/report/index.html"
```

This matters because the report now depends on a machine-readable contract file rather
than inventing a separate truth.

## A short checkpoint before you continue

Pause here and ask:

- could a downstream script work only from `publish/v1/`?
- could a reviewer explain why each promoted file is public?
- could the internal workflow tree change without automatically breaking the consumer?

If the answer to any of these is no, the bundle is not yet ready.

## Give every artifact one job

The bundle works only if each artifact has a stable role:

- `summary.json` and `summary.tsv`: machine-facing contract files
- `report/index.html`: human-facing interpretation
- `manifest.json`: inventory and checksum evidence
- `provenance.json`: software-context evidence
- `discovered_samples.json`: reviewed discovery record

Once those roles are clear, a downstream maintainer can ask better questions:

- which file should my code read
- which file should a human inspect
- which file tells me whether the bundle is damaged
- which file tells me what software context produced the bundle

## Why this role separation matters educationally

This is the moment where learners usually stop calling everything "the output."

That change in language is important. Once each artifact has one named job, bundle review
becomes more precise and much easier to teach.

## Inventory the contract explicitly

The publish rule should gather the promoted surfaces into a manifest with stable relative
paths:

```python
rule manifest:
    input:
        summary_json = rules.summarize.output.json,
        summary_tsv  = rules.summarize.output.tsv,
        report_html  = rules.report.output.html,
        provenance   = rules.provenance.output.json,
        discovered   = rules.publish_discovered_samples.output.json,
    output:
        json = "publish/v1/manifest.json"
```

The important thing is not the syntax. It is the claim the manifest makes: these are the
files that belong to the public bundle.

Use stable relative paths and checksums, for example:

```json
{
  "contract_version": "v1",
  "files": [
    {"path": "summary.json", "sha256": "..."},
    {"path": "summary.tsv", "sha256": "..."}
  ]
}
```

Do not write absolute machine-specific paths into the manifest. The contract must travel
with the bundle.

## Verify the bundle from the consumer side

Now make the bundle prove itself through two routes:

```sh
python scripts/verify_publish.py --publish publish/v1
python scripts/consume_summary.py publish/v1/summary.json
```

The first route checks the bundle's internal coherence. The second route checks whether a
consumer can use the documented machine-facing surface without any secret knowledge of the
repository.

That second test is often where weak publish boundaries become obvious.

## What the learner should notice now

The bundle is no longer just "generated output." It has become something that can be
verified from the outside.

That is a major shift in maturity, and it is what Module 06 is trying to normalize.

## Think through change scenarios

Now imagine three possible changes:

1. `summary.json` gains a new optional field.
2. `report/index.html` is renamed to `report/report.html`.
3. another team starts reading `results/sample-a/kmer.json` because the publish bundle
   does not yet expose what they need.

These changes do not mean the same thing:

- the first may be a compatible additive change
- the second is likely a public-path compatibility problem
- the third is a warning that the bundle may need to grow, not permission to bypass it

That is exactly the judgment this module is trying to teach.

## The repaired publish story

By the end of the repair, the workflow can be described cleanly:

1. internal results remain workflow-operational detail
2. a smaller versioned bundle becomes the downstream contract
3. machine and human artifacts have different jobs
4. manifests and provenance defend different parts of trust
5. consumer tests review the bundle from the outside

That is what it means to promote results into a versioned publish bundle.

## Review questions for the repaired design

When you inspect a repository shaped like this, ask:

1. which files are public promises and which remain internal workflow state
2. which machine-facing artifact a downstream program should read first
3. where integrity evidence lives and what it can actually prove
4. which change would require a version discussion
5. how the bundle would behave for a consumer that knows nothing about `results/`

If those answers are visible, the module's publish story has landed.
