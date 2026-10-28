# Module 07 — Firewalls, NAT, Proxies, and Load Balancing

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** Which intermediary is allowed to accept, transform, route, or reject traffic, and which identity survives each hop?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Place Atlas behind a bounded reverse proxy, define host firewall policy, remove untrusted forwarding headers, and demonstrate health-aware backend removal.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Distinguish packet filtering, connection tracking, NAT, forwarding, proxying, and application routing.
- Read a least-privilege nftables policy and predict its stateful behavior.
- Separate forward proxies, reverse proxies, L4 load balancers, and L7 gateways.
- Handle client identity and forwarding headers only across trusted proxy hops.
- Design health checks, connection draining, and bounded retries without request amplification.
- Explain what a load balancer can and cannot prove about application correctness.

## Capstone increment

Place Atlas behind a bounded reverse proxy, define host firewall policy, remove untrusted forwarding headers, and demonstrate health-aware backend removal.

## Filtering, translation, proxying, and balancing are different mechanisms

A firewall decides whether traffic may pass according to packet, connection, interface, identity, or application context. NAT rewrites addresses or ports and tracks mappings. A proxy terminates one connection and creates another. A load balancer selects among backends; it may operate at transport or application level.

These mechanisms are often combined in one managed product, but the design must still say which function owns each decision.

## Stateful firewall policy starts from expected flows

nftables can track connection state. A common host policy accepts established and related traffic, allows loopback, permits necessary control traffic such as ICMP/ICMPv6, opens a small set of inbound ports, and drops the rest.

The Atlas fixture is intentionally readable. It allows HTTPS on 8443 and a placeholder management source. The placeholder must be narrowed before deployment. Copying it unchanged would be a policy failure.

```bash
nft -c -f capstone/nftables/atlas.nft
nft list ruleset
```

The static check proves syntax, not that the rule is loaded in the intended namespace, ordered correctly with other tables, or safe for remote administration.

## ICMP is not optional noise

ICMP and ICMPv6 carry errors and network-control functions. Blocking all ICMP can break path MTU discovery and IPv6 neighbor/router behavior. A least-privilege policy permits required types and rate-limits where appropriate rather than applying a slogan.

## NAT changes addressing, not application trust

Source NAT commonly allows private hosts to share an external address. Destination NAT maps an external tuple to an internal service. Neither authenticates the caller. An address observed after NAT may identify an egress gateway, not the original workload.

NAT state can expire. Long-lived idle connections may fail even when both endpoints remain healthy. Record keepalive and timeout behavior where intermediaries exist.

## A reverse proxy owns a new trust boundary

The Atlas edge accepts the client TLS connection and opens a separate HTTP connection to the loopback API. The API can trust forwarding metadata only if:

- direct access to the API is prevented or distinguishable;
- the proxy removes client-supplied forwarding headers;
- the proxy writes canonical forwarding fields;
- the API knows which peer addresses are trusted proxies;
- the deployment accounts for multiple proxy hops deliberately.

The teaching proxy discards `Forwarded`, `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Proto`, and `X-Real-IP` from the incoming request, then writes its own bounded values. It does not concatenate untrusted identity.

## L4 and L7 balancing have different evidence

A transport load balancer usually selects a backend connection using address, port, and transport state. An application load balancer can route by HTTP host, path, method, or headers and may terminate TLS. The latter sees more application context but owns more protocol behavior.

A load balancer health check proves only the check. A TCP connect check proves a listener accepted a handshake. An HTTP liveness check proves a handler responded. A readiness check may prove a selected dependency set. None automatically proves the next business operation.

## Retries can multiply work

If the edge retries, the client retries, and the backend also retries a dependency, one failed request can create a retry tree. The Atlas edge retries only safe `GET` and `HEAD` requests across alternate backends, once per candidate. It does not retry `POST /jobs`, because Course 1 has not defined an end-to-end idempotency key for the teaching API.

A bounded retry policy names method safety, failure classes, total deadline, attempt count, backoff, and duplicate-effect protection.

## Connection draining preserves bounded in-flight work

Removing a backend from new selection does not terminate existing connections automatically. A deployment should:

1. mark the backend not ready;
2. stop assigning new work;
3. wait for bounded in-flight work or a deadline;
4. close listeners or stop the process;
5. force termination only after the grace period.

For long-lived connections, draining may require explicit protocol support or client reconnect behavior.

## Forward proxy versus reverse proxy

A forward proxy acts on behalf of clients reaching external services. A reverse proxy acts on behalf of servers receiving client traffic. Both terminate connections and can observe sensitive data. Environment variables such as `HTTP_PROXY` can redirect outbound library traffic unexpectedly; `NO_PROXY` matching has implementation-specific details.

Course 1 does not use an outbound proxy, but it records egress purpose and destination policy in the network plan.

## Worked investigation: every request appears internal

The API audit log reports `127.0.0.1` for every caller because the reverse proxy is the direct TCP peer. A developer changes the API to trust any `X-Forwarded-For` value. Now a direct client can claim any source.

The correct repair is architectural:

- keep the API loopback-only or firewall it to proxy peers;
- have the proxy remove and rewrite forwarding identity;
- configure the application with an exact trusted-proxy set;
- log both direct peer and derived client identity;
- test a spoofed incoming header.

