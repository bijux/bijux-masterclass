# Case 4 — The impossible rollout

Atlas API has three replicas, `maxSurge: 1`, `maxUnavailable: 0`, hard hostname anti-affinity, and two eligible Nodes. Existing Pods consume all feasible slots. The new revision is admitted, but the surge Pod remains Pending.

All major cluster components are healthy. The Deployment controller correctly refuses to remove an old available Pod because zero unavailability is allowed. The scheduler correctly refuses to place the new Pod because no feasible slot exists. The rollout policy and capacity topology are jointly impossible.

The team evaluates repairs:

1. delete the Pending Pod — rejected; it recreates with the same constraints;
2. increase progress deadline — rejected; time does not create capacity;
3. weaken readiness — rejected; it changes eligibility, not placement;
4. add an eligible Node — safe if capacity can be provisioned within release objectives;
5. permit one unavailable replica — possible only after accepting reduced availability;
6. relax anti-affinity — possible only after accepting a weaker failure-domain policy.

The chosen repair is explicit and recorded with resolved rollout integers. The release gate is changed to check surge feasibility before promotion.

**Lesson:** some rollout failures are proofs that the declared strategy cannot execute in the available topology.
