# Runbook — Gateway route does not serve traffic

1. Verify the expected GatewayClass controller is active.
2. Inspect Gateway listener acceptance, addresses, and certificate references.
3. Inspect Route status per parent: Accepted, ResolvedRefs, and Programmed.
4. Check hostname intersection, listener namespace policy, and section name.
5. Verify ReferenceGrant in the target namespace for cross-namespace references.
6. Inspect Service and endpoint usability after route attachment succeeds.
7. Run one positive and one deliberately non-matching protocol probe.
