# Final Review — Reconstruct, Build, and Defend

Complete this review after all ten modules and laboratories. Do not read the [answer and evaluator guide](final-review-solutions.md) until a complete first attempt exists.

## Part I — Closed-book reconstruction

Draw and explain:

1. TypeScript source → checker → emitted JavaScript → Node ESM loading → process behavior.
2. The responsibilities of Node, ECMAScript, TypeScript, npm, package metadata, and the operating system.
3. The acceptance–conversion–domain pipeline for a positive integer token.
4. The difference among `===`, `Object.is`, Map/Set equality, truthiness, `||`, and `??`.
5. A closure that observes a mutable binding and a closure that preserves a snapshot.
6. Method, extracted function, bound function, arrow function, and explicit `this` parameter behavior.
7. A heap graph demonstrating alias mutation, shallow spread, and path-local structural sharing.
8. A discriminated union with one exhaustive function and one runtime decoder.
9. An array/Map/Set decision table and one generic relationship that earns its type parameters.
10. An ESM graph with runtime edges, type-only edges, one public entry, and no cycle.
11. The trust boundary from bytes/text to JSON syntax to unknown value to trusted domain object.
12. A promise ownership graph with sequential and aggregate ownership.
13. The StudyLedger architecture and effect order for a mutating command.
14. An evidence matrix connecting claims to type-check, unit, filesystem, and process tests.

## Part II — Prediction examination

Select twenty unseen cases from `compiler-labs`, two from each module. For each:

- classify static and runtime outcome before tools;
- state the exact rule;
- identify the first decisive phase;
- propose the smallest requirement-preserving repair;
- reject one repair that merely silences the checker or exception.

Target: at least sixteen correct initial classifications and a correct causal explanation for all corrections.

## Part III — Diagnostic clinics

### Clinic A — false static confidence

A configuration is parsed with `JSON.parse(text) as Config`. Production later fails on `config.output.directory`. Produce the missing runtime contract, decoder stages, errors, and tests.

### Clinic B — hidden alias mutation

A function returns `{ ...inventory }` after changing `inventory.items[0].stock`. Draw identities, identify every observer of the mutation, and repair the update while preserving untouched identities.

### Clinic C — unowned asynchronous work

A command invokes `void save(path, ledger)` and immediately prints success. State all observable false claims and repair application/process boundaries.

### Clinic D — module graph mismatch

Editor imports resolve; emitted Node code fails on `./command`. Diagnose package mode, compiler mode, source specifier, emitted graph, and test route.

### Clinic E — overbroad catch

A loader catches every error and returns an empty ledger. Distinguish missing, permission, malformed JSON, invalid schema, and programming defects. Explain the data-loss risk.

## Part IV — Independent construction

Build `expense-note`, a persistent CLI with these behaviors:

```text
expense-note add --category <text> --amount-cents <integer> --note <text>
expense-note list [--category <text>]
expense-note remove <id>
expense-note summary
expense-note help
expense-note version
```

Requirements:

- strict TypeScript and ESM;
- canonical decimal parsing for cents;
- positive monotonic IDs;
- immutable domain updates;
- injected timestamps;
- versioned JSON decoded from unknown;
- unknown-key and duplicate-ID policy;
- deterministic ID-order output;
- asynchronous missing-file/load/save behavior;
- command, domain, validation, and I/O errors;
- unit, codec, filesystem, application, and process tests.

Do not copy StudyLedger names or layout. Derive boundaries from the product.

## Part V — StudyLedger independent change

Choose one:

1. **Rename topic** — preserve ID and history; validate new topic; update search and process tests.
2. **Reopen** — decide legal terminal states and what history survives.
3. **Labels** — define normalization, duplicates, order, storage compatibility, search, and rendering.
4. **Date-range summary** — define inclusive bounds, UTC/timezone policy, and which timestamp controls inclusion.

Before coding, submit an impact map:

```text
command grammar
static command type
domain transition/query
runtime validation
storage compatibility
canonical encoding
rendering
application orchestration
help
unit/integration/process evidence
non-affected boundaries
```

## Part VI — Oral defense

Answer without tools:

