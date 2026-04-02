# Metaprogramming Capstone Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Capstone guide"]
  page["Metaprogramming Capstone Guide"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

The metaprogramming capstone is the executable proof for the course. It is a compact
incident-plugin runtime where decorators, descriptors, metaclasses, and introspection
must coexist without hiding responsibility.

## What the capstone proves

- configuration invariants can live on descriptor-backed fields
- wrappers can preserve callable metadata while still recording action history
- class-definition-time registration can stay deterministic and testable
- manifest export can expose the runtime shape without executing plugin behavior

## Read these guides together

- [Capstone Map](capstone-map.md)
- [Capstone File Guide](capstone-file-guide.md)
- [Capstone Proof Checklist](capstone-proof-checklist.md)
- [Capstone Extension Guide](capstone-extension-guide.md)

## Best entrypoints

- repository guide: `capstone/README.md`
- runtime architecture: `capstone/ARCHITECTURE.md`
- proof route: `capstone/PROOF_GUIDE.md`
- source: `capstone/src/incident_plugins/`
- tests: `capstone/tests/`

## Review questions

- Which work happens before an instance exists?
- Which runtime facts are inspectable from the public surface?
- Which mechanism would you replace first if you had to simplify the design?
