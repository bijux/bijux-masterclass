# Module 02 Exercises: Design the Configured RAG API

Work against `capstone/module-reference-states/module-02`. Preserve Module 01
cleaning, chunk metadata, deterministic embeddings, canonical deduplication, and
output order unless an exercise explicitly selects a non-default policy.

Run the learning proof first:

```bash
PYTHONPATH=capstone/module-reference-states/module-02/src \
  python -m pytest -q \
  capstone/module-reference-states/module-02/tests/learning/test_module_02_data_first_apis.py
```

Record your prediction before executing. Use [Exercise Answers](exercise-answers.md)
only after you have evidence.

## Exercise 1: Classify the API inputs

Starting context: `iter_rag_core` accepts `docs`, `config`, and `deps`.

Objective: classify every field reachable from those arguments as run input, policy
data, pure capability, or observation effect.

Constraints:

- do not classify only by Python type;
- state who constructs and owns each value;
- identify one field that would be harmful in a different group.

Expected evidence: an ownership table covering `RagEnv`, `RulesConfig`,
`CleanConfig`, cleaner, embedder, and taps.

Acceptance checks:

- configuration contains no open file or reader instance;
- dependencies contain behavior rather than serializable policy;
- the Module 01 default-value proof remains valid.

## Exercise 2: Add a cleaning policy

Starting context: `CleanConfig.rule_names` is ordered data interpreted through
`RULES`.

Objective: add a pure `casefold` cleaning rule and expose it through validated
configuration.

Constraints:

- name the rule by stable behavior;
- do not change default cleaning;
- reject unknown names at the boundary;
- preserve rule order.

Expected evidence:

- a unit test for the rule itself;
- a test showing order relative to another rule;
- a boundary configuration test;
- the default Module 01 compatibility test still passes.

Acceptance checks:

- `CleanConfig` remains frozen and tuple-based;
- no callable is serialized into config;
- valid non-default policy changes only the abstract text and derived chunks.

## Exercise 3: Compare rule representations

Starting context: Module 02 supports function closures, frozen predicate data, and a
guarded text expression.

Objective: express “keep computer-science documents with abstracts of at least four
characters” in all three representations.

Constraints:

- use only the current taught parser surface;
- inspect predicate data without executing it;
- do not claim function closures are structurally equal;
- include one rejecting document for each condition.

Expected evidence: a table comparing equality, inspection, serialization, execution,
and validation needs.

Acceptance checks:

- all three routes agree on the fixture set;
- short-circuit behavior is explained;
- unsafe parsed input is rejected before a document is evaluated.

## Exercise 4: Prove boundary short-circuiting

Starting context: `full_rag_api_path` receives a `Reader` capability and returns a
`Result`.

Objective: prove that an `Err` reader result prevents cleaning and embedding.

Constraints:

- use a fake reader;
- use cleaner and embedder test doubles that record or fail if called;
- preserve the original `Err` value;
- do not catch all exceptions inside the core.

Expected evidence: an ordered event trace for successful and failing reads.

Acceptance checks:

- failure performs only the reader event;
- success runs the configured core after reading;
- `result_map` and `result_and_then` skip their functions for `Err`;
- the result says nothing about retry or cleanup policy.

## Exercise 5: Add neutral stage observation

Starting context: `RagTaps` observes completed kept, cleaned, and pre-deduplicated
chunk stages.

Objective: report counts and safe identifiers without changing API output.

Constraints:

- do not store abstract text;
- do not use a tap to filter or replace values;
- state whether callback exceptions propagate;
- compare a tapped run with an untapped run.

Expected evidence:

- identical chunks and `Observations`;
- exact callback order and stage counts;
- a statement that chunk taps occur before canonical deduplication.

Acceptance checks:

- output neutrality is tested with structural equality;
- callback-owned state is explicitly bounded;
- observation remains an injected dependency;
- the test does not overclaim thread safety or privacy.

## Completion review

You are ready for Module 03 when you can show:

- default equality with the Module 01 RAG transformation;
- one immutable policy value and the function it configures;
- one expression pipeline with its cardinality changes;
- one expected boundary failure represented as data;
- one observation hook proven neutral;
- the exact reference-state command supporting each claim.
