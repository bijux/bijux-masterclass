# Exercises — Module 04: Unary RPCs, Metadata, Status, and Rich Errors

Work through all twelve problems before opening the answers. In **Unary RPCs, Metadata, Status, and Rich Errors**, every response must settle this question: **How should a unary RPC expose success and failure so that generated clients receive stable application meaning rather than transport accidents or leaked internals?** For every answer, separate the authoritative boundary from convenient diagnostics, then explain which failing experiment would force you to revise the design.

## 1. Which fields belong in metadata for `CreateRun`, and which belong in the request message?

Write a concise engineering answer and name the decisive proof.

## 2. Map an invalid algorithm, a missing run, and a stale revision to gRPC statuses.

Write a concise engineering answer and name the decisive proof.

## 3. Why is `UNKNOWN` or `INTERNAL` an inadequate default for expected domain conflicts?

Write a concise engineering answer and name the decisive proof.

## 4. What makes an error detail safe for a client?

Write a concise engineering answer and name the decisive proof.

## 5. Where should a database unique-constraint error be translated?

Write a concise engineering answer and name the decisive proof.

## 6. Why should a generic interceptor not decide run ownership by itself?

Write a concise engineering answer and name the decisive proof.

## 7. Describe the ambiguous outcome when `CreateRun` commits but the response is lost.

Write a concise engineering answer and name the decisive proof.

## 8. Differentiate application `CancelRun` from transport cancellation.

Write a concise engineering answer and name the decisive proof.

## 9. When should a client treat `UNAVAILABLE` as retryable?

Write a concise engineering answer and name the decisive proof.

## 10. How should a hidden resource be represented to an authenticated but unauthorized caller?

Write a concise engineering answer and name the decisive proof.

## 11. Why is a global gRPC-to-HTTP status map insufficient?

Write a concise engineering answer and name the decisive proof.

## 12. Define the proof that Python and TypeScript expose equivalent unary behavior.

Write a concise engineering answer and name the decisive proof.
