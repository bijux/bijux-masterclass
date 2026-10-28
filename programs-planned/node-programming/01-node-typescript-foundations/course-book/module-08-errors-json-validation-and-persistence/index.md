# Module 8 — Errors, JSON, Runtime Validation, and Persistence Contracts

> **Question:** Where does untrusted data become trusted, and what state remains visible after each kind of failure?

## Why this comes now

StudyLedger has a trusted in-memory model and module boundaries. Persistence introduces text that may be missing, truncated, edited, stale, or malicious. TypeScript declarations do not cross that boundary automatically. The storage module must parse syntax, validate structure, enforce domain invariants, and preserve enough context to diagnose failure without partially publishing state.

## Outcomes

You can:

- distinguish throwing, returning failure data, and process termination;
- catch values as `unknown` and preserve causal errors;
- treat `JSON.parse` results as untrusted;
- build path-aware validation from small predicates;
- separate syntax, structural, domain, and version failures;
- define a canonical persistence format and deterministic encoding;
- ensure a failed load does not mutate an existing ledger;
- ensure a failed save is not reported as a successful command.

## 1. JavaScript can throw any value

```ts
throw 'failure';
```

Although good application code throws `Error` objects, catch bindings must be treated as `unknown`:

```ts
try {
  await operation();
} catch (error: unknown) {
  if (error instanceof Error) {
    // safe access to message and cause
  }
}
```

Do not assume every rejection is an `Error`. A boundary translator can normalize values while preserving the original as cause.

## 2. Error classes represent boundaries

StudyLedger distinguishes:

- `CommandError` — raw invocation grammar or token conversion;
- `ValidationError` — malformed persisted structure;
- `DomainError` — valid command cannot be applied to current state;
- `StorageError` — file read/write/replace failure.

The classes do not exist merely for `instanceof`. They allow the process layer to select messages and exit statuses without parsing strings.

```ts
export class StorageError extends Error {
  override readonly name = 'StorageError';

  constructor(message: string, options?: ErrorOptions) {
    super(message, options);
  }
}
```

Add context at the boundary that knows it. Do not wrap an error at every function level with a nearly identical message.

## 3. JSON syntax is not domain validity

```ts
const parsed: unknown = JSON.parse(text);
```

Even valid JSON can contain:

- an array where an object is expected;
- missing or extra version fields;
- duplicate session IDs;
- invalid state-specific fields;
- timestamps with arbitrary text;
- an invalid `nextId` relative to retained records.

Validation is a pipeline:

```text
bytes/text
   ↓ JSON syntax
unknown JavaScript value
   ↓ structural checks
candidate fields
   ↓ domain checks
trusted Ledger
```

Each stage should report its own failure category.

## 4. Path-aware issues

A useful issue identifies location and expectation:

```ts
interface ValidationIssue {
  readonly path: string;
  readonly message: string;
}
```

For example:

```text
sessions[2].actualMinutes: expected a positive safe integer
```

Collecting several independent issues can help with configuration files. Fail-fast validation can be simpler when later checks depend on earlier structure. StudyLedger validates each record with path context and stops before constructing a ledger if any issue exists.

## 5. Construct from validated values

Avoid returning the original object after checks. Construct a new trusted value:

```ts
function parsePlannedSession(value: unknown, path: string): PlannedSession {
  const record = expectRecord(value, path);
  const id = expectPositiveSafeInteger(record['id'], `${path}.id`);
  const topic = expectString(record['topic'], `${path}.topic`);
  // ...
  return { status: 'planned', id, topic, plannedMinutes, createdAt };
}
```

This prevents unvalidated extra prototypes or aliases from becoming part of the domain and creates one clear trust transition.

## 6. Versioned storage

StudyLedger stores:

```json
{
  "format": "STUDY_LEDGER_V1",
  "nextId": 4,
  "sessions": []
}
```

A version is a compatibility claim, not decoration. The V1 decoder accepts exactly the modeled format and rejects unknown versions. A future migration should be explicit rather than interpreting new data as old data accidentally.

Canonical encoding uses:

- stable top-level property construction;
- sessions sorted by ascending ID;
- omitted absent optional properties;
- two-space JSON indentation;
- one trailing newline.

JSON object property order is observable in produced text but should be treated as the product’s encoder policy, not a universal semantic equality rule.

## 7. Load is a candidate operation

A loader should produce either a complete trusted ledger or a failure. It should not mutate an existing ledger record by record:

```ts
async function loadLedger(path: string): Promise<Ledger> {
  const text = await readFile(path, 'utf8');
  const parsed: unknown = JSON.parse(text);
  return validateLedger(parsed);
}
```

A missing file is product policy. StudyLedger treats `ENOENT` as an empty ledger only at the named repository boundary. Other read failures remain errors. Do not catch every error and return empty state; that would turn permission failure or corruption into apparent data loss.

## 8. Save and visibility

The course writes a complete candidate to a same-directory temporary file and renames it into place. This reduces exposure to partial writes within the stated single-process learner contract.

It does not claim universal crash durability, concurrent-writer safety, or identical overwrite semantics on every filesystem. Course 6 treats durability and platform-specific replacement deeply.

The application reports mutation success only after save fulfills. If the domain transition succeeds but persistence rejects, the command fails visibly.

