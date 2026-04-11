# Effect Capabilities and Static Checking


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Effect Boundaries Resource Safety"]
  page["Effect Capabilities and Static Checking"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Read the first diagram as a placement map: this page is one concept inside its parent module, not a detached essay, and the capstone is the pressure test for whether the idea holds. Read the second diagram as the working rhythm for the page: name the problem, study the example, identify the boundary, then carry one review question forward.

**Module 07 – Main Track Core**

> **Main track**: Cores 1, 3–10 (Ports & Adapters + Capability Protocols → Production).  
> This is a **required** core. Every production FuncPipe system uses mypy-checked capability protocols.

## Progression Note
Module 7 takes the lawful containers and pipelines from Module 6 and puts all effects behind explicit boundaries.

| Module | Focus                                   | Key Outcomes                                                                 |
|--------|-----------------------------------------|-------------------------------------------------------------------------------|
| 6      | Monadic Flows as Composable Pipelines   | Lawful `and_then`, Reader/State/Writer patterns, error-typed flows          |
| 7      | Effect Boundaries & Resource Safety     | Ports & adapters, capability protocols, resource-safe IO, idempotency       |
| 8      | Async / Concurrent Pipelines            | Backpressure, timeouts, resumability, fairness (built on 6–7)               |

**Core question**  
How do you use `typing.Protocol` and `mypy --strict` to define and **statically enforce** effect capabilities, ensuring cores only access declared methods and enabling truly modular FP designs?

**What you now have after M07C01–M07C05 + this core**
- Pure domain core  
- Zero direct I/O in domain code  
- All I/O behind swappable ports  
- Effectful operations described as pure data (`IOPlan`)  
- Typed capability protocols for every common effect  
- Reliable resource cleanup  
- Pure, composable logging via Writer  
- **Statically verified capability isolation** – with `mypy --strict`, explicit types (no `Any`), and CI import rules, core code cannot reach beyond its declared capabilities

**What the rest of Module 7 adds**
- Idempotent effect design  
- Transaction/session patterns  
- Incremental migration playbook  
- Production story: CI, golden tests, shadow traffic

You are now five steps away from a complete production-grade functional architecture.

## 1. Laws & Invariants (machine-checked where possible)

| Law / Invariant            | Description                                                                                  | Enforcement          |
|----------------------------|----------------------------------------------------------------------------------------------|----------------------|
| Capability Minimalism      | Each protocol contains **only** the methods required by its capability. No extras.          | Code review          |
| Capability Isolation       | Core code types its dependencies as protocols; mypy prevents calling undeclared methods. Import layering (no infra imports in domain) enforced by CI. | mypy --strict + CI   |
| Compliance                 | Concrete adapters satisfy all protocol members; extra methods are invisible through protocol types. | mypy --strict        |
| Substitutability           | We sample substitutability with Hypothesis: different implementations of the same protocol yield identical core behavior on the same logical inputs. | Hypothesis (adapter equivalence) |
| No Any Escape              | Public capability signatures contain no `Any`; all types are explicit.                      | mypy --strict        |

These laws turn capability injection from a runtime pattern into a **type-checked + property-tested + review-enforced discipline**.

## What mypy Enforces, and What It Does Not

It often helps to separate two different guardrails:

- `mypy --strict` enforces protocol usage, explicit types, and undeclared-method errors
- CI or review rules enforce architectural layering, such as “domain modules do not import infra adapters”

That split is important. Static typing protects capability *shape*. Layering checks
protect dependency *direction*. Module 07 needs both.

## 2. Decision Table – When to Use Which Protocol Pattern?

| Scenario                           | Runtime Check Needed? | Composition Needed? | Recommended Pattern                  |
|------------------------------------|-----------------------|---------------------|--------------------------------------|
| Pure static duck typing            | No                    | No                  | Plain `Protocol`                     |
| Multiple capabilities              | No                    | Yes                 | Multiple inheritance                 |
| Dynamic checking (rare)            | Yes                   | No                  | `@runtime_checkable Protocol`        |
| Generic capabilities               | No                    | Yes                 | `class Cache(Protocol): ...` with `Option[T]` where needed |

**Rule**: Prefer static-only protocols. Use `@runtime_checkable` only when you truly need `isinstance(x, Protocol)` (almost never in production).

## 3. Public API – Composed Capability Protocols (`capstone/src/funcpipe_rag/domain/capabilities.py`)

```python
# capstone/src/funcpipe_rag/domain/capabilities.py – mypy --strict clean
from __future__ import annotations
from datetime import datetime
from collections.abc import Iterator
from typing import Protocol

from funcpipe_rag.core.rag_types import Chunk, RawDoc
from funcpipe_rag.domain.logging import LogEntry
from funcpipe_rag.result.types import ErrInfo, Option, Result

__all__ = [
    "StorageRead",
    "StorageWrite",
    "Storage",           # composed read + write
    "Clock",
    "Logger",
    "Cache",
]

class StorageRead(Protocol):
    def read_docs(self, path: str) -> Iterator[Result[RawDoc, ErrInfo]]: ...

class StorageWrite(Protocol):
    def write_chunks(self, path: str, chunks: Iterator[Chunk]) -> Result[None, ErrInfo]: ...

class Storage(StorageRead, StorageWrite, Protocol):
    """Composed capability: full read/write access."""

class Clock(Protocol):
    def now(self) -> datetime: ...

class Logger(Protocol):
    def log(self, entry: LogEntry) -> None: ...

class Cache(Protocol):
    def get(self, key: str) -> Result[Option[Chunk], ErrInfo]: ...
    def set(self, key: str, chunk: Chunk) -> Result[None, ErrInfo]: ...
```

Zero concrete code. Zero imports from infra. These are pure, composable capability interfaces.

**Note**: Full shell bundles (e.g. `RagCapabilities`) are defined in shell code, not domain – cores must depend on minimal protocols only.

## 4. Reference Implementations – Real & Mock Adapters

### 4.1 Concrete Adapter Implementing Multiple Capabilities (structural, no inheritance from Protocol)

```python
# Illustrative example (not a repo file): one adapter implementing multiple capabilities structurally.
class FullAdapter: ...
```

### 4.2 mypy + CI Catching Violations (Negative Example)

```python
# Illustrative anti-pattern (not a repo file): infra import in domain code.
from funcpipe_rag.infra.adapters.file_storage import FileStorage  # ← illegal import (layering rule)

def bad_core(adapter: StorageRead):
    adapter.some_private_method()        # ← mypy error: "StorageRead" has no attribute "some_private_method"
    _ = FileStorage()                    # ← mypy allows it, but layering forbids it
```

**Explanation**: mypy enforces protocol method usage. Import layering (no infra in
domain) is enforced separately in CI or review rules. Treat them as cooperating checks,
not as one tool doing everything.

### 4.3 Core Using Only Declared Capabilities

```python
# Illustrative example (not a repo file): core depends only on declared capabilities.
def rag_core_needing_read_and_clock(
    storage: StorageRead,
    clock: Clock,
) -> Writer[Iterator[Chunk], Logs]:
    start = clock.now()
    docs = storage.read_docs("in.csv")
    # ... pure processing
    return trace_stage(f"processed in {clock.now() - start}")
```

### 4.4 Shell Injecting Full Capabilities

```python
# shell/prod.py
cap = FullAdapter()  # implements Storage + Clock + Logger structurally
result = rag_shell(cap).run(env)
```

## 5. Property-Based Proofs (selected)

```python
@given(docs=doc_list_strategy())
def test_capability_substitutability(docs):
    class MockRead(StorageRead):
        def read_docs(self, path: str) -> Iterator[Result[RawDoc, ErrInfo]]:
            yield from (Ok(d) for d in docs)

    class RealRead(StorageRead):
        # alternate implementation using a different internal iteration style
        def read_docs(self, path: str) -> Iterator[Result[RawDoc, ErrInfo]]:
            for d in tuple(docs):
                yield Ok(d)

    # Core uses only StorageRead capability
    mock_res = list(rag_core_needing_read_only(MockRead()))
    real_res = list(rag_core_needing_read_only(RealRead()))
    assert mock_res == real_res
```

We sample substitutability with Hypothesis for critical capabilities.

## 6. Big-O & Allocation Guarantees

| Operation         | Time | Call-stack | Heap | Allocation |
|-------------------|------|------------|------|------------|
| Protocol dispatch | O(1) | O(1)       | O(1) | O(1)       |

Protocols introduce no additional runtime overhead beyond normal method dispatch (they are erased at runtime).

## 7. Anti-Patterns & Immediate Fixes

| Anti-Pattern              | Symptom                              | Fix                                      |
|---------------------------|--------------------------------------|------------------------------------------|
| Concrete adapter in core  | Import from infra → coupling         | Depend only on protocol                  |
| God capability            | One protocol with 40 methods         | One capability → one protocol            |
| Any in signatures         | Type escape hatch                    | Explicit domain types only               |
| Nominal inheritance only  | Inflexible mocking                   | Structural subtyping via Protocol        |

## 8. Pre-Core Quiz

1. Capability protocols are…? → **Statically checked minimal interfaces**  
2. Core depends on…? → **Only the protocol, never the concrete adapter**  
3. mypy --strict catches…? → **Undeclared method access**  
4. Import layering enforced by…? → **CI rules (e.g. import-linter)**  
5. Real power comes from…? → **Static verification of capability boundaries**

## 9. Post-Core Exercise

1. Define a `MetricsProtocol` and compose it into a shell-only `RagCapabilities`.  
2. Write a core function that accidentally uses a concrete adapter method → show mypy error.  
3. Add a property test proving two different implementations of the same protocol yield identical results.  
4. Create a `Reader[RagCapabilities, ...]` pipeline and run it with both mock and real capabilities.

**Continue with:** [Composing Effects](../module-07-effect-boundaries-resource-safety/composing-effects.md)

You now have **statically verified capability isolation** – with `mypy --strict`, explicit types (no `Any`), and CI import rules, core code cannot reach beyond its declared capabilities. Combined with ports, `IOPlan`, resource safety, and pure logging, your architecture is effectively bulletproof. The remaining cores are specialisations and production patterns.
