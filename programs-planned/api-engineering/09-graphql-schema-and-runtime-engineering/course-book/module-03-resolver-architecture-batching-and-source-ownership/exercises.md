# Exercises — Module 03: Resolver Architecture, Batching, and Source Ownership

Work through all twelve problems before opening the answers. In **Resolver Architecture, Batching, and Source Ownership**, every response must settle this question: **How can nested graph execution remain faithful to service ownership without producing N+1 calls?** Do not stop at terminology. Show how the decision changes a request, durable state, consumer, operator action, or release result, and state how that consequence is tested.

## 1. Why does N+1 appear naturally in field execution?


## 2. What must a DataLoader cache key contain?


## 3. Why must loaders be request-scoped?


## 4. What does batching prove that caching alone does not?


## 5. How should missing batch keys be represented?


## 6. Why can one giant batch still be unsafe?


## 7. Who should authorize artifact access?


## 8. What is wrong with a resolver opening a database connection?


## 9. How does a graph request deadline reach resolvers?


## 10. What telemetry identifies N+1 in production?


## 11. Why can a global loader be correct in tests and unsafe in production?


## 12. When can a gateway compute a field without a source call?
