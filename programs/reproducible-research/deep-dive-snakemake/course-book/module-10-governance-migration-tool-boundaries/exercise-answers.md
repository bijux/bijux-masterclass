# Exercise Answers

These answers are model explanations, not the only acceptable wording.

What matters is whether the reasoning protects trust while change is being planned.

## How to use these answers

Read this file only after attempting the exercises yourself.

Use the answer key for three checks:

1. did you name the right boundary
2. did you preserve the right proof route
3. did you explain trust preservation instead of only architectural taste

Different wording can still be strong if the reasoning stays specific, evidence-first,
and stewardship-focused.

The strongest self-study packets also leave behind six concrete artifacts:

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
- invisible complexity, because discovery logic lives in helper code reviewers cannot
  explain quickly

Which risk to address first:

- contract drift

Why:

- hidden downstream dependence on internal results makes every later migration more risky

Evidence route to inspect first:

- the file API and publish verification route, such as `make verify-report`

The main lesson is to review the current trust boundary before touching implementation.

Weak answers start by describing the desired future state and never make current truth
explicit enough to defend or preserve.

## Exercise 2: Sequence a migration

A safer order would be:

1. change report generation ownership first, while keeping the same published outputs
2. compare proof routes and outputs to make sure the migration is behavior-preserving
3. review and then change sample discovery with explicit dry-run comparison
4. leave platform submission until the workflow contract and proof route are stable

What proof must survive:

- publish verification
- dry-run meaning
- any comparison route between old and new output surfaces

Which change should wait:

- platform migration

Why:

- it changes the ownership boundary most broadly and should not be mixed with unresolved
  workflow-truth changes

Weak sequences try to modernize everything at once and then lose the comparison route that
would have made the migration trustworthy.

The missing but important sentence is usually this one:

> If I move all three boundaries together, I lose the ability to tell which change broke
> trust or which proof route stopped holding.

## Exercise 3: Write governance rules

A strong set of rules could be:

1. every new published file must update the file API and verification route
2. profiles may change operating policy but not workflow meaning
3. helper boundaries must stay reviewable, with ownership and proof surfaces kept visible

Why these work:

- they are short enough to enforce
- they each protect a recurring source of drift

Weak rules read like essays, mention five boundaries at once, and cannot be mapped to one
clear review decision.

The strongest answers also say why the rules are short enough to survive real review:
each one protects one recurring failure pattern and can be checked in a bounded way.

## Exercise 4: Name the anti-pattern

Anti-pattern families:

- removing benchmark files: evidence suppression
- adding a new published TSV without verification updates: contract drift
- moving analytical thresholds into `profiles/slurm/config.yaml`: policy leaks

Most dangerous change:

- moving analytical thresholds into the profile

Why:

- it quietly changes workflow meaning through an operating surface, which makes context
  comparison and future review much less trustworthy

Recovery step to require first:

- move the semantic setting back into visible workflow or config boundaries, then audit the
  profile again

Weak answers call every problem "technical debt" and therefore hide which proof route must
be restored first.

## Exercise 5: Decide the tool boundary

A strong recommendation would say:

- Snakemake should keep owning reproducible workflow orchestration and trusted publish bundles
- another system should own user-triggered requests, access control, and tenancy-aware scheduling
- the split should be made reviewable through explicit submission metadata, profile review,
  and published output verification

Why this is strong:

- it keeps file-based workflow truth where it is already visible
- it hands platform-native concerns to the system built to own them
- it names the handoff evidence rather than only naming the destination tool

Weak answers blur responsibility until nobody can say where workflow truth ends and
platform behavior begins.

## Exercise 6: Build a current-truth inventory

A strong inventory separates declared contract from observed dependence. It links each
target to owners, consumers, semantic config, execution policy, software, and proof.
Undocumented reads from `results/` and semantic profile keys rank above cosmetic
structure. Preserve current public schema, representative semantics, and consumer routes
before changing implementation, even when the current shape is inconvenient.

What a strong answer makes visible:

- what is already trusted
- what is only convenient internally
- what mismatch creates the largest migration risk

