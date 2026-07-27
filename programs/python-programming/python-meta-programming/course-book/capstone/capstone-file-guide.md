# Capstone File Guide

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Capstone"]
  page["Capstone File Guide"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Use this guide when you opened the capstone but still do not know which file owns which
responsibility. The goal is not to read the whole tree. The goal is to choose one source
file, one matching proof file, and one honest next move.

## Start by question

| If your question is... | Start with | Then read |
| --- | --- | --- |
| what exists before any instance is created | `framework.py` | `test_registry.py` |
| how one field validates and stores data | `fields.py` | `test_fields.py` |
| how one wrapped action preserves metadata | `actions.py` | `test_runtime.py` |
| how the abstractions look in a concrete plugin | `plugins.py` | `test_runtime.py` |
| how the public review surface is assembled | `cli.py` | `test_cli.py` |

## Source files

### `framework.py`

Owns the metaclass, generated constructor signature, registry, manifest export, and
runtime invocation entrypoints.

### `fields.py`

Owns descriptor-backed configuration semantics, coercion, and field manifest metadata.

### `actions.py`

Owns callable wrapping, signature preservation, and action history recording.

### `plugins.py`

Owns concrete delivery plugins that make the abstractions visible in realistic examples.

### `cli.py`

Owns public inspection and invocation commands that expose the runtime without hiding it.

## Test files

### `test_fields.py`

Proves field validation, coercion, and per-instance behavior.

### `test_registry.py`

Proves constructor signature generation, deterministic registration, and action metadata preservation.

### `test_runtime.py`

Proves manifest export, runtime invocation, and action-history recording.

### `test_cli.py`

Proves the public command surface stays observational and reviewable.

## Reading tip

When a mechanism feels too abstract, move from the owning source file to the matching
test file immediately. The capstone teaches best when implementation and proof stay adjacent.

## What not to do first

- Do not start in `plugins.py` if the ownership model is still fuzzy.
- Do not start in tests if you cannot yet name the owning source file.
- Do not open every file in order when one question only needs one ownership route.

## Module-to-file route

- Modules 01-03: `framework.py`, `test_registry.py`, and `test_runtime.py`
- Modules 04-05: `actions.py` and `test_runtime.py`
- Modules 06-08: `fields.py` and `test_fields.py`
- Module 09: `framework.py` and `test_registry.py`
- Module 10 and mastery review: `cli.py`, `test_cli.py`, and the saved bundles under `artifacts/`

## Good stopping point

Stop when you can name:

- one owning source file
- one matching test file
- one reason you do not need the rest of the tree yet
