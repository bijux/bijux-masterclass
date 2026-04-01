# Interfaces in Python: Duck Typing, ABCs, Protocols (Prescriptive Choices)

## Purpose

This core examines Python's interface mechanisms—duck typing, Abstract Base Classes (ABCs), and typing Protocols—as prescriptive tools for defining collaboration contracts without rigid class hierarchies. Duck typing supports simple, internal collaborations where method presence implies compatibility; ABCs provide runtime enforcement for pluggable extensions, such as plugin systems; Protocols facilitate static type checking for hints without requiring inheritance. In the monitoring domain, apply these to the M02C18 rule evaluators: a `RuleEvaluator` Protocol for static hints in core use cases (satisfied structurally by both the `BaseRule` hierarchy and ad-hoc implementations); and a `RulePlugin` ABC for runtime plugin registration (a distinct role with additional metadata, using virtual subclass registration for third-party compatibility). Guideline: Assign one mechanism per collaboration role—Protocol for core domain hints, ABC for extension points—to minimize coupling and avoid mixing, while permitting supersets in layered roles (e.g., ABCs building on Protocol shapes via composition). Extending M02C18's template hierarchy, this core defines interfaces for evaluation, illustrating each mechanism's strengths and avoiding overkill, thereby reducing ad-hoc dependencies in M02C16's orchestrator.

## 1. Baseline: Ad-Hoc Collaborations and Interface Smells in the Monitoring Domain

Prior cores (M02C18) rely on concrete classes for rule evaluation, resulting in tight coupling: `RuleEvaluationUseCase` assumes specific implementations like `ThresholdRule`, failing silently if variants change. Smells include absent contracts (callers infer shapes); runtime failures (missing methods); and static oversights (mypy overlooks mismatches in `List[Any]`). Flat signatures leak internals; extensibility halts as consumers hardcode classes; testability weakens without verifiable roles. Example: `__init__(rules: List[Any])` permits invalid inputs; no documented contract or safe extension.

```python
# interface_baseline.py
from __future__ import annotations
from typing import List, Any
from semantic_types_model import RuleEvaluation, Metric, RuleType, Threshold  # Semantics

class RuleEvaluationUseCase:
    """Baseline: Assumes concrete classes; no contracts."""

    def __init__(self, rules: List[Any]):  # List[Any]; no shape guarantee
        self._rules = rules

    def evaluate(self, metrics: List[Metric]) -> List[RuleEvaluation]:
        all_evals = []
        for rule in self._rules:
            # Ad-hoc: Assumes .evaluate and .rule_type exist
            evals = rule.evaluate(metrics)  # Runtime error if missing
            all_evals.extend(evals)
        return all_evals

# Concrete rules (from M02C18; no interface)
class ThresholdRule:
    def __init__(self, threshold: Threshold):
        self._threshold = threshold

    @property
    def rule_type(self) -> RuleType:
        return RuleType("threshold")

    def evaluate(self, metrics: List[Metric]) -> List[RuleEvaluation]:
        filtered = [m for m in metrics if m.value >= self._threshold.value]
        return [RuleEvaluation(rule=self.rule_type, metric=m) for m in filtered]

class BadRule:  # Mismatch: No evaluate
    def bad_method(self, metrics):
        return []

# Usage: Coupling smell (hardcodes concretes); no safe extensibility
def create_use_case(threshold: Threshold):
    return RuleEvaluationUseCase([
        ThresholdRule(threshold),
        BadRule(),  # Silent mismatch
    ])

if __name__ == "__main__":
    metrics = [Metric(1, "cpu", 0.9), Metric(2, "cpu", 0.7)]
    use_case = create_use_case(Threshold(0.85))
    try:
        evals = use_case.evaluate(metrics)
        print(f"Evaluations: {len(evals)}")  # Runtime error on BadRule
    except AttributeError as e:
        print(f"Smell exposed: {e}")  # "'BadRule' object has no attribute 'evaluate'"
```

**Baseline Smells Exposed**:
- **Ad-Hoc Shapes**: Use case infers `evaluate`; runtime errors on mismatches.
- **Coupling Increase**: Callers bind to concretes; extensibility impeded.
- **Static Silence**: Mypy ignores `List[Any]`; no consumer hints.
- **Test Fragility**: Suites presume shapes; plugins disrupt isolation.
- **No Safe Extensibility**: New rules risk runtime issues; contracts undocumented.

These issues undermine flexibility: interfaces define roles explicitly, unlike the baseline's reliance on happenstance.

