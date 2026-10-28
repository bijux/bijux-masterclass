# Checkpoint — Module 02: HTTP Edge and Canonicalization

## Required result

FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.

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

## Defend the design

1. Answer the central question: **Which bytes and proxy assertions does the application actually trust before framework parsing begins?**
2. Demonstrate this capstone result: FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: critical singleton headers, trusted proxy assertions, media type, body size, and strict JSON are decided before model construction.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—FastAPI and Fastify reject ambiguous edge input consistently before application models are constructed.—all focused checks pass, the **HTTP Edge and Canonicalization** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
