# Course 7 bridge — from recoverable data to governed delivery

Course 6 ended with a data plane whose authority, recovery gates, protected resources, and migration order are explicit. Course 7 does not replace those decisions with automation. It asks a harder question: **how may automation change the system without pretending that reconciliation proves data safety?**

The Course 6 handoff imposes five non-negotiable constraints:

1. retained volumes, snapshots, backup manifests, and recovery keys are not ordinary prune candidates;
2. schema and storage migration phases have an order that a controller may execute but may not invent;
3. a deployment rollback is not automatically a data rollback;
4. restore evidence must remain current before promotion;
5. delivery credentials must not become backend data credentials.

Course 7 adds a new control loop around the existing Kubernetes runtime. Git, OCI registries, renderers, delivery controllers, admission controls, and progressive-delivery systems each own a different transition. The learner must know which transition failed before choosing a repair.

The resulting **Atlas Delivery Plane 1.0** publishes reviewed, immutable desired-state revisions; renders them deterministically; reconciles them with inventory and prune protection; promotes the same artifact identities through environments; and records enough evidence to explain every release decision.
