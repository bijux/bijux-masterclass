# DVC Reference Capstone

The DVC course has a stable place for its executable reference project in `capstone/`.

That reference project demonstrates the full contract taught in the course:

- immutable data identity
- explicit stage dependencies
- tracked parameters and metrics
- experiment promotion rules
- CI-backed recovery checks
- remote and retention discipline

The reference implementation is an incident-escalation pipeline with:

- deterministic train and eval splits from a committed source dataset
- a truthful four-stage `dvc.yaml` graph (`prepare`, `fit`, `evaluate`, `publish`)
- a learned logistic model serialized into `models/model.json`
- tracked metrics in `metrics/metrics.json`
- a stable publish boundary at `publish/v1/` with a manifest and report
- a recovery drill that pushes to a local remote, deletes cache and workspace state, then restores them through DVC

From the repository root, the course-level proof target is:

```bash
make COURSE=reproducible-research/deep-dive-dvc test
```
