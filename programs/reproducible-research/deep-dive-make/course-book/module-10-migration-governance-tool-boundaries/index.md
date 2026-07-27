# Module 10: Migration, Governance, and Make Boundaries

Module 10 is where the course stops asking, "Can you make this build run?" and starts
asking, "Can you inherit it responsibly, change it safely, and explain when Make should
keep or lose ownership?"

That is a different skill.

A mature build steward needs to:

- review a Make system without collapsing into taste arguments
- separate broken truth from ordinary design debt
- move one boundary at a time without erasing the current proof routes
- write governance that future maintainers can actually enforce
- say plainly when Make is still the right owner and when another tool should take over

This module is about stewardship, not just repair.

## Why this module matters

By the time a Make build becomes long-lived, the hard problems are rarely syntax
problems. They are stewardship problems:

- CI depends on helpers that were never meant to be public
- one release route now builds, packages, uploads, and mutates remote state
- a migration is needed, but nobody knows what evidence must survive the move
- maintainers can feel the build is risky, yet cannot explain exactly why
- "replace Make" and "leave it alone" both sound simpler than honest review

This module exists so those conversations stop being emotional and start becoming
evidence-based.

## The running question

Carry this question through every page:

> What evidence would let me improve this build while keeping trust in its current and
> future behavior?

Strong Module 10 answers usually mention one or more of these:

- a review artifact that makes the present system legible
- a migration step that moves one boundary while keeping a comparison route alive
- a governance rule that protects a public contract or proof surface
- an antipattern described in terms of truth loss or ownership drift
- a tool-boundary decision defended by modeling fit rather than novelty

## What this module is really for

By the end of the module, you should be able to explain five things clearly:

- how to review an inherited Make build without defaulting to style complaints
- how to stage a migration so each move keeps proof alive
- what governance rules keep a build teachable and maintainable over time
- which recurring build smells deserve immediate intervention
- when Make is still the most honest owner and when it is not

Those are course-closing skills. They depend on everything earlier in the program:
graph truth, parallel safety, determinism, target contracts, release boundaries, and
operational evidence.

## How to treat this module

Treat Module 10 as one serious stewardship session, not as a loose epilogue.

You are not required to replace Make.

You are required to understand one real Make system well enough that keeping, repairing,
or handing off a concern becomes a defendable decision.

If you finish the module with only opinions about "cleanups" or "modernization," you
have missed the point.

## The live stewardship route

Use one inherited build review and one bounded handoff decision as the anchors for the
day:

```mermaid
flowchart LR
  review["Inventory targets, outputs, and writers"] --> characterize["Preserve current proof routes"]
  characterize --> classify["Classify risks and ownership boundaries"]
  classify --> move["Design one smallest responsible boundary move"]
  move --> govern["Write rules future maintainers can actually enforce"]
```

That route keeps change tied to trust instead of taste.

## Stewardship packet to build all day

Keep one packet as you work through the module. By the end it should contain:

- one first-pass build review
- one target/output ownership inventory
- one proof-preserving migration step
- one governance note with an enforcement path
- one tool-boundary decision record
- one bounded repair or migration sequence

If those artifacts are missing, you are probably talking about the build more than you
are stewarding it.

## Decide by responsibility, not by tool fashion

For each concern, compare the ownership it needs with the ownership Make can provide:

| Concern | Local file graph? | External state? | Long-running orchestration? | Likely owner |
| --- | ---: | ---: | ---: | --- |
| compile sources into objects | yes | no | no | Make |
| assemble and verify a local bundle | yes | no | no | Make |
| upload and retry against a remote service | partly | yes | possibly | workflow or publication tool |
| coordinate a distributed research pipeline | partly | yes | yes | workflow scheduler |

These are starting judgments, not universal answers. A handoff is justified when another
tool has a clearer responsibility model for the concern, not merely because it is newer.

Every proposed handoff should still have a visible contract:

```mermaid
flowchart LR
  make["Make-owned local artifact"] --> contract["versioned file and metadata contract"]
  contract --> external["external owner"]
  external --> receipt["status or receipt evidence"]
```

Without that contract, "migration" often means hidden coupling moved from one script to
another.

## Study route

Read the module in this order the first time:

1. [Reviewing Build Contracts and Current Truth](reviewing-build-contracts-and-current-truth.md)
2. [Migration Plans That Preserve Proof](migration-plans-that-preserve-proof.md)
3. [Governance Rules for Long-Lived Builds](governance-rules-for-long-lived-builds.md)
4. [Recurring Build Antipatterns and Recovery](recurring-build-antipatterns-and-recovery.md)
5. [Deciding When Make Should Stop Owning the Problem](deciding-when-make-should-stop-owning-the-problem.md)
6. [Worked Example: Planning a Safe Build Migration](worked-example-planning-a-safe-build-migration.md)
7. [Exercises](exercises.md)
8. [Exercise Answers](exercise-answers.md)
9. [Glossary](glossary.md)

That order matters because the worked example and practice surfaces are much more useful
once the review, migration, governance, smell, and tool-boundary vocabulary is already
stable.

## The file set in this module

| File | Why it exists |
| --- | --- |
| `index.md` | orient the stewardship day and define the packet you should leave with |
| `reviewing-build-contracts-and-current-truth.md` | teach first-pass review without style drift |
| `migration-plans-that-preserve-proof.md` | teach how to move one boundary while keeping evidence alive |
| `governance-rules-for-long-lived-builds.md` | turn taste into enforceable maintainer rules |
| `recurring-build-antipatterns-and-recovery.md` | help you recognize repeated forms of truth loss quickly |
| `deciding-when-make-should-stop-owning-the-problem.md` | teach honest tool-boundary decisions |
| `worked-example-planning-a-safe-build-migration.md` | show the whole module in one migration narrative |
| `exercises.md` | pressure-test your stewardship reasoning |
| `exercise-answers.md` | compare your reasoning against a reference shape |
| `glossary.md` | stabilize the vocabulary for review, migration, and boundary arguments |

## Commands to keep close

These commands form the review loop for Module 10:

```sh
make -n all
make --trace all
make -p > build/review.dump
make -j1 all
make -j8 all
```

The exact targets may change from repository to repository. The point is stable evidence:
dry-run meaning, trace meaning, database meaning, and serial-versus-parallel behavior.

## Learning outcomes

By the end of this module, you should be able to:

- write an evidence-based review of a legacy Make build
- stage a migration without discarding convergence, traceability, or comparison checks
- define governance rules for public targets, includes, macros, and proof surfaces
- recognize recurring build failures as patterns instead of one-off anecdotes
- explain where Make should keep ownership and where it should hand off responsibility

## Exit standard

Do not move on until all of these are true:

- you can review one real Make system without defaulting to style complaints
- you can describe a migration sequence that preserves proof after each step
- you can write governance rules another maintainer could actually apply
- you can name recurring anti-patterns and explain why they are costly
- you can defend one tool-boundary choice in terms of ownership and evidence
- you can complete the exercises and leave a durable stewardship packet another
  maintainer could repeat

When those feel ordinary, Module 10 has done its job.
