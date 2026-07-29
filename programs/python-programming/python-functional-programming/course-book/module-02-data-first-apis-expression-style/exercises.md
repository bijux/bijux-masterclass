# Module 02 Exercises: Design the Configured RAG API

Work against `capstone/module-reference-states/module-02`. Preserve Module 01
cleaning, chunk metadata, deterministic embeddings, canonical deduplication, and
output order unless an exercise explicitly selects a non-default policy.

Run both focused proof owners first:

```bash
make PROGRAM=python-programming/python-functional-programming \
  capstone-data-api-proof
make PROGRAM=python-programming/python-functional-programming \
  capstone-data-shell-proof
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
- make `boundary_rag_config` the semantic validator for every entry point;
- reject unknown names, booleans, and nonpositive sizes before dependency selection;
- preserve rule order.

Expected evidence:

- a unit test for the rule itself;
- a test showing order relative to another rule;
- mapping-boundary tests for valid, unknown-rule, boolean, zero, and negative input;
- a CLI-boundary test proving an unknown name returns `Err` before execution;
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

## Exercise 4: Prove injected and concrete boundaries

Starting context: `full_rag_api_path` receives a `Reader` capability and returns a
`Result`; `shells/rag_api_shell.run` owns the concrete CSV-to-JSONL route.

Objective: prove that an `Err` reader result prevents cleaning and embedding, then
prove the real filesystem shell preserves successful core values and failure timing.

Constraints:

- use a fake reader for control-flow proof;
- use cleaner and embedder test doubles that record or fail if called;
- preserve the original `Err` value;
- use temporary paths for the real adapter proof;
- compare decoded JSONL with `full_rag_api_docs`, not only with expected counts;
- check whether output exists after load and write failures;
- do not catch all exceptions inside the core.

Expected evidence:

- an ordered event trace for successful and failing injected reads;
- valid CSV, header-only CSV, malformed CSV, missing input, and unavailable output
  cases against the concrete shell;
- an explicit boundary between what the fake proof and real-adapter proof establish.

Acceptance checks:

- failure performs only the reader event;
- success runs the configured core after reading;
- `result_map` and `result_and_then` skip their functions for `Err`;
- a load failure creates no output;
- valid JSONL decodes to the exact pure API chunks in order;
- write failure is identified as occurring after core work;
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
- one real filesystem proof that distinguishes load and write failure timing;
- one observation hook proven neutral;
- the exact focused Make route supporting each claim.
