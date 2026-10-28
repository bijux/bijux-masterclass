# Module 28 Reasoned Solutions

## A. Primitive policy

SchemaKit uses non-coercing primitives and finite numbers. Boxed objects are objects, not primitives. Negative zero is accepted as a finite number unless a refinement rejects it. Literal comparison follows `Object.is` for the supported primitive literal domain.

## B. Optional fields

The object parser checks own presence. Missing optional fields are omitted. Present values are validated with the inner schema; inherited values do not satisfy required fields. Getters should be avoided or rejected by descriptor-aware plain-data policy if invoking them is not acceptable.

## C. Bounds

Validate array length before allocating output. Accumulate only up to the issue limit and preserve source-index order. Return a copied readonly view so later input mutation cannot invalidate the result.

## D. Unions

All-member diagnostics are informative but can grow rapidly. A bounded summary preserves the union-level failure and selected member details. Reordering overlapping members changes first-success behavior and may be breaking.

## E. Recursion

A data-tree schema should reject or bound cycles and excessive depth. Supporting general graphs requires identity tracking and a different output model; it should not be implied by `lazy` alone.

## F. Laboratory

The independent decoder should use one result model and one path context, not throw for ordinary validation failures. Its inferred output must come from schema values rather than duplicated aliases.

## G. SchemaKit

The finished library separates JSON syntax, schema issues, construction errors, refinement failures, and thrown `parse` errors. Public outputs are copied/read-only, and internal contexts remain absent from declarations.

## H. Reconstruction standard

A complete answer names runtime check, output construction, static extraction, error path, bounds, and tests for both success type and rejected values.

## I. Algebra

Each combinator has both a runtime operation and a type-level projection. Array creates a new trusted collection rather than returning the untrusted input. Object constructs a new output with an explicit unknown-key policy. Transform can change output type and must translate thrown conversion errors. Lazy defers schema construction but still needs recursion and cycle policy. Recording these dimensions exposes combinators that are precise statically but incomplete operationally.

## J. Optionality

Missing optional fields should be omitted. A present `undefined` is validated as a present value and normally fails unless the inner schema accepts it. Inherited properties do not satisfy required own fields. Accessors are a policy decision because reading may execute code; data-shaped boundaries may reject them or document that getters run. Unknown keys follow the selected reject/strip policy. This behavior matches `age?: number`, not `age: number | undefined`.

## K. Union order

First-success unions make order observable when schemas overlap. Reordering can therefore be behaviorally breaking even when the inferred union type is unchanged. Bounded diagnostics should include one top-level union failure plus a limited number of member issues and paths, never the entire rejected object.

## L. Recursive input

Depth is a product resource limit, not a TypeScript concern. A WeakSet or equivalent active-path tracker can detect reference cycles while decoding. JSON syntax cannot encode cycles, but direct JavaScript callers can pass cyclic objects to the schema API, so the runtime library must define the result.

## M. Limits

Length and key-count checks should occur before allocating output proportional to hostile declarations. Issue collection should stop at its bound. Recursive depth should be checked before descending. Identifier lengths should be checked before branding or indexing. Limits should produce stable error codes rather than generic allocation failures.

## N. Two evidence classes

A type test can prove that `Infer<typeof User>` has the intended shape. It cannot prove that `User.parse` rejects malformed input. A runtime test can prove rejection and paths but cannot prove declaration inference. A library release needs both because consumers use both contracts.

## O. Getters and proxies

Ordinary property access can invoke getters; reflection operations can invoke proxy traps. A schema library running in the same JavaScript realm cannot promise that validation is side-effect free for arbitrary hostile objects. SchemaKit’s honest boundary is data-shaped values under a documented plain-object policy. Security-sensitive isolation requires serialized input or a separate execution boundary.

## P. Canonical output

Validation establishes a trusted semantic value. Canonical rendering chooses stable textual order and formatting for that value. Sorting object keys recursively makes insertion order irrelevant and produces durable fixtures and hashes. It does not make two semantically different values equal, and it must not read unvalidated arbitrary objects as though they were trusted data.
