# ADR 0002 — Extract Notification Delivery first

**Decision:** move webhook subscriptions and delivery attempts into an event-fed Notification Service.

**Reason:** delivery is asynchronous, independently retryable, independently retained, and does not belong on run-completion critical paths.

**Rollback:** stop the consumer, replay from the last committed event position, and restore the legacy dispatcher during the bounded coexistence window.
