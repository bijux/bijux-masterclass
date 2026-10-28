# Reference — Promotion evidence schema

A promotion record contains release ID, target environment, predecessor, candidate commit, image/chart/OCI digests, renderer versions, render digest, compatibility, policy, migration phase, recovery gates, target cluster profile, progressive plan, approvers, exceptions, timestamps, and evidence limitations.

The record is immutable. Corrections create a superseding record rather than editing history.

## Extended reader notes

A promotion record should be machine-readable and human-reviewable. Minimum fields are: release identifier; predecessor; source commit; image, chart, and source artifact digests; renderer and version; environment inputs; rendered-set digest; target fleet; data phase; rollback frontier; evidence gates; approvals; decision; and unresolved limitations.

Every gate names its subject. “Security passed” is insufficient when the scanned digest differs from the promoted digest. Every observation has a timestamp and evidence class. Time-sensitive results such as vulnerabilities, secret adoption, restore tests, and fleet capability may expire. `not-executed` is distinct from `pass` and cannot be hidden by a numerical score.

The schema is also an incident index. An operator should be able to locate the exact desired state, reconstruct the render, identify the controller version, and determine whether rollback remains safe without searching ephemeral CI logs.
