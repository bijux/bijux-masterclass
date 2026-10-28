# Course 4 Compiler and Runtime Investigations

The 80 cases isolate one causal claim at a time. Predict the category before running the suite:

- `typecheck-pass`;
- `typecheck-fail`;
- `run-pass`;
- `run-fail`.

A failure case counts only when it fails for the target rule recorded in `manifest.json`. An unrelated import, syntax, or configuration failure is not evidence.

```bash
make investigations
```

The runner type-checks every case independently and executes only the runtime categories. Runtime-pass output must match exactly; runtime-fail stderr must contain the declared causal text.
