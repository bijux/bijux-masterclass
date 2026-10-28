# Module 15 Reasoned Solutions

## A. False inheritance repair

`ReportService` should own or receive a `Store` capability and forward only the operations required by its public report contract. Storage errors should be translated at the application boundary where report context is available. The store should not be exposed unless callers are intentionally granted storage authority. A factory or application composition root should own cleanup.

Extending `FileStore` is a weak repair because it claims substitutability and publishes unrelated storage methods merely to reuse implementation.

## B. Four composition mechanisms

A private-field class gives runtime brand identity and shared prototype methods. A closure factory gives lexical privacy but creates method functions per factory call and has no class identity. Prototype delegation shares methods but requires deliberate per-instance state. Copying methods creates own properties and breaks live linkage to the source behavior.

No mechanism is universally best. The decision follows identity, scale, replacement, reflection, and lifecycle requirements.

## C. Mixin conflict

Silent last-wins behavior is unstable because application order becomes an undocumented semantic input. A principled design either gives the capabilities distinct names, composes through documented `super` calls, or stores separate `labeling` and `audit` collaborators. The explicit collaborator design is usually easiest to inspect and test.

## D. Least-authority renderer

A `NodeReadView` should expose only stable reads such as `id`, `label`, and an attribute snapshot. A TypeScript readonly interface prevents ordinary writes through that view. If hostile or untyped code is in scope, a wrapper object or frozen plain snapshot provides a stronger runtime boundary. Readonly typing alone is not a security boundary.

## E. Cross-capability failure

Mutate-then-save exposes unsaved state if save fails. Save-then-mutate can persist a state the in-memory authority never publishes if local publication fails. Candidate-save-publish gives the application a strong pre-publication failure rule when the store contract is reliable. A transaction object may be required when both sides support rollback or a journal.

The correct design names which state is authoritative after each failure. “Use a transaction” is not an explanation until the transaction boundary and durability semantics are stated.

## F. Object assignment audit

`Object.assign` reads enumerable source values, executes getters, ignores non-enumerable methods, includes enumerable symbols, and installs ordinary data properties. It has no collision policy beyond later overwrite. Private-field methods copied to foreign receivers remain branded to their declaring class and can fail.

If copying remains required, use complete descriptors and an explicit duplicate policy. In most application architecture, nested composition is clearer.

## G. Laboratory

A complete document design keeps search index, tag policy, and version history as separate capabilities. The document owns orchestration and returns read-only snapshots. The renderer receives only a read view. Tests replace each capability independently.

## H. ObjectAtlas transfer

The atlas should be the authority for graph membership and parent-child consistency. Nodes should not reach into storage. The codec should not mutate live graph state. Rendering should not receive mutation capability. The application layer should coordinate candidate state and save behavior.

## I. Reconstruction standard

A complete answer names whether behavior is linked or copied, where state lives, and who owns lifecycle. It does not use “composition” as a slogan detached from authority.
