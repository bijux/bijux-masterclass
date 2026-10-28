# Module 27 — Node ESM Packages, Exports, and Consumer Contracts

> **Question:** Which files and names are truly public when Node, TypeScript, package metadata, declarations, and downstream importers all participate in resolution?

## Why this comes now

Module 26 established declarations as a public artifact. Declarations do not choose how a consumer reaches that artifact. Node.js resolves a runtime module. TypeScript resolves source and declarations under a configured host model. npm installs a package tree. `package.json` states module format and supported entry points. These systems must agree.

A library can type-check internally and still fail for consumers because:

- emitted relative imports lack required extensions;
- `exports` points JavaScript and declarations at different APIs;
- internal files are accidentally reachable and become de facto public;
- a `types` entry points at stale declarations;
- CommonJS and ESM load separate module instances;
- a default export is declared but named exports execute;
- tests import source files instead of the package name;
- package files omit runtime or declaration artifacts.

This module defines the package boundary that SchemaKit will publish.

## Outcomes

By the end of the module, you can:

- explain the roles of `type`, `main`, `exports`, `imports`, and declaration metadata;
- trace an ESM import through TypeScript checking, emission, and Node execution;
- use explicit `.js` relative specifiers in NodeNext TypeScript source;
- separate type-only imports from runtime edges;
- design subpath exports with corresponding runtime and declaration artifacts;
- explain why introducing `exports` can be breaking;
- reject accidental deep imports and hidden runtime side effects;
- avoid the dual-package hazard by choosing an explicit module-format policy;
- test the installed or built package as a consumer rather than only its source graph.

## 1. Package metadata participates in execution

A package is not only a directory of JavaScript. `package.json` changes how specifiers are interpreted.

```json
{
  "name": "@example/schemakit",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  }
}
```

`"type": "module"` makes `.js` files in the package ESM unless a nearer package boundary says otherwise. `exports` defines supported package-name entry points and encapsulates undeclared subpaths for normal package resolution.

The `types` condition is interpreted by TypeScript tooling; Node selects a runtime condition such as `import`. Both entries must describe the same public surface.

## 2. Relative ESM specifiers name emitted files

In NodeNext TypeScript source:

```ts
import { parse } from './parser.js';
```

The source file may be `parser.ts`, but the runtime file after emission is `parser.js`. The specifier describes the runtime graph. TypeScript resolves it back to source during checking.

An extensionless import that works in a bundler or older CommonJS environment may fail under Node ESM.

```ts
// Avoid for direct Node ESM execution:
// import { parse } from './parser';
```

Course 3 uses one direct-Node ESM model instead of hiding differences behind a bundler.

## 3. Type-only imports do not create runtime edges

```ts
import type { Schema } from './core.js';
import { createSchema } from './core.js';
```

With `verbatimModuleSyntax`, type-only intent remains explicit. The `Schema` import is erased; `createSchema` remains.

This distinction affects:

- circular runtime dependencies;
- module initialization order;
- side effects;
- package graph size;
- consumer compatibility.

Do not convert a runtime import to `import type` merely to silence a cycle. Confirm that the imported name is truly erased and move shared runtime authority if necessary.

## 4. `exports` defines a supported public surface

Without `exports`, consumers may deep-import any installed path they can guess:

```ts
import { helper } from '@example/schemakit/dist/internal/helper.js';
```

