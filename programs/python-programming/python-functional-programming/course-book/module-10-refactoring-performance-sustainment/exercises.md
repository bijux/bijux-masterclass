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

## Performance budgeting: reject a one-dimensional win

**Starting context:** read `review/performance.py` and
`test_performance_budget_is_a_pure_multi_dimensional_decision`.

**Objective:** evaluate an alternative observation that halves latency but doubles
peak memory, then decide whether it can replace the current RAG stage.

**Constraints:**

- do not call a clock or profiler inside `evaluate_budget`;
- keep latency, memory, and throughput thresholds explicit;
- report every violated dimension in stable order;
- require semantic equivalence before considering the budget result.

**Expected evidence:** the same immutable observation always produces the same
decision, and a latency win cannot hide a memory or throughput failure.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_10_sustainment.py \
  -k performance_budget_is_a_pure_multi_dimensional_decision
```

Earlier contract preserved: the optimized Module 05 embedding path must still
produce equivalent `Chunk` values before performance can justify selecting it.

## Observability: preserve facts without creating hidden policy

**Starting context:** read `review/observability.py` and
`test_observability_is_data_that_does_not_change_pipeline_decisions`.

**Objective:** add a `rank` observation and explain why a failure count belongs in
the summary while the decision to abort does not.

**Constraints:**

- observations must be immutable values;
- preserve encounter order in `summary.stages`;
- define the empty fold result;
- reject impossible negative or failure-greater-than-processed counts.

**Expected evidence:** repeated folds over the same tuple produce equal summaries,
including stable stage order and totals.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_10_sustainment.py \
  -k observability_is_data_that_does_not_change_pipeline_decisions
```

Earlier contract preserved: Module 07 keeps effects at the shell, and Module 04
typed failures remain the RAG control-flow values rather than being replaced by
metrics.

## Property-based regression: state equivalence in domain terms

**Starting context:** read `embedding_batches_equivalent` and
`test_optimized_embedding_preserves_the_domain_contract`.

**Objective:** introduce a deliberate metadata mismatch in one result and predict
the smallest counterexample Hypothesis needs to reject equivalence.

**Constraints:**

- compare success and failure variants explicitly;
- preserve chunk identity, text, metadata, model, and vector values;
- apply numeric tolerance only to vectors;
- do not assert implementation type equality.

**Expected evidence:** generated batches accept the shipped pure and hybrid routes,
while a one-item metadata change makes the predicate false.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_10_sustainment.py \
  -k optimized_embedding_preserves_the_domain_contract
```

Earlier contract preserved: Module 05's optimized representation is replaceable
only while the public `Chunk` and typed-failure semantics remain equivalent.
