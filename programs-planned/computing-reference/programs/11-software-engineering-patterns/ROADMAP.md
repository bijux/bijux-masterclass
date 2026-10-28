# 11. Software Engineering: Patterns

**Program code:** `SEPAT`

**Purpose:** Build a rigorous vocabulary for recurring software design problems, the forces that shape them, and the consequences of applying or misapplying established patterns.

**Level-II professional outcome:** Ready to recognize, select, adapt, combine, and critique design, integration, concurrency, data, and distributed-system patterns without pattern-driven overengineering.

**Prerequisites:** OOP foundations; software design fundamentals; experience maintaining a nontrivial codebase.

**Primary ownership:** pattern form and forces; object design patterns; enterprise application patterns; integration and messaging patterns; concurrency patterns; distributed resilience patterns; data-access patterns; anti-patterns; pattern languages; pattern selection.

**Explicit exclusions:** domain discovery and modeling (Program 09); system-wide architecture design (Program 12); protocol algorithms (Program 27); platform product design (Program 29).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Pattern Thinking and Pattern Languages

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Recurring Problems, Context, Forces, and Consequences** | `001-recurring-problems-context-forces-and-consequences.md` |
| 002 | **Pattern Versus Idiom, Principle, Recipe, and Framework** | `002-pattern-versus-idiom-principle-recipe-and-framework.md` |
| 003 | **Reading and Writing a Pattern Form** | `003-reading-and-writing-a-pattern-form.md` |
| 004 | **Pattern Intent and Applicability** | `004-pattern-intent-and-applicability.md` |
| 005 | **Trade-Offs and Negative Consequences** | `005-trade-offs-and-negative-consequences.md` |
| 006 | **Pattern Composition** | `006-pattern-composition.md` |
| 007 | **Pattern Sequences and Pattern Languages** | `007-pattern-sequences-and-pattern-languages.md` |
| 008 | **Refactoring Toward and Away from Patterns** | `008-refactoring-toward-and-away-from-patterns.md` |
| 009 | **Pattern Hype and Cargo-Cult Design** | `009-pattern-hype-and-cargo-cult-design.md` |
| 010 | **Selecting a Pattern from Forces Rather Than Names** | `010-selecting-a-pattern-from-forces-rather-than-names.md` |

### Block 02 — Creational Patterns

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Simple Factory and Creation Functions** | `011-simple-factory-and-creation-functions.md` |
| 012 | **Factory Method** | `012-factory-method.md` |
| 013 | **Abstract Factory** | `013-abstract-factory.md` |
| 014 | **Builder** | `014-builder.md` |
| 015 | **Prototype** | `015-prototype.md` |
| 016 | **Singleton and Its Hidden Global State** | `016-singleton-and-its-hidden-global-state.md` |
| 017 | **Object Pool** | `017-object-pool.md` |
| 018 | **Dependency Injection as a Creation Pattern** | `018-dependency-injection-as-a-creation-pattern.md` |
| 019 | **Lazy Initialization** | `019-lazy-initialization.md` |
| 020 | **Comparing Creational Patterns Under Change** | `020-comparing-creational-patterns-under-change.md` |

### Block 03 — Structural Patterns

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Adapter** | `021-adapter.md` |
| 022 | **Bridge** | `022-bridge.md` |
| 023 | **Composite** | `023-composite.md` |
| 024 | **Decorator** | `024-decorator.md` |
| 025 | **Facade** | `025-facade.md` |
| 026 | **Flyweight** | `026-flyweight.md` |
| 027 | **Proxy** | `027-proxy.md` |
| 028 | **Module and Package Facades** | `028-module-and-package-facades.md` |
| 029 | **Ports and Adapters as a Structural Pattern** | `029-ports-and-adapters-as-a-structural-pattern.md` |
| 030 | **Combining Structural Patterns Without Indirection Explosion** | `030-combining-structural-patterns-without-indirection-explosion.md` |

### Block 04 — Behavioral Patterns I

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Chain of Responsibility** | `031-chain-of-responsibility.md` |
| 032 | **Command** | `032-command.md` |
| 033 | **Interpreter as an Object Pattern** | `033-interpreter-as-an-object-pattern.md` |
| 034 | **Iterator** | `034-iterator.md` |
| 035 | **Mediator** | `035-mediator.md` |
| 036 | **Memento** | `036-memento.md` |
| 037 | **Observer** | `037-observer.md` |
| 038 | **State** | `038-state.md` |
| 039 | **Strategy** | `039-strategy.md` |
| 040 | **Template Method** | `040-template-method.md` |

