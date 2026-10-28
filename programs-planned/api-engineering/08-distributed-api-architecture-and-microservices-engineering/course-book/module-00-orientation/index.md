# Orientation — freeze the predecessor and define the extraction laboratory

Course 8 begins by proving that Course 7’s handoff is unchanged. The handoff contains RPC contracts, migration history, ownership records, interaction decisions, release evidence, shared vectors, and the service-boundary dossier. Do not redesign from memory.

## Orientation outcome

By the end of orientation you can trace one run through every current contract and identify which decisions are still local. You have selected a primary language track, executed the dependency-light proof, and recorded which claims require a live database or deployment environment.

## Step 1 — verify the handoff

Run:

```bash
make predecessor-proof
```

The handoff manifest must verify exactly. A changed predecessor invalidates later comparison evidence.

Read:

```text
capstone/predecessor/handoff/service-boundary-dossier.yaml
capstone/predecessor/handoff/rpc-case/interaction-decisions.yaml
capstone/predecessor/handoff/rpc-case/service-ownership.yaml
capstone/predecessor/handoff/contracts/compatibility-policy.yaml
```

## Step 2 — trace the existing platform

Trace one successful analysis through:

```text
public HTTP request
→ local application command
→ database transaction
→ durable event publication
→ worker gRPC interaction
→ artifact publication
→ run completion
→ notification delivery
```

Mark:

- each authoritative writer;
- each transaction boundary;
- each stable effect identity;
- each synchronous deadline;
- each event or RPC contract;
- each security decision;
- each recovery mechanism.

The current platform is a modular service with external dependencies and worker processes. Do not call every process a microservice.

## Step 3 — distinguish five boundaries

Explain the difference between:

### Process boundary

Separate operating-system process. It may still belong to one service and one release.

### Deployment boundary

Can be rolled out separately. This does not prove data, change, or ownership independence.

### Service boundary

Owns a coherent capability, interfaces, operations, and—when applicable—authoritative data.

### Data-ownership boundary

Exactly one authority writes a fact and governs its migration, retention, and recovery.

### Team boundary

One accountable group can approve changes, operate the capability, and respond to incidents.

These boundaries sometimes align. Assuming they always align creates distributed monoliths.

## Step 4 — choose a primary track

```bash
make python-proof
make typescript-proof
```

Select one track for implementation work. Record the other as comparative evidence.

## Step 5 — run the baseline

```bash
make boundary-proof
make capstone-tour
make core-proof
```

The tour should complete a run, store one artifact effect, complete the saga, create one notification effect, and report clean reconciliation.

## Readiness diagnostic

You are ready for Module 1 when you can answer:

1. Why does a remote method not automatically imply a service?
2. Which current facts must remain in one Analysis Control transaction?
3. Why can Notification fail without changing run completion truth?
4. What makes Artifact a plausible but conditional extraction?
5. Why is Worker Plane a separate deployment but not a data owner?
6. Which Course 7 proof would be invalidated by a shared database?
7. Which parts of the baseline are environment-backed rather than dependency-light?

Record any weak answer before continuing.
