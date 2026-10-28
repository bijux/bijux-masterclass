# Module 30 Workbook

This workbook is a whole-library review. Short answers without affected surfaces do not count.

## A. Contract map

List every SchemaKit public runtime value, public type, internal authority, package specifier, data format, and process boundary. Name the source of truth and evidence for each.

## B. Assertion dossier

Find every `as` and non-null assertion. For each, record the claimed relationship, runtime proof, invariant owner, and counterexample test. Remove unsupported assertions.

## C. Declaration-only review

Read built declarations without source. Write the questions a new consumer can and cannot answer. Repair opaque or leaked types at the source boundary.

## D. Package consumer review

Import root, JSON, and testing subpaths from a separate built fixture. Prove internal deep imports fail and import performs no external effect.

## E. Resource limits

Test array, object-key, issue, union-member, and recursion-depth bounds. Confirm diagnostics do not retain full rejected input.

## F. Independent laboratory

Complete [Typed Library Architecture Audit](../../labs/module-30-typed-library-architecture-audit/README.md).

## G. Discriminated-union impact map

Before coding, cover:

- construction validation;
- runtime selection;
- inferred union output;
- issue paths/codes;
- package export;
- declaration output;
- type tests;
- runtime tests;
- docs;
- compatibility;
- bounds.

## H. Independent implementation

Implement `discriminatedUnion`. Add a project-event example and a consumer fixture. Compare ordinary union and discriminated union behavior on unknown tags and overlapping shapes.

## I. Oral defense

Explain why SchemaKit does not include async schemas, universal exact types, recursive path unions, JSON Schema generation, class-based domain objects, or plugin registries in Course 3.

## J. Reconstruction

Tell the entire Course 3 story from structural assignability to package evolution, using one SchemaKit decision at each step.

## I. Surface agreement audit

Build a table with rows for each SchemaKit public operation and columns for runtime implementation, inferred type, emitted declaration, export path, error behavior, tests, and compatibility notes. Any empty cell is unresolved work.

## J. Impact map

For `discriminatedUnion(key, variants)`, identify:

- construction-time validation;
- discriminant key constraints;
- literal extraction;
- duplicate detection;
- runtime object policy;
- selected variant parsing;
- error paths;
- inferred union output;
- public exports;
- declaration readability;
- old consumer behavior;
- future variant additions.

Order the work so the public contract cannot get ahead of runtime truth.

## K. Consumer simulation

Create three consumers: ordinary application, test helper user, and package author wrapping SchemaKit. Build them against emitted declarations and run them against emitted JavaScript. Attempt one unsupported deep import and require it to fail.

## L. Failure review

Inject a wrong declaration path, an incorrect optional runtime rule, an unbounded union diagnostic, and a migration that loses tags. For each, name the verification layer that should catch it. Add missing evidence where no current test detects the defect.

## M. Release defense

Without notes, explain the complete path from unknown JSON to trusted `ProjectV2`, then through canonical output and package import. Defend every assertion, every runtime limit, every exported subpath, and every compatibility claim.

## N. Independent architecture

Complete the Typed Library Architecture Audit in a domain unrelated to validation. The final design must still align runtime behavior, inferred types, declarations, exports, and migration policy. This is the transfer proof for Course 3.

## O. Release-candidate rehearsal

Build an installation-shaped package, run all consumer fixtures, inspect declarations, execute the CLI, validate old stored fixtures, and attempt unsupported imports. Record results in one release table. A result without a command or artifact is not evidence.

## P. Oral architecture defense

Answer without opening source: Which layer owns runtime trust? Which type computation derives output? Which assertion is hardest to justify? Which package path is intentionally private? Which old data version remains supported? Which change would force a major release? Which resource limit prevents diagnostic explosion?
