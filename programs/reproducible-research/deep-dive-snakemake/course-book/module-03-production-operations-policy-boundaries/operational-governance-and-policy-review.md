# Operational Governance and Policy Review

Production operation does not stay healthy because one maintainer is careful once.

It stays healthy when the repository makes policy changes reviewable later.

That is the governance question for Module 03:

> if a profile, proof route, or recovery policy changes next month, how will the next maintainer know whether the change was operational, semantic, or dangerous?

This page answers that question.

## How to read this page

Read this page with one review pressure in mind:

> if this operational diff appears six months from now, what exact order should a maintainer
> inspect it in?

That question keeps governance concrete. The page is not about abstract maturity. It is
about making the repository teach the next reviewer where to look first.

## Why this lesson belongs in Module 03

Production policy is not complete when the repository merely contains profiles and proof
commands. It becomes durable only when another maintainer can review changes without
rebuilding the whole mental model from scratch.

That is why this page belongs at the end of the day:

- the policy surfaces already exist
- failure behavior already has names
- proof routes already have purposes
- governance now ties them into a stable review discipline

## Governance starts with naming the boundary

Policy review becomes vague when teams cannot name what a policy surface is allowed to do.

Module 03 keeps the boundary small:

- profiles may change execution context
- failure policy may change recovery behavior
- staging policy may change operational placement
- proof routes may change how the repository demonstrates trust

None of those should silently change workflow meaning.

That is the sentence governance must keep alive.

## A quick self-check before you keep reading

Think about one recent operational change you have seen in any repository.

Could you answer all of these quickly?

- which boundary owned the change
- which question the review was supposed to settle
- which route or artifact should have proved the answer

If not, the problem was probably governance clarity, not reviewer effort.

## What a healthy policy change looks like

A healthy operational diff usually has three qualities:

- the owning boundary is obvious
- the review question is proportionate
- the evidence route is named

Example:

- boundary: `profiles/ci/config.yaml`
- question: does this change CI execution context without changing workflow meaning
- evidence route: compare dry-runs or run `make profile-audit`

That is a much stronger review habit than "looks harmless."

## What a weak policy change looks like

Weak operational diffs often have these warning signs:

- semantic settings move into a profile because it felt convenient
- recovery behavior changes without an explanation of the failure class
- proof commands are edited without clarifying what claim got stronger or weaker
- one maintainer starts using extra local flags that the repository never records

Those are governance problems because the next reviewer cannot reconstruct the intent.

## The repository should teach review order

Good governance is not only about what is stored. It is also about where a reviewer looks
first.

For Module 03, the healthy review order is usually:

1. profile files
2. workflow or config files only if the policy boundary seems to leak
3. proof-route targets such as `profile-audit`, `verify`, or `confirm`
4. resulting evidence bundles if the change claims to affect trust

That review order keeps operational diffs from turning into random repository archaeology.

## The beginner trap here

Learners often assume governance means writing more documentation somewhere else.

Module 03 is teaching a different habit:

- put the policy in named repository surfaces
- put the proof routes in named repository surfaces
- review those surfaces in a stable order

That is much stronger than hoping a future maintainer remembers the team's folklore.

## One durable governance habit

When a production change lands, the reviewer should be able to answer:

- what boundary owns this change
- what question should this diff settle
- what command or artifact confirms the answer

If one of those is missing, the change is harder to trust than it should be.

## What a good Module 03 explanation sounds like

Strong:

> This diff belongs to the CI profile boundary, so review starts there; the first proof
> question is whether execution context changed without changing workflow meaning.

Weak:

> It is only an ops tweak, so we can probably skim it.

## A useful governance table

| Change type | First review question | Good first proof route |
| --- | --- | --- |
| profile diff | does this alter context only, or workflow meaning too | dry-run comparison or `make profile-audit` |
| retry or incomplete-policy diff | which failure class is this now treating differently | rule logs plus one rerun or recovery demonstration |
| staging or latency diff | does this change placement only, or the trust boundary too | context comparison and one executed verification route |
| proof-target diff | what claim is stronger or weaker after this edit | run the changed proof route deliberately |
| local shell habit not in the repository | should this become an explicit policy surface | encode it in profile, Makefile, or docs before relying on it |

This is the kind of table that helps a real maintainer review calmly.

## Review a scheduler-policy change in four passes

Use the generated scheduler-policy bundle rather than reading every file at
once.