## 9. Error rendering belongs at the process edge

Library code returns or throws typed errors. `main.ts` maps them to:

- user-facing stderr;
- exit code 2 for command grammar;
- exit code 1 for domain, validation, or storage failure;
- exit code 0 for success.

A library must not call `process.exit`, because that prevents callers and tests from observing cleanup or handling errors.

## 10. StudyLedger increment

Implement:

- `validateLedger(value: unknown): Ledger`;
- state-specific session validators;
- format and `nextId` invariants;
- duplicate-ID rejection;
- deterministic `encodeLedger`;
- async load with missing-file policy;
- candidate-file save;
- typed errors with causes.

Use malformed fixtures. Test syntax failure separately from valid JSON with invalid domain structure.

## Common wrong models

### “JSON.parse returns my interface”

It returns a runtime value whose structure has not been established.

### “Catching and returning empty state is resilient”

It can convert corruption and permission errors into silent data loss.

### “Custom errors are only class ceremony”

They can preserve failure categories across layers without string parsing.

### “A temp file makes storage transactional”

It improves one failure boundary. It does not prove concurrent safety or universal durability.

### “A successful domain update is a successful command”

The command’s visible contract may require persistence to complete first.

## 11. Errors describe failed boundaries

A useful error answers three questions:

1. what operation was attempted?
2. at which product boundary did it fail?
3. what causal detail should the next layer retain?

JavaScript permits throwing any value:

```ts
throw 'bad';
throw 17;
throw { reason: 'bad' };
```

Therefore `catch (error: unknown)` is the honest starting point. When wrapping an unknown cause, do not assume `.message` exists.

Custom error classes are justified when callers need stable categories or structured fields. StudyLedger distinguishes command, domain, storage-validation, and storage-I/O errors because the process shell renders them differently and chooses different exit statuses.

## 12. Validate in layers

A JSON document can be syntactically valid and still violate every domain rule. A robust decoder performs layered checks:

```text
bytes/text
   ↓ JSON syntax
unknown JavaScript value
   ↓ root shape and version
candidate fields
   ↓ field validation
state-specific candidate
   ↓ cross-field invariants
trusted domain value
```

Do not construct the trusted interface and then “check a few fields.” Build a new value only from validated components.

Path-aware issues make nested failures actionable:

```text
$.sessions[2].actualMinutes: expected an integer from 1 to 2880
```

Collect independent issues when doing so does not require inventing missing prerequisites. Once the root is not an object, reporting every child field as missing adds noise rather than information.

## 13. Exact objects and unknown keys

Structural TypeScript types allow wider objects. A storage schema may choose to reject unknown keys to catch misspellings and unsupported future data:

```json
{
  "status": "completed",
  "actualMinute": 20
}
```

If unknown keys are ignored, this typo may combine with a missing required `actualMinutes` field. Reporting both paths gives a direct repair.

Unknown-key rejection is a compatibility policy. A forward-compatible protocol may instead preserve or ignore unknown fields. Course 1 uses strict local storage because one program owns both encoding and decoding.

## 14. Version markers define migration authority

A format marker such as `STUDY_LEDGER_V1` means the decoder recognizes one schema. It does not mean every future field can be appended without review.

For each change, decide:

- can old readers safely ignore it?
- can new readers distinguish old records?
- is a default semantically honest?
- must data be migrated before ordinary use?
- will canonical re-encoding erase information?

A V2 migration should be an explicit function from validated V1 to validated V2, not a collection of ad hoc optional defaults in the main decoder.

## 15. Loading is a candidate operation

Do not mutate live state while decoding records one by one. Parse and validate a complete candidate, then publish it:

```text
existing in-memory ledger remains valid
        ↓
read complete candidate text
        ↓
validate complete candidate value
        ↓
return candidate or error
```

If record 20 is invalid, records 1–19 must not have partially replaced the caller’s state. This is the same candidate-publication pattern used for immutable domain updates.

## 16. Save semantics must be stated narrowly

StudyLedger writes a unique temporary file in the destination directory and then renames it. Under ordinary single-process use, readers do not observe a half-written JSON document.

That does not automatically guarantee:

- crash durability after power loss;
- atomic replacement on every filesystem and operating system combination;
- correct behavior under concurrent writers;
- directory metadata synchronization;
- preserved permissions or ownership in every deployment.

Later systems courses build stronger file protocols. Course 1’s contract is explicit single-user local persistence.

## 17. Success belongs after the effect

A domain transition produces a candidate ledger. The command is not successful until persistence fulfills:

```ts
const next = planSession(current, input, now);
await save(path, next);
return successMessage(next);
```

Printing before `await save` creates a false external fact. Tests should arrange a rejecting save and prove no success result is returned.

## Practice sequence

Complete the [workbook](workbook.md), then [Validated Configuration](../../labs/module-08-validated-configuration/README.md). Add V1 storage and hostile fixtures to StudyLedger.

## Ready to continue

Continue when you can point to the exact line where untrusted data becomes a newly constructed trusted value and explain every state visible after read, validation, transition, and save failure.

Next: [Module 9 — Promises, Event-Loop Ordering, CLI Boundaries, and Async Files](../module-09-promises-event-loop-cli-and-files/index.md)
