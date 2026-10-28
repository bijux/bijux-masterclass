# Artifact index consumer

**Input:** `org.bijux.analysis.artifact.published.v1`.

**Effect:** materialize owner- and tenant-aware search metadata. The event contains metadata and a checksum, not artifact content.

**Replay:** projection-safe. The index can be rebuilt under a new effect version and compared before cutover.
