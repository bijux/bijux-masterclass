# Exercises — Module 02: Service Boundaries, Bounded Contexts, and Contract Ownership

Work through all twelve problems before opening the answers. In **Service Boundaries, Bounded Contexts, and Contract Ownership**, every response must settle this question: **How do we draw service boundaries around cohesive decisions and language without turning tables, classes, or teams into accidental services?** Treat each problem as a design review: state the rule, construct the smallest counterexample, and select an oracle capable of rejecting your own answer.

## 1. Why is RunService plus ProjectService plus DatasetService likely worse than Analysis Control?


## 2. What makes Worker Plane a compute plane rather than a business service?


## 3. Can a gateway be called a microservice? Why is that label insufficient?


## 4. Why should Artifact Service not import Analysis Control domain classes?


## 5. Who owns the `AnalysisRunCompleted` event contract?


## 6. What is the difference between contract owner and state owner?


## 7. Why are generated Protobuf messages acceptable to share while a `canCompleteRun` library is risky?


## 8. A service owns no data but has a distinct deployment and protocol. Is it invalid?


## 9. How does ubiquitous language help detect a boundary?


## 10. What indicates a distributed monolith even if services have separate repositories?


## 11. Who owns an artifact reference stored in Analysis Control?


## 12. Why is one accountable operational owner a completion gate?

