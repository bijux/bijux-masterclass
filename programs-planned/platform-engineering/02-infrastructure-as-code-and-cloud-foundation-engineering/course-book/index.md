# Infrastructure as Code and Cloud Foundation Engineering

Infrastructure as code is often taught as syntax: write a resource block, run a plan, apply it. That is not enough for a platform engineer.

A real cloud foundation is a long-lived agreement among configuration, state, provider APIs, organizational policy, human approvals, and workloads that depend on the result. The difficult failures are rarely missing braces. They are ownership failures: two pipelines write the same state, an imported resource has no stable configuration, a module hides a security decision, a “harmless” rename destroys a database, a successful apply leaves an unhealthy data plane, or an emergency console change is never reconciled.

This book develops a disciplined model of those failures while building Atlas Cloud Foundation 1.0.

## Course arc

1. Understand OpenTofu as a graph-based change engine.
2. Treat state as sensitive operational data with locking and recovery requirements.
3. Build modules that raise architectural meaning instead of wrapping resources mechanically.
4. Establish account, identity, audit, budget, and policy boundaries.
5. Design explicit network paths.
6. Grant short-lived workload authority and protect secrets and keys.
7. Build replaceable compute from versioned inputs.
8. Engineer edge, durable data, backup, and restore.
9. Import, refactor, and migrate without accidental replacement.
10. Release infrastructure through tested, reviewable, policy-governed automation.

The course culminates in a final defense where the learner must explain not only what exists, but how it changes, how it fails, and how another operator recovers it.
