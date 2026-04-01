# Core 8: Versioning and Migration of FuncPipe Contracts and Pipeline Graphs

**Module 10**
> **Core question:**  
> How do you version and migrate FuncPipe contracts (events, ports, configs, graphs) across bounded contexts with enforceable rules for backward/forward compatibility, enabling zero-downtime evolution and safe deprecation?

In this core, we establish rigorous, enforceable versioning for the FuncPipe RAG Builder (now at `funcpipe-rag-10`). All public contracts are versioned with explicit semantic rules. Events and graphs are immutable primitives with major-only versioning (breaking = new major). Ports follow inbound-stable (2-major deprecation) / outbound-evolvable contracts. Configs use semver. Compatibility is verified with PBT (new accepts old; old rejects new with typed error; invariants preserved after translation). Deprecation is exactly two major versions. Builds on Core 7's contexts.

**Motivation Bug:** Unversioned or poorly versioned contracts cause cascading breaks, downtime during upgrades, and "works on my machine" migrations.

**Delta from Core 7:** Contexts isolate domains; versioning makes evolution safe across time.

**Versioning & Migration Contract (Normative):**
- Events & graphs: major-only (v1, v2); primitives only; additive optional fields allowed within major (lenient readers ignore unknown + MUST emit telemetry).
- Ports: inbound stable for 2 majors (breaking requires new port + shim); outbound new versions on breaking.
- Configs: semver; defaults may change in minor (warn on old).
- Event types:
  - Closed-world channel (finite known types): new type = breaking → new major.
  - Open-world channel (consumers ignore unknown types): new type = same major.
- Compatibility mode: consumers lenient for additive changes (ignore unknown optional fields + telemetry); strict reject on breaking major.
- Deprecation: exactly two major versions supported concurrently.
- Rollout order:
  - Additive (same major): producer first (lenient consumers tolerate new fields).
  - Breaking (new major): dual-publish vN and vN+1 → consumers upgrade to read vN+1 → producer drops vN.
- Stored events/reprocessing: keep upcasters for the last two majors in a separate "archive" toolchain; old logs require explicit migration or archive runner.
- Enforcement: PBT compatibility suite + runtime version guards + mypy.

**Audience:** Architects/engineers managing evolving FP systems.

**Outcome:**
1. Version all contracts with explicit rules.
2. Write semantic compatibility PBT.
3. Migrate with deprecation windows + dual-publish.
4. Version graphs as immutable specs.

---
## 1. Laws & Invariants
| Law                        | Description                                                                                  | Enforcement                          |
|----------------------------|------------------------------------------------------------------------------------------------|--------------------------------------|
| **Event/Graph Versioning** | Major-only; breaking change = new major; additive optional = same major (lenient ignore + telemetry). | Naming + PBT                         |
| **Port Stability**         | Inbound ports stable for 2 majors; outbound new versions on breaking.                        | Mypy + PBT                           |
| **Backward Compatibility** | New version accepts old inputs/events; translates + preserves invariants.                    | PBT suite                            |
| **Forward Compatibility**  | Old version rejects unknown major with typed error; ignores unknown optional fields + telemetry. | PBT suite + runtime guards           |
| **Deprecation Window**     | Exactly two major versions supported concurrently.                                            | Runtime + CI                         |
| **Graph Immutability**     | Graphs are immutable, major-versioned specs; changes create new major.                       | Serialization + canonical hash checks|

These are enforceable engineering constraints.

---
## 2. Decision Table
### Events & Graphs (major-only)
| Change Type                | Same Major | New Major | Notes                                |
|----------------------------|------------|-----------|--------------------------------------|
| Additive optional field    | Yes        | No        | Lenient readers ignore + telemetry   |
| New event type (closed-world) | No      | Yes       | Breaking → new major                 |
| New event type (open-world) | Yes       | No        | Consumers ignore unknown types       |
| Field rename/remove        | No         | Yes       | New major + migration ACL            |
| Semantics change           | No         | Yes       | New major                            |

### Ports & Configs (semver)
| Change Type                | Minor | Major | Notes                                |
|----------------------------|-------|-------|--------------------------------------|
| Additive optional field    | Yes   | No    | Lenient readers ignore               |
| Config default change      | Yes   | No    | Warn on old                          |
| Field rename/remove        | No    | Yes   | Major + shim                         |
| Semantics change           | No    | Yes   | Major                                |

**Major for breaking; minor for additive.**

---
## 3. Public API (Versioning Blueprint)
```text
contracts/
  events/
    clean_doc_produced/
      v1.py          # CleanDocProducedV1
      v2.py          # CleanDocProducedV2 (breaking)
      current.py     # alias to latest
  ports/
    inbound_raw_source/
      v1.py
      v2.py          # breaking inbound change
      current.py
  graphs/
    rag/
      v1.json        # canonical JSON
      v2.json
      current.json
```

Runtime version guards in ACL/ports.

