# Core 9: Governance – Ownership, Change Control, and “Unsafe” Extensions of FuncPipe

**Module 10**
> **Core question:**  
> How do you govern a mature FuncPipe system with clear ownership, controlled change processes, and principled allowances for “unsafe” extensions while protecting purity, laws, and evolvability?

In this core, we establish enforceable governance for the FuncPipe RAG Builder (now at `funcpipe-rag-10`). Governance defines ownership per bounded context, change control workflows (reviews, approvals, deprecation enforcement), and a formal “unsafe extension” policy: isolated deviations from observable purity (globals, IO, nondeterminism, shared mutable state). Local mutation is allowed as implementation detail. This prevents purity drift while allowing pragmatic wins. Builds on Core 8's versioning.

**Motivation Bug:** Without governance, FP systems regress: new contributors add globals, “just this once” mutations leak, ownership is ambiguous, breaking changes slip through.

**Delta from Core 8:** Versioning enables safe evolution; governance enforces discipline and allows controlled exceptions.

**Governance Contract (Normative):**
- Ownership: each bounded context has one primary owning team (documented in OWNERS); secondary teams optional but required for cross-cutting changes (shared FP primitives, public contracts, multiple contexts). Tie-breaker: platform team has final say.
- Change control: PRs touching a context require primary owner approval; breaking changes or unsafe-semantic changes require RFC + 2-major deprecation.
- Unsafe extensions: two categories:
  - unsafe-implementation: semantics unchanged, drop-in replacement for pure impl (must prove equivalence PBT).
  - unsafe-semantic: semantics changed (e.g., global cache, nondeterminism); requires RFC + new major version of affected contract(s) + new graph major.
- Unsafe code lives only in `contexts/*/unsafe/` or adapters; injected as strategy from orchestration (core never imports unsafe).
- Enforcement: CODEOWNERS (primary required), pre-commit hooks, PBT for unsafe facades, static scanners (forbidden-imports for random/time/IO libs in core; custom AST for globals/shared state in core).
- Deprecation: exactly two major versions (aligned with Core 8).

**Audience:** Tech leads/architects maintaining large FP codebases.

**Outcome:**
1. Assign primary owners per context.
2. Define change control + RFC process.
3. Allow unsafe extensions with explicit category + equivalence/new-law PBT.
4. Automate enforcement.

---
## 1. Laws & Invariants
| Law                        | Description                                                                                  | Enforcement                          |
|----------------------------|------------------------------------------------------------------------------------------------|--------------------------------------|
| **Ownership**              | Primary owner required; approves merges. Secondary required for cross-cutting (tie-breaker: platform). | CODEOWNERS + PR rules                |
| **Change Control**         | Breaking or unsafe-semantic changes require RFC + 2-major deprecation.                        | PR template + CI gate                |
| **Unsafe Isolation**       | Unsafe code only in `contexts/*/unsafe/` or adapters; injected as strategy (core never imports unsafe). | import-linter + reviews              |
| **Facade Purity**          | Public API of unsafe-implementation wrappers has no observable impurity.                     | PBT + runtime checks                 |
| **Equivalence Mandate**    | unsafe-implementation ships with pure reference + PBT proving equivalence.                   | Required in PR (no RFC)              |
| **Semantic Shift Mandate** | unsafe-semantic changes create new major version of affected contract(s) + new graph major.  | Required in RFC                      |

These are enforceable engineering constraints.

---
## 2. Decision Table
| Change Type                     | Primary Owner Approval | RFC Required | Deprecation Window | Recommended                  |
|---------------------------------|------------------------|--------------|--------------------|------------------------------|
| Additive (same major)           | Yes                    | No           | N/A                | Minor bump                   |
| Breaking (new major)            | Yes                    | Yes          | 2 majors           | Major bump + RFC             |
| unsafe-implementation           | Yes                    | No           | N/A                | Equivalence PBT              |
| unsafe-semantic                 | Yes                    | Yes          | 2 majors           | New major + RFC              |
| Config default change           | Yes                    | No           | Warn 1 minor       | Minor + warning              |

**Require primary owner sign-off; RFC for breaking/unsafe-semantic.**

---
## 3. Public API (Governance Blueprint)
```text
contexts/
  cleaning/
    OWNERS         # primary: @cleaning-squad
                    # secondary: @platform-fp (for shared primitives)
    core.py
    unsafe/        # only here or adapters
    ...
OWNERS (root)      # platform team for shared FP primitives
RFC_TEMPLATE.md    # required for breaking/unsafe-semantic changes
```

