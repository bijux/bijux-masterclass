# Course 1 Reference Desk

This reference condenses the mechanisms used throughout the course. It is not a substitute for the explanatory chapters. Use it while building after the mental model is established.

## 1. Runtime and static layers

| Layer | Owns | Does not own |
|---|---|---|
| ECMAScript | JavaScript values, operators, objects, functions, promises, modules | Node files, process APIs, TypeScript checks |
| Node.js | host APIs, ESM loading, processes, files, timers, tests | static type proof |
| TypeScript | source analysis, diagnostics, emission | runtime validation or execution |
| npm | dependency installation, scripts, package metadata workflows | JavaScript semantics |
| operating system | files, paths, process creation, permissions, clocks | application domain policy |

Canonical route:

```bash
npm install
npm run typecheck
npm run build
npm test
```

## 2. Strict configuration used by the course

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "useUnknownInCatchVariables": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "verbatimModuleSyntax": true
  }
}
```

Interpret each option by the weak assumption it exposes. Do not disable an option to silence a design problem without first naming that assumption.

## 3. Primitive categories

```text
undefined
null
boolean
number
bigint
string
symbol
```

Objects and functions have identity. Arrays, maps, sets, dates, regexes, errors, promises, buffers, and module namespace objects are object values.

Useful number checks:

```ts
Number.isFinite(value)
Number.isInteger(value)
Number.isSafeInteger(value)
Number.isNaN(value)
```

`typeof null` is historically `'object'`; always exclude null when checking record-like data.

## 4. Conversion and defaults

| Expression | Policy |
|---|---|
| `Number(raw)` | broad JavaScript numeric conversion |
| `parseInt(raw, 10)` | parses a valid prefix, not a complete grammar |
| `Boolean(value)` | truthiness conversion |
| `left || right` | choose right for any falsy left operand |
| `left ?? right` | choose right only for null or undefined |
| `value?.field` | avoid nullish property traversal; result may still be absent/invalid |

Canonical positive decimal:

```ts
if (!/^(0|[1-9]\d*)$/u.test(raw)) throw new Error('invalid decimal');
const value = Number(raw);
if (!Number.isSafeInteger(value) || value <= 0) throw new Error('invalid range');
```

## 5. Equality

| Relation | Important behavior |
|---|---|
| `===` | no coercion; `NaN` differs from itself; `0` equals `-0` |
| `Object.is` | `NaN` equals itself; `0` differs from `-0` |
| Map/Set key equality | SameValueZero: `NaN` matches; signed zeros match |
| object `===` | identity, not structural equality |
| text matching | define normalization, case, locale, and substring/exact policy |

## 6. Strings

```ts
text.length              // UTF-16 code units
[...text].length         // Unicode code points
Buffer.byteLength(text)  // UTF-8 bytes under default encoding
text.normalize('NFC')    // one normalization policy
```

User-perceived grapheme clusters may differ from all three counts.

## 7. Function forms

```ts
function named(value: number): number { return value * 2; }
const expression = function (value: number): number { return value * 2; };
const arrow = (value: number): number => value * 2;
```

Callable contract checklist:

```text
parameters
return
receiver / this
timing
call count
order
retention
concurrency
failure
```

Explicit receiver:

```ts
function read(this: { value: number }): number {
  return this.value;
}
```

## 8. Objects and identity

```ts
const alias = original;       // same object
const shallow = { ...original }; // new outer object, nested references shared
const arrayCopy = [...source];    // new array, element references shared
```

Targeted update:

```ts
const updated = {
  ...item,
  supplier: { ...item.supplier, email },
};
```

`readonly` restricts writes through a static view. `Object.freeze` is shallow at runtime.

## 9. Discriminated unions

```ts
type Result =
  | { readonly kind: 'ok'; readonly value: string }
  | { readonly kind: 'error'; readonly message: string };

function render(result: Result): string {
  switch (result.kind) {
    case 'ok': return result.value;
    case 'error': return `error: ${result.message}`;
  }
}
```

Exhaustiveness helper:

```ts
function assertNever(value: never): never {
  throw new Error(`unexpected value: ${JSON.stringify(value)}`);
}
```

## 10. Unknown data guards

```ts
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
```

A predicate is trusted by the checker; test it like parser code. Build trusted values from checked fields rather than casting the original object.

## 11. Optional properties

```ts
interface Note {
  readonly text?: string; // absent or a string under exact optional types
}
```

If explicit undefined is meaningful, declare it:

```ts
readonly text: string | undefined;
```

Omission and present-undefined differ under enumeration, `in`, spread, and JSON behavior.

## 12. Collection selection

| Collection | Strength |
|---|---|
| `Array<T>` | stable sequence and duplicate values |
| `Map<K,V>` | key/value relation with arbitrary keys and insertion order |
| `Set<T>` | unique membership with insertion order |
| object/interface | known property vocabulary and record shape |

Common array adapters:

```ts
map      one output per visited input
filter   subset of source values
flatMap  zero or more outputs per input
find     first match or undefined
some     any match, short-circuit
 every   all match, short-circuit
