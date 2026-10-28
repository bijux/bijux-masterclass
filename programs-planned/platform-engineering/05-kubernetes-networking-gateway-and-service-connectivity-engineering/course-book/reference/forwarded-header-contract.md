# Forwarded-header contract

Atlas accepts forwarded client metadata only from an authenticated and network-approved Gateway hop.

The Gateway:

- discards untrusted inbound `X-Forwarded-*` values;
- writes the observed immediate client address according to edge policy;
- writes the accepted external scheme and authority;
- propagates a bounded request identifier;
- does not convert IP address into application authorization.

The API:

- trusts these headers only on the Gateway path;
- records direct peer and forwarded value separately;
- rejects ambiguous duplicate values according to the HTTP-edge contract;
- uses authenticated user/workload identity for authorization.

Direct backend access must not be treated as though it traversed the trusted edge.
