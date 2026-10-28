# Program Glossary

**Acknowledgement** — a consumer-group decision that one delivery attempt has been handled according to policy; it is not proof that every downstream consequence succeeded.

**Admission control** — a bounded decision about whether work may enter a constrained resource or queue.

**Analysis Runs API** — the public synchronous HTTP interface of the Analysis Runs Platform.

**Analysis Events API** — the public asynchronous interface introduced in Course 6.

**Authoritative state** — durable state owned by the component responsible for a fact or decision.

**Backpressure** — propagation of downstream capacity limits so upstream work does not grow without bound.

**Canonicalization** — converting a value into one unambiguous representation for identity, comparison, or signing.

**Capstone** — the continuing Analysis Runs Platform used to make the curriculum executable.

**Compatibility** — whether existing request writers, response readers, consumers, and deployed versions can continue to behave correctly after a change.

**Contract** — the externally visible messages, semantics, errors, security decisions, compatibility commitments, and workflows on which another party may rely.

**Correlation ID** — an identifier grouping a broader journey; it is not automatically an event ID, causation ID, trace ID, or partition key.

**Course policy** — a deliberate invariant stricter or more specific than a normative standard, adopted so the capstone remains interoperable and mechanically reviewable.

**Critical journey** — a user or system outcome whose success population, failure modes, and service objective are explicitly defined.

**Dead letter** — a delivery placed under explicit custody after normal retry policy cannot produce an acceptable effect.

**Dependency-light proof** — evidence that runs without optional live infrastructure; it must not be presented as live-dependency evidence.

**Durable oracle** — a database, storage, or other authoritative fact that establishes whether a committed outcome occurred.

**Effect version** — identity used to distinguish a consumer’s versioned business effect from a delivery attempt or source event.

**Evidence class** — the declared strength and environment of a proof: deterministic, local-process, live-dependency, representative, or operated.

**Handoff** — immutable, sanitized artifacts from one course that define the next course’s starting boundary.

**Idempotency** — a guarantee that repeated requests or deliveries with the same identity do not create unintended additional logical effects.

**Integration event** — a stable, owned fact published for independently evolving consumers; not a serialized private aggregate or imperative command.

**Invariant** — a condition that must remain true across legal state changes and failure paths.

**Lease** — time-bounded ownership of work that allows recovery after a worker disappears.

**Open workload** — demand scheduled independently of response completion; useful for exposing queue growth under overload.

**Profile** — versioned cross-artifact engineering policy, such as Security, Reliability, Performance, or Event Profile 1.0.

**Public API version** — the semantic interface version consumers depend on, independent of specification, service-release, or migration versions.

**Replay** — controlled reprocessing of retained events or evidence, usually scoped, dry-run capable, and separated from external side effects.

**Residual risk** — a named risk that remains after controls and proofs, with assumptions and ownership made explicit.

**Service release** — one deployable implementation version; it may change without changing the public API.

**SLI** — a precisely defined measurement of a service outcome population.

**SLO** — a versioned objective over an SLI, including window, target, exclusions, and ownership.

**Source of truth** — the boundary authorized to declare a fact; projections and telemetry may observe it but do not compete with it.

**Transactional outbox** — publication intent committed in the same transaction as the authoritative state change, then delivered asynchronously.

**Trace link** — a relationship used when asynchronous work does not have valid synchronous parent-child timing.

**Workload identity** — a canonical fingerprint of demand model, operation mix, payload/data distribution, duration, and other semantic benchmark inputs.
