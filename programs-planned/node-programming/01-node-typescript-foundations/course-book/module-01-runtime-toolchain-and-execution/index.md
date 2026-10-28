# Module 1 — Runtime, Toolchain, ESM, and the JavaScript/TypeScript Boundary

> **Question:** What runs, what is checked, what is emitted, and which file or package metadata controls each step?

## Why this comes first

A Node.js project contains several mechanisms that are often compressed into the word “JavaScript”: the ECMAScript language, the Node runtime, TypeScript’s static checker, the compiler’s emitted files, npm’s package metadata, the ESM resolver, and the operating-system process. When those mechanisms are not separated, failures are diagnosed at the wrong layer. A missing import extension is “a TypeScript problem”; malformed JSON is “type safe”; a globally installed compiler silently differs from the package; a successful build is treated as evidence that the program will run.

Course 1 begins by giving every mechanism a name and an observable responsibility.

## Outcomes

By the end of the module you can:

- trace a `.ts` file from source text to process behavior;
- distinguish syntax acceptance, type checking, emission, module resolution, and execution;
- explain why TypeScript types do not validate runtime input;
- configure a strict ESM package without relying on ambiguous defaults;
- use local package scripts rather than an accidental global toolchain;
- write one pure function, one public entry point, and one built-in Node test;
- identify which StudyLedger facts belong to package metadata, source types, runtime checks, and process behavior.

## 1. Four artifacts, not one program

Consider:

```ts
export function double(value: number): number {
  return value * 2;
}
```

There are at least four relevant artifacts:

1. **TypeScript source** — contains syntax erased before ordinary JavaScript execution.
2. **Static program** — the relationships TypeScript derives among declarations and expressions.
3. **Emitted JavaScript** — executable module text after type-only syntax is removed.
4. **Running process** — actual values, module effects, environment, streams, and exit status.

The annotation `: number` constrains TypeScript callers. It does not insert a runtime guard:

```ts
const untrusted: unknown = JSON.parse('"not a number"');

// An assertion changes the checker's belief; it does not change the value.
const claimed = untrusted as number;
console.log(double(claimed)); // NaN
```

The decisive error is not “TypeScript failed”. The program replaced evidence with an assertion. At runtime the value is still a string, multiplication coerces it, and the result is `NaN`.

Use the course’s first invariant:

> A fact about an external value becomes trustworthy only through a runtime check performed by an authority responsible for that boundary.

## 2. Node is the host, JavaScript is the executed language

ECMAScript specifies core language behavior: values, objects, functions, coercion, promises, and modules. Node hosts that language and supplies process-oriented APIs such as files, paths, terminals, timers, tests, child processes, and networking.

This distinction matters in code review:

```ts
import { readFile } from 'node:fs/promises';

const text = await readFile('settings.json', 'utf8');
const value = JSON.parse(text);
```

- `await`, strings, promises, and `JSON.parse` are language/runtime concepts.
- `node:fs/promises` is a Node API.
- path interpretation and file errors are operating-system conditioned.
- the static type of `value` should be treated as `unknown` at the application boundary, even though the historical declaration of `JSON.parse` is permissive.

A useful mental diagram is:

```text
ECMAScript semantics
        hosted by
Node.js runtime
        exposes
standard-library and process boundaries
```

TypeScript sits beside this execution path. It checks source relationships and emits JavaScript; it is not the host.

## 3. The canonical course route

The course uses an explicit compile route:

```text
src/*.ts
   │
   ├── TypeScript parse and static check
   │
   └── JavaScript emission into dist/
             │
             └── Node loads ESM and runs the process
```

Node 24 can strip erasable TypeScript syntax directly in supported cases. That is useful and covered as a platform capability, but it does not replace `tsc --noEmit` or a normal build. Type stripping removes syntax; it does not establish that the static program is valid.

A project script therefore separates checks:

```json
{
  "scripts": {
    "typecheck": "tsc -p tsconfig.json --noEmit",
    "build": "tsc -p tsconfig.json",
    "test": "npm run build && node --test dist/tests"
  }
}
```

Each command proves something different:

| Command | Establishes | Does not establish |
|---|---|---|
| `typecheck` | configured static relationships are accepted | emitted files run correctly |
| `build` | JavaScript and declarations can be emitted | runtime behavior is correct |
| `node --test` | selected executable behaviors satisfy tests | every input, platform, or timing is correct |

## 4. Package metadata controls interpretation

The course uses ECMAScript modules throughout:

```json
{
  "type": "module"
}
```

The field tells Node that `.js` files in the package are ESM. Being explicit avoids relying on syntax detection or inherited defaults.

TypeScript is configured for Node’s module rules:

```json
{
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext"
  }
}
```

A relative TypeScript import names the emitted JavaScript path:

```ts
import { parseDuration } from './duration.js';
```