```mermaid
flowchart LR
    Q["1. state claim"] --> C["2. inspect contract"]
    C --> E["3. inspect evidence"]
    E --> D["4. record decision"]
    D -->|"unclear"| Q
```

### State the claim

Use a sentence narrow enough to disprove:

> The accepted profile preserves four threads, 8,000 MB, and 30 minutes while
> changing no semantic field.

“The Slurm profile works” is not reviewable here. The local audit never contacts
Slurm.

### Inspect the owned contract

Read `job-contract.json` before any generated output. Separate:

- required execution resources;
- workflow-semantic fields;
- output identity.

If the proposed change alters `minimum_score`, route it to semantic review. If
it alters how `mem_mb` becomes a scheduler flag, keep it in operational review.

### Inspect discriminating evidence

Read `summary.tsv`, then the relevant checks in `report.json`. A trustworthy
audit includes both:

- one accepted translation;
- rejected counterexamples that would expose missing memory, under-provisioning,
  and semantic leakage.

Happy-path output alone cannot show that the boundary is enforced.

### Record a decision with a limit

Use a decision record like:

```text
Decision: ACCEPT local resource translation
Evidence: SCHEDULER_MAPPING_RECORDED = PASS
Limit: no scheduler was contacted
Next proof: site integration with job ID and worker output verification
```

The limit is not a disclaimer to hide at the bottom. It tells the next operator
which proof remains missing.

## Assign evidence to owners

```mermaid
flowchart TD
    R["rule author"] --> A["declared threads, memory, runtime"]
    P["profile maintainer"] --> B["scheduler argument mapping"]
    O["site operator"] --> C["account, partition, mounts, execution"]
    V["result reviewer"] --> D["output meaning and verification"]
    A --> G["production acceptance"]
    B --> G
    C --> G
    D --> G
```

No single owner can prove the entire production story:

| Owner | Can approve | Cannot approve alone |
| --- | --- | --- |
| rule author | resource declaration and semantic contract | site queue behavior |
| profile maintainer | deterministic resource translation | output correctness |
| site operator | scheduler and storage integration | analytical threshold |
| result reviewer | content and publish contract | executor configuration |

This ownership split prevents “operations” from becoming a catch-all review
label.

## Use stop conditions during review

Stop approval when:

- a profile changes sample identity, threshold, or output meaning;
- the request asks for fewer resources than the rule declares;
- a required resource disappears during translation;
- the receipt does not reveal whether execution occurred;
- site-specific claims have no job ID or worker evidence;
- a retry policy has no eligible failure class or attempt bound.

Stopping is not the same as rejecting the entire design. It identifies the
smallest missing proof or misplaced responsibility.

## Rehearse governance failure

Run:

```console
gmake scheduler-policy-selftest
```

The tests remove each intended cause. For example, restoring memory to the
`missing-memory` profile must make the rejection finding fail. That behavior
shows that the audit is checking a causal boundary rather than merely finding a
file with “rejected” in its name.

## Why command folklore is a governance smell

If the real production story lives in Slack messages, wiki fragments, or one maintainer's
shell history, the repository is already harder to trust.

That is why Module 03 keeps returning to:

- versioned profiles
- named proof routes
- stable review bundles

These are governance tools because they move operational knowledge back into reviewable
repository surfaces.

## Common failure modes

| Failure mode | What it looks like | Better repair |
| --- | --- | --- |
| a profile accumulates semantic toggles over time | operational review quietly becomes semantic review | move meaning back into config or workflow code |
| proof routes multiply without distinct purposes | nobody knows which command proves what | document the proof ladder and keep route purposes narrow |
| local incident flags become permanent habits | production operation depends on memory | promote durable habits into profiles or Make targets |
| policy bundles are generated but never read with a question in mind | evidence exists without judgment | record the review question alongside the route |
| governance depends on one maintainer's intuition | continuity breaks during handoff | encode review order and ownership in repository surfaces |

## The explanation a reviewer trusts

Strong explanation:

> this diff changes CI execution policy only, so the first review surface is the CI profile;
> the policy boundary is checked with `make profile-audit`, and no semantic workflow files
> should need to change for the review to stay clean.

Weak explanation:

> this is just an ops tweak, so it probably does not matter much.

The strong version preserves review discipline. The weak version erodes it.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain why policy changes need named ownership boundaries
- describe one healthy review order for an operational diff
- identify one sign that command folklore is replacing repository governance
- explain how proof routes support handoff and long-term maintenance