1. Which StudyLedger facts exist only in TypeScript, and which values exist only at runtime?
2. Why is a type assertion not a decoder?
3. Why do relative TypeScript imports use `.js`?
4. When does readonly fail to provide snapshot semantics?
5. Which state transitions are legal and which module owns them?
6. Why does `JSON.parse` begin a trust boundary rather than end one?
7. Which promises exist during plan and who observes rejection?
8. Why does summary not call the clock?
9. What does same-directory temporary replacement protect?
10. Why can a missing-file fallback be correct while a catch-all fallback is dangerous?
11. Which tests would detect success printed before save?
12. Which behaviors remain platform-conditioned?
13. What is StudyLedger’s public API and what remains private?
14. Which feature would force a V2 storage format?
15. What would break first under concurrent writers?

## Scoring guide

| Area | Weight |
|---|---:|
| Runtime and checker distinction | 15 |
| Values, coercion, identity, and state modeling | 20 |
| Modules, errors, validation, and persistence | 20 |
| Promises, process, and async effects | 15 |
| Tests and causal diagnosis | 15 |
| Independent construction/change | 15 |

Recommended completion standard: 85/100, with no score below 70% in runtime/checker distinction, unknown-data validation, or promise ownership. Those are dependency skills for the next course.

## Required deliverables

The final review is complete only when the following artifacts exist:

1. a closed-book reconstruction document;
2. predictions and causal explanations for the selected investigation cases;
3. repaired clinic implementations with focused regression tests;
4. the independent Expense Note product;
5. one StudyLedger change with its prewritten impact map;
6. a short oral-defense recording or written transcript;
7. a final claim ledger separating validated behavior from non-contracts.

The claim ledger should contain at least these columns:

| Claim | Authority | Evidence | Boundary not proved |
|---|---|---|---|
| malformed persisted sessions are rejected | codec | hostile fixture tests | arbitrary future V2 migration |
| success follows save | application | delayed/rejecting save fake and process test | crash durability after rename |
| list order is stable | query/render | order tests | locale-sensitive natural-language sorting |

This prevents “all tests pass” from becoming an unbounded conclusion.

## Independent-construction constraints

The Expense Note product may reuse the course’s reasoning methods but not StudyLedger’s source files. It must:

- use integer cents rather than binary floating-point currency;
- decode stored JSON from `unknown`;
- define duplicate-ID and unknown-key policy;
- separate command grammar, domain behavior, codec, storage, orchestration, rendering, and process binding;
- produce deterministic category summaries;
- await persistence before reporting mutation success;
- contain at least one unit, codec, filesystem, application-order, and process-lifecycle test.

Frameworks and third-party validators are excluded from this assessment because they would hide the mechanisms being tested. They become appropriate after the reader can explain what those tools would replace.

## Completion decision

A score is not sufficient when a load-bearing misconception remains. Do not mark the course complete if any of these statements cannot be defended with code and evidence:

- TypeScript evidence and runtime evidence are different.
- Unknown external values become trusted only through validation and construction.
- Object identity and promise ownership remain observable parts of behavior.
- ESM source, emitted imports, package metadata, and Node resolution must agree.
- A successful command includes its required asynchronous effects.
- Tests prove bounded claims at selected boundaries, not universal correctness.

After completing the review, wait at least seven days and repeat the reconstruction section before starting Course 2. That later course assumes these foundations are retrievable, not merely familiar.

## Final defense standard

The defense is not a recital of syntax. Use concrete traces. When asked about one command, follow its argument tokens through parsing, domain construction, current-state loading, transition, encoding, asynchronous save, rendering, and exit status. When asked about one malformed file, identify the exact layer that rejects it and why later layers never receive a trusted value.

For every design choice, be prepared to name one rejected alternative. Examples include direct JSON assertions, shared mutable singleton state, top-level environment reads, success output before persistence, floating-point money, unstable iteration order, or a catch-all empty-state fallback. Explain not merely that the alternative is “bad,” but which observable contract it violates.

A reader who can complete this defense can begin the second course. A reader who can only recognize the final code should repeat the delayed reconstruction and one independent lab before advancing.
