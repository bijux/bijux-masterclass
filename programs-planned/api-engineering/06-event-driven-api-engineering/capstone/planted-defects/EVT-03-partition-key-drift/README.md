# EVT-03-partition-key-drift

**Mutation:** Producer changes partition key from runId to eventId.

**Required oracle:** ordering proof rejects two lifecycle facts for one run landing in different partitions.

The learner must show the named proof fails before repair and passes after repair. A code review comment alone is not completion evidence.
