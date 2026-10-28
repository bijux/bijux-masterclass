# Checkpoint — Module 02: HTTP Edge and Canonicalization

## Required result

Establish host, forwarding, media-type, strict-JSON, body-size, and canonicalization rules before model validation.

## Demonstrate

- Define direct-client and trusted-proxy behavior.
- Reject ambiguous singleton headers and duplicate JSON members.
- Normalize only after preserving raw evidence.
- Enforce content type and body limits before model validation.
- Separate browser CORS policy from API authentication.

## Commands

```bash
make module-proof MODULE=02 TRACK=python
make module-proof MODULE=02 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **HTTP Edge and Canonicalization** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **HTTP Edge and Canonicalization**
- focused result for: Define direct-client and trusted-proxy behavior.
- public, durable, security, or operational observation showing: FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **raw HTTP edge evaluation**
- a limitation statement naming every live dependency required to support the strongest **HTTP Edge and Canonicalization** claim but not exercised

## Defend the design

1. Answer the central question: **Which bytes and proxy assertions does the application actually trust before framework parsing begins?**
2. Demonstrate this capstone result: FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.
3. Show the **HTTP Edge and Canonicalization** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: critical singleton headers, trusted proxy assertions, media type, body size, and strict JSON are decided before model construction.
5. State which environment-backed **HTTP Edge and Canonicalization** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.—all focused checks pass, the **HTTP Edge and Canonicalization** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
