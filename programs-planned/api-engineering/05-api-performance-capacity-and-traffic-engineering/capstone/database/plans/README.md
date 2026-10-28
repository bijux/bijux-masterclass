# Packaged PostgreSQL plan fixtures

These four JSON documents are deterministic teaching fixtures shaped like
`EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` output. They let the dependency-light
course proof exercise plan traversal, block accounting, sequential-scan
identification, disk-sort detection, and before/after comparison.

They are **Class A fixtures**, not measurements from the learner's machine and
not evidence that migration 009 improves a live database. The live lab must use
representative data and capture its own plans. Keep the SQL, parameter set,
PostgreSQL version, statistics state, schema revision, and data distribution
beside every live plan.
