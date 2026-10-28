# Module 3 Solutions

## A. Closures

The first prints `4`; the closure reads the current captured binding. The `while` example prints `[3, 3, 3]` because every closure reads the same outer `index` after the loop. Capture a new `const current = index` inside each iteration and close over `current`.

## B. `this`

The detached call has no receiver in strict ESM code, so `this` is `undefined`. One repair is `const add = meter.add.bind(meter)`. Another is a pure function `add(value, amount)` returning the next value, with the caller explicitly updating state. The second often makes mutation authority clearer.

## C. Contract

`selectFirst` calls the predicate synchronously in source order, at most once per inspected element, stops after the first truthy result, does not retain the callback, does not mutate the array, and allows thrown errors to propagate. The returned item is the original reference, not a copy.

## D. Clock

Branch on the typed command before invoking the dependency. A fake clock increments a counter and returns a fixed date. Tests assert zero calls for `list` and one for `start`.

## E–F. Design notes

The budget owns invocation count. It should not catch and retry arbitrary callback errors unless the contract says effects are repeatable. StudyLedger accepts time as a value in transitions. Equal ledger, command, and timestamp inputs should produce equal results.

## G. Readiness answer

Closures retain lexical access, not frozen snapshots. Declarations and expressions initialize differently. Ordinary functions receive a call-site receiver; arrows do not. Types describe callable shape, while product documentation describes count and lifetime. Injection moves nondeterministic acquisition to a boundary that tests can replace.

## Extended solution

The original retry type leaves unanswered timing, count at zero, which failures trigger retry, whether results are cached, whether calls overlap, whether the last error is preserved, and whether the callback is retained. A synchronous design can require `attempts` to be positive, call in a loop, return on first success, and rethrow the final error after exactly N failures.

The extracted `save` method loses its receiver. One repair is `await saver.save('{}')`, preserving method invocation. Another is `const save = saver.save.bind(saver)`, creating a bound callable. Refactoring `save` to close over `path` and require no receiver can be cleaner if the API does not conceptually expose an object method.

`forEach` ignores returned promises. Sequential ownership uses `for...of` with await. Concurrent ownership uses `await Promise.all(items.map(save))`. The StudyLedger clock is injected because call count and chosen instant are product-relevant; patching global Date affects unrelated code and can conceal an accidental global read.