Do not infer authorization from source IP. The forwarded address is operational context, not a user identity.

## Managed load balancers map to the same questions

A cloud load balancer adds managed listeners, certificates, health checks, zones, routing, and telemetry. The exact product differs, but the architecture must still answer:

```text
Where is TLS terminated?
Which backend address is reachable?
Which headers are created or rewritten?
Which health signal controls routing?
How are zones selected?
What is the idle timeout?
What is the source identity seen by the backend?
How is draining performed?
```

These questions become Course 2 requirements rather than provider console screenshots.

## Atlas implementation bridge

Read `proxy.py`, `nftables/atlas.nft`, and `nginx/atlas.conf`. The Python edge makes header and retry policy executable; nginx is the maintained-proxy deployment example. The firewall file is syntax-checked but must not be loaded remotely without a console and rollback.

Inject an incoming `X-Forwarded-For` value and verify the API receives the edge-derived identity instead. Stop the backend and verify a bounded 503 rather than an infinite retry loop.

## Design review prompts

- Which peer is allowed to create forwarding identity?
- Which requests can be retried without duplicate effects?
- Which ICMP traffic is required?
- How is a backend drained?
- Does a managed load balancer change business authorization ownership?

## Boundary case: asymmetric paths

The request and response can traverse different routers, NAT devices, or policies. Stateful firewalls may drop return traffic if they do not observe the initiating flow. Source-based routing and multi-interface hosts can create asymmetric paths that work intermittently.

Packet evidence at both ends, connection tracking, and route selection are stronger than assuming symmetry from the diagram.

## Boundary case: health check as load

A deep readiness check that queries every dependency at high frequency can become significant traffic or synchronize failure across the fleet. Check only prerequisites needed for routing, cache results briefly where appropriate, and make the health path cheaper than ordinary work. Avoid placing destructive repair in a health handler.

## Intermediary worksheet

```text
intermediary:
layer terminated:
new connection created:
identity received:
identity forwarded:
TLS responsibility:
health signal:
retry policy:
timeout/idle policy:
drain behavior:
failure response:
```

Complete one row for host firewall, cloud load balancer, reverse proxy, and any outbound proxy. If a row has no owner, the traffic path is not governable.

## Field method: preserve identity and retry ownership across intermediaries

Every intermediary terminates one connection and may create another. Draw both connections. Record where TLS terminates, which source address is visible, which headers are trusted, which timeout applies, and which component may retry. A diagram with one arrow from client to service hides the decisions that produce most edge incidents.

Forwarded identity is an assertion by a trusted proxy, not client-controlled truth. The Atlas teaching edge removes incoming `Forwarded`, `X-Forwarded-*`, and `X-Real-IP` fields before writing its own bounded values. The application must trust them only when the immediate peer belongs to the configured proxy boundary. In a multi-proxy path, define how many hops are trusted and reject ambiguous chains.

Retries multiply demand. If a client performs three attempts, a load balancer performs two, and a proxy performs two, one logical operation can become twelve backend attempts. Restrict retries to operations whose semantics and idempotency permit them, use one owner where possible, preserve an overall deadline, and cap total attempts. The teaching edge retries only safe reads after a connection-level failure; it does not replay `POST /jobs`.

Connection draining is a protocol between routing and process lifecycle. First stop admitting new work, then allow bounded in-flight work to finish, then close or terminate. A load balancer's health removal delay, proxy keepalive pool, application shutdown deadline, and systemd `TimeoutStopSec` must form one coherent budget. Killing the process before route withdrawal creates avoidable resets; waiting forever blocks deployment.

NAT can obscure original addresses and maintain state that outlives one endpoint. Stateful firewalls depend on observing both directions. Asymmetric routing can therefore break traffic even when each one-way route appears valid. Diagnose from both ends and include connection-tracking state when the firewall is stateful.

The bundled Python edge is a semantic demonstrator for header policy, bounded body handling, TLS, safe retry, and graceful termination. The maintained Nginx example is closer to an operational proxy but still requires environment-specific hardening, log policy, certificate automation, and load testing. Neither is presented as a universal production edge.


## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| Forwarded client identity is trusted only across an explicitly trusted proxy boundary. | Atlas security policy | spoofed-header regression |
| Stateful firewall acceptance and NAT translation are not caller authentication. | network mechanism | packet/connection state plus application identity |
| Unsafe or non-idempotent requests are not retried by the teaching edge. | Atlas proxy policy | backend-failure request test |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### Trusted-header ambiguity

Appending client-supplied forwarding fields without an exact proxy chain permits identity spoofing.

### Health-check overclaim

A successful TCP or HTTP probe does not prove business correctness.

### Retry tree

Independent retries at client, proxy, service, and dependency layers amplify load during failure.


## Module synthesis

Return to the central question: **Which intermediary is allowed to accept, transform, route, or reject traffic, and which identity survives each hop?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**The API trusts any client-supplied `X-Forwarded-For`, allowing an external caller to impersonate a private source address.**—fails for the predicted reason.

## Continue

Module 08 moves the proven host model into a virtual-machine and image lifecycle.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
