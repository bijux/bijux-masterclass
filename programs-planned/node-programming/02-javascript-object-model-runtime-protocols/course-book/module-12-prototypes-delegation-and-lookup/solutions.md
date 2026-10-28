# Module 12 Reasoned Solutions

## A. Three prototype relationships

For a normal constructor call:

```text
Object.getPrototypeOf(item) === RecordItem.prototype
Object.getPrototypeOf(RecordItem) === Function.prototype
Object.getPrototypeOf(RecordItem.prototype) === Object.prototype
```

The constructor’s `.prototype` property is an object used as the internal prototype of ordinary instances created by `new`. The function object has its own internal prototype, usually `Function.prototype`. “The prototype of the function” could incorrectly refer to either relationship; precise code and vocabulary avoid that ambiguity.

## B. Read trace with receiver

Lookup begins at `rectangle`, continues to `middle`, then finds the accessor on `base`. The receiver remains `rectangle`. The getter therefore reads `rectangle.width` and `rectangle.height`, producing `20`.

If forwarding substituted `base` as receiver, the getter would read dimensions from `base`, not from the original object. The principled proxy forwarding form is commonly `Reflect.get(target, key, receiver)` because it preserves the receiver from the intercepted operation. Even that form has caveats around private fields, addressed later.

## C. Assignment classification

Representative cases:

- inherited writable data property: assignment normally creates a shadowing own property on the receiver;
- inherited setter: the setter runs with the receiver as `this` and decides where state is stored;
- inherited non-writable data property: strict assignment fails;
- inherited mutable object: `receiver.items.push(...)` mutates the single inherited array unless the receiver has its own `items` property.

The last case is not a property assignment. The read finds a shared array, and the array operation mutates that array. This distinction is why “it comes from the prototype” is not enough to predict whether state is shared.

## D. Shared mutable state repair

All three repairs can create per-instance state. A class with a private field is often the clearest public abstraction because it makes state ownership explicit and prevents accidental external replacement. `Object.create` is appropriate when direct delegation is the teaching or product requirement. A constructor function is semantically valid but offers less clarity than class syntax for new code unless compatibility or function-level metaprogramming matters.

A weak repair clones `queueBehavior` with spread. That duplicates method values and still relies on a copy convention rather than establishing a stable construction boundary.

## E. Pollution-resistant merge

A principled implementation first requires a non-null object, then examines complete own descriptors. Accessor properties are rejected rather than executed. Keys are validated and normalized before insertion into a fresh null-prototype record. A `Set` tracks normalized names to reject semantic duplicates.

Spread is not sufficient because it:

- reads enumerable property values and may invoke getters;
- ignores non-enumerable own properties without explaining the policy;
- does not validate key grammar or values;
- does not detect normalized duplicates;
- creates an ordinary object with a prototype unless the destination is chosen explicitly.

## F. `instanceof` counterexample

`Object.create(ClassName.prototype)` places the prototype object in the chain, so ordinary `instanceof` succeeds. It does not execute the constructor and therefore does not install private fields. Calling a method that accesses `#state` fails the private-brand check.

A public predicate should follow the domain boundary. For trusted in-process instances, a class-provided brand check may be useful. For parsed or cross-realm external data, validate the data representation. `instanceof` can be one signal, but it is not equivalent to complete domain validity.

## G. Laboratory

A correct policy catalog stores stateless behavior on a shared prototype and gives each policy its own rule data. Overrides become own properties with tested shadowing. Open-ended option keys use a null-prototype dictionary or `Map`. No shared mutable arrays live on the prototype.

## H. ObjectAtlas transfer

Class methods naturally live on `AtlasNode.prototype`. The node’s own private fields carry state. Attribute keys are kept outside the ordinary prototype namespace. Prototype-chain inspection uses `Object.getPrototypeOf` and descriptors rather than reading arbitrary properties.

Changing a plain object’s prototype is a weak deserialization repair. It creates method lookup but does not establish private fields, validated identifiers, parent-child invariants, or canonical attribute storage. Reconstruct through the public factory and validate every stored field.

## I. Reconstruction standard

A strong explanation traces both lookup and receiver. It distinguishes method sharing from state sharing and treats `instanceof` as a prototype-chain relation rather than a certificate that all construction invariants hold.
