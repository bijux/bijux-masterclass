# The Analysis Runs Platform

## Domain workflow

The same user journey anchors all ten courses:

```text
create a project
→ register or upload a dataset
→ submit an analysis run
→ observe queued, running, completed, failed, or cancelled state
→ retrieve a verified artifact
→ notify downstream consumers
```

The domain is intentionally small enough to understand and rich enough to expose real engineering pressure: asynchronous work, retries, ownership, file transfer, authorization, pagination, streaming, webhooks, events, RPC, service boundaries, graph composition, and platform publication.

## Core facts and owners

- **Analysis Control** owns projects, datasets, analysis-run state, legal transitions, attempts, idempotency, and completion authority.
- **Artifact Delivery** owns artifact content and transfer once extracted in Course 8; earlier courses keep it as a module inside the service.
- **Notification Delivery** owns webhook subscriptions and delivery attempts once extracted.
- **Worker Plane** performs computation but never owns the truth of a run.
- **Graph Gateway** composes capabilities but owns no business fact.
- **API Platform** owns discovery, publication, evidence workflows, and support routing—not domain authorization.

## Why one domain is pedagogically stronger

A new project in every course would hide whether earlier guarantees survive. The continuous platform forces accumulation. For example, a completed analysis is simultaneously:

- an HTTP resource state;
- a committed database fact;
- an authorized tenant-owned object;
- a reliability journey outcome;
- a performance workload completion;
- an integration event source;
- an RPC-visible result;
- one step in a distributed workflow;
- a GraphQL field source;
- a governed API product behavior.

A repair at one layer is invalid if it breaks another. This is the program’s central discipline.
