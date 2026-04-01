# In-Process Event Dispatch: Tiny Observer and Event Bus

## Purpose

Dispatch domain events **synchronously in-process** to handlers, without frameworks.

You will build a tiny event bus suitable for a Python service and learn the correctness constraints (ordering, error handling, reentrancy).

## 1. The Minimal Event Bus Contract

An event bus does two things:
- accept an event,
- call registered handlers for that event type.

In-process dispatch is usually synchronous:
- publish returns only after handlers ran.

This is simple and easy to test, but you must decide what happens when a handler fails.

## 2. A Tiny, Testable Implementation

```python
from collections import defaultdict
from typing import Callable, Type, Any

Handler = Callable[[Any], None]

class EventBus:
    def __init__(self):
        self._handlers: dict[Type[Any], list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: Type[Any], handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: Any) -> None:
        for handler in list(self._handlers[type(event)]):
            handler(event)
```

Teaching note: this is intentionally small. The goal is clarity, not feature count.

## 3. Error Handling Policy (You Must Choose One)

Common policies:

1. **Fail-fast**: first handler error aborts publish.
   - good for correctness if handlers are critical.
2. **Best-effort**: run all handlers, collect errors.
   - good for side-effects like logging/metrics.

Write the policy down and test it. “Undefined policy” becomes production chaos.

## 4. Ordering and Reentrancy

- Handler ordering should be deterministic (insertion order) for testability.
- Reentrancy: a handler may publish more events.
  - This can be fine, but it can also create deep call stacks and cycles.

Rule: keep handlers small and avoid publishing the same event type recursively unless you can prove termination.

## 5. Event Bus is Infrastructure

The bus is not “domain logic”. Keep it in infrastructure or application, and keep handlers as adapters around domain operations.

Domain emits events; application wires handlers; infrastructure executes them.

## Practical Guidelines

- Keep the event bus minimal and testable.
- Choose and document an error handling policy for handler failures.
- Make handler ordering deterministic for reproducible tests.
- Avoid complex reentrant event graphs; keep handlers small and focused.

## Exercises for Mastery

1. Extend the event bus to support multiple event types and write tests for handler ordering.
2. Implement best-effort error collection and write a test showing both handlers run even if one fails.
3. Create a handler that updates a projection when `RuleActivated` is published.
