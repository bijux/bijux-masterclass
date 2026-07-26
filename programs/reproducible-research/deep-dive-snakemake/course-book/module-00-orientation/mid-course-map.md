# Mid-Course Map
Use this page when Modules 01 to 03 feel stable and you need a deliberate bridge into
scaling, software boundaries, publish trust, and operating-context review. The goal is to
keep the middle of the course shaped by workflow questions instead of by repository sprawl.

## Mid-course route

```mermaid
flowchart LR
  m4["Module 04<br/>scaling boundaries"] --> m5["Module 05<br/>software seams"]
  m5 --> m6["Module 06<br/>publish trust"]
  m6 --> m7["Module 07<br/>workflow architecture"]
  m7 --> m8["Module 08<br/>operating contexts"]
```

## Use this map for these pressures

| If the pressure is... | Start with | Keep nearby | Capstone cross-check |
| --- | --- | --- | --- |
| where a structural workflow change belongs | Module 04 | [Boundary Review Prompts](../reference/boundary-review-prompts.md) | [Capstone File Guide](../capstone/capstone-file-guide.md) |
| where workflow orchestration ends and helper software begins | Module 05 | [Review Checklist](../reference/review-checklist.md) | [Capstone Architecture Guide](../capstone/capstone-architecture-guide.md) |
| what downstream users are actually allowed to trust | Modules 06 to 07 | [Proof Matrix](../guides/proof-matrix.md) | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |
| which differences across local, CI, and scheduler contexts are policy-only | Module 08 | [Topic Boundaries](../reference/topic-boundaries.md) | [Capstone Proof Guide](../capstone/capstone-proof-guide.md) |

## Module clusters

### Modules 04 to 05: scaling and software seams

Use this cluster when the workflow already feels real, but the repository is starting to
split across files, helper code, and validation surfaces.

- Module 04 teaches scaling, interfaces, and reviewable repository structure.
- Module 05 teaches the boundary between Snakemake logic and the software it drives.

Leave this cluster able to explain where a change belongs before you edit it.

### Modules 06 to 07: publish trust and architecture

Use this cluster when the workflow is becoming a downstream-facing system.

- Module 06 teaches versioned publish contracts and downstream trust.
- Module 07 teaches workflow architecture and stable file APIs.

Leave this cluster able to separate internal run state from public outputs.

### Module 08: operating contexts

Use this step when the main pressure is execution context rather than workflow meaning.

- Module 08 teaches how local, CI, and scheduler policy differ without semantic drift.

Leave this step able to explain what changed across contexts and why the workflow promise
did or did not change.

## Questions this map should answer

When the course reaches its middle, the common failure is not lack of syntax. It is lack
of ownership clarity. Use this page to answer questions like:

- Is this change about the workflow graph or about helper software?
- Is this value part of output meaning or only execution policy?
- Is this path internal working state or a surface someone else can trust?
- Would another repository file clarify ownership or merely hide it?

If you cannot phrase the question in one of those forms yet, go back to the smaller
module example before opening more repository surfaces.

## When to leave this route

Move to [mastery-map.md](mastery-map.md) once the question becomes stewardship,
migration, or whether Snakemake should keep owning the concern at all.

## Good next move after this map

Open exactly one of these before resuming:

- [Module Checkpoints](../guides/module-checkpoints.md) if you need the exit bar
- [Pressure Routes](../guides/pressure-routes.md) if urgency is shaping the reading order
- [Capstone Map](../capstone/capstone-map.md) if the module is clear but the repository
  surface is not
