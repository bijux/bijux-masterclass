# Exercises — Resolver Architecture, Batching, and Source Ownership

Answer before reading the worked answers. Each response must name the invariant, failure mode, and decisive evidence.

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

