# Course 6 Compiler and Runtime Investigations

The 80 investigations train causal prediction across TypeScript and Node.js networking. Forty cases are expected to type-check, thirty are expected to fail during type checking, four type-check and pass at runtime, and six type-check but fail at runtime for the declared reason.

The broader outcome model matters. TypeScript can reject an invalid callback or missing union case, but it cannot prove that a TCP read contains one complete message, that a TLS certificate names the intended host, that a timed-out POST was not committed, or that an SSE subscriber cannot grow an unbounded queue.

Each manifest record names:

- the expected category;
- the governing checker, runtime, or protocol rule;
- the decisive phase;
- the intended causal failure;
- the smallest requirement-preserving repair;
- a tempting repair that weakens the product.

Run all cases:

```bash
make investigations
```

Outcome categories:

- `typecheck-pass`
- `typecheck-fail`
- `run-pass`
- `run-fail`

Before running a case, write the expected category and one-sentence cause. After running it, explain any difference at the correct layer: TypeScript assignability, JavaScript execution, Node API behavior, operating-system behavior, protocol semantics, or product policy.

Runtime cases use bounded local servers or pure protocol logic. They do not require public DNS or Internet access. A case fails if it produces the right category for an unrelated cause; the intended diagnostic or runtime event must be the decisive one.