Writing `./duration.ts` describes the source tree rather than the runtime module graph and is not the course convention. Writing `./duration` asks Node’s ESM resolver to perform extension search that it does not perform for relative imports.

Built-in modules use explicit `node:` specifiers:

```ts
import { test } from 'node:test';
import assert from 'node:assert/strict';
```

This makes the boundary visible and prevents a package name from being mistaken for the built-in API.

## 5. Strict configuration is a reasoning policy

The course base configuration enables more than `strict`:

```json
{
  "types": ["node"],
  "strict": true,
  "noUncheckedIndexedAccess": true,
  "exactOptionalPropertyTypes": true,
  "useUnknownInCatchVariables": true,
  "noImplicitReturns": true,
  "verbatimModuleSyntax": true
}
```

The explicit `types` list is part of the Node boundary. TypeScript 6 and 7 no longer assume that every installed `@types` package belongs in the global program; naming `node` makes the intended host declarations deliberate and keeps unrelated ambient packages out.

These options expose different weak assumptions:

- only the declared Node ambient types enter the program;
- indexing may produce `undefined`;
- an absent optional property is not automatically equivalent to a present property containing `undefined`;
- thrown values are not guaranteed to be `Error` objects;
- every function path must satisfy its return contract;
- type-only imports must be declared as type-only imports.

Do not memorize flags as a prestige checklist. For each option, state the invalid assumption it makes visible.

## 6. Local tools and reproducible commands

A command named `tsc` found on the shell path may not be the version declared by the package. The package owns its toolchain:

```bash
npm install
npm run typecheck
```

npm adds `node_modules/.bin` to package scripts, so `tsc` resolves to the local dependency. The `engines` field documents the supported Node range; `.nvmrc` helps a version manager select it; `packageManager` records the intended npm line.

These files are related but not interchangeable:

| File or field | Responsibility |
|---|---|
| `.nvmrc` | version-manager convenience |
| `engines.node` | supported runtime contract or warning policy |
| `packageManager` | intended package-manager version |
| `devDependencies` | project-local build and type tools |
| `package-lock.json` | resolved dependency graph after installation |

A lockfile belongs in a real application. The source course does not fabricate a lockfile without performing the corresponding registry resolution; generate and commit it when installing from the configured registry.

## 7. Tests are executable specifications from Day 1

A first function can already have a meaningful contract:

```ts
export interface RuntimeVersion {
  readonly major: number;
  readonly minor: number;
  readonly patch: number;
}

export function parseNodeVersion(raw: string): RuntimeVersion {
  const match = /^v(\d+)\.(\d+)\.(\d+)$/.exec(raw);
  if (match === null) {
    throw new Error(`invalid Node version: ${raw}`);
  }

  const [, majorText, minorText, patchText] = match;
  return {
    major: Number(majorText),
    minor: Number(minorText),
    patch: Number(patchText),
  };
}
```

A test imports the public function:

```ts
import test from 'node:test';
import assert from 'node:assert/strict';
import { parseNodeVersion } from '../src/index.js';

test('parses a complete Node version', () => {
  assert.deepEqual(parseNodeVersion('v24.19.0'), {
    major: 24,
    minor: 19,
    patch: 0,
  });
});
```

The invalid-input test matters as much as the successful example. It proves the parser does not accept partial versions or silently produce `NaN`.

## 8. StudyLedger increment

Create the package and its first boundary:

```text
capstone/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   └── main.ts
└── tests/
```

Implement:

- a `VERSION` constant;
- a pure `renderHelp()` function;
- a binary that recognizes only `help` and `version`;
- tests importing the library rather than reaching into private modules.

Do not add persistence, time, or session state yet. Day 1 proves that package interpretation, checking, emission, imports, tests, and process output agree.

## 9. Common wrong models

### “TypeScript runs the program”

TypeScript checks and may emit. JavaScript runs in Node.

### “A type assertion validates a value”

An assertion suppresses a static objection. It inserts no runtime evidence.

### “The import works in my editor, so Node can load it”

Editor resolution and runtime ESM resolution can differ. Use NodeNext and emitted `.js` specifiers.

### “The build passed, so the CLI works”

Emission does not exercise files, process arguments, streams, or exit status.

### “Strict mode makes runtime errors impossible”

Strict checking narrows a class of static mistakes. External data, effects, timing, and incorrect declarations remain runtime concerns.

## 10. Trace one command through every authority

Consider the future command:

```text
studyledger plan --topic "Narrowing" --minutes 35
```

A beginner often describes this as “TypeScript runs the CLI.” That sentence hides every useful diagnostic boundary. A more accurate trace is:

