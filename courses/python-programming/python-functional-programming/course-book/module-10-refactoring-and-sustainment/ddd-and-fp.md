# Core 7: Domain-Driven Design Meets FP – Aligning Bounded Contexts with Pipelines

**Module 10**
> **Core question:**  
> How do you structure large functional systems as independently evolvable bounded contexts with pure cores, explicit ports/events, verifiable isolation, and clear boundary contracts while preserving composability and law-based reasoning?

In this core, we restructure the FuncPipe RAG Builder (now at `funcpipe-rag-10`) as a set of bounded contexts. Each context is a self-contained functional domain owning:
- its ubiquitous language (local types, errors, combinators),
- pure core (invariants + pipelines),
- explicit ports (inbound/outbound protocols),
- versioned immutable domain events (built from primitives only),
- anti-corruption layers (pure translators with minimal compatibility policy).

Contexts evolve independently. Orchestration is thin wiring governed by explicit platform-level policies (ordering, delivery, retries). Isolation is enforced statically (layered import-linter) and verified at runtime.

**Motivation Bug:** Monolithic pipelines create hidden coupling: a change in cleaning breaks indexing; scaling embedding requires redeploying everything; ownership is ambiguous.

**Delta from Core 6:** Advanced patterns improve single-context pipelines; DDD+FP enables safe multi-context systems with independent evolution.

**DDD+FP Contract (Normative):**
- Each context owns its types, errors, invariants.
- Core imports only stdlib + shared FP primitives (funcpipe.core, funcpipe.result, funcpipe.eq, funcpipe.combinators) + own context.
- ACL imports upstream events + own context.
- Communication via versioned immutable events (primitives only; no upstream types).
  Event schema discipline: field names/semantics owned by producer context; downstream treats unknown fields as error (strict) or drops (lenient) – policy declared per consumer ACL.
- Anti-corruption layers are pure translators with minimal compatibility policy (e.g., version gating).
- Orchestration owns workflow and delivery guarantees (ordering, retries, dedup) as platform/system context policy – not domain invariants.
- Isolation enforced via layered import-linter contracts (CI) + runtime smoke test.

**Audience:** Architects/engineers building large, long-lived FP systems.

**Outcome:**
1. Split system into bounded contexts with local types/events.
2. Enforce isolation with layered import-linter + runtime check.
3. Version events (primitives only) + write compatibility PBT.
4. Orchestrate with explicit platform policies.

---
## 1. Laws & Invariants
| Law                        | Description                                                                                  | Enforcement                          |
|----------------------------|------------------------------------------------------------------------------------------------|--------------------------------------|
| **Context Isolation**      | Core: stdlib + shared FP + own context only.<br>ACL: upstream events + own context only.<br>Adapters: infra + own context. | Layered import-linter + runtime smoke |
| **Local Ubiquitous Language** | Domain concepts (types, errors, combinators) defined exactly once per context.              | Ownership matrix + linter            |
| **Invariant Ownership**    | Each domain invariant belongs to exactly one context.                                         | PBT per context                      |
| **Event Immutability**     | Domain events are frozen dataclasses built from primitives; versioned (v1, v2).              | frozen=True + mypy + PBT             |
| **ACL Minimal Policy**     | ACLs are pure translators with minimal compatibility policy only (e.g., version gating).     | Reviews + PBT                        |
| **Backward Compatibility** | New context versions accept old events; old versions reject unknown fields with typed error. | Two-way PBT compatibility suite      |

These are enforceable engineering constraints.

---
## 2. Decision Table
| Signal                             | Single Context | Multiple Contexts          | Recommended                  |
|------------------------------------|----------------|----------------------------|------------------------------|
| Distinct terminology/invariants    | No             | Yes                        | Multiple                     |
| Divergent change cadence           | No             | Yes                        | Multiple                     |
| Different scaling / tech needs     | No             | Yes                        | Multiple                     |
| Different failure semantics        | No             | Yes                        | Multiple                     |
| Shared evolution pace              | Yes            | Risky                      | Single                       |

**Split when any signal is "Yes".**

