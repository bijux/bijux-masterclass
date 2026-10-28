# Contract release fixtures

These descriptions are executable compatibility exercises, not decorative archives.

| Directory | Purpose |
|---|---|
| `v1.0/` | Previously published consumer baseline. |
| `v1.1/` | Compatible release that adds a webhook-subscription operation and an optional project field. |
| `attempted-v1.2-breaking/` | Deliberately invalid minor release: operation ID change, response removal, and a narrowed input pattern. CI must reject it. |
| `v2.0/` | Deliberate major break accompanied by migration evidence. |

Run `make releases` for the built-in comparator and `make oasdiff` for the pinned external compatibility engine.
