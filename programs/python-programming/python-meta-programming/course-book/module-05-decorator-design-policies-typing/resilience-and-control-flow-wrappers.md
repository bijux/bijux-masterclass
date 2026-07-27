# Resilience and Control-Flow Wrappers


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Decorator Design Policies Typing"]
  page["Resilience and Control-Flow Wrappers"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

The moment a wrapper starts retrying, timing out, or rate-limiting, it is no longer only
changing what happens around a call. It is changing whether, when, and how often the
underlying function gets to run.

That makes these decorators especially important to review honestly.
They are often the first wrappers in a codebase that can multiply side effects while
still presenting a deceptively small call surface.

## The sentence to keep

When reviewing a resilience wrapper, ask:

> how does this decorator change control flow, failure behavior, or timing at the call
> boundary?

That is the right question because these wrappers do not merely observe calls. They govern
them.

Add one more question immediately after it:

> what side effect or failure risk becomes more likely because this wrapper is allowed to try again, wait, or refuse work?

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

It also owns an idempotency question that thin wrappers usually avoid:

- what if the underlying function already performed part of its work before failing?
- what if a second attempt is not morally the same as the first attempt?

That is why "retry" is never only a reliability keyword. It is a behavior multiplier.

## Timeout changes waiting semantics, not only behavior

A timeout wrapper changes the relationship between caller and work:

- the caller stops waiting after a threshold
- the wrapped work may still continue depending on implementation strategy
- failure now includes timeout-specific behavior, not only the original function's exceptions

That is a major semantic change, even if the wrapper code still looks compact.

It also means timeout language must stay precise. "Timed out" may mean:

- the caller stopped waiting
- the wrapper raised a timeout-specific failure
- the underlying work might still be running depending on strategy

Those are different operational stories, and the wrapper should not blur them.

## Rate limiting changes scheduling semantics

Rate limiting governs when calls are allowed to happen at all:

- calls may block and wait
- calls may be rejected
- state about prior calls now shapes later calls

At that point the decorator is governing traffic, not just transforming one callable in
place.

That is exactly why policy-heavy decorators need slower review than thin wrappers.

Rate limits also expose a fairness question:

- who waits?
- who gets rejected?
- which earlier calls now shape later callers?

That is scheduling policy, not only defensive wrapping.

## One picture of the control-flow change

```text
Thin wrapper:
  caller -> wrapper -> original function -> result

Resilience wrapper:
  caller -> policy gate -> maybe wait / retry / abort -> original function -> maybe repeat
```

That diagram is the difference between observation and governance.

Use it as a repair prompt when a review comment says "the decorator just retries." The
diagram shows that the wrapper has inserted a policy gate between caller and work.

## Single-threaded boundaries matter here

The examples in this module stay synchronous and single-threaded on purpose.

That means:

- no async cancellation model
- no cross-thread state coordination
- no distributed rate-limit storage

Those limits are important because they keep the design cost visible. A wrapper that is
already subtle in single-threaded sync code becomes even more expensive under concurrency.

This is also the right place to reject overconfident wording. A synchronous teaching
wrapper should not imply production-grade cancellation, coordination, or distributed
quota behavior that it does not actually implement.

## Backoff, jitter, and quotas are policy knobs

Small configuration details matter a lot:

- exponential backoff changes retry pacing
- jitter changes herd behavior under failure
- quota windows change fairness and burst behavior

These are policy decisions, not harmless implementation details. If the wrapper owns them,
the review has to own them too.

Use this quick comparison during review:

| Policy knob | What it changes for callers |
| --- | --- |
| retry count | how many chances the work gets before failure becomes final |
| backoff schedule | how long the caller may wait across attempts |
| jitter | how predictable or coordinated repeated attempts become |
| quota window | whether bursts are absorbed, delayed, or rejected |

## These wrappers should preserve non-policy surfaces

Even when semantics change, the wrapper should still preserve what it can:

- callable metadata
- names and docs
- signature transparency when the wrapper claims to preserve the original call contract

This is one of the recurring lessons of the course: stronger policy does not excuse weaker
observability.

Observability also includes the stopping rule. A reviewer should be able to say, in plain
language, exactly when the wrapper stops retrying, stops waiting, or stops admitting
calls.

## Common resilience-wrapper failure modes

These are the failures to catch before approving the design:

| Failure mode | Why it weakens the wrapper | Repair move |
| --- | --- | --- |
| retrying non-idempotent work blindly | later attempts may duplicate side effects | narrow the retry surface or move the policy to an explicit owner |
| hiding timeout strategy behind vague language | callers cannot tell whether work was cancelled, abandoned, or still running | state the waiting contract and the unresolved work story explicitly |
| rate limiting with invisible shared state | later callers are governed by history they cannot inspect | expose the owner or move coordination to a clearer component |
| preserving metadata while hiding stop conditions | tools can inspect the callable but humans still cannot predict wrapper behavior | document or expose the control-flow rule directly |

## Review rules for resilience wrappers

When reviewing retry, timeout, or rate-limit decorators, keep these questions close:

- what control-flow rule does the wrapper now own?
- which exceptions or timing outcomes are now different from the original callable?
- what state or timing knobs shape later calls?
- are concurrency or async limitations being documented honestly?
- has this policy become large enough that an explicit object or service would be easier to review?
- what is the exact stopping rule, and can a reviewer state it without paraphrasing vaguely?

## Exit check for this page

Before moving on, make sure you can do all of these:

- name one way a retry wrapper can multiply side-effect risk
- explain one timeout sentence that would be misleading without clarifying what still happens to the work
- describe one fairness question a rate-limit wrapper now owns
- state the wrapper's stopping rule in plain language

## What to practice from this page

Try these before moving on:

1. Implement a bounded retry decorator and explain exactly when it stops retrying.
2. Write down one timeout implementation caveat for sync code.
3. Compare one rate-limit decorator to an explicit limiter object and explain which design would be easier to review under growth.

If those feel ordinary, the next step is annotation-aware runtime behavior, where the
wrapper begins to claim knowledge about types and contracts.

## Continue through Module 05

- Previous: [Decorator Factories and Parameter Capture](decorator-factories-and-parameter-capture.md)
- Next: [Annotation-Aware Runtime Contracts](annotation-aware-runtime-contracts.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
