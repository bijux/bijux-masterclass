# Exercises — Module 03: Data Ownership, Replication, and Cross-Service Query Design

Work through all twelve problems before opening the answers. In **Data Ownership, Replication, and Cross-Service Query Design**, every response must settle this question: **How can each service own its writes while the system still answers cross-capability questions without shared tables or hidden distributed transactions?** Do not stop at terminology. Show how the decision changes a request, durable state, consumer, operator action, or release result, and state how that consequence is tested.

## 1. Why is a separate schema not sufficient for database-per-service?


## 2. A projection receives version 8 after version 6. What should happen?


## 3. When is gateway composition preferable to a local projection?


## 4. Why must a partial response be explicit?


## 5. What makes a replicated view non-authoritative?


## 6. Why is a global migration head incompatible with independent service release?


## 7. How should Notification Service react to an old duplicate event?


## 8. What is wrong with bilateral table synchronization?


## 9. When is a reporting data product preferable to an API join?


## 10. How can an artifact be orphaned without data corruption?


## 11. Why must TypeScript reject unsafe integer versions even though Python can represent them?


## 12. What is the safe alternative to uncontrolled dual writes during extraction?