---
## 4. Reference Implementations
### 4.1 Versioned Event (Major-Only)
```python
# contracts/events/clean_doc_produced/v1.py
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class CleanDocProducedV1:
    version: Literal["1"] = "1"
    doc_id: str
    abstract: str
    produced_at_ms: int

# contracts/events/clean_doc_produced/v2.py
@dataclass(frozen=True)
class CleanDocProducedV2:
    version: Literal["2"] = "2"
    doc_id: str
    text: str  # renamed from abstract
    produced_at_ms: int
```

### 4.2 Compatibility ACL (Lenient + Strict + Telemetry)
```python
# contexts/chunking/acl.py
import logging
from typing import TypedDict

from pydantic import BaseModel, ValidationError

from contracts.events.clean_doc_produced.v1 import CleanDocProducedV1
from contracts.events.clean_doc_produced.v2 import CleanDocProducedV2
from .types import ChunkingIngressV1, ChunkingTranslationError
from funcpipe.core import Result, Ok, Err

logger = logging.getLogger(__name__)

class _V1Model(BaseModel):
    version: Literal["1"]
    doc_id: str
    abstract: str
    produced_at_ms: int
    model_config = {"extra": "allow"}

class _V2Model(BaseModel):
    version: Literal["2"]
    doc_id: str
    text: str
    produced_at_ms: int
    model_config = {"extra": "allow"}

def from_clean_doc_produced(raw: dict) -> Result[ChunkingIngressV1, ChunkingTranslationError]:
    version = raw.get("version", "1")
    try:
        if version == "1":
            parsed = _V1Model(**raw)
            if parsed.model_extra:
                logger.warning("Ignored unknown fields in CleanDocProduced v1: %s", parsed.model_extra.keys())
            return Ok(ChunkingIngressV1(
                doc_id=parsed.doc_id,
                text=parsed.abstract,
                metadata={"cleaned_at_ms": parsed.produced_at_ms},
            ))
        if version == "2":
            parsed = _V2Model(**raw)
            if parsed.model_extra:
                logger.warning("Ignored unknown fields in CleanDocProduced v2: %s", parsed.model_extra.keys())
            return Ok(ChunkingIngressV1(
                doc_id=parsed.doc_id,
                text=parsed.text,
                metadata={"cleaned_at_ms": parsed.produced_at_ms},
            ))
    except ValidationError as exc:
        return Err(ChunkingTranslationError("validation_error", str(exc)))
    return Err(ChunkingTranslationError("unsupported_version", f"v{version}"))
```

### 4.3 Old Version Rejection (Strict Reader)
```python
# old_contexts/chunking/v1/acl.py
from pydantic import BaseModel, ValidationError

class _OldV1Model(BaseModel):
    version: Literal["1"]
    doc_id: str
    abstract: str
    produced_at_ms: int
    model_config = {"extra": "forbid"}

def from_clean_doc_produced(raw: dict) -> Result[...]:
    if raw.get("version", "1") != "1":
        return Err(ChunkingTranslationError("unsupported_version", "this version only accepts v1"))
    try:
        _OldV1Model(**raw)
    except ValidationError as exc:
        return Err(ChunkingTranslationError("validation_error", str(exc)))
    # ...
```

### 4.4 Port Evolution Rules
- Inbound: stable for 2 majors (breaking requires new port + shim adapter).
- Outbound: new versions on breaking; old deprecated over 2 majors.

### 4.5 Pipeline Graph Versioning (Major-Only, Canonical JSON)
```python
# graphs/rag_v1.json (canonical, sorted keys)
{
  "version": "1",
  "contexts": {
    "cleaning": "v1",
    "chunking": "v2"
  },
  "policy": {
    "batch_size": 128,
    "ordering": "stable"
  }
}
```

Loader with validation + canonical hash:

```python
import json
import hashlib
from pydantic import BaseModel, ValidationError

class RagGraphV1(BaseModel):
    version: Literal["1"]
    contexts: dict[str, str]
    policy: dict

def load_pipeline_graph(path: str) -> tuple[RagGraphV1, str]:
    with open(path) as f:
        raw = f.read()
    canon = json.dumps(json.loads(raw), sort_keys=True, separators=(",", ":"))
    graph_hash = hashlib.sha256(canon.encode()).hexdigest()
    data = json.loads(canon)
    try:
        graph = RagGraphV1(**data)
    except ValidationError as exc:
        raise ValueError(f"Invalid graph {path}: {exc}")
    return graph, graph_hash
```

### 4.6 Event Evolution Rules
- Additive optional fields → same major.
- Breaking rename/remove/semantics → new major.
- New event type:
  - Closed-world channel → new major.
  - Open-world channel → same major.
- Converters live in downstream ACL.
- Compatibility PBT verifies new accepts old + old rejects new with explicit error.

### 4.7 Orchestration Shell with Platform Policy
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
            translated = from_clean_doc_produced(event.to_dict())
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
Versioned contracts + compatibility checks + dual-publish for breaking majors enable zero-downtime upgrades.

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
translated = from_clean_doc_produced(event.to_dict())
if translated.is_ok():
    await chunking.ingest(translated.ok())
```

**Next: core 9. Governance – Ownership, Change Control, and “Unsafe” Extensions of FuncPipe**
