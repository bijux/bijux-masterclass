# Worked answers — Service Identity, Authorization, and Trust Propagation

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. Why is workload identity insufficient to authorize an artifact upload?

It proves which service or worker is calling, not which tenant, run, attempt, checksum, and action are allowed. Resource authority must be narrower.

**Decisive evidence:** capability authorization vector

## 2. What is the confused-deputy risk when Artifact Service trusts `X-User-Id`?

A caller can forge or overstate user authority, and Artifact Service cannot prove who validated it or for which audience. Signed delegation or capability is required.

**Decisive evidence:** forged-header rejection test

## 3. Why does a capability include audience?

A token minted for Artifact Service must not be replayed to Analysis Control or another service. Audience limits where the authority is meaningful.

**Decisive evidence:** wrong-audience test

## 4. Why bind an upload capability to checksum and maximum size?

It limits what bytes and resource cost the holder may create, preventing substitution and unbounded upload under an otherwise valid token.

**Decisive evidence:** checksum and size proof

## 5. Can mTLS replace resource authorization?

No. It authenticates the workload channel, not whether that workload may act on a specific tenant resource for a user.

**Decisive evidence:** workload-versus-resource policy matrix

## 6. Why should the original public bearer token not automatically be forwarded to every service?

It may have the wrong audience, excessive scope, long lifetime, and exposure surface. Downstream delegation should be purpose- and audience-bound.

**Decisive evidence:** token propagation review

## 7. What context is safe to put in trace baggage?

Only bounded non-sensitive diagnostic context. Credentials, API keys, PII, and authorization decisions must not be placed there.

**Decisive evidence:** baggage redaction test

## 8. Who performs the decisive artifact authorization?

Artifact Service, because it owns the artifact. Gateway and Control may reject early or mint authority, but the owner validates the capability and resource.

**Decisive evidence:** owner-side authorization proof

## 9. Why must Control reauthorize completion after artifact upload?

The run attempt or tenant policy may change during transfer. Storage authority does not imply completion authority.

**Decisive evidence:** stale capability schedule

## 10. What does network policy contribute?

It restricts reachable paths and reduces blast radius. It is defense in depth, not a substitute for service authentication or business authorization.

**Decisive evidence:** network-policy and application-policy comparison

## 11. How does short capability lifetime reduce coupling and risk?

Artifact Service can verify locally without a synchronous Control call, while the brief lifetime limits leakage and stale-policy exposure.

**Decisive evidence:** capability lifetime analysis

## 12. Why is a shared internal superuser token unacceptable?

It erases service attribution, grants excessive authority, makes revocation broad, and turns one credential compromise into platform-wide access.

**Decisive evidence:** credential inventory and compromise scenario
