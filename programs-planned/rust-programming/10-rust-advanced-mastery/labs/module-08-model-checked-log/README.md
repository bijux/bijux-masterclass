# Laboratory 8 — Model-Checked Log

[Course 10](../../README.md) · [Common laboratory method](../../../START_HERE.md#laboratory-method)

## Product

Build a compact mutation engine and an independent model, then exhaustively compare them across every operation sequence within a bounded state space. The engine should use a representation different from the model so the test does not reproduce the same defect twice.

The starter supplies a `BTreeMap` model for `Put`, `Remove`, and `Clear`. Implement the system under test with a sorted vector or another deliberately different representation. Compare state after every operation prefix, not only after the complete sequence.

### State space

Choose and document finite bounds for:

- keys;
- values;
- operation alphabet;
- maximum sequence length;
- optional capacity or transaction size;
- failure injection points.

The explorer must produce the shortest divergent prefix and show both states. A raw assertion after millions of cases is not a useful diagnostic.

### Engine invariants

For a sorted-vector implementation:

- keys are unique;
- items remain in key order;
- replacing a key does not create a duplicate;
- removing an absent key is a documented no-op or typed error;
- clear leaves the canonical empty state;
- failure does not partially reorder or mutate unrelated entries.

Add direct unit tests for representation invariants as well as model comparison.

### Independence review

List every helper shared by the model and engine. Shared domain operation types are acceptable; shared mutation algorithms are not. If both sides call one `apply` function, the comparison proves only that a function equals itself.

### Transfer

Add a bounded all-or-nothing transaction operation. The model may clone its small map; the engine should use a candidate representation or rollback strategy appropriate to its design. Enumerate transactions containing success, duplicate keys, removal, and capacity failure. Compare both the result and the post-failure state after every prefix.

### Using the reference

Complete the explorer from `starter/` before inspecting `solution/`. The reference demonstrates recursive enumeration but is intentionally compact. Improve its failure report and state-space accounting rather than copying its formatting.

### Completion standard

You can explain why the model is simpler and independent, why the state space is finite, and why prefix comparison localizes the first divergence. If the explorer can consume unbounded memory or time from an input value, its verification claim is incomplete.
