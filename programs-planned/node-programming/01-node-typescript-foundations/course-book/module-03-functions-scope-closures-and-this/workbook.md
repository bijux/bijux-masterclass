# Module 3 Workbook

## A. Closure prediction

Predict the outputs:

```ts
let value = 1;
const read = () => value;
value = 4;
console.log(read());
```

```ts
const readers: Array<() => number> = [];
let index = 0;
while (index < 3) {
  readers.push(() => index);
  index += 1;
}
console.log(readers.map((reader) => reader()));
```

Then rewrite the second example to capture a distinct value per iteration.

## B. `this` diagnosis

Explain why this fails and provide two principled repairs:

```ts
const meter = {
  value: 0,
  add(amount: number) {
    this.value += amount;
  },
};

const add = meter.add;
add(3);
```

One repair may preserve method semantics; the other should eliminate hidden receiver dependence.

## C. Callback contract

Design the complete contract for:

```ts
function selectFirst<T>(items: readonly T[], predicate: (item: T) => boolean): T | undefined;
```

State count, order, timing, storage, mutation, and thrown-error behavior.

## D. Clock injection

Implement an application function that calls a supplied clock exactly once only when handling `start`. It must not call the clock for `list`. Test call count without using timers.

## E. Independent laboratory

Complete [Callback Budget](../../labs/module-03-callback-budget/README.md). Its callback may be invoked at most a configured number of times and must stop after the first accepted result.

## F. StudyLedger transfer

Add `Clock`, ID allocation, session creation, and start transition. Domain functions must be deterministic and serializable. Write one test proving two equal inputs produce deeply equal outputs.

## G. Reconstruction

Explain:

- captured binding versus copied value;
- function declaration versus initialized function expression;
- ordinary function `this` versus arrow lexical `this`;
- callback type versus invocation policy;
- why effect injection belongs at an application boundary.

## H. Callable-contract clinic

A utility has this signature:

```ts
function retry<T>(operation: () => T, attempts: number): T
```

List at least six unanswered behavioral questions. Then redesign the signature and documentation for a synchronous operation that may be invoked up to `attempts` times only after thrown errors. State whether the last error is preserved and whether attempts may be zero.

Diagnose the bug:

```ts
const saver = {
  path: 'ledger.json',
  async save(text: string) {
    await writeFile(this.path, text);
  },
};
const save = saver.save;
await save('{}');
```

Give two principled repairs and compare their API consequences.

## I. Promise-returning callback trap

Predict the completion and rejection behavior of `items.forEach(async item => save(item))`. Rewrite it once for sequential saving and once for concurrent start with one owning promise.

## J. StudyLedger checkpoint

Inject a clock into the application layer. Write tests proving `summary` calls it zero times and `plan` calls it exactly once. Explain why patching global `Date` is weaker evidence.
