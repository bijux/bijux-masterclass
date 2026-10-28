# Standards Map

## Stable and frontier profiles

The program distinguishes a broadly executable baseline from standards-frontier material when tool support differs. The release currently uses:

- OpenAPI 3.1.2 as the executable HTTP-description baseline and OpenAPI 3.2.0 as the frontier;
- JSON Schema 2020-12 semantics for modern schema reasoning;
- AsyncAPI 3.1.0 for asynchronous API descriptions;
- a CloudEvents 1.0-compatible event-envelope profile;
- proto3 as the executable Protobuf baseline and Edition 2024 as the frontier;
- GraphQL September 2025;
- W3C Trace Context Recommendation semantics;
- OWASP ASVS 5.0.0 as a security-verification reference;
- CycloneDX 1.7 and SLSA 1.2 vocabularies in Course 10.

## Normative text, recommendation, and course policy

Every chapter should label important rules as one of:

1. **Normative specification requirement** — required by a cited standard.
2. **Interoperability recommendation** — one legal choice that reduces ambiguity.
3. **Course policy** — a deliberately stricter invariant chosen for the capstone.
4. **Tool behavior** — observed behavior of a pinned implementation.
5. **Architecture decision** — a local ownership or release choice.

This prevents local preferences from being misrepresented as universal rules.

## Living standards

When a standard advances, update the version ledger, examples, compatibility assumptions, and proof expectations together. Do not silently change one document and leave checked fixtures on another version.
