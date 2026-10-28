# Evidence model

GraphQL systems fail when one proof layer is mistaken for another. This course uses eight evidence layers.

1. **Schema evidence** — SDL and catalogue prove what capabilities are declared.
2. **Operation evidence** — checked documents prove what active clients request.
3. **Admission evidence** — validation, trusted-document, and cost reports prove whether an operation may execute.
4. **Authorization evidence** — field and tenant tests prove who may observe or mutate each capability.
5. **Execution evidence** — resolver, batch, timeout, and partial-response tests prove runtime behavior.
6. **Source-authority evidence** — service call logs and ownership maps prove the graph did not bypass owners.
7. **Transport evidence** — HTTP and subscription tests prove framing, status, cancellation, and resume behavior.
8. **Release evidence** — schema diff and old-operation execution prove compatible evolution.

A passing schema linter cannot prove absence of N+1 calls. A passing resolver unit test cannot prove an active mobile operation still validates. A successful query cannot prove another tenant cannot traverse the same field. Each claim must name its decisive evidence layer.

The dependency-light analyzer is intentionally bounded. It parses the operation forms used in the course and evaluates the course cost profile. Independent GraphQL implementations remain required for standards conformance.
