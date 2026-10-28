# Orientation — OpenAPI Contract Engineering

> **Program stage:** Course 1 of 6 — Specify the promise.

> **Orientation question:** What must be known, frozen, runnable, and honestly reported before the first teaching module begins?

## Purpose

Orientation protects learning time. Day 1 should begin with the course responsibility, not with an unknown shell, a broken package manager, an unverified predecessor, or a language track chosen by accident. You will locate the authoritative course book, verify the incoming boundary, select an implementation route, and prove that the local repository can detect at least one controlled failure.

## Incoming boundary

Basic programming ability and no assumed OpenAPI experience.

Do not edit predecessor or handoff files. If their integrity proof fails, repair the extraction or obtain a correct predecessor package; do not regenerate history from the current implementation.

## Learning outcomes

By the end of orientation, you can:

- state this course's responsibility and its non-responsibilities;
- distinguish the Analysis Runs Platform from its HTTP API and later event API;
- identify the public API, specification, profile, service-release, and migration version axes;
- choose the primary and comparison language tracks deliberately;
- locate the chapter, implementation, fixture, lab, checkpoint, and proof paths;
- run dependency-light diagnostics and report unavailable live dependencies honestly;
- make one narrow proof fail, explain why, repair it, and retain the regression.
- produce `contract-boundary.md` explaining the authority and evidence unique to this course.

## Repository map

```text
course-book/     authoritative learner material
capstone/        continuing Analysis Runs Platform and evidence
scripts/         bounded proof and packaging routes
tests/           regressions and planted-defect sensitivity
reports/         machine-readable executed evidence
```

The root README is a map. It is not a substitute for the course-book sequence.

## Course-specific boundary

Course 1 begins before durability. The authoritative artifact is the canonical OpenAPI source and its deterministic bundle, not a framework-generated document. The two reference providers are observations of that contract. Orientation therefore focuses on raw HTTP, YAML/JSON structure, reference resolution, examples, and provider-neutral behavior. Do not infer PostgreSQL, production identity, hostile-input resistance, or operated reliability from a green contract proof; those become explicit later responsibilities.

## Language decision

Both Python/FastAPI and TypeScript/Fastify are used symmetrically to prove that the contract is language-neutral. Record the choice and the reason. The comparison track exists to test whether the invariant is architectural, not to double the typing workload.

## First proof

```bash
make doctor
make core-proof
make core-proof
```

Read every skipped or not-executed result. A missing live database, broker, network topology, renderer, or external CLI is an evidence boundary, not a successful experiment.

## Readiness self-check

Before continuing, explain in your own words:

1. what this course adds to the platform;
2. what the predecessor has already settled;
3. which file is authoritative for the learner;
4. which state or contract artifact is authoritative for the system;
5. which proof can run locally and which requires live infrastructure;
6. how your primary and comparison tracks will be used.

Continue only when those answers are concrete and the orientation lab can be reproduced from a clean working tree.
