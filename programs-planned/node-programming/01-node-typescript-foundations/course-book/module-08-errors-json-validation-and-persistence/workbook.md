# Module 8 Workbook

## A. Failure taxonomy

Classify each: malformed command token, valid JSON with missing fields, unknown storage version, impossible state transition, missing file, permission denied, disk write failure, programmer assertion failure.

## B. Validator construction

Build validators for a versioned configuration containing mode, positive concurrency, and an optional output path. Return all independent issues with paths.

## C. Cause preservation

Repair:

```ts
try {
  return await readFile(path, 'utf8');
} catch {
  throw new Error('load failed');
}
```

The repaired error must identify operation and path and preserve the original value.

## D. Canonical encoding

Define a deterministic JSON encoding policy for records with optional notes and unordered input. Write tests that would fail if order or newline policy changes.

## E. Independent laboratory

Complete [Validated Configuration](../../labs/module-08-validated-configuration/README.md). It requires path-aware issues and construction from checked fields.

## F. StudyLedger transfer

Implement V1 validation and persistence. Add fixtures for invalid JSON, wrong format, duplicate IDs, invalid state fields, and inconsistent `nextId`.

## G. Reconstruction

Explain unknown catch values, error translation, JSON syntax versus domain validity, validator authority, canonical encoding, missing-file policy, and save-before-success behavior.

## H. Hostile storage fixture

Construct one JSON document containing at least six independent defects: wrong format, unknown root key, duplicate ID, invalid timestamp, impossible chronology, and state-specific missing field. Decide which issues can be reported together and which depend on a prerequisite.

Repair this loader:

```ts
async function load(path: string): Promise<Ledger> {
  try {
    return JSON.parse(await readFile(path, 'utf8')) as Ledger;
  } catch {
    return emptyLedger();
  }
}
```

Your repair must distinguish missing file, malformed JSON, invalid schema, and I/O failure.

## I. Save-claim review

Write the strongest accurate claim supported by same-directory temporary write plus rename. Then list three stronger properties it does not prove.

## J. StudyLedger checkpoint

Implement V1 decoding from `unknown`, duplicate detection, chronological validation, and canonical encoding. Add a test that a failed decode leaves the caller’s existing ledger unchanged.