Once consumers depend on that path, reorganizing internals can break them. An explicit export map prevents normal access to undeclared paths:

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./json": {
      "types": "./dist/json.d.ts",
      "import": "./dist/json.js"
    },
    "./testing": {
      "types": "./dist/testing.d.ts",
      "import": "./dist/testing.js"
    }
  }
}
```

This is SchemaKit's public package surface. Internal modules remain internal even if included in the tarball.

## 5. Adding `exports` can break existing users

If a previous package allowed:

```ts
import '@example/package/lib/parser.js';
```

and a new `exports` map omits that path, the import stops resolving. Encapsulation is valuable, but introducing it to an existing package requires:

- inventory of historical deep imports;
- compatibility aliases or a major release;
- migration instructions;
- tests for documented paths;
- deliberate handling of `package.json` access if consumers relied on it.

Package boundary changes are compatibility changes even when runtime functions are untouched.

## 6. Condition order and agreement

Conditional exports are evaluated according to object key order for recognized conditions. Put specific conditions before broad fallbacks and keep the tree simple.

For an ESM-only TypeScript package, prefer one runtime format unless CommonJS support is a real product requirement. A complex map with `import`, `require`, `node`, `default`, browser conditions, and several declaration trees creates a testing matrix that must be owned.

SchemaKit chooses:

- ESM only;
- supported Node LTS range stated in `engines`;
- one declaration tree;
- explicit main, JSON, and testing subpaths;
- no default export;
- no wildcard export of internals.

## 7. The dual-package hazard

Publishing CommonJS and ESM versions of a stateful package can cause one application to load two distinct module instances. Singleton registries, class identities, symbols, caches, and `instanceof` checks can then diverge.

Possible strategies include:

- ESM-only publication;
- one shared underlying CommonJS state with an ESM wrapper;
- stateless APIs;
- carefully tested conditional exports.

Course 3 chooses ESM-only because the educational goal is a precise package contract, not maximum historical compatibility.

## 8. `main`, `types`, and `exports`

`main` is an older single-entry runtime field. `types` or `typings` traditionally points to a root declaration. `exports` can define multiple runtime entry points and encapsulation. Modern TypeScript can use a `types` condition per export.

When `exports` is present, treat it as authoritative for supported package-name imports. Keep any root `types` field aligned for tools that consult it, but do not publish conflicting trees.

A package review should compare:

| Specifier | Runtime target | Declaration target | Test |
|---|---|---|---|
| package root | `dist/index.js` | `dist/index.d.ts` | public consumer |
| `/json` | `dist/json.js` | `dist/json.d.ts` | JSON consumer |
| `/testing` | `dist/testing.js` | `dist/testing.d.ts` | test-only consumer |
| internal path | unavailable | unavailable | negative resolution |

## 9. Self-reference

A package can import itself by its own name when `exports` is configured. This can test public boundaries internally:

```ts
import { string } from '@example/schemakit';
```

However, build order matters because the export target may point to `dist` that does not yet exist. Consumer fixtures usually run after build. Source files should generally use relative internal imports rather than routing every internal edge through the public package boundary.

Use self-reference in dedicated consumer tests, not as a substitute for coherent source modules.

## 10. `imports` for private aliases

The `imports` field defines package-internal specifiers beginning with `#`:

```json
{
  "imports": {
    "#internal/*": "./dist/internal/*.js"
  }
}
```

This can make internal paths resilient to file movement and prevent confusing relative chains. It also adds resolution policy and can hide architecture if overused.

Course 3 uses ordinary relative internal imports. The concept is included because large packages may benefit from explicit private specifiers later.

## 11. Exporting types and values

```ts
export type { Schema, Infer } from './core.js';
export { string, number, object } from './schemas.js';
```

A type-only re-export has no runtime binding. Consumers must use `import type` when appropriate under strict verbatim module semantics.

Do not declare a type and value with the same name unless the merged meaning is deliberate and documented. Classes, enums, and namespaces occupy different static/runtime namespaces in ways that can confuse package consumers.

SchemaKit keeps naming direct:

- `Schema` — type-only interface;
- `SchemaError` — runtime class and instance type;
- `string`, `number`, `object` — runtime schema factories;
- `Infer` — type-only helper.

## 12. Side effects at import time

A library import should not unexpectedly:

- read environment variables;
- open files or sockets;
- register process handlers;
- mutate globals;
- install prototype methods;
- start timers;
- print output.

Side effects complicate testing, tree shaking, initialization order, and multi-package composition. If a package intentionally performs registration, expose an explicit function or a clearly named side-effect entry point.

SchemaKit's entry points define values and classes only. Parsing begins when a caller invokes a schema.

## 13. Package file selection

Publishing tools may include more or fewer files than expected. Control the artifact through a `files` list and inspect the packed result.

