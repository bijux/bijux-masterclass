# Module 14 Reasoned Solutions

## A. Surface inspection

The constructor object owns static `count` along with built-in function properties and `prototype`. `Example.prototype` owns the getter descriptor `total`, method `method`, and `constructor`. An instance owns `publicField`. The private field is stored through the private-name mechanism and is absent from ordinary own-key reflection.

A correct explanation also notes that class methods and accessors are non-enumerable prototype properties, while a public field is an enumerable own data property under ordinary class-field semantics.

## B. TypeScript privacy comparison

TypeScript `private` prevents typed access through the declared API, but it is not an ECMAScript private name. Depending on emission, the runtime member remains reachable as an ordinary property. `#value` triggers a runtime brand check and cannot be reached through string or symbol reflection.

A weak conclusion says `#private` makes secrets secure. Public methods, logs, snapshots, process inspection, and deliberate leaks remain possible. The guarantee is encapsulation from ordinary language-level property access.

## C. Initialization trace

The order is:

```text
before super
base field
base constructor
derived field
after super
```

Derived `this` is unavailable before `super`. Base fields initialize before the base constructor body. Derived fields initialize after `super` returns and before the remaining derived constructor statements.

If the base initializer calls an overridden method that accesses a derived private field, the call happens before the derived private field is installed. The principled repair removes virtual dispatch from construction.

## D. Constructor hazard repair

A static factory can:

1. validate input;
2. construct a complete base object without overridable calls;
3. call a post-construction method;
4. return only after the object is ready.

Composition can supply a collaborator as ordinary data, establish all state, then invoke it from a normal method. Both approaches remove partially initialized dynamic dispatch.

Optional fields are a weak repair because they widen every later state to include an invalid construction-only phase.

## E. Instance independence

Public field initializers such as `items: string[] = []` and `index = new Map()` run per instance. Prototype containers are single shared identities reached by every instance that lacks a shadowing own property. Tests should compare both semantic contents and `===` identity.

## F. Class or factory decision

A validated identifier can use a small class or branded plain value; the choice depends on runtime identity and methods. A stateful bank account earns a class with private state. Pure formatting functions need no object. A replaceable collaborator is usually an interface-shaped plain object. Persisted JSON is plain data and must be validated before reconstruction. A resource may use a class if identity and close-state invariants matter.

The principle is authority and lifecycle, not “objects with nouns should be classes.”

## G. Laboratory

The bank must validate the complete transfer before mutating either account. A static parse or open factory separates raw input from valid instances. Tests must prove private brand behavior, independent state, and failure atomicity.

## H. ObjectAtlas transfer

`AtlasNode` should copy or freeze outward snapshots rather than expose private arrays or dictionaries. Reconstruction validates a plain record and invokes the legitimate constructor/factory. A counterfeit object with the right prototype may satisfy `instanceof` but fails any method that touches a private field.

## I. Reconstruction standard

A complete answer distinguishes class syntax layers and treats initialization order as a correctness property. It does not use inheritance merely for method reuse and does not confuse stored data with a live branded instance.