## 2. Interface Principles: Duck Typing, ABCs, Protocols—One per Role

Python's interfaces emphasize shape (duck typing) or explicitness (ABCs for runtime checks, Protocols for static verification). Guideline: Employ duck typing for low-stakes internals; ABCs for enforceable extensions; Protocols for type hints. Restrict to one mechanism per role to prevent confusion, allowing supersets for layered responsibilities (e.g., ABCs composing Protocol-satisfying objects).

### 2.1 Principles

- **Duck Typing**: Compatibility via method presence ("if it walks like a duck..."); ideal for internal, simple collaborations with runtime-only safety.
- **ABCs**: Runtime contracts through `isinstance` and virtual `register`; suited for pluggable extensions (e.g., third-party plugins).
- **Protocols**: Structural subtyping (`typing.Protocol`); enables static mypy checks without inheritance.
- **One Style per Role**: Internal evaluation? Duck + Protocol. Plugin registration? ABC. Avoid mixing; supersets permissible for extensions.
- **Trade-offs**: Duck offers flexibility but risks runtime errors; ABCs ensure enforcement at inheritance cost; Protocols provide hints sans runtime overhead.
- **Testing Differences**: Duck: Mock shapes; ABC: `isinstance` assertions; Protocol: Static error simulation via mypy.

### 2.2 Refactored Model: Interfaces for Rule Evaluators

Refactor M02C18's hierarchy: Introduce `RuleEvaluator` Protocol for static hints in core collaborations (satisfied structurally by `BaseRule` subtypes and ad-hoc classes like `LambdaRule`). Define `RulePlugin` ABC for runtime plugin registration (distinct role: adds metadata; composes Protocol-satisfying objects via adapters). Core use case relies on Protocol (duck dispatch + static checks); plugin loader enforces ABC, yielding adapters that satisfy Protocol. No mixing: Domain uses Protocol for evaluation; extensions use ABC for registration. Note: The `BaseRule` ABC provides a template method implementation that satisfies the `RuleEvaluator` Protocol structurally, enabling inheritance-based customization via hooks while adhering to the protocol's shape.

