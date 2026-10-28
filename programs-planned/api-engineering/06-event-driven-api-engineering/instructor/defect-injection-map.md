# Defect injection map

| Defect | Introduce | Decisive proof |
|---|---|---|
| EVT-01 | Rename a command as a past-tense event | taxonomy review |
| EVT-02 | Acknowledge before committing effect | crash/redelivery experiment |
| EVT-03 | Partition by event ID | same-run ordering vector |
| EVT-04 | Commit state without outbox | reconciliation query |
| EVT-05 | Deduplicate only by event ID | tenant/effect-version vector |
| EVT-06 | Add a required field in minor release | compatibility proof |
| EVT-07 | Enable replay side effects | replay policy proof |
| EVT-08 | Window by processing time | delayed-event experiment |
| EVT-09 | Grant wildcard producer authority | security proof |
| EVT-10 | Retry forever | dead-letter and lag proof |

Inject one defect at a time. Preserve the failing evidence before repair. Reset deterministic state between experiments.
