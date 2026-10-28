# Module 05 — Hostile Input and File Handling

> **Program stage:** Course 3 of 6 — Defend the promise.

> **Central question:** How are hostile strings, numbers, paths, filenames, uploads, and serialized structures constrained at the correct boundary?

## Where this module fits

Harden semantic input, Unicode, filenames, paths, archives, serialization, and file transfer. You arrive from Module 04 with all earlier checkpoints still green. API 1.2 and its durable service behavior are fixed. This course adds controls derived from explicit threats; it does not redefine successful business outcomes or treat middleware configuration as proof of security. The result is the baseline for **Outbound HTTP, SSRF, and Webhook Integrity**.

## Learning outcomes

- Distinguish schema validation from semantic security validation.
- Reject traversal after decoding and normalization.
- Treat filenames as labels, never paths.
- Bound archive and upload expansion.
- Prevent SQL, command, template, and deserialization injection.

## Capstone result

Harden input parsing, Unicode, traversal, MIME, streaming upload, checksum, query, and error behavior.

A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.

## Core security model

### Driving question

> How does the service process attacker-controlled text, numbers, paths, files, and archives without changing interpretation, escaping boundaries, or exhausting resources?

Schema validation is one layer. Secure input processing also constrains bytes, encoding, normalization, semantics, interpreter boundaries, storage paths, cumulative resources, and cleanup after failure.

### 1. Layered validation

Byte, syntax, schema, semantic, authorization, and interpreter-safety checks answer different questions.

Normalize only by explicit domain rule; reject invisible or directional controls where they undermine review or equality.

A client filename is metadata. Storage keys are server-generated and paths are resolved below a fixed root.

Decode, normalize, resolve, and verify ancestry; reject absolute paths, traversal, symlinks, and platform-specific alternate forms.

Count bytes while reading, abort before exceeding the limit, compute digest incrementally, and never buffer an unbounded upload.

Write to a private staging file, validate integrity, publish without clobber, and clean up on every failure.

Limit member count, individual and cumulative size, expansion ratio, path types, and links—or refuse extraction entirely.

Use SQL parameters, no shell interpolation, safe templates, and explicit serializers; validation does not make string concatenation safe.

### Synthesis

Draw the capstone data flow and annotate where each concept is owned. Any concept with no owner becomes a Module 05 defect.

## Input crosses several interpreters

An OpenAPI or framework schema proves that a value has an expected syntactic shape. Security depends on what later interpreters do with that value: SQL planners, filesystems, shells, template engines, archive readers, URL parsers, image libraries, and downstream services. Validation must therefore be placed immediately before the interpretation whose assumptions it protects.

Use a staged model:

```text
raw bytes -> protocol parser -> schema validation -> semantic validation
          -> authorization -> interpreter-specific safe construction
```

Do not create one generic `sanitize()` function. Escaping for HTML does not make a SQL identifier safe; normalizing a filename does not make it a URL; removing `../` does not confine a filesystem path.

### Files are content, not paths supplied by the client

Treat an uploaded filename as optional display metadata. Generate storage keys on the server. For any path-like input, percent-decode once where the surrounding protocol requires it, reject control and bidirectional formatting characters, resolve against a fixed root, verify the resolved path remains beneath that root, and define symbolic-link behavior. Recheck at the operation boundary if an attacker can change the filesystem between validation and use.

Streaming limits must count actual bytes. Enforce per-file, per-request, per-tenant, and available-storage budgets while reading. Stage to a private location, compute the digest during the stream, verify declared checksum and media policy, then publish atomically. A failure or disconnect removes the staging object; an already-published object with the same digest is an idempotent result only if the bytes match.

Archives require cumulative policy before or during extraction: member count, total uncompressed bytes, per-member size, compression ratio, path confinement, link rejection, nesting depth, and accepted member kinds. Checking only the archive file size does not constrain expansion.

Unicode policy should be narrow and documented. Normalization can make visually equivalent labels compare consistently, but it can also change identifiers. Reject control and bidirectional override characters where they provide no legitimate value. Preserve the original value only if the display requirement is real and the output context handles it safely.

Parameter binding protects SQL values, not SQL structure. Sort columns, directions, table names, operators, and JSON-path expressions require fixed allowlists mapped to trusted fragments. The same rule applies to command-line flags and template names: pass data through typed APIs and never concatenate untrusted structure.

Error responses should identify the public field and rule without returning filesystem roots, SQL text, parser stack traces, antivirus output, or snippets of hostile content. Restricted events can record a bounded reason code and pseudonymous correlation data.

## Security requirements and standards

The course profile turns the mental model into enforceable requirements. `MUST` denotes a non-compensable course invariant; `SHOULD` requires a recorded exception.

