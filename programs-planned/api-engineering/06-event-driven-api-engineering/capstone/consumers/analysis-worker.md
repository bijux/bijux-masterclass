# Analysis worker consumer

**Input:** `com.bijux.analysis.command.start.v1`

**Effect:** claim or reconcile one durable run execution. The stable command identity is `start:<runId>:<generation>`. A duplicate command must observe existing execution state rather than launch another independent run.

**Ordering:** by `runId`.

**Replay:** workflow review is mandatory because the command can initiate expensive work. Historical commands are never replayed blindly.