### Block 05 — Behavioral Patterns II and Object Collaboration

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Visitor** | `041-visitor.md` |
| 042 | **Null Object** | `042-null-object.md` |
| 043 | **Specification** | `043-specification.md` |
| 044 | **Method Object** | `044-method-object.md` |
| 045 | **Role Object** | `045-role-object.md` |
| 046 | **Double Dispatch** | `046-double-dispatch.md` |
| 047 | **Event Listener and Callback** | `047-event-listener-and-callback.md` |
| 048 | **Policy Object** | `048-policy-object.md` |
| 049 | **Object Mother and Test Data Builder** | `049-object-mother-and-test-data-builder.md` |
| 050 | **Diagnosing Behavioral Pattern Misuse** | `050-diagnosing-behavioral-pattern-misuse.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Enterprise Application Patterns

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Transaction Script** | `051-transaction-script.md` |
| 052 | **Domain Model** | `052-domain-model.md` |
| 053 | **Table Module** | `053-table-module.md` |
| 054 | **Service Layer** | `054-service-layer.md` |
| 055 | **Unit of Work** | `055-unit-of-work.md` |
| 056 | **Identity Map** | `056-identity-map.md` |
| 057 | **Data Mapper** | `057-data-mapper.md` |
| 058 | **Active Record** | `058-active-record.md` |
| 059 | **Lazy Load** | `059-lazy-load.md` |
| 060 | **Choosing an Enterprise Domain and Persistence Pattern** | `060-choosing-an-enterprise-domain-and-persistence-pattern.md` |

### Block 07 — Messaging and Integration Patterns

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Message Channel** | `061-message-channel.md` |
| 062 | **Message Router** | `062-message-router.md` |
| 063 | **Message Translator** | `063-message-translator.md` |
| 064 | **Canonical Data Model** | `064-canonical-data-model.md` |
| 065 | **Content-Based Router** | `065-content-based-router.md` |
| 066 | **Publish-Subscribe Channel** | `066-publish-subscribe-channel.md` |
| 067 | **Competing Consumers** | `067-competing-consumers.md` |
| 068 | **Claim Check** | `068-claim-check.md` |
| 069 | **Dead-Letter Channel** | `069-dead-letter-channel.md` |
| 070 | **Designing an Integration Flow from Message Semantics** | `070-designing-an-integration-flow-from-message-semantics.md` |

### Block 08 — Concurrency and Reactive Patterns

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Reactor** | `071-reactor.md` |
| 072 | **Proactor** | `072-proactor.md` |
| 073 | **Half-Sync/Half-Async** | `073-half-sync-half-async.md` |
| 074 | **Leader-Followers** | `074-leader-followers.md` |
| 075 | **Thread Pool** | `075-thread-pool.md` |
| 076 | **Active Object** | `076-active-object.md` |
| 077 | **Monitor Object** | `077-monitor-object.md` |
| 078 | **Future and Promise** | `078-future-and-promise.md` |
| 079 | **Producer-Consumer with Bounded Buffers** | `079-producer-consumer-with-bounded-buffers.md` |
| 080 | **Selecting a Concurrency Pattern from Blocking and Ownership Constraints** | `080-selecting-a-concurrency-pattern-from-blocking-and-ownership-constraints.md` |

### Block 09 — Distributed and Resilience Patterns

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Retry with Bounded Backoff** | `081-retry-with-bounded-backoff.md` |
| 082 | **Timeout and Deadline** | `082-timeout-and-deadline.md` |
| 083 | **Circuit Breaker** | `083-circuit-breaker.md` |
| 084 | **Bulkhead** | `084-bulkhead.md` |
| 085 | **Rate Limiter** | `085-rate-limiter.md` |
| 086 | **Load-Shedding Pattern** | `086-load-shedding-pattern.md` |
| 087 | **Saga** | `087-saga.md` |
| 088 | **Transactional Outbox** | `088-transactional-outbox.md` |
| 089 | **Idempotent Consumer** | `089-idempotent-consumer.md` |
| 090 | **Combining Resilience Patterns Without Failure Amplification** | `090-combining-resilience-patterns-without-failure-amplification.md` |

### Block 10 — Data, Evolution, and Pattern Judgment

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Repository** | `091-repository.md` |
| 092 | **Data Transfer Object** | `092-data-transfer-object.md` |
| 093 | **Change Data Capture Pattern** | `093-change-data-capture-pattern.md` |
| 094 | **Event Sourcing** | `094-event-sourcing.md` |
| 095 | **Command Query Responsibility Segregation** | `095-command-query-responsibility-segregation.md` |
| 096 | **Materialized View** | `096-materialized-view.md` |
| 097 | **Strangler Fig** | `097-strangler-fig.md` |
| 098 | **Branch by Abstraction Pattern** | `098-branch-by-abstraction-pattern.md` |
| 099 | **Recognizing Golden Hammer, Big Ball of Mud, and Distributed Monolith** | `099-recognizing-golden-hammer-big-ball-of-mud-and-distributed-monolith.md` |
| 100 | **Conducting a Pattern Review from Context, Forces, and Evidence** | `100-conducting-a-pattern-review-from-context-forces-and-evidence.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
