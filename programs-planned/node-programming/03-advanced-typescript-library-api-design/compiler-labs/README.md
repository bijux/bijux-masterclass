# Type-Checker and Runtime Investigations

These eighty cases isolate TypeScript library-design rules. Predict before running them.

## Outcome vocabulary

- `typecheck-pass` — the selected checker accepts the intended relationship.
- `typecheck-fail` — the checker rejects the source for the named cause.
- `run-pass` — emitted JavaScript completes with the exact expected output.
- `run-fail` — emitted JavaScript fails for the named runtime reason.

A failure counts only when the intended cause is decisive. A typo that happens to make a negative case fail is not evidence for the target rule.

## Method

1. Read the case source without opening its manifest record.
2. Predict the first decisive phase.
3. Name source and target types or runtime values.
4. Run `make investigations`.
5. Repair the requirement rather than deleting it.
6. Compare the principled repair with the weak repair recorded in the manifest.
