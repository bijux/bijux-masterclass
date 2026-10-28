# Practical Examination — The Atlas Host Is Green but Jobs Do Not Complete

## Scenario

The edge returns `200` for liveness and `202` for job submission. Jobs remain in `processing`. A recent hardening and storage change was deployed. CPU is low. Operators propose restarting every process and making `/var/lib/atlas` world-writable.

## Time box

120 minutes in a disposable VM or the supplied simulation environment.

## Required work

1. Record process, supervisor, cgroup, listener, mount, permission, and spool state before repair.
2. State at least three plausible hypotheses and the observation that distinguishes each.
3. Identify the first failed boundary.
4. Repair the owning mechanism without granting broad authority or deleting queue evidence.
5. Demonstrate recovery of the existing job or explain why recovery is not safe.
6. Submit a new job through verified TLS and retrieve the result.
7. Stop and restart the worker gracefully.
8. Clean all temporary changes and verify the baseline.

## Deliverables

- timestamped command transcript;
- before/after causal diagram;
- evidence table with claim, oracle, result, and evidence class;
- exact configuration diff;
- focused regression result;
- residual-risk statement;
- one Course 2 requirement updated if the incident exposed a missing infrastructure assumption.

## Scoring emphasis

Diagnosis and boundary preservation matter more than speed. Restarting or weakening permissions before collecting evidence loses points even when service resumes.
