# Module 07 Exercises

Work from `capstone/module-reference-states/module-07/`. That directory is the
completed Module 07 application state. Module 06 is the before-state, while
Modules 08 and 09 and the live capstone must retain every boundary contract
proved here.

For each exercise, name the domain-owned contract, the shell action that
interprets it, and the concrete infrastructure detail that must remain outside
the pure RAG core.

## Ports and adapters: substitute storage without changing behavior

**Starting context:** read `StorageRead`, `FileStorage`, and `InMemoryStorage`,
then run `test_storage_adapters_preserve_rag_read_behavior`.

**Objective:** add a third document to both fixtures and make the shared
domain-facing function filter one requested category before returning document
identifiers.

**Constraints:**

- keep the function parameter typed as `StorageRead`;
- do not branch on the adapter class;
- compare complete observable results from both adapters;
- do not move CSV parsing into the domain-facing function.

**Expected evidence:** both adapters return the same ordered identifiers for the
requested category.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k storage_adapters_preserve_rag_read_behavior
```

Earlier contract preserved: the Module 06 RAG computation still consumes
`RawDoc` values and typed failures; only the source of those values changes.
