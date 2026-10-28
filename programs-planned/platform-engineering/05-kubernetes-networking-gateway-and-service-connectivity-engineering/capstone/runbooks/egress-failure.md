# Runbook — egress dependency unavailable

1. Record logical hostname, approved ports, TLS name, and required path.
2. Capture DNS answers and address classification for each family.
3. Verify source policy and route to proxy, NAT, gateway, or private endpoint.
4. Record the actual connected peer and compare it with the approved answer set.
5. Revalidate every redirect and retry destination.
6. Inspect NAT/proxy capacity and connection reuse before increasing retries.
7. Preserve intended denial to loopback, link-local, metadata, and unapproved private destinations.
