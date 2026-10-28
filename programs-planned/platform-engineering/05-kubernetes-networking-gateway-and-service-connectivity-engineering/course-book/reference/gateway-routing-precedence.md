# Gateway routing precedence review

Test a matrix, not one URL:

```text
listener hostname
Route hostname
request authority
path exact/prefix
method/header constraints
backend reference
```

Confirm:

- listener and Route hostname intersection;
- most-specific path behavior;
- conflict resolution independent of file order;
- unknown hostname/path rejection;
- parent-specific attachment status;
- reference resolution and generation freshness;
- backend readiness and policy.

A broad catch-all Route can make positive tests pass while stealing traffic from a more specific intended owner. Negative host/path cases are required release evidence.
