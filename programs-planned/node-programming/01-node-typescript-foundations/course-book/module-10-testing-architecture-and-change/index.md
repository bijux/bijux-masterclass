# Module 10 — Testing, Architecture, Integration, and Independent Change

> **Question:** Can you make a cross-layer change and prove the process still behaves correctly without tutorial imitation?

## Why this comes now

The final module introduces no large language mechanism. It integrates the previous nine. A complete Node.js program can type-check and still be wrong at runtime, validate values and still mishandle aliases, await promises and still publish success before persistence, or pass unit tests while its binary writes the wrong stream.

Mastery is demonstrated through independent change: identify every affected authority, update the smallest coherent set of boundaries, and produce evidence at the level where the promise is observable.

## Outcomes

You can:

- select unit, integration, fixture, type-check, and process evidence by claim;
- use Node’s built-in test runner with isolated temporary resources;
- test deterministic time through injection rather than sleeping;
- test asynchronous rejection and process exit behavior directly;
- explain StudyLedger’s dependency direction and state transition path;
- trace one feature through grammar, types, validation, persistence, rendering, and tests;
- distinguish source completeness from cross-platform or production proof.

## 1. Tests protect contracts, not functions

A test should name the promise:

```ts
import test from 'node:test';
import assert from 'node:assert/strict';

test('completing a session preserves the prior ledger on invalid duration', () => {
  // arrange, act, assert
});
```

Avoid tests whose only claim is that a private helper returned its current implementation detail. Refactoring should be possible while public behavior remains protected.

## 2. Four main evidence boundaries

### Pure unit tests

Use for parsers, transitions, normalization, queries, and rendering. They are fast and make inputs explicit.

### Module integration tests

Import the public `index.js` and exercise several internal components together. These tests catch broken exports and incorrect composition.

### Persistence tests

Use temporary directories and real files to verify missing-file policy, canonical bytes, malformed fixtures, and save/load behavior. They do not prove every filesystem’s crash semantics.

### Process tests

Spawn the compiled CLI and observe:

- exit code;
- stdout;
- stderr;
- resulting file;
- behavior over several invocations.

Only this boundary proves the shell-facing contract.

Type-check investigations complement these tests by proving static relationships that may have no runtime symptom.

## 3. Test isolation

Each test owns its resources:

```ts
const directory = await mkdtemp(join(tmpdir(), 'study-ledger-'));
try {
  // test
} finally {
  await rm(directory, { recursive: true, force: true });
}
```

Do not share one mutable file across tests. Process-level test runners may isolate files in child processes, but filesystem paths, environment variables, ports, and global module state can still collide if the test design shares them.

## 4. Deterministic dependencies

Never test clock behavior by sleeping until time changes. Inject a clock:

```ts
const clock = () => new Date('2026-08-09T08:00:00.000Z');
```

For multiple calls, supply a sequence and assert consumption count. Similarly inject or isolate environment, paths, and external adapters.

The test should fail if the implementation reads a global instead of the supplied dependency.

## 5. Testing errors

A rejection test should inspect category and relevant context:

```ts
await assert.rejects(
  () => loadLedger(path),
  (error: unknown) => {
    assert.ok(error instanceof ValidationError);
    assert.match(error.message, /sessions\[1\]/);
    return true;
  },
);
```

Do not overfit to complete operating-system error wording. Test application-added context and stable categories; allow low-level cause text to vary.

## 6. Architecture review

StudyLedger should satisfy this direction:

```text
process/main
      ↓
application ───> command parser
      ↓                ↓
repository ─────────> domain/query
```

Review questions:

- Does domain code import `node:` APIs?
- Does parsing execute effects?
- Does storage decide domain transitions?
- Does the binary contain business rules?
- Can a read-only command avoid write access?
- Can a failed mutation leave a partially changed in-memory ledger?
- Can success print before save fulfills?
- Can tests replace time without patching globals?

## 7. Independent feature trace

Suppose you add labels. The change affects:

1. command grammar and duplicate-option policy;
2. label normalization and bounds;
3. session types;
4. V1 compatibility decision or a V2 migration;
5. canonical encoding order;
6. search semantics;
7. list rendering;
8. unit, persistence, and process tests;
9. help and documentation.

The correct response is not necessarily “edit every file.” First decide whether labels belong to sessions, plans, or a separate index, and whether the current storage version can represent them compatibly.

## 8. The test pyramid is not a quota

More unit tests than process tests is common because pure cases are cheaper. The correct distribution follows risk and observability. One process test can protect a broad shell contract, while many focused validator tests cover malformed shapes.

Do not chase coverage percentage without asking which behavior remains unchallenged. A line can execute without its important alternative being tested.

## 9. What Course 1 does not prove

Even a complete `make proof` does not establish:

- behavior on every maintained operating system;
- safety under concurrent writers;
- crash durability;
- locale-independent human text behavior;
- absence of every dependency or runtime vulnerability;
- scalability to unbounded files or records;
- correctness of future Node or TypeScript versions.

These are explicit handoffs to later courses, not excuses for vague claims.

## 10. Final construction

Complete [Reading Ledger](../../labs/module-10-reading-ledger/README.md) from its contract without copying StudyLedger. Then finish StudyLedger and select an independent feature.

