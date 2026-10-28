# Conditions and events

Conditions are durable-ish current observations on an object. Events are bounded, aggregated diagnostic records and should not be treated as an immutable audit log.

A useful condition contains:

```yaml
type: Ready
status: "False"
reason: Unschedulable
message: no node satisfies CPU and topology requirements
observedGeneration: 4
lastTransitionTime: 2026-08-09T10:00:00Z
```

Use stable reasons for automation. Keep messages concise and human-readable. Change transition time only when status changes, not on every reconcile.
