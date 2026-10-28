# Module 17 Reasoned Solutions

## A. Iterable classification

An array is a reusable iterable and produces fresh iterators. An array iterator is an iterable iterator and is one-shot. A generator function is callable but not itself an iterable sequence. Calling it creates a generator object, which is a one-shot iterable iterator. A custom object returning a fresh generator is reusable. An object with only `next` is an iterator-like value but not directly consumable by `for...of` because it lacks the iterable protocol.

## B. Manual iterator

The iterator must store current position and terminal state. It validates a positive step, checks whether the current value is below the end, and checks safe arithmetic before advancing. Once terminal, it always returns `{ done: true, value: undefined }`.

The reusable wrapper stores only range configuration and creates a new iterator in `[Symbol.iterator]`. Returning `this` from the wrapper would make it one-shot and conflate configuration with traversal state.

## C. Generator control trace

The first `next` starts execution and yields `1`; its argument is ignored. The next supplied number becomes `first`. The following yield is `first + 1`. A later supplied number becomes `second`, then the generator returns the string and executes `finally` before terminal completion.

Calling `return` enters completion and executes `finally`. Calling `throw` injects an exception at the suspended yield; because the body does not catch it, `finally` runs and the throw escapes.

## D. Early close

Complete consumption reaches normal completion and runs `finally`. `break`, loop-body throw, and explicit `return` invoke iterator closing and run `finally`. A consumer that manually calls `next` and abandons the iterator does not automatically close it; cleanup then depends on later reachability and should not be treated as deterministic.

The principled design documents ownership and provides explicit close when manual consumption is supported.

## E. Traversal orders

Preorder yields before descendants, postorder after descendants, and breadth-first by levels. A general graph needs a visited policy. Once-per-node uses a set and is suitable for analysis. Once-per-path preserves path multiplicity but can grow exponentially and needs cycle/path guards.

## F. Mutation policy

Live traversal may include or omit changes depending on timing and data structure. Snapshot traversal must capture enough structure to make later mutations irrelevant. Fail-fast traversal compares a revision and rejects once structural state changes. ObjectAtlas chooses fail-fast structural traversal because it detects mixed-version walks without copying the entire graph. Label changes may remain allowed if labels do not affect traversal structure and the contract states that yielded views are live or snapshotted.

## G. Laboratory

A complete hierarchy walker gives each traversal a fresh state object, detects cycles, preserves child order, proves early-close cleanup, and distinguishes structural revision from unrelated metadata revision.

## H. ObjectAtlas transfer

The default iterator should be fresh and deterministic. Named traversal methods should share one internal graph-reading abstraction without changing order semantics. Revision tests must fail before yielding another value after structural mutation.

## I. Reconstruction standard

A complete answer describes traversal as a state machine and includes cleanup and retention. It does not treat generator syntax as the design itself.
