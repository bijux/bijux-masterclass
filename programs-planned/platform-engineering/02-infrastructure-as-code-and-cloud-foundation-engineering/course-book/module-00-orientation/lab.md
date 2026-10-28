# Orientation Lab — Prove the Boundary Before Creating Infrastructure

## Goal

Demonstrate that the repository, Course 1 handoff, local toolchain, and optional cloud identity are the exact inputs intended for this course.

## Safety boundary

Do not run `tofu apply`, create credentials, modify an AWS Organization, or use an account whose owner and purpose are unclear. The orientation lab is read-only.

## Baseline

Begin from a clean extraction or checkout. No `.terraform` directory, saved plan, generated state, cloud credential file, or prior lab report may be treated as course evidence.

## Hypothesis

The dependency-light course can be verified without cloud authority, and the optional AWS lane can be entered only when caller account, region, budget, and cleanup ownership match the declared sandbox boundary.

## Controlled action

1. Run `make doctor` and retain the environment classification.
2. Run `make predecessor-proof` and inspect the nine inherited files.
3. Record Python, OpenTofu, AWS CLI, and MkDocs availability.
4. Search the repository for static cloud credentials and private production material.
5. When AWS is available, set `ATLAS_AWS_ACCOUNT_ID` and `ATLAS_AWS_REGION`, then run `make aws-preflight`.
6. Compare the observed caller with the declared sandbox account and verify the region.
7. Record the cost budget, quota assumptions, resource owner, and teardown deadline.
8. Run `make core-proof` to establish the dependency-light baseline.

## Oracle

The predecessor hashes match; the dependency-light proof uses no cloud credential; no secret appears in the repository; and the optional AWS caller identity exactly matches the declared sandbox account and region before any plan or apply.

## Evidence

Retain the doctor output, predecessor verification, credential scan result, optional STS caller identity, region/budget/cleanup declaration, and the core-proof result.

## Interpretation

State which evidence classes are available. A machine with Python but no OpenTofu or AWS credentials is still ready for the full dependency-light reading and semantic labs; it is not ready for native HCL or cloud claims.

## Cleanup

Remove generated cache and report files with `make clean`. Do not delete the retained evidence journal. Verify that no cloud resource was created.

## Completion gate

Proceed only when the Course 1 handoff is exact and every optional cloud action would target an explicitly owned sandbox with a cleanup deadline.
