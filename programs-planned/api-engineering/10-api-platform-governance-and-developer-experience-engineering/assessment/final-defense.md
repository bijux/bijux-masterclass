# Final platform defense

Demonstrate Analysis API Platform 1.0 from five perspectives. The **consumer** must discover and use an interface safely. The **API owner** must publish and evolve a release. The **governance reviewer** must interpret evidence, handle a bounded exception, and reject an unsafe candidate. The **operator** must reconcile approved and observed runtime state and route support. The **platform product owner** must interpret adoption, time to first success, deprecated usage, and support burden without substituting vanity activity for outcomes.

The defense must include:

1. discovery of the HTTP, event, RPC, GraphQL, and platform-control surfaces and their owners;
2. verification of immutable contract releases by digest;
3. one policy pass, one review-required exception, and one hard rejection;
4. a deprecation impact report that blocks unsafe retirement;
5. generation of a new API surface from the golden path, followed by explanation of what the template cannot decide;
6. a documentation and isolated-sandbox onboarding flow ending in a recorded first successful outcome;
7. SDK publication with contract digest, SBOM, provenance-profile evidence, and an honest statement of what was not externally attested;
8. runtime desired-state reconciliation without domain policy at the edge;
9. product metrics that distinguish discovery and adoption from successful consumer outcomes;
10. a federated decision explaining what the platform team owns, what the domain owner owns, what the operator owns, and which risks require governance review;
11. one recovery scenario for catalog, registry, portal, or policy-engine unavailability;
12. a final residual-risk statement distinguishing executed proof, environment-backed proof, and unproven production behavior.

A successful defense explains authority, mechanism, failure mode, evidence, limitation, and accountable next action. Merely showing green reports is insufficient.
