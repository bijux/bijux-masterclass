# Checkpoint — Module 02: Operations, Parameters, and Messages

## Required result

Complete project and dataset messages, including pagination inputs, creation responses, and problem representations.

## Demonstrate

- Model path, query, header, cookie, and body input deliberately.
- Use request bodies and media types correctly.
- Describe response codes, headers, and representations as a complete outcome.
- Choose stable operation identifiers.
- Validate examples against their schemas.

## Commands

```bash
make -C capstone parse
make -C capstone examples
make -C capstone bundle-check
make -C capstone python-test
make -C capstone typescript
make -C capstone python-live
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Operations, Parameters, and Messages** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Operations, Parameters, and Messages**
- focused result for: Model path, query, header, cookie, and body input deliberately.
- public, durable, security, or operational observation showing: Projects and datasets now have complete create, list, retrieve, update, and delete message contracts.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **Operations, Parameters, and Messages**
- a limitation statement naming every live dependency required to support the strongest **Operations, Parameters, and Messages** claim but not exercised

## Defend the design

1. Answer the central question: **How do we specify every input and output precisely enough that independent clients serialize the same exchange?**
2. Demonstrate this capstone result: Projects and datasets now have complete create, list, retrieve, update, and delete message contracts.
3. Show the **Operations, Parameters, and Messages** defect, the first failing oracle, and the exact regression retained after repair.
4. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Projects and datasets now have complete create, list, retrieve, update, and delete message contracts.—all focused checks pass, the **Operations, Parameters, and Messages** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
