# Runbook — Atlas Certificate or Name Failure

## Trigger

Verified clients report unknown issuer, name mismatch, expiry/not-yet-valid, incomplete chain, or TLS negotiation failure.

## Diagnose in order

1. Resolve the requested name and record addresses.
2. Confirm the route and endpoint.
3. Inspect the certificate served for the requested SNI.
4. Verify chain, SAN, validity, key usage, and client trust source.
5. Check HTTP authority separately after TLS succeeds.

## Recover

Repair DNS, routing, certificate selection, chain, trust distribution, or clock according to the failed layer. Preserve an overlap window during rotation.

## Prohibited shortcut

Do not disable certificate verification or replace the request name with an unrelated IP as the final repair.
