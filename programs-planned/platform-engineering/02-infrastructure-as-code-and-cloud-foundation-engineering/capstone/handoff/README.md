# Course 2 → Course 3 Handoff

This directory is the complete, bounded handoff to **Container, OCI, and
Software Supply Chain Engineering**. Course 3 may change how Atlas is packaged
and executed, but it must preserve the identities, network paths, durable data,
configuration/secret sources, health semantics, and release evidence declared
here.

The handoff is intentionally smaller than the Course 2 repository. A consumer
should not need backend credentials, raw state, or private recovery material to
understand the workload contract.
