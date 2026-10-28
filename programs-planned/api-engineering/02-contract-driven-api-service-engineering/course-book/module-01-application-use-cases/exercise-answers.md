# Reference Answers — Module 01: Application Use Cases and Boundaries

Read after attempting all twelve Application Use Cases and Boundaries exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Explain why the OpenAPI contract is an input to this course rather than an output.

Course 1 already established and verified the public promise. This course tests whether an implementation can fulfil it durably. Editing the contract to make an implementation easier would erase the very constraint being studied.

## 2. Draw the ownership path for `createProject`. Where may HTTP status `201` be selected?

The route knows the operation and serializes the use-case result as `201`; the use case decides that creation succeeded and returns the created project plus location identity. SQL code must not select HTTP status.

## 3. What is the difference between a Pydantic/TypeBox model and an application command?

The former validates a transport representation and may include aliases or framework metadata. The command expresses application intent after authentication and parsing. Keeping them separate prevents transport evolution from becoming business coupling.

## 4. When is a port justified?

When the application requires a capability with a meaningful behavioral contract—such as atomic conditional update, durable job claim, or artifact publication—and a concrete technology should remain replaceable or independently testable.

## 5. Why pass the principal explicitly after middleware already authenticated it?

Explicit data makes authorization visible in signatures, direct tests, and repository predicates. Ambient context can leak across concurrency and hides which operations actually depend on identity.

## 6. Classify `clock`, `identifier source`, `repository`, and `JSON encoder` as likely ports or utilities.

Clock, identifier source, and repository are collaborators because their behavior affects observable state and tests. A canonical JSON encoder may remain a pure utility unless the application truly needs multiple strategies.

## 7. What does the composition root own during shutdown?

It owns resources it constructed: server lifecycle, pools, transports, and worker controls. Application use cases should not close shared resources or register process signals themselves.

## 8. Why is one universal CRUD repository weaker than use-case-oriented methods?

CRUD does not express ownership, preconditions, atomicity, pagination order, or transaction coupling. A method such as `update_project_if_version` states a guarantee that generic `save` cannot.

## 9. Give a stable application error for a concealed foreign resource.

A not-found condition can intentionally represent both absence and foreign ownership. The transport maps it to the documented 404 problem without revealing existence.

## 10. How can two language tracks be equivalent without identical folders?

Equivalence is defined at the frozen contract and shared scenarios. Python and TypeScript may use idiomatic module boundaries as long as operation ownership, guarantees, and wire behavior match.

## 11. Trace operation-to-use-case mapping in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/service.py` and `capstone/tracks/typescript-fastify/src/service.ts`. The required invariant is that route adapters translate HTTP input into application commands; use cases own decisions.

## 12. Compare operation-to-use-case mapping across Python and TypeScript

Both tracks must preserve this invariant: route adapters translate HTTP input into application commands; use cases own decisions. The intentional difference is that Python uses explicit service methods and protocols; TypeScript uses structural interfaces and async methods.
