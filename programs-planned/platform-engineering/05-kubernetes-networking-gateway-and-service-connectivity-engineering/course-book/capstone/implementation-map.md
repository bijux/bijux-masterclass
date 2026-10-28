# Capstone implementation map

The capstone uses one implementation only where it clarifies an ownership or failure boundary. It does not reproduce a complete Kubernetes network stack.

| Course concept | Executable artifact | Decisive proof |
|---|---|---|
| address domains and routes | `capstone/atlas_net/models.py`, `routing.py` | longest-prefix and family-specific route tests |
| path MTU | `mtu.py` | calculated boundary plus small/large packet experiment |
| CNI/IPAM lifecycle | `cni.py`, `capstone/cni-go/` | replay, repeated delete, generation-safe GC, dependency status |
| Service convergence | `services.py` | desired versus per-Node programmed generation |
| endpoint locality | `locality.py` | hard-local rejection and preference fallback |
| DNS records and caches | `dns.py` | exact candidate names, negative-cache timeline, UDP loopback DNS |
| NetworkPolicy semantics | `policy.py` | independent source egress and destination ingress decisions |
| Gateway attachment/routing | `gateway.py` | listener/Route/reference and request-match tests |
| trusted proxy behavior | `localnet.py`, `network_lab.py` | replacement of forged forwarding headers |
| public TLS | `tls.py`, `capstone/pki/` | CA/hostname negative controls and real loopback handshake |
| egress policy | `egress.py` | hostname, resolved set, peer, redirect, and address-class decisions |
| categorical release | `release.py`, `capstone/releases/` | accepted/rejected/review/not-executed fixtures |
| operational investigation | `capstone/scripts/` | ten bounded experiments and final game day |
| native cluster lane | `capstone/kind/`, `capstone/cilium/` | guarded environment-backed proof when tools are available |
| Course 6 boundary | `capstone/handoff/` | exact manifest verification |

## How to read the map

The semantic implementation exposes decisions that a production implementation may hide in controller state, kernel maps, proxy configuration, or cloud resources. A passing semantic test establishes the rule. The native lane must still prove the chosen CNI, Service data plane, policy engine, Gateway, DNS, and cloud integration.

No removed or obsolete source file is part of the teaching route. `make core-proof` exercises every dependency-light artifact named above.
