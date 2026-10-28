# Laboratory 13 — Receiver-Safe Command Adapter

## Product

Build a command registry that stores callable operations without losing their intended receiver or hiding invocation policy. The registry must support ordinary functions, receiver-bound methods, and explicit constructor invocation as separate operations.

The common defect is to read `service.execute` and store the resulting function value as if its later call still remembered `service`. It does not. The laboratory requires you to derive `this` from the call site and then choose a repair whose authority is narrow and testable.

## Contract

`adaptMethod(receiver, method)` returns a receiver-independent function that uses `Reflect.apply`. `CommandRegistry` registers named commands, rejects duplicates, and invokes each command exactly once. `constructWith` uses `Reflect.construct` and is not confused with ordinary invocation.

The registry must not mutate the receiver, bind unrelated methods, or catch and rewrite domain failures into success. Tests record receiver identity, argument order, call count, and thrown errors.

## Cases to explain

- direct method call;
- extracted method call;
- wrapper arrow that forwards to a method;
- `bind` with a receiver and prefix argument;
- a bound constructible function called with `new`;
- an arrow used with `new`;
- a function with an explicit TypeScript `this` parameter;
- `Reflect.apply` versus `Reflect.construct`.

## Prohibited shortcuts

Do not convert every class method into an arrow field. Do not bind the entire service at construction time. Do not use `any` to suppress receiver diagnostics. Do not catch a `TypeError` and retry with a guessed receiver.

## Transfer

Add command middleware that receives a receiver-independent `next` function. State whether middleware may invoke `next` zero, one, or multiple times and enforce that policy with tests.
