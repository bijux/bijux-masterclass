<a id="top"></a>

# Mk Layer Guide

Deep Dive Make uses layered `mk/*.mk` files on purpose. This page explains what each
layer owns so the repository stays legible as the learner moves beyond the top-level
Makefile.

Use it when `capstone/mk/` feels like a pile of fragments instead of an intentional
architecture.

---

## Reading Order

Read the layers in this order:

1. `capstone/mk/contract.mk`
2. `capstone/mk/common.mk`
3. `capstone/mk/macros.mk`
4. `capstone/mk/objects.mk`
5. `capstone/mk/stamps.mk`
6. `capstone/mk/rules_eval.mk`

That order moves from platform contract, to shared policy, to reusable helpers, to graph
discovery, to modeled hidden inputs, and finally to optional rule generation.

[Back to top](#top)

---

## Layer Responsibilities

| File | Responsibility |
| --- | --- |
| `contract.mk` | declares the GNU Make version floor and feature probes that define the repository boundary |
| `common.mk` | centralizes shared flags and deterministic compilation policy |
| `macros.mk` | provides safe shell-snippet helpers used by public rules |
| `objects.mk` | discovers source files deterministically and maps them into build artifacts |
| `stamps.mk` | models hidden inputs and non-file boundaries without breaking `make -q all` |
| `rules_eval.mk` | contains the quarantined optional `$(eval)` demo rather than mixing it into the main build |

[Back to top](#top)

---

## What Each Layer Must Not Do

| File | Boundary to protect |
| --- | --- |
| `contract.mk` | should not hide operational behavior or regular build rules |
| `common.mk` | should not smuggle platform-specific surprises into artifact meaning |
| `macros.mk` | should not become an undocumented public API by itself |
| `objects.mk` | should not mix discovery policy with unrelated shell logic |
| `stamps.mk` | should not reintroduce `FORCE` into the transitive closure of `all` |
| `rules_eval.mk` | should not become required for the normal build path |

[Back to top](#top)

---

## Best Companion Pages

Use these pages with this guide:

* [`capstone-file-guide.md`](capstone-file-guide.md)
* [`capstone-map.md`](capstone-map.md)
* [`proof-matrix.md`](proof-matrix.md)

[Back to top](#top)
