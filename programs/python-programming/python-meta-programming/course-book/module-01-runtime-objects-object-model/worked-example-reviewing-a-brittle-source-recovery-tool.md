# Worked Example: Reviewing a Brittle Source-Recovery Tool

The five core lessons in Module 01 are easiest to trust when they show up in one review
incident that feels tempting and flawed at the same time.

This example starts with a helper that looks clever in a small demo:

- it receives a function object
- it reads `func.__code__.co_filename`
- it reads `func.__code__.co_firstlineno`
- it scans the source file by indentation
- it claims to "recover the source" of the function

On a tiny script, that can appear to work. In a real codebase, it is brittle enough to
mislead reviewers and users.

That makes it the right worked example for Module 01.

## The incident

Assume a team built a debugging helper called `print_source(func)` to show "the real
implementation" of a callable during incident review.

The team reports four problems:

1. decorated functions often print wrapper code instead of the original implementation
2. nested functions lose their surrounding context and look harder to understand
3. REPL or notebook code raises file-related errors
4. formatting changes can break the indentation-based extraction logic

Every one of those failures is rooted in the Module 01 object model.

## The starting helper

```python
def print_source(func):
    code = func.__code__
    filename = code.co_filename
    start_line = code.co_firstlineno - 1

    if not filename or "<" in filename:
        raise OSError(f"Cannot read real file for {filename!r}")

    with open(filename, "r", encoding="utf-8") as handle:
        lines = handle.readlines()

    if start_line < 0 or start_line >= len(lines):
        raise ValueError("co_firstlineno is out of bounds for file")

    def_line = lines[start_line]
    def_indent = len(def_line) - len(def_line.lstrip(" \t"))
    result = [def_line]

    index = start_line + 1
    while index < len(lines):
        line = lines[index]
        stripped = line.lstrip(" \t")
        current_indent = len(line) - len(stripped)

        if stripped and current_indent <= def_indent and not stripped.startswith(")"):
            break

        result.append(line)
        index += 1

    while result and not result[-1].strip():
        result.pop()

    print("".join(result), end="")
```

The helper is not nonsense. That is exactly why it is a good teaching example.

It uses real runtime facts from the function object. The mistake is treating those facts
as a stable source-recovery contract.

## Step 1: name the exact object surface being used

Before judging the helper, classify its inputs:

- `func.__code__` is a code-object surface
- `co_filename` is metadata about where the code thinks it came from
- `co_firstlineno` is a starting-line hint

What is missing is just as important:

- no guaranteed end line
- no promise that the callable is the original undecorated function
- no promise that the filename points to a normal readable file

This is the first repair in thinking:

> the helper is built on diagnostic surfaces, not on a supported source-recovery API.

That alone should lower your confidence immediately.

## Step 2: explain why decorated functions fail

Suppose the codebase contains:

```python
def decorated(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@decorated
def multiply(x, y):
    return x * y
```

If you pass `multiply` into `print_source`, the function object you are inspecting is
often the wrapper returned by the decorator, not the original undecorated function.

That failure is pure Module 01:

- function objects are ordinary runtime objects
- decorators can replace one function object with another
- source recovery based on the current function object's `__code__` therefore follows the
  replacement, not your intention

The helper is not "slightly off." It is answering a different question than the team
thinks it is answering.

## Step 3: explain why nested functions lose context

Now consider:

```python
def outer(base):
    def inner(value):
        return value + base
    return inner
```

If you recover the source of `outer(5)`, you may only extract the nested `inner`
definition without the surrounding scope that gives `base` meaning.

Again, this is a Module 01 object-model issue:

- the returned callable is a function object with closure state
- the closure carries captured bindings, not rich source context
- code-object line metadata is not a complete model of lexical meaning

The function still works because closures are runtime objects. The source-recovery helper
still fails because it is trying to reconstruct source-level context from insufficient
runtime metadata.

## Step 4: explain why non-file contexts fail

Interactive and generated environments make the problem worse.

In a REPL, notebook, zipapp, or tool-managed runtime:

- `co_filename` may point to a synthetic label like `"<stdin>"`
- the original file may not exist anymore
- the code may have been transformed before execution

The helper reacts by raising `OSError`, but the deeper lesson is broader:

> a function object is real even when its original source file is absent, synthetic, or
> transformed.

That is why source recovery is the wrong mental model for the core runtime object lesson.

## Step 5: formatting breaks the heuristic even in files

Even in ordinary files, indentation scanning is a weak boundary detector.

Small changes can break it:

- multi-line signatures
- decorators above the function
- nested definitions
- comments and blank lines arranged unexpectedly
- code generators or formatters that alter layout without changing meaning

That is a useful Module 01 warning sign:

> if a runtime trick depends on surface formatting to recover semantics, it is already too
> far from the object model to trust as a core capability.

## A stronger first move: ask for supported introspection first

If the real goal is debugging or review, a better first move is usually:

- `inspect.signature(func)`
- `func.__name__`
- `func.__qualname__`
- `func.__module__`
- `inspect.getsource(func)` when available, with a clear failure path

That is not perfect either, but it is a healthier contract:

- use supported introspection first
- treat source retrieval as conditional
- fail clearly instead of pretending a heuristic is ground truth

## A healthier rewrite

```python
import inspect


def describe_function(func):
    print("name:", func.__name__)
    print("qualified name:", func.__qualname__)
    print("module:", func.__module__)
    print("signature:", inspect.signature(func))

    try:
        source = inspect.getsource(func)
    except OSError as exc:
        print("source unavailable:", exc)
    else:
        print(source.rstrip())
```

This rewrite is more honest because it does not claim that the runtime object model can
guarantee source reconstruction. It reports what the function object actually knows and
then asks a supported helper for source when possible.

## What this example teaches about Module 01

This worked example ties the module together:

- functions are runtime objects with metadata and code objects
- decorators can replace one function object with another
- closures carry runtime bindings, not recovered source context
- modules matter because filenames and globals come from runtime context, not from abstract source alone
- supported and diagnostic surfaces must be kept separate

That is the real lesson. The helper fails not because Python is inconsistent, but because
the tool asked the runtime object model to promise more than it actually promises.

## The review loop to keep

When you meet a clever introspection helper, run this loop:

1. name the exact object surfaces it depends on
2. classify those surfaces as supported or diagnostic-only
3. list the runtime situations where the helper's assumptions stop holding
4. rewrite the tool around supported facts first

If you can do that here, Module 01 has done its job and Module 02 can teach safe
inspection with much less ambiguity.
