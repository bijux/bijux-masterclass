# StudyLedger

StudyLedger is the cumulative product for **Node.js and TypeScript Foundations**. It records planned study sessions, explicit state transitions, completed effort, abandoned work, and aggregate progress in one local JSON file.

The product exists to integrate the course’s ten mechanisms in one program whose boundaries remain visible:

```text
terminal arguments
       ↓
typed command
       ↓
domain transition
       ↓
validated ledger state
       ↓
canonical JSON
       ↓
asynchronous file replacement
```

It is intentionally built with Node’s standard library. Frameworks and schema libraries would reduce code, but they would hide the runtime/type boundary that Course 1 is designed to teach.

## Commands

```text
studyledger plan --topic <text> --minutes <integer>
studyledger start <id>
studyledger complete <id> --minutes <integer> [--note <text>]
studyledger abandon <id> --reason <text>
studyledger list [--status planned|active|completed|abandoned]
studyledger show <id>
studyledger search --query <text>
studyledger summary
studyledger help
studyledger version
```

Set `STUDY_LEDGER_FILE` to isolate a ledger. Otherwise the CLI uses `~/.studyledger.json`.

## Architectural boundaries

| Module | Responsibility |
|---|---|
| `command.ts` | Convert untrusted argument tokens into a typed `Command` |
| `domain.ts` | Own session validity and legal state transitions |
| `codec.ts` | Convert untrusted JSON into validated domain state and back |
| `storage.ts` | Own asynchronous file effects and replacement policy |
| `app.ts` | Coordinate one use case without owning parsing or persistence details |
| `render.ts` | Produce deterministic human-facing text |
| `main.ts` | Bind the application to the real process |

## Persistence contract

The storage root is:

```json
{
  "format": "STUDY_LEDGER_V1",
  "nextId": 2,
  "sessions": []
}
```

The decoder treats JSON as `unknown`, rejects extra fields, checks every state-specific field, rejects duplicate identifiers, validates chronology, and requires `nextId` to be greater than every existing identifier.

Saving writes a unique temporary file in the destination directory and renames it over the destination. This avoids exposing a partially written JSON document during ordinary single-process use. The course does not claim crash durability, cross-process locking, or adversarial filesystem safety; those belong to later systems courses.

## Verification

```bash
npm run typecheck
npm test
npm run demo
```

The test suite covers pure domain transitions, command parsing, unknown-data validation, asynchronous storage, orchestration behavior, and the real CLI process.
