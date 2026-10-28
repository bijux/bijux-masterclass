# Exercises — RPC Boundaries, Service Ownership, and Interaction Choice

Answer before opening the reference answers. For every answer, state the governing rule, one failure example, and the evidence that decides the case.

## 1. A public browser client needs to list analysis runs. Should this become a gRPC method? Explain the governing factors.

Write a concise engineering answer and name the decisive proof.

## 2. An internal worker must receive assignments and report progress for several hours. Compare unary polling, durable events, and a bidirectional RPC stream.

Write a concise engineering answer and name the decisive proof.

## 3. Why is a generated stub not equivalent to a local function call even when the signature looks identical?

Write a concise engineering answer and name the decisive proof.

## 4. A proposed ProjectService exposes CRUD for the projects table. Identify the smell and propose a capability-oriented alternative.

Write a concise engineering answer and name the decisive proof.

## 5. For CreateRun, name the contract, state, deadline, retry, and operational owners.

Write a concise engineering answer and name the decisive proof.

## 6. When is a durable event preferable to a synchronous RPC even if gRPC would be faster?

Write a concise engineering answer and name the decisive proof.

## 7. Why should a worker progress frame not automatically become the public AnalysisRunProgressed event?

Write a concise engineering answer and name the decisive proof.

## 8. Describe the failure path when an HTTP request calls two RPCs and the second times out after committing.

Write a concise engineering answer and name the decisive proof.

## 9. What evidence would justify deploying DatasetTransferService separately?

Write a concise engineering answer and name the decisive proof.

## 10. Give one interaction that should remain a local call throughout this course.

Write a concise engineering answer and name the decisive proof.

## 11. Why does mirroring tables into services tend to create a distributed monolith?

Write a concise engineering answer and name the decisive proof.

## 12. Write a decision rule for HTTP, events, gRPC, and local calls.

Write a concise engineering answer and name the decisive proof.
