# Module 26 Reasoned Solutions

## A. Parity

A declaration mismatch is not repaired by making the type broader until every runtime value fits. The public contract should describe intended behavior, and the runtime should be adapted when it violates that intent. Tests need both checked consumer source and emitted JavaScript execution.

## B. Scope

Imports/exports create an external module. A top-level declaration without module syntax may affect globals. `declare module 'name'` describes a module specifier. An augmentation targets an existing module and requires corresponding runtime behavior when values are added.

## C. Emission

Repair source annotations or export structure. Editing generated declarations creates drift at the next build. A stable public type should not expose local symbols, mutable accumulators, or private source paths.

## D. Tests

Positive tests assert inferred results, not only compilation. Each negative test should contain one intended error. Public-entry imports prove the supported consumer route; a source-relative test does not.

## E. Augmentation

The runtime effect must load before use, and conflicts can arise when multiple packages augment the same member. An explicit wrapper or adapter is usually easier to discover, remove, and version unless ecosystem-wide open extension is the intended architecture.

## F. Laboratory

The legacy counter declaration must match named exports, construction/call behavior, callback timing, and error behavior. The strongest evidence compiles a consumer and executes it against the actual JavaScript file.

## G. SchemaKit

The declaration matrix should show type-only exports separately from runtime exports. Subpath declarations must align with their runtime files. Internal `Decoder<T>` or parser contexts should remain unreachable.

## H. Reconstruction standard

A complete answer treats `.d.ts`, JavaScript, and package metadata as separate artifacts with separate tests. “TypeScript generated it” is not sufficient evidence.

## I. Artifact alignment

The declaration file is a consumer contract, not runtime evidence. Each exported value declaration must correspond to an emitted binding reachable through the same package path. Type-only declarations intentionally have no binding. Declaration maps aid source navigation but do not change semantics. Package metadata determines whether consumers can resolve the files at all.

## J. Wrong declaration

A dishonest return type can make valid numeric operations appear invalid and invalid string operations appear safe. Type checking the declaration alone cannot detect the mismatch. A consumer fixture that builds and runs against emitted JavaScript closes this evidence gap. Generated declarations reduce drift, but tests still matter when JavaScript implementations or manual declaration facades are involved.

## K. Type/value namespaces

Classes generally create both a type and a runtime value. Interfaces and type aliases are erased. Type-only imports state that no runtime binding is needed. Under verbatim module syntax, TypeScript does not silently rewrite an incorrect value import into a type-only dependency. This makes package effects and runtime resolution more explicit.

## L. Consumer fixture

The consumer should depend on the built package surface, not relative source paths. Its success proves declaration resolution and runtime entry-point resolution together. A deep source import can conceal a broken `exports` map and is therefore weak evidence.

## M. Declaration quality

Private implementation names should not appear in a public signature unless they are intentionally exported. Large anonymous inferred types make diagnostics and compatibility reviews difficult. Named public aliases can stabilize the contract while remaining generated from source. Overloads should be ordered from specific to general and must match runtime behavior.

## N. Compatibility fixture

Declaration compatibility is best tested from old consumer source. Renaming a public type can break explicit imports even if an equivalent structural type remains. Overload order can alter inference. A generic default change can modify inferred output without a compile error. Narrowed inputs reject old calls. Returning a concrete internal class leaks future compatibility obligations. The fixture should compile against the candidate declaration output, not the library source tree.

## O. Export census

A runtime namespace contains value exports only. Interfaces and type aliases legitimately appear only in declarations. Every declared function, class, constant, or object needs a corresponding runtime export at the same supported path. An unexplained runtime-only export may become an accidental capability if reachable through the package map; an unexplained declaration-only value is dishonest.
