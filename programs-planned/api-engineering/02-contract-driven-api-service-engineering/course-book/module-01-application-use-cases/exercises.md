# Exercises — Module 01: Application Use Cases and Boundaries

## 1. Explain why the OpenAPI contract is an input to this course rather than an output.

## 2. Draw the ownership path for `createProject`. Where may HTTP status `201` be selected?

## 3. What is the difference between a Pydantic/TypeBox model and an application command?

## 4. When is a port justified?

## 5. Why pass the principal explicitly after middleware already authenticated it?

## 6. Classify `clock`, `identifier source`, `repository`, and `JSON encoder` as likely ports or utilities.

## 7. What does the composition root own during shutdown?

## 8. Why is one universal CRUD repository weaker than use-case-oriented methods?

## 9. Give a stable application error for a concealed foreign resource.

## 10. How can two language tracks be equivalent without identical folders?

## 11. Trace operation-to-use-case mapping in the primary implementation

Read `capstone/tracks/python-fastapi/src/analysis_service/service.py` or `capstone/tracks/typescript-fastify/src/service.ts` in your primary track. Trace one accepted input and one rejected or failed input from the public/application boundary to the authoritative result. Name the focused regression that would fail if the central guard were removed.

## 12. Compare operation-to-use-case mapping across Python and TypeScript

Compare `capstone/tracks/python-fastapi/src/analysis_service/service.py` with `capstone/tracks/typescript-fastify/src/service.ts`. Identify the shared invariant, one deliberate language or library difference, and one source-shape difference that must not become a parity requirement.

## Submission format

Submit Module 01 decisions with one counterexample and one decisive oracle each. Cite complete source paths for implementation answers and retain the module-specific defect evidence.
