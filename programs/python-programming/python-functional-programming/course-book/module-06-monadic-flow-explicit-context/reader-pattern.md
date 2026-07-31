# Reader: Make Shared Read-Only Context Explicit

`iter_chunk_doc` already accepts `RagEnv` as an ordinary argument:

```python
chunks = list(iter_chunk_doc(doc, env))
```

That is often the best design. One function needs one value, and the
dependency is visible.

Reader becomes interesting when several reusable operations need the same
read-only environment and repeated argument threading obscures the flow.
Reader packages a function of the form `Environment -> Value` and gives those
functions `map` and `and_then`.

The goal is not to eliminate closures. Reader itself is built from closures.
The goal is to make the shared environment an explicit part of the program’s
type and to supply it at one visible run boundary.

## Read the type as a function

For this module:

```text
Reader[RagEnv, list[str]]
```

means approximately:

```text
RagEnv -> list[str]
```

The value is a description waiting for an environment. Constructing it does
not chunk the document. Calling `.run(env)` does.

This distinction will matter again in Module 08, where constructing an async
description and executing it are separate events.

## Run one chunk program with two environments

The learning proof fixes the document and the Reader program:

```python
doc = CleanDoc(
    doc_id="reader",
    title="Reader",
    abstract="abcdefghij",
    categories="fp",
)

program: Reader[RagEnv, list[str]] = asks(
    lambda env: [
        chunk.text
        for chunk in iter_chunk_doc(doc, env)
    ]
)
```

Only the environment changes:

```python
assert program.run(
    RagEnv(chunk_size=4)
) == ["abcd", "efgh", "ij"]

assert program.run(
    RagEnv(chunk_size=6)
) == ["abcdef", "ghij"]
```

Run the proof:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k reader_runs_same_rag_chunk_program_with_explicit_env
```

Predict the chunk lists before running. The useful observation is not merely
that the two outputs differ. It is that the same program value receives both
policies at `.run`.

## The implementation is ordinary function composition

The Module 06 Reader has one field:

```python
@dataclass(frozen=True)
class Reader(Generic[C, T]):
    run: Callable[[C], T]

    def map(self, f: Callable[[T], U]) -> Reader[C, U]:
        return Reader(lambda cfg: f(self.run(cfg)))

    def and_then(
        self,
        f: Callable[[T], Reader[C, U]],
    ) -> Reader[C, U]:
        return Reader(
            lambda cfg: f(self.run(cfg)).run(cfg)
        )
```

`map` runs the existing description with an environment, then applies a plain
transformation.

`and_then` runs the first description, uses its value to choose a second
Reader, and supplies the same environment to that second description.

No dependency injection framework is involved. The environment is an ordinary
immutable value.

## Four primitives and their meanings

```python
reader_pure(value)
```

Creates a Reader that ignores its environment and returns `value`.

```python
ask()
```

Returns the complete environment.

```python
asks(lambda env: env.chunk_size)
```

Selects one value from the environment.

```python
local(change, program)
```

Runs `program` with a derived environment without changing the caller’s
original value.

`local` should be used sparingly. If local overrides become common, the
environment may contain unrelated policies that should have separate owners.

## Compose only when composition clarifies ownership

Suppose two projections share `RagEnv`:

```python
chunk_size = asks(lambda env: env.chunk_size)
overlap = asks(lambda env: env.overlap)
```

You can combine them:

```python
policy = chunk_size.and_then(
    lambda size: overlap.map(
        lambda amount: (size, amount)
    )
)
```

Both descriptions receive the same `RagEnv`. The example is useful for reading
Reader mechanics, but constructing `(env.chunk_size, env.overlap)` directly is
clearer in production code. An abstraction must improve the surrounding
design, not merely demonstrate that it can express a tuple.

Reader is more justified when:

- several reusable steps share the same environment;
- the caller should select the environment once;
- subprograms must compose without expanding every intermediate signature; and
- tests benefit from running one unchanged program under controlled
  environments.

## Ordinary arguments, closure capture, and Reader

These are all valid tools:

| Shape | Good fit | Main review question |
| --- | --- | --- |
| `f(value, env)` | one or a few local calls | Is the dependency already clear enough? |
| closure capturing `env` | a small configured callable | Can the caller still see and replace the captured value? |
| `Reader[Env, A]` | several composable descriptions share one environment | Does the added type make dependency flow easier to inspect? |

Closure capture is not automatically hidden or untestable. A factory such as
`make_chunker(env)` can be explicit and easy to test. Reader is one disciplined
representation for repeated shared-context composition, not a universal
replacement.

## Reader does not execute effects safely

This is a dangerous inference:

```python
Reader(lambda env: open(env.path).read())
```

Wrapping file I/O in Reader does not make it pure, close the file, classify
errors, or provide a resource boundary. It merely delays a function that still
performs I/O.

In Module 06, the Reader example calls the pure `iter_chunk_doc`. Module 07
introduces ports, adapters, and resource ownership for actual effects.

## Laws are compared at a supplied environment

Reader objects contain functions, so their law tests compare runs:

```text
reader_pure(x).and_then(f).run(env)
==
f(x).run(env)
```

The suite checks left identity, right identity, associativity, `ask` identity,
and `local` composition over generated values and environments.

Run it:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/test_reader_laws.py
```

The laws support regrouping Reader descriptions. They do not prove that the
environment has the right fields, that chunking policy is correct, or that a
function inside Reader is free of effects.

## Common wrong turns

- **Wrapping a single argument automatically.** An ordinary parameter is
  usually clearer.
- **Calling Reader “no closures.”** Reader stores a callable and is commonly
  implemented with closures.
- **Putting mutable services in a value called config.** Read-only context and
  effectful capabilities have different ownership concerns.
- **Building one enormous environment.** A type containing every application
  dependency hides which subprogram needs what.
- **Claiming `.run(test_env)` proves purity.** Replaceability is useful, but it
  does not remove effects from the supplied function.

## What the focused proof establishes

The learning test proves that:

- one Reader program accepts its `RagEnv` at execution;
- two environments produce the exact expected chunk sequences; and
- there is no module-global chunk size in that tested route.

It does not prove that Reader should replace every `RagEnv` parameter or that
all operations placed inside Reader are pure.

Continue with [Explicit State Threading](explicit-state-threading.md). The
environment there changes between operations, so the observable type becomes
`State -> (Value, State)`.