reduce   explicit accumulator transition
```

`sort` mutates. Use a copy or `toSorted` when source identity must remain unchanged.

## 13. Useful generic relationships

```ts
function get<T extends object, K extends keyof T>(value: T, key: K): T[K] {
  return value[key];
}

function first<T>(values: readonly T[], accept: (value: T) => boolean): T | undefined {
  return values.find(accept);
}
```

A generic parameter should connect at least two meaningful positions or constraints. `function parse<T>(text: string): T` cannot establish arbitrary T.

## 14. ESM imports and exports

```ts
import { parseCommand } from './command.js';
import type { Command } from './command.js';
import { readFile } from 'node:fs/promises';

export { parseCommand } from './command.js';
export type { Command } from './command.js';
```

Relative ESM imports name emitted `.js` files. Avoid hidden import-time effects. Curate public exports.

## 15. Errors and causes

```ts
try {
  return await operation();
} catch (error: unknown) {
  throw new StorageError('cannot load ledger', { cause: error });
}
```

Stable error categories belong at product boundaries. Do not assume thrown values are Error objects.

Validation result:

```ts
type ValidationResult<T> =
  | { readonly ok: true; readonly value: T }
  | { readonly ok: false; readonly issues: readonly Issue[] };
```

## 16. JSON trust boundary

```ts
const parsed: unknown = JSON.parse(text);
```

Validation order:

```text
syntax → root shape/version → fields → state variant → cross-field invariants → trusted value
```

Unknown keys, duplicate IDs, ordering, and format compatibility are product policies, not automatic JSON properties.

## 17. Promises

```ts
async function load(): Promise<string> { /* ... */ }
const value = await load();
const values = await Promise.all(inputs.map(loadOne));
```

Every started promise needs an observer. `void promise` discards the value; it does not make rejection safe.

Sequential:

```ts
for (const item of items) await save(item);
```

Concurrent start with aggregate ownership:

```ts
await Promise.all(items.map((item) => save(item)));
```

## 18. Basic scheduling

```ts
console.log('sync');
Promise.resolve().then(() => console.log('promise'));
setTimeout(() => console.log('timer'), 0);
```

For this simple setup: synchronous output, then promise reaction, then timer. Do not infer universal timer/I/O ordering.

## 19. CLI parsing

```ts
import { parseArgs } from 'node:util';

const parsed = parseArgs({
  args,
  options: { minutes: { type: 'string' } },
  allowPositionals: true,
  strict: true,
  tokens: true,
});
```

The application still owns duplicate options, required fields, domain conversion, positionals, help, and exit policy.

## 20. Filesystem promises

```ts
import { readFile, writeFile, rename } from 'node:fs/promises';
```

Inspect `NodeJS.ErrnoException.code` only after a safe error check. Missing file, malformed file, permission failure, and failed replacement are different outcomes.

## 21. Built-in tests

```ts
import test from 'node:test';
import assert from 'node:assert/strict';

test('names the behavior', async () => {
  await assert.rejects(() => operation(), /context/u);
});
```

Use temporary directories for real file boundaries and child processes for streams/status.

## 22. StudyLedger exit policy

```text
0  successful command
1  domain, validation, storage, or unexpected failure
2  usage/command grammar failure
```

Success output follows successful persistence for mutating commands.

## 23. Diagnostic sequence

When a Node/TypeScript program fails:

1. confirm local Node, npm, and compiler versions;
2. confirm package and compiler configuration;
3. classify static, emission, resolution, runtime, and design phase;
4. inspect actual runtime values rather than asserted types;
5. identify identity, mutation, promise, and effect ownership;
6. reproduce at the nearest observable boundary;
7. repair the requirement, not only the symptom.

## 24. Runtime/checker diagnostic matrix

Start with the observed artifact rather than the nearest-looking source line.

| Observation | First authority to inspect | Typical evidence |
|---|---|---|
| editor shows a type error | selected TypeScript project | effective config, local compiler version, complete diagnostic |
| build emits nothing | checker or emitter | `noEmit`, project references, output path, compiler exit status |
| Node cannot load a module | ESM resolver | emitted specifier, extension, package `type`, exports map, actual file |
| import exists but value is unavailable | linking/evaluation graph | named/default export, type-only import, cycle, initialization order |
| value has an impossible shape | runtime boundary | raw argument, parsed JSON, assertion, validation path |
| file remains old after “success” | async/effect ordering | awaited save, error propagation, success-render timing |
| process test hangs | lifecycle ownership | open handles, unawaited work, inherited stdio, child exit observation |

A single failure can cross several rows. For example, an extensionless import may be accepted by one editor configuration, emitted unchanged, and rejected by Node. The repair is not “make the editor quiet”; it is to make the source, selected checker, emitted graph, and runtime resolver agree.

## 25. Numeric boundary recipe

For a textual integer policy, write the stages explicitly:

```text
1. accepted textual grammar
2. conversion operation
3. finite/integer/safe-integer checks
4. sign and range checks
5. trusted domain constructor
```

Example policy for positive study minutes:

```ts
const DECIMAL_INTEGER = /^(?:0|[1-9]\d*)$/u;

