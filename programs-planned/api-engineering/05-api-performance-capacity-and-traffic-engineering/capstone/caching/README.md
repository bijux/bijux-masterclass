# Cache design package

The course does not require Redis. The executable cache is process-local so the
learner can prove key identity, expiry, version invalidation, single-flight
collapse, and authorization boundaries without adding an external system.

A production design review must still answer:

- which representation is cached;
- which principal and tenant dimensions are part of the key;
- what source version invalidates the entry;
- whether stale data is permitted and for how long;
- how failures affect freshness;
- whether each process owns an independent cache;
- what evidence justifies introducing a distributed cache.
