# IPAM ownership and recovery

An IPAM record should bind:

```text
network
attachment ID
generation
container/sandbox identity
Pod UID
interface
address family
allocated address
Node
creation time
active/released state
```

Display names are insufficient because they can be reused. Allocation must serialize uniqueness. Dual-stack failure policy must state whether one-family success rolls back or produces partial state.

Recovery questions:

- What survives plugin restart and Node reboot?
- Who declares an attachment abandoned?
- How is stale Node cleanup fenced from a replacement generation?
- How are leaked addresses detected before exhaustion?
- How is address reuse delayed or validated to avoid misdelivery?

Garbage collection should produce an audit of removed and retained records. Manual deletion of IPAM files is a break-glass action with a snapshot and rollback plan.