1. The implementation MUST satisfy **Layered validation**: Byte, syntax, schema, semantic, authorization, and interpreter-safety checks answer different questions.
2. The implementation MUST satisfy **Canonical identifiers**: Normalize only by explicit domain rule; reject invisible or directional controls where they undermine review or equality.
3. The implementation MUST satisfy **Filename non-authority**: A client filename is metadata. Storage keys are server-generated and paths are resolved below a fixed root.
4. The implementation MUST satisfy **Path confinement**: Decode, normalize, resolve, and verify ancestry; reject absolute paths, traversal, symlinks, and platform-specific alternate forms.
5. The implementation MUST satisfy **Bounded streaming**: Count bytes while reading, abort before exceeding the limit, compute digest incrementally, and never buffer an unbounded upload.
6. The implementation MUST satisfy **Atomic publication**: Write to a private staging file, validate integrity, publish without clobber, and clean up on every failure.
7. The implementation MUST satisfy **Archive policy**: Limit member count, individual and cumulative size, expansion ratio, path types, and links—or refuse extraction entirely.
8. The implementation MUST satisfy **Interpreter separation**: Use SQL parameters, no shell interpolation, safe templates, and explicit serializers; validation does not make string concatenation safe.

## Worked attacks and defenses

The Hostile Input and File Handling cases are bounded course fixtures. Trace the attacker-controlled value through every interpreter, then identify the policy decision and smallest rejection evidence; do not target external systems.

### Attack 1 — Encoded traversal

A remote fixture or archive member uses percent-encoded `..` or mixed separators to escape the root.

### Attack 2 — Symlink escape

A path inside the root points to a file outside it and is followed during read or publication.

### Attack 3 — Unicode disguise

A filename contains bidirectional controls that render a dangerous extension misleadingly.

### Attack 4 — Decompression bomb

A tiny archive expands beyond memory, disk, or file-count budgets.

### Attack 5 — MIME confusion

Declared `text/csv` content is executable or binary data later served with unsafe headers.

### Attack 6 — SQL structure injection

A sort or filter field is concatenated into SQL despite value parameterization elsewhere.


## Python implementation

Use `pathlib.Path.resolve(strict=False)` plus ancestry checks, `os.open` flags or no-follow semantics where required, chunked hashing, exclusive publication, and `unicodedata` inspection. Keep SQL identifiers on a server-owned allowlist; parameterize values.

## TypeScript implementation

Use `node:path` resolution and relative checks, `fs.open` with exclusive/no-follow-capable patterns, streamed `Transform` byte counting, `crypto.createHash`, and allowlisted SQL fragments. Reject `__proto__`, `prototype`, and `constructor` recursively in untrusted objects.

## Failure patterns

For each pattern, explain why it can look reasonable, construct the smallest counterexample, and identify the missing authoritative boundary.

### 1. Checking only for the literal substring `../`.


### 2. Resolving a path once and then following a changed symlink later.


### 3. Using the client filename as the final path.


### 4. Checking `Content-Length` but not actual streamed bytes.


### 5. Extracting an archive before enforcing cumulative limits.


### 6. Using parameter binding for values but concatenating attacker-controlled sort columns.


## What you add to the capstone

### Objective

Process valid and hostile uploads, paths, filenames, Unicode, archives, and query controls through both tracks. Plant a decoded-traversal omission and an unbounded buffering implementation; capture escape/resource evidence and repair.

## Representative implementation

These are the smallest useful entry points for **Hostile Input and File Handling**.

### Python — `capstone/tracks/python-fastapi/src/api_security/input_security.py`

