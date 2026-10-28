# Exercises — HTTP, Events, and gRPC in One Architecture: Release and Final Defense

Answer before opening the reference answers. For every answer, state the governing rule, one failure example, and the evidence that decides the case.

## 1. Assign one responsibility each to public HTTP, durable events, local calls, and gRPC.

Write a concise engineering answer and name the decisive proof.

## 2. Why should gRPC be introduced before extracting a separate deployable service?

Write a concise engineering answer and name the decisive proof.

## 3. Design a safe shadow step for GetRun and explain why CreateRun is harder.

Write a concise engineering answer and name the decisive proof.

## 4. Why is automatic local fallback after an ambiguous CreateRun RPC failure unsafe?

Write a concise engineering answer and name the decisive proof.

## 5. What public evidence must remain unchanged during cutover?

Write a concise engineering answer and name the decisive proof.

## 6. Who publishes AnalysisRunCompleted after a worker result arrives over gRPC?

Write a concise engineering answer and name the decisive proof.

## 7. How should Course 4 and Course 5 gates participate in the RPC release?

Write a concise engineering answer and name the decisive proof.

## 8. Name three signs that a proposed gRPC service would create a distributed monolith.

Write a concise engineering answer and name the decisive proof.

## 9. Why are RPC API version and service release version separate?

Write a concise engineering answer and name the decisive proof.

## 10. Describe a rollback-compatible migration sequence for migrations 013–015.

Write a concise engineering answer and name the decisive proof.

## 11. What must the final defense prove after response loss?

Write a concise engineering answer and name the decisive proof.

## 12. What evidence belongs in the Course 8 service-boundary dossier?

Write a concise engineering answer and name the decisive proof.
