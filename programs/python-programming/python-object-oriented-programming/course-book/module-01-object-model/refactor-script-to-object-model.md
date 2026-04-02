# Refactor 0 – Script → Object Model with Correct Identity/Data-Model Semantics


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Object Model"]
  page["Refactor 0 – Script → Object Model with Correct Identity/Data-Model Semantics"]
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

## Purpose

This core applies Module 1 principles to refactor a naïve monitoring script—built on dicts and lists—into an object model with `Metric` (value type: content-based equality and hashing), `Rule` (entity type: identity equality), and `Alert` (entity type: identity equality). The refactor treats values as immutable to enable safe sharing of instances and controlled ownership of collections, resolves unhashability, and preserves behavioral equivalence. Implement minimal data-model methods (`__eq__`, `__hash__`, `__repr__`) to support these semantics, drawing on identity (M01C01), attributes (M01C02), invariants (M01C03), encapsulation (M01C04), equality/hashing (M01C05), and aliasing avoidance (M01C06).

## 1. Baseline Script: Demonstrating Semantic Failures

The script fetches metrics as dicts, attaches them to a rule dict, and evaluates alerts. It functions but fails under Module 1 scrutiny: shared lists enable aliasing; dicts are unhashable, preventing container use; logical duplicates produce redundant alerts without deduplication.

```python
# naive_monitor.py

def fetch_metrics():
    return [
        {"timestamp": 1, "name": "cpu", "value": 0.8},
        {"timestamp": 2, "name": "cpu", "value": 0.9},
        {"timestamp": 3, "name": "mem", "value": 0.7},
        {"timestamp": 2, "name": "cpu", "value": 0.9},  # Logical duplicate
    ]

def build_rule(name, threshold):
    return {"name": name, "threshold": threshold, "metrics": []}

def attach_metrics(rule, metrics):
    rule["metrics"] = metrics  # Aliasing: shared mutable list

def evaluate(rule):
    alerts = []
    for m in rule["metrics"]:
        if m["value"] > rule["threshold"]:
            alerts.append({"rule": rule["name"], "metric": m})  # Nested dicts
    return alerts

if __name__ == "__main__":
    metrics = fetch_metrics()
    rule = build_rule("cpu_high", 0.85)
    attach_metrics(rule, metrics)
    alerts = evaluate(rule)
    print("Alerts:", alerts)
```

**Output**:  
Alerts: [{'rule': 'cpu_high', 'metric': {'timestamp': 2, 'name': 'cpu', 'value': 0.9}}, {'rule': 'cpu_high', 'metric': {'timestamp': 2, 'name': 'cpu', 'value': 0.9}}]

**Exposed Failures**:
- **Aliasing (M01C06)**: Post-attachment mutation propagates:  
  ```python
  metrics.append({"timestamp": 999, "name": "disk", "value": 0.95})
  print(len(evaluate(rule)))  # Now 3, unexpectedly
  ```
- **Unhashability**: Dicts cannot enter sets:  
  ```python
  set(metrics)  # TypeError: unhashable type: 'dict'
  set(alerts)   # TypeError: unhashable type: 'dict'
  ```
- **No Deduplication (M01C05)**: Logical duplicates yield separate alerts; no consistent equality.

## 2. Refactored Object Model: Implementing Disciplined Semantics

Use `__slots__` for attributes (M01C02). `Metric` is immutable via read-only properties and a mutation guard, bypassed during construction with `object.__setattr__`. `Rule` encapsulates metrics; both it and `Alert` rely on default object equality/hashing for identity semantics—no overrides needed. Entities inherit Python's default object behavior, where equality is by identity (`x == y` iff `x is y`) and hashing uses object ID (M01C01, M01C05). Two `Rule` instances with the same name and threshold are distinct entities, and sets/dicts will treat them as different keys.

### 2.1 Metric: Value Type

Content-based equality and hashing enable deduplication and container use. Immutability is enforced post-construction to prevent hash violations.

```python
from __future__ import annotations

class Metric:
    __slots__ = ("_timestamp", "_name", "_value")

    def __init__(self, timestamp: int, name: str, value: float) -> None:
        if not 0 <= value <= 1:
            raise ValueError("Value must be between 0 and 1")
        # Bypass guard during construction
        object.__setattr__(self, "_timestamp", timestamp)
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_value", value)

    def __setattr__(self, name: str, value: object) -> None:
        # Enforce immutability for value fields (M01C06)
        if name in ("_timestamp", "_name", "_value"):
            raise AttributeError(f"{name} is immutable; create a new Metric instance")
        object.__setattr__(self, name, value)

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> float:
        return self._value

    def __eq__(self, other):
        if not isinstance(other, Metric):
            return NotImplemented
        return (
            self._timestamp,
            self._name,
            self._value,
        ) == (
            other._timestamp,
            other._name,
            other._value,
        )

    def __hash__(self):
        return hash((self._timestamp, self._name, self._value))

    def __repr__(self):
        return f"Metric(ts={self.timestamp!r}, name={self.name!r}, value={self.value!r})"
```

### 2.2 Rule and Alert: Entity Types

