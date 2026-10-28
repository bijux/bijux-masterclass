# Module 14 Workbook

Draw four surfaces for each class exercise: constructor object, prototype object, instance own properties, and private state. Do not place every member inside one imaginary class box.

## A. Surface inspection

For this class, predict where every member appears:

```ts
class Example {
  static count = 0;
  publicField = 1;
  #privateField = 2;

  get total(): number {
    return this.publicField + this.#privateField;
  }

  method(): number {
    return this.total;
  }
}
```

List the output categories for:

```ts
Reflect.ownKeys(Example);
Reflect.ownKeys(Example.prototype);
Reflect.ownKeys(new Example());
```

Explain why private state appears in none of them.

## B. TypeScript privacy comparison

Implement one class with `private value` and one with `#value`. Compile and inspect emitted JavaScript under the course target. Then write runtime code that attempts reflective access. State which guarantees come from the checker and which from the runtime.

## C. Initialization trace

Predict the exact log order:

```ts
class Base {
  baseField = this.log('base field');

  constructor() {
    this.log('base constructor');
  }

  log(message: string): string {
    console.log(message);
    return message;
  }
}

class Derived extends Base {
  derivedField = this.log('derived field');

  constructor() {
    console.log('before super');
    super();
    console.log('after super');
  }
}
```

Then add an override of `log` that reads a derived private field and explain the failure.

## D. Constructor hazard repair

Repair a base class whose constructor calls an overridable `initialize()` method. Provide two designs:

1. static factory that constructs and then initializes;
2. composition in which a collaborator is supplied and invoked only after state is complete.

Explain why making fields optional is a weak repair.

## E. Instance independence

Design a class containing an array and a map. Prove that two instances do not share them. Then intentionally place the containers on a prototype and demonstrate the failure. Connect the result to public field initialization.

## F. Class or factory decision

For each product, choose a class, closure factory, or plain object and defend the choice:

- immutable validated identifier;
- stateful bank account with invariant-preserving transitions;
- two pure formatting functions;
- one configurable collaborator with no identity;
- a persisted record reconstructed from JSON;
- a resource requiring explicit close.

## G. Independent laboratory

Complete [Private Counter Bank](../../labs/module-14-private-counter-bank/README.md). It requires private balances, safe transfers, full validation before publication, static factories, and tests for brand and instance independence.

## H. ObjectAtlas transfer

Implement `AtlasNode` with private state and public snapshots. Add tests for:

- valid and invalid construction;
- independent child arrays and attribute records;
- no mutable-container escape;
- private-brand failure on a counterfeit prototype object;
- round-trip reconstruction through `fromRecord`;
- no overridable call during construction.

## I. Reconstruction and defense

Without notes, explain:

- class constructor/static side versus instance side;
- prototype methods versus own fields;
- runtime private brand;
- TypeScript-private limitations;
- base and derived initialization order;
- constructor dispatch hazards;
- inheritance versus method sharing;
- why a plain persistence record should not be treated as a live class instance.
