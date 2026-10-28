# StudyLedger Engineering Guide

StudyLedger is the cumulative construction for Course 1. It is small enough to understand completely and large enough to require deliberate boundaries. The program is not a demonstration shell around one function. It has a real command language, a domain state machine, persistence, asynchronous effects, deterministic rendering, and process-level behavior.

## 1. Product contract

A study session begins as `planned`. It may become `active`, then `completed`; or it may become `abandoned` from either the planned or active state. Completed and abandoned states are terminal.

```text
planned ───────► active ───────► completed
   │                │
   └──────────────► └──────────► abandoned
```

The program must make illegal transitions visible. Completing a planned session is not “close enough” to starting and completing it. Starting a completed session is not an idempotent no-op. The state machine is part of the product meaning.

A successful mutating command must satisfy all of the following:

1. its arguments parse without accidental coercion;
2. the current file either does not exist or decodes into a valid ledger;
3. the domain transition succeeds without mutating the prior value;
4. the new ledger encodes canonically;
5. the save completes;
6. only then does the command report success.

A read-only command loads and validates the same file but never rewrites it.

## 2. Module-by-module construction

### Module 1 — Establish the executable package

Create an ESM package with a strict TypeScript configuration. Add the library entry point and a binary entry point. Prove that the program can distinguish its own direct execution from import by a test or a small runtime experiment.

Do not add domain logic yet. The objective is to establish the distinction among TypeScript source, emitted ESM JavaScript, package metadata, and the Node process.

### Module 2 — Parse primitive command values explicitly

Define the `plan` command. Treat terminal arguments as strings. Convert the minutes option only through a parser that rejects whitespace, signs, decimal notation, zero, and unsafe integers.

Do not use `Number(raw)` as the complete validation policy. `Number('')`, `Number('  ')`, and `Number('1e3')` demonstrate why conversion and acceptance are separate decisions.

### Module 3 — Make functions reveal authority and invocation

Extract pure helpers for positive integers and required options. Keep the real clock behind an injected `now()` function. A test must prove that a read-only command does not ask for time and that a mutating command asks exactly once.

This is the first architectural use of a callback: the callback is not decorative dependency injection. It makes nondeterministic time an explicit effect owned by the application boundary.

### Module 4 — Use immutable domain updates

Define the ledger and session shapes. Every transition returns a new ledger. Unchanged sessions preserve identity; the changed session receives a new object. Tests should keep older ledger values and prove that their states have not changed.

This is not a blanket claim that mutation is always bad. It is a local design choice that makes failed transitions, historical test values, and application orchestration easier to reason about.

### Module 5 — Encode the state machine with a discriminated union

Represent `planned`, `active`, `completed`, and `abandoned` as different variants. Fields that are meaningful only in one state belong only to that variant. Rendering and storage validation must switch exhaustively on `status`.

The type checker now helps prevent direct access to `actualMinutes` on a planned session, but external JSON can still lie. The runtime decoder remains necessary.

### Module 6 — Add deterministic queries and summaries

Add list, search, and summary operations. Define their ordering and matching rules. Search should operate over the topic plus terminal detail, without mutating or reordering the ledger. Summary must distinguish planned effort from completed effort rather than collapsing two different facts into one number.

### Module 7 — Protect package boundaries

Export only the API that tests and callers need through `src/index.ts`. Keep parsing helpers and storage internals private unless their behavior is itself part of the reusable contract. Use `.js` specifiers in TypeScript source because the emitted ESM files are JavaScript.

### Module 8 — Validate the persistence boundary

Treat `JSON.parse` as returning `unknown`. The decoder must validate:

- root shape and format marker;
- unknown fields;
- positive safe identifiers;
- state-specific fields;
- bounded text;
- canonical timestamps;
- chronological ordering;
- duplicate identifiers;
- `nextId` consistency.

