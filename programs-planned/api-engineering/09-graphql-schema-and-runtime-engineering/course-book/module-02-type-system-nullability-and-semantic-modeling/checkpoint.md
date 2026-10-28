# Checkpoint 02 — Type System, Nullability, and Semantic Modeling

Do not continue until every condition is supported by executable or inspected evidence.

- [ ] Every schema field has a deliberate nullability decision tied to a real source guarantee.
- [ ] OneOf input coercion accepts exactly one non-null member and rejects zero, multiple, or null members.
- [ ] Enums, interfaces, unions, custom scalars, and input objects are used for semantic reasons rather than cosmetic grouping.
- [ ] Controlled resolver failures demonstrate the intended null-bubbling boundary.
- [ ] The schema contains no output field whose non-null promise is stronger than the underlying service can sustain.
- [ ] Lab 02 report includes accepted and rejected coercion cases plus the response position affected by failure.

**Gate:** run `make module-02-proof`. A green command without the lab report and the listed evidence does not count.
