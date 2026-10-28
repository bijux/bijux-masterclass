# Final verification

This record separates what the release environment executed from what remains environment-backed.

## Executed course proof

The finalized source tree passed:

```text
Course 4 predecessor handoff:       10 exact files
Course-book navigation:             107 exact pages
Course-book words:                  approximately 56,000
Numbered modules:                   10 plus orientation
Exercises / worked answers:         120 / 120
Laboratories / checkpoints:         10 / 10
Python tests:                       30 passed
Go modules:                         2 passed
Kubernetes/Gateway resources:       18 parsed resources
Release candidates:                 7 classified
Planted defects:                    10 verified
Course 6 handoff:                   10 exact files
Capstone experiments:               10 passed
Course manifest payload:             287 exact files
Program overlay manifest payload:    302 exact files
```

The educational-quality proof additionally requires:

- every core chapter to contain at least 2,000 words;
- orientation to contain at least 800 words;
- every worked answer to contain at least 55 words;
- no repeated long prose four or more times;
- no unfinished markers;
- exact exercise/answer heading identity;
- complete lab and checkpoint structures.

## Real local network evidence

The loopback lane executed real processes and sockets for:

- UDP DNS query and response;
- positive and negative DNS behavior;
- Service-style selection across multiple backend processes;
- removal of an unready endpoint from new selection;
- TLS chain verification against the course CA;
- rejection of the wrong certificate hostname;
- successful SNI and hostname verification for `atlas.test` while the TCP address was pinned to loopback;
- HTTP authority enforcement;
- replacement of untrusted forwarding metadata;
- egress redirect and connected-peer classification.

The course private-key fixtures are non-deployable educational material and are stored with mode `0600`.

## Executed toolchain

```text
Python: 3.13.5
Go:     1.23.2
OpenSSL: 3.5.5
Host:   Linux x86_64
```

## Not executed in the release environment

The environment did not provide `kubectl`, kind, Docker/Podman, Cilium CLI, kubeconform, or MkDocs. Therefore the release does not report these as successful:

- live Kubernetes API admission/defaulting/conversion;
- real CNI attachment, IPAM, route, and policy enforcement;
- CoreDNS running inside a cluster;
- EndpointSlice-to-node data-plane convergence on multiple Nodes;
- native dual-stack and cross-Node behavior;
- Gateway controller reconciliation and data-plane programming;
- cloud load-balancer, managed DNS, NAT, firewall, or private-endpoint behavior;
- multi-node or multi-zone failure;
- representative production capacity, upgrades, incidents, and recovery;
- strict MkDocs site rendering.

The package contains guarded procedures, oracles, cleanup, and evidence requirements for these lanes. Their absence remains `not-executed`, not a synthetic pass.

## Claim boundary

The release is a production-intent, deeply verified educational reference. It proves the internal Atlas contracts and the executed local mechanisms. It does not certify any Kubernetes distribution, CNI, Gateway controller, cloud provider, or operated production environment.
