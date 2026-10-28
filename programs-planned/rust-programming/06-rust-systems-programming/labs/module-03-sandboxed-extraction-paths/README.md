# Laboratory 53 — Sandboxed Extraction Paths

This is the independent product for **Course 6, Module 53: Paths, Names, and Platform Boundaries**. Read the [module chapter](../../course-book/module-53-paths-names-and-platform-boundaries/index.md) and complete its [workbook](../../course-book/module-53-paths-names-and-platform-boundaries/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a portable logical-path parser and a bounded extraction resolver. The lab separates archive syntax from host path syntax and refuses direct parent, root, prefix, empty, and dot components.

## Why this laboratory exists

This lab separates portable archive identity from host pathname behavior. The goal is not to claim a perfect sandbox with pathname preflight; it is to define the exact lexical and filesystem assumptions under which extraction is acceptable. Write the threat model before using `PathBuf`, because path convenience methods do not choose that policy for you.

## Contract

A logical name is UTF-8, uses `/`, contains 1–32 nonempty components, and is at most 1024 bytes. Components may not be `.` or `..` and may not contain NUL. `resolve_under` joins only validated components beneath a provided root. A helper rejects any existing symlink component under the stated fresh-tree threat model.

## Required milestones

1. Create a `LogicalPath` newtype with private validated components.
2. Keep original native `PathBuf` values in host-conversion errors.
3. Resolve by components rather than textual concatenation.
4. Inspect existing ancestors with `symlink_metadata`.
5. Document why this is not race-free in an attacker-controlled tree.

## Adversarial cases

- absolute-looking logical names
- empty component from doubled slash
- dot and dot-dot
- NUL
- more than 32 components
- existing symlink ancestor where supported
- destination filename collision

## Evidence to produce

- a table separating logical-name rules from host-path observations;
- tests for absolute forms, parent and current components, empty components, backslashes, drive markers, and control characters;
- tests for existing files, existing symlink ancestors, and non-directory ancestors;
- a step-by-step creation trace for one nested destination;
- an explicit statement of the remaining time-of-check/time-of-use race.

## Prohibited shortcuts

Do not treat `canonicalize` as a portable archive identity, accept a path because its rendered string starts with the base string, join unvalidated components, overwrite an existing destination, follow a known symlink ancestor, or claim adversarial containment from lexical checks alone. A policy may be deliberately limited, but its limit must be part of the contract.

## Transfer

Design a cache-key policy for host paths and decide whether it needs native identity, canonical resolved identity, or a portable logical name.

## Comparing with the reference

Compare threat models before comparing helper functions. Determine whether each implementation rejects the same lexical forms, inspects every existing ancestor, creates missing directories one component at a time, and preserves no-overwrite behavior at final creation. Note which race requires descriptor-relative OS APIs rather than another string check.

## Completion check

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/` and do not open `solution/` until the contract, adversarial cases, and transfer are implemented or a precise blocker is written.

The laboratory is complete when the tests and documented failure paths pass, and you can answer this question without the chapter:

> How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?

Run the local proof route:

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```
