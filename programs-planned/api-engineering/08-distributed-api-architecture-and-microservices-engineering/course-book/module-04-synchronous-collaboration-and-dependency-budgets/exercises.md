# Exercises — Module 04: Synchronous Collaboration, API Composition, and Dependency Budgets

Work through all twelve problems before opening the answers. In **Synchronous Collaboration, API Composition, and Dependency Budgets**, every response must settle this question: **How do we keep synchronous service collaboration bounded so that fan-out, retries, and version skew do not make the public request path fragile?** For every answer, separate the authoritative boundary from convenient diagnostics, then explain which failing experiment would force you to revise the design.

## 1. Why does a three-service serial path reduce availability?


## 2. Why is a synchronous cycle more than a diagram smell?


## 3. Who owns the deadline for a public request?


## 4. What is wrong with retries in client, gateway, mesh, and callee simultaneously?


## 5. How should the gateway represent an unavailable artifact service for a completed run?


## 6. Why can parallel fan-out still be harmful when it lowers latency?


## 7. A run list triggers one artifact RPC per row. What should change?


## 8. When can a read retry be safe?


## 9. Why can service discovery not decide retry safety?


## 10. What does maximum public synchronous depth protect?


## 11. When should the gateway skip optional composition?


## 12. Why is a batch endpoint sometimes better than client-side concurrency?