---
## 3. Public API (Context Blueprint)
```text
contexts/
  cleaning/
    __init__.py      # re-exports core + ports + events only
    types.py         # RawDoc, CleanDoc, CleaningError
    core.py          # pure functions + pipelines
    ports.py         # InboundRawSource, OutboundCleanSink
    events.py        # CleanDocProducedV1(frozen=True, primitives only)
    acl.py           # translate_from_upstream(event) -> Result[ChunkingIngressV1, ChunkingTranslationError]
    config.py        # CleaningConfig
```

Adapters are internal; consumers import only core/ports/events.

---
## 4. Reference Implementations
### 4.1 Context-Local Types & Errors
```python
# contexts/cleaning/types.py
from dataclasses import dataclass

@dataclass(frozen=True)
class CleaningError:
    code: str
    message: str

@dataclass(frozen=True)
class RawDoc:
    doc_id: str
    title: str
    abstract: str
    categories: str  # space/comma-separated

@dataclass(frozen=True)
class CleanDoc:
    doc_id: str
    title: str
    abstract: str
    categories: str
```

### 4.2 Pure Core with Local Invariants
```python
# contexts/cleaning/core.py
import re
from .types import RawDoc, CleanDoc, CleaningError
from .config import CleaningConfig
from funcpipe.core import Result, Ok, Err

def _has_allowed_category(categories: str, prefixes: tuple[str, ...]) -> bool:
    """Precondition: categories is space/comma-separated list of tags.
    Invariant: at least one tag has an allowed prefix."""
    cats = re.split(r"[,\s]+", categories.strip())
    return any(any(cat.startswith(p) for p in prefixes) for cat in cats)

def clean_doc(raw: RawDoc, cfg: CleaningConfig) -> Result[CleanDoc, CleaningError]:
    if len(raw.abstract) < cfg.min_abstract_length:
        return Err(CleaningError("too_short", f"abstract < {cfg.min_abstract_length} chars"))
    if not _has_allowed_category(raw.categories, cfg.allowed_prefixes):
        return Err(CleaningError("irrelevant_category", f"no prefix in {cfg.allowed_prefixes}"))
    cleaned_abstract = raw.abstract.lower().strip()
    return Ok(CleanDoc(
        doc_id=raw.doc_id,
        title=raw.title.strip(),
        abstract=cleaned_abstract,
        categories=raw.categories,
    ))
```

### 4.3 Versioned Domain Event (Primitives Only)
```python
# contexts/cleaning/events.py
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class CleanDocProducedV1:
    version: Literal["1"] = "1"
    doc_id: str
    title: str
    abstract: str
    categories: str
    produced_at_ms: int
```

### 4.4 Anti-Corruption Layer (Pure Translator with Minimal Compatibility Policy)
```python
# contexts/chunking/acl.py
from contexts.cleaning.events import CleanDocProducedV1
from .types import ChunkingIngressV1, ChunkingTranslationError
from funcpipe.core import Result, Ok, Err

def from_clean_doc_produced(event: CleanDocProducedV1) -> Result[ChunkingIngressV1, ChunkingTranslationError]:
    if event.version != "1":
        return Err(ChunkingTranslationError("unsupported_version", f"v{event.version}"))
    return Ok(ChunkingIngressV1(
        doc_id=event.doc_id,
        text=event.abstract,
        metadata={"title": event.title, "categories": event.categories, "cleaned_at_ms": event.produced_at_ms},
    ))
```

### 4.5 Ports Example
```python
# contexts/cleaning/ports.py
from typing import Protocol, AsyncIterator
from funcpipe.core import Result
from .types import RawDoc, CleanDoc, CleaningError

class InboundRawSource(Protocol):
    async def raw_docs(self) -> AsyncIterator[Result[RawDoc, CleaningError]]: ...

class OutboundCleanSink(Protocol):
    async def store(self, docs: AsyncIterator[Result[CleanDoc, CleaningError]]) -> None: ...
```

### 4.6 Layered Import-Linter Contracts (Runnable INI)
```ini
[importlinter]
root_package = contexts

[importlinter:contract:core_isolation]
name = Core isolation
type = forbidden
source_modules = contexts.*.core
forbidden_modules = contexts.*
ignore_imports =
    contexts.*.core -> contexts.*.types
    contexts.*.core -> contexts.*.config
    contexts.*.core -> funcpipe.*

[importlinter:contract:acl_upstream_events]
name = ACL upstream events only
type = forbidden
source_modules = contexts.*.acl
forbidden_modules = contexts.*
ignore_imports =
    contexts.chunking.acl -> contexts.cleaning.events
    contexts.embedding.acl -> contexts.chunking.events
    # etc.
```

