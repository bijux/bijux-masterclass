# Probe decision table

| Question | Probe/control | Typical failure action |
|---|---|---|
| Has slow initialization completed? | startup probe | continue startup budget or fail/restart after threshold |
| Is process irrecoverably stuck and restart is plausible? | liveness probe | container restart |
| Should this instance receive normal work? | readiness probe | remove from eligible endpoint population |
| Should deletion wait while work drains? | preStop + signal handling + grace period | controlled termination |
| Is a controller rollout stable? | availability/minReadySeconds | withhold rollout progress |

A probe must not be chosen by endpoint availability alone. The question and repair action must match.
