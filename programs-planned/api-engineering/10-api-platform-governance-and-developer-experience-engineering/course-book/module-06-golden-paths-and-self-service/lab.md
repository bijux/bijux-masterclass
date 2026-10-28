# Lab 06 — Generate, break, and repair a golden path

## Setup

Run `make template-proof`. Inspect the template specification and skeleton.

## Controlled action

Generate `reporting-api` with valid parameters. Then attempt invalid API identity,
an unresolved placeholder, an extra undeclared output, and an embedded token.
Finally, alter a safe default and determine whether the template needs a patch,
minor, or major release.

## Oracle

Valid generation is deterministic and complete. Invalid inputs fail before
publication. Secret and output-contract defects fail. Version impact is explained
from generated-consumer compatibility, not intuition.

## Required evidence

Create `reports/module-06-golden-path.json` with template version, parameters,
file digests, rejected defects, and upgrade classification.

## Cleanup

Delete generated scratch projects and rerun template proof.

## Completion gate

The golden path is useful without being magical: it creates a safe proposed API,
not an automatically approved active product.
