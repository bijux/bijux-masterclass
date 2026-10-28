# Architecture

## Boundary map

```text
                         canonical OpenAPI 3.1.2 source
                                      |
                  +-------------------+-------------------+
                  |                   |                   |
             deterministic       derived views       Arazzo workflow
                bundle           via Overlay          and links
                  |                   |                   |
        +---------+---------+         |          consumer outcome
        |                   |         |
 Python FastAPI       TypeScript Fastify             generated SDKs
 Pydantic models      TypeBox schemas                + handwritten clients
        |                   |                              |
        +---------+---------+------------------------------+
                  |
        provider-neutral behavior suite
                  |
     lint / mock / generated tests / compatibility / proof report
```

The contract is a peer artifact, not output owned by either framework. Provider-generated descriptions are compared with it to expose defaults, omitted responses, framework validation shapes, and serialization drift.

## Internal design

Both providers contain the same conceptual layers:

1. **transport and operation registration** maps methods and paths to handlers;
2. **contract models** validate requests and constrain serialized responses;
3. **authentication** resolves deterministic credentials and checks scopes;
4. **store** owns state transitions, object visibility, idempotency records, and artifact creation;
5. **problem translation** emits one public error vocabulary.

The in-memory store is deliberate. A database would add transaction and persistence concerns without improving the OpenAPI lessons. The store still uses locks or single-process ownership so idempotency and state changes have precise semantics.

## Source layout

The OpenAPI root contains stable metadata and references. Path Items live under `spec/paths/`; component categories are separated under `spec/components/`. The bundler resolves external references according to the referencing document's location and writes deterministic YAML plus a SHA-256 digest.

A split is accepted only when it improves ownership or reuse. One-field fragments and anonymous chains are rejected as reference theater.

## Trust boundaries

- Incoming credentials are untrusted until mapped to a principal.
- Scope possession does not imply object ownership.
- Callback and webhook destinations are untrusted network coordinates and are constrained to a training host.
- Response models are allowlists; internal fields cannot leak merely because a store object contains them.
- Examples are test data, not decorative prose.
- Tool output is evidence only when its command, version, input, and result are recorded.
