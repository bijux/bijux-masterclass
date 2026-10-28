# Glossary — API Security Engineering

Use this glossary alongside `program-book/glossary.md`. Program terms keep one meaning across all six courses; the entries below add course-specific distinctions.

Terms are defined as used in this program. When an Internet or OpenAPI specification gives a narrower normative meaning, the chapter and standards page name it.

## Threat

A plausible actor, capability, action, and consequence that can violate a security property.

## Asset

Data, capability, identity, availability, or evidence that the system must protect.

## Trust boundary

A point where the system begins relying on an assertion made under a different authority, not necessarily a network hop.

## Abuse case

A concrete adversarial scenario stating attacker capability, action, prohibited outcome, and evidence.

## Security invariant

A property that must hold for every relevant execution, such as tenant isolation.

## Residual risk

Accepted or unresolved exposure remaining after controls, with assumptions and ownership stated explicitly.

## Resource server

The API that accepts and validates access tokens to protect resources; it is not the authorization server.

## JWT profile

The configured set of accepted algorithms, keys, types, issuers, audiences, times, and required claims.

## JWKS

A JSON Web Key Set published by a trusted issuer and used under a configured key-selection policy.

## Audience

The resource server or service for which a token is intended.

## Revocation

A decision to reject a still-unexpired credential or key.

## Principal

The authenticated caller identity and validated attributes used by policy.

## Authorization policy

A default-deny rule over operation, principal, resource facts, relationship, and context.

## BOLA

Broken object-level authorization: access to an object without the required relationship or tenant permission.

## Existence concealment

Returning an indistinguishable not-found outcome for selected unauthorized foreign resources.

## Canonicalization

Producing one defined interpretation after protocol parsing; careless or repeated normalization can create ambiguity.

## Strict JSON

A constrained parser profile rejecting duplicate members, malformed encoding, excessive depth, and unsupported numeric forms.

## Path confinement

Resolving a path under a fixed root and proving it cannot escape through encoding, normalization, or links.

## SSRF

Server-side request forgery: abuse of server-initiated network access to reach forbidden destinations or capabilities.

## Connected-peer verification

Checking that the actual remote address used by the connection remains within the validated destination set.

## Webhook replay

Reusing an otherwise valid signed delivery to apply an effect more than once.

## Secret provider

A narrow interface that supplies secret bytes without making them generally renderable application values.

## Pepper

A separately stored secret used in keyed verification of stored credential digests.

## Pseudonymization

Replacing direct identifiers with keyed, stable aliases while retaining controlled correlation.

## Rate limit

A bound on admitted cost over time for a defined identity and operation dimension.

## Concurrency limit

A bound on simultaneous ownership of a scarce resource.

## Hostile vector

A language-neutral adversarial input with an expected security outcome.

## Mutant

A controlled implementation defect used to show that a security test can detect removal of a control.

## SBOM

A software bill of materials describing components present in a build or artifact.

## Incident containment

Actions that block or bound an active compromise while preserving necessary evidence and service safety.