```python
BIDI_CONTROLS = frozenset(chr(x) for x in [0x061C, *range(0x202A, 0x202F), *range(0x2066, 0x206A)])


def validate_filename(value: str, *, max_length: int = 160) -> str:
    if not value or len(value) > max_length:
        raise SecurityControlError("invalid-filename", "filename length is invalid")
    if value in {".", ".."} or "/" in value or "\\" in value or "\x00" in value:
        raise SecurityControlError("invalid-filename", "filename contains a path or control delimiter")
    if any(ch in BIDI_CONTROLS or unicodedata.category(ch).startswith("C") for ch in value):
        raise SecurityControlError("invalid-filename", "filename contains an invisible control character")
    return value


def confined_path(root: Path, value: str, *, percent_decode: bool = True) -> Path:
    decoded = unquote(value) if percent_decode else value
    candidate = Path(decoded)
    if candidate.is_absolute():
        raise SecurityControlError("path-escape", "absolute paths are prohibited")
    root_resolved = root.resolve()
    resolved = (root_resolved / candidate).resolve(strict=False)
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise SecurityControlError("path-escape", "path escapes the configured root")
    return resolved


def reject_symlink(path: Path) -> None:
    current = path
    while True:
        if current.exists() and current.is_symlink():
            raise SecurityControlError("symlink-prohibited", "symbolic links are prohibited")
        if current.parent == current:
            return
        current = current.parent


@dataclass(frozen=True, slots=True)
class ArchiveMember:
    name: str
    size: int
    kind: str = "file"


def validate_archive_members(
    members: Sequence[ArchiveMember],
    *,
    max_members: int = 100,
    max_member_bytes: int = 10_000_000,
    max_total_bytes: int = 50_000_000,
) -> None:
    if len(members) > max_members:
        raise SecurityControlError("archive-limit", "archive member count exceeds the limit")
    total = 0
    for member in members:
        if member.kind != "file":
            raise SecurityControlError("archive-entry", "archive contains a prohibited entry type")
        validate_filename(Path(member.name).name)
        normalized = Path(member.name)
        if normalized.is_absolute() or ".." in normalized.parts:
            raise SecurityControlError("archive-path", "archive member path escapes the root")
        if member.size < 0 or member.size > max_member_bytes:
            raise SecurityControlError("archive-limit", "archive member size exceeds the limit")
        total += member.size
        if total > max_total_bytes:
            raise SecurityControlError("archive-limit", "archive expanded size exceeds the limit")
```

### TypeScript — `capstone/tracks/typescript-fastify/src/security/input-security.ts`

```typescript
import { isAbsolute, relative, resolve, sep } from "node:path";
import { SecurityControlError } from "./errors.js";

const BIDI = /[\u061c\u202a-\u202e\u2066-\u2069]/u;
const CONTROLS = /[\u0000-\u001f\u007f]/u;

export function validateFilename(value: string, maxLength = 160): string {
  if (value.length === 0 || value.length > maxLength || value === "." || value === ".." || value.includes("/") || value.includes("\\") || BIDI.test(value) || CONTROLS.test(value)) throw new SecurityControlError("invalid-filename", "filename is not accepted");
  return value;
}

export function confinedPath(root: string, input: string, percentDecode = true): string {
  let decoded: string;
  try { decoded = percentDecode ? decodeURIComponent(input) : input; }
  catch { throw new SecurityControlError("path-escape", "path encoding is invalid"); }
  if (isAbsolute(decoded)) throw new SecurityControlError("path-escape", "absolute paths are prohibited");
  const base = resolve(root); const candidate = resolve(base, decoded); const rel = relative(base, candidate);
  if (rel === ".." || rel.startsWith(`..${sep}`) || isAbsolute(rel)) throw new SecurityControlError("path-escape", "path escapes the configured root");
  return candidate;
}

export interface ArchiveMember { readonly name: string; readonly size: number; readonly kind?: string }
export function validateArchiveMembers(members: readonly ArchiveMember[], options: { maxMembers?: number; maxMemberBytes?: number; maxTotalBytes?: number } = {}): void {
  const maxMembers = options.maxMembers ?? 100; const maxMember = options.maxMemberBytes ?? 10_000_000; const maxTotal = options.maxTotalBytes ?? 50_000_000;
  if (members.length > maxMembers) throw new SecurityControlError("archive-limit", "archive member count exceeds the limit");
  let total = 0;
  for (const member of members) {
    if ((member.kind ?? "file") !== "file") throw new SecurityControlError("archive-entry", "archive contains a prohibited entry type");
    const normalized = member.name.replaceAll("\\", "/");
    if (normalized.startsWith("/") || normalized.split("/").includes("..")) throw new SecurityControlError("archive-path", "archive member path escapes the root");
    validateFilename(normalized.split("/").at(-1) ?? "");
    if (!Number.isSafeInteger(member.size) || member.size < 0 || member.size > maxMember) throw new SecurityControlError("archive-limit", "archive member size exceeds the limit");
    total += member.size; if (total > maxTotal) throw new SecurityControlError("archive-limit", "archive expanded size exceeds the limit");
  }
}
```

Compare the two tracks by this invariant: **decoding, normalization, path resolution, symlink policy, byte budgets, and archive budgets are applied in the correct order**. The intended implementation difference is: path and stream libraries differ; the final confined object and rejection cases must match.

## Module synthesis

The module answer to “How do valid-looking values become injection, traversal, confusion, or resource-exhaustion attacks after parsing?” is now executable in the capstone: A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.

## Next in the story

Module 06, [Outbound HTTP, SSRF, and Webhook Integrity](../module-06-outbound-http-ssrf-and-webhooks/index.md), asks: *How does the service call a user-chosen destination without becoming a network pivot or accepting forged delivery?* The current checkpoint must remain green while that new responsibility is added.
