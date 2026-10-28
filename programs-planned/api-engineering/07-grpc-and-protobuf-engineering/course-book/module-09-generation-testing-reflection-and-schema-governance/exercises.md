# Exercises — Module 09: Generation, Testing, Reflection, and Schema Governance

Work through all twelve problems before opening the answers. In **Generation, Testing, Reflection, and Schema Governance**, every response must settle this question: **How do we make proto source, generated code, runtime services, tests, descriptors, reflection, and release policy agree without treating code generation as proof?** The strongest answer distinguishes specification, implementation, and operational evidence, then demonstrates where a plausible shortcut would fail.

## 1. Why is generated source not the contract source of truth?

Write a concise engineering answer and name the decisive proof.

## 2. What should be pinned for reproducible generation besides `protoc`?

Write a concise engineering answer and name the decisive proof.

## 3. Compare the roles of `protoc` and Buf.

Write a concise engineering answer and name the decisive proof.

## 4. What does a descriptor set prove?

Write a concise engineering answer and name the decisive proof.

## 5. What does runtime reflection prove, and what does it not prove?

Write a concise engineering answer and name the decisive proof.

## 6. Why can a mock server not prove CreateRun idempotency?

Write a concise engineering answer and name the decisive proof.

## 7. Name the minimum test layers for WatchRun.

Write a concise engineering answer and name the decisive proof.

## 8. Why can a binary-compatible field rename fail generated-client compatibility?

Write a concise engineering answer and name the decisive proof.

## 9. What information belongs in the RPC catalogue but not the `.proto`?

Write a concise engineering answer and name the decisive proof.

## 10. When should generated source be checked into the repository?

Write a concise engineering answer and name the decisive proof.

## 11. How should an unavailable Buf tool be represented in verification?

Write a concise engineering answer and name the decisive proof.

## 12. Define the deterministic generation release gate.

Write a concise engineering answer and name the decisive proof.
