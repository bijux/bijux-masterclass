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

## Async property testing: vary pressure without adding real I/O

**Starting context:** read `async_gather` and
`test_bounded_async_gather_preserves_input_order`.

**Objective:** extend the generated concurrency range and explain why the expected
list must not change.

**Constraints:**

- construct fresh `AsyncPlan` values with `async_pure`;
- keep generated lists bounded;
- include empty and single-item cases;
- do not use sleeps as an assertion of scheduler behavior.

**Expected evidence:** every successful result equals the input list for all
generated concurrency limits.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_10_sustainment.py \
  -k bounded_async_gather_preserves_input_order
```

Earlier contract preserved: Module 08's bounded scheduler may change completion
timing, but ordered gather retains input order and the `Result` failure boundary.

## Advanced patterns and scaling: distinguish three readiness states

**Starting context:** read `pipelines/distributed.py`,
`review/scaling.py`, and
`test_scaling_review_separates_installation_implementation_and_proof`.

**Objective:** assess a locally installed backend that has a compiler but lacks a
backpressure proof.

**Constraints:**

- do not import or install the optional backend;
- keep installation, implementation, and semantic proof distinct;
- report missing proofs in stable order;
- require all declared proofs before implementation readiness.

**Expected evidence:** installed and implemented is still not ready when one
required semantic proof is missing.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_10_sustainment.py \
  -k scaling_review_separates_installation_implementation_and_proof
```

Earlier contract preserved: a future compiler must retain Module 08 ordering,
failure, and pressure contracts; local execution remains the semantic oracle.

## DDD and FP: assign review ownership without inventing services

**Starting context:** inspect `PACKAGE_GROUPS` in `review_cli.py` and
`test_package_groups_name_review_ownership_not_only_directories`.

**Objective:** decide which owner reviews a change that touches both
`pipelines/configured.py` and `policies/retry.py`.

**Constraints:**

- choose ownership by stable responsibility, not directory proximity alone;
- do not move packages for diagram symmetry;
- keep RAG domain language separate from operational policy;
- make every published package group accountable.

**Expected evidence:** the report exposes one durable owner for each review group,
and the cross-group change names both required reviewers.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_10_sustainment.py \
  -k package_groups_name_review_ownership_not_only_directories
```

Earlier contract preserved: existing package boundaries and imports remain stable;
Module 10 adds review accountability rather than a speculative service split.

## Versioning and migration: separate shape from semantics

**Starting context:** read `review/migration.py`,
`upcast_metadata_v1`, and
`test_metadata_migration_pairs_shape_review_with_an_executable_upcaster`.

**Objective:** classify adding a required `language` field, then design the
upcaster input needed to supply it honestly.

**Constraints:**

- classify added optional and added required fields differently;
- do not invent a language value inside a pure translator without a declared rule;
- preserve source and tag meaning;
- state which persisted or wire formats remain untested.

**Expected evidence:** the shape review says `requires-migration`, and the proposed
upcaster makes the source of `language` explicit.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_10_sustainment.py \
  -k metadata_migration_pairs_shape_review_with_an_executable_upcaster
```

Earlier contract preserved: Module 05 domain invariants remain true after
translation, including immutable tags and unchanged provenance.

## Governance: require a claim-to-command route

**Starting context:** read `review/evidence.py`, `EVIDENCE_CLAIMS`, and
`test_governance_claim_fails_closed_when_executable_evidence_is_missing`.

**Objective:** add a ranking-stability claim and decide which source, test, and
focused command make it reviewable.

**Constraints:**

- a claim must name at least one required path;
- missing paths must remain visible and ordered;
- do not treat file presence as a passing test;
- keep filesystem discovery outside `assess_evidence`.

**Expected evidence:** omitting either the implementation or proof path makes the
claim incomplete; supplying both makes it discoverable and names a runnable route.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_10_sustainment.py \
  -k governance_claim_fails_closed_when_executable_evidence_is_missing
```

Earlier contract preserved: governance describes how existing RAG laws are
reviewed; it does not replace those laws with repository metadata.

## Capstone delivery: distinguish discoverability from execution

**Starting context:** run `make review-check`, then read
`test_delivery_check_exposes_a_machine_readable_release_gate`.

**Objective:** remove one declared test path in a temporary project tree and
explain why the check fails even though its implementation path exists.

**Constraints:**

- do not run declared commands inside the evidence assessor;
- emit both human-readable and JSON reports;
- return a nonzero exit code for incomplete evidence;
- state which separate command proves execution.

**Expected evidence:** the incomplete temporary tree returns exit code 1 and names
the missing test; the real capstone returns 0 before its focused tests run.

**Acceptance check:**

```bash
make review-check
pytest -q tests/learning/test_module_10_sustainment.py \
  -k delivery_check_exposes_a_machine_readable_release_gate
```

Earlier contract preserved: the existing pytest and confirmation routes remain
the behavioral authority; the delivery check makes their claim mapping fail closed.
