# Case 2 — Force detach and split brain

## Incident

A Node becomes unreachable while hosting the current database primary. An operator force-detaches the volume and starts the same ordinal on another Node. Minutes later, the old Node returns and both processes can reach data paths.

## Evidence

- The old primary held generation 41.
- The replacement was started without incrementing or enforcing a fencing generation.
- Storage detach status was used as proof that the old writer had stopped.
- The old Node had experienced a control-plane partition, not confirmed power loss.

## Failure

Attachment state reduced access but did not revoke application authority. The system had leader selection without fencing. Two writers could now produce incompatible histories.

## Correct response

Stop client writes, preserve both histories, determine the last common committed generation, and follow the database’s documented split-brain recovery. For future recovery, allocate a new monotonic generation before replacement and require every write to be rejected unless it carries the current generation. Couple force detach with an external proof that the old writer is fenced.

## Lesson

A force-detach runbook must name the data-service authority and the stale-writer oracle. “Volume attached to only one Node” is not a sufficient application guarantee.
