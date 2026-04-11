<a id="top"></a>

# Capstone Review Worksheet

Use this page when you want to review the capstone as an inherited workflow repository,
not just read it as course material. The point is to leave with explicit judgments you
could defend in code review, maintenance planning, or a handoff.

## How to use the worksheet

Work top to bottom. For each section:

1. answer the question in your own words
2. name the file or saved bundle that supports the answer
3. record one risk only if you can point to the owning boundary

If you cannot name the evidence, the judgment is still too soft.

[Back to top](#top)

## Repository contract

Ask:

- what the repository claims to build and publish
- which files are public contracts and which are internal execution detail
- whether a new maintainer could discover the supported routes without oral explanation

Best evidence:

- `capstone/Snakefile`
- `capstone/Makefile`
- `capstone/workflow/contracts/FILE_API.md`
- [Capstone Guide](index.md)

[Back to top](#top)

## Workflow truth

Ask:

- where the real file contracts live
- where dynamic discovery becomes a durable artifact
- whether any important behavior still feels hidden or nondeterministic

Best evidence:

- `capstone/workflow/rules/preprocess.smk`
- `capstone/publish/v1/discovered_samples.json`
- walkthrough or tour bundle surfaces

[Back to top](#top)

## Policy and operating context

Ask:

- which differences across local, CI, and SLURM are operational policy
- what would count as semantic drift rather than policy drift
- whether a profile change could silently alter the published meaning of the workflow

Best evidence:

- `capstone/profiles/local/config.yaml`
- `capstone/profiles/ci/config.yaml`
- `capstone/profiles/slurm/config.yaml`
- [Profile Audit Guide](profile-audit-guide.md)

[Back to top](#top)

## Publish boundary

Ask:

- which outputs are safe for downstream trust
- which artifacts remain internal run state or supporting evidence
- whether the promoted contract is smaller and clearer than the whole repository

Best evidence:

- `capstone/publish/v1/`
- `capstone/workflow/contracts/FILE_API.md`
- [Publish Review Guide](publish-review-guide.md)
- verify-report bundle surfaces

[Back to top](#top)

## Architecture and ownership

Ask:

- whether the top-level `Snakefile` still explains the repository shape
- whether rule files, modules, scripts, and package code each have a readable job
- where you would place the next non-trivial change and why

Best evidence:

- `capstone/Snakefile`
- `capstone/workflow/rules/`
- `capstone/workflow/modules/`
- `capstone/workflow/scripts/`
- `capstone/src/capstone/`

[Back to top](#top)

## Record the result

Finish with one of these judgments:

- trust as-is
- trust with one named follow-up boundary
- do not trust yet because one specific proof or ownership question is unresolved

If your conclusion is longer than a short paragraph, the review probably drifted away
from one bounded question.

[Back to top](#top)