1. the operating system starts a Node process with an argument vector;
2. Node resolves the emitted ESM entry file under package metadata;
3. the entry file reads `process.argv` and hands ordinary strings to the command parser;
4. TypeScript has already checked the source relationships, but its types are absent now;
5. the parser validates option grammar and converts the minutes token;
6. the domain layer constructs a legal planned session;
7. the storage layer encodes the new ledger and performs asynchronous file effects;
8. the process adapter writes success only after the save promise fulfills.

This trace gives each failure an owner. If `--minutes` is missing, the command grammar failed. If the existing file is malformed, the storage boundary failed. If the import path lacks `.js`, module resolution failed before command parsing. If success prints before the save settles, application orchestration failed even though every individual function may type-check.

Use a phase table when diagnosis is unclear:

| Phase | Input | Output | Typical evidence |
|---|---|---|---|
| package selection | directory and `package.json` | module interpretation | `node` process test |
| TypeScript check | `.ts` graph and `tsconfig` | diagnostics | `tsc --noEmit` |
| emission | accepted source | `.js`, maps, declarations | build artifact inspection |
| ESM resolution | import specifiers | loaded module graph | direct Node execution |
| application boundary | argument strings | typed command | parser unit tests |
| domain boundary | command and ledger | candidate ledger | pure transition tests |
| effect boundary | candidate and path | persisted bytes | temporary-directory test |

### Resolver failures are not interchangeable

Three similar-looking import defects have different causes:

```ts
import { parse } from './parser';     // runtime extension missing
import { parse } from './parser.ts';  // source path named, not emitted path
import type { Parser } from './parser.js'; // correct when only the type is needed
```

Under direct Node ESM, the first asks the runtime to perform extension search it does not perform. The second may be accepted only under special compiler options and points at a file absent from the emitted graph. The third correctly states that the dependency is static only and that the runtime graph contains no import for it.

### Native TypeScript execution is a different tool

Modern Node releases can execute many `.ts` files by stripping erasable type syntax. That capability is useful for small scripts and development workflows. It does not make the type checker part of Node, and it does not support every syntax that requires transformation. The course therefore keeps three routes separate:

```text
tsc --noEmit       static acceptance

tsc                configured emission

node dist/main.js  runtime behavior
```

Running source directly may be an additional convenience route, but it cannot replace the first command. A source file can be executable after stripping and still contain a type error; conversely, a valid static program can depend on module or platform behavior that fails at runtime.

## 11. Configuration options as exposed assumptions

A strict configuration is valuable only when you can name the assumption exposed by each option. For example:

```ts
const rows: string[] = [];
console.log(rows[0].toUpperCase());
```

Without `noUncheckedIndexedAccess`, the static type of `rows[0]` is commonly treated as `string`, although the runtime value is `undefined`. The option does not make arrays safer by itself. It forces the program to establish non-emptiness locally.

Likewise, `exactOptionalPropertyTypes` separates these representations:

```ts
interface Result {
  note?: string;
}

const absent: Result = {};
// const presentUndefined: Result = { note: undefined }; // rejected
```

That distinction matters when object keys are serialized, enumerated, merged, or checked with `in`. An option is therefore a policy about which weak assumptions deserve friction during development.

## 12. Toolchain ownership and drift

A project that invokes a global `tsc` has delegated its static semantics to the developer’s machine. Two people can run the same command name and receive different diagnostics or emission. The package must own the compiler version and the command that invokes it.

The baseline files form one contract:

```text
.nvmrc             selected Node line
engines.node        supported runtime range
packageManager      intended npm version
package.json        local TypeScript and Node declarations
tsconfig.base.json  static and emission policy
```

No single file enforces all the others. CI should report the actual versions before proof. A lockfile records resolved packages after a real installation; inventing one without registry resolution would be less trustworthy than omitting it and stating the open boundary.

### Decision procedure

When a first-run failure occurs, ask in this order:

1. Did the intended local executable run?
2. Did the intended configuration load?
3. Was the source accepted or rejected statically?
4. Did emission create the files named by imports and scripts?
5. Did Node interpret those files as ESM?
6. Did runtime input satisfy the assumptions types could not prove?

That order prevents “fixes” such as adding assertions to a module-resolution error or changing compiler flags to conceal malformed external data.

## Practice sequence

1. Complete the [workbook](workbook.md) without running the first prediction set.
2. Build [Runtime Report](../../labs/module-01-runtime-report/README.md).
3. Implement the StudyLedger Day 1 increment.
4. Compare your package graph with the chapter’s four-artifact model.
5. Read the [reasoned solutions](solutions.md) only after recording your predictions.

## Ready to continue

Continue when you can explain which artifact or mechanism owns each of these: a type error, an import-not-found error, malformed JSON, a thrown file error, a failing assertion, and a nonzero process exit.

Next: [Module 2 — Values, Coercion, Equality, Control Flow, and Invariants](../module-02-values-coercion-equality-and-control/index.md)
