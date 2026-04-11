# Runtime Power Ladder

Use this page when a metaprogramming design feels impressive but the review question is
really about blast radius, timing, and ownership.

The ladder is not a prestige scale. It is a way to compare how far each mechanism reaches
into runtime behavior and how much review evidence it should owe in return.

## The ladder

From lower power to higher power:

1. explicit code and ordinary objects
2. wrappers and decorators
3. descriptors and attribute-level control
4. metaclasses and class-creation hooks
5. import hooks, AST transforms, and dynamic execution with global consequences

Moving upward is not automatically wrong. It means the approval bar gets higher because
the mechanism becomes harder to observe, harder to reverse, or harder to scope tightly.

## What each rung is for

### 1. Explicit code and ordinary objects

Use this when a function, method, class, or helper can own the behavior directly.

Why it is the default:

- the timing is visible
- the owner is explicit
- tests and debugging usually stay straightforward

### 2. Wrappers and decorators

Use this when call-time policy belongs around a callable and can stay transparent.

Typical honest cases:

- thin logging
- light validation
- explicit registration

Review pressure:

- preserve metadata
- preserve tracebacks
- measure hot-path overhead when relevant

### 3. Descriptors and attribute-level control

Use this when one attribute access path is the right owner for validation, coercion, or
storage rules.

Typical honest cases:

- field-level validation
- attribute-backed caching
- reusable per-field contracts

Review pressure:

- keep source of truth explicit
- keep per-instance behavior inspectable
- avoid turning one field abstraction into a hidden framework

### 4. Metaclasses and class-creation hooks

Use this only when the behavior truly belongs before the class exists as a finished object.

Typical honest cases:

- declaration-time namespace control
- hierarchy-wide registration at class definition time
- class-shape enforcement that lower-power tools cannot own

Review pressure:

- keep import-time effects visible
- keep registration deterministic and resettable
- justify why a decorator or helper is insufficient

### 5. Import hooks, AST transforms, and dynamic execution

Use this only for tooling-grade problems or tightly bounded trusted-runtime cases.

Typical honest cases:

- instrumentation
- coverage and tracing
- controlled code generation for trusted inputs

Review pressure:

- name the process-wide blast radius
- provide cleanup and disable paths
- stop security claims at real trust and isolation boundaries

## The approval question

For any rung above the first, ask:

> What does this mechanism own that the rung below it cannot own honestly enough?

If the answer is vague, ornamental, or mostly about elegance, stay lower.

## Keep, change, reject examples

- Keep a descriptor when one field contract is the real owner.
- Change a wrapper that hides traceback or signature information.
- Reject a metaclass when a decorator can register classes explicitly enough.
- Reject import-hook discovery when explicit imports or entry points keep the runtime more visible.

## Related reference pages

- [Review Checklist](review-checklist.md)
- [Boundary Review Prompts](boundary-review-prompts.md)
- [Topic Boundaries](topic-boundaries.md)
- [Module Dependency Map](module-dependency-map.md)
