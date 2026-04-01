<a id="top"></a>
# Module 4: Decorators Level 1 – Function Transformation Basics

<a id="toc"></a>
## Table of Contents

1. [Introduction](#introduction)
2. [Core 16: Nested Functions → Functions That Return Functions](#core16)
3. [Core 17: @decorator Syntax Is Just func = decorator(func)](#core17)
4. [Core 18: First Real Decorators: @timer, @once, @deprecated](#core18)
5. [Core 19: functools.wraps and Writing Your Own Identity-Preserving Wrapper](#core19)
6. [Synthesis: Controlled Transformation of First-Class Functions](#synthesis)
7. [Capstone: @cache - Didactic Memoization from Scratch](#capstone)
8. [Glossary (Module 4)](#glossary)

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="introduction"></a>
## Introduction   

Building on Module 1’s foundation—functions as first-class, metadata-rich callables—and Modules 2–3’s introspection tools for safe attribute probing and signature inspection, we now move to the first truly *transforming* layer of metaprogramming: decorators. A decorator is a callable that takes a function (the decoratee) and returns a new callable with augmented behaviour; the `@decorator` syntax is just `f = decorator(f)` written declaratively. This mechanism lets you inject cross-cutting concerns such as logging, timing, validation, and memoization cleanly, without editing the original function body.

(Typing aside: writing decorators that keep static type checkers happy is non-trivial. Python 3.10’s `ParamSpec` and `Concatenate` (PEP 612) allow decorators to preserve the original function’s parameter types in type-checker land. This module stays focused on runtime mechanics; decorator typing patterns are taken up briefly in Module 5 and in more depth in later volumes.)

This module develops decorators through four practical pillars:

- **Core 16: Nested functions** – functions that return functions; closures as the mechanical basis for decorators.  
- **Core 17: `@decorator` syntax** – `@d` and `@d1 @d2` as `f = d(f)` / `f = d1(d2(f))`.  
- **Core 18: First real decorators** – `@timer`, `@once`, `@deprecated` as practical, stateful examples.  
- **Core 19: `functools.wraps`** – identity-preserving wrappers that keep names, docs, and signatures intact.  

The capstone introduces a didactic `@cache` decorator: a manual, single-threaded memoization layer that intentionally stops short of production quality and serves as a contrast class to `functools.lru_cache`.

Each core follows the standard structure introduced in the book’s introduction.

We also make the risk profile explicit:

- Simple decorators (`@timer`, `@deprecated`, thin wrappers with `@wraps`) are generally safe in library and application code when they remain transparent and side-effect-free apart from their advertised concern.  
- Stateful decorators (`@once`, `@cache`, retries, rate-limits) change semantics and can interact badly with concurrency, recursion, and mutability. These must be treated as *small frameworks*, designed with clear contracts and explicit limitations, not as throwaway syntactic sugar.  
- All stateful patterns shown in this module are **single-threaded and synchronous**; they deliberately ignore locks, async/await, and process-level coordination. Concurrency-safe and async-aware variants are deferred to later volumes.

The goal is to make you fluent with decorator mechanics (nested functions, `@` syntax, wrapping, identity preservation) and disciplined about their use: you should be able to read and write decorators that are transparent, introspection-friendly, and honest about their costs, and to recognise immediately when a decorator has crossed the line from “thin wrapper” into “small framework” with semantic and concurrency implications.

```mermaid
graph TD
  subgraph DefinitionTime["Definition time"]
    decorated["`@decorator` or `@factory(config)` on `func`"]
    build["`decorator(func)` builds `wrapper`"]
    wraps["`@functools.wraps(original_func)` copies metadata and sets `__wrapped__`"]
    closure["`wrapper` closes over `original_func` and decorator state"]
    rebind["Module name `func` now points to `wrapper`"]
    stack["Stacked decorators nest right-to-left: `func = d3(d2(d1(func)))`"]
    decorated --> build --> wraps --> closure --> rebind --> stack
  end

  subgraph CallTime["Call time"]
    caller["Caller executes `func(*args, **kwargs)`"]
    pre["Pre-call logic<br/>timers, cache lookup, warnings, validation"]
    original["Call closed-over `original_func(*args, **kwargs)`"]
    post["Post-call logic<br/>logging, cache store, counters, LRU updates"]
    result["Return transformed result to caller"]
    caller --> pre --> original --> post --> result
  end
```

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="core16"></a>
## Core 16: Nested Functions → Functions That Return Functions

### Canonical Definition

A decorator is fundamentally a callable that accepts a function (the decoratee) as its argument and returns a new callable with augmented behaviour. This is achieved via nested functions: the outer (decorator) function defines the inner (wrapper) function, which captures the decoratee and additional state via closures (Module 1, `__closure__`). The wrapper implements the enhanced `__call__` protocol, delegating to the decoratee after or around custom logic. Formally, for a decorator `d` and function `f`, `d(f)` yields `w` such that `w(*args, **kwargs)` executes pre/post logic and invokes `f(*args, **kwargs)`, preserving the original return value and call semantics (metadata such as the visible signature is only preserved if you additionally use tools like `functools.wraps` or explicit `__signature__` assignment).

### Deep Dive Explanation

Nested functions unlock decorators by encapsulating the decoratee and configuration within a closure, leveraging Python's lexical scoping for state isolation without global variables. This pattern—outer accepts callable, inner wraps invocation—mirrors higher-order functions but specialises for transformation, enabling patterns like logging or retries without subclassing. Historically, decorators were formalised in PEP 318 (2003, Python 2.4) as syntactic sugar atop this nesting, but the mechanics trace to closures in Python 2.2. Why nesting? It ensures the wrapper "remembers" the decoratee without shared module-level state, tying to Module 2's `callable` for runtime checks (e.g., `if not callable(func): raise TypeError`) and back to Module 1’s `__closure__` cells as the concrete runtime vehicle for “remembering” `func` and any decorator state. Pedagogically, start here to demystify: the wrapper is a proxy, not a replacement—trace delegation to verify equivalence, then augment for transformation.

### Examples

Basic nesting without augmentation (manual wrapper, no `@` syntax yet):

```python
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    # NOTE: must return the new wrapper; if we forget this, simple_decorator(greet)
    # would return None and replace the original function with a non-callable.
    return wrapper

def greet(name):
    return f"Hello, {name}!"

greet_wrapped = simple_decorator(greet)  # manual wrapping: what @simple_decorator automates
print(greet_wrapped("Alice"))  # Calling greet\nHello, Alice!
# Trace: wrapper captures func via closure (co_freevars=('func',)); delegates args/kwargs; prints pre-call.
```

With state (counter via closure):

```python
def counter_decorator(func):
    count = 0  # Closed over by wrapper
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"Call {count} to {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@counter_decorator
def add(x, y):
    return x + y

print(add(2, 3))  # Call 1 to add\n5
print(add(4, 1))  # Call 2 to add\n5

@counter_decorator
def multiply(x, y):
    return x * y

print(multiply(2, 3))  # Call 1 to multiply\n6
print(multiply(4, 1))  # Call 2 to multiply\n4
# Trace: Each wrapper instance has independent count (separate closures); nonlocal mutates closure cell.

# These first examples deliberately omit functools.wraps so you can see the raw
# “outer defines inner, then return inner” pattern. In real code you almost
# always combine this structure with functools.wraps to preserve the original
# function’s name, docstring, and signature (developed fully in Core 19).
```

### Advanced Notes and Pitfalls

- Wrapper must accept `*args, **kwargs` to forward arbitrary signatures (Core 11 preview).
- Pitfall: Forgetting `nonlocal` in Python 3 for mutable closure vars—assigns locally, breaking state.
- Pitfall: Infinite recursion if the wrapper rebinds the original function name (e.g., `func = wrapper` inside wrapper) and calls the global name instead of the closed-over `func`. Always delegate to the closed-over `func`, not a rebinding-prone global.
- Pitfall: Forgetting to return wrapper from the decorator body—at decoration time the function name will be rebound to None instead of a callable, and every call will fail immediately.
- Pitfall: The wrapper must propagate exceptions unchanged unless the decorator explicitly documents new error behaviour; swallowing or rewriting errors silently makes debugging significantly harder.
- Extension: Use Module 2 `callable(func)` for runtime checks.

### Exercise

Implement `log_calls(func)` nesting a wrapper that logs args/kwargs pre-call (format: "func(args=..., kwargs=...)"). Test on variadic (e.g., `sum(iterable)`); verify closure isolation by applying to two functions—counters independent.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="core17"></a>
## Core 17: @decorator Syntax Is Just func = decorator(func)

### Canonical Definition

The `@decorator` syntax (PEP 318) is syntactic sugar for function assignment: `@d` atop `def f(): ...` equates to `f = d(f)`, where `d` (or the result of evaluating the decorator expression) is evaluated once at definition time, transforming `f` post-body execution. Multiple decorators stack right-to-left: if `@d_outer` is written above `@d_inner`, the result is `f = d_outer(d_inner(f))`; more generally, `@d2 @d1 def f(): ...` becomes `f = d2(d1(f))`. The decoratee `f` is the raw function object (Module 1), passed unbound; the result replaces `f` in the namespace.

### Deep Dive Explanation

This syntax elevates nesting from verbose wrapping (`f = d(f)`) to declarative, reading as "apply d to f"—enhancing readability for chains like `@timer @validate`. Evaluation at definition ensures the *transformation step* itself runs once at definition/import time instead of on every call; the resulting wrapper still adds its own per-call overhead, as any additional logic would. Historically, proposed for clarity over manual calls, it integrates with Module 3's `getsource` (decorators excluded from `co_firstlineno`). Why sugar? Reduces boilerplate while preserving semantics: the transformed `f` retains invocability (Core 9). Pedagogically, equate `@d def f(): pass` to manual—trace `id(f)` pre/post to confirm replacement, then stack for composition.

#### Diagram: How `@decorator` and stacked decorators compose

```text
Diagram: Decorator Application & Composition (@-syntax desugared)
==================================================================

1. Definition time - single decorator (executed once)
-----------------------------------------------------

Source code:                              Desugared exactly to:

    @d                                        def f(...):
    def f(...):                                   body                  # raw function object
        body

                                              f = d(f)                  # wrapper returned
                                                                        # name "f" now = wrapper


2. Definition time - stacked decorators (bottom -> top application)
-------------------------------------------------------------------

Source code:                              Step-by-step desugaring:

    @d3                                       def f(...):
    @d2                                           body                  # raw original f
    @d1
    def f(...):                               f = d1(f)                 # innermost first
        body                                  f = d2(f)                 # middle wrapper
                                              f = d3(f)                 # outermost last
                                                                        # final f = d3(d2(d1(f)))

Pipeline (what name "f" refers to after decoration):

original f --> [d1 wrapper] --> [d2 wrapper] --> [d3 wrapper]
                                                     ^
                                                     final binding of name "f"


3. Call time - execution order on every f(...)
-----------------------------------------------

caller calls:  f(args, kwargs)

               |
               v
   outermost wrapper (d3)   <-- applied last at definition time
               |
               v
      middle wrapper (d2)
               |
               v
   innermost wrapper (d1)   <-- applied first at definition time
               |
               v
   original function body executes
               |
               v
   result returns upward: d1 -> d2 -> d3 -> caller
```

In other words: decoration (`f = d3(d2(d1(f)))`) happens once at import/definition time; the chain of wrapper calls runs on every invocation of `f`.

### Examples

Single decorator:

```python
def uppercase(func):
    def wrapper(text):
        return func(text).upper()
    return wrapper

@uppercase
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # HELLO, ALICE!
# Trace: Equivalent to greet = uppercase(greet); wrapper delegates text, uppercases return.
```

Stacked (right-to-left):

```python
def add_exclaim(func):
    def wrapper(text):
        return func(text) + "!"
    return wrapper

def trim(func):
    def wrapper(text):
        return func(text.strip())
    return wrapper

@add_exclaim
@trim
@uppercase
def message(text):
    return f"{text} world"

print(message("  hello  "))  # HELLO WORLD!
# Trace: message = add_exclaim(trim(uppercase(message))); innermost uppercase, then trim input, exclaim output.
```

### Advanced Notes and Pitfalls

- Decorators apply to `def`/`async def`/`class`; for lambdas, manual.
- Pitfall: Decorator factories return decorator functions—`@factory(arg)` first evaluates `factory(arg)` once at definition time to obtain a decorator, then applies that decorator to the function (`f = factory(arg)(f)`).
- Pitfall: Syntax errors in decorator propagate at definition (e.g., `TypeError` if non-callable).
- Extension: Use Module 2 `type(func)` to classify decoratee pre-wrap.

### Exercise

Apply stacked `@uppercase @add_exclaim` to a function returning lowercase; verify composition by printing intermediates (e.g., manual `upper_then_exclaim`). Induce pitfall: pass non-callable to `@`—trace error timing.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="core18"></a>
## Core 18: First Real Decorators: @timer, @once, @deprecated

### Canonical Definition

Practical decorators transform via domain-specific logic: `@timer` measures execution (time.perf_counter); `@once` enforces idempotency (singleton execution per decorated function, ignoring subsequent arguments); `@deprecated` warns on use (warnings.warn, PEP 387). Each returns a wrapper delegating to the decoratee, injecting pre/post actions while preserving return value and raising exceptions unchanged.

### Deep Dive Explanation

These exemplars illustrate decorators' utility: timing for profiling, once for lazy init, deprecation for API evolution—each exploiting `*args, **kwargs` forwarding and closure-based state. They build on Core 16 nesting, using Module 2 `callable` implicitly via delegation. Historically, `@timer` echoes profiling tools (cProfile), `@once` singleton-style initialization patterns, `@deprecated` maintenance best practices. We chose exactly these three because they match real production concerns:

- `@timer` – measuring execution time of hot paths using `time.perf_counter`.
- `@once` – one-time initialization with cached state on the wrapper (e.g. `_once_result`).
- `@deprecated` – signalling obsolete APIs via `warnings.warn` at the call site.

Together they show that the same decorator skeleton can support timing, caching-like one-shot behavior, and API lifecycle signalling with only small changes to the wrapper body. Pedagogically, trace `@timer`: wrapper times delta, prints, delegates—extend to log files for realism.

### Examples

@timer:

```python
import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"{func.__name__} took {elapsed:.4f}s")
    return wrapper

@timer
def slow_compute(n):
    time.sleep(n / 10)
    return n ** 2

print(slow_compute(5))  # slow_compute took 0.5001s\n25
# Trace: perf_counter monotonic; delegates result; prints post, even on exceptions.
```

@once (idempotent, per-function execution):

```python
import functools

def once(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, '_once_result'):
            wrapper._once_result = func(*args, **kwargs)
        return wrapper._once_result
    return wrapper

@once
def expensive_setup():
    print("Setting up once...")
    return "initialized"

print(expensive_setup())  # Setting up once...\ninitialized
print(expensive_setup(ignored_arg=42))  # initialized (ignores args after first call)
# Trace: Instance attr for state (per decorated function object, thread-unsafe); skips on second+ call.
```

@deprecated:

```python
import warnings
import functools

def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is deprecated; use alternative.",
            DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)
    return wrapper

@deprecated
def old_api(value):
    return value * 2

print(old_api(3))  # /path:1: DeprecationWarning: old_api is deprecated; use alternative.\n6
# Trace: warn at caller level; stack shows user frame; delegates unchanged.
```

Notice that `@timer`, `@once`, and `@deprecated` now all use `functools.wraps` on their inner wrapper to keep the original function’s name, docstring, and signature intact. In the earlier “bare” examples in Core 16 we skipped this on purpose so you could see the core wrapping pattern; Core 19 will dig into `functools.wraps` and identity preservation in depth.

### Advanced Notes and Pitfalls

- @timer: Use `timeit` for repeats; contextlib for RAII-style. Our implementation uses try/finally, so timing reports even on exceptions.
- @once: Thread-unsafe (use a lock for concurrency); semantics are per-decorated-function execution, not per-argument memoization:
  - if the first call raises, no result is cached and later calls will re-run the function;
  - after the first successful call, all subsequent calls ignore their arguments entirely.
- @deprecated: Version in message; stacklevel=2 for caller frame. Note: Users can silence `DeprecationWarning` via the warnings filter; if the deprecation is critical, you may choose to raise instead in a future version.
- Pitfall: If try/finally is omitted, exceptions bypass post-logic—always include it for robustness.
- Extension: Combine `@once @timer`—order matters: `@once @timer` skips timer after first call (once caches pre-timer); `@timer @once` runs timer on every call (once inside timer).

### Exercise

Implement `@retry(times=3)`: wraps, catches Exception, retries up to times (exponential backoff optional). Test on failing func; verify deprecation in `@deprecated @retry`.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="core19"></a>
## Core 19: functools.wraps and Writing Your Own Identity-Preserving Wrapper

### Canonical Definition

`functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)` is a decorator factory yielding a wrapper that copies attributes from `wrapped` (e.g., `__name__`, `__doc__`, `__module__`) to preserve identity for introspection (Module 1). `WRAPPER_ASSIGNMENTS` = `('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')`; `WRAPPER_UPDATES` = `('__dict__', '__wrapped__')`. Custom wrappers replicate via `setattr(wrapper, attr, getattr(wrapped, attr, None))`. This is the formal tool that makes the forward references in Core 16 and Core 18 concrete.

### Deep Dive Explanation

Bare wrappers lose metadata (`wrapper.__name__ == 'wrapper'`), confounding tools like `help` or `inspect.signature` (Module 3)—`@wraps` restores via assignment, setting `__wrapped__` for unwrapping (e.g., `inspect.unwrap`). Historically, `functools` (2.5) standardised amid decorator proliferation. Why preserve? Maintains debuggability: tracebacks show original names, signatures bind correctly. Ties to Module 1 `__qualname__` (nesting) and Module 2 `vars` (inspect state). Pedagogically, contrast bare vs wrapped: `inspect.signature` fails on bare—use `@wraps` universally for professionalism.

```text
Diagram: functools.wraps – Preserving Function Identity
=================================================================

1. Bare decorator – identity destroyed
--------------------------------------

    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    @decorator
    def original(x: int, y: int) -> int:
        """Add two numbers."""
        return x + y

Result → wrapper overwrites everything:

```mermaid
graph TD
  broken["Decorated function without `@wraps`"]
  broken --> name["`__name__ = \"wrapper\"`"]
  broken --> qualname["`__qualname__ = \"wrapper\"`"]
  broken --> doc["`__doc__ = None`"]
  broken --> annotations["`__annotations__ = {}`"]
  broken --> wrapped["`__wrapped__` missing"]
```

Real-world breakage
• help(), Sphinx, docstrings → empty or wrong
• inspect.signature → (*args, **kwargs)
• Tracebacks, debuggers, IDEs → "wrapper"
• Type checkers, pydantic, serializers → lost hints


2. With @functools.wraps – identity fully restored
--------------------------------------------------

    import functools

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

Result → wrapper is indistinguishable from original:

```mermaid
graph TD
  preserved["Decorated function with `@functools.wraps`"]
  preserved --> name["`__name__ = \"original\"`"]
  preserved --> qualname["`__qualname__ = \"original\"`"]
  preserved --> doc["`__doc__` preserved"]
  preserved --> annotations["`__annotations__` preserved"]
  preserved --> module["`__module__` preserved"]
  preserved --> dict["`__dict__` mirrors original"]
  preserved --> wrapped["`__wrapped__ = original func`"]
```


3. What @functools.wraps actually does
--------------------------------------

Copies directly:
    __module__, __name__, __qualname__, __doc__, __annotations__

Merges:
    wrapper.__dict__.update(func.__dict__)

Adds:
    wrapper.__wrapped__ = func


4. Introspection now works perfectly
------------------------------------

• inspect.signature → (x: int, y: int) -> int
• help(), Sphinx, IDEs → correct name/doc/annotations
• Tracebacks/debuggers → real function name
• inspect.unwrap → original undecorated function


Non-negotiable rule for every decorator you write
-------------------------------------------------

    @functools.wraps(func)   # always on the innermost wrapper

Omitting it silently breaks every tool that depends on correct metadata.
Never publish a decorator without it.
```

### Examples

Bare vs preserved:

```python
import functools
import inspect

def bare_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def preserved_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bare_decorator
def bare_func(x):
    """Bare doc."""
    return x

@preserved_decorator
def preserved_func(x):
    """Preserved doc."""
    return x

print(bare_func.__name__)  # wrapper
print(preserved_func.__name__)  # preserved_func
print(inspect.signature(bare_func))  # (*args, **kwargs) — lost
print(inspect.signature(preserved_func))  # (x) — retained
print(preserved_func.__doc__)  # Preserved doc.
# Trace: wraps copies at wrap time; __wrapped__ enables inspect.unwrap(bare_func) → original (3.4+).
```

Custom preservation in a decorator:

```python
def custom_wraps(wrapped):
    def decorator(inner):
        inner.__name__ = wrapped.__name__
        inner.__doc__ = wrapped.__doc__
        inner.__module__ = wrapped.__module__
        inner.__wrapped__ = wrapped
        return inner
    return decorator

def my_decorator(func):
    @custom_wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@my_decorator
def example(x):
    return x * 2

print(example.__name__)  # example — copied
# Trace: custom_wraps as factory; used in decorator for reusable pattern.
```

### Advanced Notes and Pitfalls

- `__wrapped__` chains for stacked (inspect.unwrap recurses).
- Pitfall: wraps copies at decoration—mutations post-wrap (e.g., `__doc__=`) not reflected; re-decorate if needed.
- Pitfall: C functions lack some attrs—wraps skips gracefully.
- Extension: For advanced cases (e.g., decorators that change the calling convention), you can override the visible signature explicitly via `inner.__signature__ = inspect.signature(wrapped)` so that Module 3 tooling built on `inspect.signature` still reports the callable correctly.

### Exercise

Refactor `@timer` with `@wraps`; verify `help(timer_func)` shows original doc/name. Implement custom `my_wraps` copying extras (`__annotations__`); test on annotated func—trace signature retention.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="synthesis"></a>
## Synthesis: Controlled Transformation of First-Class Functions

Cores 16–19 take the static object model and introspection machinery from Modules 1–3 and make it *transforming*:

- Core 16 (nested functions) shows how closures let you build wrappers that remember the original function and any decorator state.
- Core 17 (`@decorator` syntax) turns explicit `f = d(f)` wiring into declarative annotations, stacking multiple transformations predictably.
- Core 18 (e.g. `@timer`, `@once`, `@deprecated`) demonstrates real-world behaviours—timing, one-shot initialisation, deprecation signalling—implemented as disciplined wrappers.
- Core 19 (`functools.wraps`) closes the loop with Module 3: it preserves names, docs, annotations, and the unwrapped function so that `inspect` still sees the *logical* callable, not just the outermost wrapper.

The pattern is now clear: Module 1 gave you first-class callables; Module 2 taught you how to inspect and classify them; Module 3 gave you structured views (`Signature`, provenance, frames); Module 4 uses all of that to build decorators that change *behaviour* while keeping identities and introspection surfaces honest. The capstone `@cache` decorator then acts as a didactic stress test: it is useful but intentionally non-production, forcing you to confront the semantic and concurrency pitfalls that appear the moment a decorator stops being “just logging” and starts caching or controlling side effects.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="capstone"></a>
## Capstone: @cache - Didactic Memoization from Scratch

> **Warning (didactic only, not production)**  
> The `@cache` implementation below is an educational re-implementation of `functools.lru_cache`. It is single-threaded, not safe under concurrency, and requires all arguments to be hashable in its canonical form. For production code, always prefer `functools.lru_cache` or a well-tested caching library.

### Canonical Implementation

```python
import functools
from typing import Any, Callable, Dict, Hashable, Optional

def cache(maxsize: Optional[int] = 128) -> Callable:
    """Factory: returns decorator with LRU cache of maxsize (None for unlimited; 0 disables caching)."""
    if maxsize is not None and maxsize < 0:
        raise ValueError("maxsize must be >= 0 or None")

    if maxsize == 0:
        def decorator_no_cache(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                return func(*args, **kwargs)

            def cache_clear() -> None:
                """No-op for disabled cache (maxsize=0)."""
                pass

            wrapper.cache_clear = cache_clear
            return wrapper
        return decorator_no_cache

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Key: (args, frozenset(kwargs.items())) — requires all components to be hashable.
            try:
                key: Hashable = (args, frozenset(kwargs.items()))
            except TypeError as e:
                raise TypeError(
                    "cache() only supports hashable arguments in its canonical form; "
                    "for unhashable arguments, see the 'unhashable extension' variant "
                    "later in this core."
                ) from e

            if key in wrapper._cache:
                # LRU: move to end (naive FIFO-based LRU; O(n) due to list.pop(0))
                wrapper._cache_order.remove(key)
                wrapper._cache_order.append(key)
                return wrapper._cache[key]

            # Miss: compute
            result = func(*args, **kwargs)

            # Evict oldest key if at capacity (naive FIFO-based LRU; O(n) due to list.pop(0))
            if maxsize is not None and len(wrapper._cache_order) >= maxsize:
                oldest = wrapper._cache_order.pop(0)
                del wrapper._cache[oldest]

            # Store
            wrapper._cache[key] = result
            wrapper._cache_order.append(key)
            return result

        # Cache state: instance attrs for debuggability (inspectable/clearable)
        wrapper._cache: Dict[Hashable, Any] = {}
        wrapper._cache_order: list = []  # For LRU eviction

        def cache_clear():
            """Clear cache."""
            wrapper._cache.clear()
            wrapper._cache_order.clear()

        wrapper.cache_clear = cache_clear  # Expose method
        return wrapper
    return decorator

# Usage example
@cache(maxsize=3)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(fib(10))  # 55 (caches intermediates)
print(fib(5))   # 5 (hit)
fib.cache_clear()
print(fib(3))   # 2 (recaches post-clear)
```

### Optional Extension: Unsafe Unhashable Support (Didactic Only)

```python
# Do NOT use in real code – for teaching purposes only
def _make_unhashable_key(args, kwargs):
    # Order- and repr-dependent; for small demos only.
    return f"{args!r}|{dict(kwargs)!r}"

# Inside wrapper, replace the key block with:
# try:
#     key = (args, frozenset(kwargs.items()))
# except TypeError:
#     key = _make_unhashable_key(args, kwargs)
```

### Deep Dive Explanation

`@cache` operationalises memoization: factory parameterises size (0 disables, None unlimited), decorator wraps with `@wraps` for metadata, state via instance attrs for debuggability (e.g., inspect `wrapper._cache`). Key hashes args/kwargs exactly as `functools.lru_cache` does in its canonical form. `cache_clear` exposed as method. Ties to Module 1 `__call__` (delegation), Core 16 closure (state via attrs), Core 18 logic (miss/hit). Pedagogically, trace fib: recursive calls hit cache, reducing tree. For production, replace list with OrderedDict (O(1) move_to_end) and use `functools.lru_cache`.

### Examples

LRU eviction (finite):

```python
@cache(maxsize=2)
def expensive(a, b):
    print(f"Computing {a}+{b}")
    return a + b

expensive(1, 2)  # Computing 1+2\n3
expensive(3, 4)  # Computing 3+4\n7 (cache full)
expensive(1, 2)  # 3 (hit; moves to end)
expensive(5, 6)  # Computing 5+6\n11 (evicts 3+4)
```

Unlimited cache:

```python
@cache(maxsize=None)
def unlimited_fib(n: int) -> int:
    if n < 2:
        return n
    return unlimited_fib(n-1) + unlimited_fib(n-2)

print(unlimited_fib(10))  # 55 (grows unbounded)
```

Disabled cache:

```python
@cache(maxsize=0)
def no_cache_fib(n: int) -> int:
    if n < 2:
        return n
    return no_cache_fib(n-1) + no_cache_fib(n-2)

print(no_cache_fib(5))  # 5 (no caching)
print(no_cache_fib(5))  # 5 (recomputes)
no_cache_fib.cache_clear()  # No-op
```

### Advanced Notes and Pitfalls

- Canonical version: only supports hashable arguments; this mirrors `functools.lru_cache` and avoids the semantic traps of serialising mutables into keys. From a static-typing perspective, this also keeps the callable’s apparent type simple (purely value-based caching on positional/keyword arguments); more sophisticated, typed caches belong in the later, typing-aware decorator module.
- Optional extension: serialising unhashable arguments into keys (e.g. via `str` or `pickle`) is didactic but dangerous:
  - order- and repr-dependent,
  - prone to collisions across runs or processes,
  - interacts badly with mutation after the call.
  Use only in tightly controlled demos, never in production.
- Pitfall: Thread-safety absent—concurrent access can corrupt the cache or LRU order. Production caches must protect their internal state with locks or use thread-safe primitives.
- Pitfall: O(n) remove/pop(0)—didactic; use collections.OrderedDict for O(1).
- CPython: Hash collisions rare.

### Exercise

Extend `@cache` with `typed=False` param: if True, key includes type(args)—prevents int/str mix (e.g., fib(1) != fib("1")). Test with fib(30) with/without—verify speedup.

You have completed Module 4.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="glossary"></a>
## Glossary (Module 4)

| Term                            | Definition                                                                                                                                          |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Decorator**                   | A callable that takes a function (or class) and returns a new callable with modified/augmented behavior.                                            |
| **`@decorator` syntax**         | Syntactic sugar for rebinding: `@d` above `def f` means `f = d(f)` executed at definition/import time.                                              |
| **Stacked decorators**          | Multiple `@` lines compose right-to-left: `@d3 @d2 @d1` becomes `f = d3(d2(d1(f)))`; call-time executes wrappers outer → inner.                     |
| **Decoration time**             | One-time transformation step when the function is defined (typically import time): wrappers are built and the name is rebound.                      |
| **Call time**                   | Per-invocation execution of the wrapper chain, running pre/post logic around the original function call.                                            |
| **Decoratee**                   | The original function being wrapped; captured by the wrapper (usually via closure) and invoked by delegation.                                       |
| **Wrapper function**            | The returned callable that implements the new behavior: accepts `*args, **kwargs`, runs extra logic, then delegates to the decoratee.               |
| **Nested function**             | Inner function defined inside another function; the mechanical basis of decorators because it can capture the decoratee and state.                  |
| **Closure**                     | Captured environment that lets the wrapper “remember” the decoratee and any decorator state (counters, caches, config).                             |
| **Closure state**               | Mutable state stored in a closure cell (via `nonlocal`) or on the wrapper object (attributes), used by stateful decorators.                         |
| **`nonlocal`**                  | Keyword enabling mutation of a captured outer-scope variable inside the wrapper; required for closure-held counters, flags, etc.                    |
| **Decorator factory**           | A callable that returns a decorator, used as `@factory(config)`; evaluated once at definition time, then applied to the function.                   |
| **Forwarding wrapper**          | Wrapper that accepts arbitrary arguments and forwards them unchanged to the decoratee; typically `def wrapper(*args, **kwargs)`.                    |
| **Semantic transparency**       | Property of a “thin” decorator that preserves behavior and error model aside from its declared concern (e.g., timing/logging).                      |
| **Stateful decorator**          | Decorator that changes semantics by storing state across calls (cache, once, retries, rate limits); should be treated as “small framework.”         |
| **`functools.wraps`**           | Standard wrapper helper that copies identity metadata to the wrapper and sets `__wrapped__` to the original function.                               |
| **Identity metadata**           | Function attributes needed for debuggability and tooling: `__name__`, `__qualname__`, `__doc__`, `__module__`, `__annotations__`, and `__dict__`.   |
| **`__wrapped__`**               | Attribute pointing from wrapper to decoratee; enables `inspect.unwrap` and signature recovery through wrapper chains.                               |
| **Introspection friendliness**  | Preserving names/docs/signatures so tools (`help`, Sphinx, `inspect.signature`) report the logical callable rather than `wrapper(*args, **kwargs)`. |
| **Exception transparency**      | Policy where the wrapper lets exceptions propagate unchanged unless the decorator explicitly documents altered error behavior.                      |
| **`@timer` decorator**          | Wrapper that measures duration of each call (typically with `time.perf_counter`) and reports it; should use `try/finally` to time even on errors.   |
| **`@once` decorator**           | Idempotent decorator that runs the function at most once and returns the first successful result for all later calls, ignoring later arguments.     |
| **`@deprecated` decorator**     | Wrapper that emits a warning on use (commonly `warnings.warn(..., DeprecationWarning, stacklevel=2)`) while delegating behavior unchanged.          |
| **Stacklevel**                  | Warnings parameter controlling which caller frame is reported; used to blame the user call site rather than the decorator wrapper.                  |
| **Memoization**                 | Caching function results keyed by arguments so repeated calls return cached values rather than recomputing.                                         |
| **Cache key canonicalization**  | Converting `(args, kwargs)` into a hashable key (e.g., `(args, frozenset(kwargs.items()))`), requiring hashable components.                         |
| **LRU cache discipline**        | Least-Recently-Used eviction policy: when capacity is reached, discard the entry unused for the longest time.                                       |
| **`cache_clear` hook**          | Explicit method exposed by a cache wrapper to reset internal state deterministically (important for tests and long-running processes).              |
| **Didactic cache**              | Educational cache implementation that is intentionally incomplete (e.g., single-threaded, O(n) eviction); contrasted with `functools.lru_cache`.    |
| **Concurrency caveat**          | Stateful decorators without locks can corrupt state under multi-threading/async; correctness requires explicit concurrency design.                  |
| **Decorator order sensitivity** | The order of stacked decorators changes semantics (e.g., `@once @timer` vs `@timer @once` determines whether timing runs once or always).           |

Proceed to Module 5: Decorators Level 2 – Real-World & Typing-Aware.

<span style="font-size: 1em;">[Back to top](#top)</span>
