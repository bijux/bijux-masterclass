# FlowLedger

FlowLedger is the cumulative product for **Node.js Streams, Filesystems, and Data Pipeline Architecture**. It processes NDJSON incrementally and makes byte representation, backpressure, validation, compression, child-process supervision, staged output, and terminal reporting part of one public contract.

## Commands

```text
flowledger inspect <input> [--gzip-input]
flowledger normalize <input> <output> [--gzip-input] [--gzip-output] [--replace]
flowledger filter <input> <output> --kind <kind> [--gzip-input] [--gzip-output] [--replace]
flowledger verify <input> --sha256 <hex>
flowledger through <input> <output> [--replace] -- <program> [argument...]
flowledger help
flowledger version
```

## Build and test

```bash
npm run typecheck
npm run build
npm test
npm run demo
```

## Source map

| File | Responsibility |
|---|---|
| `domain.ts` | FlowEvent validation and canonical encoding |
| `streams.ts` | byte taps, expansion bounds, incremental NDJSON decode, selection, and encoding |
| `pipeline.ts` | inspect, normalize/filter, gzip, digest, and verification orchestration |
| `transaction.ts` | stage creation, synchronization, destination policy, rename, and cleanup |
| `child.ts` | direct spawn, concurrent stdio, bounded stderr, child status, and publication coordination |
| `command.ts` | typed CLI grammar |
| `app.ts` | command-to-application routing |
| `render.ts` | deterministic help and operation reports |
| `errors.ts` | causal public error categories |
| `limits.ts` | semantic product limits |
| `main.ts` | process boundary and exit status |

## Core guarantees

- input chunk boundaries do not define record boundaries;
- malformed UTF-8, over-limit lines, invalid JSON, and invalid events are rejected before publication;
- high-water marks are not substituted for line, event, expansion, identifier, or stderr limits;
- source, canonical, and final-output byte domains have separate counts and digests;
- output is written to an exclusive same-directory stage and renamed only after the complete pipeline succeeds;
- a nonzero or signalled child cannot publish stdout;
- final reports are deterministic for the same logical input and options;
- every stream, file, stage, and child process has one lifecycle owner.

## Deliberate non-guarantees

FlowLedger does not claim authentication from SHA-256 alone, universal crash durability, adversarial filesystem race safety, cross-process writer exclusion, or atomic publication of several independent files.

Read the full [FlowLedger engineering guide](../course-book/capstone.md) before changing stage order, digest placement, limits, error categories, or publication behavior.

## Bounded representations

FlowLedger declares independent limits for raw source bytes, decompressed bytes, unfinished line bytes, event count, final output bytes, child stdout bytes, and retained child stderr. Stream high-water marks regulate queue pressure but do not replace these product limits. Successful transform reports name source, canonical, and final-output SHA-256 domains separately; successful child reports name input and output byte domains separately.
