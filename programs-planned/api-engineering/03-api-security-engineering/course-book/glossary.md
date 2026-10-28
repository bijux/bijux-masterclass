# Glossary — API Security Engineering

These terms have precise meanings in Course 3. Use them with the program glossary at `program-book/glossary.md`, which preserves shared meanings across the complete sequence.

## asset

Something with value that the system must protect, such as credentials, tenant data, availability, artifact integrity, or audit evidence.

## threat

A plausible actor, condition, or action capable of violating a security property of an asset.

## abuse case

A concrete hostile or improper interaction described from the attacker’s goal through the expected defensive outcome.

## trust boundary

A point where data or authority crosses between components, identities, networks, or administrative domains with different assumptions.

## security invariant

A security property that must hold across all relevant paths, such as “a principal cannot read another tenant’s artifact.”

## principal

The authenticated identity on whose behalf a request or action is evaluated.

## issuer

The authority identified by a token’s `iss` claim and trusted to create the credential under a configured policy.

## audience

The intended recipient identified by a credential; the resource server must reject tokens not issued for it.

## scope

A delegated permission string constraining categories of actions; it does not by itself establish tenant membership or object ownership.

## role

A named grouping of permissions or responsibilities assigned within a defined administrative context.

## tenant

An isolation domain whose data, quotas, policies, and memberships must not be confused with those of another tenant.

## object ownership

The relationship establishing which principal or tenant controls a specific resource instance.

## default deny

The policy that access is refused unless a rule explicitly authorizes the exact action and resource context.

## confused deputy

A failure in which a component with authority is induced to use that authority for a caller who is not entitled to the result.

## canonicalization

The process of converting multiple textual or structural representations into one form before comparison, signing, policy, or hashing.

## SSRF

Server-side request forgery: attacker influence over outbound requests that can reach unintended hosts, networks, protocols, or credentials.

## replay

Reuse of a valid credential, signed message, or request outside its intended one-time or freshness boundary.

## secret rotation

Replacing active secret material while supporting a bounded overlap and an explicit retirement path for the old version.

## audit event

A privacy-bounded, security-relevant record of who attempted what action, on which protected object, with which decision and reason.

## abuse budget

A bounded allowance for costly or suspicious behavior, enforced across dimensions such as principal, tenant, operation, and resource cost.

## residual risk

The explicitly accepted risk remaining after controls and verification, with an owner, rationale, review point, and limits.