### 4.7 Runtime Isolation Smoke Test
```python
# ci/test_runtime_isolation.py
import importlib
import pytest

@pytest.mark.parametrize("context", ["cleaning", "chunking", "embedding", "indexing"])
def test_context_core_imports_clean(context):
    core = importlib.import_module(f"contexts.{context}.core")
    assert core.__name__.endswith(".core")
```

### 4.8 Event Evolution Rules
- Additive optional fields → minor version.
- Breaking rename/remove → major version.
- Converters live in downstream ACL.
- Compatibility PBT verifies new accepts old + old rejects new with explicit error.

### 4.9 Orchestration Shell with Platform Policy
```python
# shell.py
import logging
from contexts.cleaning import CleaningContext
from contexts.chunking.acl import from_clean_doc_produced
from contexts.chunking import ChunkingContext

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class OrchestrationPolicy:
    batch_size: int = 128
    ordering: Literal["stable", "unordered"] = "stable"
    delivery: Literal["at-least-once", "at-most-once"] = "at-least-once"
    dedup_key: Callable[[CleanDocProducedV1], Hashable] | None = lambda e: e.doc_id
    retry_policy: RetryPolicy = field(default_factory=lambda: RetryPolicy(max_attempts=3))

async def rag_orchestration(cfg: GlobalConfig, policy: OrchestrationPolicy):
    cleaning = CleaningContext(cfg.cleaning)
    chunking = ChunkingContext(cfg.chunking)

    seen = set() if policy.delivery == "at-most-once" else None

    async for raw_batch in batch_source(cfg.source_path, policy.batch_size):
        clean_events = await cleaning.process_batch(raw_batch)
        for event in clean_events:
            key = policy.dedup_key(event) if policy.dedup_key else None
            if seen is not None and key in seen:
                continue
            translated = from_clean_doc_produced(event)
            if translated.is_err():
                logger.warning("ACL failure: %s", translated.err())
                continue
            ingest = lambda: chunking.ingest(translated.ok())
            result = await policy.retry_policy.run(ingest)
            if result.is_ok() and seen is not None and key is not None:
                seen.add(key)  # ack-based dedup
```

---
## 5. Property-Based Proofs
Per-context PBT as before + compatibility suite + runtime isolation.

---
## 6. Runtime Preservation Guarantee
Contexts independently deployable/testable/scalable; versioned events enable rolling upgrades; platform policies control cross-context behaviour.

---
## 7. Anti-Patterns & Immediate Fixes
| Anti-Pattern               | Symptom                          | Fix                                      |
|----------------------------|----------------------------------|------------------------------------------|
| Shared domain types        | Evolution deadlock               | Local types + primitive events           |
| Direct cross-context calls | Hidden coupling                  | Ports/events only                        |
| Policy in shell            | Domain logic in orchestration    | Explicit platform policy objects         |
| Unversioned events         | Breaking changes without notice  | Versioned primitive events + compatibility PBT |

---
## 8. Pre-Core Quiz
1. Context owns…? → **Types, errors, invariants, language**  
2. Cross-context…? → **Versioned primitive events + ACL**  
3. Isolation enforced by…? → **Layered import-linter + runtime smoke**  
4. Orchestration is…? → **Thin wiring + platform policy**  
5. Benefit…? → **Independent evolution + clear ownership**

## 9. Post-Core Exercise
1. List bounded contexts in your system.  
2. Extract one to local types + primitive events + ACL.  
3. Add layered import-linter rules + runtime isolation test.  
4. Write two-way compatibility PBT.

**Pipeline Usage (Idiomatic)**
```python
# Inside cleaning
cleaned = clean_doc(raw, cfg)

# Cross-context (orchestration)
translated = from_clean_doc_produced(event)
if translated.is_ok():
    await chunking.ingest(translated.ok())
```

**Next: core 8. Versioning and Migration of FuncPipe Contracts and Pipeline Graphs**
