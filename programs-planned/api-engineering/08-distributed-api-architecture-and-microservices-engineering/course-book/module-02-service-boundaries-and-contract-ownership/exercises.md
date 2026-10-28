# Exercises — Service Boundaries, Bounded Contexts, and Contract Ownership

Answer before reading the worked answers. Every answer must name the governing invariant and decisive evidence.

## 1. Why is RunService plus ProjectService plus DatasetService likely worse than Analysis Control?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 2. What makes Worker Plane a compute plane rather than a business service?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 3. Can a gateway be called a microservice? Why is that label insufficient?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 4. Why should Artifact Service not import Analysis Control domain classes?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 5. Who owns the `AnalysisRunCompleted` event contract?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 6. What is the difference between contract owner and state owner?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 7. Why are generated Protobuf messages acceptable to share while a `canCompleteRun` library is risky?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 8. A service owns no data but has a distinct deployment and protocol. Is it invalid?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 9. How does ubiquitous language help detect a boundary?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 10. What indicates a distributed monolith even if services have separate repositories?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 11. Who owns an artifact reference stored in Analysis Control?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.

## 12. Why is one accountable operational owner a completion gate?

Write a concrete engineering answer. State one failure that the wrong decision creates and name the decisive proof.