```python
class Rule:
    __slots__ = ("_name", "_threshold", "_metrics")

    def __init__(self, name: str, threshold: float) -> None:
        if not 0 <= threshold <= 1:
            raise ValueError("Threshold must be between 0 and 1")
        self._name = name
        self._threshold = threshold
        self._metrics: list[Metric] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def threshold(self) -> float:
        return self._threshold

    def attach_metric(self, metric: Metric) -> None:
        if not isinstance(metric, Metric):
            raise TypeError("Expects Metric instance")
        self._metrics.append(metric)  # Reference to immutable value; aliasing safe

    def evaluate(self) -> list[Alert]:
        return [
            Alert(self, m)
            for m in self._metrics
            if m.value > self._threshold
        ]

    def __repr__(self):
        return f"Rule(name={self.name!r}, threshold={self.threshold!r})"


class Alert:
    __slots__ = ("_rule", "_metric")

    def __init__(self, rule: Rule, metric: Metric) -> None:
        self._rule = rule
        self._metric = metric

    @property
    def rule(self) -> Rule:
        return self._rule

    @property
    def metric(self) -> Metric:
        return self._metric

    def __repr__(self):
        return f"Alert(rule={self.rule.name!r}, metric={self.metric!r})"
```

## 3. Refactored Flow: Equivalence with Safety

```python
# refactored_monitor.py
from naive_monitor import fetch_metrics

def build_cpu_rule():
    return Rule("cpu_high", 0.85)

def attach_metrics(rule: Rule, metrics: list[Metric]):
    for m in metrics:
        rule.attach_metric(m)

if __name__ == "__main__":
    raw = fetch_metrics()
    metrics = [Metric(r["timestamp"], r["name"], r["value"]) for r in raw]
    # Optional: unique_metrics = set(metrics)  # Deduplication via value semantics
    rule = build_cpu_rule()
    attach_metrics(rule, metrics)  # Preserves duplicates for equivalence
    alerts = rule.evaluate()
    print("Alerts:", alerts)
```

**Output**:  
Alerts: [Alert(rule='cpu_high', metric=Metric(ts=2, name='cpu', value=0.9)), Alert(rule='cpu_high', metric=Metric(ts=2, name='cpu', value=0.9))]

**Resolutions**:
- `set(metrics)` yields 3 items (deduplication available via value semantics).
- Appending to raw post-conversion: no effect on alerts.
- `set(alerts)` succeeds (2 distinct entities).
- Structured `__repr__` aids debugging.

## 4. Tests: Contract Verification

Assert semantics via public interfaces only.

```python
# test_refactored_model.py
import unittest
from refactored_model import Metric, Rule, Alert
from naive_monitor import fetch_metrics
from refactored_monitor import build_cpu_rule, attach_metrics

class TestRefactoredSemantics(unittest.TestCase):
    def setUp(self):
        raw = fetch_metrics()
        self.metrics = [Metric(r["timestamp"], r["name"], r["value"]) for r in raw]
        self.rule = build_cpu_rule()
        attach_metrics(self.rule, self.metrics)
        self.alerts = self.rule.evaluate()

    def test_baseline_equivalence(self):
        self.assertEqual(len(self.alerts), 2)
        self.assertEqual(self.alerts[0].metric.name, "cpu")

    def test_metric_value_semantics(self):
        m1 = Metric(2, "cpu", 0.9)
        m2 = Metric(2, "cpu", 0.9)
        m3 = Metric(3, "mem", 0.7)
        self.assertEqual(m1, m2)
        self.assertEqual(hash(m1), hash(m2))
        self.assertNotEqual(m1, m3)
        self.assertEqual(len({m1, m2, m3}), 2)

    def test_entity_identity_semantics(self):
        rule1 = Rule("cpu_high", 0.85)
        rule2 = Rule("cpu_high", 0.85)
        self.assertIsNot(rule1, rule2)
        self.assertNotEqual(rule1, rule2)

        alert1 = Alert(rule1, self.metrics[1])
        alert2 = Alert(rule1, self.metrics[1])
        self.assertIsNot(alert1, alert2)
        self.assertNotEqual(alert1, alert2)
        self.assertEqual(len({alert1, alert2}), 2)

    def test_aliasing_isolation(self):
        fresh_rule = build_cpu_rule()
        external_metrics = self.metrics.copy()
        attach_metrics(fresh_rule, external_metrics)
        external_metrics.append(Metric(999, "disk", 0.95))
        alerts = fresh_rule.evaluate()
        self.assertEqual(len(alerts), 2)
        self.assertFalse(any(a.metric.timestamp == 999 for a in alerts))

    def test_container_safety(self):
        metric_set = set(self.metrics)
        self.assertEqual(len(metric_set), 3)
        alert_dict = {a: a.metric.value for a in self.alerts}
        self.assertEqual(len(alert_dict), 2)
        self.assertEqual(list(alert_dict.values()), [0.9, 0.9])

    def test_metric_immutability(self):
        m = Metric(1, "cpu", 0.9)
        # Deliberately accessing private field to verify guard (violates encapsulation for test)
        with self.assertRaises(AttributeError):
            m._value = 0.1
```

**Execution**: All tests pass, confirming resolutions.

## Practical Guidelines

- Audit baselines for unhashability and aliasing; convert values first.
- Use private fields and guards for immutability; defaults for entity identity.
- Test equality/hashing explicitly; expose via public properties.
- Refactor incrementally, verifying equivalence.

## Exercises for Mastery

1. Add `__lt__` to `Metric` (timestamp-based); test `sorted(set(metrics))`.
2. Create anemic dict-based `Rule`; compare set inclusion failures.
3. Add `Rule.get_metrics_count()`; test post-mutation isolation.

This refactor establishes Module 1 semantics, enabling Module 2 responsibilities.
