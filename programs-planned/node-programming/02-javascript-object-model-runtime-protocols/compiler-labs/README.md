# Type-Checker and Runtime Investigations

These eighty isolated programs test the boundary among TypeScript's static model, JavaScript object semantics, Node execution, and product design. Predict before running the supplied route. A failure counts only when it occurs for the intended causal reason recorded in `manifest.json`.

## Outcome vocabulary

- `typecheck-pass` — strict TypeScript accepts the source.
- `typecheck-fail` — strict TypeScript rejects the source for the named relationship.
- `run-pass` — emitted JavaScript completes with the exact output.
- `run-fail` — emitted JavaScript fails for the specified runtime reason.

## Distribution

| Outcome | Cases |
|---|---:|
| `run-fail` | 12 |
| `run-pass` | 9 |
| `typecheck-fail` | 28 |
| `typecheck-pass` | 31 |

## Method

1. Read title and source without opening the manifest explanation.
2. Predict static and runtime outcomes.
3. Name the first decisive phase and governing object-model rule.
4. Run `make investigations`.
5. Repair the requirement rather than merely avoiding the diagnostic.
6. Compare the principled and weak repairs.

## Catalog

| ID | Module | Category | Question |
|---|---:|---|---|
| `m11-c01` | 11 | `typecheck-pass` | Complete data descriptor |
| `m11-c02` | 11 | `typecheck-fail` | Descriptor writable must be Boolean |
| `m11-c03` | 11 | `typecheck-pass` | Reflect own keys include symbols |
| `m11-c04` | 11 | `typecheck-fail` | Property key is not always string |
| `m11-c05` | 11 | `run-pass` | Enumeration surfaces differ |
| `m11-c06` | 11 | `run-fail` | Spread invokes an enumerable getter |
| `m11-c07` | 11 | `typecheck-pass` | Symbol-keyed metadata is typed |
| `m11-c08` | 11 | `typecheck-fail` | Descriptor lookup may be absent |
| `m12-c01` | 12 | `typecheck-pass` | Inherited method uses derived receiver |
| `m12-c02` | 12 | `run-fail` | Prototype object lacks instance field initialization |
| `m12-c03` | 12 | `typecheck-pass` | Own-property check precedes read |
| `m12-c04` | 12 | `typecheck-fail` | Explicit this contract rejects wrong receiver |
| `m12-c05` | 12 | `run-pass` | Inherited getter preserves receiver |
| `m12-c06` | 12 | `run-fail` | Inherited input is rejected |
| `m12-c07` | 12 | `typecheck-pass` | Null-prototype dictionary remains explicit |
| `m12-c08` | 12 | `typecheck-fail` | Prototype method needs declared receiver field |
| `m13-c01` | 13 | `typecheck-pass` | Explicit receiver method call |
| `m13-c02` | 13 | `typecheck-fail` | Extracted explicit-this method cannot be called bare |
| `m13-c03` | 13 | `typecheck-fail` | Arrow function is not constructible |
| `m13-c04` | 13 | `typecheck-pass` | Construct signature states construction |
| `m13-c05` | 13 | `run-pass` | Bound constructor preserves prefix arguments |
| `m13-c06` | 13 | `run-fail` | Extracted method loses receiver at runtime |
| `m13-c07` | 13 | `typecheck-pass` | Bound prefix arguments remain typed |
| `m13-c08` | 13 | `typecheck-fail` | Callable interface is not a constructor |
| `m14-c01` | 14 | `typecheck-pass` | Private brand predicate |
| `m14-c02` | 14 | `typecheck-fail` | Private field is inaccessible outside class |
| `m14-c03` | 14 | `typecheck-fail` | Derived constructor cannot use this before super |
| `m14-c04` | 14 | `run-fail` | Prototype forgery lacks private brand |
| `m14-c05` | 14 | `run-pass` | Class field initialization order |
| `m14-c06` | 14 | `typecheck-pass` | Static private field belongs to constructor |
| `m14-c07` | 14 | `typecheck-fail` | Private fields are not structurally interchangeable |
| `m14-c08` | 14 | `typecheck-pass` | Constructor return type remains instance |
| `m15-c01` | 15 | `typecheck-pass` | Narrow capability injection |
| `m15-c02` | 15 | `typecheck-fail` | Missing capability method is rejected |
| `m15-c03` | 15 | `typecheck-fail` | Class cannot extend two bases |
| `m15-c04` | 15 | `typecheck-pass` | Constrained mixin preserves base type |
| `m15-c05` | 15 | `run-pass` | Composition preserves call order |
| `m15-c06` | 15 | `run-fail` | Copied accessor executes during composition |
| `m15-c07` | 15 | `typecheck-fail` | Readonly capability cannot be replaced |
| `m15-c08` | 15 | `typecheck-pass` | Function composition needs compatible stages |
| `m16-c01` | 16 | `typecheck-pass` | Unique symbol property contract |
| `m16-c02` | 16 | `typecheck-fail` | Different unique symbols are incompatible |
| `m16-c03` | 16 | `typecheck-pass` | Iterator protocol is typed |
| `m16-c04` | 16 | `typecheck-fail` | Iterator item type mismatch |
| `m16-c05` | 16 | `run-pass` | Primitive conversion receives a hint |
| `m16-c06` | 16 | `run-fail` | Non-primitive conversion result fails |
| `m16-c07` | 16 | `typecheck-pass` | toStringTag getter returns string |
| `m16-c08` | 16 | `typecheck-fail` | Protocol method return type is enforced |
| `m17-c01` | 17 | `typecheck-pass` | Repeatable iterable creates generator |
| `m17-c02` | 17 | `typecheck-fail` | Iterator result item type mismatch |
| `m17-c03` | 17 | `typecheck-pass` | Generator return and yield types |
| `m17-c04` | 17 | `typecheck-fail` | Yielded value violates generator contract |
| `m17-c05` | 17 | `run-pass` | Early break closes generator |
| `m17-c06` | 17 | `run-fail` | Mutation invalidates traversal |
| `m17-c07` | 17 | `typecheck-fail` | Iterator is not automatically iterable |
| `m17-c08` | 17 | `typecheck-pass` | IterableIterator satisfies both protocols |
| `m18-c01` | 18 | `typecheck-pass` | Reflect preserves receiver |
| `m18-c02` | 18 | `typecheck-fail` | ownKeys trap returns property keys |
| `m18-c03` | 18 | `typecheck-pass` | Revocable proxy exposes revoke |
| `m18-c04` | 18 | `typecheck-pass` | Proxy target retains static shape |
| `m18-c05` | 18 | `run-fail` | Private field rejects proxy receiver |
| `m18-c06` | 18 | `run-fail` | Proxy cannot hide non-configurable key |
| `m18-c07` | 18 | `typecheck-fail` | Proxy constructor requires object target |
| `m18-c08` | 18 | `typecheck-pass` | Define-property trap can delegate |
| `m19-c01` | 19 | `typecheck-pass` | Structured clone preserves typed data shape |
| `m19-c02` | 19 | `typecheck-fail` | WeakRef requires an object target |
| `m19-c03` | 19 | `typecheck-pass` | Disposable contract requires Symbol.dispose |
| `m19-c04` | 19 | `typecheck-fail` | Missing disposal method violates contract |
| `m19-c05` | 19 | `run-pass` | Structured clone preserves cycle |
| `m19-c06` | 19 | `run-fail` | JSON cannot clone a cycle |
| `m19-c07` | 19 | `typecheck-pass` | Finalization registry held value is explicit |
| `m19-c08` | 19 | `typecheck-fail` | Readonly map prevents remapping mutation |
| `m20-c01` | 20 | `typecheck-pass` | Readonly view hides mutation authority |
| `m20-c02` | 20 | `typecheck-fail` | Readonly children reject push |
| `m20-c03` | 20 | `typecheck-pass` | Exhaustive representation switch |
| `m20-c04` | 20 | `typecheck-fail` | Missing representation branch is visible |
| `m20-c05` | 20 | `run-fail` | Plain persistence loses class behavior |
| `m20-c06` | 20 | `run-pass` | Runtime and record remain separate |
| `m20-c07` | 20 | `typecheck-fail` | Private mutation method stays inaccessible |
| `m20-c08` | 20 | `typecheck-pass` | Protocol capability can be tested safely |
