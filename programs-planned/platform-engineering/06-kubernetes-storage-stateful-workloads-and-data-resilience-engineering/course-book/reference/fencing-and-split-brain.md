# Fencing and split brain

Leader election selects a current actor. Fencing prevents previous actors from continuing to mutate authoritative state.

A robust fencing token is monotonic and checked by the protected system:

```text
writer A → generation 8 → accepted
writer B takes over → generation 9 → accepted
late writer A → generation 8 → rejected
```

## Mechanism comparison

| Mechanism | Useful for | Limitation |
|---|---|---|
| Kubernetes Lease | coordinating current holder | stale holder may still write outside the lease |
| storage detach | removing access path | old process may retain access during partition or timeout |
| quorum term | replicated data services | requires correct consensus membership and persistence |
| database advisory lock | cooperative writers | not safe if a writer bypasses the same database boundary |
| monotonic fencing token | rejecting stale effects | protected store must enforce the token |
| external power/storage fencing | terminating old host or access | operationally expensive and provider-specific |

## Required proof

Simulate takeover while the old process remains alive. The new writer must make progress and the old generation must fail closed. Restart the coordinator and repeat. A proof that only stops the old process is not a fencing proof.