```python
# interface_model.py (domain/rules.py extension)
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol, List, runtime_checkable, Callable
from semantic_types_model import RuleType, RuleEvaluation, Metric, Threshold  # Semantics

# Protocol: Static hints for core evaluation role (structural satisfaction)
@runtime_checkable
class RuleEvaluator(Protocol):
    """Static contract: Shape for rule evaluation."""

    @property
    def rule_type(self) -> RuleType: ...

    def evaluate(self, metrics: List[Metric]) -> List[RuleEvaluation]: ...

# ABC: Runtime enforcement for plugin registration role (superset via composition)
class RulePlugin(ABC):
    """Runtime contract: Metadata + evaluation; composes RuleEvaluator."""

    @property
    @abstractmethod
    def plugin_name(self) -> str: ...

    @abstractmethod
    def get_evaluator(self) -> RuleEvaluator: ...

# Existing M02C18 hierarchy satisfies Protocol structurally (duck + static)
# Inline for self-containment (M02C18 implementation)
class BaseRule(ABC):
    """From M02C18: Template hierarchy satisfies RuleEvaluator."""

    def _normalize_metrics(self, metrics: List[Metric]) -> List[Metric]:
        return metrics[:]

    def _to_evaluations(self, metrics: List[Metric]) -> List[RuleEvaluation]:
        return [RuleEvaluation(rule=self.rule_type, metric=m) for m in metrics]

    def evaluate(self, metrics: List[Metric]) -> List[RuleEvaluation]:
        normalized = self._normalize_metrics(metrics)
        filtered = self._filter_high(normalized)
        return self._to_evaluations(filtered)

    @property
    @abstractmethod
    def rule_type(self) -> RuleType:
        """Contract: Subclass provides type."""
        pass

    @abstractmethod
    def _filter_high(self, metrics: List[Metric]) -> List[Metric]:
        """Hook: Subclass provides filter."""
        pass

class ThresholdRule(BaseRule):
    def __init__(self, threshold: Threshold):
        self._threshold = threshold

    @property
    def rule_type(self) -> RuleType:
        return RuleType("threshold")

    def _filter_high(self, metrics: List[Metric]) -> List[Metric]:
        return [m for m in metrics if m.value >= self._threshold.value]

class RateRule(BaseRule):
    def __init__(self, delta_threshold: Threshold):
        self._delta_threshold = delta_threshold

    @property
    def rule_type(self) -> RuleType:
        return RuleType("rate")

    def _filter_high(self, metrics: List[Metric]) -> List[Metric]:
        if len(metrics) < 2:
            return []
        rates = [metrics[i].value - metrics[i-1].value for i in range(1, len(metrics))]
        high_rate_indices = [i for i, rate in enumerate(rates, start=1) if rate > self._delta_threshold.value]
        return [metrics[i] for i in high_rate_indices]

# Pure duck: Structural satisfaction of Protocol (no inheritance)
class LambdaRule:
    """Ad-hoc evaluator: Satisfies RuleEvaluator structurally for duck + static."""

    def __init__(self, rule_type: RuleType, filter_fn: Callable[[List[Metric]], List[Metric]]):
        self._rule_type = rule_type
        self._filter_fn = filter_fn

    @property
    def rule_type(self) -> RuleType:
        return self._rule_type

    def evaluate(self, metrics: List[Metric]) -> List[RuleEvaluation]:
        filtered = self._filter_fn(metrics)
        return [RuleEvaluation(rule=self.rule_type, metric=m) for m in filtered]

# Plugin adapter: Composes RuleEvaluator (true adaptation)
class PluginAdapter(RulePlugin):
    """ABC implementation: Wraps evaluator with metadata."""

    def __init__(self, evaluator: RuleEvaluator, plugin_name: str):
        self._evaluator = evaluator
        self._plugin_name = plugin_name

    @property
    def plugin_name(self) -> str:
        return self._plugin_name

    def get_evaluator(self) -> RuleEvaluator:
        return self._evaluator

# Third-party example: Structural class registered virtually with ABC
class ThirdPartyRateRule:
    """External: Implements shape; registered for isinstance."""

    def __init__(self, delta_threshold: Threshold):
        self._delta_threshold = delta_threshold

    @property
    def plugin_name(self) -> str:
        return "third_party_rate"

    def get_evaluator(self) -> RuleEvaluator:
        def filter_fn(metrics: List[Metric]) -> List[Metric]:
            if len(metrics) < 2:
                return []
            rates = [metrics[i].value - metrics[i-1].value for i in range(1, len(metrics))]
            high_rate_indices = [i for i, rate in enumerate(rates, start=1) if rate > self._delta_threshold.value]
            return [metrics[i] for i in high_rate_indices]
        return LambdaRule(RuleType("rate"), filter_fn)

# Register third-party for runtime enforcement
RulePlugin.register(ThirdPartyRateRule)

# Non-compliant: Missing methods (fails ABC)
class BadPlugin(RulePlugin):
    pass  # Abstract: missing plugin_name/get_evaluator

# Factory: Domain (Protocol via duck); plugins (ABC composition)
def create_domain_rule(rule_type: str, threshold: Threshold) -> RuleEvaluator:
    if rule_type == "threshold":
        return ThresholdRule(threshold)
    elif rule_type == "rate":
        return RateRule(threshold)
    elif rule_type == "lambda_debug":
        return LambdaRule(RuleType("debug"), lambda ms: ms[:1])  # Pure duck
    raise ValueError(f"Unknown: {rule_type}")

def create_plugin(rule_type: str, threshold: Threshold, is_third_party: bool = False) -> RulePlugin:
    if rule_type == "rate":
        evaluator = create_domain_rule("rate", threshold)
        return PluginAdapter(evaluator, "rate_plugin")
    elif rule_type == "third_party_rate":
        return ThirdPartyRateRule(threshold)  # Registered ABC
    raise ValueError(f"Unknown plugin: {rule_type}")
```

**Rationale**:
- **Duck Typing**: `BaseRule` and `LambdaRule` for internals—shape enables dispatch without ceremony.
- **ABCs**: `RulePlugin` for extensions (`isinstance` + `register`); composes via `get_evaluator` to avoid duplication. This enables runtime validation for third-party code: external classes can implement the shape and be registered virtually, passing `isinstance` without direct inheritance—key in a duck-typed language for pluggable systems.
- **Protocols**: `RuleEvaluator` provides static hints—mypy verifies structural compatibility (e.g., accepts `LambdaRule`).
- **One per Role**: Evaluation: Protocol + duck. Registration: ABC. No overlap in core flow.
- **Superiority**: Decouples consumers from concretes; extensible via registration. Versus baseline: Prevents mismatches via hints/enforcement.

## 3. Integrating into Responsibilities: Orchestrator Flow