---
## 4. Reference Implementations
### 4.1 Ownership (CODEOWNERS)
```ini
# .github/CODEOWNERS
contexts/cleaning/* @cleaning-squad @platform-fp
contexts/chunking/* @chunking-squad
funcpipe/core/* @platform-fp
```

### 4.2 Change Control (PR Template)
```markdown
# PR Template
- Primary context owner: @...
- Type: [additive | breaking | unsafe-implementation | unsafe-semantic]
- If breaking/unsafe-semantic: RFC link
- Deprecation plan (if applicable):
```

### 4.3 Unsafe Extension Policy (Strategy Injection)
```python
# contexts/chunking/types.py
from typing import Protocol, Sequence, TypeVar, Hashable

T = TypeVar("T", bound=Hashable)

class DedupStrategy(Protocol[T]):
    def __call__(self, items: Sequence[T]) -> list[T]: ...

# Pure default
def pure_dedup(items: Sequence[T]) -> list[T]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# contexts/chunking/core.py – pure facade
from .types import DedupStrategy

def chunk_pipeline(docs: Sequence[CleanDoc], dedup: DedupStrategy[Chunk] = pure_dedup) -> list[Chunk]:
    chunks = []
    for doc in docs:
        chunks.extend(chunk_doc(doc))
    return dedup(chunks)

# contexts/chunking/unsafe/dedup.py – unsafe-implementation (semantics unchanged)
def fast_scoped_dedup(items: Sequence[T]) -> list[T]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# contexts/chunking/unsafe/global_dedup.py – unsafe-semantic (global once-ever dedup)
_GLOBAL_CACHE: set[T] = set()

def fast_global_dedup(items: Sequence[T]) -> list[T]:
    result: list[T] = []
    for item in items:
        if item not in _GLOBAL_CACHE:
            _GLOBAL_CACHE.add(item)
            result.append(item)
    return result

# orchestration chooses strategy
policy = OrchestrationPolicy(use_fast_global_dedup=True)
dedup = fast_global_dedup if policy.use_fast_global_dedup else pure_dedup
chunks = chunk_pipeline(docs, dedup)
```

### 4.4 Deprecation Enforcement
Aligned with Core 8 (2 majors).

### RAG Integration
Assign owners; unsafe strategies injected by orchestration; enforce via CODEOWNERS + PR template.

---
## 5. Property-Based Proofs
Mandatory equivalence PBT for unsafe-implementation; new-law PBT for unsafe-semantic.

```python
@given(items=st.lists(st.integers(), max_size=1000))
def test_fast_scoped_equiv(items):
    pure = pure_dedup(items)
    fast = fast_scoped_dedup(items)
    assert pure == fast
    orig = list(items)
    fast_scoped_dedup(items)
    assert items == orig  # input unchanged

@given(stream1=st.lists(st.integers(), max_size=1000), stream2=st.lists(st.integers(), max_size=1000))
def test_global_dedup_law(stream1, stream2):
    # Law: global once-ever dedup across calls
    _GLOBAL_CACHE.clear()
    a = fast_global_dedup(stream1)
    b = fast_global_dedup(stream2)
    assert set(a + b) == set(stream1) | set(stream2)
```

---
## 6. Runtime Preservation Guarantee
Ownership + change control prevent drift; unsafe extensions injected + equivalence-tested (or new-law tested).

---
## 7. Anti-Patterns & Immediate Fixes
| Anti-Pattern               | Symptom                          | Fix                                      |
|----------------------------|----------------------------------|------------------------------------------|
| Orphaned context           | Stale code                       | Primary owner required                   |
| Silent breaking change     | Production outages               | RFC + 2-major deprecation                |
| Purity drift               | Hidden mutation                  | Strategy injection + pure facade         |
| God reviewer               | Bottlenecks                      | Per-context primary owners               |

---
## 8. Pre-Core Quiz
1. Ownership…? → **Primary + optional secondary**  
2. Breaking/unsafe-semantic…? → **RFC + 2-major**  
3. Unsafe…? → **Strategy injection + pure facade + equiv/new-law PBT**  
4. Deprecation…? → **2 majors**  
5. Benefit…? → **Controlled evolution without drift**

## 9. Post-Core Exercise
1. Add OWNERS with primary/secondary to your contexts.  
2. Write RFC template.  
3. Implement one unsafe strategy + facade + equiv/new-law PBT.  
4. Add CODEOWNERS enforcement.

**Pipeline Usage (Idiomatic)**
```python
# Orchestration chooses strategy
dedup = fast_global_dedup if policy.use_fast_global_dedup else pure_dedup
chunks = chunk_pipeline(docs, dedup)
```

**Next: core 10. Teaching, Onboarding, and Designing the Bridge from FuncPipe to ParaPipe**