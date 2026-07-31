# Isolating Side Effects

A RAG application must read input and write output. Purity does not remove those
effects. It gives them a narrow owner so the transformation between them can be
reasoned about as values.

Module 01 uses one boundary:

```text
rag_shell
  read CSV  ->  full_rag(docs, env)  ->  write JSONL
    effect             pure                 effect
```

The tracked state does not yet inject clocks, random sources, loggers, readers, or
writers. Those capabilities appear when later modules teach explicit context and
boundary protocols.

## Classify effects by observation

An effect is behavior that cannot be captured only by the returned value. Common
Python examples include:

- reading or writing files;
- printing or logging;
- accessing time, randomness, environment, or process state;
- mutating an argument, global, cache, or shared collection;
- performing network or database I/O.

This function returns a deterministic value but is still effectful:

```python
def clean_and_report(doc: RawDoc) -> CleanDoc:
    cleaned = clean_doc(doc)
    print(cleaned.doc_id)
    return cleaned
```

Replacing the call with `cleaned` removes output. Substitution changes behavior.

## Read the actual boundary

Module 01's `rag_shell.py` has one public function:

```python
def rag_shell(env: RagEnv, input_path: str, output_path: str) -> None:
    try:
        with open(input_path, encoding="utf-8") as input_file:
            reader = csv.DictReader(input_file)
            docs = [RawDoc(**row) for row in reader]
    except (UnicodeDecodeError, csv.Error, TypeError, ValueError) as exc:
        raise ValueError(
            f"Failed to read or parse CSV file '{input_path}': {exc}"
        ) from exc

    chunks = full_rag(docs, env)

    with open(output_path, "w", encoding="utf-8") as output_file:
        for chunk in chunks:
            json.dump(asdict(chunk), output_file, ensure_ascii=False)
            output_file.write("\n")
```

The exact local variable names may differ; the ownership does not.

### What the shell owns

- path interpretation;
- file lifetime;
- CSV parsing;
- conversion from untyped row mappings to `RawDoc`;
- JSON serialization;
- write ordering;
- translation of selected read/parse failures.

### What the pure core owns

- text normalization;
- chunk boundaries;
- deterministic embedding;
- structural deduplication;
- canonical result order.

If `full_rag` opened a path, its output would depend on external state. If
`rag_shell` implemented chunking, domain behavior would become harder to test without
I/O. The boundary separates those reasons to change.

## Resource lifetime is already visible

The `with` statements guarantee file handles are closed when their blocks exit,
including exceptional exits. That is a resource-safety fact, but Module 01 does not
yet build a general resource policy. Module 07 develops acquisition and release in
depth.

Keep the current claim narrow:

```text
the shell uses context managers for its two file handles
```

Do not generalize it to retries, transactional output, cancellation safety, or
multi-resource cleanup.

## Failure routes

### Input file cannot be opened

`FileNotFoundError` and `PermissionError` are not included in the shell's translated
exception tuple. They propagate from `open`. This is observable public behavior.
Module 01 does not yet provide a typed failure value.

### CSV row shape is invalid

If a row cannot construct `RawDoc`, the shell raises a `ValueError` with the input
path and chains the original exception.

### Output fails after partial writing

The shell writes directly to the destination. A disk or serialization failure may
leave a partial JSONL file. Module 01 makes no atomic-write guarantee.

### Pure core receives a valid but empty batch

`full_rag([], env)` returns an empty list. The shell creates an empty output file.
That is a domain outcome, not an exceptional boundary route.

These limitations matter because "thin shell" does not mean "production-complete
adapter."

## Do not inject unused capabilities

An environment bundle with logger, clock, and random source may look forward-thinking:

```python
@dataclass(frozen=True)
class Environment:
    log: Callable[[str], None]
    now: Callable[[], datetime]
    seed: int
```

If Module 01's RAG core does not use those capabilities, the bundle adds vocabulary
without solving a current pressure. It can also mislead learners into believing
dependency injection itself creates purity.

The Module 01 reference state therefore keeps only `RagEnv`, the configuration value
that directly determines chunk output.

## Testing the boundary honestly

Module 01 keeps core and boundary evidence separate:

| Proof | Observable claim | Deliberate limit |
| --- | --- | --- |
| `test_module_01_purity_foundations.py` | domain values and transformations obey six named laws | it performs no file I/O |
| `test_module_01_shell_boundary.py` | the CSV/JSONL adapter preserves successful values and follows four boundary routes | it does not make the shell pure or production-complete |

The tracked shell proof uses pytest's temporary directory and exercises this decision
table:

| Input route | Expected observation | Ownership established |
| --- | --- | --- |
| two valid rows | parsed JSONL equals `asdict` values from direct `full_rag`; source bytes are unchanged | the shell delegates domain meaning and only serializes the result |
| headers with no rows | the destination exists and is empty | an empty pure result is a successful domain outcome |
| row missing `abstract` | contextual `ValueError`; destination does not exist | row construction failure is translated before writing starts |
| missing input path | `FileNotFoundError`; destination does not exist | path-open failure propagates unchanged |

From the repository root, run the boundary proof:

```bash
make PROGRAM=python-programming/python-functional-programming \
  capstone-shell-proof
```

The equivalence assertion is made after JSON parsing, not by comparing raw JSON text.
Whitespace and object-key formatting belong to serialization; chunk field values and
line order belong to the boundary contract.

This proof still says nothing about atomic replacement, disk exhaustion, arbitrary
path security, concurrent writers, or recovery from a mid-write failure. It also
cannot establish the absence of every hidden effect: a return-value assertion would
still pass if `full_rag` logged secretly. Read `full_rag.py` and `rag_shell.py`
alongside the tests when reviewing effect ownership.

The order of operations is part of the current contract:

```text
open input -> parse all rows -> call full_rag -> open output -> write lines
```

That order explains why malformed input cannot create the destination, while a write
failure can leave a partial destination. A future streaming adapter could change the
failure timing and would need a different proof.

## Boundary review checklist

1. Which operation first observes external state?
2. Which operation last changes external state?
3. Is domain logic between them callable without I/O?
4. Who owns resource lifetime?
5. Which exceptions are translated, and which propagate?
6. Can output be partially written?
7. Are any injected capabilities unused?
8. Does the documentation claim only behavior that code and tests establish?

## Learner work

Run `capstone-shell-proof`, then inspect its four tests. For each test, identify the
first observation that would fail if domain work moved into the shell. Propose one
additional boundary case and state whether it belongs in Module 01 or requires a
later contract such as atomic output or streaming consumption.

Finally, draw the call boundary and mark every line that can observe or change
external state. Preserve the six-test core proof; boundary coverage is additive, not
a substitute for pure laws.

Continue with [Equational Reasoning](equational-reasoning.md), where the now-isolated
pure expressions can be rewritten under explicit laws.
