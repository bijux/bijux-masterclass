# Loopback graph-composition laboratory

This laboratory starts four independent HTTP servers on loopback addresses:
Analysis Control, Artifact Service, Notification Service, and the Graph
Gateway. The gateway accepts one registered operation by SHA-256 identity and
then makes real network calls to the three service owners. No resolver reads a
shared business database.

The exercise isolates four claims that are easy to blur in an in-process test:

1. **Composition is remote collaboration.** The gateway performs two Analysis
   Control reads and one batched call to each supporting service.
2. **Tenant context crosses every boundary.** A tenant-B request cannot observe
   the tenant-A project, even through the composition layer.
3. **Partial failure is field-specific.** When Artifact Service returns `503`,
   each affected `artifacts` field becomes `null` and receives an exact GraphQL
   error path. Project, run, and delivery data remain available.
4. **A trusted document is not arbitrary query text.** The lab accepts only the
   exact digest of `GetProjectOverview.graphql`.

Run it from the course root:

```bash
make network-lab-proof
```

The test is dependency-light and uses the Python standard library. It does not
claim to replace a production GraphQL server, service mesh, workload identity
system, or distributed tracing topology. Its purpose is narrower: to prove the
composition and failure semantics taught in Modules 3 and 8 over actual TCP
boundaries.
