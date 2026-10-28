# Analysis API Platform 1.0 capstone

The capstone turns the interfaces and services produced by Courses 1–9 into one governed platform product. It preserves the authority of every predecessor layer:

- domain services own business facts and authorization;
- OpenAPI, AsyncAPI, Protobuf, and GraphQL remain native contract authorities;
- the platform owns discovery metadata, immutable publication, policy execution, lifecycle workflows, golden paths, documentation, sandbox orchestration, artifact publication, runtime reconciliation, and product-support evidence;
- automated policy can reject objective violations, but accountable people own exceptional risk and business judgment.

The dependency-light implementation is deliberately small enough to read. It is not presented as a replacement for an operated catalog, package registry, gateway, identity system, or portal. The environment-backed routes explain how to integrate those systems without transferring business ownership to the platform.

Begin with `course-book/capstone-map.md`, then run:

```bash
make capstone-tour
make network-lab-proof
make core-proof
```
