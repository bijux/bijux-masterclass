# Exercises

Use these exercises to practice promotion judgment, not only file movement.

The strongest answers will explain what is being promoted, who can trust it, and which
evidence makes that trust defensible.

## Exercise 1: Write a promotion contract

A candidate model is ready for downstream incident escalation review.

Write a short promotion statement that names:

- what is being promoted
- which downstream consumer may use it
- which params and metrics justify it
- what should remain internal

## Exercise 2: Design a release surface

Design a `publish/v1/` bundle for a promoted DVC result.

List the files you would include and explain why each file belongs there.

Also name one internal file or directory that should not be part of the consumer contract.

## Exercise 3: Find the audit gap

A bundle has:

```text
publish/v1/
  model.json
  metrics.json
  params.yaml
```

There is no manifest, and the metrics were produced before the promoted parameter change.

Write a review note that explains the audit gap and the repair.

## Exercise 4: Define a registry boundary

A team tells consumers:

> Use whatever model is in `outputs/latest/`.

Rewrite this as a stronger registry or publish-boundary contract.

Your answer should say what consumers may depend on and what they should ignore.

## Exercise 5: Reject or repair a promotion

A promoted release contains debug plots, two model files, old metrics, and no review note.

Decide whether you would reject the promotion or repair it before acceptance.

Explain what evidence or bundle changes you would require.

## Mastery check

You have a strong grasp of this module if your answers consistently keep five ideas
visible:

- promotion is a downstream trust contract
- release surfaces should be small and stable
- params, metrics, locks, and manifests answer different audit questions
- registry boundaries protect consumers from internal churn
- neat-looking bundles can still be rejected when evidence is inconsistent
