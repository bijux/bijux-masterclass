# Capstone Review Worksheet

Use this page when you want to review the capstone as an inherited DVC repository, not
just read it as course material. The point is to leave with explicit judgments you could
defend in code review, maintenance planning, or a handoff.

## How to use the worksheet

Work top to bottom. For each section:

1. answer the question in your own words
2. name the file or saved bundle that supports the answer
3. record one risk only if you can point to the owning boundary

If you cannot name the evidence, the judgment is still too soft.

## Repository contract

Ask:

- what the repository claims to build, compare, promote, and restore
- which files are public contracts and which are internal execution detail
- whether a new maintainer could discover the supported routes without oral explanation

Best evidence:

- `capstone/dvc.yaml`
- `capstone/Makefile`
- `capstone/publish/v1/manifest.json`
- [DVC Capstone Guide](index.md)

## State authority

Ask:

- which layer is authoritative for declaration, execution, and promotion
- whether `dvc.yaml` and `dvc.lock` still tell compatible stories
- where params and metrics become reviewable instead of folkloric

Best evidence:

- `capstone/dvc.yaml`
- `capstone/dvc.lock`
- `capstone/params.yaml`
- `capstone/metrics/metrics.json`

## Promotion boundary

Ask:

- which promoted files are safe for downstream trust
- which artifacts remain internal repository state or supporting evidence
- whether the promoted contract is smaller and clearer than the whole repository

Best evidence:

- `capstone/publish/v1/`
- [Capstone Proof Guide](capstone-proof-guide.md)
- verify or verify-report bundle surfaces

## Recovery and durability

Ask:

- what survives local loss because the remote still has it
- what can be rebuilt from declarations alone and what cannot
- which downstream trust claims survive because recovery restored both recorded state and promoted state

Best evidence:

- `capstone/.dvc-remote/`
- `capstone/dvc.lock`
- [Capstone Proof Guide](capstone-proof-guide.md)
- recovery review bundle surfaces

## Ownership and change placement

Ask:

- whether declaration, implementation, promotion, and verification still live in readable places
- where you would place the next non-trivial change and why
- which changes would require stronger release or recovery review before approval

Best evidence:

- `capstone/dvc.yaml`
- `capstone/src/incident_escalation_capstone/`
- `capstone/src/incident_escalation_capstone/publish.py`
- `capstone/src/incident_escalation_capstone/verify.py`

## Record the result

Finish with one of these judgments:

- trust as-is
- trust with one named follow-up boundary
- do not trust yet because one specific proof or ownership question is unresolved

If your conclusion is longer than a short paragraph, the review probably drifted away
from one bounded question.
