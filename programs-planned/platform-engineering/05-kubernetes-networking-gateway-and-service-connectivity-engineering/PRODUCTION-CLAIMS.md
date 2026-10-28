# Production claims and evidence boundary

The course provides production-intent designs and dependency-light semantic proofs. A semantic model can prove that a policy engine, route matcher, endpoint selector, or release classifier follows the stated Atlas contract. It cannot certify a particular CNI, service proxy, CoreDNS deployment, Gateway controller, kernel, cloud load balancer, or managed cluster.

Evidence is classified as:

1. **Document evidence** — contracts, manifests, and reviewable design.
2. **Semantic evidence** — deterministic models and shared vectors.
3. **Local network evidence** — real loopback sockets, DNS packets, TLS, proxying, and process failure.
4. **Cluster evidence** — real Kubernetes, CNI, DNS, NetworkPolicy, Service, and Gateway resources.
5. **Environment evidence** — cloud load balancers, routed networks, managed DNS, and operated failure domains.
6. **Operated evidence** — representative traffic, upgrades, incidents, capacity, and recovery over time.

Only executed evidence is reported as executed. Missing infrastructure never becomes a synthetic pass.