Your defense should show:

- the raw-input boundary;
- the trusted domain boundary;
- object identity and update policy;
- module direction;
- promise ownership;
- persistence visibility;
- process behavior;
- evidence for every public claim;
- remaining non-contracts.

## 11. Build an evidence matrix before writing tests

Map each product claim to the nearest observable boundary:

| Claim | Best first evidence |
|---|---|
| minutes parser rejects exponent notation | pure unit test |
| illegal state transition preserves prior ledger | domain unit test with retained value |
| public entry exports only supported names | module integration or structural test |
| malformed JSON reports a session path | codec fixture test |
| missing file becomes empty ledger | real temporary-directory test |
| success waits for save | application test with a controlled rejecting dependency |
| usage failure writes stderr and exits 2 | spawned process test |
| source relationship should be rejected | type-check investigation |

A larger test is not automatically stronger. A process test can prove the CLI contract but may localize parser defects poorly. Use several distances where the product has several boundaries.

## 12. The Node test runner and isolation

`node:test` supports asynchronous tests, nested tests, hooks, mocking facilities, and process-level configuration. Course 1 uses the smallest subset needed for explicit contracts:

```ts
import test from 'node:test';
import assert from 'node:assert/strict';

test('description names the promise', async () => {
  const actual = await operation();
  assert.deepEqual(actual, expected);
});
```

Do not rely on execution order among independent tests. Each test owns its directory, environment, and mutable fixtures. Cleanup should occur even after assertion failure, commonly through `try/finally` or test hooks.

Avoid time-based sleeps. A sleep proves only that a duration elapsed in one environment. Inject clocks, use controllable promises, or observe an explicit event.

## 13. Fakes, stubs, and mocks by responsibility

The terminology matters less than fidelity to the real boundary:

- a **stub** returns controlled values;
- a **fake** implements a simpler working version, such as in-memory storage;
- a **spy** records calls for later assertions;
- a **mock expectation** fails when a specified interaction differs.

Course 1 usually needs small fakes and spies built from functions. A fake repository must preserve the same asynchronous and failure contract as the real repository. If the real `save` returns `Promise<void>`, a synchronous test helper returning `void` is not the same dependency.

Test interactions only when order or count is part of the product. StudyLedger tests that `save` occurs before success because this is a published command guarantee. It does not assert every private helper call.

## 14. Invariant tests are stronger than example-only tests

Examples protect named cases. Invariants protect a relationship across many cases. Even without a property-testing library, tables and generated loops can challenge an invariant:

```ts
for (const raw of ['', ' ', '+1', '-1', '1.0', '1e3']) {
  assert.throws(() => parsePositiveInteger(raw));
}
```

Useful Course 1 invariants include:

- encoding then decoding a valid ledger preserves meaning;
- invalid transitions leave the supplied ledger unchanged;
- list and search never mutate source order;
- every successful plan increments `nextId` exactly once;
- read-only commands never save;
- canonical output does not depend on object insertion accidents.

Later courses add property-based and fuzz testing. The reasoning starts here.

## 15. Architecture is a dependency claim

A directory tree is not architecture by itself. State the allowed direction:

```text
main/process
    ↓
application
   ↙   ↘
domain  storage
```

Then test or audit the properties that matter:

- domain imports no `node:` APIs;
- storage does not parse CLI tokens;
- main contains no transition policy;
- application receives effects through a narrow dependency object;
- public `index.ts` does not expose temporary-file helpers.

A static source audit can catch some violations. Integration behavior catches others. The explanation should survive file renaming.

## 16. Independent change as the final proof

Choose one feature not implemented by the chapter. `reopen` is a useful example: a completed or abandoned session may become planned again under a named policy.

Before coding, answer:

1. Which source states are legal?
2. Which fields survive and which are removed?
3. Does the same ID remain?
4. Is a new timestamp required?
5. Can V1 storage represent the result without migration?
6. Which command grammar is added?
7. Which renderers or summaries change?
8. Which unit, codec, application, and process evidence is necessary?

The point is not feature volume. It is the ability to trace a requirement through every authority without copying a prepared patch.

## 17. Course 1 completion standard

You are ready to continue when you can build a different small Node program from a written contract and explain:

- which values exist at runtime;
- which facts are static only;
- where unknown data becomes trusted;
- which identities may change;
- who owns each promise;
- which module owns each policy;
- what each test actually proves;
- what the product explicitly does not claim.

That foundation is what makes later work with prototypes, streams, HTTP, databases, workers, and production systems learnable rather than framework-dependent.

## Common wrong models

### “Unit tests are enough because every function is tested”

Module resolution, files, streams, and exit status are not function-local promises.

### “A process test should assert exact system error text”

Stable application context and categories are better contracts than platform wording.

### “High coverage means high confidence”

Coverage reports execution, not the quality of assertions or input space.

### “Dependency injection means a container framework”

Course 1 uses ordinary function parameters and small interfaces.

### “Final means production proven”

The course produces a complete, bounded educational product and states the evidence boundary honestly.

## Completion

You are ready for Course 2 when you can reconstruct StudyLedger from its public contract and implement a different small Node.js product without searching for a framework to supply the missing mental model.

Return to the [course index](../index.md) or complete the [final review](../final-review.md).
