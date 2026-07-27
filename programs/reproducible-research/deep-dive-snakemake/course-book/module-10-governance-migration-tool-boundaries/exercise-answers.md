# Exercise Answers

These answers are model explanations, not the only acceptable wording.

What matters is whether the reasoning protects trust while change is being planned.

## How to use these answers

Read this file only after attempting the exercises yourself.

Use the answer key for four checks:

1. did you name the right boundary
2. did you preserve the right proof route
3. did you explain trust preservation instead of only architectural taste
4. did you leave behind artifacts another maintainer could review without oral context

Different wording can still be strong if the reasoning stays specific, evidence-first,
and stewardship-focused.

The strongest self-study packets leave behind six concrete artifacts:

- one current-truth note
- one migration sequence
- one short governance ruleset
- one characterization packet
- one governance check with a failing fixture
- one tool-handoff ownership note

If your answers rely only on the attractiveness of the proposed future state, the
stewardship reasoning is still too thin.

## Exercise 1: Review the current repository honestly

Strong top risks:

- contract drift, because downstream notebooks still read `results/`
- policy leakage, because one profile changes sample filtering
- invisible complexity, because report or discovery logic lives in helper code reviewers
  cannot explain quickly

Which risk to address first:

- contract drift

Why:

- hidden downstream dependence on internal results makes every later migration more risky

Evidence route to inspect first:

- the file API and publish verification route, such as `make verify-report`

One awkward behavior to describe honestly:

- downstream consumers rely on an internal `results/` path that was never declared as a
  public contract

Why the first review note is not yet a migration plan:

- it names what is already trusted and where the repository is lying, but it does not yet
  decide what should move first or what proof must survive the move

The main lesson is to review the current trust boundary before touching implementation.

Weak answers start by describing the desired future state and never make current truth
explicit enough to defend or preserve.

## Exercise 2: Sequence a migration

A safer order would be:

1. repair publish contract drift while keeping the same published outputs
2. compare proof routes and consumer expectations to make sure the repair is
   behavior-preserving
3. move semantic settings out of profiles and verify that context comparison still tells
   the truth
4. move report implementation ownership only after those truth repairs stay stable
5. leave platform submission or service handoff until the workflow contract and proof
   route are stable

Which boundary moves first:

- the publish contract boundary

What proof must survive:

- publish verification
- consumer comparison against the publish bundle
- dry-run and profile comparison once semantic settings move
- any before-and-after comparison route between old and new owners

Which change should wait:

- platform migration

Why:

- it changes the ownership boundary most broadly and should not be mixed with unresolved
  workflow-truth changes

Why doing all three together would damage the comparison route:

- if contract repair, policy repair, and service handoff happen in one motion, the team
  can no longer tell which boundary broke trust or which proof route stopped holding

Weak sequences try to modernize everything at once and then lose the comparison route
that would have made the migration trustworthy.

## Exercise 3: Write governance rules the team can keep using

A strong set of rules could be:

1. every new published file must update the file API and verification route
2. profiles may change operating policy but not workflow meaning
3. migrations must preserve a reviewable comparison route until the new boundary earns trust

Repository surfaces protected:

- publish contract and file API
- profile boundary
- migration and ownership boundary

Example changes each rule would reject:

- adding `publish/v1/summary.tsv` without file-API coverage
- moving a sample-selection threshold into `profiles/slurm/config.yaml`
- deleting the old verification path before the new owner has a trustworthy comparison
  route

Why the wording is short enough to survive real review:

- each rule protects one recurring failure pattern and can be checked in a bounded way

How a maintainer would know the rule was violated:

- a missing file-API entry, a semantic key inside a profile, or a migration plan without a
  surviving proof route is visible in one review surface instead of hidden inside a policy essay

Weak rules read like essays, mention five boundaries at once, and cannot be mapped to one
clear review decision.

## Exercise 4: Name the anti-pattern family

Anti-pattern families:

- removing benchmark files: evidence suppression
- adding a new published TSV without verification updates: contract drift
- moving analytical thresholds into `profiles/slurm/config.yaml`: policy leakage

Most dangerous change:

- moving analytical thresholds into the profile

Why:

- it quietly changes workflow meaning through an operating surface, which makes context
  comparison and future review much less trustworthy

Recovery step to require first:

- move the semantic setting back into visible workflow or config boundaries, then audit the
  profile again

Proof route to consult first:

- profile audit plus dry-run comparison across contexts

Why calling everything "technical debt" is too weak:

- it hides which trust boundary was damaged and therefore hides which proof route must be
  restored before any approval is honest

Weak answers flatten distinct failures into one generic complaint and therefore lose the
right repair order.

## Exercise 5: Decide the tool boundary

A strong recommendation would say:

- Snakemake should keep owning sample discovery, declared targets, reproducible file
  execution, and the trusted publish bundle
- another system should own user-triggered requests, access control, tenancy-aware
  scheduling, and service-facing status behavior
- the split should be made reviewable through explicit request metadata, ownership notes,
  and published output verification

Handoff artifact or schema:

- one request schema carrying requester identity, workflow revision, semantic config,
  requested targets, and idempotency key

One ownership line to refuse to blur:

- the external service must not silently redefine scientific targets or publish semantics

How workflow truth stays independently verifiable after the handoff:

- the publish bundle, manifest, and verification route can still be checked from the
  repository artifacts even if the service UI is unavailable

Why this is strong:

- it keeps file-based workflow truth where it is already visible
- it hands platform-native concerns to the system built to own them
- it names the handoff evidence rather than only naming the destination tool

