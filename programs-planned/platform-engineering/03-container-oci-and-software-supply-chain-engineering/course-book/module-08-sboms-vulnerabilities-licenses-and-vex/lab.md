# Laboratory — Turn scanner findings into release decisions

## Goal

Generate an Atlas SBOM, measure its completeness, evaluate vulnerability findings, and author one bounded VEX statement.

## Safety boundary

Use the course vulnerability database and synthetic findings. Do not publish VEX claims about real third-party vulnerabilities from this lab without independent review.

## Baseline

Generate CycloneDX 1.7 evidence for the accepted API subject and validate structure, subject, required components, hashes, and licenses.

## Hypothesis

Policy will reject an incomplete BOM, fail a confirmed affected finding, require review for under-investigation evidence, and accept a precise not-affected VEX only for its exact subject.

## Controlled action

1. remove the Atlas component;
2. add an ambiguous component identity;
3. evaluate the affected fixture;
4. author a not-affected VEX using the reachability fixture;
5. change the subject digest without updating VEX;
6. add a component with unknown license.

## Oracle

Each case receives the correct fail/review/pass classification and explanation. Stale or incomplete evidence never passes because its JSON validates.

## Evidence

Submit BOM, independent completeness comparison, vulnerability decisions, VEX statement, license decision, and policy report.

## Interpretation

Explain the difference between detection confidence, exploitability, remediation priority, and release authorization.

## Cleanup

Remove defect BOM/VEX artifacts from the accepted release tree and rerun the capstone tour.

## Completion gate

A reviewer can trace every release decision from exact subject to inventory to finding to owned disposition.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
