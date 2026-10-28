# Rollout mathematics reference

For desired replicas `R`:

```text
surge integer       = ceil(R × surge percentage)
unavailable integer = floor(R × unavailable percentage)
maximum total Pods  = R + surge integer
minimum available   = R - unavailable integer
```

Integer values are used directly. Percentages must be resolved for each replica count.

| R | 25% surge | 25% unavailable | max Pods | min available |
|---:|---:|---:|---:|---:|
| 1 | 1 | 0 | 2 | 1 |
| 2 | 1 | 0 | 3 | 2 |
| 3 | 1 | 0 | 4 | 3 |
| 4 | 1 | 1 | 5 | 3 |
| 5 | 2 | 1 | 7 | 4 |
| 10 | 3 | 2 | 13 | 8 |

These are policy bounds. Scheduling, quota, readiness, topology, and disruption can make them infeasible.