Integrate into M02C18's `RuleEvaluationUseCase`: Accept `List[RuleEvaluator]` for static hints + duck dispatch; plugin loader enforces ABC, returning Protocol-satisfying evaluators. Domain remains pure; ports unaffected. Aligns with M02C16's evaluator via Protocol.

```python
# interface_monitor.py (application/use_cases.py extension)
from __future__ import annotations
from typing import List
from interface_model import RuleEvaluator, RulePlugin, create_domain_rule, create_plugin  # Interfaces
from semantic_types_model import Metric, RuleEvaluation, Threshold  # Consistent

class RuleEvaluationUseCase:
    """Use case: Depends on Protocol (static + duck); no ABC in core."""

    def __init__(self, rules: List[RuleEvaluator]):  # Static hint
        self._rules = rules  # Mypy verifies shapes

    def evaluate(self, metrics: List[Metric]) -> List[RuleEvaluation]:
        all_evals = []
        for rule in self._rules:
            all_evals.extend(rule.evaluate(metrics))  # Duck dispatch
        return all_evals

# Plugin loader: ABC enforcement for registration role
class PluginLoader:
    """Extension: Registers/enforces ABC."""

    def __init__(self):
        self._plugins = []

    def register(self, plugin: object):
        if not isinstance(plugin, RulePlugin):
            raise TypeError(f"Must satisfy RulePlugin: {plugin}")
        self._plugins.append(plugin)

    def load_rules(self) -> List[RuleEvaluator]:
        return [p.get_evaluator() for p in self._plugins]  # ABC → Protocol

# Wiring: Core (duck + Protocol) + plugins (ABC adapters)
def create_orchestrator_with_interfaces(threshold: Threshold):
    from application.use_cases import MonitoringUseCase  # M02C16
    from application.ports import MetricFetchPort, AlertPersistencePort, AlertNotifierPort
    from infrastructure.adapters import HttpMetricAdapter, InMemoryAlertRepository, ConsoleAlertNotifier
    # Infra (illustrative)
    fetch_adapter: MetricFetchPort = HttpMetricAdapter()
    persistence_adapter: AlertPersistencePort = InMemoryAlertRepository()
    notifier_adapter: AlertNotifierPort = ConsoleAlertNotifier()
    # Domain: Core (Protocol satisfaction)
    core_rules = [
        create_domain_rule("threshold", threshold),
        create_domain_rule("lambda_debug", threshold)  # Duck example
    ]
    # Plugins: ABC registration
    loader = PluginLoader()
    rate_threshold = Threshold(0.1)
    loader.register(create_plugin("rate", rate_threshold))  # Adapter
    loader.register(create_plugin("third_party_rate", rate_threshold))  # Registered
    plugin_rules = loader.load_rules()  # ABC → Protocol
    all_rules = core_rules + plugin_rules
    evaluator = RuleEvaluationUseCase(all_rules)  # Protocol hint
    use_case = MonitoringUseCase(fetch_adapter, persistence_adapter, notifier_adapter, evaluator)
    return use_case
```

**Benefits Demonstrated**:
- **Decoupling**: Use case uses Protocol hints; loader enforces ABC—structural acceptance.
- **Layer Integrity**: Domain interfaces verified statically; application dispatches via duck.
- **Extensibility**: ABC registration supports third-parties; core flow unintruded.

## 4. Tests: Verifying Interface Enforcement and Polymorphism

Tests affirm static hints (mypy simulation), runtime checks (`isinstance` for ABC), duck dispatch, and rejections. (Note: Relies on `semantic_types_model` for semantics; in full codebase, runs via `python -m unittest`.)

