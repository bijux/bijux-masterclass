# Module 06 Glossary

Use these meanings while reading Module 06. The terms describe observable
FuncPipe behavior, not merely page titles.

## Flow operations

| Term | Meaning in this module |
| --- | --- |
| context | A rule surrounding a value, such as possible failure, successful absence, read-only environment, changing local state, or ordered trace data. |
| `map` | Apply `T -> U` to a successful or present value while preserving the surrounding context. |
| `map_err` | Transform the error value of a Result without changing a success. This changes the error vocabulary and should preserve useful provenance. |
| `and_then` / bind | Apply `T -> Context[U]` to a successful value and keep one context layer. For Result and Option, the stopping variant skips the function. |
| short-circuit | Preserve a stopping case such as `Err` or `NoneVal` without evaluating the next dependent operation. |
| lift | Apply a plain function to values already inside one or more contexts without rewriting the plain function to accept containers. |
| applicative combination | Combine contextual inputs whose values do not depend on one another. Result remains fail-fast in Module 06; Validation accumulates independent failures. |
| dependent step | An operation that cannot run until an earlier operation produces a successful value. |
| independent input | An input that can be checked or produced without the successful value of another input. |

## Laws and evidence

| Term | Meaning in this module |
| --- | --- |
| left identity | Introducing a value with the context’s success constructor before bind does not change the next operation’s result. |
| right identity | Binding a contextual value to its success constructor preserves the original contextual value. |
| associativity | Regrouping dependent operations without reordering them preserves the contextual result. |
| functor composition | Two pure `map` operations agree with one `map` containing the same composed function order. |
| law property | A property-based test of a structural rule over a bounded generated domain. It is not proof of a RAG business policy. |
| characterization test | A test that records existing public behavior before a refactor, whether or not that behavior is ideal. |
| equivalence property | A comparison of before and after observations over generated inputs. It supports preservation, not design superiority. |

## Explicit contexts

| Term | Meaning in this module |
| --- | --- |
| Reader | A description equivalent to `Environment -> Value`, with operations for composing computations that share a read-only environment. |
| `ask` | A Reader description that returns the complete environment. |
| `asks` | A Reader description that selects a value from the environment. |
| `local` | Run a Reader description with a derived environment for that run. It does not mutate the caller’s environment. |
| State | A description equivalent to `State -> (Value, State)`, used for explicit local state transitions. |
| initial state | The state value supplied by the caller to `run_state`; it is part of the program input. |
| Writer | A description that returns a payload and ordered trace entries without emitting them externally. |
| `tell` | A Writer description whose payload is `None` and whose meaningful output is one trace entry. |
| payload preservation | A wrapper returns the same domain value while adding context such as trace data or metrics. |

## Layering and boundaries

| Term | Meaning in this module |
| --- | --- |
| outer context | The first decision in a nested type. In `Result[Option[T], E]`, retrieval success or failure is decided before presence or absence. |
| layer order | The arrangement of two contexts; changing it can change failure, absence, state-retention, or trace-retention behavior. |
| transpose | Convert between two supported layer orders while preserving every modeled case. |
| successful absence | An operation completed correctly but found no value, represented by `Ok(NoneVal())` in the retrieval example. |
| expected exception | A named exception from a narrow boundary operation that the caller can handle as a typed result. |
| unexpected exception | A defect or unmodeled failure that remains raised rather than being mislabeled as a domain error. |
| exception bridge | An adapter that runs one throwing operation, catches only declared expected classes, and maps them to `Result` or `Validation`. |
| assembly-time policy | Choosing wrappers while building a callable so the domain function does not inspect feature flags during every run. |
| endomorphic validator | A validator shaped `T -> Result[T, E]`; success preserves the input type so an existing pipeline can follow. |

## Application terms

| Term | Meaning in this module |
| --- | --- |
| preservation claim | The earlier FuncPipe observation that must remain equal after a flow refactor: normalized values, chunk boundaries, order, embeddings, or error provenance. |
| call trace | A test-owned list recording which operations ran. It proves skipped or exactly-once work when result equality cannot. |
| context ledger | A comparison of the simplest direct representation with Reader, State, Writer, Result, or a wrapper, including the evidence required to justify the choice. |
| Module 06 reference state | `capstone/module-reference-states/module-06/`, the completed code and tests for explicit flow context before Module 07 effects. |
