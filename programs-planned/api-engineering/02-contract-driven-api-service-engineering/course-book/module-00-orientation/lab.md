# Orientation Lab — Establish a Trustworthy Starting Point

## Objective

Prove that the Course 2 repository, predecessor boundary, language choice, and evidence routes are understood before module work begins.

## Setup conditions

- extract the program into a clean workspace;
- do not modify predecessor or handoff files;
- ensure Python, Node.js, and Make are discoverable;
- create `work/orientation/` for evidence;
- record unavailable optional infrastructure before running proofs.

## Failure action and investigation

1. Read the course responsibility and incoming boundary aloud or write them from memory.
2. Run `make doctor` and `make predecessor-proof`.
3. Select the primary track and locate its implementation root and focused tests.
4. Locate the same invariant in the comparison track.
5. Introduce one reversible, dependency-light defect: alter one idempotency vector so the same key is reused with a different request fingerprint but is still marked as a replay.
6. Predict which focused proof should fail, run it, and capture the smallest failing output.
7. Restore the original file, rerun the narrow proof, then run `make core-proof`.
8. Write the exact live dependency or external tool not exercised in this environment.

## Operational oracle

The predecessor remains byte-identical, the planted defect is rejected by the predicted proof, the restored tree passes the dependency-light course proof, and no unavailable live route is reported as passed.

## Required evidence

Create:

```text
work/orientation/
├── durability-boundary.md
├── track-choice.md
├── doctor.txt
├── predecessor-proof.txt
├── planted-defect.md
├── repaired-proof.txt
└── evidence-boundary.md
```

`planted-defect.md` must name the claim, owner, failure, predicted oracle, actual observation, and permanent regression.

## Cleanup and reset

Remove transient caches and processes, restore the fixture from version control or the packaged archive, retain only reviewable evidence, and verify that the predecessor manifest still passes.

## Completion gate

- [ ] course responsibility and predecessor boundary are stated correctly;
- [ ] primary and comparison tracks are recorded;
- [ ] the course book and capstone paths are located;
- [ ] one controlled defect was rejected and repaired;
- [ ] dependency-light proof passes from the restored tree;
- [ ] unavailable live evidence is explicitly named.
