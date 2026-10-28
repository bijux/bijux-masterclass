# Capstone walkthrough

1. Verify the Course 3 handoff manifest.
2. Validate production-intent manifests and exact image subjects.
3. Create an AtlasWorkload in the semantic API store.
4. Reconcile until no writes occur.
5. stop one control loop and show desired state remains without convergence.
6. restart it and prove recovery without duplicate children.
7. calculate an API rollout and inject failed readiness.
8. explain an impossible scheduling case.
9. execute finalizer cleanup with one denied attempt and one successful retry.
10. generate and verify the Course 5 handoff.

Run `make capstone-tour` for the dependency-light path. Run `make kind-proof` only in an isolated, fully provisioned local-cluster environment.
