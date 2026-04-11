# Anti-Patterns and Review Interventions

Anti-patterns rarely announce themselves as bad ideas.

They usually begin as reasonable shortcuts:

- "just this one local file"
- "copy the latest model"
- "we can document the parameter later"
- "the remote probably has it"
- "the experiment result is obvious"

Module 10 asks you to stop those shortcuts early.

## Common DVC anti-patterns

| Anti-pattern | Why it spreads | Review intervention |
| --- | --- | --- |
| path as identity | filenames feel concrete | ask for content identity or DVC evidence |
| hidden parameter | quick local tuning | move meaningful controls into reviewed params |
| metadata-only merge | Git diff looks complete | require remote-backed verification |
| copy-latest promotion | easy release movement | require versioned bundle and manifest |
| experiment as branch substitute | convenient exploration | require intent, comparison, and disposition |
| cleanup by storage pressure | cost feels urgent | require retention and dry-run review |

The intervention should name the missing contract.

## Intervene with a repair path

Weak:

> This is an anti-pattern.

Stronger:

> This promotes `outputs/latest/model.json`, which gives consumers a moving target. Please
> publish a versioned bundle with manifest, params, metrics, and review note.

The stronger comment teaches the desired state.

## Avoid anti-pattern inflation

Not every imperfection is an anti-pattern.

Reserve the term for habits that damage state identity, reproducibility, comparability,
promotion trust, or recovery. Otherwise the review language becomes noise.

Ask:

- would this make a future result harder to explain?
- would this make recovery harder?
- would this make consumers depend on unsupported internals?
- would this hide a meaningful control change?

If yes, intervene.

## Review checkpoint

You understand this core when you can:

- identify a shortcut that damages a state contract
- explain why the shortcut is tempting
- write a review intervention with a repair path
- avoid labeling harmless style differences as anti-patterns
- connect anti-patterns to course contracts

Anti-pattern review is not scolding. It is contract preservation.
