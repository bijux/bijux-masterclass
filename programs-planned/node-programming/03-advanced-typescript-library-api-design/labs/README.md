# Course 3 Laboratories

The ten laboratories are independent products. They isolate one type-system or library-design mechanism so that SchemaKit is not the only context in which you can use it.

| Module | Laboratory | Main proof |
|---:|---|---|
| 21 | Structural Contract Catalog | structural compatibility, literal preservation, branding, runtime exactness |
| 22 | Typed Projection Engine | generic relationships, key tuples, indexed access, inference |
| 23 | Command Outcome Matrix | conditional types, `infer`, distribution, exhaustive runtime dispatch |
| 24 | Typed Change Event Surface | mapped keys, key remapping, template-literal event names |
| 25 | Variance-Safe Event Router | callback input direction, exact event indexing, readonly exposure |
| 26 | Legacy Runtime Declaration Facade | JavaScript runtime and handwritten declaration agreement |
| 27 | Encapsulated ESM Library Surface | exports, subpaths, type-only imports, private internals |
| 28 | Composable Decoder Library | runtime `unknown` validation paired with static inference |
| 29 | Evolvable Client SDK | compatibility fixtures, deprecation, adapters, versioned input |
| 30 | Typed Library Architecture Audit | complete public-surface and change-impact review |

## Method

1. Read the laboratory contract without opening `reference/`.
2. Run the starter tests and identify what is already established.
3. Write a relationship table before adding type expressions.
4. Add one positive and one negative type test before implementation.
5. Implement the smallest API that satisfies the contract.
6. Run type checking, emitted-runtime tests, and declaration inspection where required.
7. Compare with the reference by decision, not line count.

A lab is incomplete if its runtime tests pass while its public type claims are untested.
