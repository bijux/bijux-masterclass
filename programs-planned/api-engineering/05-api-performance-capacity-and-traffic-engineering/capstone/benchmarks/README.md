# Benchmark laboratory

The course ships three complementary harnesses:

1. `harness/run_tour.py` is dependency-light and deterministic enough for the
   release package. It proves measurement identity, correctness gating, outcome
   conservation, HTTP validators, byte ranges, and comparison behavior.
2. `locust/locustfile.py` expresses a closed interactive model in Python.
3. `k6/*.js` expresses open-arrival and mixed workloads without relying on a
   tool default.

The local harness is not a production capacity test. It deliberately reports
**evidence class B**. k6 and Locust examples become meaningful only after the
learner records generator capacity, network topology, target limits, data scale,
and source revision. A benchmark result without those identities is rejected.
