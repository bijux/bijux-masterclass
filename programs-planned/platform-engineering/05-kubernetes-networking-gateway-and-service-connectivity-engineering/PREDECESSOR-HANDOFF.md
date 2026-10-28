# Course 4 predecessor handoff

Course 5 consumes the exact handoff emitted by Course 4 at:

```text
capstone/predecessor/handoff/
```

The handoff fixes the workload facts that networking is not allowed to redefine:

- API and worker workload identities;
- namespaces, labels, selectors, and named ports;
- readiness and endpoint-eligibility expectations;
- workload security context and immutable image identity;
- DNS, NetworkPolicy, Gateway, and topology requirements;
- known risks and the inherited version ledger.

`make predecessor-proof` verifies every handed-off byte against the predecessor manifest before the course proceeds.

Course 5 may implement connectivity around these workloads. It may not silently change labels to make a Service select, broaden a security context to make a probe work, replace an immutable image subject, redefine readiness, or claim a topology guarantee that Course 4 did not establish. Any such change is a cross-course contract revision and must be reviewed as one.
