# Mid-Course Map

Use this page when Modules 01 to 03 feel stable and you need a deliberate bridge into
scaling, software boundaries, publish trust, and operating-context review. The middle of
the course is where many learners start confusing workflow meaning, repository
structure, and execution context. This map exists to keep those pressures separate.

## If you are learning this without the live class

Read this page in four passes:

1. identify the exact middle-course pressure you are under
2. choose one module cluster rather than browsing the whole middle stretch
3. keep one capstone cross-check beside the module instead of replacing it
4. stop when you can name the new boundary the cluster teaches

If you skip step 2, the middle of the course can start feeling like one large architecture shelf instead of a sequence of distinct design questions.

## The middle-course progression

```mermaid
flowchart LR
  m4["Module 04<br/>scaling boundaries"] --> m5["Module 05<br/>software seams"]
  m5 --> m6["Module 06<br/>publish trust"]
  m6 --> m7["Module 07<br/>workflow architecture"]
  m7 --> m8["Module 08<br/>operating contexts"]
```

## What changes in the middle of the course

Earlier modules ask, "What is this workflow claiming to do?"

Middle modules ask harder follow-up questions:

- Where should the next change belong?
- Which repository splits clarify ownership?
- Which outputs are public versus internal?
- Which differences across contexts are policy-only?

This is where the course stops being only about workflow behavior and starts being about
workflow design under growth.

## The packet you should keep for middle-course work

Keep one small packet beside you:

- one current pressure statement
- one module cluster you chose on purpose
- one capstone cross-check
- one boundary question the cluster should answer
- one note on what would count as widening too early

If the packet starts listing many modules at once, you have already made the route too broad.

## Use this map for these pressures

| If the pressure is... | Start with | Keep nearby | First capstone cross-check |
| --- | --- | --- | --- |
| where a structural workflow change belongs | Module 04 | [Boundary Review Prompts](../reference/boundary-review-prompts.md) | [Capstone File Guide](../capstone/capstone-file-guide.md) |
| where workflow orchestration ends and helper software begins | Module 05 | [Review Checklist](../reference/review-checklist.md) | [Capstone Architecture Guide](../capstone/capstone-architecture-guide.md) |
| what downstream users are actually allowed to trust | Modules 06 to 07 | [Proof Matrix](../guides/proof-matrix.md) | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |
| which differences across local, CI, and scheduler contexts are policy-only | Module 08 | [Topic Boundaries](../reference/topic-boundaries.md) | [Capstone Proof Guide](../capstone/capstone-proof-guide.md) |

## Read this middle stretch as three clusters

### Modules 04 to 05: scaling and software seams

Use this cluster when the workflow already feels real, but the repository is starting to
split across files, helper code, validation surfaces, and software boundaries.

- Module 04 teaches scaling, interfaces, and ownership-preserving splits.
- Module 05 teaches the boundary between Snakemake logic and the software it drives.

Leave this cluster able to explain where a change belongs before you edit it.

### Modules 06 to 07: publish trust and architecture

Use this cluster when the workflow is becoming a downstream-facing system rather than a
local internal build script.

- Module 06 teaches versioned publish contracts and downstream trust.
- Module 07 teaches workflow architecture and stable file APIs.

Leave this cluster able to separate internal run state from public outputs.

### Module 08: operating contexts

Use this step when the main pressure is execution context rather than workflow meaning.

- Module 08 teaches how local, CI, and scheduler policy differ without semantic drift.

Leave this step able to explain what changed across contexts and why the workflow promise
did or did not change.

## A middle-course card you should be able to fill before widening the route

Use a table like this:

| Pressure | Boundary the next cluster should clarify | Smallest module cluster |
| --- | --- | --- |
| scaling | where the next split belongs | Modules 04 to 05 |
| downstream trust | what is public versus internal | Modules 06 to 07 |
| context drift | what is policy versus semantic meaning | Module 08 |

If you cannot fill the middle column, the route is still too broad to help.

## Questions this map should help you answer

If the course middle is going well, you should be able to form questions like these:

- Is this change about the workflow graph or about helper software?
- Is this value part of output meaning or only execution policy?
- Is this path internal working state or a surface someone else can trust?
- Would another repository file clarify ownership or merely hide it?

If you cannot yet phrase the problem that way, go back to the smaller module example
before widening into a larger repository surface.

## What goes wrong when learners treat the middle of the course as one big shelf

Use this card before you keep browsing:

| If you are about to... | The likely hidden problem is... | Smaller route |
| --- | --- | --- |
| read Modules 04 to 08 as one uninterrupted block | cluster boundaries are being ignored | pick one cluster by pressure |
| use capstone structure to understand ownership before the module is clear | corroboration is replacing learning | stay in the module example and one capstone cross-check |
| read architecture material before the workflow claim is legible | repository design is outrunning workflow truth | go back one cluster |
| treat context review as purely infrastructure | semantic versus policy boundaries are still fuzzy | stay with Module 08 plus one audit surface |

If the smaller route feels too narrow, that usually means it is protecting the actual learning sequence.

## Middle-course mistakes to avoid

- splitting files because the repository feels crowded rather than because ownership is
  clearer
- treating publish directories as a convenience pile instead of as a contract
- using profiles to hide analytical differences
- reading architecture material before the current workflow claim is legible
- treating context review as if it were only an infrastructure concern

## When to leave this route

Move to [Mastery Map](mastery-map.md) when the question changes from design and trust
surfaces to stewardship pressure:

- a workflow incident needs evidence before edits
- migration or governance is now the main concern
- the right answer may be handing a concern off rather than keeping it inside Snakemake

## A five-line middle-course note you should be able to write from memory

If this page has done its job, you should be able to write:

1. what middle-course pressure you are under
2. which module cluster matches it
3. what boundary that cluster should clarify
4. which capstone cross-check is small enough to keep nearby
5. why a broader route would be premature

If you cannot do that, the middle stretch is still too blurred.

## Best next move after this page

Open exactly one of these before resuming:

- [Module Checkpoints](../guides/module-checkpoints.md) if you need the exit bar
- [Pressure Routes](../guides/pressure-routes.md) if urgency is reshaping the reading
  order
- [Capstone Map](../capstone/capstone-map.md) if the module is clear but the repository
  route is not
