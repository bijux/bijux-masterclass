# Resilience and Control-Flow Wrappers

The moment a wrapper starts retrying, timing out, or rate-limiting, it is no longer only
changing what happens around a call. It is changing whether, when, and how often the
underlying function gets to run.

That makes these decorators especially important to review honestly.

## The sentence to keep

When reviewing a resilience wrapper, ask:

> how does this decorator change control flow, failure behavior, or timing at the call
> boundary?

That is the right question because these wrappers do not merely observe calls. They govern
them.

## Retry changes failure semantics

A retry decorator can be useful, but it is already a policy engine:

- it decides which exceptions count as retryable
- it decides how many attempts are allowed
- it decides how long to sleep between attempts
- it decides when the failure becomes final

That is far more than "just wrapping a function."

```python
import functools
import time


def retry(exceptions=(Exception,), max_attempts=3, initial_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
                    delay *= 2

        return wrapper

    return decorator
```

This wrapper now owns a clear call-policy contract. That is why it belongs in Module 05,
not the thin-wrapper module.

## Timeout changes waiting semantics, not only behavior

A timeout wrapper changes the relationship between caller and work:

- the caller stops waiting after a threshold
- the wrapped work may still continue depending on implementation strategy
- failure now includes timeout-specific behavior, not only the original function's exceptions

That is a major semantic change, even if the wrapper code still looks compact.

## Rate limiting changes scheduling semantics

Rate limiting governs when calls are allowed to happen at all:

- calls may block and wait
- calls may be rejected
- state about prior calls now shapes later calls

At that point the decorator is governing traffic, not just transforming one callable in
place.

That is exactly why policy-heavy decorators need slower review than thin wrappers.

## One picture of the control-flow change

```text
Thin wrapper:
  caller -> wrapper -> original function -> result

Resilience wrapper:
  caller -> policy gate -> maybe wait / retry / abort -> original function -> maybe repeat
```

That diagram is the difference between observation and governance.

## Single-threaded teaching boundaries matter here

The examples in this module stay synchronous and single-threaded on purpose.

That means:

- no async cancellation model
- no cross-thread state coordination
- no distributed rate-limit storage

Those limits are important because they keep the design cost visible. A wrapper that is
already subtle in single-threaded sync code becomes even more expensive under concurrency.

## Backoff, jitter, and quotas are policy knobs

Small configuration details matter a lot:

- exponential backoff changes retry pacing
- jitter changes herd behavior under failure
- quota windows change fairness and burst behavior

These are policy decisions, not harmless implementation details. If the wrapper owns them,
the review has to own them too.

## These wrappers should preserve non-policy surfaces

Even when semantics change, the wrapper should still preserve what it can:

- callable metadata
- names and docs
- signature transparency when the wrapper claims to preserve the original call contract

This is one of the recurring lessons of the course: stronger policy does not excuse weaker
observability.

## Review rules for resilience wrappers

When reviewing retry, timeout, or rate-limit decorators, keep these questions close:

- what control-flow rule does the wrapper now own?
- which exceptions or timing outcomes are now different from the original callable?
- what state or timing knobs shape later calls?
- are concurrency or async limitations being documented honestly?
- has this policy become large enough that an explicit object or service would be easier to review?

## What to practice from this page

Try these before moving on:

1. Implement a bounded retry decorator and explain exactly when it stops retrying.
2. Write down one timeout implementation caveat for sync code.
3. Compare one rate-limit decorator to an explicit limiter object and explain which design would be easier to review under growth.

If those feel ordinary, the next step is annotation-aware runtime behavior, where the
wrapper begins to claim knowledge about types and contracts.
