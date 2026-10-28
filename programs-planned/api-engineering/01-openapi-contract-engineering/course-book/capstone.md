# Capstone — OpenAPI Contract Engineering

## One continuing platform

The capstone is the Analysis Runs Platform. Principals create projects, register datasets, submit analysis runs, observe progress, retrieve verified artifacts, and receive or consume completion facts. Course 1 does not replace the platform; it adds the responsibility **specify the promise**.

## Starting state

Basic programming ability and no assumed OpenAPI experience.

## Course increments

| Module | Platform increment |
|---:|---|
| 1 | Establish health and project operations as raw messages, OpenAPI operations, and equivalent provider behavior. |
| 2 | Complete project and dataset messages, including pagination inputs, creation responses, and problem representations. |
| 3 | Define precise project, dataset, run, artifact, and problem schemas with a shared valid/invalid fixture corpus. |
| 4 | Split the contract into owned documents, resolve every reference offline, and produce deterministic bundles. |
| 5 | Add the analysis-run workflow, idempotency key, status resource, ETags, cancellation, and Problem Details. |
| 6 | Map every operation to both providers and compare generated observations with the canonical contract. |
| 7 | Build the consumer and contract-test ladder against the mock and both real providers. |
| 8 | Describe API-key and OAuth-style schemes, scopes, anonymous overrides, and documented security failures. |
| 9 | Create compatible and rejected release candidates, compatibility gates, and public/partner audience views. |
| 10 | Publish the OpenAPI 3.2 frontier, streaming and webhook contracts, links, and an Arazzo workflow. |


## Language tracks

Both Python/FastAPI and TypeScript/Fastify are used symmetrically to prove that the contract is language-neutral.

Shared fixtures, vectors, operation maps, releases, and black-box scenarios define parity. Identical class names or directory shape do not.

## Capstone reading order

1. read the module chapter and identify the owning mechanism;
2. inspect the narrow source path named by the chapter;
3. inspect the corresponding test or vector;
4. run the focused proof;
5. perform the lab modification in a working branch;
6. return to the chapter and explain how the implementation realizes the model.

## Handoff discipline

The predecessor material is read-only evidence. The current course may add a compatible public interface, migration, or profile only when its release rules permit it. It must not rewrite earlier history to simplify the present implementation.

**Outgoing handoff:** A frozen API 1.1 contract, operation ledger, schema fixtures, security decisions, workflows, and provider-neutral behavioral scenarios.

## Final capstone question

Can you trace one accepted case and one rejected, failed, overloaded, or duplicated case from the public boundary to the authoritative outcome, then name the proof and limitation at every layer this course owns?