Collect independent validation issues when practical. Do not continue constructing a value after a missing prerequisite makes the rest of the branch meaningless.

### Module 9 — Add asynchronous storage and the real CLI

Use promise-based filesystem operations. Missing storage means an empty ledger only for `ENOENT`; permission failures and malformed data are different outcomes. Save through a unique same-directory temporary file and rename it after the complete write.

Bind the program to `process.argv`, `process.env`, `stdout`, `stderr`, and `exitCode` only in `main.ts`. Keep process termination out of the reusable library.

### Module 10 — Prove the complete boundary

Add tests at several distances:

- domain tests for legal and illegal transitions;
- parser tests for token contracts;
- codec tests for hostile values;
- storage tests using temporary directories;
- application tests with fake effects;
- process tests that spawn the emitted CLI.

Then add one independent feature. Recommended choices are `reopen`, `rename`, or a date-range query. The feature must cross every affected layer and preserve compatibility with existing data.

## 3. Error model

StudyLedger separates command, domain, validation, and I/O failures. The classes are not used to imitate an enterprise exception hierarchy. They give the process shell enough information to choose an exit status and render a stable error code while preserving `cause` for diagnosis.

| Failure | Example | Exit status |
|---|---|---:|
| Usage | missing `--minutes` | 2 |
| Domain | complete a planned session | 1 |
| Storage validation | duplicate identifier | 1 |
| I/O | unreadable file or failed replacement | 1 |
| Success | command completed | 0 |

Unexpected programmer defects also exit 1, but they render `UNEXPECTED` rather than pretending to be user input errors.

## 4. Invariants worth defending

### Identifier invariant

Every session identifier is a positive safe integer. Identifiers are unique. `nextId` is greater than every existing identifier and remains below the point at which incrementing would cease to be safe.

### State invariant

State-specific fields agree with the discriminant. A completed session has start and completion times plus actual minutes. An abandoned session records whether work had begun. Planned and active sessions cannot contain terminal fields.

### Chronology invariant

Creation does not follow start. Start does not follow completion or abandonment. The program compares normalized UTC timestamps rather than arbitrary locale strings.

### Persistence invariant

A successfully loaded ledger has already crossed the unknown-data boundary. Domain code does not repeatedly revalidate storage shape. A successful save writes one canonical representation of the current typed value.

### Reporting invariant

Success output is emitted only after a mutating save resolves. Read-only commands never rewrite storage. Stable tab-separated output lets tests and shell tools inspect behavior without depending on object property enumeration.

## 5. Deliberate limitations

Course 1 keeps the persistence design honest and bounded. It does not provide:

- cross-process locking;
- crash-durable `fsync` protocols;
- schema migration beyond V1 recognition;
- transactional multi-file state;
- hostile-file peak-memory bounds;
- remote access control;
- concurrent writers.

These are not missing details concealed by a “production-ready” label. They are explicit future responsibilities. The capstone is complete for its declared single-user, local-file contract.

## 6. Final defense

You should be able to answer these questions without opening the source:

1. Why does TypeScript not remove the need for `decodeLedger`?
2. Which module is allowed to establish a legal state transition?
3. Why does a read-only command not call the clock?
4. What does the same-directory temporary file protect, and what does it not protect?
5. Why are command numbers parsed from a restricted decimal grammar before conversion?
6. Which evidence proves that success is not reported before persistence?
7. What changes would a `reopen` feature require across the architecture?
8. Which current design claim would fail first under concurrent writers?

If these answers depend on “because the code does it,” the architecture is not yet internalized. State the product requirement and then show how the code enforces it.

## 7. Command-by-command contract

### `plan`

```text
studyledger plan --topic <text> --minutes <integer>
```

The parser rejects missing, repeated, unknown, or malformed options. The domain trims the topic, rejects empty/control-character/oversized text, checks the planned-minute range, allocates exactly one ID, and uses one injected timestamp. Success is emitted after persistence.

### `start`