export function parsePositiveMinutes(token: string): number {
  if (!DECIMAL_INTEGER.test(token)) {
    throw new RangeError('minutes must be a base-10 integer');
  }

  const value = Number(token);
  if (!Number.isSafeInteger(value) || value <= 0) {
    throw new RangeError('minutes must be a positive safe integer');
  }

  return value;
}
```

The regular expression defines accepted text. `Number` performs conversion. `Number.isSafeInteger` and the range check establish the domain invariant. Removing any stage changes the language accepted by the product.

## 26. Identity and immutable-update recipe

Before editing nested state, answer:

1. Which bindings refer to the same outer object?
2. Which nested arrays or objects are shared?
3. Which path must change?
4. Which untouched identities should remain shared?
5. Can validation fail before any publication?

A path-local update generally has this shape:

```ts
const index = inventory.items.findIndex((item) => item.id === id);
if (index < 0) throw new Error(`unknown item: ${id}`);

const previous = inventory.items[index];
if (previous === undefined) throw new Error('index invariant violated');

const nextStock = previous.stock + delta;
if (!Number.isSafeInteger(nextStock) || nextStock < 0) {
  throw new RangeError('invalid resulting stock');
}

const nextItems = inventory.items.map((item, position) =>
  position === index ? { ...item, stock: nextStock } : item,
);

return { ...inventory, items: nextItems };
```

The candidate is fully validated before return. Untouched item identities remain shared; the changed item, array, and outer inventory receive new identities.

## 27. Discriminated-union recipe

Use one literal field to select a state and put state-specific data inside the corresponding member:

```ts
type Session =
  | { readonly status: 'planned'; readonly id: number; readonly topic: string }
  | { readonly status: 'active'; readonly id: number; readonly topic: string; readonly startedAt: string }
  | { readonly status: 'completed'; readonly id: number; readonly topic: string; readonly actualMinutes: number };
```

Then keep operations narrow:

```ts
function complete(session: Extract<Session, { status: 'active' }>, minutes: number): Session {
  return { status: 'completed', id: session.id, topic: session.topic, actualMinutes: minutes };
}
```

The type relationship helps trusted code. An external object still needs runtime checks for status, common fields, and state-specific fields before it becomes a `Session`.

## 28. Unknown-data validation recipe

A reliable decoder follows dependency order:

```text
text syntax
    ↓
non-null object shape
    ↓
format/version marker
    ↓
required and optional keys
    ↓
primitive field types
    ↓
field-domain constraints
    ↓
cross-field invariants
    ↓
