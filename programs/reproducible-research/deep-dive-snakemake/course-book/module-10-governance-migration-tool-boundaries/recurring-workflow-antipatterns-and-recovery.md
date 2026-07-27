# Recurring Workflow Antipatterns and Recovery

One sign that a workflow team is maturing is that it stops treating every painful problem
as a one-off exception.

Many of the same failures return again and again. Module 10 calls those what they are:
recurring anti-patterns.

## How to use this page

Read this page when you feel tempted to describe a recurring workflow problem as bad luck
or as a one-time awkward pull request.

Work through it in this order:

1. name the anti-pattern family
2. describe the current repository symptom
3. identify the technical repair
4. identify the review habit that must change to stop recurrence

This is how one repair becomes stewardship instead of temporary relief.

## Why anti-pattern language matters

If a repository problem is described only as a local annoyance, it is easy to "fix" the
symptom and keep the underlying habit.

Anti-pattern language helps you say:

- this kind of shortcut keeps producing the same trust problem
- this is bigger than one file or one pull request
- recovery means changing the review habit, not only the implementation detail

That is a governance skill, not only a debugging skill.

## Start by naming the habit, not only the latest breakage

Beginners often focus on the newest symptom:

- a rerun happened unexpectedly
- a profile behaved differently
- a published file drifted
- a helper became hard to review

Those symptoms matter, but Module 10 wants the deeper diagnosis: what recurring habit made
this kind of failure likely in the first place?

## Five anti-pattern families worth stopping early

| Anti-pattern | What it usually looks like | Why it keeps hurting |
| --- | --- | --- |
| hidden inputs | helper code or shell state influences outputs without declared inputs | reruns, trust, and migration reasoning become unreliable |
| policy leaks | profiles or deployment-specific settings alter workflow meaning | context changes become semantic changes in disguise |
| contract drift | downstream users depend on internal results or unstable published paths | migration and compatibility review become guesswork |
| invisible complexity | helper packages or wrappers own more logic than the visible workflow suggests | review moves from repository evidence to insider knowledge |
| evidence suppression | logs, benchmarks, or verification routes disappear when the team feels pressure | the workflow gets quieter and less trustworthy at the same time |

These are worth memorizing because they recur across repositories.

## Hidden inputs

This anti-pattern appears when real dependencies live outside declared rule inputs:

- helper scripts read undeclared config files
- wrappers inspect environment variables nobody documented
- shell commands depend on working-directory state or side files

The immediate damage is rerun confusion.

The bigger damage is migration confusion, because nobody can confidently say what behavior
must be preserved.

Recovery:

- declare the input if it is real
- move the hidden state into visible config or file contracts
- add a proof route that exposes the dependency in review

## Policy leaks

This happens when profiles or operating context begin to own semantics:

- one profile filters samples differently
- one environment changes published path meaning
- one scheduler-specific setting quietly changes analytical behavior

The repository may still run, but its meaning now depends on context in a way reviewers
cannot safely ignore.

Recovery:

- move semantic choices back into workflow or config boundaries
- keep profiles focused on execution policy
- use profile-audit surfaces to compare contexts honestly

## Contract drift

This anti-pattern appears when the public contract is not enforced strongly enough:

- notebooks read `results/` instead of `publish/v1/`
- reports are scraped because structured publish artifacts are unclear
- files get added to published outputs without documentation or verification updates

Recovery:

- strengthen the file API
- repair verification and manifests
- move consumers back onto the public contract

This is often a slower kind of breakage, which makes it easy to ignore until migration
time.

## Invisible complexity

Repositories sometimes stay tidy on the surface by pushing meaning into places reviewers do
not naturally inspect:

- a helper package owns discovery logic nobody can see from the rule files
- wrappers become mini-frameworks
- checkpoints and helper layers hide rather than explain workflow shape

Recovery:

- surface the ownership boundary
- document or expose the critical artifacts the helper creates
- simplify the visible route from `Snakefile` to public outputs

Invisible complexity is dangerous because the repository can still look clean.

## Evidence suppression

This is the anti-pattern many teams call "cleanup":

- benchmark files are removed because they look noisy
- verify routes are skipped because the migration is in progress
- logs are shortened until they stop answering real questions
- the team stops generating comparison artifacts because they feel temporary

Recovery:

- restore the smallest honest evidence route
- decide which review question each artifact answers
- remove noise only after a stronger replacement exists

Quieter is not the same thing as clearer.

## A small example

Imagine a repository where:

- downstream users read `results/`
- one cluster profile changes sample filtering
- report generation moved into a package nobody reviews directly
- verification is run only before releases

That is not four unrelated nuisances.

It is one repository with contract drift, policy leaks, invisible complexity, and weak
evidence discipline.

The right response is not one patch. It is a recovery plan that tackles the anti-pattern
family by family.

## One concrete recovery scenario

Suppose a repository now has all of these at once:

- notebooks read `results/` directly
- one profile changes sample filtering
- helper code owns most of discovery logic
- verification only runs before releases

The wrong response is to call that "a few cleanup items."

The stronger response is to classify the pattern mix:

1. contract drift
2. policy leaks
3. invisible complexity
4. evidence suppression

Once the families are named, recovery can be sequenced more honestly:

- repair the public contract
- move semantic choices out of profiles
- expose discovery ownership
- restore proof routes that reviewers can run under pressure

## Recovery should change the habit, not only the file

For each anti-pattern, ask two questions:

1. what technical repair is needed now
2. what review rule will stop this from quietly coming back

That second question is what turns a fix into stewardship.

## The beginner mistake to catch early

The most common beginner mistake is solving the last incident in a way that leaves the
habit untouched.

For example:

- declaring one missing input but leaving the hidden-input pattern alive elsewhere
- fixing one profile leak while keeping semantic keys socially acceptable in profiles
- restoring one benchmark file while still treating evidence as optional clutter

A strong recovery asks, "what rule or review habit will stop this from happening again?"

## Keep this standard

When a workflow problem repeats, stop describing it as bad luck.

Name the anti-pattern.

Once you can name the pattern, you can repair both the repository and the review habit
that allowed it to persist.
