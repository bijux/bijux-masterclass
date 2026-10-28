# Study plan

This is a ten-day intensive course. A day is complete when the checkpoint evidence exists, not when the chapter has been read.

| Day | Morning | Afternoon | Evening evidence |
|---:|---|---|---|
| 0 | verify Course 4 handoff and tools | map the inherited Atlas paths | orientation report and evidence boundary |
| 1 | address domains and packet paths | route and MTU investigation | transition ledger |
| 2 | CNI lifecycle and IPAM | crash, replay, and garbage-collection lab | attachment recovery report |
| 3 | Services and EndpointSlices | readiness and stale-programming lab | convergence timeline |
| 4 | DNS and resolver behavior | negative cache and TCP fallback lab | exact query/answer timeline |
| 5 | NetworkPolicy semantics | default-deny rollout | allow/deny truth table |
| 6 | locality, source identity, dual stack | hard-local failure and family tests | topology decision record |
| 7 | Gateway API roles and attachment | hostname, path, and reference lab | condition and ownership review |
| 8 | TLS and HTTP integrity | certificate and backend-boundary lab | trust-path evidence |
| 9 | egress and mesh boundaries | peer validation and retry amplification | egress decision record |
| 10 | troubleshooting and conformance | final layered game day | release dossier and Course 6 handoff |

## Daily rhythm

A useful rhythm is:

```text
08:30  retrieval review
09:00  chapter and diagrams
11:00  worked investigation
13:00  implementation reading
15:00  controlled laboratory
18:00  exercises
20:00  checkpoint and evidence commit
```

Do not compress two labs into one evening. Network failures are educational only when baseline, fault, observation, repair, and cleanup are kept distinct.

## Primary implementation lane

Use the Python semantic model and loopback network laboratory for every module. Read the Go CNI lifecycle implementation in Module 2. Use the kind+Cilium lane after the semantic checkpoint, not before it. Native tools provide implementation evidence; they should not replace the mechanism model.

## Review intervals

At the start of Days 4, 7, and 10, reconstruct earlier paths without notes:

- Day 4: direct Pod and Service paths;
- Day 7: DNS, policy, locality, and source identity;
- Day 10: public Gateway to backend plus egress return path.

A learner who cannot reconstruct the path should revisit the earlier checkpoint before adding another abstraction.