Weak answers blur responsibility until nobody can say where workflow truth ends and
platform behavior begins.

## Exercise 6: Build a current-truth inventory

A strong inventory separates declared contract from observed dependence. It links each
target to owners, consumers, semantic config, execution policy, software boundaries, and
proof routes.

Typical headings:

- declared targets and normal completion surface
- actual downstream consumers and their paths
- semantic configuration versus profile policy
- software and runtime boundaries
- publish contracts and file-API coverage
- existing proof routes and missing proof routes

High-risk mismatches:

- notebooks consume `results/` while docs imply they consume `publish/`
- semantic thresholds appear inside profiles instead of visible config
- a published file exists with no file-API entry or verification coverage

Facts to preserve before migration:

- public publish schema
- representative semantics of trusted outputs
- current consumer routes until a versioned replacement exists
- one proof route that can compare old and new ownership honestly

Why the inventory is evidence rather than busywork:

- it is the map that stops migration from erasing relied-on behavior by accident

What a strong answer makes visible:

- what is already trusted
- what is only convenient internally
- what mismatch creates the largest migration risk

If the inventory reads like a redesign wishlist, it is already too late in the process.

## Exercise 7: Write characterization checks

Characterization checks should encode relied-on behavior without declaring every
incidental byte permanent.

Strong checks would assert:

- expected target membership
- required schema fields and identifiers
- units and representative semantics
- ordering only when ordering is part of the documented contract

A good failing candidate:

- one candidate output drops a required field or changes the meaning of a published value

What the checks intentionally do not freeze:

- temporary paths
- log wording
- internal rule names
- harmless ordering differences when ordering is not contractual

Why byte-for-byte comparison may be too strong or too weak:

- it is too strong when timestamps or harmless formatting change, and too weak when a file
  can stay byte-stable while public meaning drifts somewhere else that consumers rely on

The main lesson is that characterization protects relied-on behavior without freezing
every accidental implementation detail.

Weak answers either freeze every byte blindly or say "we should stay flexible" without
protecting the behavior consumers actually depend on.

## Exercise 8: Migrate one ownership boundary

Move only one owner at a time and run both implementations against fixed fixtures.

Example answer shape:

- old owner:
  - report assembly hidden in one helper script with weak review visibility
- candidate owner:
  - explicit report boundary near the publish contract
- comparison:
  - schema and representative semantic comparison for the public report, byte comparison
    only where determinism is contractual
- proof before and after:
  - current publish verification plus one focused comparison packet
- rollback:
  - revert if public meaning, failure visibility, or consumer expectations no longer match

Why unchanged public meaning matters more than nicer internal structure:

- the migration is only honest if trust survives the move; cleaner internals do not justify
  surprising consumers or deleting the proof route

Why this is strong:

- it moves one concern at a time
- it chooses comparison strength by contract, not habit
- it preserves a real escape route

Weak answers celebrate new structure before they say what would trigger rollback.

## Exercise 9: Enforce one governance rule

The automated check should express one durable boundary and report the exact violating
file, key, or contract.

Strong example:

- policy statement:
  - every published file must have file-API coverage and a verification route
- focused implementation:
  - compare publish outputs against file-API declarations and fail when one is absent
- passing and failing fixtures:
  - one fixture with matching publish entries and one with an undocumented public file
- failure message:
  - tell the maintainer to document, verify, version, or remove the public artifact

Why this belongs in governance rather than only in review culture:

- the team keeps violating a durable repository promise, so the boundary must be taught
  and enforced automatically instead of depending on reviewer memory

The main lesson is that governance becomes durable only when it becomes reviewable and
repairable.

Weak checks fail loudly but teach nothing. Strong checks tell the maintainer which
boundary was crossed and what repair would restore trust.

## Exercise 10: Design and review a tool handoff

The external service should:

- authenticate and authorize requests
- create an idempotent run identity
- submit bounded workflow inputs
- expose status and cancellation
- return results without redefining scientific targets

Snakemake should keep owning:

- declared file execution
- trusted publish artifacts
- workflow-level provenance
- the verification route for the publish bundle

Strong request, status, and result properties:

- request schema carries semantic config, workflow revision, requester identity, requested
  targets, and idempotency key
- status schema distinguishes queued, running, failed, cancelled, and published states
- result schema returns the publish manifest, provenance, and verification route
- cancellation policy states whether cancellation is best-effort, immediate, or only
  future-facing

Ownership and failure table should make visible:

- who owns request validation
- who owns execution truth
- who owns cancellation semantics
- who owns result publication
- which failures belong to the service versus the workflow

Provenance strategy:

- every run records workflow revision, semantic config, operating context, request
  identity, and result manifest so retries and failures cannot create ambiguous ownership

End-to-end proof:

- the returned publish bundle can still be verified from repository artifacts even if the
  external service disappears or its UI becomes unavailable

What would make the handoff dishonest:

- a design where the bundle is only trustworthy through the service and not on its own

Why this is strong:

- it turns ownership into inspectable contracts
- it keeps the publish bundle verifiable without requiring trust in the service itself

Weak answer pattern:

- "the platform will handle it, so the workflow does not need to explain as much anymore"

That sentence gives up exactly the independent verification boundary the module is trying
to protect.

## Self-check

If your answers consistently explain:

- what the current repository is already promising
- what proof must survive the next change
- which governance rule blocks recurring drift
- what ownership line makes the system easier to trust
- which artifacts let another maintainer review your reasoning independently

then you are using Module 10 correctly.
