# State: Return Local Progress Explicitly

Reader describes a computation that reads the same environment throughout:

```text
RagEnv -> Value
```

State describes a computation that receives a state value and returns a new
one alongside its result:

```text
Progress -> (Value, Progress)
```

Nothing mutates in place. The change is explicit in the return value.

This can clarify several dependent updates, but a fold or an ordinary tuple is
often simpler. Learn State as a composition tool with a cost, not as the
mandatory replacement for every counter.

## Start from the FuncPipe progress requirement

The learning proof chunks ten normalized characters into three chunks:

```text
"abcd", "efgh", "ij"
```

It wants to retain:

- the current chunk text as the flow value;
- the number of observed chunks; and
- the number of observed characters.

The progress model is immutable:

```python
@dataclass(frozen=True)
class Progress:
    chunks: int = 0
    characters: int = 0
```

One accounting operation has this conceptual signature:

```text
str -> State[Progress, str]
```

Its implementation returns the text and a new progress value:

```python
def account(text: str) -> State[Progress, str]:
    return State(
        lambda progress: (
            text,
            Progress(
                chunks=progress.chunks + 1,
                characters=(
                    progress.characters + len(text)
                ),
            ),
        )
    )
```

## Run the complete state transition

The operations are dependent because each one must receive the progress
returned by the preceding operation:

```python
program = (
    account(chunks[0].text)
    .and_then(lambda _: account(chunks[1].text))
    .and_then(lambda _: account(chunks[2].text))
)

initial = Progress()
value, final = run_state(program, initial)
```

The expected observation is:

```python
assert value == "ij"
assert final == Progress(chunks=3, characters=10)
assert initial == Progress()
```

Run it:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k state_threads_rag_chunk_progress_without_global_mutation
```

The last assertion matters. It distinguishes returning a new frozen value from
mutating the caller’s initial state.

## Trace `and_then` by hand

For initial `Progress()`:

| Operation | Returned value | Returned state |
| --- | --- | --- |
| `account("abcd")` | `"abcd"` | `Progress(chunks=1, characters=4)` |
| `account("efgh")` | `"efgh"` | `Progress(chunks=2, characters=8)` |
| `account("ij")` | `"ij"` | `Progress(chunks=3, characters=10)` |

`State.and_then` passes only the value into the function you provide. It
threads the updated state internally:

```python
def and_then(
    self,
    f: Callable[[T], State[S, U]],
) -> State[S, U]:
    def run(state: S) -> tuple[U, S]:
        value, next_state = self.run(state)
        return f(value).run(next_state)

    return State(run)
```

The caller still controls when the whole description runs and which initial
state it receives.

## `get`, `put`, and `modify`

The Module 06 API includes three small descriptions:

```python
get()          # state -> (state, state)
put(new)       # state -> (None, new)
modify(f)      # state -> (None, f(state))
```

They are useful when a composed operation needs to inspect or replace state
without manually constructing `State`.

For example, update progress and keep the chunk as the main value:

```python
def account_chunk(chunk: Chunk) -> State[Progress, Chunk]:
    return modify(
        lambda progress: Progress(
            chunks=progress.chunks + 1,
            characters=(
                progress.characters + len(chunk.text)
            ),
        )
    ).map(lambda _: chunk)
```

The `map` restores the domain value after `modify` returns `None`.

## Compare State with a fold

If the only requirement is a final aggregate, a fold is clearer:

```python
final = reduce(
    lambda progress, chunk: Progress(
        chunks=progress.chunks + 1,
        characters=(
            progress.characters + len(chunk.text)
        ),
    ),
    chunks,
    Progress(),
)
```

Choose State when:

- several reusable operations update the same local state;
- those operations also pass meaningful values to dependent steps;
- the caller must choose the initial state; and
- the state transition should compose without manual tuple unpacking.

Choose a fold when:

- traversal and aggregation are the whole problem;
- only the final aggregate matters; and
- introducing `State[S, A]` would hide a straightforward reduction.

The module exercise asks you to justify this choice, not just implement the
State version.

## State is not shared mutable state

State does not provide:

- synchronization between threads or tasks;
- atomic updates to shared storage;
- persistence;
- crash recovery; or
- global progress reporting.

It models a local state transition as a value. Two calls to
`run_state(program, Progress())` are separate runs. If the application needs
shared concurrent progress, Module 08’s coordination rules and an appropriate
effect boundary are required.

## Layering State with failure requires a policy

These types do not mean the same thing:

```text
State[S, Result[A, E]]
Result[State[S, A], E]
```

In the first shape, running State produces both an updated state and a Result.
A failure value may therefore accompany state changes.

In the second shape, an outer `Err` means there is no State program to run.

Module 06 does not prescribe one large Reader-State-Result stack. If you layer
contexts, state the failure and state-retention policy first and test it.
[Layered Containers](layered-containers.md) develops that reasoning with the
smaller Result/Option case.

## What the laws allow

The State law tests compare both returned components after running from the
same initial state. They cover:

```text
left identity
right identity
associativity
get followed by put
put followed by get
modify with identity
```

Run them:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/test_state_laws.py
```

These laws support regrouping State descriptions. They do not prove the
progress formula is correct. The learning test supplies that application
evidence by asserting exact chunk and character counts.

## Common wrong turns

- **Mutating fields inside `State.run`.** The wrapper does not make in-place
  mutation referentially transparent.
- **Reading a module-global counter.** That removes the caller-supplied initial
  state and makes runs interfere.
- **Using State for a single sum.** A fold communicates simple aggregation
  more directly.
- **Asserting only the final count.** Compare the returned domain value, every
  state field, and the unchanged initial value.
- **Calling State concurrency-safe.** Local value threading is not
  synchronization.

## What the focused proof establishes

The learning test proves deterministic local progress for one ordered chunk
sequence, explicit initial and final states, and preservation of the original
frozen value.

It does not prove concurrency safety, persistence, or that State is preferable
to a fold for every aggregation.

Continue with [Error-Typed Flows](error-typed-flows.md), where the module
separates recoverable boundary failures from unexpected exceptions.
