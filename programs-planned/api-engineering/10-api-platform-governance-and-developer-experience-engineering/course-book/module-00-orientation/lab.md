# Orientation lab — Lock the predecessor and classify claims

## Setup

Run `make doctor`, `make predecessor-proof`, and inspect
`capstone/predecessor/handoff/BOUNDARY.json`.

## Controlled action

Create a scratch copy of `schema.graphql`, change one field, and point a scratch
registry entry to it. Then run predecessor and registry checks.

## Oracle

The original handoff remains valid. The changed bytes must receive a new release
identity or be rejected; they may not overwrite Graph API 1.0.

## Required evidence

Record the original digest, changed digest, rejecting check, platform authority,
and domain authority in `reports/orientation-boundary.json`.

## Cleanup

Delete the scratch artifact and report. Rerun predecessor proof.

## Completion gate

You can explain why the platform can publish a release but cannot silently mutate
the owner’s release.