```json
{
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ]
}
```

Ensure the package contains:

- every runtime target in `exports`;
- every declaration target;
- declaration maps/source files if promised;
- required metadata;
- no tests, secrets, local caches, or construction paths unless deliberate.

`npm pack --dry-run` is useful evidence when the exact npm baseline is available.

## 14. Consumer fixtures

A strong consumer fixture lives outside the source graph and imports only documented specifiers. It checks:

- runtime import success;
- type inference;
- type-only imports;
- subpath resolution;
- rejected deep imports;
- no default export if none is promised;
- package version/engine expectations if relevant.

The fixture should run against built or packed artifacts, not TypeScript path aliases that bypass package metadata.

## 15. Package compatibility

Changes that may be breaking:

- removing or renaming an export;
- changing named to default export;
- changing ESM/CommonJS format;
- adding `exports` without old path aliases;
- moving a declaration condition;
- changing an entry from type-only to runtime or reverse;
- adding import-time side effects;
- changing class identity across dual builds;
- dropping a Node version;
- changing package files or source-map availability.

SemVer review must include metadata and resolution, not only function signatures.

## 16. SchemaKit package plan

SchemaKit exposes:

### Root

```ts
Schema
Infer
Issue
ParseResult
SchemaError
string
number
boolean
literal
optional
nullable
array
tuple
object
union
record
refine
transform
lazy
```

### `./json`

```ts
parseJson
safeParseJson
```

### `./testing`

```ts
expectAccept
expectReject
formatIssues
```

The testing subpath is deliberate so testing helpers do not enlarge the ordinary runtime surface.

## 17. A package-resolution ledger

For each public specifier, record:

| Question | Record |
|---|---|
| source entry | Which `.ts` file owns the export? |
| emitted runtime | Which `.js` file executes? |
| declaration | Which `.d.ts` file is consumed? |
| export condition | `types`, `import`, other? |
| runtime format | ESM or CommonJS? |
| side effects | What happens on import? |
| consumer test | Which external fixture imports it? |
| compatibility | What existing path depends on it? |
| packaged file | Is it included in the artifact? |

## 18. Common wrong models

### “If TypeScript resolves it, Node will resolve it”

Compiler configuration and runtime package resolution can differ.

### “The source is TypeScript, so consumers receive types”

Consumers need reachable declarations aligned with entry points.

### “A file in the package is public”

With `exports`, only declared subpaths are supported through normal package resolution.

### “Adding exports only improves encapsulation”

It can break prior deep imports.

### “Dual ESM/CJS publication is just two builds”

State and identity may be duplicated.

### “Type-only imports are style”

They change the runtime module graph.

## 19. Use the idea in a complete program

Module 27 finalizes SchemaKit's package boundary:

- ESM-only publication;
- NodeNext source and declaration resolution;
- explicit `.js` internal specifiers;
- root, JSON, and testing exports;
- no public internal decoder paths;
- built consumer fixtures;
- package metadata and file-list review;
- import-time purity tests.

The independent lab builds another package surface with formatting and testing subpaths.

## Practice sequence

1. Trace every workbook import through source, declaration, metadata, and runtime.
2. Predict the eight Module 27 investigations.
3. Inventory one package's accidental deep imports.
4. Complete [Encapsulated ESM Library Surface](../../labs/module-27-encapsulated-esm-library-surface/README.md).
5. Implement SchemaKit exports from [the capstone guide](../capstone.md#module-27--esm-package-surface).
6. Build a consumer fixture that never imports source-relative paths.

## Ready to continue

You are ready for Module 28 when you can explain:

- why `.js` appears in NodeNext TypeScript source imports;
- how type-only imports change the runtime graph;
- what `exports` encapsulates;
- why adding `exports` may break users;
- the dual-package hazard;
- how runtime and declaration conditions align;
- which three SchemaKit subpaths are supported and why.

Next: [Runtime Schemas, Static Inference, and Validation Algebra](../module-28-runtime-schemas-static-inference-and-validation-algebra/index.md).
