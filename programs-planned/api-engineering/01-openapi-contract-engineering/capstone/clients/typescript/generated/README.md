# TypeScript generator evidence

`schema.reference.d.ts` is a deliberately small, checked-in teaching snapshot. It makes operation naming and the generated surface reviewable before optional tool installation. It is **not** presented as output executed in every environment.

From `capstone/`, the authoritative generation route is:

```bash
make clients-generate
```

The pinned `openapi-typescript` command writes `schema.generated.d.ts`. That file is disposable and ignored by Git. Generation failures, transformed constructs, and unsupported material features belong in the capability report; generated code is never hand-edited to manufacture a pass.
