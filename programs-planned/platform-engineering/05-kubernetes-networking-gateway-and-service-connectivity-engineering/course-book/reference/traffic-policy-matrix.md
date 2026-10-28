# Traffic policy matrix

| Policy | Eligible endpoints | Fallback | Main benefit | Main risk |
|---|---|---|---|---|
| `internalTrafficPolicy: Cluster` | cluster-wide | inherent | availability across Nodes | cross-Node hop/source changes |
| `internalTrafficPolicy: Local` | local Node only | none | local hop, implementation-specific source behavior | no local endpoint means no service |
| `externalTrafficPolicy: Cluster` | cluster-wide | inherent | broader availability | possible source translation/cross-Node path |
| `externalTrafficPolicy: Local` | local Node only | none | source preservation in some designs | load-balancer/placement dependency |
| `trafficDistribution: PreferClose` | all eligible, nearby preferred | remote | latency/cost preference | skew; not a guarantee |

Choose from workload placement and failure evidence. A hard local policy requires local capacity on every receiving Node or appropriate load-balancer registration.
