# Learning Contract

Use this page when your study habits are starting to blur. Deep Dive Snakemake is not a
course you finish by skimming every page. It is a course you finish by being able to
defend one workflow boundary, one failure mode, and one proof route at a time.

This page is the reset button for that discipline.

## The short contract

For each important idea, the course asks you to do three honest things:

1. predict before you run
2. observe what Snakemake planned or did
3. explain the result in workflow language, not in vague impressions

If you skip prediction, you never test your mental model. If you skip observation, you
fall back to guessing. If you skip explanation, commands become ritual.

## When to return to this page

Come back here when any of these start happening:

- you are opening more pages but understanding less
- you keep choosing proof routes that are larger than the claim
- you are browsing the capstone instead of learning from the module
- you can recognize terms but cannot defend them in your own words

Those are study problems, not content-volume problems.

## The three questions to ask before widening the surface

Before opening more material, ask:

1. Did I make a prediction?
2. Did I inspect the smallest surface that could falsify it?
3. Can I explain the result without copying the page’s wording?

If any answer is no, the right next step is usually smaller, not broader.

## What the course is asking from you

Before you call a module done, you should be able to:

1. explain the contract or boundary in plain language
2. name the failure that would appear if the contract were false
3. choose one command, artifact, or file that tests the claim
4. explain why a heavier proof route would be unnecessary right now

If you can only recognize the vocabulary, you are not done.

## What the material owes you

The course pages should present each important idea in a usable order:

1. the contract question
2. the failure mode that makes it matter
3. the design or repair rule
4. the proof route that can confirm the claim
5. the capstone route only after the local idea is clear

When a page skips from slogan to commands, it is forcing the learner to reconstruct the
lesson design alone.

## The honest module loop

Use this loop whenever a module starts feeling diffuse:

1. read the overview and identify the current boundary question
2. write one sentence that begins with `The contract here is...`
3. write one sentence that begins with `If this were false, I would expect...`
4. run the smallest proof route that could disprove your understanding
5. explain the result in plain language
6. move on only when the explanation sounds like yours, not like copied course prose

## What good progress looks like

A strong study session usually leaves you with:

- one workflow, dry-run, or review artifact you can explain without notes
- one mistake you can now name clearly
- one believable reason the current proof route was enough
- one small next step instead of a pile of open tabs

That is better progress than reading more pages without ownership of the idea.

## The proof surfaces you should keep reaching for

These proof surfaces recur because they answer different classes of question:

| Surface | Use it to answer |
| --- | --- |
| dry-run output | what Snakemake intends to do before execution |
| `--summary` | what outputs exist and how Snakemake currently sees them |
| `--list-changes` | why code, params, or inputs now justify reruns |
| `FILE_API.md` | what downstream users are allowed to trust |
| publish bundle contents | what the repository promotes as a stable contract |
| verification and test targets | whether the workflow can defend its claims after execution |

Good study means choosing the surface that fits the claim instead of jumping to the
largest available route.

## When the capstone is appropriate

Open the capstone when the local idea is already stable and you want to see it survive a
real repository shape.

Do not open the capstone yet when:

- you still need the first explanation of the concept
- you cannot name the failure the module is trying to prevent
- you do not know which command or artifact would count as proof
- the repository still feels larger than the lesson itself

Use [Capstone Map](../capstone/capstone-map.md) when the concept is clear but the route
through the repository is not.

## Signs you are fooling yourself

Pause and reset if:

- you keep widening the reading surface because one page did not click
- you can quote the term but cannot give a concrete failure example
- you chose the strongest proof route because it felt safer than reasoning
- you can follow the capstone mechanically but cannot say which boundary owns the
  behavior

Those usually mean you need one smaller question, not one bigger resource.

## The beginner mistake to catch early

The most common beginner mistake is believing that confusion can be solved by widening
the surface:

- more support pages
- stronger proof routes
- earlier capstone entry
- later modules that sound more advanced

Most of the time the durable fix is the opposite: shrink the question until one boundary,
one failure mode, and one proof route become defensible.
