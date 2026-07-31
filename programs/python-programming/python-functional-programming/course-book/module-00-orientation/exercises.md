# Orientation Exercises

These exercises make the study method observable before Module 01 asks you to change
code. Work against the tracked Module 01 state, not the live endpoint, unless an
exercise explicitly asks you to compare them.

## Exercise 1: Choose an honest proof boundary

### Starting context

A teammate makes each of these claims:

1. “Module 01 rejects `True` as a chunk size.”
2. “Every tracked module state matches its generated history worktree.”
3. “The live capstone remains healthy after a cross-package refactor.”

### Objective

Choose the smallest suitable command for each claim from:

```text
capstone-foundation-proof
history-verify
capstone-test
test
```

### Constraints

- Do not choose a broader command merely because it contains the narrower test.
- Distinguish behavioral evidence from generated-state integrity.
- State what each selected command cannot prove.

### Expected evidence

Produce a three-row table with the claim, command, why it is sufficient, and proof
limit.

### Acceptance checks

- The exact chunk-size claim uses the tracked Module 01 learning proof.
- The state-coherence claim uses history verification rather than application tests.
- The cross-package live refactor uses at least the live capstone suite.

### Earlier contract to preserve

The capstone remains cumulative: a narrow Module 01 proof must not silently import the
live Module 10 implementation.

## Exercise 2: Route a focused failure

### Starting context

Imagine the foundation proof fails here:

```python
assert "".join(chunk.text for chunk in chunks) == cleaned.abstract
```

You have not changed embedding, deduplication, file loading, or the shell.

### Objective

Write a failure-investigation route that begins with the smallest owning surface.

### Constraints

- Name the first source function and file to inspect.
- Explain why at least two other files are not the first owner.
- Give one plausible defect and one counterexample that would expose it.
- Do not propose a fix until you can state the broken law.

### Expected evidence

Provide:

1. the law in plain language
2. the first source owner
3. one concrete input, expected chunks, and reconstructed text
4. the focused command you would rerun

### Acceptance checks

- The route starts at `chunk_doc` in the Module 01 `pipeline_stages.py`.
- The counterexample checks both text coverage and offsets.
- The rerun remains bounded to `capstone-foundation-proof`.

### Earlier contract to preserve

Cleaning remains deterministic; a chunking investigation must not alter the cleaned
document to make the assertion pass.

## Exercise 3: Separate the first state from the endpoint

### Starting context

The live capstone contains packages for results, policies, effects, async coordination,
interop, and review evidence. None of those packages appears in the tracked Module 01
source tree.

### Objective

Explain why teaching Module 01 from the live package would distort the application
delta.

### Constraints

- Inspect both `capstone/module-reference-states/module-01/src/funcpipe_rag/` and
  `capstone/src/funcpipe_rag/`.
- Identify two live concerns that belong to later modules.
- Identify one foundation law that the live endpoint must still preserve.
- Do not argue that later code is bad merely because it is more complex.

### Expected evidence

Write a short comparison with these headings:

- pressure visible in Module 01
- later pressure visible only in the endpoint
- preserved foundation law
- teaching cost of starting from the endpoint

### Acceptance checks

- The comparison distinguishes cumulative growth from disconnected examples.
- Each later concern is assigned to a plausible later module.
- The preserved law is backed by a named Module 01 learning test.

### Earlier contract to preserve

Later modules may add boundaries and representations, but they must not erase the
deterministic pure-core contract established first.

## Exercise 4: Design a re-entry route

### Starting context

You completed Modules 01 through 04 two months ago. You remember why pure functions
matter, but you no longer trust your understanding of lazy materialization or typed
stream failures. A new project pressure concerns async backpressure.

### Objective

Design the shortest defensible route back into the course.

### Constraints

- Do not restart automatically at Module 01.
- Do not jump directly to Module 08 because the project mentions async work.
- Name the last contract you still trust and the first contract you need to re-prove.
- Use one reading surface, one tracked state, and one focused proof before moving on.

### Expected evidence

Produce a re-entry record:

```text
trusted through:
uncertain contract:
first module to revisit:
source or state to inspect:
focused evidence:
move-forward condition:
```

### Acceptance checks

- The route revisits streaming foundations before async coordination.
- The move-forward condition is observable, not “read the page.”
- The route widens only after the uncertain earlier contract is trustworthy again.

### Earlier contract to preserve

Async reasoning depends on knowing when work is produced and materialized; the recovery
route must restore that Module 03 contract before adding Module 08 scheduling pressure.

## Review route

Compare your decisions with [Orientation Exercise Answers](exercise-answers.md). Do not
grade by identical wording. Grade by scope, ownership, preserved behavior, and the
honesty of the claimed evidence.
