# Resource units and QoS reference

## CPU

`1` CPU is one logical CPU unit. `100m` is one tenth of a CPU. Requests influence scheduling; limits become CFS quota on Linux when enforced.

## Memory

Memory values use bytes or binary/decimal suffixes. `128Mi` is 134,217,728 bytes. Memory is not throttled like CPU; exceeding a hard cgroup limit can terminate a process.

## QoS classes

- **Guaranteed:** every container has equal CPU request/limit and memory request/limit.
- **Burstable:** at least one request or limit exists but Guaranteed rules are not met.
- **BestEffort:** no CPU or memory requests/limits.

QoS class influences pressure handling; it is not an availability guarantee.

## Atlas baseline hypothesis

```text
request: 100m CPU, 64Mi memory
limit:   500m CPU, 128Mi memory
```

These values are inherited hypotheses, not production sizing evidence. Course 5 measures and revises them.
