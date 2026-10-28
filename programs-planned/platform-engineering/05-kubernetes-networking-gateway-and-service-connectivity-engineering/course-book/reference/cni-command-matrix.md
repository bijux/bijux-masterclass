# CNI command matrix

| Command | Primary question | Required behavior | Important failure evidence |
|---|---|---|---|
| ADD | create or confirm attachment | idempotent replay; compatible result; rollback or inspectable partial state | allocation owner, namespace/link changes, chain stage |
| DEL | remove owned attachment | safe repeated call; tolerate absent namespace; do not delete newer generation | attachment generation, IPAM release, host link cleanup |
| CHECK | compare expectation and observation | report drift without destructive repair | missing interface, address, route, or chained state |
| STATUS | can plugin service new work? | dependency-aware readiness | configuration presence versus actual dependency health |
| GC | remove abandoned state | use runtime-provided valid attachment set; generation safe | removed IDs and retained current owners |

Command support and exact semantics depend on the negotiated CNI specification and plugin. Treat exit status, stderr, and result version as protocol evidence.
