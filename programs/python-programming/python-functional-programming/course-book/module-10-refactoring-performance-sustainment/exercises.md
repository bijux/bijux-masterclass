# Module 10 Exercises

Work from the live capstone at `capstone/`. Module 09 is the preserved comparison
state, not the place to implement these changes.

For every exercise, keep observations separate from decisions. Record what was
measured or discovered, pass plain values to a deterministic rule, and state which
earlier RAG behavior must remain unchanged.

## Systematic refactor: make the starting observation trustworthy

**Starting context:** read `build_summary` in
`boundaries/shells/review_cli.py` and
`test_review_inventory_counts_nested_sources_once`.

**Objective:** explain why counting `rag/` and `rag/domain/` independently inflates
the `rag-model` total, then add another nested review path without changing the
reported number.

**Constraints:**

- keep the configured review paths visible in the report;
- deduplicate by discovered file identity, not by subtracting a known constant;
- do not mutate the configured package group;
- do not change any RAG runtime behavior.

**Expected evidence:** the report count equals the size of a set of discovered
Python paths even when one configured path contains another.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_10_sustainment.py \
  -k review_inventory_counts_nested_sources_once
```

Earlier contract preserved: Module 09 package boundaries and proof routes remain
unchanged; only their review observation becomes accurate.
