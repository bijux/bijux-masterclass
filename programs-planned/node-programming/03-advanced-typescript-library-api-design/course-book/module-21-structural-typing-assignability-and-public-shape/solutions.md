# Module 21 Reasoned Solutions

## A. Assignability

The assignment through `value` succeeds. Its source type contains `id: string`, so it satisfies the minimum target surface. The fresh literal assigned directly to `ReadUser` receives an excess-property error for `role`. The runtime object could still contain `role`; this diagnostic is a construction check, not exactness.

With `exactOptionalPropertyTypes`, `{}` and `{ cache: false }` satisfy `Options`. `{ cache: undefined }` does not, because a present optional property must contain `boolean`. Use `cache: boolean | undefined` when presence is required and undefined is a valid value.

The index read is `number | undefined` under `noUncheckedIndexedAccess`; the assignment to `number` fails. A string index signature constrains possible values but does not prove key existence. Narrow, provide a default, or use a lookup API that represents absence.

`Mode` is `'fast' | 'safe'`. `satisfies` checks each value against the record value contract while retaining the finite inferred keys. Annotating the variable as `Record<string, ...>` widens the key domain to `string`.

## B. Assertions

The JSON assertion claims a shape without validation. Parse to `unknown`, check the object and property, then construct trusted data.

The non-null assertion on the descriptor is valid only if code established the own property without an intervening mutation. A robust helper handles `undefined` or creates the property itself before lookup.

The `UserId` assertion is justified only when `validated` passed the complete user-ID invariant immediately beforehand. Keep the assertion inside the constructor so arbitrary callers cannot brand values.

## C. Exactness

A strong project policy accepts ordinary or null-prototype records, inspects own string keys without invoking inherited getters, rejects unknown keys, ignores symbols only if the product explicitly declares them outside the data model, distinguishes missing tags from present invalid values, copies accepted arrays, rejects duplicates, and returns path-aware issues. The validated result can expose readonly arrays and exact optional presence even though the raw input was `unknown`.

## D. Brands

A database user ID and validated port are good candidates because accidental interchange matters and construction enforces stable invariants. A canonical package subpath may also be branded inside a package-authoring tool. A display name or search query usually needs validation but not nominal separation unless several validated string domains are frequently mixed. A JSON string before parsing is not a domain identity; brand the validated result, not an unexamined encoding.

## E. Result states

One truthful model is:

```ts
type LoadResult<T> =
  | { readonly ok: true; readonly value: T; readonly source: 'cache' | 'origin' }
  | { readonly ok: false; readonly error: Error };
```

An exhaustive consumer switches on `ok`. Do not include `fromCache` on failures unless the failure contract has a meaningful cache origin.

## F. Laboratory

The feature declaration should preserve literal IDs with a `const` generic or `satisfies`. Runtime construction must still trim and validate IDs and reject duplicates. The branded ID is produced only by that validator. A duplicate or malformed ID is an example that static shape alone cannot reject.

## G. SchemaKit

`ParseResult<T>` should be discriminated and readonly. `Issue` should contain bounded diagnostic context rather than the complete rejected value. The `SchemaName` constructor validates syntax before its local assertion. The plain-object helper must not treat arrays or arbitrary class instances as configuration records. Tests should prove narrowing in both branches and rejection of an unvalidated branded string.

## H. Reconstruction standard

A complete answer separates four layers:

- structural compatibility of types;
- special fresh-literal feedback;
- mutation capability exposed by a reference;
- runtime validation and identity.

Any answer that uses “interface” as a synonym for runtime shape remains incomplete.

## I. Assignability matrix reasoning

The stored object is assignable to the narrower target because TypeScript compares required target members against the source shape. The extra `role` member remains in the runtime object but is not visible through the target type. A fresh literal receives the additional excess-property check because TypeScript treats it as a likely misspelling or unintended public field. Moving the literal through a variable does not create runtime validation; it only changes which static heuristic applies.

With exact optional properties, `{ timeout: undefined }` is not the same as absence. The present property must contain a number unless `undefined` is explicitly part of the value type. Distinct unique-symbol brands reject substitution because the witness properties are structurally different. A readonly target blocks mutation through that reference only; a mutable source alias can still change the object.

Principled repairs preserve the product distinction: model the extra field, omit it, widen the target deliberately, include `undefined` deliberately, convert between branded domains through validation, or isolate/freeze the object when runtime immutability is required. Assertions and disabled strictness are weak because they erase evidence rather than establishing it.

## J. Exactness policy

Ignoring unknown keys yields a normalized output containing only understood fields. Rejecting unknown keys makes misspellings visible but can make forward-compatible data unreadable. Preserving unknown keys requires an output type and storage policy that acknowledge those values. Excess-property checking cannot implement any of these because it occurs only in selected source-code contexts and disappears after emission.

## K. Three checking forms

The broad annotation normally widens individual route values to `string`. `satisfies` checks the route constraint while retaining each literal path. An assertion asks the checker to trust the programmer and can accept a value the checker never proved. The preserved literal type can drive route-specific return types or exhaustive route metadata without a second declaration.

## L. Branding boundary

The parser should accept `unknown`, narrow to `string`, enforce a finite length and grammar, and only then apply the brand assertion inside the construction boundary. The local assertion is justified by preceding runtime evidence. A public `brand(value: string)` function with no checks would turn the witness into decoration.

## M. Public shape

Consumers need the feature definition, catalog operations, and construction function. They do not need the internal map, duplicate-detection set, or mutable staging structures. Tests should use public behavior—IDs, lookup, duplicate rejection, and inferred literals—rather than importing implementation helpers.
