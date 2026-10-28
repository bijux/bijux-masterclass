# Exercises — Module 05: Mutations, Idempotency, Concurrency, and Domain Results

Work through all twelve problems before opening the answers. In **Mutations, Idempotency, Concurrency, and Domain Results**, every response must settle this question: **How do graph mutations preserve the durable command guarantees of the owning service?** A useful solution connects semantics to mechanism: who owns the decision, what can go wrong, and which retained artifact proves the claimed outcome.

## 1. Does serial top-level mutation execution make two fields atomic?


## 2. Why use one input object per mutation?


## 3. Where should an idempotency record live?


## 4. What happens when a client retries with the same key and same input?


## 5. What happens when the same key carries changed input?


## 6. Why is expectedVersion checked in Analysis Control?


## 7. Distinguish CONFLICT from PRECONDITION_FAILED.


## 8. When should a domain problem be in data rather than errors?


## 9. What belongs in the GraphQL errors array for a mutation?


## 10. Why preserve clientMutationId?


## 11. Can the gateway retry startAnalysis automatically?


## 12. Why avoid a generic updateRun mutation?
