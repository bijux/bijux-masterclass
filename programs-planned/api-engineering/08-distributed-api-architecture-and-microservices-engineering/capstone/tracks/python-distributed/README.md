# Python reference track

This track is a dependency-light semantic reference for Course 8. It models service ownership, versioned projections, synchronous dependency budgets, sagas, capability tokens, routing, extraction, and reconciliation without pretending that an in-process test is a production network.

Run with:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m distributed_api.tour
```