```text
studyledger start <id>
```

Only a planned session may start. The start timestamp cannot precede creation. The same ID and planning fields survive. Calling start on active or terminal state is a transition error, not a no-op.

### `complete`

```text
studyledger complete <id> --minutes <integer> [--note <text>]
```

Only active sessions may complete. Actual minutes have their own range. An omitted or whitespace-only note becomes null under the product policy. Completion cannot precede start.

### `abandon`

```text
studyledger abandon <id> --reason <text>
```

Planned and active sessions can be abandoned. The terminal value records `startedAt: null` or the real start timestamp so history is unambiguous. Completed and already abandoned states reject the transition.

### Read-only commands

`list`, `show`, `search`, and `summary` load and validate the ledger but do not call the clock or save. Listing is ID ordered. Search matches topic plus terminal note/reason under one explicit case policy. Summary separates planned from actual completed minutes.

## 8. Storage grammar

The root shape is exact:

```json
{
  "format": "STUDY_LEDGER_V1",
  "nextId": 3,
  "sessions": []
}
```

Each state has an exact property set. The decoder rejects unknown properties, duplicate IDs, invalid text, invalid numbers, invalid timestamps, impossible chronology, and `nextId` not greater than existing IDs. It accepts any source order but returns sessions in ID order and emits canonical formatted JSON.

Validation is dependency-aware. It can report unknown root keys and duplicate IDs together, but it does not attempt state chronology until required timestamp fields are valid.

## 9. Error and exit matrix

| Boundary | Stable code | Example | Exit |
|---|---|---|---:|
| command grammar | `COMMAND_INVALID` | missing `--minutes` | 2 |
| domain value | `DOMAIN_INVALID` | planned minutes above limit | 1 |
| lookup | `DOMAIN_MISSING` | unknown session ID | 1 |
| state transition | `DOMAIN_TRANSITION` | complete planned session | 1 |
| storage schema | `STORAGE_INVALID` | duplicate persisted ID | 1 |
| storage effect | `STORAGE_IO` | permission or rename failure | 1 |
| unexpected defect | `UNEXPECTED` | violated internal assumption | 1 |

Errors preserve causes where layers translate them. User-facing rendering avoids depending on complete operating-system wording.

## 10. Test inventory

The complete capstone includes twenty tests across six files:

- domain transition, identity, search, and summary behavior;
- command grammar and duplicate options;
- canonical encoding, round-trip, unknown properties, duplicates, and chronology;
- application effect order, clock use, and failed save behavior;
- missing/malformed storage in temporary directories;
- real multi-process CLI lifecycle and usage status.

A future extension should add evidence at the nearest affected boundary before adding a broad end-to-end test.

## 11. Review StudyLedger as a learner

Do not memorize its file layout. Reconstruct these decisions:

- `domain.ts` is free of Node imports because domain legality does not require a host API;
- `codec.ts` imports domain validators because persistence must establish the same invariants;
- `storage.ts` knows paths and promises but not commands;
- `app.ts` coordinates effects but receives them as dependencies;
- `main.ts` is the only process adapter;
- `render.ts` creates deterministic text and no effect;
- `index.ts` curates reusable exports.

Then challenge one decision. Could command parsing return a result union rather than throw? Could the repository be represented as one object instead of two functions? Could notes preserve empty string instead of null? A different answer is valid only when its consequences are carried through tests and storage.

## 12. Independent feature rubric

An independent feature is complete when:

1. the behavioral rule is written before code;
2. command syntax is unambiguous;
3. the domain transition/query is pure and tested;
4. unknown persisted data remains validated;
5. V1 compatibility is defended or migration is introduced;
6. output ordering remains deterministic;
7. application effect order is preserved;
8. process help and status remain correct;
9. no unrelated module gains authority;
10. the non-contracts remain honest.

The goal is not to add the largest feature. It is to prove that the architecture supports reasoned change.