fresh trusted value
```

Collect independent issues only when later checks do not depend on earlier success. Do not report “field must be positive” when the field is absent, because the second issue depends on a value that does not exist.

Use paths such as `sessions[3].actualMinutes` so that diagnostics remain useful after the object grows. Reject unknown keys under a strict persistence format; otherwise misspellings silently disappear during canonical re-encoding.

## 29. Promise ownership recipe

For every operation that returns a promise, name:

- who starts it;
- who awaits or returns it;
- where rejection becomes product failure;
- whether sibling work has already started;
- what cancellation can and cannot stop;
- which output is allowed before completion.

Sequential ownership:

```ts
for (const path of paths) {
  results.push(await inspect(path));
}
```

Concurrent start with aggregate ownership:

```ts
const pending = paths.map((path) => inspect(path));
const results = await Promise.all(pending);
```

These have different start timing and failure behavior. Neither is automatically superior. A detached promise is acceptable only when its lifecycle, rejection handling, and shutdown behavior are separately owned.

## 30. ESM package checklist

For a strict ESM package, verify:

```text
package.json:        "type": "module"
tsconfig:            NodeNext module and resolution
relative source:     explicit .js runtime specifier
runtime import:      ordinary import
static-only import:  import type
public entry:        deliberate exports only
top-level work:      no accidental I/O or environment capture
```

Do not infer public API from which source files can be reached by relative paths. Package `exports`, documented entry points, and supported types define the contract. Internal files may change without compatibility promises.

## 31. Error translation checklist

Translate an error only when crossing an authority boundary. A useful wrapper adds:

- the failed operation;
- the relevant resource or identifier;
- a stable product-level category;
- the original cause when it is an `Error`;
- no fabricated claim about what completed.

Avoid converting every failure to a string early. Structured errors support process rendering, tests, retry policy, and causal inspection. At the process edge, render a stable message and set status; do not leak platform-specific stacks by default.

## 32. Test-boundary matrix

| Claim | Strongest nearby evidence |
|---|---|
| pure transition preserves previous state | unit test with value and identity assertions |
| decoder rejects malformed external data | table of hostile unknown values and path-aware issues |
| save is awaited before success | application test with a controllable rejecting/delayed fake |
| storage round-trips through real files | temporary-directory integration test |
| ESM entry and exit status work | child-process test against emitted JavaScript |
| public package surface remains curated | test importing only the documented entry and metadata review |
| asynchronous ordering is deterministic where promised | delayed fakes plus stable final-order assertions |

A test is evidence for a named claim, not a general certificate. The closest possible test is usually easiest to diagnose; the furthest necessary test catches boundary mismatches that pure tests cannot observe.

## 33. CLI boundary recipe

Treat the command line as a token grammar, not as a collection of convenient string lookups.

A parser should decide:

- which positionals exist and in which order;
- which options are flags and which require values;
- whether an option may repeat;
- whether unknown options are rejected;
- how `--` terminates option parsing;
- which conversions and domain checks follow syntax parsing;
- whether help and version bypass storage and other effects.

A robust route is:

```text
argv tokens
    ↓
syntactic parse
    ↓
command-specific required/duplicate checks
    ↓
text-to-value conversion
    ↓
domain validation
    ↓
typed Command
```

Keep parsing separate from execution. This makes a malformed command incapable of partially mutating state and lets parser tests run without touching files or process globals.

## 34. Persistence boundary recipe

A persistence module should answer four separate questions:

1. **What does missing mean?** A named first-run policy may return empty state for `ENOENT`; other failures should remain failures.
2. **What does valid mean?** Decode from text through JSON syntax, unknown-data validation, and domain construction.
3. **When is new state visible?** A same-directory temporary file followed by rename narrows the partial-write window for ordinary single-process use.
4. **What is not promised?** Crash durability, concurrent-writer isolation, advisory locking, hostile symlink defense, and cross-filesystem behavior require stronger mechanisms.

Preserve a candidate model: load into a new value, validate it completely, and publish it only after success. The existing in-memory state should not become half decoded because one later record is malformed.

## 35. Strict-option interpretation

Several course compiler options encode specific reasoning policies:

- `strict` enables the main family of strict checks; it is a baseline, not a proof certificate.
- `noUncheckedIndexedAccess` makes indexed reads include absence when the checker cannot prove the key exists.
- `exactOptionalPropertyTypes` distinguishes an absent property from a present property whose value is `undefined`.
- `useUnknownInCatchVariables` prevents thrown values from being trusted as `Error` without narrowing.
- `noImplicitOverride` makes class override intent explicit when classes appear in later courses.
- `verbatimModuleSyntax` keeps type-only and runtime imports honest under ESM emission.

Do not enable a flag merely because it is “stricter.” Understand which hidden assumption it exposes and repair the code at that boundary.

## 36. Final pre-debug questions

Before changing code, ask:

1. What exact artifact failed: source check, emission, module load, value conversion, domain transition, I/O, or process contract?
2. What was the actual runtime value, including `undefined`, `null`, `NaN`, alias identity, or rejected promise?
3. Which module or function had authority to validate, mutate, persist, or render it?
4. Which claim was made too early or too broadly?
5. What smallest experiment distinguishes the competing explanations?
6. What regression test would fail before the principled repair and pass after it?

This sequence is slower than random editing for the first minute and much faster over the next hour.


### Node ambient types under TypeScript 7

A Node project should state its ambient host types explicitly:

```json
{
  "compilerOptions": {
    "types": ["node"]
  }
}
```

This does not import runtime code. It tells the checker which global declaration package belongs to the program. Imports such as `node:fs/promises` still name the actual runtime module. A missing `types` entry can therefore look like a module or global-name failure even when the JavaScript runtime itself provides the API.