```python
# test_interface_model.py
import unittest
from typing import List
from unittest.mock import Mock
from interface_model import (
    RuleEvaluator, RulePlugin, create_domain_rule, create_plugin,
    LambdaRule, PluginAdapter, ThirdPartyRateRule
)
from interface_monitor import RuleEvaluationUseCase, PluginLoader
from semantic_types_model import RuleEvaluation, RuleType, Metric, Threshold

class TestInterfaces(unittest.TestCase):

    def setUp(self):
        self.metrics = [Metric(1, "cpu", 0.9), Metric(2, "cpu", 1.1)]
        self.threshold = Threshold(0.85)
        self.rate_threshold = Threshold(0.1)

    def test_duck_typing_internal(self):
        # Duck: Shape dispatches for internals
        threshold_rule = create_domain_rule("threshold", self.threshold)
        evals = threshold_rule.evaluate(self.metrics)
        self.assertEqual(len(evals), 2)
        self.assertEqual(evals[0].rule, RuleType("threshold"))

    def test_protocol_structural_satisfaction(self):
        # Protocol: Static hint accepts structural (e.g., LambdaRule)
        # Simulation: rules: List[RuleEvaluator] = [ThresholdRule(...), LambdaRule(...)]  # Mypy OK
        # vs. mismatch: BadRule()  # Mypy error: missing evaluate/rule_type
        lambda_rule = LambdaRule(RuleType("debug"), lambda ms: ms[:1])
        evals = lambda_rule.evaluate(self.metrics)
        self.assertEqual(len(evals), 1)  # First metric only
        self.assertEqual(evals[0].rule, RuleType("debug"))
        # Runtime structural check
        self.assertTrue(isinstance(lambda_rule, RuleEvaluator))

    def test_abc_runtime_enforce_and_register(self):
        # ABC: isinstance + register for third-party
        rate_plugin = create_plugin("rate", self.rate_threshold)
        self.assertIsInstance(rate_plugin, RulePlugin)
        third_party = ThirdPartyRateRule(self.rate_threshold)
        self.assertIsInstance(third_party, RulePlugin)  # Via register

    def test_adapter_composition(self):
        # Adapter: Composes without duplication
        inner = create_domain_rule("rate", self.rate_threshold)
        adapter = PluginAdapter(inner, "test")
        self.assertEqual(adapter.plugin_name, "test")
        evals = adapter.get_evaluator().evaluate(self.metrics)
        self.assertEqual(len(evals), 1)  # Second metric triggers

    def test_use_case_enforcement(self):
        # Use case: Protocol hint + duck (mixed shapes)
        rules = [
            create_domain_rule("threshold", self.threshold),
            LambdaRule(RuleType("custom"), lambda ms: [ms[0]]),
            create_plugin("rate", self.rate_threshold).get_evaluator()  # Via ABC
        ]
        use_case = RuleEvaluationUseCase(rules)
        evals = use_case.evaluate(self.metrics)
        self.assertEqual(len(evals), 4)  # Aggregated dispatch

    def test_plugin_loader_rejection(self):
        # Loader: Enforces ABC, rejects non-conformant
        loader = PluginLoader()
        good_plugin = create_plugin("rate", self.rate_threshold)
        loader.register(good_plugin)
        self.assertEqual(len(loader._plugins), 1)
        bad_obj = object()  # No RulePlugin
        with self.assertRaises(TypeError):
            loader.register(bad_obj)

    def test_polymorphism_no_mixing(self):
        # Roles separated: Protocol for eval, ABC for load
        core_rules = [create_domain_rule("threshold", self.threshold)]  # Duck + Protocol
        loader = PluginLoader()
        loader.register(create_plugin("third_party_rate", self.rate_threshold))  # ABC
        plugin_rules = loader.load_rules()  # → Protocol
        all_rules = core_rules + plugin_rules
        evals_list = [r.evaluate(self.metrics) for r in all_rules]
        self.assertEqual(len(evals_list[0]), 2)  # Threshold
        self.assertEqual(len(evals_list[1]), 1)  # Third-party rate
```

**Execution Note**: In the full codebase (with `semantic_types_model`), `python -m unittest test_interface_model.py` passes, verifying enforcement, structural polymorphism, and role separation.

## Practical Guidelines

- **Duck Typing**: Internals/simple shapes; runtime dispatch, no overhead.
- **ABCs**: Extensions/runtime (`register` for structural `isinstance`); use for third-party pluggability.
- **Protocols**: Static hints (`Protocol`); mypy ensures shapes without inheritance.
- **One per Role**: Evaluation? Duck + Protocol. Registration? ABC. Audit for mixing; supersets via composition.
- **Domain Fit**: Evaluators: Protocol hints; loaders: ABC enforcement.

**Impacts on Design**:
- **Decoupling**: Depend on shapes/contracts, not implementations.
- **Extensibility**: Structural plugins via registration; static safety via Protocols.

## Exercises for Mastery

1. **Interface CRC**: Define `EvaluationSink` Protocol for outputs; map use case interactions.
2. **Enforcement Audit**: Inject mismatched shape into `List[RuleEvaluator]`; verify mypy/runtime errors.
3. **Style Mix Simulation**: Apply ABC to core evaluation; refactor to Protocol + duck, measure test/maintenance gains.

This core prescribes interfaces for Module 2. Core 20 refactors the layered architecture with roles and hierarchies.
