# Worked Answers — Module 01: Application Use Cases and Boundaries

Use these solutions to audit your reasoning for **Application Use Cases and Boundaries**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Explain why the OpenAPI contract is an input to this course rather than an output.

Course 1 already established and verified the public promise. This course tests whether an implementation can fulfil it durably. Editing the contract to make an implementation easier would erase the very constraint being studied.

The chapter’s decisive distinction is this: The bundled OpenAPI description, operation ledger, behavioral scenarios, security matrix, and generated clients form the predecessor handoff. They are not suggestions. During Modules 1–9 the service must conform to those bytes; internal difficulty is solved internally. This constraint separates implementation engineering from redesign.

## 2. Draw the ownership path for `createProject`. Where may HTTP status `201` be selected?

The route knows the operation and serializes the use-case result as `201`; the use case decides that creation succeeded and returns the created project plus location identity. SQL code must not select HTTP status.

In the cumulative capstone, the rule becomes concrete: Parse and authenticate the request, translate it into a command, call one application use case, and serialize the documented result. It may know HTTP; it must not own domain transitions or SQL.

## 3. What is the difference between a Pydantic/TypeBox model and an application command?

The former validates a transport representation and may include aliases or framework metadata. The command expresses application intent after authentication and parsing. Keeping them separate prevents transport evolution from becoming business coupling.

A useful way to reason about the boundary is: Pydantic or TypeBox models describe accepted transport values. They should be converted into commands before application work. Likewise, database rows and filesystem metadata are not response models. Translation keeps framework defaults, SQL column names, and storage details from becoming accidental API commitments.

## 4. When is a port justified?

When the application requires a capability with a meaningful behavioral contract—such as atomic conditional update, durable job claim, or artifact publication—and a concrete technology should remain replaceable or independently testable.

The implementation consequence is: A port exists when the application needs a capability whose implementation may vary and whose behavior can be specified. ProjectRepository and ArtifactStore are meaningful; a one-method wrapper around json.dumps is usually not. Ports express required guarantees, not generic CRUD.

## 5. Why pass the principal explicitly after middleware already authenticated it?

Explicit data makes authorization visible in signatures, direct tests, and repository predicates. Ambient context can leak across concurrency and hides which operations actually depend on identity.

The important nuance is: Authentication occurs at the transport edge, but the resulting principal is an explicit input to every protected use case. Ownership is therefore not ambient global state. Later authorization-aware SQL can bind the principal directly into predicates.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 6. Classify `clock`, `identifier source`, `repository`, and `JSON encoder` as likely ports or utilities.

Clock, identifier source, and repository are collaborators because their behavior affects observable state and tests. A canonical JSON encoder may remain a pure utility unless the application truly needs multiple strategies.

Under concurrency or failure, the distinction becomes: Concrete dependencies are assembled once at process startup: settings, connection pool, repository, artifact store, clock, identifier source, outbound transport, and service. Business modules should not read environment variables or instantiate pools. This makes lifecycle and replacement visible.

## 7. What does the composition root own during shutdown?

It owns resources it constructed: server lifecycle, pools, transports, and worker controls. Application use cases should not close shared resources or register process signals themselves.

The design remains honest only if: For Application Use Cases and Boundaries , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 8. Why is one universal CRUD repository weaker than use-case-oriented methods?

CRUD does not express ownership, preconditions, atomicity, pagination order, or transaction coupling. A method such as `update_project_if_version` states a guarantee that generic `save` cannot.

The consumer-facing consequence is: The excerpt for Application Use Cases and Boundaries isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

## 9. Give a stable application error for a concealed foreign resource.

A not-found condition can intentionally represent both absence and foreign ownership. The transport maps it to the documented 404 problem without revealing existence.

The operational consequence is: The application reports stable conditions such as not found, forbidden, precondition required, precondition failed, conflict, and invalid state. It does not raise FastAPI exceptions or Fastify reply objects. The transport maps these conditions to the predecessor Problem Details contract.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 10. How can two language tracks be equivalent without identical folders?

Equivalence is defined at the frozen contract and shared scenarios. Python and TypeScript may use idiomatic module boundaries as long as operation ownership, guarantees, and wire behavior match.

The strongest engineering interpretation is: The Application Use Cases and Boundaries increment must preserve the frozen API and every earlier durability invariant while delivering this result: Create transport, application, and adapter boundaries for the fixed operation ledger The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 11. Trace operation-to-use-case mapping in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/service.py` and `capstone/tracks/typescript-fastify/src/service.ts`. The required invariant is that route adapters translate HTTP input into application commands; use cases own decisions.

The defect-oriented view is: Claim Required evidence ---: --- --- 1 predecessor manifest verifies byte-for-byte Write the narrow command and machine-readable oracle. 2 operation map has exactly one owner per language Write the narrow command and machine-readable oracle. 3 use-case tests run without HTTP Write the narrow command and machine-readable oracle. 4 route handlers contain no domain transition table Write the narrow command and machine-readable oracle.

## 12. Compare operation-to-use-case mapping across Python and TypeScript

Both tracks must preserve this invariant: route adapters translate HTTP input into application commands; use cases own decisions. The intentional difference is that Python uses explicit service methods and protocols; TypeScript uses structural interfaces and async methods.

Across the Python and TypeScript tracks, the invariant is: The Application Use Cases and Boundaries increment must preserve the frozen API and every earlier durability invariant while delivering this result: Create transport, application, and adapter boundaries for the fixed operation ledger The comparison track must expose the same public outcomes even when internal libraries and control flow differ.