Example inventory headings:

- declared targets and normal completion surface
- actual downstream consumers and their paths
- semantic configuration versus profile policy
- software and runtime boundaries
- publish contracts and file-API coverage
- existing proof routes and missing proof routes

Why this is strong:

- it gives migration work a factual starting point
- it shows where documentation already disagrees with behavior
- it orders the risks by trust damage instead of annoyance

The key explanatory sentence is:

> The inventory is not a redesign wishlist; it is the evidence map that stops migration
> from erasing behavior consumers already rely on.

## Exercise 7: Write characterization checks

Characterization checks encode relied-upon behavior without declaring every incidental
byte permanent. Assert expected target membership, required schema, identifiers, units,
ordering only when contractual, and representative calculations. A candidate that drops
a required field fails. Temporary paths, log wording, and internal rule names remain free
to change unless they are documented public promises.

The main lesson is that characterization protects relied-upon behavior without freezing
every accidental implementation detail.

Weak answers either freeze every byte blindly or say "we should stay flexible" without
protecting the behavior consumers actually depend on.

## Exercise 8: Migrate one ownership boundary

Move only one owner at a time and run both implementations against fixed fixtures.
Byte equality is suitable for strictly deterministic contract files; schema plus semantic
comparison is better when timestamps or harmless ordering differ. Keep current proof
green, add focused evidence for the new owner, and revert if public meaning, failure
visibility, or rebuild behavior cannot be explained.

A strong answer also states when the old path can be retired and when rollback is still
the honest option.

Example answer shape:

- old owner:
  - report assembly hidden in one helper script with weak review visibility
- candidate owner:
  - explicit report boundary near the publish contract
- comparison:
  - schema and representative semantic comparison for the public report, byte comparison
    only where determinism is contractual
- rollback:
  - revert if public meaning, failure visibility, or consumer expectations no longer match

Why this is strong:

- it moves one concern at a time
- it chooses comparison strength by contract, not habit
- it preserves a real escape route

## Exercise 9: Enforce a governance rule

The automated check should express one durable boundary and report the exact violating
file or key. For example, compare publish outputs with file-API entries and fail when one
is absent. A failing fixture proves enforcement. The message should direct maintainers to
document, verify, version, or remove the public artifact rather than merely saying policy
failed.

The main lesson is that governance becomes durable only when it becomes reviewable and
repairable.

Weak checks fail loudly but teach nothing. Strong checks tell the maintainer which
boundary was crossed and what repair would restore trust.

The strongest answers also say explicitly why the rule belongs in governance:

> This is not only a reviewer preference; it is a durable repository promise that the team
> keeps violating unless the boundary is taught and enforced automatically.

## Exercise 10: Design and review a tool handoff

The external service authenticates and authorizes requests, creates an idempotent run
identity, submits bounded workflow inputs, exposes status and cancellation, and never
redefines scientific targets. Snakemake owns declared file execution and the verifiable
publish bundle. The handoff records request identity, workflow revision, semantic config,
operating context, and result manifest so failures and retries cannot create ambiguous
ownership.

The main lesson is that a tool handoff is only trustworthy when responsibility and
verification remain separable instead of being absorbed into one vague platform story.

Example handoff properties:

- request schema carries semantic config, workflow revision, and requester identity
- status schema distinguishes queued, running, failed, cancelled, and published states
- result schema returns the publish manifest, provenance, and verification route
- cancellation policy states whether cancellation is best-effort, immediate, or only
  future-facing

Why this is strong:

- it turns ownership into inspectable contracts
- it keeps the publish bundle verifiable without requiring trust in the service itself

Weak answer pattern:

- "the platform will handle it, so the workflow does not need to explain as much anymore"

That sentence gives up exactly the independent verification boundary the module is trying
to protect. If your answers still sound like that, keep revising.

## Self-check

If your answers consistently explain:

- what the current repository is already promising
- what proof must survive the next change
- which governance rule blocks recurring drift
- what ownership line makes the system easier to trust

then you are using Module 10 correctly.
