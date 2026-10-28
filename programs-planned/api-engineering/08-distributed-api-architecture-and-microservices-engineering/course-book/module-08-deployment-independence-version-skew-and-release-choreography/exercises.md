# Exercises — Module 08: Deployment Independence, Version Skew, and Release Choreography

Work through all twelve problems before opening the answers. In **Deployment Independence, Version Skew, and Release Choreography**, every response must settle this question: **How can services release independently while old and new clients, events, schemas, and database migrations coexist safely?** Use the cumulative platform, not an invented toy system. Preserve inherited guarantees and make every new assumption explicit and falsifiable.

## 1. Why is a separate deployment pipeline not proof of independent deployment?


## 2. What does provider 1.1 need to preserve for consumer 1.0?


## 3. How can consumer 1.1 work with provider 1.0?


## 4. Why must event consumers understand retained historical versions?


## 5. What is the service-owned expand-and-contract sequence?


## 6. Why can rollback fail after a successful code deployment?


## 7. What does shadow comparison need beyond response equality?


## 8. Why is permanent support for every version harmful?


## 9. How can Notification Service release independently?


## 10. What makes Artifact Service rollback harder than Notification rollback?


## 11. Why should a platform catalogue record but not centrally execute all migrations?


## 12. When is a breaking service release acceptable?

