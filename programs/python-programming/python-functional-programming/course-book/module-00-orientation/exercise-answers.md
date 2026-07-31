# Orientation Exercise Answers

These are review routes, not scripts to copy. A different answer is defensible when it
uses a narrower sufficient proof, identifies the same ownership boundary, and states
its limits honestly.

## Answer 1: Choose an honest proof boundary

| Claim | Smallest suitable command | Why it is sufficient | What it does not prove |
| --- | --- | --- | --- |
| Module 01 rejects `True` as a chunk size | `make PROGRAM=python-programming/python-functional-programming capstone-foundation-proof` | the tracked Module 01 learning test constructs `RagEnv(chunk_size=True)` and expects failure | other Module 01 laws for untested inputs, later state coherence, or live endpoint health |
| tracked states match generated history | `make PROGRAM=python-programming/python-functional-programming history-verify` | this compares every generated module worktree with its declared tracked source | application behavior inside those files |
| live capstone remains healthy after a cross-package refactor | `make PROGRAM=python-programming/python-functional-programming capstone-test` | it runs the live unit and integration suite across packages | strict typing, packaging, documentation, and every behavior not represented by a test |

If the refactor changes public types, packaging, generated reports, or documentation,
the full course `test` target becomes the honest route. “At least the capstone tests”
in the exercise matters: proof scope follows the changed contract, not a fixed ranking
of commands.

Common wrong turns:

- Running `test` for the exact chunk-size claim hides whether you know which state owns
  the law.
- Running `capstone-test` for history coherence tests the endpoint, not the relationship
  between tracked and generated states.
- Treating a green command as universal proof ignores untested inputs and surfaces.

This answer proves that you can route three kinds of claims. It does not prove the
claims until the commands actually pass in your checkout.

## Answer 2: Route a focused failure

The broken law is: concatenating chunks in offset order must reconstruct the complete
cleaned abstract without gaps, overlap, or invented text.

The first owner is `chunk_doc` in the Module 01
`src/funcpipe_rag/pipeline_stages.py`. `embed_chunk` receives an already formed chunk
and cannot repair missing text. `rag_shell.py` owns file and console effects and is not
part of the pure trace. `structural_dedup_chunks` is also downstream; investigate it
only if individual document chunks are correct before deduplication.

A useful counterexample is a cleaned abstract of `"abcdefg"` with `chunk_size=3`:

```text
expected text:    ["abc", "def", "g"]
expected offsets: [(0, 3), (3, 6), (6, 7)]
reconstruction:  "abcdefg"
```

A plausible defect is a loop condition that stops when fewer than three characters
remain, producing `["abc", "def"]`. Another is computing the last `end` as
`start + chunk_size` without bounding it to the document length. The existing test
checks reconstruction and exact offsets, so rerun:

```bash
make PROGRAM=python-programming/python-functional-programming capstone-foundation-proof
```

Common wrong turns:

- changing the test input until the final partial chunk disappears
- changing `clean_doc` so its output matches the defective chunks
- opening the composed pipeline before confirming the owning stage contract

A passing rerun proves the six recorded examples, including this reconstruction law.
It does not prove arbitrary chunk inputs; broader property tests would be separate
evidence.

## Answer 3: Separate the first state from the endpoint

### Pressure visible in Module 01

The first state needs immutable values and deterministic transforms for cleaning,
chunking, embedding, and canonical deduplication. The core question is whether a reader
can substitute a value with the result of its pure expression without hidden behavior.

### Later pressure visible only in the endpoint

`domain/effects/async_/` represents Module 08 scheduling and backpressure pressure.
`interop/` and `boundaries/shells/cli.py` represent Module 09 ecosystem and CLI
boundaries. `review/` represents Module 10 sustainment evidence. These surfaces are not
gratuitous, but they answer problems the learner has not reached in Module 01.

### Preserved foundation law

The endpoint must still preserve deterministic pure-core behavior. The Module 01 test
`test_pure_core_preserves_inputs_and_canonicalizes_output` records that contract.

### Teaching cost of starting from the endpoint

A learner would have to separate foundational value transformations from result
containers, policies, effects, adapters, and review machinery before seeing why the
first design exists. That reverses the course's pressure order. The tracked state keeps
the first decision reviewable; the endpoint later demonstrates that the decision can
survive growth.

Common wrong turns:

- describing every later package as overengineering instead of asking which later
  pressure earned it
- treating reference states as disconnected sample applications
- claiming the foundation law survives without naming executable evidence

This comparison proves you can locate concept timing. It does not establish that every
live implementation still satisfies the early law; that requires live or cumulative
tests.

## Answer 4: Design a re-entry route

A defensible record is:

```text
trusted through: Module 02 data-first values and configuration
uncertain contract: Module 03 demand, bounded consumption, and materialization
first module to revisit: Module 03
source or state to inspect: module-03 streaming stages and learning test
focused evidence: run the Module 03 streaming dataflow learning proof
move-forward condition: predict and explain demand for a bounded prefix, then pass the proof
```

From the Functional Programming program directory, the focused evidence is:

```bash
PYTHONPATH=capstone/module-reference-states/module-03/src \
  python -m pytest -q \
  capstone/module-reference-states/module-03/tests/learning/test_module_03_streaming_dataflow.py
```

After that condition is met, revisit Module 04's stream failure representation. Move to
Module 08 only after you can explain which producer, consumer, buffer, and demand signal
create the async pressure.

Common wrong turns:

- restarting at Module 01 despite still trusting its and Module 02's contracts
- jumping to Module 08 because its title matches the current project vocabulary
- using `history-verify` as behavioral proof; it establishes state integrity, not lazy
  consumption
- using “I reread the page” as the move-forward condition

The route proves recovery judgment when you can execute and explain its evidence. It
does not prove Module 04 or Module 08 until their own claims are inspected and tested.
