# Assessment Rubric

The course is scored out of 100. A score of 85 is required, but the non-compensable gates below must also pass.

| Area | Points | Evidence expected |
|---|---:|---|
| Process and lifecycle reasoning | 10 | descriptor/process map, graceful and ungraceful stop evidence |
| Identity and supervision | 10 | privilege-transition table, effective unit and negative path tests |
| Resource engineering | 10 | workload envelope, cgroup counters, bounded failure interpretation |
| Storage and recovery | 12 | atomic publication reasoning, disk-failure response, empty-destination restore |
| Networking and transport | 10 | listener/route/TCP evidence and timeout ownership |
| DNS, TLS, and HTTP authority | 12 | verified name path, wrong-name rejection, chain/rotation reasoning |
| Firewall, proxy, and load balancing | 8 | packet/intermediary policy, forwarded identity, retry and drain analysis |
| VM and cloud systems | 10 | replacement dossier, provider mapping, weakest failure-domain argument |
| Final game day and runbooks | 10 | hypothesis, first oracle, repair, regression, cleanup, residual risk |
| Course 2 handoff | 8 | manifested, testable provider-neutral requirements and acceptance evidence |

## Performance levels

**Excellent:** The learner explains causal ownership, preserves first-failure evidence, distinguishes evidence classes, and chooses a repair that preserves earlier boundaries.

**Competent:** The mechanism and evidence are correct, but trade-offs or residual risks require prompting.

**Insufficient:** The response relies on command output without interpretation, tool defaults without ownership, or a stronger claim than the environment established.

## Non-compensable gates

The learner does not pass if any of these remain unresolved:

1. TLS verification is disabled as a final solution.
2. a public or management listener is exposed without explicit policy;
3. a service runs with unexplained root or broad capability authority;
4. durable state or backup restoration is unverified;
5. a lab leaves processes, mounts, firewall rules, credentials, or cloud resources behind;
6. an availability claim ignores a critical single failure domain;
7. the Course 2 handoff lacks acceptance evidence or contains unmanifested changes;
8. dependency-light core proof does not pass from a clean extraction.
